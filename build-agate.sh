#!/usr/bin/env bash
# Reproducible kernel-image build for agate-bakasu-susfs.
set -euo pipefail
cd "$(dirname "$0")"
TOOLCHAIN_DIR="${TOOLCHAIN_DIR:-/mnt/storage/android-kernel-build/toolchains/proton-clang}"
BUILD_JOBS="${BUILD_JOBS:-2}"
OUT_DIR="${OUT_DIR:-out}"
if [[ ! -x "$TOOLCHAIN_DIR/bin/clang" ]]; then
  echo "Missing Proton Clang at $TOOLCHAIN_DIR/bin/clang" >&2
  exit 2
fi
if [[ ! -d BakaSU/kernel ]]; then
  echo "Vendored BakaSU kernel sources missing." >&2
  exit 2
fi
export PATH="$TOOLCHAIN_DIR/bin:$PATH"
make O="$OUT_DIR" ARCH=arm64 agate_defconfig
for symbol in CONFIG_KSU=y CONFIG_KSU_SUSFS=y CONFIG_THREAD_INFO_IN_TASK=y; do
  grep -Fqx "$symbol" "$OUT_DIR/.config" || {
    echo "Missing expected config: $symbol" >&2; exit 2;
  }
done
make -j"$BUILD_JOBS" O="$OUT_DIR" ARCH=arm64 CC=clang LLVM=1 LLVM_IAS=1 \
  CROSS_COMPILE=aarch64-linux-gnu- CROSS_COMPILE_ARM32=arm-linux-gnueabi- Image.gz
mkdir -p artifacts
install -m 0644 "$OUT_DIR/arch/arm64/boot/Image.gz" artifacts/agate-bakasu-susfs-Image.gz
sha256sum artifacts/agate-bakasu-susfs-Image.gz
echo "Built kernel Image.gz only. Flashable boot image requires verification against current ROM."
