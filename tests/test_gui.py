import os
import tempfile
import unittest
from contextlib import chdir
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import gradio as gr
import numpy as np
from mivolo import gui


class _FakePredictor:
    def __init__(self):
        self.detector = SimpleNamespace(detector_kwargs={})
        self.age_gender_model = SimpleNamespace(
            device="cpu",
            meta=SimpleNamespace(use_persons=True, disable_faces=False, with_persons_model=True),
        )
        self.received_image = None

    def recognize(self, image):
        self.received_image = image.copy()
        detected = SimpleNamespace(n_faces=1, n_persons=2)
        return detected, image.copy()


class GradioApplicationTests(unittest.TestCase):
    @patch("mivolo.gui.hf_hub_download", return_value="/cache/model.pth.tar")
    def test_default_checkpoint_uses_pinned_official_revision(self, download):
        with (
            patch("mivolo.gui.load_dotenv"),
            patch("mivolo.gui.os.getenv", return_value=None),
        ):
            resolved = gui._resolve_checkpoint_path(gui.DEFAULT_MODEL, None)

        self.assertEqual(resolved, "/cache/model.pth.tar")
        download.assert_called_once_with(
            repo_id="iitolstykh/mivolo_v2",
            filename="mivolo_v2_384_0.15.pth.tar",
            revision="4eb4bb906ffd13ebbea70205691afbe30ccbc09e",
            token=None,
        )

    @patch("mivolo.gui.hf_hub_download", return_value="/cache/model.pth.tar")
    def test_hugging_face_token_loads_from_project_dotenv(self, download):
        with tempfile.TemporaryDirectory() as directory:
            project_directory = Path(directory)
            (project_directory / ".env").write_text("HF_TOKEN=test-token\n", encoding="utf-8")

            with chdir(project_directory), patch.dict(os.environ, {}, clear=True):
                resolved = gui._resolve_model_path(None, "example/models", "model.pt")

        self.assertEqual(resolved, "/cache/model.pth.tar")
        download.assert_called_once_with(
            repo_id="example/models",
            filename="model.pt",
            revision=None,
            token="test-token",
        )

    @patch("mivolo.gui.hf_hub_download", return_value="/cache/model.pth.tar")
    def test_process_hugging_face_token_takes_precedence_over_dotenv(self, download):
        with tempfile.TemporaryDirectory() as directory:
            project_directory = Path(directory)
            (project_directory / ".env").write_text("HF_TOKEN=file-token\n", encoding="utf-8")

            with chdir(project_directory), patch.dict(os.environ, {"HF_TOKEN": "process-token"}, clear=True):
                gui._resolve_model_path(None, "example/models", "model.pt")

        self.assertEqual(download.call_args.kwargs["token"], "process-token")

    @patch("mivolo.gui._model_cache_directory", return_value=Path("/cache/mivolo"))
    @patch("mivolo.gui.gdown.cached_download", return_value="/cache/mivolo/model.pth.tar")
    def test_readme_google_drive_checkpoint_uses_lazy_cache(self, cached_download, _cache_directory):
        resolved = gui._resolve_checkpoint_path(gui.MODEL_VOLO_IMDB_AGE, None)

        self.assertEqual(resolved, "/cache/mivolo/model.pth.tar")
        cached_download.assert_called_once_with(
            url="https://drive.google.com/uc?id=17ysOqgG3FUyEuxrV3Uh49EpmuOiGDxrq",
            path="/cache/mivolo/model_only_age_imdb_4.29.pth.tar",
            quiet=False,
        )

    def test_model_catalog_matches_downloadable_readme_checkpoints(self):
        self.assertEqual(len(gui.MODEL_SOURCES), 6)
        self.assertEqual(sum(source.google_drive_id is not None for source in gui.MODEL_SOURCES.values()), 5)
        self.assertEqual(gui.MODEL_SOURCES[gui.DEFAULT_MODEL].filename, gui.CHECKPOINT_FILENAME)

    @patch("mivolo.gui._get_predictor")
    @patch("mivolo.gui.gdown.cached_download")
    @patch("mivolo.gui.hf_hub_download")
    def test_build_app_does_not_load_or_download_models(self, hf_download, gdown_download, get_predictor):
        app = gui.build_app()

        self.assertIsInstance(app, gr.Blocks)
        config = app.get_config_file()
        model_component = next(
            component for component in config["components"] if component["props"].get("label") == "Model"
        )
        configured_choices = tuple(tuple(choice) for choice in model_component["props"]["choices"])

        self.assertEqual(configured_choices, gui.MODEL_CHOICES)
        self.assertEqual(model_component["props"]["value"], gui.DEFAULT_MODEL)
        hf_download.assert_not_called()
        gdown_download.assert_not_called()
        get_predictor.assert_not_called()

    def test_inference_converts_color_and_propagates_options(self):
        predictor = _FakePredictor()
        rgb_image = np.array([[[10, 20, 30]]], dtype=np.uint8)

        with (
            patch("mivolo.gui._resolve_model_path", return_value="detector.pt"),
            patch("mivolo.gui._resolve_checkpoint_path", return_value="checkpoint.pth.tar"),
            patch("mivolo.gui._get_predictor", return_value=predictor),
        ):
            output, status = gui.run_inference(
                rgb_image,
                0.35,
                0.65,
                gui.DEFAULT_MODEL,
                gui.MODE_PERSON,
                "cpu",
                None,
                None,
            )

        np.testing.assert_array_equal(predictor.received_image, np.array([[[30, 20, 10]]], dtype=np.uint8))
        np.testing.assert_array_equal(output, rgb_image)
        self.assertEqual(predictor.detector.detector_kwargs["conf"], 0.35)
        self.assertEqual(predictor.detector.detector_kwargs["iou"], 0.65)
        self.assertTrue(predictor.age_gender_model.meta.use_persons)
        self.assertTrue(predictor.age_gender_model.meta.disable_faces)
        self.assertIn("1 face(s), 2 person(s)", status)

    def test_persons_only_mode_rejects_face_only_checkpoint(self):
        predictor = _FakePredictor()
        predictor.age_gender_model.meta.with_persons_model = False
        rgb_image = np.array([[[10, 20, 30]]], dtype=np.uint8)

        with (
            patch("mivolo.gui._resolve_model_path", return_value="detector.pt"),
            patch("mivolo.gui._resolve_checkpoint_path", return_value="checkpoint.pth.tar"),
            patch("mivolo.gui._get_predictor", return_value=predictor),
        ):
            output, status = gui.run_inference(
                rgb_image,
                0.4,
                0.7,
                gui.MODEL_VOLO_IMDB_AGE,
                gui.MODE_PERSON,
                "cpu",
                None,
                None,
            )

        self.assertIsNone(output)
        self.assertIn("face-only model does not support persons-only", status)
        self.assertIsNone(predictor.received_image)

    @patch("mivolo.gui.build_app")
    def test_main_passes_app_settings_to_launch(self, build_app):
        app = MagicMock()
        build_app.return_value = app

        gui.main(["--server-port", "7861"])

        launch_arguments = app.launch.call_args.kwargs
        self.assertEqual(launch_arguments["server_name"], "127.0.0.1")
        self.assertEqual(launch_arguments["server_port"], 7861)
        self.assertIn("theme", launch_arguments)
        self.assertIn("css", launch_arguments)

    @patch("mivolo.gui._resolve_checkpoint_path")
    @patch("mivolo.gui._resolve_model_path")
    def test_empty_input_returns_status_without_resolving_models(self, resolve_model_path, resolve_checkpoint_path):
        output, status = gui.run_inference(
            None,
            0.4,
            0.7,
            gui.DEFAULT_MODEL,
            gui.MODE_FACE_PERSON,
            "auto",
            "",
            "",
        )

        self.assertIsNone(output)
        self.assertIn("Upload an image", status)
        resolve_model_path.assert_not_called()
        resolve_checkpoint_path.assert_not_called()


if __name__ == "__main__":
    unittest.main()
