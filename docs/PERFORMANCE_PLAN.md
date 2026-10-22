# Performance optimization plan — Linux 4.14.336 / agate (MT6893)

Target: Xiaomi 11T (agate, MT6893), Linux 4.14.336, BakaSU v4.2.0-rc3 + SUSFS v2.3.0.
Goal: measurable performance improvements without touching thermal/power safety and without
breaking the root/hiding stack.

## Measured current state (2026-10-22)

| Item | Current value | Comment |
| --- | --- | --- |
| Compiler flags | `CONFIG_CC_OPTIMIZE_FOR_PERFORMANCE=y`, `CONFIG_LTO_NONE=y` | LTO must stay off for KSU |
| Preemption / HZ | `CONFIG_PREEMPT=y`, `CONFIG_HZ_250` | 250 Hz |
| Debug overhead | `CONFIG_DEBUG_KERNEL=y`, `CONFIG_SCHED_DEBUG=y`, **`CONFIG_SCHEDSTATS=y`** | `SLUB_DEBUG`/`PAGE_OWNER`/`KASAN`/`PROVE_LOCKING` are already **off** |
| Cmdline debug params | `slub_debug=OFZPU`, `page_owner=on` | **Ignored** — the matching configs are not set (no overhead) |
| TCP | `CONFIG_DEFAULT_TCP_CONG="bic"`, runtime `westwood`, qdisc `pfifo_fast`, **no BBR, no fq/fq_codel** | |
| ARM64 features | **`CONFIG_ARM64_LSE_ATOMICS` off**, `SHA1_ARM64_CE` / `GHASH_ARM64_CE` / `CRC32_ARM64_CE` off | SHA2/AES CE already on |
| zram | `lzo [lz4]`, 5.88 GB, swap active | lz4 selected |
| UFS (`/dev/sda` = bootdevice host0) | scheduler **`[cfq]`**, `read_ahead_kb=128`, `nr_requests=64` | dm/zram = `none` |
| UFS HPB | **enabled** (HPB v0221, hit 38892 / miss 16050) | tunables under `ufshpb_lu2` |
| schedutil | up_rate_limit 20000 µs / down 10000 µs (both clusters) | |
| VM | swappiness 60, vfs_cache_pressure 80, dirty_ratio 20 | |
| CPU | 3 policies: little max 2.0 GHz, big max 3.0 GHz | |

## Baseline measurement (do this before any change)

1. CPU/GPU: Geekbench 6, 3DMark Wild Life, PCMark (record scores + device temperature).
2. Storage: `fio` (push a static arm64 binary) — `randread 4k`, `randwrite 4k`, `seqread`.
3. Network: `iperf3` over Wi-Fi (local server).
4. Memory: `dumpsys meminfo`, `cat /sys/block/zram0/mm_stat`.
5. Boot: cold boot time (`adb shell getprop sys.boot_completed` timing with logcat timestamps).
6. Idle drain: 1 h screen-off battery drop.

Keep the baseline kernel/boot image for rollback.

---

## Phase 1 — runtime tunables (no rebuild, low risk) ⭐ start here

All of these can be applied with `su -c "echo ... > ..."` and persisted in a KSU module
`post-fs-data.sh`/`service.sh`. Measure each one; keep only the wins.

| # | Change | Before | Candidate | Expected |
| --- | --- | --- | --- | --- |
| 1.1 | UFS scheduler | `cfq` | `deadline` (or `none`) | lower I/O latency, better flash behavior |
| 1.2 | UFS read-ahead / queue depth | 128 kB / 64 | 256 kB / 128 | sequential read throughput |
| 1.3 | schedutil up rate limit | 20000 µs | 5000–10000 µs | UI responsiveness (more power) |
| 1.4 | VM swappiness (zram present) | 60 | 100 | better zram use / fewer OOM kills |
| 1.5 | `vfs_cache_pressure` | 80 | 100 | reclaim behavior |
| 1.6 | `dirty_ratio` | 20 | 10–15 | less write burst latency / flash wear |
| 1.7 | UFS HPB prefetch (`pre_req_max_tr_len`, throttle) | vendor default | test 256 / relaxed | random-read hit rate |

Note: `slub_debug=`/`page_owner=` on the cmdline are dead options on this config — no gain there.

## Phase 2 — kernel rebuild, config-only (low–moderate risk)

| # | Config | Rationale |
| --- | --- | --- |
| 2.1 | `CONFIG_ARM64_LSE_ATOMICS=y` | runtime-detected LSE atomics (A78/A55) speed up contended code; falls back safely |
| 2.2 | `CONFIG_CRYPTO_CRC32_ARM64_CE=y` | CRC32 for f2fs/ext4 checksums |
| 2.3 | `CONFIG_CRYPTO_SHA1_ARM64_CE=y`, `CONFIG_CRYPTO_GHASH_ARM64_CE=y` | TLS/GCM throughput (SHA2/AES CE already on) |
| 2.4 | `CONFIG_TCP_CONG_BBR=y`, `CONFIG_NET_SCH_FQ=y`, `CONFIG_NET_SCH_FQ_CODEL=y` | keep `westwood` default; allow BBR + fq_codel testing |
| 2.5 | `CONFIG_SCHEDSTATS=n`, `CONFIG_SCHED_DEBUG=n` | remove scheduler statistics overhead |
| 2.6 | `CONFIG_HZ_300` (optional) | responsiveness vs power — bench first |
| 2.7 | `CONFIG_CRYPTO_ZSTD=y` + zram zstd option (optional) | better compression ratio vs speed trade-off |

Build → flash `boot_a` → re-run the Phase 0 suite. Revert individual configs if a regression appears.

## Phase 3 — targeted patches (moderate risk, bench-driven)

- PELT half-life / capacity tuning in `kernel/sched/pelt.c` (responsiveness).
- schedutil `iowait_boost` behaviour.
- UFS HPB tuning (prefetch/throttle) based on hit/miss counters.
- F2FS mount options (userspace `/vendor/etc/fstab`, careful with OTA).
- zram writeback/discard policy.

## Explicitly rejected (not worth the risk on this device)

| Item | Why not |
| --- | --- |
| MGLRU | merged in 6.1; no usable 4.14 backport |
| le9uo / uLMK | designed for 4.19+; 4.14 port is not available |
| BBRv3 | requires newer TCP APIs |
| LTO / ThinLTO | must stay off for KernelSU compatibility |
| `-O3` kernel-wide | size/instability issues in practice |
| `slub_debug`/`page_owner` removal | already disabled at config level — no effect |
| KSM | CPU/memory trade-off, not a win for this workload |
| thermal throttling off | unsafe for battery/SoC |

## Guardrails

- One change at a time; keep a log of before/after numbers.
- Always keep the previous boot image (`fastboot flash boot_a` rollback).
- Benchmark at a stable temperature (avoid measuring under throttling).
- Do not touch thermal/power tables or GPU voltage.
