from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COPY_EXTENSIONS = {".html", ".json", ".xml", ".md"}
DYNAMIC_COPY = {
    "assets/riviera-chooser.js",
    "assets/hotel-engine.js",
}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv"}

def is_copy_file(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return path.suffix.lower() in COPY_EXTENSIONS or rel in DYNAMIC_COPY

changed = 0
checked = []
for path in ROOT.rglob("*"):
    if not path.is_file() or not is_copy_file(path):
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
    checked.append(path)

leftovers = []
for path in checked:
    text = path.read_text(encoding="utf-8")
    if "—" in text or "–" in text:
        leftovers.append(path.relative_to(ROOT).as_posix())

if leftovers:
    raise SystemExit("Long dashes remain in public copy:\n- " + "\n- ".join(leftovers))

print(f"Short-dash house style applied to {changed} copy file(s); {len(checked)} checked.")
