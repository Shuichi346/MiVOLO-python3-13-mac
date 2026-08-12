import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PackagingTests(unittest.TestCase):
    def test_project_metadata_uses_python_313_and_uv_entry_points(self):
        with (ROOT / "pyproject.toml").open("rb") as project_file:
            project = tomllib.load(project_file)

        self.assertEqual(project["project"]["requires-python"], ">=3.13")
        self.assertEqual(project["project"]["scripts"]["mivolo-cli"], "mivolo.cli:main")
        self.assertEqual(project["project"]["scripts"]["mivolo-gui"], "mivolo.gui:main")
        self.assertIn("omegaconf>=2.3.1,<3", project["project"]["dependencies"])
        self.assertIn("python-dotenv>=1.1,<2", project["project"]["dependencies"])
        self.assertEqual((ROOT / ".python-version").read_text(encoding="utf-8").strip(), "3.13")
        self.assertTrue((ROOT / "uv.lock").is_file())

    def test_legacy_install_files_delegate_without_pkg_resources(self):
        setup_source = (ROOT / "setup.py").read_text(encoding="utf-8")
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")

        self.assertNotIn("pkg_resources", setup_source)
        self.assertNotIn("requirements.txt", setup_source)
        self.assertIn("-e .", requirements)

    def test_shipped_runtime_and_scripts_have_no_cuda_paths(self):
        source_files = [
            *sorted((ROOT / "mivolo").rglob("*.py")),
            *sorted((ROOT / "tools").glob("*.py")),
            *sorted((ROOT / "scripts").glob("*.sh")),
            ROOT / "eval_pretrained.py",
            ROOT / "eval_tools.py",
            ROOT / "measure_time.py",
        ]

        for source_file in source_files:
            with self.subTest(source_file=source_file.relative_to(ROOT)):
                source = source_file.read_text(encoding="utf-8").lower()
                self.assertNotIn("cuda", source)
                self.assertNotIn("cublas", source)


if __name__ == "__main__":
    unittest.main()
