# Flashing and recovery notes

**Experimental kernel. No stable release.**

The BakaSU + legacy SUSFS image has booted once on Xiaomi 11T running crDroid v12.10-20260518 (Android 16). Long-term stability, independent app root grants, and individual SUSFS operations are not yet established.

The memory-cgroup accounting source was changed after that device test. A successful new build does not constitute a retest, and no automatic flashing is performed by the build script.

The output of build-agate.sh is an ARM64 kernel Image.gz, **not** a complete Android boot image or a flashable ZIP. A boot image must match the ROM, partition layout, DTB and ramdisk. Wrong images can leave the phone unable to boot.

Preserve known-working boot images for each slot and maintain a functioning fastboot/recovery path. Never overwrite a working fallback before another image has been validated. Device-specific flashing, rollback or root-grant testing must be conducted separately and intentionally by its owner.

Test details: docs/DEVICE_VALIDATION.md.
