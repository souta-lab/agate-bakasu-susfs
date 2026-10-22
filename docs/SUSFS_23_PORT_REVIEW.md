# SUSFS 2.3.0 / Linux 4.14 compatibility preflight

Current status: **not ported or built**. This isolated branch is a read-only
compatibility preflight. The BakaSU + SUSFS v1.5.5 build-tested branch is unchanged.

The original SUSFS 2.3.0 source was examined at upstream commit
f43926dc94b8ffbf9b74321313536600f69367b1 (2026-10-19), from the
gki-android12-5.10 branch. The agate kernel source is 4.14.336.

## Measured compatibility blockers

1. The original patch set targets Linux 5.10 and fails to apply to many
   changed Linux 4.14 vendor files. It is not a drop-in replacement.
2. The upstream code references fsnotify handle_inode_event; the 4.14 vendor
   fsnotify interface has handle_event. The callbacks have different
   signatures and lock and ownership requirements.
3. The upstream patch expects fs/proc/bootconfig.c, missing in this 4.14 tree.
4. The original SUSFS checkout includes a GPL-3.0 LICENSE while this kernel
   is GPL-2.0-only. Redistribution of combined source/binaries requires an
   explicit license-compatibility and copyright-holder authorization review.

## Repeat the PC-only test

    python3 tools/audit_susfs23_kernel_api.py --kernel . --upstream /path/to/susfs-2.3.0

This does not edit source, enable any hiding/evasion mechanisms, run ADB,
compile or flash a device.

## Existing working branch

The bakasu-susfs-4.14 branch remains on SUSFS v1.5.5, with prior
boot evidence and a separate signed memcg LRU accounting source patch.
It should not be labeled as v2.x without actual integration.
