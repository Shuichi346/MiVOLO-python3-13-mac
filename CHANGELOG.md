
## 0.7.0 (12.08.2026)

### Added

- Python 3.13+ project metadata, uv lockfile, and repository-local environment workflow.
- Gradio 6 image interface with lazy documented model downloads and local-only binding.
- Official version-pinned download source for the legacy MiVOLO checkpoint.
- Explicit OmegaConf dependency required by the documented detector checkpoint.
- Shared macOS path normalization and automatic MPS/CPU device selection.
- Focused offline compatibility tests for packaging, runtime, CLI, and GUI behavior.

### Changed

- Replaced executable `setup.py` metadata parsing with declarative PEP 517 packaging.
- Updated timm, PyTorch, Ultralytics, and Hugging Face integrations to current supported APIs.
- Updated validation, timing, and dataset-preparation utilities to the shared MPS/CPU device policy.
- Moved command-line behavior into the `mivolo-cli` entry point while retaining `demo.py` compatibility.
- Restricted legacy checkpoint loading instead of automatically falling back to unsafe pickle deserialization.

## 0.4.1dev (15.08.2023)

### Added
- Support for video streams, including YouTube URLs
- Instructions and explanations for various export types.

### Changed
- Removed CutOff operation. It has been proven to be ineffective for inference time and quite costly at the same time. Now it is only used during training.

## 0.4.2dev (22.09.2023)

### Added

- Script for AgeDB dataset convertation to csv format
- Additional metrics were added to README
