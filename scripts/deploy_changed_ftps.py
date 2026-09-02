#!/usr/bin/env python3
"""Deploy only changed public Mametas files to OVH over explicit FTPS.

The script is intentionally conservative:
- validates required OVH secrets before connecting;
- uploads added/modified public files only;
- never deletes remote files automatically;
- excludes repository-only material (docs, scripts, data, workflows, archives).
"""

from __future__ import annotations

import os
import posixpath
import ssl
import subprocess
import sys
from ftplib import FTP_TLS, error_perm
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]

EXCLUDED_PREFIXES = (
    ".git/",
    ".github/",
    "docs/",
    "scripts/",
    "data/",
    "lesnicoises-v8-no-mercy-update/",
    "lesnicoises-v8-no-mercy-update 2/",
)
EXCLUDED_NAMES = {
    "deploy-canary.txt",
    "README.md",
    "README-V22.txt",
    "README-V22.1.txt",
    "README-V22.3.txt",
    "README-V22_2.txt",
    "_V18-NOTES.txt",
    "_V19-NOTES.txt",
    "_V20-NOTES.txt",
}
EXCLUDED_SUFFIXES = (".zip",)


def is_public(path: str) -> bool:
    clean = path.lstrip("./")
    if not clean or clean in EXCLUDED_NAMES:
        return False
    if clean.startswith(EXCLUDED_PREFIXES):
        return False
    if clean.endswith(EXCLUDED_SUFFIXES):
        return False
    return True


def changed_files() -> tuple[list[str], list[str]]:
    after = os.environ.get("GITHUB_SHA", "").strip()
    before = os.environ.get("BEFORE_SHA", "").strip()
    if not after:
        raise RuntimeError("GITHUB_SHA is missing")
    if not before or set(before) == {"0"}:
        before = f"{after}^"

    output = subprocess.check_output(
        ["git", "diff", "--name-status", "--find-renames", before, after],
        cwd=ROOT,
        text=True,
    )
    uploads: list[str] = []
    deletions: list[str] = []
    for raw in output.splitlines():
        if not raw.strip():
            continue
        fields = raw.split("\t")
        status = fields[0]
        if status.startswith("R") and len(fields) >= 3:
            old, new = fields[1], fields[2]
            if is_public(old):
                deletions.append(old)
            if is_public(new):
                uploads.append(new)
        elif status.startswith("D") and len(fields) >= 2:
            if is_public(fields[1]):
                deletions.append(fields[1])
        elif len(fields) >= 2 and status[0] in {"A", "M", "C", "T"}:
            if is_public(fields[-1]):
                uploads.append(fields[-1])
    return sorted(set(uploads)), sorted(set(deletions))


def ensure_dir(ftp: FTP_TLS, remote_root: str, relative_dir: str) -> None:
    ftp.cwd("/")
    parts = [p for p in PurePosixPath(remote_root.strip("/")).parts if p not in {"", "."}]
    parts.extend(p for p in PurePosixPath(relative_dir).parts if p not in {"", "."})
    for part in parts:
        try:
            ftp.cwd(part)
        except error_perm:
            ftp.mkd(part)
            ftp.cwd(part)


def main() -> int:
    uploads, deletions = changed_files()
    print(f"Public files to upload: {len(uploads)}")
    for path in uploads:
        print(f"  + {path}")
    if deletions:
        print("Remote deletions intentionally skipped for safety:")
        for path in deletions:
            print(f"  - {path}")

    if not uploads:
        print("No public file changed; nothing to deploy.")
        return 0

    required = {
        "OVH_FTP_SERVER": os.environ.get("OVH_FTP_SERVER", "").strip(),
        "OVH_FTP_USERNAME": os.environ.get("OVH_FTP_USERNAME", "").strip(),
        "OVH_FTP_PASSWORD": os.environ.get("OVH_FTP_PASSWORD", ""),
        "OVH_FTP_ROOT": os.environ.get("OVH_FTP_ROOT", "").strip(),
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        print(
            "DEPLOYMENT SKIPPED: missing GitHub Actions secrets: " + ", ".join(missing),
            file=sys.stderr,
        )
        return 0

    context = ssl.create_default_context()
    ftp = FTP_TLS(context=context, timeout=45)
    ftp.connect(required["OVH_FTP_SERVER"], 21)
    ftp.login(required["OVH_FTP_USERNAME"], required["OVH_FTP_PASSWORD"])
    ftp.prot_p()
    ftp.set_pasv(True)

    try:
        for rel in uploads:
            local = ROOT / rel
            if not local.is_file():
                raise RuntimeError(f"Changed path is not a file: {rel}")
            remote_dir = posixpath.dirname(rel)
            ensure_dir(ftp, required["OVH_FTP_ROOT"], remote_dir)
            remote_name = posixpath.basename(rel)
            with local.open("rb") as handle:
                ftp.storbinary(f"STOR {remote_name}", handle)
            print(f"Uploaded {rel}")
    finally:
        try:
            ftp.quit()
        except Exception:
            ftp.close()

    print("Mametas FTPS deployment completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
