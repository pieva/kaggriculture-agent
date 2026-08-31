"""Build script to bundle the frozen Antigravity C2 Livestock variant (LS1) into standalone submission_antigravity_livestock.py."""

from pathlib import Path
from typing import List, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ANTIGRAVITY_LS_DIR = PROJECT_ROOT / "src" / "agricola" / "strategy" / "antigravity_livestock"

SUBMISSION_TEMPLATE = '''"""
Standalone submission file for Kaggle Kaggriculture.
Generated automatically from Antigravity C2 Livestock Diagnostic Variant (LS1).
"""

from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Any, Dict, List, Optional, Set, Tuple

# ====================================================
# --- Antigravity C2 Livestock Configuration ---
# ====================================================
{config_code}

# ====================================================
# --- Antigravity C2 Livestock Decision Policy ---
# ====================================================
{policy_code}

# ====================================================
# --- Antigravity C2 Livestock Agent Class ---
# ====================================================
{agent_code}

# ====================================================
# --- Kaggle Entrypoint ---
# ====================================================
_agent_instance = AntigravityC2LivestockAgent()


def agent(observation: Dict[str, Any], configuration: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Kaggle submission entry point for Antigravity C2 Livestock Strategy Agent."""
    return _agent_instance(observation, configuration)
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


def build_submission_antigravity_livestock(output_path: Optional[str] = None) -> Path:
    out_file = Path(output_path) if output_path else PROJECT_ROOT / "submission" / "submission_antigravity_livestock.py"
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with open(ANTIGRAVITY_LS_DIR / "c2_livestock_config.py", "r", encoding="utf-8") as f:
        config_code = clean_imports(f.read(), [
            "from __future__ import annotations",
            "from dataclasses import",
            "from typing import",
            "import math",
        ])

    with open(ANTIGRAVITY_LS_DIR / "c2_livestock_policy.py", "r", encoding="utf-8") as f:
        policy_code = clean_imports(f.read(), [
            "from __future__ import annotations",
            "from dataclasses import",
            "from typing import",
            "import math",
            "from agricola.strategy.antigravity_livestock.c2_livestock_config",
        ])

    with open(ANTIGRAVITY_LS_DIR / "agent_c2_livestock.py", "r", encoding="utf-8") as f:
        agent_code = clean_imports(f.read(), [
            "from __future__ import annotations",
            "from typing import",
            "from agricola.strategy.antigravity_livestock.c2_livestock_config",
            "from agricola.strategy.antigravity_livestock.c2_livestock_policy",
        ])

    bundled_code = SUBMISSION_TEMPLATE.format(
        config_code=config_code.strip(),
        policy_code=policy_code.strip(),
        agent_code=agent_code.strip(),
    )

    out_file.write_text(bundled_code, encoding="utf-8")
    print(f"Generated Antigravity Livestock standalone submission at: {out_file}")
    return out_file


if __name__ == "__main__":
    build_submission_antigravity_livestock()
