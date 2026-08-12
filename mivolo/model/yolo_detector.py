from typing import Dict, Union

import numpy as np
import PIL
from ultralytics import YOLO
from ultralytics.engine.results import Results

from mivolo.runtime import resolve_device, supports_half
from mivolo.structures import PersonAndFaceResult


class Detector:
    def __init__(
        self,
        weights: str,
        device: str = "auto",
        half: bool = True,
        verbose: bool = False,
        conf_thresh: float = 0.4,
        iou_thresh: float = 0.7,
    ):
        self.yolo = YOLO(weights)
        self.yolo.fuse()

        self.device = resolve_device(device)
        self.half = half and supports_half(self.device)

        if self.half:
            self.yolo.model = self.yolo.model.half()

        self.detector_names: Dict[int, str] = self.yolo.model.names

        # init yolo.predictor
        self.detector_kwargs = {
            "conf": conf_thresh,
            "iou": iou_thresh,
            "quantize": 16 if self.half else None,
            "verbose": verbose,
            "device": str(self.device),
        }
        # self.yolo.predict(**self.detector_kwargs)

    def predict(self, image: Union[np.ndarray, str, "PIL.Image"]) -> PersonAndFaceResult:
        results: Results = self.yolo.predict(image, **self.detector_kwargs)[0]
        return PersonAndFaceResult(results)

    def track(self, image: Union[np.ndarray, str, "PIL.Image"]) -> PersonAndFaceResult:
        results: Results = self.yolo.track(image, persist=True, **self.detector_kwargs)[0]
        return PersonAndFaceResult(results)
