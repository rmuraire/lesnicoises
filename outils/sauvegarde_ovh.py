#!/usr/bin/env python3
"""Sauvegarde complète du dossier web OVH, en lecture seule.

Lit chaque fichier du dossier web par SFTP (aucune écriture, aucune
suppression, aucun renommage côté serveur), puis produit :
  - sauvegarde/www/...             copie fidèle du dossier web
  - inventaire.tsv                 chemin, taille, date, SHA-256 de chaque fichier
  - figees/...                     les images listées dans figees-attendues.tsv
  - figees/verification.tsv        leur empreinte comparée à celle relevée en production
  - rapport.md                     résumé lisible

Variables d'environnement : OVH_FTP_SERVER, OVH_FTP_USERNAME,
OVH_FTP_PASSWORD, OVH_FTP_ROOT (secrets GitHub existants), OVH_FTP_PORT (22).
"""
from __future__ import annotations

import hashlib
import os
import posixpath
import shutil
import stat
import sys
import time
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

import paramiko

OUT = Path("sauvegarde/www")


def connect():
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
    sftp = client.open_sftp()
    home = sftp.normalize(".")
    parts = [p for p in PurePosixPath(os.environ["OVH_FTP_ROOT"].strip().strip("/")).parts if p not in ("", ".")]
    root = posixpath.join(home, *parts) if parts else home
    return client, sftp, home, root


def walk(sftp, root):
    """Yield (relative path, attributes) for every regular file under root."""
    stack = [""]
    while stack:
        rel_dir = stack.pop()
        for attr in sorted(sftp.listdir_attr(posixpath.join(root, rel_dir)), key=lambda a: a.filename):
            rel = posixpath.join(rel_dir, attr.filename) if rel_dir else attr.filename
            mode = attr.st_mode or 0
            if stat.S_ISDIR(mode):
                stack.append(rel)
            elif stat.S_ISREG(mode):
                yield rel, attr
            else:
                print(f"Ignoré (ni fichier ni dossier) : {rel}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    client, sftp, home, root = connect()
    try:
        entries = list(walk(sftp, root))
        rows = []
        for i, (rel, attr) in enumerate(entries):
            dest = OUT / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            for attempt in range(4):
                try:
                    sftp.get(posixpath.join(root, rel), str(dest))
                    break
                except (OSError, EOFError, paramiko.SSHException):
                    if attempt == 3:
                        raise
                    try:
                        client.close()
                    except Exception:
                        pass
                    time.sleep(2 * (attempt + 1))
                    client, sftp, home, root = connect()
            size = dest.stat().st_size
            if size != attr.st_size:
                raise SystemExit(f"Taille incohérente pour {rel} : {size} != {attr.st_size}")
            mtime = datetime.fromtimestamp(attr.st_mtime or 0, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            rows.append((rel, size, mtime, sha256_file(dest)))
            if i and i % 100 == 0:
                print(f"{i} fichiers copiés", flush=True)
        root_is_home = root.rstrip("/") == home.rstrip("/")
    finally:
        client.close()

    with open("inventaire.tsv", "w", encoding="utf-8") as fh:
        fh.write("chemin\toctets\tmodifie_utc\tsha256\n")
        for rel, size, mtime, sha in sorted(rows):
            fh.write(f"{rel}\t{size}\t{mtime}\t{sha}\n")

    expected = {}
    for line in Path("figees-attendues.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        rel, prefix, size = line.split("\t")
        expected[rel] = (prefix, int(size))
    by_rel = {r[0]: r for r in rows}
    checks = []
    for rel, (prefix, size) in sorted(expected.items()):
        row = by_rel.get(rel)
        if row is None:
            checks.append((rel, "absent du serveur"))
            continue
        target = Path("figees") / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(OUT / rel, target)
        ok = row[3].startswith(prefix) and row[1] == size
        checks.append((rel, "identique au relevé du 11 octobre" if ok else "DIFFÉRENT du relevé du 11 octobre"))
    Path("figees").mkdir(exist_ok=True)
    with open("figees/verification.tsv", "w", encoding="utf-8") as fh:
        fh.write("chemin\tresultat\n")
        for rel, res in checks:
            fh.write(f"{rel}\t{res}\n")

    total = sum(r[1] for r in rows)
    bad = [c for c in checks if not c[1].startswith("identique")]
    report = [
        "# Sauvegarde OVH du dossier web",
        "",
        f"- Date : {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"- Fichiers copiés : {len(rows)}",
        f"- Volume : {total / 1e6:.1f} Mo",
        f"- Dossier web à la racine de l'hébergement : {'oui' if root_is_home else 'non'}",
        f"- Images figées vérifiées : {len(checks) - len(bad)} sur {len(checks)}",
        "- Aucune écriture, suppression ni modification n'a été faite sur le serveur.",
    ]
    Path("rapport.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    if os.environ.get("GITHUB_ACTIONS") == "true":
        msg = "%0A".join(line.replace("%", "%25") for line in report[2:])
        print(f"::notice title=Sauvegarde OVH::{msg}")
        if bad:
            print("::warning title=Images figées::" + "%0A".join(f"{r} {s}" for r, s in bad))
    return 0


if __name__ == "__main__":
    sys.exit(main())
