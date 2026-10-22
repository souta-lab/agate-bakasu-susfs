# Vendored BakaSU kernel source

- Upstream source: https://github.com/Baka-SU/BakaSU
- Starting upstream commit: dac2d186406a0d2b0ce3c67cad5a1fa1adbf9f4d (2026-10-20)
- License for kernel source: kernel/LICENSE (GPL-2.0)
- Modifications: allow KSU_MANUAL_HOOK with Linux 4.14 legacy SUSFS v1.5.5; select the legacy mount and prctl behavior, while retaining BakaSU superuser and management functionality.
- Original BakaSU API for SUSFS 2.x is **not** fully backported. The agate port uses the existing legacy SUSFS feature interface for the actual kernel. Do not represent as SUSFS 2.x.
- Kbuild has pinned upstream version 35236 and a recognizable 'agate' suffix to avoid broken git-rev detection when vendored.
