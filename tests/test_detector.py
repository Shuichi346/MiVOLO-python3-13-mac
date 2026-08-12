import unittest
from unittest.mock import MagicMock, patch

import torch

from mivolo.model.yolo_detector import Detector


class DetectorConfigurationTests(unittest.TestCase):
    @patch("mivolo.model.yolo_detector.supports_half", return_value=False)
    @patch("mivolo.model.yolo_detector.resolve_device", return_value=torch.device("cpu"))
    @patch("mivolo.model.yolo_detector.YOLO")
    def test_detector_uses_current_ultralytics_precision_argument(
        self,
        yolo_class,
        _resolve_device,
        _supports_half,
    ):
        yolo = MagicMock()
        yolo.model.names = {0: "person", 1: "face"}
        yolo_class.return_value = yolo

        detector = Detector("detector.pt", device="cpu")

        self.assertNotIn("half", detector.detector_kwargs)
        self.assertIsNone(detector.detector_kwargs["quantize"])
        self.assertEqual(detector.detector_kwargs["device"], "cpu")


if __name__ == "__main__":
    unittest.main()
