# Xiaomi 11T device validation (2026-10-22)

Device: Xiaomi 11T / agate (fastboot: amber), ROM crDroid v12.10-20260518, Android 16.
Integrated BakaSU v4.2.0-rc3 and legacy SUSFS v1.5.5; Linux 4.14.336, Proton Clang 15.
Only boot_a was flashed; the original ramdisk and DTB were preserved.

## Confirmed
- fastboot flash boot_a returned OKAY for sending and writing.
- ADB reconnected, sys.boot_completed=1, uname -r = 4.14.336-ge81914ad3933-dirty.
- SELinux Enforcing and Android services activity, package, SurfaceFlinger, camera, audio present.
- ReSukiSU v4.2.0-rc3 Manager reports running/Built-in, driver v4.2.0-rc3-dac2d186-agate (35236/5); kernel logs show the app recognized as manager.
- Legacy SUSFS prctl interceptor: non-root ADB shell (uid 2000) executed tests/susfs_abi_probe.c. Option 0xDEADBEEF returned zero; adjacent unrecognized option 0xDEADBEEE returned -EINVAL. Exit status zero.
- The earlier workqueue flush_work warning was absent from this initial boot's captured kernel log.
- Prior working boot image has been saved locally for rollback.

## Unresolved
- mem_cgroup_update_lru_size(..., 1, -1): lru_size -1 warning reproduced at mm/memcontrol.c:1002, HeapTaskDaemon, about 54 seconds into boot.
- Full SUSFS path, mount, and kstat behavioral tests need authorized root; non-root prctl intercept alone does not establish them.
- Independent app superuser grants not tested. Manager shows SuperUser: 0. Shell lacking the su binary alone is not a root failure.
- ReSukiSU Manager 35171 shows an update prompt for the kernel driver's pinned 35236.
- Boot success does not establish long-term stability or successful physical camera/audio playback.
- This is legacy SUSFS v1.5.5, not SUSFS 2.x.

## Repeat ABI smoke test (developer Linux host)

    clang --target=aarch64-linux-android26 -fuse-ld=lld -static -nostdlib -fno-stack-protector -fno-pie -O2 -Wl,-e,_start -Wl,--no-dynamic-linker -o susfs_abi_probe tests/susfs_abi_probe.c
    adb push susfs_abi_probe /data/local/tmp/
    adb shell chmod 755 /data/local/tmp/susfs_abi_probe
    adb shell /data/local/tmp/susfs_abi_probe
    adb shell rm -f /data/local/tmp/susfs_abi_probe

The probe neither needs root nor alters SUSFS configuration.

## Build hashes
Image.gz: 5b2175708cce31c6802af1bda315a7fd790288ee7b677760f3d7643d21b7c1dc
boot_a.img: c56241e94e714971546cc0b6c1f94a661dd9c6ceabf02bd37acf563680788c55

Raw device logs with private application/process details remain local.
