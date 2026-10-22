# Release notes

## 2026-10-22 — SUSFS v2.3.0 on Linux 4.14.336 (non-GKI) 🎉

**This build moves the kernel from SUSFS v1.5.5 (legacy prctl) to SUSFS v2.3.0
(non-GKI manual port, supercall interface) while keeping BakaSU v4.2.0-rc3 as the root solution.**

Tested setup:

- Xiaomi 11T / agate (fastboot product: amber), MediaTek MT6893
- crDroid 12.10-20260518, Android 16
- Linux 4.14.336, ARM64, Proton Clang 15
- BakaSU v4.2.0-rc3 (`dac2d186`) in **SUSFS Inline hook** mode
- SUSFS **v2.3.0, NON-GKI**, supercall (`sys_reboot` → `ksu_handle_sys_reboot` → `SUSFS_MAGIC`)

### Verified on-device

- The kernel boots: `sys.boot_completed=1`, SELinux Enforcing, no panic/BUG.
- Root works: `4.2.0-rc3-65-gdac2d186:KernelSU`, `u:r:ksu:s0`.
- `ksu_susfs show version` → **v2.3.0** (`show variant` → **NON-GKI**).
- dmesg: `susfs is initialized! version: v2.3.0`.
- Enabled features: `SUS_PATH`, `SUS_MOUNT`, `SUS_KSTAT`, `SPOOF_UNAME`, `ENABLE_LOG`,
  `HIDE_KSU_SUSFS_SYMBOLS`, `SPOOF_CMDLINE_OR_BOOTCONFIG`, `OPEN_REDIRECT`, **`SUS_MAP`**.
- Functional: `add_sus_path`, `add_sus_map`, `set_uname` → all exit 0.
- Boot-time configuration applied: custom-ROM trace hiding, cmdline spoof
  (green / locked / enforcing), 10 `sus_path` entries.
- The sidex15 `susfs4ksu-module` R28 **universal binary** works unchanged
  (it auto-detects the 2.x `sys_reboot` ABI).

### What changed

- Removed all SUSFS v1.5.5 kernel hooks (including the legacy `prctl` interface and `sus_su`).
- Ported the SUSFS 2.3.0 kernel-side code to Linux 4.14.336: 24 files, ~103 hunks,
  with 4.14-specific adaptations for statx, fsnotify, compat readdir, `smaps_rollup`,
  mount fsnotify RCU pointers, and the supercall path.
- Rebuilt the KSU side against upstream KernelSU sources and switched BakaSU to the
  **SUSFS Inline hook** method (the 1.5.5 legacy shim is gone).
- Updated Kconfig and `agate_defconfig` to the 2.3.0 feature set (`SUS_MAP` etc.).
- Full clean build: 4,607 objects, 0 errors.
  `artifacts/agate-bakasu-susfs-Image.gz` — sha256
  `dfb816261b2301a65456e00c419ed34ce7aecd37db7065eb33adb592316e78d1`.

### Known limitations

- `execveat()` uses the existing BakaSU hooks only (same as the 1.5.5 build).
- Long-duration stability and vendor features (camera, sound, charging, radio) were not
  exhaustively tested.
- Upstream SUSFS is marked GPL-3.0, this kernel tree is GPL-2.0-only — do not redistribute
  combined binaries/sources without a license/compatibility review.
- Play Integrity `DEVICE`/`STRONG` remain unavailable (TEE-attestation bound); `BASIC` passes.

### Upgrade / rollback

Keep a boot image from your exact ROM build. Flash only `boot_a`:

~~~bash
adb reboot bootloader
fastboot flash boot_a agate-susfs230-boot_a_final.img
fastboot reboot
~~~

Rollback: `fastboot flash boot_a <your previous boot image>`.

---

# Previous build

## First public build (2026-10-22)

The first public build of this Xiaomi 11T agate kernel setup: KernelSU Next 3.2.0 legacy with
manual hooks and SUSFS 1.5.5. The kernel was built from source and tested on crDroid 12.10 /
Android 16 / Linux 4.14.336. KernelSU root worked, manual hooks were active and SUSFS
initialized correctly during boot.

Use any build at your own risk. Keep a working boot image from the exact ROM build you are using
before flashing anything. Other ROMs, firmware bases and Android versions have not been tested.
