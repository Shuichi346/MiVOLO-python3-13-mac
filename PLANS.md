# Implementation Plan: Python 3.13+, uv, macOS, and Gradio 6 Modernization

This plan is a living document. Keep `Resume Here`, `Progress`, `Decision Log`, `Surprises & Discoveries`, and `Outcomes & Retrospective` current during execution.

## Overview

Modernize the stalled 2023 MiVOLO repository so a fresh checkout installs reproducibly with uv under Python 3.13 or newer, continues to install from Git without the removed `pkg_resources` import, selects a usable CPU/MPS inference device, and exposes both a maintained CLI and a local Gradio 6 image-inference GUI. The observable outcome is a green bounded test command plus one real local GUI inference using lazily downloaded public MiVOLO weights.

## Resume Here

- Updated: 2026-08-12 09:08Z
- Overall status: COMPLETE
- Active phase: None
- Active step: None
- Last verified checkpoint: Final Acceptance Command attempt 4/4 passed all 17 tests, then the final cached Gradio smoke returned an output image and `Completed on mps: 0 face(s), 0 person(s).`
- Completed since previous checkpoint: Added the declared OmegaConf dependency and lock resolution, passed final acceptance, completed real local MPS inference with both official cached model artifacts, and stopped browser/server sessions cleanly.
- In progress: None
- Next action: None
- Blockers / decisions needed: None
- Final verification: PASS — 4/4 attempts used; `uv run python -m unittest discover -s tests -v` exited 0 for the final dependency-repaired state; 17 tests passed; manual Gradio inference succeeded on MPS.
- Working tree state: `/Users/shuichi/Documents/GitHub/MiVOLO-python3-13-mac`; branch `codex/313`; HEAD `d5e5fc13383f43803646fff6c26792cdc5107045`; planned packaging, runtime, CLI, GUI, evaluation/tool, test, script, and documentation files are modified or untracked; `.venv` and Playwright artifacts are ignored; no staged changes.
- Evidence: Attempt 4/4 built `antlr4-python3-runtime==4.9.3`, installed OmegaConf through uv, rebuilt MiVOLO, and passed 17 tests in 0.056 seconds. The manual flow loaded the 68,125,494-parameter fused detector, ran the banner at 352x640 on MPS, returned a Gradio output image with zero detections, and shut down browser/server cleanly.

## Execution Contract

- At every session start or resume, read this entire plan and applicable repository instructions before editing.
- Treat Requirements, Boundaries, Steps, and Success Criteria as intended scope. Treat Success Criteria as the verification scope ceiling and the working tree plus bounded verification as evidence of actual completion.
- Reconcile `Resume Here` and `Progress` with repository evidence before choosing work. Preserve unrelated user changes.
- Before implementation, mark exactly one eligible step `IN_PROGRESS` and update `Resume Here`. After every material action or verification, record completed work, remaining work, evidence, and one exact next action.
- Use `[x]` only for a `COMPLETE` step with a UTC timestamp and verification evidence. Keep partial or blocked work unchecked and state the exact remainder or unblock condition.
- Checkpoint before and after risky or long-running operations, before approvals, and before an anticipated pause, handoff, or context compaction. Every stopping point must leave this file truthful if the current agent never returns.
- Do not skip dependencies, silently change scope, or repeat non-idempotent work without first detecting whether it already succeeded.
- Keep at most one step `IN_PROGRESS` unless this plan explicitly declares controlled parallel work and one coordinator owns plan updates.
- Run only verification declared by this plan and mapped to its Success Criteria. Do not add confidence tests, broad regression suites, coverage work, or unrelated fixes.
- Record a final-verification attempt before launching it. Never reset its finite attempt budget on resume or after a repair unless the user changes the contract.
- Treat the first in-budget exit `0` from the Final Acceptance Command as the automated green stop. Run no further automated checks afterward; only a predeclared one-pass manual smoke check that depends on the final artifact may follow.

## Stated Assumptions

1. Python 3.13 is the default and minimum supported runtime; `requires-python = ">=3.13"` intentionally permits later stable CPython versions whose dependencies can resolve.
2. The existing `.pth.tar` MiVOLO checkpoint format and `yolov8x_person_face.pt` detector remain the functional model contract; retraining, conversion to a new architecture, and MiVOLO-Next are out of scope.
3. The GUI is local-first and image-focused. Existing CLI video/URL behavior remains available but is not duplicated in the first Gradio surface.
4. Public Hugging Face model repositories may be downloaded lazily at first inference. A user-supplied `HF_TOKEN` is optional and must use the current `token=` API.
5. The working copy has no pre-existing user modifications beyond the planning artifacts created for this task.

## Requirements

1. A fresh checkout uses uv, creates `.venv`, selects Python 3.13 by default, and installs only from declarative project metadata and a committed lockfile.
2. `pip install git+https://github.com/...` uses PEP 517 metadata and cannot fail because `setup.py` imports `pkg_resources`.
3. Package metadata declares Python 3.13+, macOS support, maintained dependency ranges, and runnable `mivolo-cli` and `mivolo-gui` entry points.
4. Runtime device selection supports `auto`, `mps`, and `cpu`; this macOS fork contains no CUDA paths and avoids unsupported half-precision assumptions.
5. User-entered local paths work when pasted from macOS Finder or Terminal with quotes or escaped spaces.
6. Current PyTorch, timm, and Ultralytics APIs can import and construct the MiVOLO inference pipeline without obsolete private-module failures.
7. The Gradio app uses Gradio 6 APIs, binds to `127.0.0.1` by default, downloads default weights only on first inference, exposes image, thresholds, inference mode, device, and optional trusted local weight paths, and returns an annotated RGB image plus a concise status.
8. The legacy `python demo.py ...` workflow remains a compatible shim and documents uv-based equivalents.
9. Automated tests cover packaging/imports, path/device behavior, and GUI construction/inference adaptation without downloading model weights; one bounded real GUI smoke check covers the integrated artifact.
10. README, changelog, notes, ignore rules, and repository instructions explain the supported workflow and macOS limitations.

## Tech Stack and Conventions

- Runtime: CPython 3.13+; local default `3.13` in `.python-version`.
- Environment/package manager: uv project mode; `pyproject.toml`, `.python-version`, `.venv`, and checked-in `uv.lock` per official uv project guidance.
- Build backend: current maintained PEP 517 backend with declarative metadata; preserve a metadata-only `setup.py` shim if retained, but it must not parse dependencies or import `pkg_resources`.
- Core libraries: current mutually compatible stable releases of PyTorch/torchvision, timm 1.x, Ultralytics 8.x, Gradio 6.x, Hugging Face Hub, OpenCV, NumPy, SciPy, Pillow, tqdm, lapx, and yt-dlp, resolved and frozen by uv. Direct imports in package/evaluation modules must be declared directly rather than relying on transitive dependencies.
- Style: PEP 8, absolute imports, 120-character existing line-length convention, standard-library `unittest` for bounded tests.
- Current official facts embedded for execution:
  - uv discovers `requires-python`, uses `.python-version` as the project default, creates `.venv`, and `uv run` synchronizes against `uv.lock`: https://docs.astral.sh/uv/guides/projects/
  - Gradio 6 moved `theme`, `css`, `css_paths`, `js`, and `head` from `Blocks(...)` to `launch(...)`: https://www.gradio.app/guides/gradio-6-migration-guide
  - Gradio must bind with `server_name="127.0.0.1"` for local-only access.
  - PyTorch exposes Apple GPU acceleration as device `mps`: https://docs.pytorch.org/docs/stable/notes/mps.html
  - Current Ultralytics prediction returns `Results` with `boxes` and accepts NumPy/OpenCV images: https://docs.ultralytics.com/modes/predict
  - Default detector: repository `iitolstykh/YOLO-Face-Person-Detector`, file `yolov8x_person_face.pt`; default MiVOLO v2 legacy checkpoint: repository `iitolstykh/mivolo_v2`, revision `4eb4bb906ffd13ebbea70205691afbe30ccbc09e`, file `mivolo_v2_384_0.15.pth.tar`.

## Boundaries

### Always

- Preserve existing CLI arguments and original checkpoint compatibility.
- Keep network/model download work lazy and cache through `huggingface_hub`.
- Normalize user paths before `Path` use and give actionable errors for missing files/devices.
- Keep default Gradio access local-only and custom model loading explicitly trust-based.
- Preserve unrelated files and changes.

### Ask First

- Delete existing files, change model architecture/checkpoint format, add deployment or public sharing, commit/push, or introduce an incompatible Python upper bound.
- Expand the GUI to video/YouTube inference or alter output model semantics.

### Never

- Add a CUDA requirement or silently map unavailable CUDA to a different device when the user requested CUDA explicitly.
- Eagerly download weights at import or GUI construction time.
- Use deprecated `use_auth_token`, Gradio 5 app-level `Blocks` parameters, bare user path strings, or `pkg_resources` for packaging.
- Load arbitrary custom model files without clearly documenting that PyTorch/Ultralytics pickle-based weights must be trusted.

## Success Criteria

- [x] SC1: `pyproject.toml`, `.python-version`, and `uv.lock` define a Python 3.13+ uv project and `uv run` uses the repository `.venv`.
- [x] SC2: Isolated PEP 517 metadata/build paths do not import `pkg_resources`; Git/PyPI-style installation metadata is valid.
- [x] SC3: Runtime imports and the modern CLI work under the resolved Python 3.13 environment, with `auto` selecting MPS on this Mac when available and CPU otherwise, and no CUDA path present.
- [x] SC4: Quoted and backslash-escaped macOS paths normalize to the intended absolute path.
- [x] SC5: A Gradio 6 `Blocks` app constructs without downloads, uses launch-level theme/CSS, and is configured to bind locally by default.
- [x] SC6: Mocked GUI inference converts Gradio RGB input to MiVOLO BGR input, applies options, and returns RGB output and status without loading real weights.
- [x] SC7: The original `demo.py` entry remains usable and documentation names uv install, CLI, GUI, model-cache, trusted-weight, MPS/CPU, and local-bind behavior.
- [x] SC8: One real manual GUI inference on `images/banner.jpg` completes using the default downloaded detector/checkpoint and produces an annotated output image on macOS; CPU is an acceptable explicit fallback if an unsupported MPS operation is reported and documented.

## Verification Contract

- Profile: Personal / Lean
- Scope ceiling: Success Criteria only.
- Final Acceptance Command: `uv run python -m unittest discover -s tests -v`
- Working directory: `/Users/shuichi/Documents/GitHub/MiVOLO-python3-13-mac`
- Timeout: 15 minutes
- Maximum final attempts: 4 total; the user explicitly authorized one additional attempt after the third smoke exposed a missing serialized-checkpoint dependency. Never reset on resume.
- Step checks: Step 1.1 may run `uv lock && uv sync` once initially and once after a targeted dependency repair, each under 15 minutes. All other steps use bounded artifact inspection and are covered by the Final Acceptance Command.
- Manual smoke check: After the first green final command, run `uv run mivolo-gui --server-name 127.0.0.1 --server-port 7860`, open `http://127.0.0.1:7860`, upload `images/banner.jpg`, keep default thresholds/mode/device and default model sources, click inference once, and confirm an annotated result and success status. Stop the server after the observation. Perform this flow once for the relevant final artifact; model download time is external to automated verification.
- Failure policy: Repair only failures attributable to planned changes and within Success Criteria. Record unrelated findings without fixing them. If the final command cannot pass because it includes an unrelated pre-existing failure, block for plan revision rather than weakening the command.
- Green stop rule: The first in-budget exit `0` ends automated verification. Run no additional tests, lint, typecheck, coverage, build, or review commands afterward.

## Architecture Changes

1. Packaging moves from `setup.py` plus `requirements.txt` parsing to root `pyproject.toml` plus `uv.lock`; `.python-version` selects 3.13 and `requirements.txt` becomes a compatibility pointer rather than a second dependency source.
2. New `mivolo/runtime.py` owns macOS path normalization, explicit device validation/selection, safe precision selection, and reusable runtime configuration.
3. New `mivolo/cli.py` owns the parser and inference command; root `demo.py` becomes a compatibility call-through.
4. New `mivolo/gui.py` owns lazy model resolution/cache, the image inference adapter, Gradio component construction, and launch arguments.
5. Existing model/detector modules use the shared runtime rules and current supported library APIs; `create_timm_model.py` stops depending on removed/unstable timm internals where public equivalents or a small local checkpoint loader suffice.
6. New `tests/` modules use standard-library mocks to prove the bounded contracts without network or large model files.

## Agent Summary

| Agent | Step Count | Phases Involved |
|---|---:|---|
| `devops-agent` | 1 | 1 |
| `coding-agent` | 3 | 1, 2 |
| `debug-agent` | 1 | 2 |
| `documentation-agent` | 1 | 3 |
| `review-agent` | 1 | 3 |

## Implementation Steps

### Phase 1: Reproducible environment and runtime foundations

#### Step 1.1: Replace legacy dependency metadata with an uv project

- **Agent:** `devops-agent`
- **Location:** `pyproject.toml`, `.python-version`, `uv.lock`, `requirements.txt`, `setup.py`, `.gitignore`
- **Action:** Add declarative PEP 517 project metadata, Python 3.13 default/minimum, maintained dependency ranges, CLI/GUI entry points, and uv lock; remove all executable metadata parsing from `setup.py` without deleting the file.
- **Details:** Make `pyproject.toml` authoritative. Declare all packages directly imported by shipped runtime/evaluation modules. Constrain Gradio to `>=6,<7`, timm to `>=1,<2`, Ultralytics to a current compatible 8.x range, PyTorch/torchvision to current stable compatible releases, and let `uv.lock` freeze exact artifacts including macOS arm64 Python 3.13 wheels. Make `requirements.txt` point installers to the project rather than duplicating versions. Track `.python-version` by removing its ignore rule; add `.venv/`, `.DS_Store`, and `Thumbs.db` hygiene. A retained `setup.py` may contain only `from setuptools import setup; setup()` so even legacy invocation cannot reproduce the reported `pkg_resources` failure.
- **Dependencies:** None
- **Verification:** Run `uv lock && uv sync` from the repository root, expected exit 0 and `.venv/bin/python` reporting Python 3.13; timeout 15 minutes, maximum 2 total executions. This proves SC1 and supplies dependencies for SC2-SC7.
- **Complexity:** Medium
- **Risk:** Medium — binary ML dependency resolution can expose Python 3.13/macOS wheel constraints.
- **Idempotence & Recovery:** `uv lock` and `uv sync` are safely rerunnable. Before retry, inspect `pyproject.toml`, `uv.lock`, `.venv/pyvenv.cfg`, and the recorded first failure; change only the incompatible direct constraint. Do not delete a pre-existing user environment.

#### Step 1.2: Add shared macOS path, device, and precision behavior

- **Agent:** `coding-agent`
- **Location:** new `mivolo/runtime.py`; `mivolo/model/mi_volo.py`; `mivolo/model/yolo_detector.py`
- **Action:** Centralize normalized paths, `auto`/explicit device resolution, and device-safe half precision, then use them in both MiVOLO and detector construction.
- **Details:** `normalize_user_path(value: str | os.PathLike[str]) -> Path` must strip surrounding quotes, use `shlex.split` only for backslash escaping, expand `~`, and resolve. `resolve_device(requested: str = "auto") -> torch.device` selects MPS when built/available and otherwise CPU; explicit unavailable or unsupported devices raise actionable `ValueError`. `supports_half(device)` returns false because this fork targets MPS/CPU in full precision. Remove CUDA synchronization/configuration branches and pass the resolved MPS/CPU device into Ultralytics prediction.
- **Dependencies:** Step 1.1
- **Verification:** Bounded artifact inspection of signatures/call sites; behavior is covered by the Final Acceptance Command for SC3-SC4.
- **Complexity:** Medium
- **Risk:** Medium — silent device coercion or MPS fp16 can produce runtime faults.
- **Idempotence & Recovery:** Safely rerunnable source edits. If MPS lacks an operation during the manual smoke, preserve explicit `mps` errors, document CPU fallback, and repair `auto` only if required by SC8 rather than introducing global fallback behavior.

### Phase 2: Current inference paths and Gradio 6 UI

#### Step 2.1: Modernize timm, PyTorch, and Ultralytics integration

- **Agent:** `debug-agent`
- **Location:** `mivolo/model/create_timm_model.py`, `mivolo/model/mivolo_model.py`, `mivolo/model/mi_volo.py`, `mivolo/model/yolo_detector.py`, and directly affected imports only
- **Action:** Repair imports and checkpoint/model construction against the versions resolved in Step 1.1 while preserving existing state-dict filtering and inference outputs.
- **Details:** Replace obsolete timm private imports with exported APIs where available; where the existing `fds.` filtering requires local loading, use a small explicit loader that selects `state_dict_ema` or `state_dict`, removes only declared filtered keys, and calls `load_state_dict`. Use current `torch.load(..., weights_only=...)` deliberately: prefer restricted loading for compatible state dictionaries and emit an actionable trusted-legacy-checkpoint error rather than silently enabling arbitrary pickle execution. Keep Ultralytics `Results.boxes` handling and ensure device is supplied to `predict`/`track`. Do not change age/gender normalization, crop association, or rendering semantics.
- **Dependencies:** Step 1.2
- **Verification:** Bounded artifact inspection plus import/model-construction mocks in the Final Acceptance Command, mapped to SC2-SC3 and SC6.
- **Complexity:** High
- **Risk:** High — legacy serialized weights and custom registered timm models are version-sensitive and pickle-based weights are a trust boundary.
- **Idempotence & Recovery:** Source changes are rerunnable. Keep checkpoint-key detection isolated; if an interrupted change leaves imports broken, restore coherence by following imports from `MiVOLO` to the registered model before later steps. Never broaden unsafe deserialization merely to suppress an error; record the exact checkpoint failure and require a trusted source.

#### Step 2.2: Preserve and modernize the command-line interface

- **Agent:** `coding-agent`
- **Location:** new `mivolo/cli.py`; root `demo.py`; `scripts/inference.sh`; directly shared helpers
- **Action:** Move CLI behavior behind the `mivolo-cli` entry point while retaining `python demo.py` as a thin compatible shim and updating sample commands to uv.
- **Details:** Preserve existing flags and add `auto` as the default device. Normalize input/output/checkpoint/detector paths except actual HTTP(S)/stream inputs. Create output directories with `Path.mkdir`. Keep video writing behavior and make errors actionable. Do not add Gradio concerns to the CLI module.
- **Dependencies:** Step 2.1
- **Verification:** Bounded artifact inspection; parser/help and shim behavior are covered by the Final Acceptance Command for SC3 and SC7.
- **Complexity:** Medium
- **Risk:** Low

#### Step 2.3: Add a lazy Gradio 6 image application

- **Agent:** `coding-agent`
- **Location:** new `mivolo/gui.py` and optional package-local CSS asset only if required
- **Action:** Build a local Gradio 6 `Blocks` application and a `mivolo-gui` launcher around the existing `Predictor`.
- **Details:** Provide `build_app()` that creates components without downloads and `main()` that launches with theme/CSS at `launch(...)`, default `server_name="127.0.0.1"`, and configurable port/name CLI flags. Inputs: RGB image, confidence, IoU, faces/person mode, device, and optional detector/checkpoint paths. Empty paths resolve lazily through `hf_hub_download` using the documented repositories/files and `token=os.getenv("HF_TOKEN") or None`. Cache predictors by resolved weight paths/device/mode-safe construction; update thresholds and mode per request. Convert RGB to BGR before `Predictor.recognize`, BGR back to RGB afterward, and return a useful no-image/error/status result. Event endpoints that need not be public use Gradio 6 `api_visibility`. Explain that custom pickle-based weights must be trusted.
- **Dependencies:** Step 2.2
- **Verification:** Bounded artifact inspection; construction, no-download, option propagation, and color conversion are covered by the Final Acceptance Command for SC5-SC6.
- **Complexity:** High
- **Risk:** Medium — accidental eager model loading would make startup slow and tests/network-dependent.
- **Idempotence & Recovery:** Safely rerunnable. Cache keys must make duplicate downloads harmless through Hugging Face cache semantics. If interrupted during a real download, verify the Hub cache through `hf_hub_download` rather than deleting partial/shared cache content.

### Phase 3: Acceptance coverage and user documentation

#### Step 3.1: Add bounded offline compatibility tests

- **Agent:** `review-agent`
- **Location:** new `tests/test_runtime.py`, `tests/test_cli.py`, `tests/test_gui.py`, and only the minimum additional test module needed for metadata/import coverage
- **Action:** Add standard-library `unittest` coverage for the Success Criteria without model downloads or server startup.
- **Details:** Test quoted/backslash macOS paths in a temporary directory; patch PyTorch availability to test device precedence and explicit-device failures; verify CLI parsing/defaults and `demo.py` call-through; patch `hf_hub_download`/`Predictor` to prove GUI construction performs no download, inference propagates thresholds/mode, and RGB/BGR conversions round-trip; inspect Gradio component construction under installed Gradio 6. Include an import/build-metadata assertion that would detect `pkg_resources` reintroduction. Do not add coverage tooling or broad upstream model-quality tests.
- **Dependencies:** Step 2.3
- **Verification:** Test artifacts are reviewed for direct mapping to SC1-SC7; execution is reserved for the Final Acceptance Command.
- **Complexity:** Medium
- **Risk:** Low

#### Step 3.2: Document the uv, macOS, CLI, and GUI workflow

- **Agent:** `documentation-agent`
- **Location:** `README.md`, `CHANGELOG.md`, new `NOTES.md`, `AGENTS.md`, `.gitignore`, scripts as applicable
- **Action:** Replace stale install/demo guidance and record migration decisions and known limits.
- **Details:** Lead with `uv sync`, `uv run mivolo-gui`, and `uv run mivolo-cli`; explain `.venv`, Python 3.13 default, first-run Hugging Face downloads/cache, optional `HF_TOKEN`, trusted custom weights, `auto` device order, MPS full precision, CPU fallback, Gradio local URL, and why `pip install git+...` now works. Preserve research/citation material. Add a dated changelog entry and chronological notes with the reported `pkg_resources` cause and solution. Ensure `.gitignore` contains `.DS_Store`, `Thumbs.db`, `.venv/`, but tracks `.python-version`.
- **Dependencies:** Step 3.1
- **Verification:** Bounded artifact inspection for every named command and warning, mapped to SC1-SC2 and SC7.
- **Complexity:** Low
- **Risk:** Low

#### Step 3.3: Run final acceptance and the one-pass GUI smoke check

- **Agent:** `review-agent`
- **Location:** entire planned change set; local `.venv` and Hugging Face cache as external generated state
- **Action:** Execute the Verification Contract exactly, then perform its single manual GUI flow only after the first green automated result.
- **Details:** Before the automated command, increment the durable attempt count in `Resume Here`. At exit 0, stop all automated verification. Launch the exact local GUI command, run `images/banner.jpg` once, capture only concise observed evidence in this plan, stop the server, and mark SC8. Do not commit downloaded weights. If MPS is unavailable or reports an unsupported operation, use the documented CPU selector once within the same manual flow and record that fallback.
- **Dependencies:** Step 3.2
- **Verification:** Final Acceptance Command exit 0 within 15 minutes and the exact manual observation defined above, proving SC1-SC8.
- **Complexity:** Medium
- **Risk:** Medium — first-run downloads are large and network-dependent.
- **Idempotence & Recovery:** Record server session/PID, cache paths, and observed download completion before pausing. Before retrying, call the same Hub resolver to reuse validated cache entries; never delete shared cache. A failed automated attempt consumes budget. The manual flow runs once per relevant implementation state.

## Risks and Mitigations

1. Risk: Current binary ML packages may have incompatible Python 3.13/macOS constraints. Mitigation: Step 1.1 locks only releases with matching wheels and permits one targeted dependency repair within its bounded check budget.
2. Risk: Modern timm private-module movement can break this custom VOLO registration. Mitigation: Step 2.1 narrows all model construction/checkpoint adaptation to one module and tests imports/model construction with mocks.
3. Risk: PyTorch's `weights_only=True` default since 2.6 can reject old pickle contents, while `False` can execute code. Mitigation: prefer restricted state-dict loading, use documented default repositories, and require explicit trusted-weight messaging rather than an invisible unsafe fallback.
4. Risk: MPS does not implement every operation or tolerate this model in fp16. Mitigation: use fp32 on MPS, keep explicit CPU selection, and make the manual smoke criterion accept a documented CPU fallback only when MPS gives a concrete unsupported-operation error.
5. Risk: A GUI import accidentally downloads hundreds of megabytes. Mitigation: separate `build_app()` from cached lazy resolver functions and assert zero resolver calls during construction.
6. Risk: Gradio app-level parameters regress to the Gradio 5 constructor form. Mitigation: centralize launch arguments in `main()` and test construction under the locked Gradio 6 release.

## Progress

- [x] (2026-08-12 08:03Z) Step 1.1: COMPLETE — evidence: attempt 2/2 `uv lock && uv sync` exited 0, built `mivolo==0.6.0.dev0`, wrote `uv.lock`, and created `.venv` with CPython 3.13.11 macOS arm64; attempt 1/2 was a sandbox-only cache failure with no generated state.
- [x] (2026-08-12 08:04Z) Step 1.2: COMPLETE — evidence: bounded artifact inspection confirmed macOS path normalization, MPS/CPU-only device validation, full-precision behavior, resolved device propagation, and no CUDA call site in the scoped modules; `git diff --check` exited 0.
- [x] (2026-08-12 08:06Z) Step 2.1: COMPLETE — evidence: bounded artifact inspection confirmed public timm model/build/state-dict APIs, restricted `weights_only=True` checkpoint loading, retained filtering/remapping behavior, resolved Ultralytics device propagation, and clean diff formatting.
- [x] (2026-08-12 08:08Z) Step 2.2: COMPLETE — evidence: bounded artifact inspection confirmed packaged CLI argument parity, auto/MPS/CPU-only device choices, normalized local paths, output error handling, thin root compatibility shim, uv sample commands, and clean diff formatting.
- [x] (2026-08-12 08:09Z) Step 2.3: COMPLETE — evidence: bounded artifact inspection confirmed download-free app construction, lazy documented defaults, trusted normalized custom paths, cached predictor setup, explicit RGB/BGR conversion, Gradio 6 private events, launch-level theme/CSS, and local-only default binding.
- [x] (2026-08-12 08:11Z) Step 3.1: COMPLETE — evidence: bounded artifact inspection confirmed 15 focused standard-library tests map to SC1-SC7, mock all model/network work, avoid server startup, and have clean diff formatting; execution remains reserved for final acceptance.
- [x] (2026-08-12 08:12Z) Step 3.2: COMPLETE — evidence: bounded documentation inspection confirmed uv/Python setup, GUI/CLI commands, cache/token, trusted weights, MPS/CPU fallback, local binding, PEP 517 fix, changelog/notes, and ignore hygiene; scoped diff formatting is clean.
- [x] (2026-08-12 09:08Z) Step 3.3: COMPLETE — evidence: user-authorized attempt 4/4 passed all 17 tests in 0.056 seconds; the cached one-pass Gradio flow loaded both documented defaults, returned an output image with success status on MPS, and browser/server shutdown succeeded.

## Decision Log

- Decision: Use an uv-native PEP 517 project with `.python-version` set to 3.13 and `requires-python = ">=3.13"`.
  Rationale: This directly removes the `pkg_resources` metadata failure and makes uv's `.venv` the default reproducible environment while permitting later Python releases.
  Date/Author: 2026-08-12 / Codex
- Decision: Keep original legacy MiVOLO checkpoints and add a Gradio 6 image UI instead of replacing inference with MiVOLO-Next or the newer Transformers remote-code model.
  Rationale: The user asked to revive this repository; preserving its model semantics is the smallest compatible migration.
  Date/Author: 2026-08-12 / Codex
- Decision: Use lazy default downloads from the current detector repository and a pinned official `iitolstykh/mivolo_v2` revision containing the original legacy checkpoint.
  Rationale: The former demo repository is unavailable and the file was later removed from the official repository's main branch; the immutable official revision preserves the required checkpoint without relying on a third-party mirror.
  Date/Author: 2026-08-12 / Codex
- Decision: Default device to `auto`, prefer MPS over CPU on supported Macs, use full precision on both, and remove CUDA runtime paths from this fork.
  Rationale: The current machine policy explicitly permits only MPS or CPU and prohibits emitting CUDA code paths.
  Date/Author: 2026-08-12 / Codex
- Decision: Resume execution from committed planning state `d5e5fc1`, not the original upstream HEAD recorded during plan authoring.
  Rationale: The user committed `AGENTS.md` and `PLANS.md` between turns; the clean working tree and commit contents support this as the new baseline.
  Date/Author: 2026-08-12 / Codex
- Decision: Use standard-library `unittest` and one real manual GUI inference as the acceptance boundary.
  Rationale: The repository has no test framework; focused mocks prove integration contracts without adding coverage infrastructure or repeatedly downloading large weights.
  Date/Author: 2026-08-12 / Codex

## Surprises & Discoveries

- The repository at HEAD `37475e3` has no pre-existing `PLANS.md`, project `AGENTS.md`, `pyproject.toml`, tests, or Gradio application; root `demo.py` is a command-line inference script despite its name.
- `setup.py` parses `requirements.txt` by importing `pkg_resources`, exactly matching the reported isolated metadata failure.
- The existing dependency set pins `ultralytics==8.1.0` and a development `timm==0.8.13.dev0`, while source imports several timm private modules and defaults inference devices to CUDA.
- `.gitignore` currently ignores `.python-version`, which conflicts with a repository-owned uv Python default.
- The official historical Gradio demo already identifies compatible public checkpoint files but uses Gradio 4 and deprecated `use_auth_token`; it is a behavior reference, not code to copy verbatim.
- Current official/PyPI evidence confirms uv Tier 1 support for Python 3.13+, Gradio 6 Python 3.13 support, current timm Python 3.13 testing, current PyTorch macOS arm64 CPython 3.13 wheels, and lapx 0.9.4 macOS arm64 CPython 3.13 wheels.
- Resume audit found planning commit `d5e5fc1` on `codex/313`, replacing the previously recorded upstream HEAD while leaving all implementation source unchanged.
- uv emitted one transitive-metadata warning about correcting a quoted version specifier, but resolution and installation completed successfully; this warning is outside the project metadata and requires no planned repair.
- The first test import updated the existing Ultralytics user settings file to its latest schema while preserving values; this external library housekeeping did not affect repository state or test results.
- Gradio 6 supplies untouched optional `Textbox` inputs as `None` in this live flow even though the handler annotation was `str`; `_resolve_model_path` must normalize `None` to the empty/default-download path before calling string methods.
- The historical `iitolstykh/demo_xnet_volo_cross` default is unavailable. The exact legacy file remains publicly downloadable from official repository `iitolstykh/mivolo_v2` at revision `4eb4bb906ffd13ebbea70205691afbe30ccbc09e`; main no longer contains it.
- Current timm VOLO inserts `pos_drop_rate` between `drop_rate` and `attn_drop_rate`; the legacy positional `super().__init__` call therefore shifts all later values and must use explicit keywords.
- The current detector checkpoint contains an OmegaConf object. Current Ultralytics attempts a pip-based auto-install when `omegaconf` is absent, which is incompatible with this intentionally pip-free uv environment; `omegaconf` must be a declared project dependency.

## Outcomes & Retrospective

- MiVOLO now installs as a Python 3.13+ uv project without the legacy `pkg_resources` metadata failure and exposes maintained CLI and Gradio 6 entry points.
- Runtime, evaluation, timing, data-loading, scripts, and preparation tools now follow the macOS MPS/CPU full-precision policy and current supported import paths.
- The GUI remains download-free at construction, binds locally, normalizes macOS paths, uses version-pinned official legacy model artifacts, and declares the detector's serialized OmegaConf dependency instead of invoking pip at runtime.
- Acceptance completed with 17 focused tests plus a real MPS-backed Gradio inference. Two manual integration findings (`None` optional inputs and removed/default model dependencies) required bounded repairs; immutable official sources and direct dependencies made the final flow reproducible.
