from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTENSIONS = {".html", ".js", ".css", ".json", ".xml", ".md"}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv"}

changed = 0
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
        continue
    if any(part in SKIP_DIRS for part in path.parts):
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    updated = (
        text
        .replace(" — ", " - ")
        .replace(" – ", " - ")
        .replace("—", "-")
        .replace("–", "-")
        .replace(
            "Les lieux sont réels. Les cinq matriarches sont fictives. Le point de vue, lui, est bien vivant.",
            "Guide indépendant créé par un Niçois. Des lieux réels, des choix documentés, et un point de vue bien vivant."
        )
        .replace(
            "The places are real. The five matriarchs are fictional. The point of view is very much alive.",
            "Independent guide created by a Niçois. Real places, researched choices and a point of view that is very much alive."
        )
    )
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        changed += 1

print(f"Short-dash house style applied to {changed} file(s).")
