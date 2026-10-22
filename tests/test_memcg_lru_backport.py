"""Static/source invariants + model semantics for the 4.14 memcg LRU backport.

This is NOT a device test or a test of kernel concurrency.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
HEADER = (ROOT / "include/linux/memcontrol.h").read_text()
IMPL = (ROOT / "mm/memcontrol.c").read_text()


def visible_pages(count: int) -> int:
    return max(0, count)


class MemcgLruAccountingTest(unittest.TestCase):
    def test_signed_deficit_remains_for_later_recovery(self):
        count = 0
        count -= 1
        self.assertEqual(count, -1)
        self.assertEqual(visible_pages(count), 0)
        count += 1
        self.assertEqual(count, 0)
        count += 2
        self.assertEqual(visible_pages(count), 2)

    def test_normal_counter_is_unchanged(self):
        count = 6
        for delta in [2, -5, -1, 0, 3]:
            count += delta
        self.assertEqual(count, 5)
        self.assertEqual(visible_pages(count), 5)

    def test_header_uses_signed_counter_and_safe_readers(self):
        self.assertIn("long\t\t\tlru_zone_size[MAX_NR_ZONES][NR_LRU_LISTS];", HEADER)
        self.assertIn("WARN_ON_ONCE(size < 0)", HEADER)
        self.assertIn("mem_cgroup_lru_size_or_zero", HEADER)
        # Per-zone and aggregate consumers both pass through helper.
        self.assertGreaterEqual(HEADER.count("mem_cgroup_lru_size_or_zero("), 3)

    def test_hot_path_keeps_signed_value_and_does_not_hide_warning(self):
        function = IMPL.split("void mem_cgroup_update_lru_size(", 1)[1].split(
            "\nbool task_in_mem_cgroup(", 1
        )[0]
        self.assertIn("mz->lru_zone_size[zid][lru] += nr_pages;", function)
        self.assertNotIn("WARN_ONCE(", function)
        self.assertNotIn("VM_BUG_ON(", function)
        self.assertNotIn("*lru_size = 0", function)


if __name__ == "__main__":
    unittest.main()
