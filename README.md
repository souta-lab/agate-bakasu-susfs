# agate-bakasu-susfs

**Boot-tested BakaSU + SUSFS v1.5.5 (legacy) port; experimental, with known kernel warning.**

Custom Xiaomi 11T (agate / amber / MT6893) Linux 4.14.336 kernel project.

This branch vendors **BakaSU v4.2.0-rc3** kernel code and integrates it
with the existing **Linux 4.14 SUSFS v1.5.5** implementation via Manual
Hook + legacy SUSFS mode. This DOES NOT claim SUSFS v2.x API support.

The baseline is the **Xiaomi MT6893 kernel development tree** as distributed
in Scaffold47/agate-ksun-susfs. This kernel is **not described as a Hydrogen
integration or Hydrogen-derived base**. Original upstream authorship,
copyright, and GPL licensing are preserved.

## Status

- BakaSU upstream: pinned commit dac2d186406a0d2b0ce3c67cad5a1fa1adbf9f4d.
- Linux 4.14.336 for Xiaomi 11T.
- SUSFS 1.5.5: legacy non-GKI kernel features integrated with BakaSU via Manual Hook.
- Workqueue/device mapper warning: targeted cleanup fix in block/blk-core.c;
  no runtime regression test yet.
- Memory cgroup negative LRU count: root cause not yet isolated.
- BakaSU + SUSFS legacy full Image.gz compilation and link succeeded locally.
- Booted crDroid 12.10 / Android 16 on Xiaomi 11T; ReSukiSU Manager recognizes driver.
- SUSFS legacy prctl interceptor passed a nonroot ABI smoke test.
- memcg LRU accounting warning is still reproducible; no stable release.

## Build

See [BUILDING.md](BUILDING.md), then use build-agate.sh when
all upstream compatibility issues are resolved. Do NOT flash a work-in-progress
build on a daily-use device.

Detailed status: [docs/PORTING_STATUS.md](docs/PORTING_STATUS.md)

## Credits and licensing

Xiaomi MT6893 developers, Scaffold47 (snapshot distribution), BakaSU authors,
simonpunk and SUSFS contributors, plus all authors credited in original kernel
source. This project is independent on GitHub but does not erase upstream
authorship, licensing, or technical provenance. See COPYING.

Read [2026-10-22 device validation](docs/DEVICE_VALIDATION.md) for pass/fail evidence.
