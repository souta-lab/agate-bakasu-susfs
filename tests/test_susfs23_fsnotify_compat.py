"""Compile-stage ABI adapter invariants, not a feature or runtime test."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
S = (ROOT / "fs/notify/susfs23_fsnotify_compat_414.c").read_text()
H = (ROOT / "include/linux/susfs23_fsnotify_compat_414.h").read_text()

class TestCompat(unittest.TestCase):
    def test_correct_414_callback_signature(self):
        for field in ("struct fsnotify_group *group",
                      "struct fsnotify_mark *inode_mark",
                      "struct fsnotify_mark *vfsmount_mark",
                      "const unsigned char *file_name",
                      "struct fsnotify_iter_info *iter_info"):
            self.assertIn(field, S)

    def test_bounded_filename(self):
        self.assertIn("strnlen((const char *)file_name, NAME_MAX + 1)", S)
        self.assertIn("if (!n || n > NAME_MAX)", S)

    def test_no_auto_registration_or_mount_hooks(self):
        self.assertNotIn("fsnotify_add_inode_mark(", S)
        self.assertNotIn("sys_umount(", S)
        # Allocation and registration must be explicit, never part of init.
        self.assertIn("susfs23_fsnotify_compat_create_group_414(void)", S)
        self.assertIn("susfs23_fsnotify_compat_add_inode_mark_414(", S)
        self.assertNotIn("late_initcall(", S)
        self.assertNotIn("module_init(", S)
        self.assertIn(".handle_event = susfs23_handle_event_414", S)

    def test_name_hash_not_uninitialized(self):
        self.assertIn("full_name_hash(NULL, (const char *)file_name, n)", S)

    def test_414_mark_attach_api(self):
        self.assertIn("fsnotify_add_mark(mark, inode, NULL, 0)", S)
        self.assertNotIn("fsnotify_add_inode_mark(", S)
        self.assertIn(".free_mark = susfs23_fsnotify_free_mark_414", S)

    def test_ownership_release_order(self):
        remove = S.split("void susfs23_fsnotify_compat_remove_inode_mark_414(", 1)[1].split(
            "void susfs23_fsnotify_compat_destroy_group_414(", 1)[0]
        self.assertLess(remove.find("fsnotify_destroy_mark("), remove.find("fsnotify_put_mark("))

    def test_failure_releases_initial_reference(self):
        add = S.split("int susfs23_fsnotify_compat_add_inode_mark_414(", 1)[1].split(
            "void susfs23_fsnotify_compat_remove_inode_mark_414(", 1)[0]
        self.assertIn("if (ret)", add)
        self.assertIn("fsnotify_put_mark(mark);", add)
        self.assertIn("*out = NULL;", add)

    def test_group_creation_and_destruction(self):
        self.assertIn("fsnotify_alloc_group(&susfs23_fsnotify_compat_ops_414)", S)
        self.assertIn("fsnotify_destroy_group(group)", S)

    def test_header_exposes_ops(self):
        self.assertIn("extern const struct fsnotify_ops", H)

class TestOptInBuild(unittest.TestCase):
    def test_default_disabled(self):
        k = (ROOT / "fs/notify/Kconfig").read_text()
        section = k.split("config SUSFS23_FSNOTIFY_ABI_414", 1)[1].split(
            'source "fs/notify/dnotify/Kconfig"', 1
        )[0]
        self.assertIn("default n", section)
        self.assertIn("depends on FSNOTIFY && ARM64", section)

    def test_makefile_selects_adapter_only_with_flag(self):
        m = (ROOT / "fs/notify/Makefile").read_text()
        self.assertIn(
            "obj-$(CONFIG_SUSFS23_FSNOTIFY_ABI_414) += susfs23_fsnotify_compat_414.o",
            m
        )
