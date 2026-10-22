# agate-bakasu-susfs

**Linux 4.14.336 kernel for Xiaomi 11T (agate / MT6893) — running BakaSU v4.2.0-rc3 + SUSFS v2.3.0 (non-GKI).**

> **🎉 SUSFS v2.3.0 now runs on Linux 4.14.336 (non-GKI).**
> Verified on a real Xiaomi 11T (agate / amber) running crDroid 12.10 on Android 16:
> the kernel boots, BakaSU root works, and the in-kernel SUSFS reports **v2.3.0** with the
> full 2.x feature set — including **`SUS_MAP`** and **AVC log spoofing** — over the
> **supercall** interface.

This is an independent source repository, not a GitHub fork. The source base is the
Xiaomi MT6893 kernel tree distributed by [Scaffold47/agate-ksun-susfs](https://github.com/Scaffold47/agate-ksun-susfs).
It is **not** a Hydrogen-derived integration.

## Features

| Component | Version / implementation |
| --- | --- |
| Device | Xiaomi 11T, agate (fastboot product: amber), MediaTek MT6893 |
| Kernel | Linux 4.14.336, ARM64, built with Proton Clang 15 |
| Root | **BakaSU v4.2.0-rc3** (upstream `dac2d186`, in-tree GPL-2.0 port) |
| Hook method | **SUSFS Inline hook** (`CONFIG_KSU_SUSFS`); previous builds used Manual Hook |
| SUSFS | **v2.3.0, NON-GKI port** — supercall (`sys_reboot`) interface, `SUS_MAP`, AVC log spoofing |
| Android tested | crDroid v12.10-20260518, Android 16 |
| Root manager | ReSukiSU, package `com.resukisu.resukisu` |
| Build status | Object-level + full clean build pass (4,607 objects, 0 errors) |

## Verified on-device (2026-10-22)

| Check | Result |
| --- | --- |
| Boot | `sys.boot_completed=1`, SELinux Enforcing |
| Root | `4.2.0-rc3-65-gdac2d186:KernelSU` (`u:r:ksu:s0`) |
| SUSFS version | `ksu_susfs show version` → **v2.3.0** (variant **NON-GKI**) |
| SUSFS init | dmesg: `susfs is initialized! version: v2.3.0` — no panic / BUG |
| Feature set | `SUS_PATH`, `SUS_MOUNT`, `SUS_KSTAT`, `SPOOF_UNAME`, `ENABLE_LOG`, `HIDE_KSU_SUSFS_SYMBOLS`, `SPOOF_CMDLINE_OR_BOOTCONFIG`, `OPEN_REDIRECT`, **`SUS_MAP`** |
| Functional tests | `add_sus_path`, `add_sus_map`, `set_uname` → all exit 0 |
| Boot-time config | custom-ROM trace hiding (`hide_cusrom`), cmdline spoof (green / locked / enforcing), 10 `sus_path` entries |
| Userspace | sidex15 `susfs4ksu-module` R28 universal binary (auto-detects the 2.x `sys_reboot` ABI) |
| Runtime stack | Zygisk Next 1.5.2 (3 modules), Vector/LSPosed, AlwaysStrong (TEESimulator-RS), HMA-OSS |
| Play Integrity | `BASIC` ✓, `DEVICE`/`STRONG` ✗ — hardware-attestation (TEE) bound, unchanged by SUSFS |

## Why this matters

Upstream SUSFS 2.x targets GKI kernels (5.10+) and does not apply to a vendor 4.14 tree.
This branch is a **manual non-GKI port of SUSFS 2.3.0 to Linux 4.14.336**:

- The v1.5.5 hooks were removed and replaced by the 2.3.0 hooks (24 files, ~103 hunks).
- The port uses the community **SUSFS 2.3.0 non-GKI port for Linux 4.9** as the reference
  and adapts it to the 4.14 vendor tree.
- Userspace interface: the 2.x **supercall** path
  (`sys_reboot` → `ksu_handle_sys_reboot` → `SUSFS_MAGIC`) instead of the old `prctl` one.

### Linux 4.14 adaptations

| Area | Adaptation |
| --- | --- |
| statx / `SUS_KSTAT` | `vfs_getattr_nosec()` spoof; `vfs_statx()` / `vfs_statx_fd()` syscall hooks (4.14 folds `vfs_stat`/`vfs_fstat`/`vfs_fstatat` into these) |
| fsnotify | 4.14's 10-argument `handle_event` + `fsnotify_iter_info`; `fsnotify_init_mark(mark, group)`, `fsnotify_add_mark(mark, inode, mnt, dups)` |
| `compat` readdir | moved to `fs/readdir.c` in 4.14 — `compat_fillonedir` / `compat_filldir` hooks |
| `smaps_rollup` | vendor backport `smap_gather_stats(vma, mss)` (no rollup mode) — `SUS_MAP` skips VMA-level in `show_smap` / `show_smaps_rollup` |
| Mounts | `struct mount` fsnotify marks are RCU pointers in 4.14 (`NULL` init instead of `INIT_HLIST_HEAD`) |
| Open redirect | `do_filp_open()` post-open re-open (4.14 `do_last()` resolves and opens in one step) |
| Legacy APIs | `vfs_kern_mount`, legacy IDA API, `fs/proc/cmdline.c`, `fs/pnode.h`, `fs/internal.h` `filename_lookup` |
| KSU side | BakaSU's 1.5.5 legacy shim removed; **SUSFS Inline hook mode** restored against upstream KSU sources |

## Artifacts

| File | SHA-256 |
| --- | --- |
| `artifacts/agate-bakasu-susfs-Image.gz` (14,473,559 B) | `dfb816261b2301a65456e00c419ed34ce7aecd37db7065eb33adb592316e78d1` |
| boot image `agate-susfs230-boot_a_final.img` (134,217,728 B, local repack) | `1a41a925ed874ddf5bec29a3cbf0a7a0cb6ce912f6eef799f91330bcd7eddfe2` |

The build script produces **only** `Image.gz`. A flashable boot image must be repacked against
the boot image of your exact ROM build (the verified device used the crDroid 12.10 boot ramdisk/DTB).

## Building

Requires a Linux host, kernel build prerequisites and an ARM64-capable Proton Clang 15 toolchain.
The source includes the BakaSU kernel component and its matching UAPI (no external KernelSU submodule required).

~~~bash
git clone --branch feature/susfs-2.3.4.14-port https://github.com/souta-lab/agate-ksun-susfs.git
cd agate-ksun-susfs
TOOLCHAIN_DIR=/path/to/proton-clang BUILD_JOBS=2 ./build-agate.sh
~~~

The build script checks the required kernel options and writes **artifacts/agate-bakasu-susfs-Image.gz**.
See [BUILDING.md](BUILDING.md) before using it.

## Flashing and rollback

Always keep a working boot image from the exact ROM build you are running.

~~~bash
# back up the current boot partition first
adb shell su -c "dd if=/dev/block/by-name/boot_a of=/data/local/tmp/boot_a_backup.img bs=1M"
adb pull /data/local/tmp/boot_a_backup.img

# flash the repacked boot image
adb reboot bootloader
fastboot flash boot_a agate-susfs230-boot_a_final.img
fastboot reboot

# rollback if the device does not boot
fastboot flash boot_a boot_a_backup.img
~~~

The verified device was flashed with `fastboot flash boot_a` on slot A only.
Do not flash other partitions (firmware, `lk`, `nvram`, `nvdata`, `persist`, `tee`) for a kernel change.

## Verification on the device

~~~bash
su -c 'ksu_susfs show version'          # v2.3.0
su -c 'ksu_susfs show variant'          # NON-GKI
su -c 'ksu_susfs show enabled_features' # 9 features incl. SUS_MAP
su -c 'ksu_susfs add_sus_path /sdcard/test'
su -c 'ksu_susfs add_sus_map /sdcard/test'
su -c 'dmesg | grep "susfs is initialized"'
~~~

## Known limitations

- `execveat()` paths use BakaSU's existing hooks only (same known limitation as the 1.5.5 build).
- Long-duration stability, cameras, sound, charging, radio and all vendor modules were not exhaustively tested.
- The kernel now uses the SUSFS Inline hook method; KSU-side behaviour differences were validated only
  at boot, root and SUSFS level (not every app profile/policy path).
- `CONFIG_KSU_SUSFS_SUS_SU` is not available for non-GKI (upstream constraint).
- AVC log spoofing is enabled at runtime through the supercall interface.
- The upstream SUSFS repository is marked **GPL-3.0** while this kernel tree is **GPL-2.0-only**.
  **Do not redistribute combined binaries/sources without an explicit license/compatibility review.**
- Only crDroid 12.10 on Android 16 was tested. Other ROMs, firmware bases and Android versions are untested.

**No stable release is available.** Do not assume a successful build makes the image safe for another ROM or device.

## Documentation

- [Device validation and known test limits](docs/DEVICE_VALIDATION.md)
- [SUSFS 2.3.0 port review](docs/SUSFS_23_PORT_REVIEW.md)
- [Known issues](docs/KNOWN_ISSUES.md)
- [Porting and source-version notes](docs/PORTING_STATUS.md)
- [Flashing precautions](FLASHING.md)

## Credits and licensing

Kernel source: Xiaomi MT6893 maintainers and original Linux contributors; device-source snapshot and
integration work by [Scaffold47](https://github.com/Scaffold47/agate-ksun-susfs).
BakaSU by [Baka-SU contributors](https://github.com/Baka-SU/BakaSU).
SUSFS by [simonpunk](https://gitlab.com/simonpunk/susfs4ksu) and SUSFS contributors;
the Linux 4.9 non-GKI port reference used for this work is
[wxx9248/susfs4ksu](https://github.com/wxx9248/susfs4ksu).
All upstream copyright notices and GPL-2.0 licensing obligations apply; see [COPYING](COPYING) and
[BakaSU/kernel/LICENSE](BakaSU/kernel/LICENSE).

Independent GitHub hosting does not imply independent authorship of the imported code.
