"""Bundle the Codex compact-Q0 routine controller into one standalone file."""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src" / "agricola"
CONFIG_FILE = PROJECT_ROOT / "configs" / "model_spec_c2" / "CODEX_C2_CONFIG.json"
LIFECYCLE_FILE = SRC_DIR / "strategy" / "codex_lifecycle.py"
CODEX_FILE = SRC_DIR / "strategy" / "codex_compact_q0.py"

SUBMISSION_TEMPLATE = '''"""
Standalone Codex C2 compact-Q0 routine file for Kaggle Kaggriculture.
Generated from the Foundation-f391ee2-bound Codex controller and adapter.
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
# --- Embedded Codex C2 Configuration ---
# ==========================================
CODEX_C2_CONFIG: dict[str, Any] = {config_json}

# ==========================================
# --- E16 Base Policy Definitions ---
# ==========================================
{e16_base_code}

# ==========================================
# --- Codex C2 Decision Lifecycle Runtime ---
# ==========================================
{codex_lifecycle_code}

# ==========================================
# --- Codex C2 Strategy & Agent Class ---
# ==========================================
{codex_c2_code}

# ==========================================
# --- Kaggle Entrypoint ---
# ==========================================
_agent_factory: Callable[[dict[str, Any], Any], dict[str, Any]] | None = None
_episode_sequence = 0


def agent(observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
    """Kaggle entry point for the Codex compact-Q0 routine candidate."""
    global _agent_factory, _episode_sequence
    step = int(observation.get("step", 0))
    if step == 0 or _agent_factory is None:
        _episode_sequence += 1
        player = int(observation.get("player", 0))
        _agent_factory = create_agent(
            run_context={{
                "run_id": "codex-kaggle-runtime",
                "episode_id": f"codex-episode-{{_episode_sequence:06d}}",
                "seed": None,
                "opponent_id": "KAGGLE_UNOBSERVED",
                "player_position": player,
            }}
        )
    return _agent_factory(observation, configuration)
'''


def clean_imports(code: str, remove_prefixes: list[str]) -> str:
    lines = code.split("\n")
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if any(stripped.startswith(prefix) for prefix in remove_prefixes):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def extract_e16_base_definitions() -> str:
    with open(SRC_DIR / "e16" / "policy.py", "r", encoding="utf-8") as f:
        e16_code = f.read()

    # Remove create_agent at the bottom of e16/policy.py as it is replaced by codex_c2.py create_agent
    create_agent_idx = e16_code.find("def create_agent(")
    if create_agent_idx != -1:
        e16_code = e16_code[:create_agent_idx]

    return clean_imports(e16_code, [
        "from __future__ import annotations",
        "import math",
        "from collections.abc import",
        "from copy import",
        "from typing import",
    ]).strip()


def extract_codex_c2_definitions() -> str:
    with open(CODEX_FILE, "r", encoding="utf-8") as f:
        codex_code = f.read()

    crop_rules_idx = codex_code.find("CROP_RULES:")
    if crop_rules_idx == -1:
        raise RuntimeError("compact-Q0 CROP_RULES marker is missing")
    codex_body = codex_code[crop_rules_idx:]

    return codex_body.strip()


def extract_codex_lifecycle_definitions() -> str:
    lifecycle_code = LIFECYCLE_FILE.read_text(encoding="utf-8")
    marker = 'FOUNDATION_CHECKPOINT = "f391ee2"'
    lifecycle_idx = lifecycle_code.find(marker)
    if lifecycle_idx == -1:
        raise RuntimeError("Codex lifecycle foundation marker is missing")
    return lifecycle_code[lifecycle_idx:].strip()


def build_submission_codex(output_path: str | None = None) -> Path:
    out_file = Path(output_path) if output_path else PROJECT_ROOT / "submission" / "submission_codex.py"
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config_obj = json.load(f)
    config_json = json.dumps(config_obj, indent=2)

    e16_base_code = extract_e16_base_definitions()
    codex_lifecycle_code = extract_codex_lifecycle_definitions()
    codex_c2_code = extract_codex_c2_definitions()

    bundled_code = SUBMISSION_TEMPLATE.format(
        config_json=config_json,
        e16_base_code=e16_base_code,
        codex_lifecycle_code=codex_lifecycle_code,
        codex_c2_code=codex_c2_code,
    )

    bundled_code = "\n".join(line.rstrip() for line in bundled_code.splitlines()) + "\n"
    out_file.write_text(bundled_code, encoding="utf-8")
    print(f"Successfully generated Codex compact-Q0 standalone at: {out_file}")
    return out_file


if __name__ == "__main__":
    build_submission_codex()
