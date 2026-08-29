"""Script to bundle the independent Antigravity agent into a standalone submission file for Kaggle."""

from pathlib import Path
from typing import List, Optional
import re

SUBMISSION_TEMPLATE = '''"""
Standalone submission file for Kaggle Kaggriculture.
Generated automatically for Antigravity Independent Strategy Model (E14).
"""

from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
import math

# ==========================================
# --- Core State Wrapper ---
# ==========================================
{state_code}

# ==========================================
# --- Action Builder ---
# ==========================================
{actions_code}

# ==========================================
# --- Antigravity Strategy Config & Agent ---
# ==========================================
{config_code}

{agent_code}

# ==========================================
# --- Kaggle Entrypoint ---
# ==========================================
_antigravity_config = AntigravityConfig()
_antigravity_agent = AntigravityROIAgent(config=_antigravity_config)

def agent(observation: Dict[str, Any], configuration: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Kaggle submission entry point for Antigravity Independent Strategy Agent."""
    try:
        state = GameState(observation)
        return _antigravity_agent.act(state)
    except Exception:
        return {{"farmer": ["PASS"], "hands": [], "market": []}}
'''

def clean_imports(code: str, remove_prefixes: list) -> str:
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
        output_paths = ["submission/submission_antigravity.py"]
        
    project_root = Path(__file__).resolve().parent.parent
    src_dir = project_root / "src" / "agricola"

    with open(src_dir / "core" / "state.py", "r", encoding="utf-8") as f:
        state_code = clean_imports(f.read(), [
            "from typing import",
            "from dataclasses import",
            "import math",
        ])

    with open(src_dir / "core" / "actions.py", "r", encoding="utf-8") as f:
        actions_code = clean_imports(f.read(), [
            "from typing import",
            "from dataclasses import",
            "import math",
            "from agricola.core.state",
        ])

    with open(src_dir / "strategy" / "antigravity" / "config.py", "r", encoding="utf-8") as f:
        config_code = clean_imports(f.read(), [
            "from typing import",
            "from dataclasses import",
            "import math",
            "from agricola.core.state",
            "from agricola.core.actions",
        ])

    with open(src_dir / "strategy" / "antigravity" / "agent.py", "r", encoding="utf-8") as f:
        agent_code = clean_imports(f.read(), [
            "from typing import",
            "from dataclasses import",
            "import math",
            "from agricola.core.state",
            "from agricola.core.actions",
            "from agricola.strategy.antigravity",
        ])

    bundled_code = SUBMISSION_TEMPLATE.format(
        state_code=state_code.strip(),
        actions_code=actions_code.strip(),
        config_code=config_code.strip(),
        agent_code=agent_code.strip(),
    )

    for rel_path in output_paths:
        out_file = project_root / rel_path
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(bundled_code)
        print(f"Successfully generated standalone submission at: {out_file}")

if __name__ == "__main__":
    build_submission()
