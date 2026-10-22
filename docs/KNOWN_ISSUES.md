# Known issues

Source status: BakaSU v4.2.0-rc3 + SUSFS v1.5.5 on Linux 4.14.336.

## Memory-cgroup negative LRU accounting (not root-cause resolved)

On the 2026-10-22 test build, mm/memcontrol.c:1002 warned when HeapTaskDaemon released a page via madvise and the per-zone LRU count fell to -1.

The development branch now includes an upstream-inspired backport of **signed LRU counters and read-side validity checks**. This is a substantive accounting hardening change, not proof that every missing charge/decharge has been fixed. The patch compiled; runtime retest is pending. See [MEMCG_LRU.md](MEMCG_LRU.md).

## Workqueue / device-mapper teardown

Previously: repeated WARN_ON(!work->func) in flush_work() while apexd removed device-mapper queues. The 4.14 source had bio queues that never installed a timeout work callback, but the teardown cancelled the work regardless.

This branch guards cancel_work_sync() with an initialized work callback check in block/blk-core.c. The warning was absent from the captured first boot using that patch. Extended lifecycle regression testing remains pending.

## Feature and manager compatibility

- SUSFS 1.5.5 legacy ABI: smoke-tested; individual hiding/unmount/kstat operations have not been fully verified.
- ReSukiSU Manager v4.2.0-rc3 (35171) is older than the pinned kernel driver (35236) and can show a manager-update prompt.
- An app-specific root-grant test and longer-term stability tests remain outstanding.
- No Android 16 ROM or device other than the documented crDroid Xiaomi 11T has been boot-tested.
