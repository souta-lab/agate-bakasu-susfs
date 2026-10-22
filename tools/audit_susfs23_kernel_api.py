#!/usr/bin/env python3
"""Read-only source/license/API compatibility preflight, no device actions."""
from pathlib import Path
import argparse
import json
import re


def kernel_version(root):
    text = (root / "Makefile").read_text()
    values = []
    for label in ("VERSION", "PATCHLEVEL", "SUBLEVEL"):
        m = re.search(rf"^{label}\s*=\s*(\d+)\s*$", text, re.M)
        if not m:
            raise ValueError(f"Missing kernel {label}")
        values.append(m.group(1))
    return ".".join(values)


def susfs_version(path):
    text = path.read_text()
    m = re.search(r'^#define\s+SUSFS_VERSION\s+"([^"]+)"', text, re.M)
    return m.group(1) if m else "unknown"


def license_series(root):
    p = root / "LICENSE"
    if not p.exists():
        return "unspecified"
    s = p.read_text(errors="replace", encoding="utf-8")[:400]
    m = re.search(r"Version\s+(\d+),", s)
    return f"GPL-{m.group(1)}" if m else "manual-review"


def report(kernel, upstream):
    head = upstream / "kernel_patches" / "include" / "linux" / "susfs.h"
    source = upstream / "kernel_patches" / "fs" / "susfs.c"
    if not head.is_file() or not source.is_file():
        raise ValueError("Missing upstream source files")
    fsnotify = (kernel / "include" / "linux" / "fsnotify_backend.h").read_text()
    new_susfs = source.read_text()
    checks = {
        "kernel_v4_14": kernel_version(kernel).startswith("4.14."),
        "fsnotify_handle_inode_event_available":
            "handle_inode_event" in fsnotify,
        "v2_source_requires_handle_inode_event":
            ".handle_inode_event" in new_susfs,
        "proc_bootconfig_available": (kernel / "fs/proc/bootconfig.c").exists(),
        "upstream_patch_android_5_10":
            (upstream / "kernel_patches/50_add_susfs_in_gki-android12-5.10.patch").exists(),
    }
    return {
        "kernel_version": kernel_version(kernel),
        "installed_susfs": susfs_version(kernel / "include/linux/susfs.h"),
        "candidate_susfs": susfs_version(head),
        "upstream_license": license_series(upstream),
        "kernel_license": "GPL-2.0-only (verify distribution rights)",
        "checks": checks,
        "assessment": "Needs source/API backport, compatibility review; not built or boot tested",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", required=True, type=Path)
    ap.add_argument("--upstream", required=True, type=Path)
    args = ap.parse_args()
    print(json.dumps(report(args.kernel, args.upstream), indent=2))


if __name__ == "__main__":
    main()
