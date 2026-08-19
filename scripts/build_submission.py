"""Script to bundle the Agricola agent modules into a single standalone submission file for Kaggle."""

import os
from pathlib import Path

SUBMISSION_TEMPLATE = '''"""
Standalone submission file for Kaggle Kaggriculture.
Generated automatically by scripts/build_submission.py
"""

from typing import Dict, Any, List, Optional, Tuple

# --- Core State Wrapper ---
{state_code}

# --- Action Builder ---
{actions_code}

# --- ROI Crop Agent Strategy ---
{strategy_code}

# --- Kaggle Entrypoint ---
_agent_instance = ROICropAgent()

def agent(observation: Dict[str, Any], configuration: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Kaggle submission entry point."""
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

    with open(src_dir / "strategy" / "roi_crop.py", "r", encoding="utf-8") as f:
        strategy_code = clean_imports(
            f.read(),
            ["from typing import", "from agricola.core.state", "from agricola.core.actions"]
        )

    bundled_code = SUBMISSION_TEMPLATE.format(
        state_code=state_code.strip(),
        actions_code=actions_code.strip(),
        strategy_code=strategy_code.strip(),
    )

    out_file = project_root / output_path
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(bundled_code)

    print(f"Successfully generated standalone submission at: {out_file}")


if __name__ == "__main__":
    build_submission()
