# agate-bakasu-susfs

**Experimental Linux 4.14.336 kernel for Xiaomi 11T (agate / MT6893), integrating BakaSU and legacy SUSFS 1.5.5.**

This is an independent source repository, not a GitHub fork. The source base is the Xiaomi MT6893 kernel tree distributed by Scaffold47/agate-ksun-susfs. It is **not** a Hydrogen-derived integration.

## Features

| Component | Version / implementation |
| --- | --- |
| Device | Xiaomi 11T, agate (fastboot product: amber), MT6893 |
| Kernel | Linux 4.14.336, ARM64, Proton Clang 15 |
| Root | BakaSU v4.2.0-rc3 (pinned upstream dac2d186; in-tree GPL-2.0 port) |
| Hook method | Manual Hook for Non-GKI Linux 4.14 |
| SUSFS | v1.5.5 Non-GKI, legacy prctl interface; **not SUSFS 2.x** |
| Android tested | crDroid v12.10-20260518, Android 16 |
| Root manager | ReSukiSU, package com.resukisu.resukisu |

## Current status

The combined BakaSU + SUSFS kernel **compiled, linked and booted on a Xiaomi 11T on 2026-10-22**. Android reached sys.boot_completed=1 and kept SELinux Enforcing. The ReSukiSU Manager recognized the in-kernel driver (35236/5), and a non-root ADB shell received a successful response from the legacy SUSFS prctl interceptor.

The following are not yet fully validated:

- Individual SUSFS features and superuser grants for independent apps.
- Long-duration stability, cameras, sound, charging, radio and all vendor modules.
- A new backport of upstream signed memory-cgroup LRU accounting **has passed a full kernel build but has not yet been boot-tested**.
- The original memcg LRU warning appeared on the last boot-tested kernel. The read-side accounting change is not proof the underlying imbalance is fixed.

The previous device-mapper flush_work warning did not recur in the observed initial-boot kernel log. That observation is not a full regression test.

**No stable release is available.** Do not assume a successful build makes the image safe for another ROM or device.

## Building

Requires a Linux host, kernel build prerequisites and an ARM64-capable Proton Clang 15 toolchain. The source includes the BakaSU kernel component and its matching UAPI (no external KernelSU submodule required).

~~~bash
git clone --branch bakasu-susfs-4.14 https://github.com/souta-lab/agate-bakasu-susfs.git
cd agate-bakasu-susfs
TOOLCHAIN_DIR=/path/to/proton-clang BUILD_JOBS=2 ./build-agate.sh
~~~

The build script checks the required kernel options and writes **artifacts/agate-bakasu-susfs-Image.gz**. It produces a kernel image, **not** a complete boot image or flashable ZIP. See [BUILDING.md](BUILDING.md) before using it.

## Documentation

- [Device validation and known test limits](docs/DEVICE_VALIDATION.md)
- [Memory-cgroup/LRU accounting backport](docs/MEMCG_LRU.md)
- [Known issues](docs/KNOWN_ISSUES.md)
- [Porting and source-version notes](docs/PORTING_STATUS.md)
- [Flashing precautions](FLASHING.md)

## Credits and licensing

Kernel source: Xiaomi MT6893 maintainers and original Linux contributors; device-source snapshot and integration work by [Scaffold47](https://github.com/Scaffold47/agate-ksun-susfs). BakaSU by [Baka-SU contributors](https://github.com/Baka-SU/BakaSU); SUSFS by simonpunk and SUSFS contributors. All upstream copyright notices and GPL-2.0 licensing obligations apply; see [COPYING](COPYING) and [BakaSU/kernel/LICENSE](BakaSU/kernel/LICENSE).

Independent GitHub hosting does not imply independent authorship of the imported code.
