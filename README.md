# agate-bakasu-susfs

Independent kernel development for **Xiaomi 11T (agate / MT6893)**.

Goal: a reproducible **Linux 4.14.336** kernel integrating **BakaSU**, with a verified **SUSFS** backport and fixes for kernel warnings observed on crDroid 12.10 (Android 16).

> **Status: work in progress. There is no verified BakaSU release or flashable artifact from this repository yet. Do not flash development builds.**

## Development targets

- Integrate a pinned, auditable BakaSU revision into the MT6893 4.14 kernel and retain working manual hooks.
- Port and validate SUSFS features on Linux 4.14 without silently discarding behavior.
- Investigate and correctly resolve (not suppress) these kernel warnings:
  - kernel/workqueue.c:2929 flush_work(), observed repeatedly during apexd device-mapper cleanup.
  - mm/memcontrol.c:1002 mem_cgroup_update_lru_size(), observed with lru_size -1.
- Keep a reproducible build with Proton Clang 15 and explicit source versions.
- Test boots, modules, SELinux, suspend, storage, and sustained performance on agate.

## Attribution and licensing

Kernel source snapshot imported from [Scaffold47/agate-ksun-susfs](https://github.com/Scaffold47/agate-ksun-susfs), whose README attributes its kernel source to the Xiaomi MT6893 development tree. **This project does not claim to be Hydrogen-based or a Hydrogen integration.** Original Linux/Xiaomi/MT6893 source attributions and licensing notices are retained.

Potential BakaSU integration: [Baka-SU/BakaSU](https://github.com/Baka-SU/BakaSU). SUSFS sources and original authors' notices must be retained. Evaluate **GPL license compatibility** before distributing integrated binaries.

This GitHub repository was created independently (**not a GitHub fork**). Development and upstream credit are separate questions.

## Current state

- Independent repository created; the unmodified upstream kernel source snapshot is available on the [kernel-upstream-baseline](https://github.com/souta-lab/agate-bakasu-susfs/tree/kernel-upstream-baseline) branch (source commit: a94c15b31dc0).
- Main intentionally contains documentation while BakaSU integration is developed and validated.
- Known-good upstream-derived KernelSU Next + SUSFS 1.5.5 build exists locally, but it is not a BakaSU build.
- The two reported kernel WARN events are under investigation; causes and patches are not yet verified.
- This project's main branch will only carry documented project milestones and audited source, not an untested advertised release.

**Standalone BakaSU build:** [bakasu-only-4.14 branch](https://github.com/souta-lab/agate-bakasu-susfs/tree/bakasu-only-4.14) compiles BakaSU v4.2.0-rc3-dac2d186 successfully, with SUSFS explicitly disabled. The ARM64 Image.gz and an untested boot image exist locally, but have not been flashed or boot-tested. This is not a completed BakaSU + SUSFS release.

**Integrated experimental source:** [bakasu-susfs-4.14](https://github.com/souta-lab/agate-bakasu-susfs/tree/bakasu-susfs-4.14) compiles BakaSU v4.2.0-rc3-dac2d186 and the legacy non-GKI SUSFS v1.5.5 together on Linux **4.14.336** (Manual Hook + SUSFS legacy mode). A full ARM64 kernel and unpack/repack-verified boot image were created, but **not flashed or boot-tested**. Linux 4.19 is not used.

The workqueue warning has a candidate fix; the memory-cgroup/LRU warning remains under investigation. No stable release is claimed.

See [diagnostic notes](docs/KNOWN_ISSUES.md).
