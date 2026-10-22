# agate-bakasu-susfs

**Development branch — NOT flashable, NOT verified.**

Custom Xiaomi 11T (agate / amber / MT6893) Linux 4.14.336 kernel project.

This branch pins **BakaSU** as a submodule and retains the kernel-side
SUSFS non-GKI port as a starting point. Integration with current BakaSU
is NOT yet verified: current BakaSU's inline hook validation explicitly
rejects older hook implementations and expects an updated SUSFS API.

The baseline is the **Xiaomi MT6893 kernel development tree** as distributed
in Scaffold47/agate-ksun-susfs. This kernel is **not described as a Hydrogen
integration or Hydrogen-derived base**. Original upstream authorship,
copyright, and GPL licensing are preserved.

## Status

- BakaSU upstream: pinned commit dac2d186406a0d2b0ce3c67cad5a1fa1adbf9f4d.
- Linux 4.14.336 for Xiaomi 11T.
- SUSFS 1.5.5: existing kernel-side code; BakaSU latest rejects it until proper API compatibility work is complete.
- Workqueue/device mapper warning: targeted cleanup fix in block/blk-core.c;
  no runtime regression test yet.
- Memory cgroup negative LRU count: root cause not yet isolated.
- Kernel source compatibility hooks and select objects compile; upstream SUSFS compatibility check still blocks the full kernel build.
- No BakaSU release or proven boot image.

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
