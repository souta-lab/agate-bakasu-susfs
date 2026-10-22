# Building experimental BakaSU kernel

Run from the source branch with the bundled BakaSU source:
    TOOLCHAIN_DIR=/path/to/proton-clang BUILD_JOBS=2 ./build-agate.sh

Script uses agate_defconfig and requires KSU + KSU_SUSFS. It outputs
artifacts/agate-bakasu-susfs-Image.gz only if the build succeeds.
Output is not a complete boot image, nor a flashable ZIP.

BakaSU upstream and SUSFS compatibility remain under active development.
See docs/PORTING_STATUS.md. Do not flash until runtime validation.
