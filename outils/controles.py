#!/usr/bin/env python3
"""Lance tous les contrôles bloquants avant publication.

Usage : python outils/controles.py

Code de sortie 0 si tout est conforme, 1 sinon. Les circuits de validation
et de publication l'appellent avant tout envoi vers OVH.
"""
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SITE = REPO / "site"
FORBIDDEN_SUFFIXES = {".py", ".pyc", ".zip", ".b64", ".yml", ".yaml", ".sh"}

CHECKS = [
    ("Syntaxe, pages, liens internes, SEO de base", [sys.executable, "outils/controles/controle_site.py"]),
    ("Affiliation Booking via CJ", [sys.executable, "outils/controles/controle_affiliation_booking.py"]),
    ("Structure des hubs d'hôtels", [sys.executable, "outils/controles/controle_hubs_hotels.py"]),
    ("Autotest du moteur Riviera Fit", ["node", "site/assets/riviera-chooser.js", "--self-test"]),
]


def check_site_contents() -> list[str]:
    """site/ ne doit contenir que des fichiers publiables."""
    problems = []
    for path in sorted(SITE.rglob("*")):
        if path.is_file():
            rel = path.relative_to(SITE).as_posix()
            if path.suffix.lower() in FORBIDDEN_SUFFIXES or "/.git" in f"/{rel}":
                problems.append(rel)
    return problems


def main() -> int:
    failures = []
    stray = check_site_contents()
    print("== Contenu de site/ : uniquement des fichiers publiables")
    if stray:
        print("Fichiers non publiables dans site/ :")
        for rel in stray:
            print(f"- {rel}")
        failures.append("Contenu de site/")
    else:
        print("Conforme.")
    for label, cmd in CHECKS:
        print(f"\n== {label}", flush=True)
        result = subprocess.run(cmd, cwd=REPO)
        if result.returncode != 0:
            failures.append(label)
    print()
    if failures:
        print("CONTRÔLES EN ÉCHEC : " + " ; ".join(failures))
        return 1
    print(f"Tous les contrôles sont conformes ({len(CHECKS) + 1}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
