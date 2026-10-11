#!/usr/bin/env python3
"""Mise à l'écart contrôlée des fichiers du serveur OVH absents du site.

Usage : python outils/ecarter_ovh.py apercu|deplacer

Lit la liste exacte `a-ecarter.tsv` (chemin, empreinte SHA-256 relevée par
la sauvegarde du 11 octobre 2026). Pour chaque fichier :
  - s'il a disparu ou si son empreinte a changé depuis la sauvegarde, il
    est laissé en place et signalé ;
  - sinon, en mode « deplacer », il est déplacé (jamais supprimé) dans
    <dossier personnel OVH>/mametas-hors-ligne/2026-10-11/<chemin>,
    c'est-à-dire hors du dossier web : il n'est plus accessible en ligne
    mais reste récupérable à tout moment.
Les dossiers devenus vides dans le dossier web sont retirés (uniquement
s'ils sont vides). En mode « apercu », rien n'est modifié.
"""
import hashlib
import os
import posixpath
import stat
import sys
from pathlib import PurePosixPath

import paramiko

ARCHIVE_DIR = "mametas-hors-ligne/2026-10-11"


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


def sha(sftp, path):
    h = hashlib.sha256()
    with sftp.open(path, "rb") as fh:
        fh.prefetch()
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def mkdirs(sftp, path):
    current = "/"
    for part in PurePosixPath(path).parts[1:]:
        current = posixpath.join(current, part)
        try:
            sftp.stat(current)
        except IOError:
            sftp.mkdir(current)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "apercu"
    if mode not in ("apercu", "deplacer"):
        sys.exit("mode inconnu")
    rows = [line.split("\t") for line in open("a-ecarter.tsv", encoding="utf-8").read().splitlines()[1:]]
    client, sftp, home, root = connect()
    archive = posixpath.join(home, ARCHIVE_DIR)
    if root.rstrip("/") == home.rstrip("/") or archive.startswith(root.rstrip("/") + "/"):
        sys.exit("Le dossier d'archive serait accessible en ligne : arrêt, rien n'est déplacé.")
    moved, skipped, report = 0, 0, []
    dirs = set()
    try:
        for rel, expected in rows:
            src = posixpath.join(root, rel)
            try:
                attr = sftp.stat(src)
            except IOError:
                report.append(f"déjà absent : {rel}")
                skipped += 1
                continue
            if not stat.S_ISREG(attr.st_mode or 0) or sha(sftp, src) != expected:
                report.append(f"MODIFIÉ depuis la sauvegarde, laissé en place : {rel}")
                skipped += 1
                continue
            if mode == "deplacer":
                dst = posixpath.join(archive, rel)
                mkdirs(sftp, posixpath.dirname(dst))
                sftp.rename(src, dst)
                d = posixpath.dirname(rel)
                while d:
                    dirs.add(d)
                    d = posixpath.dirname(d)
            report.append(("déplacé : " if mode == "deplacer" else "à déplacer : ") + rel)
            moved += 1
        removed_dirs = 0
        if mode == "deplacer":
            for d in sorted(dirs, key=lambda x: -x.count("/")):
                try:
                    if not sftp.listdir(posixpath.join(root, d)):
                        sftp.rmdir(posixpath.join(root, d))
                        removed_dirs += 1
                except IOError:
                    pass
    finally:
        client.close()
    head = (f"{'Déplacés' if mode == 'deplacer' else 'À déplacer'} : {moved} ; laissés en place : {skipped}"
            + (f" ; dossiers vides retirés : {removed_dirs}" if mode == "deplacer" else "")
            + f" ; destination : ~/{ARCHIVE_DIR}")
    print(head)
    for line in report:
        print("  " + line)
    if os.environ.get("GITHUB_ACTIONS") == "true":
        print("::notice title=Mise à l'écart OVH (" + mode + ")::" + head)
        kept = [line for line in report if not line.startswith(("à déplacer", "déplacé"))]
        if kept:
            print("::warning title=Laissés en place::" + "%0A".join(kept[:200]))
        if os.environ.get("GITHUB_STEP_SUMMARY"):
            with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as fh:
                fh.write(f"### Mise à l'écart OVH ({mode})\n\n{head}\n\n" + "\n".join(f"- {l}" for l in report) + "\n")


if __name__ == "__main__":
    main()
