"""Command-line interface for MiVOLO inference."""

import argparse
import logging
from pathlib import Path
from typing import Optional, Sequence
from urllib.parse import urlparse

import cv2
import yt_dlp
from mivolo.data.data_reader import InputType, get_all_files, get_input_type
from mivolo.predictor import Predictor
from mivolo.runtime import normalize_user_path
from timm.utils import setup_default_logging

_logger = logging.getLogger("inference")


def _is_remote_source(value: str) -> bool:
    return urlparse(value).scheme.lower() in {"http", "https", "rtmp", "rtsp"}


def get_direct_video_url(video_url: str):
    ydl_opts = {
        "format": "bestvideo",
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)

    if "url" in info_dict:
        direct_url = info_dict["url"]
        resolution = (info_dict["width"], info_dict["height"])
        return direct_url, resolution, info_dict["fps"], info_dict["id"]
    return None, None, None, None


def get_local_video_info(video_path: str):
    capture = cv2.VideoCapture(video_path)
    try:
        if not capture.isOpened():
            raise ValueError(f"Failed to open video source: {video_path}")
        resolution = (
            int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        )
        return resolution, capture.get(cv2.CAP_PROP_FPS)
    finally:
        capture.release()


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MiVOLO age and gender inference")
    parser.add_argument("--input", required=True, help="Image, image folder, video, or video stream URL.")
    parser.add_argument("--output", required=True, help="Folder for output results.")
    parser.add_argument("--detector-weights", required=True, help="Trusted YOLO face/person detector weights.")
    parser.add_argument("--checkpoint", required=True, help="Trusted MiVOLO checkpoint.")
    parser.add_argument(
        "--with-persons",
        action="store_true",
        help="Use person crops when the checkpoint supports them.",
    )
    parser.add_argument(
        "--disable-faces",
        action="store_true",
        help="Use only person crops when available.",
    )
    parser.add_argument("--draw", action="store_true", help="Write annotated images or video.")
    parser.add_argument(
        "--device",
        choices=("auto", "mps", "cpu"),
        default="auto",
        help="Inference device. Auto prefers MPS and falls back to CPU.",
    )
    return parser


def _normalize_local_arguments(args: argparse.Namespace) -> Path:
    if not _is_remote_source(args.input):
        args.input = str(normalize_user_path(args.input))

    output_dir = normalize_user_path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    args.output = str(output_dir)

    for attribute, label in (
        ("detector_weights", "Detector weights"),
        ("checkpoint", "MiVOLO checkpoint"),
    ):
        path = normalize_user_path(getattr(args, attribute))
        if not path.is_file():
            raise FileNotFoundError(f"{label} not found: {path}")
        setattr(args, attribute, str(path))

    return output_dir


def _process_video(args: argparse.Namespace, predictor: Predictor, output_dir: Path) -> None:
    if not args.draw:
        raise ValueError("Video processing requires --draw so results can be written.")

    source = args.input
    if "youtube.com" in source or "youtu.be" in source:
        source, resolution, fps, video_id = get_direct_video_url(source)
        if not source:
            raise ValueError("Failed to resolve the YouTube video URL.")
        output_path = output_dir / f"out_{video_id}.avi"
    else:
        name = Path(urlparse(source).path).stem or "video"
        output_path = output_dir / f"out_{name}.avi"
        resolution, fps = get_local_video_info(source)

    writer = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"XVID"),
        fps,
        resolution,
    )
    if not writer.isOpened():
        raise ValueError(f"Failed to create output video: {output_path}")

    _logger.info("Saving result to %s", output_path)
    try:
        for _, frame in predictor.recognize_video(source):
            writer.write(frame)
    finally:
        writer.release()


def _process_images(args: argparse.Namespace, predictor: Predictor, output_dir: Path) -> None:
    input_path = Path(args.input)
    image_files = get_all_files(str(input_path)) if input_path.is_dir() else [str(input_path)]

    for image_path in image_files:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to read image: {image_path}")
        _, output_image = predictor.recognize(image)

        if args.draw:
            if output_image is None:
                raise RuntimeError("Predictor did not return an annotated image.")
            output_path = output_dir / f"out_{Path(image_path).stem}.jpg"
            if not cv2.imwrite(str(output_path), output_image):
                raise ValueError(f"Failed to write output image: {output_path}")
            _logger.info("Saved result to %s", output_path)


def main(argv: Optional[Sequence[str]] = None) -> int:
    setup_default_logging()
    args = get_parser().parse_args(argv)
    output_dir = _normalize_local_arguments(args)
    predictor = Predictor(args, verbose=True)

    input_type = get_input_type(args.input)
    if input_type in {InputType.Video, InputType.VideoStream}:
        _process_video(args, predictor, output_dir)
    else:
        _process_images(args, predictor, output_dir)
    return 0
