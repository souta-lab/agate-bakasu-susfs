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
        self.assertNotIn("fsnotify_alloc_group(", S)
        self.assertNotIn("fsnotify_add_inode_mark(", S)
        self.assertNotIn("sys_umount(", S)
        self.assertIn(".handle_event = susfs23_handle_event_414", S)

    def test_name_hash_not_uninitialized(self):
        self.assertIn("full_name_hash(NULL, (const char *)file_name, n)", S)

    def test_header_exposes_ops(self):
        self.assertIn("extern const struct fsnotify_ops", H)
