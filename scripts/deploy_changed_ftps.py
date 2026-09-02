#!/usr/bin/env python3
"""Deploy Mametas public files to OVH over SFTP.

Default behaviour is intentionally conservative:
- validates required OVH secrets before connecting;
- uploads only added/modified public files;
- never deletes remote files automatically;
- excludes repository-only material (docs, scripts, data, workflows, archives).

For controlled maintenance jobs, MAMETAS_FORCE_FILES can contain a semicolon-separated
list of public paths to upload regardless of the current git diff.
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


def files_to_upload() -> tuple[list[str], list[str]]:
    forced = os.environ.get("MAMETAS_FORCE_FILES", "").strip()
    if not forced:
        return changed_files()

    uploads = []
    for raw in forced.split(";"):
        rel = raw.strip().lstrip("./")
        if not rel:
            continue
        if not is_public(rel):
            raise RuntimeError(f"Forced path is not an allowed public file: {rel}")
        if not (ROOT / rel).is_file():
            raise RuntimeError(f"Forced public file does not exist: {rel}")
        uploads.append(rel)
    return sorted(set(uploads)), []


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


def main() -> int:
    uploads, deletions = files_to_upload()
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

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=required["OVH_FTP_SERVER"],
        port=22,
        username=required["OVH_FTP_USERNAME"],
        password=required["OVH_FTP_PASSWORD"],
        timeout=45,
        banner_timeout=45,
        auth_timeout=45,
        look_for_keys=False,
        allow_agent=False,
    )

    try:
        sftp = client.open_sftp()
        try:
            home = sftp.normalize(".")
            print("Connected to OVH over SFTP.")
            for rel in uploads:
                local = ROOT / rel
                remote_dir = posixpath.dirname(rel)
                ensure_dir(sftp, home, required["OVH_FTP_ROOT"], remote_dir)
                remote_name = posixpath.basename(rel)
                sftp.put(str(local), remote_name)
                print(f"Uploaded {rel}")
        finally:
            sftp.close()
    finally:
        client.close()

    print("Mametas SFTP deployment completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
