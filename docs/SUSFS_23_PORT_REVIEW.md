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

## Linux 4.14 fsnotify adapter (implemented, compile-tested)

A reusable prototype for the fsnotify callback ABI difference is now located at:
- include/linux/susfs23_fsnotify_compat_414.h
- fs/notify/susfs23_fsnotify_compat_414.c

Upstream SUSFS 2.3.0 targets fsnotify_ops.handle_inode_event, whereas the
vendor 4.14 ABI uses fsnotify_ops.handle_event with additional inode/mark,
data, name and iterator arguments. The adapter handles the 4.14 signature
and converts its NUL-terminated filename to the bounded qstr representation
used by newer callbacks.

This file is deliberately **not linked into the production kernel**. It is
a reusable API prototype with a no-op observer, not a functioning SUSFS 2.3
installation. It does not register watchers or manipulate mounts or files.

Compile-stage verification on the actual ARM64/4.14 vendor tree:

    make O=out ARCH=arm64 agate_defconfig
    make -j2 O=out ARCH=arm64 CC=clang LLVM=1 LLVM_IAS=1 \
      CROSS_COMPILE=aarch64-linux-gnu- CROSS_COMPILE_ARM32=arm-linux-gnueabi- \
      fs/notify/susfs23_fsnotify_compat_414.o

PASS: ELF64 AArch64 relocatable object generated, and 4 focused
source/invariant tests passed. This **does not** prove runtime callback
semantics or make the upstream 2.3 source license-compatible with GPLv2.

The compatibility qstr is hashed with full_name_hash(NULL, ...); callers must not use it for parent-salted dcache lookup because the 4.14 callback does not provide the parent dentry. The callback-owned pointer is only usable synchronously.\n
NAME_MAX-byte filenames are valid on Linux. The source probe reads at most NAME_MAX + 1 bytes to distinguish 255-byte valid names from over-limit names.\n