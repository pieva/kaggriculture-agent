"""Bundle the isolated Copilot strategy into a standalone Kaggle submission."""

from pathlib import Path
from typing import List, Optional

SUBMISSION_TEMPLATE = """\
# Standalone submission file for Kaggle Kaggriculture.
# Generated automatically for Copilot Independent Strategy Model (E14).

from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass

# ==========================================
# --- Core State Wrapper ---
# ==========================================
__STATE_CODE__

# ==========================================
# --- Action Builder ---
# ==========================================
__ACTIONS_CODE__

# ==========================================
# --- Shared Telemetry / Base ---
# ==========================================
__TELEMETRY_CODE__

# ==========================================
# --- Underlying Productive Mass ROI Agent ---
# ==========================================
__PRODUCTIVE_MASS_CODE__

# ==========================================
# --- Copilot Strategy Config & Agent ---
# ==========================================
__CONFIG_CODE__

__AGENT_CODE__

# ==========================================
# --- Kaggle Entrypoint ---
# ==========================================
_copilot_config = CopilotConfig()
_copilot_agent = CopilotROIAgent(config=_copilot_config)


def agent(observation: Dict[str, Any], configuration: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    \"\"\"Kaggle submission entry point for Copilot independent strategy.\"\"\"
    try:
        state = GameState(observation)
        return _copilot_agent.act(state)
    except Exception:
        return {"farmer": ["PASS"], "hands": [], "market": []}
"""


def clean_imports(code: str, remove_prefixes: List[str]) -> str:
    lines = code.split("\n")
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if any(stripped.startswith(prefix) for prefix in remove_prefixes):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def build_submission(output_paths: Optional[List[str]] = None) -> None:
    if output_paths is None:
        output_paths = ["submission/submission_copilot.py"]

    project_root = Path(__file__).resolve().parent.parent
    root_submission = project_root / "submission_copilot.py"
    if root_submission.exists():
        root_submission.unlink()

    src_dir = project_root / "src" / "agricola"

    with open(src_dir / "core" / "state.py", "r", encoding="utf-8") as f:
        state_code = clean_imports(
            f.read(),
            [
                "from typing import",
                "from dataclasses import",
                "import math",
            ],
        )

    with open(src_dir / "core" / "actions.py", "r", encoding="utf-8") as f:
        actions_code = clean_imports(
            f.read(),
            [
                "from typing import",
                "from dataclasses import",
                "import math",
                "from agricola.core.state",
            ],
        )

    with open(src_dir / "strategy" / "hybrid_livestock_cluster_roi.py", "r", encoding="utf-8") as f:
        hybrid_code = f.read()
        config_end_idx = hybrid_code.find("class HybridLivestockClusterROIAgent:")
        telemetry_code = clean_imports(
            hybrid_code[:config_end_idx],
            [
                "from typing import",
                "from dataclasses import",
                "from agricola.core.state",
                "from agricola.core.actions",
            ],
        )

    with open(src_dir / "strategy" / "productive_mass_roi.py", "r", encoding="utf-8") as f:
        pm_code = clean_imports(
            f.read(),
            [
                "from typing import",
                "from dataclasses import",
                "from agricola.core.state",
                "from agricola.core.actions",
                "from agricola.strategy.hybrid_livestock_cluster_roi",
            ],
        )

    with open(src_dir / "strategy" / "copilot" / "config.py", "r", encoding="utf-8") as f:
        config_code = clean_imports(
            f.read(),
            [
                "from dataclasses import",
                "from typing import",
            ],
        )

    with open(src_dir / "strategy" / "copilot" / "agent.py", "r", encoding="utf-8") as f:
        agent_code = clean_imports(
            f.read(),
            [
                "from typing import",
                "from dataclasses import",
                "from agricola.core.state",
                "from agricola.strategy.copilot.config",
                "from agricola.strategy.productive_mass_roi",
            ],
        )

    bundled_code = (
        SUBMISSION_TEMPLATE
        .replace("__STATE_CODE__", state_code.strip())
        .replace("__ACTIONS_CODE__", actions_code.strip())
        .replace("__TELEMETRY_CODE__", telemetry_code.strip())
        .replace("__PRODUCTIVE_MASS_CODE__", pm_code.strip())
        .replace("__CONFIG_CODE__", config_code.strip())
        .replace("__AGENT_CODE__", agent_code.strip())
    )

    for rel_path in output_paths:
        out_file = project_root / rel_path
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(bundled_code, encoding="utf-8")
        print(f"Successfully generated standalone submission at: {out_file}")


if __name__ == "__main__":
    build_submission()
