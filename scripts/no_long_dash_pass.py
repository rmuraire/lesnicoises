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
    )
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        changed += 1

print(f"Short-dash house style applied to {changed} file(s).")
