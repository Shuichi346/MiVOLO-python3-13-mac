# Development Notes

## 2026-08-12

- The upstream Git install failed during metadata generation because `setup.py` imported `pkg_resources`, which is no
  longer guaranteed inside isolated modern build environments. Project metadata now lives in `pyproject.toml`; the
  retained `setup.py` is only a metadata-free compatibility shim.
- uv is the authoritative environment manager. `.python-version` selects Python 3.13, `uv.lock` freezes the resolved
  environment, and `.venv` remains local and ignored.
- The macOS runtime supports MPS and CPU only. `auto` selects MPS when available and otherwise CPU; both use full
  precision because the legacy model has not established safe half-precision MPS behavior. Validation, timing,
  data-loading, and dataset-preparation utilities follow the same policy.
- Gradio app construction is intentionally offline. Default detector and MiVOLO checkpoint downloads happen only on
  the first inference and use the Hugging Face cache. The legacy checkpoint is pinned to the official
  `iitolstykh/mivolo_v2` revision that still contains the original `.pth.tar` file.
- Legacy PyTorch and Ultralytics weight files are a trust boundary. The MiVOLO checkpoint loader uses restricted
  `weights_only=True` loading and reports incompatible pickle globals instead of silently enabling executable pickle.
- The documented Ultralytics detector serializes OmegaConf metadata, so OmegaConf is declared directly instead of
  relying on Ultralytics' pip-based runtime auto-install fallback.
- Gradio 6 app-level theme and CSS settings belong to `Blocks.launch()`, while `Blocks()` contains only the component
  tree.
