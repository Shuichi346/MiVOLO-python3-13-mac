# Changelog

## 0.7.0 (12.08.2026)

### Added

- Added Python 3.13+ project metadata, uv lockfile, and repository-local environment workflow.
- Added a Gradio 6 image interface with lazy documented model downloads and local-only binding.
- Added a Gradio model dropdown for all six downloadable README checkpoints, with MiVOLO v2 retained as the default.
- Added an official version-pinned download source for the legacy MiVOLO checkpoint.
- Added an explicit OmegaConf dependency required by the documented detector checkpoint.
- Added shared macOS path normalization and automatic MPS/CPU device selection.
- Added optional project-root `.env` configuration for `HF_TOKEN`, with process environment precedence.

### Changed

- Replaced executable `setup.py` metadata parsing with declarative PEP 517 packaging.
- Updated timm, PyTorch, Ultralytics, and Hugging Face integrations to current supported APIs.
- Updated validation, timing, and dataset-preparation utilities to the shared MPS/CPU device policy.
- Moved command-line behavior into the `mivolo-cli` entry point while retaining `demo.py` compatibility.
- Restricted legacy checkpoint loading instead of automatically falling back to unsafe pickle deserialization.
- Replaced Ultralytics' deprecated `half` inference argument with the current `quantize` argument.

## 0.4.1dev (15.08.2023)

### Added
- Added support for video streams, including YouTube URLs.
- Added instructions and explanations for various export types.

### Changed
- Removed CutOff operation. It has been proven to be ineffective for inference time and quite costly at the same time. Now it is only used during training.

## 0.4.2dev (22.09.2023)

### Added

- Added a script to convert AgeDB datasets to CSV format.
- Added metrics to the README.
