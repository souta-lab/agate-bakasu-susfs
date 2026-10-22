# Memory cgroup LRU accounting: 4.14 backport

## Observed failure

The 2026-10-22 agate test produced the following warning under HeapTaskDaemon during madvise page reclamation:

    mm/memcontrol.c:1002 mem_cgroup_update_lru_size(..., 1, -1): lru_size -1
    release_pages -> free_pages_and_swap_cache -> arch_tlb_finish_mmu -> zap_page_range -> SyS_madvise

The same warning occurred before and after BakaSU integration. Nothing in that trace establishes that HeapTaskDaemon caused the initial bookkeeping discrepancy. The decrement shown by the warning could simply be the first one to expose a previous mismatch.

## Backported change (source-only until next device test)

Adaptation of Kairui Song's upstream Linux-mm patch v6 1/6 (September 2026):
https://lists.openwall.net/linux-kernel/2026/09/05/707

- Store per-node, per-zone, per-LRU sizes as **signed long**, not unsigned long.
- Update counts by one signed addition under pgdat->lru_lock.
- Move underflow checking to the two LRU-size readers, warning at the consumer (WARN_ON_ONCE), and expose zero rather than a wrapped negative count.
- **Do not overwrite the negative counter with zero** during page release. This avoids mutating accounting history and lets later compensating updates restore a correct value.
- Retain a warning at the read path if the discrepancy affects the reclaim counters.

The source patch protects reclaim from interpreting -1 as ULONG_MAX and eliminates the updater-side warning that may implicate an innocent caller. It **does not identify or repair a confirmed missing LRU addition/deletion**. If the count remains negative when read, the read-side warning can still fire. Do not label the root cause fixed without an independent accounting audit and device retest.

## Code paths

- include/linux/memcontrol.h: lru_zone_size storage and safe read-side helpers.
- mm/memcontrol.c: mem_cgroup_update_lru_size accounting update.
- mm/swap.c: release_pages LRU unlink uses the same helper and the pgdat LRU lock.
- mm/vmscan.c: reclaim uses LRU count readers.

## Verification

- Static tests: tests/test_memcg_lru_backport.py (signed underflow, subsequent recovery, both safe readers, and no updater-side WARN).
- Cross-compiled mm/memcontrol.o, mm/swap.o and mm/vmscan.o using Proton Clang 15 on the developer PC.
- Full ARM64 Image.gz build succeeded with Proton Clang 15; output SHA-256: 39ac746b9e85455fb98d38672c9364217176fbdc612d91c617ad744d9e36bd45.
- **No ADB, phone access or device flashing was performed as part of this change.**

When the device owner tests a future build, compare kernel-log WARN signatures, reclaim behavior, performance, and actual memory-cgroup counters. Do not hide a persistent reader-side warning.
