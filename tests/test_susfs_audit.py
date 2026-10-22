"""Static sanity checks for the API/version audit; no device dependencies."""
from pathlib import Path
import importlib.util
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "susfs_audit", ROOT / "tools/audit_susfs23_kernel_api.py"
)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class TestAudit(unittest.TestCase):
    def test_kernel_version(self):
        self.assertEqual(audit.kernel_version(ROOT), "4.14.336")

    def test_installed_susfs_version(self):
        self.assertEqual(
            audit.susfs_version(ROOT / "include/linux/susfs.h"), "v1.5.5"
        )

    def test_missing_license(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(audit.license_series(Path(d)), "unspecified")


if __name__ == "__main__":
    unittest.main()
