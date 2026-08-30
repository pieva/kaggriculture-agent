"""Build script to bundle the frozen Codex C2 V4 candidate into standalone submission_codex.py."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src" / "agricola"
CONFIG_FILE = PROJECT_ROOT / "configs" / "model_spec_c2" / "CODEX_C2_CONFIG.json"

SUBMISSION_TEMPLATE = '''"""
Standalone Codex C2 V4 submission file for Kaggle Kaggriculture.
Generated automatically from frozen Codex C2 V4 Candidate (C2 Performance Iteration).
"""

from __future__ import annotations

from collections.abc import Callable
from copy import deepcopy
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
# --- Codex C2 Strategy & Agent Class ---
# ==========================================
{codex_c2_code}

# ==========================================
# --- Kaggle Entrypoint ---
# ==========================================
_agent_factory: Callable[[dict[str, Any], Any], dict[str, Any]] | None = None


def agent(observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
    """Kaggle submission entry point for Codex C2 V4 Candidate."""
    global _agent_factory
    step = int(observation.get("step", 0))
    if step == 0 or _agent_factory is None:
        _agent_factory = create_agent()
    return _agent_factory(observation, configuration)
'''


def clean_imports(code: str, remove_prefixes: List[str]) -> str:
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
    with open(SRC_DIR / "strategy" / "codex_c2.py", "r", encoding="utf-8") as f:
        codex_code = f.read()

    crop_rules_idx = codex_code.find("CROP_RULES = {")
    codex_body = codex_code[crop_rules_idx:]

    old_load = """def load_candidate_config(
    path: Path | str = DEFAULT_CONFIG_PATH,
) -> dict[str, Any]:
    \"\"\"Load and validate the candidate-specific configuration.\"\"\"

    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)"""

    new_load = """def load_candidate_config(
    path: Path | str | None = None,
) -> dict[str, Any]:
    \"\"\"Load and validate the candidate-specific configuration.\"\"\"

    if path is not None and Path(path).exists():
        with Path(path).open("r", encoding="utf-8") as handle:
            config = json.load(handle)
    else:
        config = deepcopy(CODEX_C2_CONFIG)"""

    if old_load in codex_body:
        codex_body = codex_body.replace(old_load, new_load)

    return codex_body.strip()


def build_submission_codex(output_path: Optional[str] = None) -> Path:
    out_file = Path(output_path) if output_path else PROJECT_ROOT / "submission" / "submission_codex.py"
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config_obj = json.load(f)
    config_json = json.dumps(config_obj, indent=2)

    e16_base_code = extract_e16_base_definitions()
    codex_c2_code = extract_codex_c2_definitions()

    bundled_code = SUBMISSION_TEMPLATE.format(
        config_json=config_json,
        e16_base_code=e16_base_code,
        codex_c2_code=codex_c2_code,
    )

    bundled_code = "\n".join(line.rstrip() for line in bundled_code.splitlines()) + "\n"
    out_file.write_text(bundled_code, encoding="utf-8")
    print(f"Successfully generated Codex C2 V4 standalone submission at: {out_file}")
    return out_file


if __name__ == "__main__":
    build_submission_codex()
