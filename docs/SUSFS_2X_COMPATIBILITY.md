# SUSFS 2.x / Linux 4.14 compatibility review

Date: 2026-10-22. **Research-only branch.** This document is not a claim of successful SUSFS 2.x integration, and no SUSFS 2.x kernel was built.

## Existing source

- Device kernel: Linux 4.14.336, Xiaomi MT6893/agate.
- BakaSU: pinned 2026-10-20 v4.2.0-rc3 source with Non-GKI manual hooks.
- Existing SUSFS kernel: v1.5.5 legacy compatibility.
- The boot-tested version stays unchanged in the bakasu-susfs-4.14 branch.

## Reviewed available references

- Mafiadan6/SUSFS-NonGKI-Patches, source revision 27d23165477294c57c43ad87c740a2e27af0d780 (2026-04-03). Describes Linux 4.14 with SUSFS v2.1.0, but is a *collection of patches* requiring an existing compatible SUSFS and other prerequisites, not a complete, stand-alone ready-to-build 2.1.0 kernel tree.
- wxx9248/susfs4ksu, kernel-4.9-v2 source revision 71345ded5af28f55d76ebcdc7a9df9cea56111e1 (2026-09-12). Contains SUSFS v2.3.0 components adapted to **Linux 4.9**, not tested on Linux 4.14. The referenced repository's LICENSE is GPL-3.0; evaluate compatibility before importing material into this GPL-2.0 Linux kernel project.
- The original simonpunk kernel-4.14 SUSFS branch remains on the v1.5.x generation; there is no supported drop-in 2.x equivalent for this vendor tree.

## Source-level findings

In the existing vendor kernel, fs/susfs.c is about 32 KiB and SUSFS 2.3.0 from the Linux 4.9 fork is about 59 KiB; include/linux/susfs_def.h also changes substantially.

Read-only patch dry-run of the eight Mafiadan6 Linux 4.14 patches against this source showed that five did not apply cleanly. Direct copying would conflate different platform APIs, hook ownership, and unrelated vendor modifications.

Both major version families differ in kernel ABI and require independent testing for memory safety, syscall correctness, lock ordering, mount and inode lifetimes, and BakaSU integration. An updated version string alone is not an upgrade.

## Boundaries / test criteria

Only non-evasion compatibility, source hygiene, license review, memory safety and crash/boot stability review are in scope for this research branch. No changes are made to application-integrity bypass or concealment features.

Any actual kernel integration would need full compilation, controlled boot testing, and behavioral regression testing before replacing the prior working image.

## Device interaction

No ADB access, device modification, flashing, or privileged test execution occurred during this review.
