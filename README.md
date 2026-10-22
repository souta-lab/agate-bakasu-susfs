# agate-bakasu-susfs

**BakaSU + legacy SUSFS kernel project for Xiaomi 11T (agate / MT6893), Linux 4.14.336.**

Independent GitHub repository built from the Xiaomi MT6893 kernel development tree distributed by Scaffold47. This project **is not Hydrogen-based**.

## Source code

The production of the experimental kernel is tracked in a separate branch:

**[bakasu-susfs-4.14 — full kernel source, build scripts, tests and technical documentation](https://github.com/souta-lab/agate-bakasu-susfs/tree/bakasu-susfs-4.14)**

This main branch is the project's landing page. To clone the actual integration source:

~~~bash
git clone -b bakasu-susfs-4.14 https://github.com/souta-lab/agate-bakasu-susfs.git
cd agate-bakasu-susfs
TOOLCHAIN_DIR=/path/to/proton-clang BUILD_JOBS=2 ./build-agate.sh
~~~

The script builds Image.gz, not a complete boot.img or flashable ZIP.

## Integration

| Component | Status |
| --- | --- |
| Linux 4.14.336 / Xiaomi MT6893 | Compiled and boot-tested on agate |
| BakaSU v4.2.0-rc3, upstream dac2d186 | Boot-tested; ReSukiSU Manager recognizes driver 35236 |
| SUSFS v1.5.5 Non-GKI | Legacy prctl ABI smoke-tested (not SUSFS 2.x) |
| block/blk-core.c workqueue teardown fix | Included; original flush_work warning absent on the observed boot |
| Signed memcg LRU accounting backport | Full ARM64 rebuild passed; **device retest outstanding** |

## Validation and limitations

On 2026-10-22 the integrated kernel booted crDroid v12.10-20260518 (Android 16) on a Xiaomi 11T, with SELinux Enforcing. A non-privileged test confirmed that the legacy SUSFS prctl entry point was reachable.

The original build had a negative LRU-count warning in mem_cgroup_update_lru_size() during HeapTaskDaemon memory reclamation. The newer source backports the upstream Linux-mm signed LRU accounting and read-side checks, avoiding unsigned wraparound and preserving counter history. It is **not evidence that the underlying accounting mismatch has been fully resolved**. The new version has been compile-tested but not boot-tested. Individual SUSFS capabilities, application root grants, long-term stability, and other Android ROMs are also unverified.

**Experimental, no stable release.** Any device testing must be performed separately with a known-working recovery image.

## Documentation and history

- [Integration README](https://github.com/souta-lab/agate-bakasu-susfs/blob/bakasu-susfs-4.14/README.md)
- [Memory-cgroup LRU accounting notes](https://github.com/souta-lab/agate-bakasu-susfs/blob/bakasu-susfs-4.14/docs/MEMCG_LRU.md)
- [Device test results](https://github.com/souta-lab/agate-bakasu-susfs/blob/bakasu-susfs-4.14/docs/DEVICE_VALIDATION.md)
- [Known issues](https://github.com/souta-lab/agate-bakasu-susfs/blob/bakasu-susfs-4.14/docs/KNOWN_ISSUES.md)
- [Original kernel snapshot](https://github.com/souta-lab/agate-bakasu-susfs/tree/kernel-upstream-baseline)
- [Earlier BakaSU-only experiment](https://github.com/souta-lab/agate-bakasu-susfs/tree/bakasu-only-4.14)

## Credits and licensing

Kernel work is derived from Xiaomi MT6893 and Linux sources, through the Scaffold47 snapshot. BakaSU is by Baka-SU contributors; SUSFS by simonpunk and contributors. The integration branch preserves upstream authorship and GPL-2.0 licensing, including COPYING and BakaSU/kernel/LICENSE. Independent GitHub hosting does not erase original authorship.
