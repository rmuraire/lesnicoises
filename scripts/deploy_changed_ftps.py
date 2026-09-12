#!/usr/bin/env python3
"""Deploy Mametas public files to OVH over SFTP.

Uploads changed public files plus generated outputs that changed during the build.
A small set of hotel hub assets/pages is always included so a previously interrupted
hotel deployment can recover cleanly. A full HTML resync is available only when
MAMETAS_FULL_SYNC=1. Remote deletions remain disabled except for explicitly listed
stale deployment artifacts that must never live in the public webroot.
"""
from __future__ import annotations

import os
import posixpath
import subprocess
import sys
from pathlib import Path, PurePosixPath

import paramiko

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PREFIXES = (
    ".git/", ".github/", "docs/", "scripts/", "data/",
    "lesnicoises-v8-no-mercy-update/", "lesnicoises-v8-no-mercy-update 2/",
)
EXCLUDED_NAMES = {
    "deploy-canary.txt", "README.md", "README-V22.txt", "README-V22.1.txt",
    "README-V22.3.txt", "README-V22_2.txt", "_V18-NOTES.txt", "_V19-NOTES.txt", "_V20-NOTES.txt",
}
EXCLUDED_SUFFIXES = (".zip",)

HOTEL_RECOVERY_OUTPUTS = {
    "assets/hotel-batch.css",
    "assets/hotels/batch-sprite.svg",
    "robots.txt",
    "sitemap-hotels-batch3.xml",
    "hotels/index.html",
    "hotels/antibes/index.html",
    "hotels/beaulieu-sur-mer/index.html",
    "hotels/cannes/index.html",
    "hotels/menton/index.html",
    "hotels/monaco/index.html",
    "hotels/mougins/index.html",
    "hotels/saint-paul-de-vence/index.html",
    "hotels/saint-tropez/index.html",
    "hotels/villefranche-sur-mer/index.html",
    "en/hotels/index.html",
    "en/hotels/antibes/index.html",
    "en/hotels/beaulieu-sur-mer/index.html",
    "en/hotels/cannes/index.html",
    "en/hotels/menton/index.html",
    "en/hotels/monaco/index.html",
    "en/hotels/mougins/index.html",
    "en/hotels/saint-paul-de-vence/index.html",
    "en/hotels/saint-tropez/index.html",
    "en/hotels/villefranche-sur-mer/index.html",
}

STALE_REMOTE_FILES = (
    ".github/workflows/mametas-production.yml",
)


def normalize_rel(path: str) -> str:
    clean = path.strip()
    while clean.startswith("./"):
        clean = clean[2:]
    return clean.lstrip("/")


def is_public(path: str) -> bool:
    clean = normalize_rel(path)
    if not clean or clean in EXCLUDED_NAMES:
        return False
    if clean.startswith(EXCLUDED_PREFIXES):
        return False
    if clean.endswith(EXCLUDED_SUFFIXES):
        return False
    return True


def committed_changes() -> tuple[set[str], set[str]]:
    after = os.environ.get("GITHUB_SHA", "").strip()
    before = os.environ.get("BEFORE_SHA", "").strip()
    if not after:
        raise RuntimeError("GITHUB_SHA is missing")
    if not before or set(before) == {"0"}:
        before = f"{after}^"
    output = subprocess.check_output(
        ["git", "diff", "--name-status", "--find-renames", before, after], cwd=ROOT, text=True
    )
    uploads: set[str] = set()
    deletions: set[str] = set()
    for raw in output.splitlines():
        if not raw.strip():
            continue
        fields = raw.split("\t")
        status = fields[0]
        if status.startswith("R") and len(fields) >= 3:
            old, new = fields[1], fields[2]
            if is_public(old):
                deletions.add(normalize_rel(old))
            if is_public(new):
                uploads.add(normalize_rel(new))
        elif status.startswith("D") and len(fields) >= 2:
            if is_public(fields[1]):
                deletions.add(normalize_rel(fields[1]))
        elif len(fields) >= 2 and status[0] in {"A", "M", "C", "T"}:
            path = fields[-1]
            if is_public(path):
                uploads.add(normalize_rel(path))
    return uploads, deletions


def materialized_changes() -> set[str]:
    """Return any public output changed or created by materialization steps."""
    changed = subprocess.check_output(["git", "diff", "--name-only"], cwd=ROOT, text=True).splitlines()
    untracked = subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT, text=True
    ).splitlines()
    paths = {normalize_rel(p) for p in changed + untracked if p.strip()}
    return {
        p for p in paths
        if is_public(p) and (ROOT / p).is_file()
    }


def hotel_recovery_outputs() -> set[str]:
    return {
        p for p in HOTEL_RECOVERY_OUTPUTS
        if is_public(p) and (ROOT / p).is_file()
    }


def all_html_outputs() -> set[str]:
    """Return every public HTML file for explicit full-sync maintenance runs."""
    outputs: set[str] = set()
    for path in ROOT.rglob("*.html"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if is_public(rel):
            outputs.add(rel)
    if (ROOT / "sitemap.xml").is_file():
        outputs.add("sitemap.xml")
    return outputs


def files_to_upload() -> tuple[list[str], list[str]]:
    forced = os.environ.get("MAMETAS_FORCE_FILES", "").strip()
    if forced:
        uploads = []
        for raw in forced.split(";"):
            rel = normalize_rel(raw)
            if not rel:
                continue
            if not is_public(rel):
                raise RuntimeError(f"Forced path is not an allowed public file: {rel}")
            if not (ROOT / rel).is_file():
                raise RuntimeError(f"Forced public file does not exist: {rel}")
            uploads.append(rel)
        return sorted(set(uploads)), []

    uploads, deletions = committed_changes()
    uploads.update(materialized_changes())
    uploads.update(hotel_recovery_outputs())
    if os.environ.get("MAMETAS_FULL_SYNC", "").strip() == "1":
        uploads.update(all_html_outputs())
    return sorted(uploads), sorted(deletions)


def chdir_remote_root(sftp: paramiko.SFTPClient, home: str, remote_root: str) -> None:
    sftp.chdir(home)
    for part in [p for p in PurePosixPath(remote_root.strip("/")).parts if p not in {"", "."}]:
        sftp.chdir(part)


def ensure_dir(sftp: paramiko.SFTPClient, home: str, remote_root: str, relative_dir: str) -> None:
    sftp.chdir(home)
    parts = [p for p in PurePosixPath(remote_root.strip("/")).parts if p not in {"", "."}]
    parts.extend(p for p in PurePosixPath(relative_dir).parts if p not in {"", "."})
    for part in parts:
        try:
            sftp.chdir(part)
        except OSError:
            sftp.mkdir(part)
            sftp.chdir(part)


def remove_stale_remote_files(sftp: paramiko.SFTPClient, home: str, remote_root: str) -> None:
    chdir_remote_root(sftp, home, remote_root)
    for rel in STALE_REMOTE_FILES:
        try:
            sftp.remove(rel)
            print(f"Removed stale remote artifact {rel}")
        except OSError:
            print(f"Stale remote artifact already absent: {rel}")
    for rel_dir in (".github/workflows", ".github"):
        try:
            sftp.rmdir(rel_dir)
            print(f"Removed empty stale remote directory {rel_dir}")
        except OSError:
            pass


def main() -> int:
    uploads, deletions = files_to_upload()
    print(f"Public files to upload: {len(uploads)}")
    for path in uploads:
        print(f"  + {path}")
    if deletions:
        print("Remote deletions intentionally skipped for safety:")
        for path in deletions:
            print(f"  - {path}")

    required = {
        "OVH_FTP_SERVER": os.environ.get("OVH_FTP_SERVER", "").strip(),
        "OVH_FTP_USERNAME": os.environ.get("OVH_FTP_USERNAME", "").strip(),
        "OVH_FTP_PASSWORD": os.environ.get("OVH_FTP_PASSWORD", ""),
        "OVH_FTP_ROOT": os.environ.get("OVH_FTP_ROOT", "").strip(),
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        print("DEPLOYMENT SKIPPED: missing GitHub Actions secrets: " + ", ".join(missing), file=sys.stderr)
        return 0

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=required["OVH_FTP_SERVER"], port=22, username=required["OVH_FTP_USERNAME"],
        password=required["OVH_FTP_PASSWORD"], timeout=45, banner_timeout=45, auth_timeout=45,
        look_for_keys=False, allow_agent=False,
    )
    try:
        sftp = client.open_sftp()
        try:
            home = sftp.normalize(".")
            print("Connected to OVH over SFTP.")
            remove_stale_remote_files(sftp, home, required["OVH_FTP_ROOT"])
            for rel in uploads:
                local = ROOT / rel
                ensure_dir(sftp, home, required["OVH_FTP_ROOT"], posixpath.dirname(rel))
                sftp.put(str(local), posixpath.basename(rel))
                print(f"Uploaded {rel}")
        finally:
            sftp.close()
    finally:
        client.close()
    print("Mametas SFTP deployment completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
