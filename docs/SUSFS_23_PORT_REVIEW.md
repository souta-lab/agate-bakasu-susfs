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
## Generic Linux 4.14 fsnotify mark lifecycle bridge

The standalone ABI adapter now implements generic create-group, attach-mark,
detach-mark and destroy-group helpers, using the actual 4.14
fsnotify_add_mark(mark, inode, NULL, 0) signature instead of newer
fsnotify_add_inode_mark(mark, inode, 0).

The adapter's fsnotify_ops supplies a free_mark callback so the kernel mark
reaper can release dynamically allocated marks after SRCU synchronization.
The caller retains the initial mark reference; successful registration adds
a group-list reference and detach plus put releases both references in order.
Failed registration releases the initial reference through fsnotify_put_mark.

Neither watcher registration nor callbacks are activated during kernel boot
because this prototype remains unlinked from the normal vmlinux target. This
checks generic ABI and allocation lifecycle only; no SUSFS feature is
reported as implemented or tested.


### Opt-in link test

The upstream-inspired but GPL-2.0-authored generic fsnotify ABI adapter can
be conditionally linked with CONFIG_SUSFS23_FSNOTIFY_ABI_414. This option
depends on FSNOTIFY and ARM64, and defaults to disabled. It is not the 2.3
SUSFS implementation and has no automatic watcher registration.

To compile/link the prototype for kernel testing (PC only):

    make O=out ARCH=arm64 agate_defconfig
    scripts/config --file out/.config -e SUSFS23_FSNOTIFY_ABI_414
    make O=out ARCH=arm64 olddefconfig
    make O=out ARCH=arm64 ... fs/notify/built-in.o

This configuration is experimental and must not be confused with a
functional SUSFS 2.3.0 kernel.
