# Building agate-bakasu-susfs

This branch packages the Linux 4.14.336 Xiaomi MT6893 kernel, the compatible in-tree BakaSU kernel source and its UAPI, and legacy SUSFS v1.5.5.

## Host requirements

- Linux, enough free disk/RAM for a full ARM64 kernel build.
- Proton Clang 15 (or separately validated compatible LLVM toolchain).
- make, standard kernel build packages, Python 3, git.
- Config: arch/arm64/configs/agate_defconfig.

## Reproducible build

~~~bash
TOOLCHAIN_DIR=/path/to/proton-clang BUILD_JOBS=2 ./build-agate.sh
~~~

The script runs agate_defconfig, verifies CONFIG_KSU, CONFIG_KSU_SUSFS and CONFIG_THREAD_INFO_IN_TASK, and builds Image.gz. Its default TOOLCHAIN_DIR is an example path from the development machine; set it explicitly on other hosts.

Output: artifacts/agate-bakasu-susfs-Image.gz. Build metadata is available under out/.config and out/vmlinux. Keep the build log and checksum when reporting a test result.

A passing compile is not an API, SELinux or device-stability test. The source does not generate a flashable ZIP; repacking a current-ROM boot image is a separate, device-sensitive operation.

## Memcg compile validation

~~~bash
export PATH=/path/to/proton-clang/bin:$PATH
make O=out ARCH=arm64 agate_defconfig
make -j2 O=out ARCH=arm64 CC=clang LLVM=1 LLVM_IAS=1 \
  CROSS_COMPILE=aarch64-linux-gnu- CROSS_COMPILE_ARM32=arm-linux-gnueabi- \
  mm/memcontrol.o mm/swap.o mm/vmscan.o
python3 -m unittest discover -s tests -p 'test_memcg_*.py'
~~~

See docs/MEMCG_LRU.md for the exact accounting change and validation limits.

## Safety

Only Xiaomi 11T / agate has been boot-tested, and only with the documented crDroid build. Make a working boot backup and have a working recovery/fastboot path before any flash. No stable release is available.
