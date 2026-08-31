"""Bundle the Antigravity C2 75K Dual-Quadrant routine controller into one standalone file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src" / "agricola"
CONFIG_FILE = PROJECT_ROOT / "configs" / "model_spec_c2" / "ANTIGRAVITY_C2_75K_DUAL_Q_CONFIG.json"
CONFIG_PY_FILE = SRC_DIR / "strategy" / "antigravity" / "c2_75k_config.py"
LIFECYCLE_FILE = SRC_DIR / "strategy" / "codex_lifecycle.py"
COMPACT_Q0_FILE = SRC_DIR / "strategy" / "antigravity" / "antigravity_compact_q0.py"
DUAL_Q_FILE = SRC_DIR / "strategy" / "antigravity" / "antigravity_dual_q0_q1.py"

SUBMISSION_TEMPLATE = '''"""
Standalone Antigravity C2 75K Dual-Quadrant (Q0+Q1) routine file for Kaggle Kaggriculture.
Generated from the Foundation-f391ee2-bound Antigravity controller and adapter.
"""

from __future__ import annotations

import hashlib
from collections import Counter, defaultdict
from collections.abc import Callable
from copy import deepcopy
from dataclasses import asdict, dataclass, field
import json
import math
from pathlib import Path
import statistics
from typing import Any, Dict


# ==========================================
# --- Embedded Antigravity C2 75K Config ---
# ==========================================
ANTIGRAVITY_C2_75K_DUAL_Q_CONFIG: dict[str, Any] = {config_json}

# ==========================================
# --- E16 Base Policy Definitions ---
# ==========================================
{e16_base_code}

# ==========================================
# --- Decision Lifecycle Runtime ---
# ==========================================
{codex_lifecycle_code}

# ==========================================
# --- Antigravity C2 75K Config Class ---
# ==========================================
{config_class_code}

# ==========================================
# --- Antigravity Base Q0 Definitions ---
# ==========================================
{antigravity_compact_code}

# ==========================================
# --- Antigravity Dual Q0+Q1 Policy ---
# ==========================================
{antigravity_dual_code}

# ==========================================
# --- Agent Factory & Kaggle Entrypoint ---
# ==========================================
class AntigravityC2_75K_Agent:
    """Antigravity C2 75K Tournament Candidate Agent."""

    def __init__(
        self,
        config: Any = None,
        *,
        run_context: dict[str, Any] | None = None,
    ) -> None:
        self.config = config or AntigravityC2_75K_Config.load()
        self.policy = AntigravityDualQPolicy(config=self.config, run_context=run_context)
        self.antigravity_75k_instance = self.policy
        self.last_exception: str | None = None
        self.error_count: int = 0
        self.fallback_count: int = 0

    def act(
        self,
        observation: dict[str, Any],
        configuration: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.policy.act(observation, configuration=configuration)

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        try:
            return self.act(observation, configuration=configuration)
        except Exception as exc:
            self.last_exception = f"{type(exc).__name__}: {exc}"
            self.error_count += 1
            self.fallback_count += 1
            return {"farmer": ["PASS"], "hands": [], "market": []}


def create_agent(run_context: dict[str, Any] | None = None) -> AntigravityC2_75K_Agent:
    return AntigravityC2_75K_Agent(run_context=run_context)


_agent_factory: Callable[[dict[str, Any], Any], dict[str, Any]] | None = None
_episode_sequence = 0


def agent(observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
    """Kaggle entry point for Antigravity 75K routine candidate."""
    global _agent_factory, _episode_sequence
    step = int(observation.get("step", 0))
    if step == 0 or _agent_factory is None:
        _episode_sequence += 1
        player = int(observation.get("player", 0))
        _agent_factory = create_agent(
            run_context={
                "run_id": "antigravity-kaggle-runtime",
                "episode_id": f"antigravity-episode-{_episode_sequence:06d}",
                "seed": None,
                "opponent_id": "KAGGLE_UNOBSERVED",
                "player_position": player,
            }
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


def extract_config_class_definitions() -> str:
    with open(CONFIG_PY_FILE, "r", encoding="utf-8") as f:
        code = f.read()

    marker = "@dataclass"
    idx = code.find(marker)
    if idx == -1:
        raise RuntimeError("Antigravity config class marker is missing")
    return code[idx:].strip()


def extract_antigravity_compact_definitions() -> str:
    with open(COMPACT_Q0_FILE, "r", encoding="utf-8") as f:
        code = f.read()

    crop_rules_idx = code.find("CROP_RULES:")
    if crop_rules_idx == -1:
        raise RuntimeError("compact-Q0 CROP_RULES marker is missing")
    body = code[crop_rules_idx:]

    return body.strip()


def extract_antigravity_dual_definitions() -> str:
    with open(DUAL_Q_FILE, "r", encoding="utf-8") as f:
        code = f.read()

    marker = 'DUAL_MODEL_SPEC_VERSION = "ANTIGRAVITY-C2-DUAL-Q0-Q1-75K-V1.0"'
    idx = code.find(marker)
    if idx == -1:
        raise RuntimeError("Antigravity dual policy DUAL_MODEL_SPEC_VERSION marker is missing")
    return code[idx:].strip()



def extract_codex_lifecycle_definitions() -> str:
    lifecycle_code = LIFECYCLE_FILE.read_text(encoding="utf-8")
    marker = 'FOUNDATION_CHECKPOINT = "f391ee2"'
    lifecycle_idx = lifecycle_code.find(marker)
    if lifecycle_idx == -1:
        raise RuntimeError("Codex lifecycle foundation marker is missing")
    return lifecycle_code[lifecycle_idx:].strip()


def build_submission_antigravity_75k(output_path: str | None = None) -> Path:
    out_file = Path(output_path) if output_path else PROJECT_ROOT / "submission" / "submission_antigravity_75k.py"
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config_obj = json.load(f)
    config_json = json.dumps(config_obj, indent=2)

    e16_base_code = extract_e16_base_definitions()
    codex_lifecycle_code = extract_codex_lifecycle_definitions()
    config_class_code = extract_config_class_definitions()
    antigravity_compact_code = extract_antigravity_compact_definitions()
    antigravity_dual_code = extract_antigravity_dual_definitions()

    bundled_code = (
        SUBMISSION_TEMPLATE
        .replace("{config_json}", config_json)
        .replace("{e16_base_code}", e16_base_code)
        .replace("{codex_lifecycle_code}", codex_lifecycle_code)
        .replace("{config_class_code}", config_class_code)
        .replace("{antigravity_compact_code}", antigravity_compact_code)
        .replace("{antigravity_dual_code}", antigravity_dual_code)
    )

    bundled_code = "\n".join(line.rstrip() for line in bundled_code.splitlines()) + "\n"
    out_file.write_text(bundled_code, encoding="utf-8")
    print(f"Successfully generated Antigravity 75K standalone at: {out_file}")
    return out_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Antigravity 75K Kaggle standalone submission.")
    parser.add_argument("--output", "-o", type=str, default=None, help="Custom output path for the submission file.")
    parser.add_argument("--submission-py", action="store_true", help="Also generate submission/submission.py.")
    args = parser.parse_args()

    out = build_submission_antigravity_75k(args.output)
    if args.submission_py:
        build_submission_antigravity_75k(str(PROJECT_ROOT / "submission" / "submission.py"))
