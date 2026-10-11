#!/usr/bin/env python3
"""Publication du dossier site/ vers l'hébergement OVH, sans dérive possible.

Usage :
  python outils/publier_ovh.py plan                    liste ce qui partirait, n'envoie rien
  python outils/publier_ovh.py envoyer --sauvegarde D  envoie les différences, garde les anciennes versions dans D
  python outils/publier_ovh.py verifier                vérifie que la production est identique à site/

Principe : on compare chaque fichier de site/ à ce que le site sert
réellement (empreinte SHA-256 lue en HTTPS, ou par SFTP pour les fichiers
que le serveur ne sert pas tels quels : .htaccess, adresses redirigées).
Seuls les fichiers différents ou absents sont envoyés. Rien n'est jamais
supprimé sur le serveur. Une publication interrompue est simplement
complétée par la suivante.

Variables d'environnement : OVH_FTP_SERVER, OVH_FTP_USERNAME,
OVH_FTP_PASSWORD, OVH_FTP_ROOT (secrets GitHub, nécessaires pour l'envoi et
pour lire par SFTP) ; MAMETAS_URL (défaut https://www.mametas.com).
"""
from __future__ import annotations

import argparse
import hashlib
import os
import posixpath
import secrets
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parents[1]
SITE = REPO / "site"
BASE_URL = os.environ.get("MAMETAS_URL", "https://www.mametas.com").rstrip("/")
USER_AGENT = "MametasPublication/1.0 (+https://www.mametas.com)"


# ---------------------------------------------------------------- local side
def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def local_files() -> dict[str, str]:
    files = {}
    for path in sorted(SITE.rglob("*")):
        if path.is_file():
            files[path.relative_to(SITE).as_posix()] = sha256_bytes(path.read_bytes())
    return files


def upload_rank(rel: str) -> int:
    """Assets first, then pages, then sitemaps/robots, server rules last."""
    name = PurePosixPath(rel).name
    if name == ".htaccess":
        return 3
    if rel.endswith((".xml", ".txt")) and "/" not in rel:
        return 2
    if rel.endswith(".html"):
        return 1
    return 0


# --------------------------------------------------------------- HTTP side
class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


_OPENER = urllib.request.build_opener(_NoRedirect)


def http_state(rel: str, nonce: str) -> tuple[str, str | int]:
    """('sha', hex) when served as is, else ('status', code) or ('error', text)."""
    url = f"{BASE_URL}/{urllib.parse.quote(rel)}?publication={nonce}"
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT, "Cache-Control": "no-cache", "Pragma": "no-cache"})
    last = ""
    for attempt in range(4):
        try:
            with _OPENER.open(req, timeout=60) as resp:
                return "sha", sha256_bytes(resp.read())
        except urllib.error.HTTPError as exc:
            if exc.code >= 500:
                last = f"HTTP {exc.code}"
            else:
                return "status", exc.code
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as exc:
            last = type(exc).__name__
        time.sleep(2 * (attempt + 1))
    return "error", last


# --------------------------------------------------------------- SFTP side
def sftp_configured() -> bool:
    return all(os.environ.get(k, "").strip() for k in
               ("OVH_FTP_SERVER", "OVH_FTP_USERNAME", "OVH_FTP_PASSWORD", "OVH_FTP_ROOT"))


class Remote:
    """SFTP session on the OVH web root, reopened transparently when OVH drops it."""

    def __init__(self):
        import paramiko  # noqa: F401  (imported here so `plan` works without it)
        self.client = None
        self.sftp = None
        self.root = None

    def open(self):
        import paramiko
        self.close()
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=os.environ["OVH_FTP_SERVER"].strip(),
            port=int(os.environ.get("OVH_FTP_PORT", "22") or 22),
            username=os.environ["OVH_FTP_USERNAME"].strip(),
            password=os.environ["OVH_FTP_PASSWORD"],
            timeout=45, banner_timeout=45, auth_timeout=45,
            look_for_keys=False, allow_agent=False)
        self.client, self.sftp = client, client.open_sftp()
        home = self.sftp.normalize(".")
        parts = [p for p in PurePosixPath(os.environ["OVH_FTP_ROOT"].strip().strip("/")).parts
                 if p not in ("", ".")]
        self.root = posixpath.join(home, *parts) if parts else home

    def close(self):
        for obj in (self.sftp, self.client):
            try:
                if obj is not None:
                    obj.close()
            except Exception:
                pass
        self.client = self.sftp = None

    def ensure(self):
        if self.sftp is None:
            self.open()

    def path(self, rel: str) -> str:
        return posixpath.join(self.root, rel)

    def retry(self, fn, *args):
        last = None
        for attempt in range(4):
            try:
                self.ensure()
                return fn(*args)
            except FileNotFoundError:
                raise
            except Exception as exc:  # OVH may drop long sessions
                last = exc
                self.close()
                time.sleep(2 * (attempt + 1))
        raise last

    def sha(self, rel: str) -> str | None:
        def _read():
            try:
                with self.sftp.open(self.path(rel), "rb") as fh:
                    fh.prefetch()
                    return sha256_bytes(fh.read())
            except FileNotFoundError:
                return None
            except IOError as exc:
                if getattr(exc, "errno", None) == 2:
                    return None
                raise
        return self.retry(_read)

    def download(self, rel: str, dest: Path) -> bool:
        def _get():
            try:
                self.sftp.stat(self.path(rel))
            except FileNotFoundError:
                return False
            except IOError as exc:
                if getattr(exc, "errno", None) == 2:
                    return False
                raise
            dest.parent.mkdir(parents=True, exist_ok=True)
            self.sftp.get(self.path(rel), str(dest))
            return True
        return self.retry(_get)

    def _mkdirs(self, rel_dir: str):
        current = self.root
        for part in PurePosixPath(rel_dir).parts:
            current = posixpath.join(current, part)
            try:
                self.sftp.stat(current)
            except IOError:
                self.sftp.mkdir(current)

    def upload(self, rel: str, local: Path):
        def _put():
            self._mkdirs(posixpath.dirname(rel))
            final = self.path(rel)
            tmp = posixpath.join(posixpath.dirname(final), f".{posixpath.basename(final)}.publication")
            self.sftp.put(str(local), tmp)
            try:
                self.sftp.posix_rename(tmp, final)
            except IOError:
                try:
                    self.sftp.remove(final)
                except IOError:
                    pass
                self.sftp.rename(tmp, final)
        return self.retry(_put)


# --------------------------------------------------------------- comparison
def compare(local: dict[str, str], remote: Remote | None) -> list[dict]:
    nonce = secrets.token_hex(6)
    rels = sorted(local)
    with ThreadPoolExecutor(max_workers=8) as pool:
        states = dict(zip(rels, pool.map(lambda r: http_state(r, nonce), rels)))
    rows = []
    for rel in rels:
        kind, value = states[rel]
        row = {"rel": rel, "local": local[rel], "via": "https", "remote": None, "note": ""}
        if kind == "sha":
            row["remote"] = value
        else:
            row["note"] = f"HTTPS {value}"
            if remote is not None:
                row["via"] = "sftp"
                row["remote"] = remote.sha(rel)
                if row["remote"] is None:
                    row["remote"] = "absent"
            else:
                row["remote"] = "inconnu"
        if row["remote"] == row["local"]:
            row["etat"] = "identique"
        elif row["remote"] == "absent":
            row["etat"] = "absent en ligne"
        elif row["remote"] == "inconnu":
            row["etat"] = "non vérifiable sans accès SFTP"
        else:
            row["etat"] = "différent"
        rows.append(row)
    return rows


# --------------------------------------------------------------- reporting
def _esc(text: str) -> str:
    return text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def annotate(level: str, title: str, lines: list[str]):
    if os.environ.get("GITHUB_ACTIONS") == "true":
        print(f"::{level} title={title}::" + _esc("\n".join(lines[:300])), flush=True)


def summary(markdown: str):
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(markdown + "\n")


def report(rows: list[dict], title: str) -> list[dict]:
    todo = [r for r in rows if r["etat"] != "identique"]
    same = len(rows) - len(todo)
    head = f"{title} : {len(rows)} fichiers dans site/, {same} identiques en production, {len(todo)} à traiter"
    print(head)
    lines = [f"{r['etat']} : {r['rel']}" + (f" ({r['note']}, lu par {r['via']})" if r['note'] else "")
             for r in todo]
    for line in lines:
        print("  " + line)
    annotate("notice", title.replace(":", " ").replace(",", " "), [head] + lines)
    md = [f"### {title}", "", head, ""]
    if todo:
        md += ["| Fichier | État |", "| --- | --- |"] + [f"| `{r['rel']}` | {r['etat']} |" for r in todo[:300]]
    summary("\n".join(md))
    return todo


# --------------------------------------------------------------- commands
def cmd_plan(args) -> int:
    remote = None
    if sftp_configured():
        remote = Remote()
    else:
        print("Accès SFTP non configuré : les fichiers non servis tels quels resteront non vérifiés.")
    try:
        rows = compare(local_files(), remote)
    finally:
        if remote:
            remote.close()
    report(rows, "Plan de publication")
    return 0


def cmd_envoyer(args) -> int:
    if not sftp_configured():
        print("Envoi impossible : secrets OVH absents.", file=sys.stderr)
        return 1
    remote = Remote()
    try:
        rows = compare(local_files(), remote)
        todo = report(rows, "Fichiers à publier")
        if not todo:
            print("Rien à publier : la production est déjà identique à site/.")
            return 0
        unknown = [r for r in todo if r["etat"] == "non vérifiable sans accès SFTP"]
        if unknown:
            print("État inconnu pour certains fichiers, envoi annulé.", file=sys.stderr)
            return 1
        backup = Path(args.sauvegarde) if args.sauvegarde else None
        if backup:
            kept = 0
            for r in todo:
                if r["etat"] == "différent" and remote.download(r["rel"], backup / r["rel"]):
                    kept += 1
            print(f"Anciennes versions conservées avant remplacement : {kept}")
        for r in sorted(todo, key=lambda r: (upload_rank(r["rel"]), r["rel"])):
            remote.upload(r["rel"], SITE / r["rel"])
            print(f"Envoyé : {r['rel']}", flush=True)
        print(f"Publication terminée : {len(todo)} fichier(s) envoyé(s), aucun supprimé.")
        return 0
    finally:
        remote.close()


def cmd_verifier(args) -> int:
    remote = Remote() if sftp_configured() else None
    try:
        rows = compare(local_files(), remote)
    finally:
        if remote:
            remote.close()
    todo = report(rows, "Vérification de la production")
    if todo:
        annotate("error", "Production différente de site/", [f"{r['etat']} : {r['rel']}" for r in todo])
        return 1
    print("Production vérifiée : chaque fichier de site/ est servi à l'identique.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("plan")
    env = sub.add_parser("envoyer")
    env.add_argument("--sauvegarde", help="dossier où conserver les versions remplacées")
    sub.add_parser("verifier")
    args = parser.parse_args()
    return {"plan": cmd_plan, "envoyer": cmd_envoyer, "verifier": cmd_verifier}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
