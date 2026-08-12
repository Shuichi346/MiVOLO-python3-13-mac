"""Runtime helpers shared by the command-line and graphical interfaces."""

import os
import shlex
from pathlib import Path
from typing import Union

import torch

PathInput = Union[str, os.PathLike[str]]


def normalize_user_path(value: PathInput) -> Path:
    """Return an absolute path from Finder- or Terminal-formatted input."""

    text = os.fspath(value).strip().strip("'\"")
    if not text:
        raise ValueError("Path cannot be empty.")

    if "\\" in text:
        parts = shlex.split(text)
        if len(parts) != 1:
            raise ValueError(f"Expected one filesystem path, received {len(parts)} values.")
        text = parts[0]

    return Path(text).expanduser().resolve()


def resolve_device(requested: str = "auto") -> torch.device:
    """Resolve the requested macOS inference device without silent coercion."""

    normalized = requested.strip().lower()
    if normalized == "auto":
        normalized = "mps" if torch.backends.mps.is_available() else "cpu"

    if normalized == "mps":
        if not torch.backends.mps.is_built():
            raise ValueError("MPS is not included in this PyTorch build. Choose 'cpu'.")
        if not torch.backends.mps.is_available():
            raise ValueError("MPS is not available on this Mac. Choose 'cpu'.")
        return torch.device("mps")

    if normalized == "cpu":
        return torch.device("cpu")

    raise ValueError("Unsupported device. Choose 'auto', 'mps', or 'cpu'.")


def supports_half(device: torch.device) -> bool:
    """Return whether MiVOLO should use half precision on this macOS fork."""

    del device
    return False
