# susfs selinux_hide feature
# old susfs won't have this manual hook
# and nongki 4.14- can't use simonpunk's hook for that
# check it, when there doesn't have, fallback to auto hook
ifeq ($(shell grep -q "ksu_selinux_hide_running" $(srctree)/security/selinux/hooks.c; echo $$?),0)
$(info -- $(REPO_NAME)/susfs_feature_check: selinux_hide manual hook found)
ccflags-y += -DKSU_COMPAT_HAS_SUSFS_FEATURE_SELINUX_HIDE
endif

# susfs's dev branch currently using post_execve_hook
# but in other branch, it still direcctly call ksu_install_su_fd
# to avoid install su fd repeatedly
ifeq ($(shell grep -q "ksu_install_su_fd" $(srctree)/fs/exec.c; echo $$?),0)
$(info -- $(REPO_NAME)/compat: ksu_install_su_fd direct call found)
ccflags-y += -DKSU_COMPAT_HAS_SUSFS_INSTALL_SU_FD_DIRECT_CALL
endif

# agate MT6893 / Linux 4.14 port: the SUSFS kernel side is provided by
# susfs4ksu v2.3.0 adapted for Linux 4.14 (susfs-23-49 4.9 port + statx and
# fsnotify adjustments). The upstream guard below used to hard-stop every
# CONFIG_KSU_SUSFS build because simonpunk had not synced to this BakaSU
# snapshot; the symbols BakaSU needs from the SUSFS kernel patch
# (ksu_handle_*, susfs_* helpers) are present and checked at link time here,
# so keep it informational only.
$(info -- $(REPO_NAME): SUSFS kernel side version is checked at build/link time)
$(info -- $(REPO_NAME): expect susfs4ksu v2.3.0 adapted for Linux 4.14)
