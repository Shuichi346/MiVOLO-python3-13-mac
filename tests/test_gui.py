import unittest
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
            meta=SimpleNamespace(use_persons=True, disable_faces=False),
        )
        self.received_image = None

    def recognize(self, image):
        self.received_image = image.copy()
        detected = SimpleNamespace(n_faces=1, n_persons=2)
        return detected, image.copy()


class GradioApplicationTests(unittest.TestCase):
    @patch("mivolo.gui.hf_hub_download", return_value="/cache/model.pth.tar")
    def test_default_checkpoint_uses_pinned_official_revision(self, download):
        with patch("mivolo.gui.os.getenv", return_value=None):
            resolved = gui._resolve_model_path(
                None,
                gui.CHECKPOINT_REPOSITORY,
                gui.CHECKPOINT_FILENAME,
                gui.CHECKPOINT_REVISION,
            )

        self.assertEqual(resolved, "/cache/model.pth.tar")
        download.assert_called_once_with(
            repo_id="iitolstykh/mivolo_v2",
            filename="mivolo_v2_384_0.15.pth.tar",
            revision="4eb4bb906ffd13ebbea70205691afbe30ccbc09e",
            token=None,
        )

    @patch("mivolo.gui._get_predictor")
    @patch("mivolo.gui.hf_hub_download")
    def test_build_app_does_not_load_or_download_models(self, download, get_predictor):
        app = gui.build_app()

        self.assertIsInstance(app, gr.Blocks)
        download.assert_not_called()
        get_predictor.assert_not_called()

    def test_inference_converts_color_and_propagates_options(self):
        predictor = _FakePredictor()
        rgb_image = np.array([[[10, 20, 30]]], dtype=np.uint8)

        with (
            patch("mivolo.gui._resolve_model_path", side_effect=["detector.pt", "checkpoint.pth.tar"]),
            patch("mivolo.gui._get_predictor", return_value=predictor),
        ):
            output, status = gui.run_inference(
                rgb_image,
                0.35,
                0.65,
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

    @patch("mivolo.gui._resolve_model_path")
    def test_empty_input_returns_status_without_resolving_models(self, resolve_model_path):
        output, status = gui.run_inference(None, 0.4, 0.7, gui.MODE_FACE_PERSON, "auto", "", "")

        self.assertIsNone(output)
        self.assertIn("Upload an image", status)
        resolve_model_path.assert_not_called()


if __name__ == "__main__":
    unittest.main()
