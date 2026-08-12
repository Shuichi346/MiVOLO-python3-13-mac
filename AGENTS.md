# Repository Instructions

## Scope

This fork modernizes MiVOLO for Python 3.13+, uv, macOS, and Gradio 6 while preserving the original inference behavior and checkpoint format.

## Python and Dependencies

- Require Python 3.13 or newer; pin the local default in `.python-version`.
- Use `uv` as the only dependency and environment manager. Keep `pyproject.toml` and `uv.lock` authoritative and run commands through `uv run`.
- Do not add `pip`, Conda, Poetry, or CUDA-only setup paths to project workflows.
- Prefer public APIs from PyTorch, timm, Ultralytics, Gradio, and Hugging Face. Do not introduce new imports from private modules when a public API exists.
- On Apple Silicon, support `mps` and `cpu`; never assume CUDA exists. Use floating-point precision supported by the selected device.

## Runtime and UI

- Normalize every user-provided filesystem path before constructing a `Path`, including quoted and backslash-escaped macOS paths.
- Resolve any external executables by absolute path, checking `/opt/homebrew/bin` and `/usr/local/bin` when shell lookup fails.
- Bind Gradio locally to `127.0.0.1` unless the user explicitly requests another address.
- For Gradio 6, pass app-level theme, CSS, JavaScript, and head settings to `launch()`, not `Blocks()`.
- Treat downloaded PyTorch/Ultralytics model files as executable artifacts. Use only documented repositories by default and tell users to trust custom weights before loading them.

## Quality and Safety

- Follow PEP 8, use UTF-8, and prefer absolute imports.
- Preserve the legacy CLI while adding modern package entry points.
- Keep model downloads lazy so importing the package or building the GUI does not require network access.
- Do not commit model weights, generated media, `.venv`, caches, or secrets.
- Update `README.md`, `CHANGELOG.md`, and `NOTES.md` when behavior, setup, or compatibility decisions change.
- Execute and maintain `PLANS.md` as the durable implementation and verification state for the current migration.
