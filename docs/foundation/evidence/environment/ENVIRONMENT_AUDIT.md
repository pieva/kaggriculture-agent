# Environment Audit

Date: 2026-08-28

## Precheck

- Branch: `main`
- HEAD: `4445aa0 Close E08 productive scale experiment`
- `python --version`: `Python 3.14.4`
- `py --version`: `Python 3.14.4`
- `where.exe python`: `C:\Python314\python.exe`
- `where.exe pip`: `C:\Python314\Scripts\pip.exe`

The active shell Python is global Python `3.14.4`, not the repository `.venv`.

## Versioned Dependency Configuration

Canonical dependency source: `pyproject.toml`.

- Declared Python support: `>=3.10`
- Runtime dependencies:
  - `kaggle-environments>=1.32.7`
  - `pandas>=2.0.0`
  - `numpy>=1.24.0`
- Dev/test dependencies:
  - `pytest>=8.0.0`
  - `ruff>=0.2.0`
- Build backend:
  - `setuptools>=61.0`

No `requirements.txt`, `requirements-dev.txt`, lock file, `setup.py`, `setup.cfg`, CI workflow or setup script was found. `.gitignore` explicitly ignores `.venv/`.

## README Divergence

`README.md` documents activation and test commands using `.venv`, but did not previously define:

- `.venv` as disposable local artifact;
- `pyproject.toml` as canonical dependency source;
- exact rebuild commands;
- multi-agent environment discipline.

## Old `.venv` State

`.venv` is ignored by Git:

- `.gitignore:30:.venv/`

No `.venv` files are tracked by Git.

The old `.venv` was not reliable. Its launcher pointed to:

`C:\Users\pietr\AppData\Local\Programs\Python\Python312\python.exe`

That Python executable is not available, so:

- `.venv\Scripts\python.exe --version` failed;
- `.venv\Scripts\python.exe -m pip --version` failed;
- `.venv\Scripts\python.exe -m pip freeze` failed.

Diagnostic output is recorded in `docs/foundation/evidence/environment/OLD_VENV_PIP_FREEZE.txt`.

## Diagnosis

The repository configuration is coherent enough to rebuild from versioned configuration. The old `.venv` is stale/broken because it references a missing Python 3.12 installation, while the host currently exposes Python 3.14.4.

No dependency set change is required. `pyproject.toml` remains the source of truth.

## Rebuild Plan

Use Python `3.12.x`. The host global Python `3.14.4` satisfies the previous loose lower bound but is not compatible with the current `kaggle-environments` transitive dependency set on this Windows host.

Canonical commands:

```powershell
<PYTHON_3_12>\python.exe -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install --no-build-isolation -e .[dev]
.\.venv\Scripts\python.exe -m pip check
```

Principle:

`Repository configuration -> .venv -> verification`

## Interrupted State Snapshot

The session was interrupted by the user while completing the editable install.

Current `.venv` state at stop time:

- `.venv` was rebuilt with Python `3.12.13` from the Codex bundled runtime.
- The old broken `.venv` was deleted.
- The attempted Python `3.14.4` rebuild was discarded because `pygame` had no compatible wheel and failed building from source with `ModuleNotFoundError: No module named 'setuptools._distutils.msvccompiler'`.
- Many transitive dependencies are installed in the Python `3.12.13` `.venv`.
- `setuptools==84.0.0` and `wheel==0.48.0` are installed.
- `pip check`: `No broken requirements found.`
- Basic imports verified: `numpy`, `pandas`, `pytest`, `ruff`.
- `kaggle_environments` import still fails because the interrupted install did not finish registering `kaggle-environments` and `kaggriculture-agent`.
- Current partial freeze: `docs/foundation/evidence/environment/CURRENT_PARTIAL_VENV_PIP_FREEZE.txt`.

No strategy or submission file was intentionally modified by this environment repair step.

Resume command:

```powershell
.\.venv\Scripts\python.exe -m pip install --no-build-isolation -e .[dev]
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -c "import kaggle_environments, agricola; print(kaggle_environments.__version__)"
```

After that, run the smoke tests requested in this audit before declaring the environment fully rebuilt.

## Final Rebuild Result

The environment rebuild was resumed and completed.

- Canonical Python used: `Python 3.12.13`
- `.venv` previous broken instance deleted: yes
- `.venv` recreated: yes
- Dependency source: `pyproject.toml`
- Dependency file changed: `requires-python` tightened from `>=3.10` to `>=3.10,<3.14`
- Reason for dependency metadata change: Python `3.14.4` attempted rebuild failed because `pygame` was built from source and failed with `ModuleNotFoundError: No module named 'setuptools._distutils.msvccompiler'`; Python `3.12.13` installed the compatible wheel set cleanly.
- Install command completed: `.\.venv\Scripts\python.exe -m pip install --no-build-isolation -e .[dev]`
- Installed project: `kaggriculture-agent==0.1.0` editable from `C:\Users\pietr\Projects\kaggriculture-agent`
- Installed Kaggle environment: `kaggle-environments==1.32.7`
- `pip check`: `No broken requirements found.`

Smoke tests:

- `.\.venv\Scripts\python.exe --version`: `Python 3.12.13`
- Import smoke: `kaggle_environments`, `numpy`, `pandas`, `pytest`, `ruff`, `agricola`: pass; `kaggle_environments.__version__ == 1.32.7`
- `py_compile` on core modules and benchmark/build scripts: pass
- Focused pytest: `tests\test_hire_nw_cluster.py`, `tests\test_water_first_hire_nw_cluster.py`, `tests\test_submission_behavioral_equivalence.py`: `12 passed`
- Non-blocking warning: `.pytest_cache` permission denied while writing cache nodeids
- Non-regression benchmark/smoke: `scripts\verify_x112_submission_candidate.py`: pass; seed `0` `$42,491`, seed `421521921` `$48,313`, source/submission equivalent

Full pytest was not run because the requested repair was environment-focused and the representative core + behavioral + benchmark smoke suite already exercised the project-critical Kaggriculture path.
