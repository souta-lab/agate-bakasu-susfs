# Porting notes and revision history

## Source identity and attribution

Device: Xiaomi 11T / agate (fastboot product amber); Linux 4.14.336 on MT6893.

Base kernel snapshot: Scaffold47/agate-ksun-susfs commit a94c15b31dc0 (Xiaomi MT6893 source). GitHub project independent from that source repository; not described as Hydrogen-based. All Linux/Xiaomi/BakaSU/SUSFS license and authorship notices are preserved.

BakaSU kernel component and UAPI are vendored from Baka-SU/BakaSU upstream dac2d186406a0d2b0ce3c67cad5a1fa1adbf9f4d (v4.2.0-rc3) with 4.14-specific changes under BakaSU/kernel. No live git submodule needed. The old KernelSU Next submodule is absent.

## Main integration changes

- Linux 4.14 uses manual hooks, with a separate CONFIG_KSU_SUSFS_LEGACY option that enables the existing SUSFS v1.5.5 Non-GKI implementation.
- Modern SUSFS 2.x API, supercall interface and features are **not** represented as supported by this legacy bridge.
- CONFIG_KALLSYMS_ALL=y supplies required symbol lookup in the vendor kernel.
- The adapted KSU hook entrypoints compile and link into vmlinux.
- The block queue timeout work cancellation was guarded when the queue has no timeout callback, addressing the device-mapper flush_work warning observed during apexd cleanup.
- Signed memcg LRU accounting and safe read-side checks are an upstream-inspired backport; see MEMCG_LRU.md.

## Validation history

- October 22: BakaSU v4.2.0-rc3 + SUSFS v1.5.5 linked and produced Image.gz with Proton Clang 15.
- Same day: the combination booted into crDroid v12.10-20260518 Android 16, reached sys.boot_completed=1, SELinux Enforcing.
- ReSukiSU Manager reported running, recognized driver version 35236/5. The legacy SUSFS prctl interceptor replied correctly to an unprivileged smoke test.
- flush_work warning was absent from the boot snapshot, but the memory-cgroup LRU warning remained (HeapTaskDaemon, LRU 1, delta -1).
- The later signed LRU accounting change was tested at source/unit and cross-compile level, but **is not covered by that device boot**. No device communication was performed as part of the memcg/README work.

See DEVICE_VALIDATION.md for test details and limitations, KNOWN_ISSUES.md for unresolved issues.
