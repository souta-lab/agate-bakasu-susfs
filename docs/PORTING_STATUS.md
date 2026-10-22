# BakaSU kernel integration status (2026-10-22)

Device: Xiaomi 11T (agate / amber), Linux 4.14.336, crDroid 12.10 Android 16.

## Provenance

The baseline source is the MT6893 kernel snapshot from Scaffold47/agate-ksun-susfs at a94c15b31dc0.
Its README identifies the Xiaomi MT6893 development tree as source.
**This project is NOT described as Hydrogen-based.**

BakaSU submodule: Baka-SU/BakaSU @ dac2d186406a0d2b0ce3c67cad5a1fa1adbf9f4d
(the GitHub main HEAD checked during development).
Old KernelSU Next submodule is removed from this experimental branch.
Original non-GKI SUSFS kernel-side code is at version v1.5.5.

## Workqueue/device-mapper warning

Source investigation identified blk_alloc_queue_node() initializing
q->timeout_work with a NULL callback for bio-only queues. The
blk_sync_queue() teardown path blindly cancelled that work, triggering
WARN_ON(!work->func) in flush_work during dm cleanup.
Patch on this branch conditions cancel_work_sync on an initialized
q->timeout_work.func. It still requires runtime regression testing.

## Memory-cgroup negative LRU count

mem_cgroup_update_lru_size reported lru_size -1 during HeapTaskDaemon
page reclamation. The kernel already guards and clamps counter underflow;
suppressing the WARN_ONCE is not a valid root-cause fix.
Requires reproducer/cgroup/page lifecycle auditing and runtime testing.
The issue remains OPEN.

## Current BakaSU compatibility blockers

BakaSU selects KSU_SUSFS as an inline-hook mode distinct from Manual Hook.
This configuration selected KSU_SUSFS=y on the kernel.
Existing non-GKI SUSFS 1.5.5 kernel hooks are not fully compatible
with current upstream BakaSU inline-hook checks, and upstream
kernel/tools/susfs_compat.mk deliberately aborts if SUSFS isn't updated.
Do not disable upstream diagnostics and present the result as verified.

Build via ./build-agate.sh. No published BakaSU flashable release
until full build, API compatibility, root permissions and stability tests pass.
The existing phone was **not** flashed with this experimental branch.
