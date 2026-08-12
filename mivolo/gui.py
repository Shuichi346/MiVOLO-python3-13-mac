"""Gradio 6 interface for local MiVOLO image inference."""

import argparse
import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional, Sequence

import gdown
import gradio as gr
import numpy as np
from huggingface_hub import hf_hub_download

from mivolo.predictor import Predictor
from mivolo.runtime import normalize_user_path

DETECTOR_REPOSITORY = "iitolstykh/YOLO-Face-Person-Detector"
DETECTOR_FILENAME = "yolov8x_person_face.pt"
CHECKPOINT_REPOSITORY = "iitolstykh/mivolo_v2"
CHECKPOINT_FILENAME = "mivolo_v2_384_0.15.pth.tar"
CHECKPOINT_REVISION = "4eb4bb906ffd13ebbea70205691afbe30ccbc09e"

MODEL_VOLO_IMDB_AGE = "volo_d1_imdb_age"
MODEL_VOLO_IMDB_AGE_GENDER = "volo_d1_imdb_age_gender"
MODEL_MIVOLO_IMDB_AGE_GENDER = "mivolo_d1_imdb_age_gender"
MODEL_VOLO_UTK_AGE = "volo_d1_utk_age"
MODEL_VOLO_UTK_AGE_GENDER = "volo_d1_utk_age_gender"
MODEL_MIVOLO_V2_LAGENDA = "mivolo_v2_lagenda"
DEFAULT_MODEL = MODEL_MIVOLO_V2_LAGENDA

MODE_FACE_PERSON = "Faces and persons"
MODE_PERSON = "Persons only"
MODE_FACE = "Faces only"

_CSS = """
.gradio-container { max-width: 1180px !important; }
.trust-note { border-left: 3px solid var(--border-color-primary); padding-left: 0.8rem; }
"""


@dataclass(frozen=True)
class PredictorConfig:
    detector_weights: str
    checkpoint: str
    device: str = "auto"
    with_persons: bool = True
    disable_faces: bool = False
    draw: bool = True


@dataclass(frozen=True)
class ModelSource:
    label: str
    filename: str
    repository: Optional[str] = None
    revision: Optional[str] = None
    google_drive_id: Optional[str] = None


MODEL_SOURCES = {
    MODEL_VOLO_IMDB_AGE: ModelSource(
        label="VOLO D1 — IMDB-cleaned — age (face only)",
        filename="model_only_age_imdb_4.29.pth.tar",
        google_drive_id="17ysOqgG3FUyEuxrV3Uh49EpmuOiGDxrq",
    ),
    MODEL_VOLO_IMDB_AGE_GENDER: ModelSource(
        label="VOLO D1 — IMDB-cleaned — age + gender (face only)",
        filename="model_imdb_age_gender_4.22.pth.tar",
        google_drive_id="1NlsNEVijX2tjMe8LBb1rI56WB_ADVHeP",
    ),
    MODEL_MIVOLO_IMDB_AGE_GENDER: ModelSource(
        label="MiVOLO D1 — IMDB-cleaned — age + gender (face + body)",
        filename="model_imdb_cross_person_4.22_99.46.pth.tar",
        google_drive_id="11i8pKctxz3wVkDBlWKvhYIh7kpVFXSZ4",
    ),
    MODEL_VOLO_UTK_AGE: ModelSource(
        label="VOLO D1 — UTKFace — age (face only)",
        filename="model_age_utk_4.23.pth.tar",
        google_drive_id="1LtDfAJrWrw-QA9U5IuC3_JImbvAQhrJE",
    ),
    MODEL_VOLO_UTK_AGE_GENDER: ModelSource(
        label="VOLO D1 — UTKFace — age + gender (face only)",
        filename="model_utk_age_gender_4.23_97.69.pth.tar",
        google_drive_id="1hKFmIR6fjHMevm-a9uPEAkDLrTAh-W4D",
    ),
    MODEL_MIVOLO_V2_LAGENDA: ModelSource(
        label="MiVOLO v2 D1 384×384 — Lagenda — age + gender (face + body)",
        repository=CHECKPOINT_REPOSITORY,
        filename=CHECKPOINT_FILENAME,
        revision=CHECKPOINT_REVISION,
    ),
}
MODEL_CHOICES = tuple((source.label, model_id) for model_id, source in MODEL_SOURCES.items())


def _resolve_model_path(
    custom_path: Optional[str],
    repository: str,
    filename: str,
    revision: Optional[str] = None,
) -> str:
    if custom_path and custom_path.strip():
        path = normalize_user_path(custom_path)
        if not path.is_file():
            raise FileNotFoundError(f"Trusted model file not found: {path}")
        return str(path)

    token = os.getenv("HF_TOKEN") or None
    return hf_hub_download(repo_id=repository, filename=filename, revision=revision, token=token)


def _model_cache_directory() -> Path:
    cache_root = Path(os.getenv("XDG_CACHE_HOME", Path.home() / ".cache")).expanduser()
    return cache_root / "mivolo"


def _resolve_checkpoint_path(model_id: str, custom_path: Optional[str]) -> str:
    if custom_path and custom_path.strip():
        path = normalize_user_path(custom_path)
        if not path.is_file():
            raise FileNotFoundError(f"Trusted model file not found: {path}")
        return str(path)

    source = MODEL_SOURCES.get(model_id)
    if source is None:
        raise ValueError(f"Unknown model selection: {model_id}")

    if source.google_drive_id:
        url = f"https://drive.google.com/uc?id={source.google_drive_id}"
        cache_path = _model_cache_directory() / source.filename
        return gdown.cached_download(url=url, path=str(cache_path), quiet=False)

    if not source.repository:
        raise ValueError(f"No download source is configured for: {source.label}")
    return _resolve_model_path(None, source.repository, source.filename, source.revision)


@lru_cache(maxsize=8)
def _get_predictor(detector_path: str, checkpoint_path: str, device: str) -> Predictor:
    config = PredictorConfig(
        detector_weights=detector_path,
        checkpoint=checkpoint_path,
        device=device,
    )
    return Predictor(config, verbose=True)


def _configure_mode(predictor: Predictor, mode: str) -> None:
    if mode == MODE_FACE_PERSON:
        predictor.age_gender_model.meta.use_persons = predictor.age_gender_model.meta.with_persons_model
        predictor.age_gender_model.meta.disable_faces = False
    elif mode == MODE_PERSON:
        if not predictor.age_gender_model.meta.with_persons_model:
            raise ValueError("The selected face-only model does not support persons-only inference.")
        predictor.age_gender_model.meta.use_persons = True
        predictor.age_gender_model.meta.disable_faces = True
    elif mode == MODE_FACE:
        predictor.age_gender_model.meta.use_persons = False
        predictor.age_gender_model.meta.disable_faces = False
    else:
        raise ValueError(f"Unknown inference mode: {mode}")


def run_inference(
    image: Optional[np.ndarray],
    confidence: float,
    iou: float,
    model_id: str,
    mode: str,
    device: str,
    detector_path: Optional[str],
    checkpoint_path: Optional[str],
):
    """Run one GUI inference request and return RGB output plus status."""

    if image is None:
        return None, "Upload an image before running inference."
    if image.ndim != 3 or image.shape[2] != 3:
        return None, "Input must be a three-channel RGB image."

    try:
        resolved_detector = _resolve_model_path(detector_path, DETECTOR_REPOSITORY, DETECTOR_FILENAME)
        resolved_checkpoint = _resolve_checkpoint_path(model_id, checkpoint_path)
        predictor = _get_predictor(resolved_detector, resolved_checkpoint, device)

        predictor.detector.detector_kwargs["conf"] = float(confidence)
        predictor.detector.detector_kwargs["iou"] = float(iou)
        _configure_mode(predictor, mode)

        bgr_image = np.ascontiguousarray(image[:, :, ::-1])
        detected_objects, output_image = predictor.recognize(bgr_image)
        if output_image is None:
            raise RuntimeError("The predictor did not return an annotated image.")

        rgb_output = np.ascontiguousarray(output_image[:, :, ::-1])
        status = (
            f"Completed on {predictor.age_gender_model.device}: "
            f"{detected_objects.n_faces} face(s), {detected_objects.n_persons} person(s)."
        )
        return rgb_output, status
    except (gdown.exceptions.DownloadError, OSError, RuntimeError, ValueError) as error:
        return None, f"Error: {error}"


def build_app() -> gr.Blocks:
    """Construct the Gradio component tree without loading model weights."""

    with gr.Blocks(title="MiVOLO Age and Gender Estimation") as app:
        gr.Markdown(
            "# MiVOLO\n"
            "Estimate age and gender from an image using face and person context. "
            "Selected model files download only when inference first runs."
        )
        gr.Markdown(
            "Custom `.pt` and `.pth.tar` files may contain executable pickle data. "
            "Only select model files you trust.",
            elem_classes=["trust-note"],
        )

        with gr.Row():
            with gr.Column():
                input_image = gr.Image(label="Input image", type="numpy", image_mode="RGB")
                with gr.Row():
                    confidence = gr.Slider(0.0, 1.0, value=0.4, step=0.05, label="Confidence")
                    iou = gr.Slider(0.0, 1.0, value=0.7, step=0.05, label="IoU")
                model_id = gr.Dropdown(
                    choices=MODEL_CHOICES,
                    value=DEFAULT_MODEL,
                    label="Model",
                    info="README checkpoints download only when first selected for inference.",
                )
                mode = gr.Radio(
                    choices=(MODE_FACE_PERSON, MODE_PERSON, MODE_FACE),
                    value=MODE_FACE_PERSON,
                    label="Inference mode",
                )
                device = gr.Dropdown(
                    choices=("auto", "mps", "cpu"),
                    value="auto",
                    label="Device",
                    info="Auto prefers Apple MPS and falls back to CPU.",
                )
                with gr.Accordion("Trusted local model files (optional)", open=False):
                    detector_path = gr.Textbox(
                        label="Detector weights",
                        placeholder="Leave empty to download the documented default",
                    )
                    checkpoint_path = gr.Textbox(
                        label="Custom MiVOLO checkpoint",
                        placeholder="Leave empty to use the selected model",
                    )
                with gr.Row():
                    clear_button = gr.Button("Clear")
                    run_button = gr.Button("Run inference", variant="primary")

            with gr.Column():
                output_image = gr.Image(label="Annotated result", type="numpy", image_mode="RGB")
                status = gr.Markdown("Ready. Model files have not been loaded.")

        inputs = [input_image, confidence, iou, model_id, mode, device, detector_path, checkpoint_path]
        run_button.click(
            fn=run_inference,
            inputs=inputs,
            outputs=[output_image, status],
            api_visibility="private",
        )
        clear_button.click(
            fn=lambda: (None, None, "Ready. Model files have not been loaded."),
            outputs=[input_image, output_image, status],
            api_visibility="private",
        )

    return app


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Launch the local MiVOLO Gradio interface.")
    parser.add_argument("--server-name", default="127.0.0.1", help="Interface to bind. Defaults to local-only.")
    parser.add_argument("--server-port", default=7860, type=int, help="Local Gradio port.")
    parser.add_argument("--inbrowser", action="store_true", help="Open the interface in the default browser.")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = get_parser().parse_args(argv)
    app = build_app()
    app.launch(
        server_name=args.server_name,
        server_port=args.server_port,
        inbrowser=args.inbrowser,
        theme=gr.themes.Soft(),
        css=_CSS,
    )
