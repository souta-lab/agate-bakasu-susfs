# Kernel warnings to investigate

These warnings were captured on a Xiaomi 11T running crDroid 12.10 (Android 16), Linux 4.14.336 custom kernel, on 2026-10-22.

## 1. Workqueue/device-mapper warning

- kernel/workqueue.c:2929 contains WARN_ON(!work->func).
- apexd triggers the warning repeatedly while deleting device-mapper devices.
- Backtrace contains flush_work -> __cancel_work_timer -> cancel_work_sync -> blk_cleanup_queue -> cleanup_mapped_device -> __dm_destroy -> dm_destroy.
- Hypothesis: uninitialized or invalid work item in block cleanup, not proof of an apexd defect.
- Validate initialization/cancellation lifecycle against upstream workqueue/block fixes, capture reproducer, and regression-test.

## 2. Memory cgroup / LRU accounting warning

- mm/memcontrol.c:1002 mem_cgroup_update_lru_size reports lru_size -1.
- Observed in HeapTaskDaemon during madvise, page release and LRU accounting.
- Requires diagnosis of mismatched page/zone/LRU tracking, not simply deleting WARN_ONCE.
- Cross-check vendor page-accounting changes and upstream stable fixes.

Both warnings predate BakaSU integration in this project. Do not assert they are caused by BakaSU or already fixed.
