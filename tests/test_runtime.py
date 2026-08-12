import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from mivolo.runtime import normalize_user_path, resolve_device, supports_half


class NormalizeUserPathTests(unittest.TestCase):
    def test_accepts_quoted_and_escaped_macos_paths(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            expected = Path(temporary_directory, "folder name").resolve()
            expected.mkdir()

            self.assertEqual(normalize_user_path(f"'{expected}'"), expected)
            self.assertEqual(normalize_user_path(str(expected).replace(" ", "\\ ")), expected)

    def test_rejects_empty_path(self):
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            normalize_user_path("  ")


class ResolveDeviceTests(unittest.TestCase):
    @patch("mivolo.runtime.torch.backends.mps.is_available", return_value=True)
    def test_auto_prefers_mps(self, _is_available):
        self.assertEqual(resolve_device("auto").type, "mps")

    @patch("mivolo.runtime.torch.backends.mps.is_available", return_value=False)
    def test_auto_falls_back_to_cpu(self, _is_available):
        self.assertEqual(resolve_device("auto").type, "cpu")

    @patch("mivolo.runtime.torch.backends.mps.is_built", return_value=True)
    @patch("mivolo.runtime.torch.backends.mps.is_available", return_value=False)
    def test_explicit_unavailable_mps_raises(self, _is_available, _is_built):
        with self.assertRaisesRegex(ValueError, "not available"):
            resolve_device("mps")

    def test_rejects_unsupported_device_and_disables_half_precision(self):
        with self.assertRaisesRegex(ValueError, "auto.*mps.*cpu"):
            resolve_device("cuda")
        self.assertFalse(supports_half(resolve_device("cpu")))


if __name__ == "__main__":
    unittest.main()
