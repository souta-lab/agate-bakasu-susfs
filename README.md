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

Base kernel source and initial device integration: [Scaffold47/agate-ksun-susfs](https://github.com/Scaffold47/agate-ksun-susfs), based on [Hydrogen](https://github.com/rio004) and Linux kernel sources, with original copyright and licensing notices retained.

Potential BakaSU integration: [Baka-SU/BakaSU](https://github.com/Baka-SU/BakaSU). SUSFS sources and original authors' notices must be retained. Evaluate **GPL license compatibility** before distributing integrated binaries.

This GitHub repository was created independently (**not a GitHub fork**). Development and upstream credit are separate questions.

## Current state

- Independent repository created; the unmodified upstream kernel source snapshot is available on the [kernel-upstream-baseline](https://github.com/souta-lab/agate-bakasu-susfs/tree/kernel-upstream-baseline) branch (source commit: a94c15b31dc0).
- Main intentionally contains documentation while BakaSU integration is developed and validated.
- Known-good upstream-derived KernelSU Next + SUSFS 1.5.5 build exists locally, but it is not a BakaSU build.
- The two reported kernel WARN events are under investigation; causes and patches are not yet verified.
- This project's main branch will only carry documented project milestones and audited source, not an untested advertised release.

See [diagnostic notes](docs/KNOWN_ISSUES.md).
