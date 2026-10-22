# Flashing

**An experimental build has booted on Xiaomi 11T, but long-term stability is unverified and a memory-cgroup WARN remains.**

A successful Image.gz compile is insufficient to validate runtime KSU, SUSFS,
DTB compatibility, module ABI, partition layout, or stability.
Do not flash this development branch.

The 2026-10-22 integration was flashed to slot A for validation after taking local backups. Details in docs/DEVICE_VALIDATION.md. Do not flash without a known-working boot backup.
