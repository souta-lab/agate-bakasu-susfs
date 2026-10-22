# Porting notes and revision history

## Source identity and attribution

Device: Xiaomi 11T / agate (fastboot product amber); Linux 4.14.336 on MT6893.

Base kernel snapshot: Scaffold47/agate-ksun-susfs commit a94c15b31dc0 (Xiaomi MT6893 source). GitHub project independent from that source repository; not described as Hydrogen-based. All Linux/Xiaomi/BakaSU/SUSFS license and authorship notices are preserved.

BakaSU kernel component and UAPI are vendored from Baka-SU/BakaSU upstream dac2d186406a0d2b0ce3c67cad5a1fa1adbf9f4d (v4.2.0-rc3) with 4.14-specific changes under BakaSU/kernel. No live git submodule needed. The old KernelSU Next submodule is absent.

SUSFS kernel code is ported from upstream SUSFS **v2.3.0** (GKI reference) with the community
**non-GKI Linux 4.9 port** (wxx9248/susfs4ksu) used as the structural reference.

## Main integration changes (SUSFS 2.3.0 branch)

- Synthetic option `CONFIG_KSU_SUSFS_LEGACY` and the v1.5.5 kernel hooks, `prctl` interface and
  `sus_su` support were removed.
- The SUSFS 2.3.0 kernel-side hooks were ported to the 4.14 vendor tree (24 files, ~103 hunks).
- Userspace interface is the 2.x **supercall**: `sys_reboot` → `ksu_handle_sys_reboot` → `SUSFS_MAGIC`.
- KSU side: BakaSU's 1.5.5 legacy shim was removed and upstream KernelSU sources restored;
  the kernel uses the **SUSFS Inline hook** method (`CONFIG_KSU_SUSFS`) instead of Manual Hook.
- Kconfig/defconfig updated to the 2.3.0 feature set: `SUS_PATH`, `SUS_MOUNT`, `SUS_KSTAT`,
  `SPOOF_UNAME`, `ENABLE_LOG`, `HIDE_KSU_SUSFS_SYMBOLS`, `SPOOF_CMDLINE_OR_BOOTCONFIG`,
  `OPEN_REDIRECT`, `SUS_MAP`.
- `CONFIG_KALLSYMS_ALL=y` supplies required symbol lookup in the vendor kernel.
- Signed memcg LRU accounting and safe read-side checks are an upstream-inspired backport; see MEMCG_LRU.md.

### Linux 4.14 API adaptations

- statx / `SUS_KSTAT`: `vfs_getattr_nosec()` spoof; `vfs_statx()` / `vfs_statx_fd()` syscall hooks
  (4.14 folds `vfs_stat`/`vfs_fstat`/`vfs_fstatat` into these inline helpers).
- fsnotify: 10-argument `handle_event` + `fsnotify_iter_info`; `fsnotify_init_mark(mark, group)`,
  `fsnotify_add_mark(mark, inode, mnt, dups)`.
- compat readdir hooks live in `fs/readdir.c` (not `fs/compat.c`) in this tree.
- `smaps_rollup` is the vendor backport with `smap_gather_stats(vma, mss)` (no rollup mode);
  `SUS_MAP` skips VMAs in `show_smap` / `show_smaps_rollup`.
- `struct mount` fsnotify marks are RCU pointers in 4.14 (NULL init, no `INIT_HLIST_HEAD`).
- Open redirect via `do_filp_open()` post-open re-open.
- Legacy APIs reused: `vfs_kern_mount`, legacy IDA API, `fs/proc/cmdline.c`, `fs/pnode.h`,
  `fs/internal.h` `filename_lookup`.

## Validation history

- 2026-10-22 (earlier): BakaSU v4.2.0-rc3 + SUSFS v1.5.5 linked and produced Image.gz with Proton Clang 15.
- Same day: the combination booted into crDroid v12.10-20260518 Android 16, reached sys.boot_completed=1, SELinux Enforcing.
  ReSukiSU Manager recognized driver version 35236/5; the legacy SUSFS `prctl` interceptor replied to an unprivileged smoke test.
- 2026-10-22 (SUSFS 2.3.0 port): full clean build (4,607 objects, 0 errors),
  `artifacts/agate-bakasu-susfs-Image.gz` sha256
  `dfb816261b2301a65456e00c419ed34ce7aecd37db7065eb33adb592316e78d1`.
- Same day: **device boot verified**. Kernel 4.14.336, `sys.boot_completed=1`, SELinux Enforcing,
  no panic/BUG. `ksu_susfs show version` → **v2.3.0**, `show variant` → **NON-GKI**,
  9 enabled features including `SUS_MAP`. dmesg: `susfs is initialized! version: v2.3.0`.
  Functional checks `add_sus_path` / `add_sus_map` / `set_uname` returned exit 0.
  Boot-time configuration (custom-ROM trace hiding, cmdline spoof, 10 `sus_path` entries) applied.
  The R28 universal userspace binary worked unchanged against the 2.x supercall ABI.
- The memory-cgroup LRU warning observed on the earlier 1.5.5 boot remains under observation.

See DEVICE_VALIDATION.md for test details and limitations, KNOWN_ISSUES.md for unresolved issues,
and SUSFS_23_PORT_REVIEW.md for the port review.
