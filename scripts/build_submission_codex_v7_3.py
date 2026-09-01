"""Bundle Codex V7.3 Dual-Q Q1-cadence into one standalone Kaggle file."""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src" / "agricola"
BASE_CONFIG_FILE = (
    PROJECT_ROOT / "configs" / "model_spec_c2" / "CODEX_C2_CONFIG.json"
)
DUAL_CONFIG_FILE = (
    PROJECT_ROOT
    / "configs"
    / "model_spec_c2"
    / "CODEX_C2_DUAL_Q0_Q1_CONFIG.json"
)
CADENCE_CONFIG_FILE = (
    PROJECT_ROOT
    / "configs"
    / "model_spec_c2"
    / "CODEX_C2_DUAL_Q1_CADENCE_CONFIG.json"
)
E16_FILE = SRC_DIR / "e16" / "policy.py"
LIFECYCLE_FILE = SRC_DIR / "strategy" / "codex_lifecycle.py"
BASE_CODEX_FILE = SRC_DIR / "strategy" / "codex_compact_q0.py"
DUAL_CODEX_FILE = SRC_DIR / "strategy" / "codex_dual_q0_q1.py"
CADENCE_CODEX_FILE = SRC_DIR / "strategy" / "codex_dual_q1_cadence.py"
DEFAULT_OUTPUT = (
    PROJECT_ROOT / "submission" / "submission_codex_v7_3_dual_q1_cadence.py"
)

SUBMISSION_TEMPLATE = '''"""
Standalone Codex C2 V7.3 Dual-Q Q1-cadence submission for Kaggriculture.

Generated from the Foundation-f391ee2-bound V7.1 controller, the isolated
V7.2 Dual-Q extension, and the verified V7.3 local livestock-cadence relief.
No repository-local imports or configuration files are required at runtime.
"""

from __future__ import annotations

import hashlib
from collections import Counter, defaultdict
from collections.abc import Callable
from copy import deepcopy
from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
from typing import Any

# ==========================================
# --- Embedded verified configurations ---
# ==========================================
CODEX_C2_CONFIG: dict[str, Any] = json.loads(r"""{base_config_json}""")
CODEX_DUAL_CONFIG: dict[str, Any] = json.loads(r"""{dual_config_json}""")
CODEX_CADENCE_CONFIG: dict[str, Any] = json.loads(r"""{cadence_config_json}""")

# ==========================================
# --- Shared E16 policy primitives ---
# ==========================================
{e16_base_code}

# ==========================================
# --- Codex decision-lifecycle runtime ---
# ==========================================
{codex_lifecycle_code}

# ==========================================
# --- Codex V7.1 compact-Q0 base ---
# ==========================================
{base_codex_code}

# ==========================================
# --- Codex V7.2 Dual-Q extension ---
# ==========================================
DUAL_MODEL_SPEC_VERSION = "CODEX-C2-V7.2-DUAL-Q0-Q1"
{dual_codex_code}

# ==========================================
# --- Codex V7.3 Q1 cadence extension ---
# ==========================================
CADENCE_MODEL_SPEC_VERSION = "CODEX-C2-V7.3-DUAL-Q1-CADENCE"
{cadence_codex_code}

# ==========================================
# --- Kaggle entrypoint ---
# ==========================================
_agent_factory: Callable[[dict[str, Any], Any], dict[str, Any]] | None = None
_episode_sequence = 0


def agent(observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
    """Kaggle entry point for Codex V7.3 Dual-Q Q1-cadence."""
    global _agent_factory, _episode_sequence
    step = int(observation.get("step", 0))
    if step == 0 or _agent_factory is None:
        _episode_sequence += 1
        player = int(observation.get("player", 0))
        _agent_factory = create_cadence_agent(
            run_context={{
                "run_id": "codex-v7-3-kaggle-runtime",
                "episode_id": f"codex-v7-3-episode-{{_episode_sequence:06d}}",
                "seed": None,
                "opponent_id": "KAGGLE_UNOBSERVED",
                "player_position": player,
            }}
        )
    return _agent_factory(observation, configuration)
'''


def _clean_imports(code: str, remove_prefixes: tuple[str, ...]) -> str:
    cleaned: list[str] = []
    for line in code.splitlines():
        stripped = line.strip()
        if any(stripped.startswith(prefix) for prefix in remove_prefixes):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def _extract_e16() -> str:
    code = E16_FILE.read_text(encoding="utf-8")
    create_agent_idx = code.find("def create_agent(")
    if create_agent_idx != -1:
        code = code[:create_agent_idx]
    return _clean_imports(
        code,
        (
            "from __future__ import annotations",
            "import math",
            "from collections.abc import",
            "from copy import",
            "from typing import",
        ),
    ).strip()


def _extract_lifecycle() -> str:
    code = LIFECYCLE_FILE.read_text(encoding="utf-8")
    marker = 'FOUNDATION_CHECKPOINT = "f391ee2"'
    start = code.find(marker)
    if start == -1:
        raise RuntimeError("Codex lifecycle foundation marker is missing")
    return code[start:].strip()


def _extract_base_codex() -> str:
    code = BASE_CODEX_FILE.read_text(encoding="utf-8")
    start = code.find("CROP_RULES:")
    if start == -1:
        raise RuntimeError("compact-Q0 CROP_RULES marker is missing")
    return code[start:].strip()


def _replace_embedded_loader(
    code: str,
    *,
    external_default: str,
    embedded_name: str,
) -> str:
    old = (
        f"    config_path = Path(path) if path is not None else {external_default}\n"
        "    with config_path.open(\"r\", encoding=\"utf-8\") as handle:\n"
        "        config = json.load(handle)"
    )
    new = (
        "    if path is None:\n"
        f"        config = deepcopy({embedded_name})\n"
        "    else:\n"
        "        config_path = Path(path)\n"
        "        with config_path.open(\"r\", encoding=\"utf-8\") as handle:\n"
        "            config = json.load(handle)"
    )
    if old not in code:
        raise RuntimeError(f"embedded loader marker missing for {embedded_name}")
    return code.replace(old, new, 1)


def _extract_dual_codex() -> str:
    code = DUAL_CODEX_FILE.read_text(encoding="utf-8")
    start = code.find("def _mirror_q1(")
    if start == -1:
        raise RuntimeError("Dual-Q mirror marker is missing")
    body = code[start:]
    return _replace_embedded_loader(
        body,
        external_default="DEFAULT_DUAL_CONFIG_PATH",
        embedded_name="CODEX_DUAL_CONFIG",
    ).strip()


def _extract_cadence_codex() -> str:
    code = CADENCE_CODEX_FILE.read_text(encoding="utf-8")
    start = code.find("def load_cadence_config(")
    if start == -1:
        raise RuntimeError("Q1 cadence loader marker is missing")
    body = code[start:]
    return _replace_embedded_loader(
        body,
        external_default="DEFAULT_CADENCE_CONFIG_PATH",
        embedded_name="CODEX_CADENCE_CONFIG",
    ).strip()


def _load_json(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_submission_codex_v7_3(output_path: str | Path | None = None) -> Path:
    """Generate the isolated V7.3 submission without touching canonical V7.1."""
    out_file = Path(output_path) if output_path is not None else DEFAULT_OUTPUT
    out_file.parent.mkdir(parents=True, exist_ok=True)
    bundled = SUBMISSION_TEMPLATE.format(
        base_config_json=json.dumps(_load_json(BASE_CONFIG_FILE), indent=2),
        dual_config_json=json.dumps(_load_json(DUAL_CONFIG_FILE), indent=2),
        cadence_config_json=json.dumps(_load_json(CADENCE_CONFIG_FILE), indent=2),
        e16_base_code=_extract_e16(),
        codex_lifecycle_code=_extract_lifecycle(),
        base_codex_code=_extract_base_codex(),
        dual_codex_code=_extract_dual_codex(),
        cadence_codex_code=_extract_cadence_codex(),
    )
    bundled = "\n".join(line.rstrip() for line in bundled.splitlines()) + "\n"
    out_file.write_text(bundled, encoding="utf-8")
    print(f"Generated Codex V7.3 standalone submission: {out_file}")
    return out_file


if __name__ == "__main__":
    build_submission_codex_v7_3()
