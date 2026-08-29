"""Script to bundle the Agricola agent modules into a single standalone submission file for Kaggle."""

import os
from pathlib import Path

SUBMISSION_TEMPLATE = '''"""
Standalone submission file for Kaggle Kaggriculture.
Generated automatically by scripts/build_submission.py
Strategy: E12-X1.12 Truebelief Economic Engine Reconstruction ProductiveMassROIAgent
"""

from typing import Dict, Any, List, Optional, Tuple, Set

# --- Core State Wrapper ---
{state_code}

# --- Action Builder ---
{actions_code}

# --- Shared Config & Telemetry ---
{telemetry_code}

# --- E11 Productive Mass ROI Agent Strategy ---
{e11_strategy_code}

# --- Kaggle Entrypoint ---
_config = ProductiveMassConfig(
    productive_core_mode="E12_TRUEBELIEF_ENGINE_X112",
    enable_land_expansion=True,
    target_cows=7,
    target_sheep=4,
    max_workers=6,
    stop_hire_day=1,
)
_agent_instance = ProductiveMassROIAgent(config=_config)

def agent(observation: Dict[str, Any], configuration: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Kaggle submission entry point for E12-X1.12 baseline candidate."""
    try:
        state = GameState(observation)
        return _agent_instance.act(state)
    except Exception:
        return {{"farmer": ["PASS"], "hands": [], "market": []}}
'''



def clean_imports(code: str, remove_internal_imports: list) -> str:
    """Strip docstrings and internal package imports."""
    lines = code.split("\n")
    cleaned = []
    for line in lines:
        if any(imp in line for imp in remove_internal_imports):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def build_submission(output_path: str = "submission/submission.py") -> None:
    """Bundle all modules into output_path."""
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src" / "agricola"

    with open(src_dir / "core" / "state.py", "r", encoding="utf-8") as f:
        state_code = clean_imports(f.read(), ["from typing import"])

    with open(src_dir / "core" / "actions.py", "r", encoding="utf-8") as f:
        actions_code = clean_imports(f.read(), ["from typing import"])

    with open(src_dir / "strategy" / "hybrid_livestock_cluster_roi.py", "r", encoding="utf-8") as f:
        hybrid_code = f.read()
        config_end_idx = hybrid_code.find("class HybridLivestockClusterROIAgent:")
        telemetry_code = clean_imports(
            hybrid_code[:config_end_idx],
            [
                "from typing import",
                "from agricola.core.state",
                "from agricola.core.actions",
            ]
        )

    with open(src_dir / "strategy" / "productive_mass_roi.py", "r", encoding="utf-8") as f:
        e11_strategy_code = clean_imports(
            f.read(),
            [
                "from typing import",
                "from agricola.core.state",
                "from agricola.core.actions",
                "from agricola.strategy.hybrid_livestock_cluster_roi",
            ]
        )

    bundled_code = SUBMISSION_TEMPLATE.format(
        state_code=state_code.strip(),
        actions_code=actions_code.strip(),
        telemetry_code=telemetry_code.strip(),
        e11_strategy_code=e11_strategy_code.strip(),
    )

    out_file = project_root / output_path
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(bundled_code)

    print(f"Successfully generated standalone submission at: {out_file}")


if __name__ == "__main__":
    build_submission()
