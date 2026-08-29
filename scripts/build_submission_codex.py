"""Build the Codex-owned standalone Kaggriculture submission."""

from pathlib import Path


SUBMISSION_TEMPLATE = '''"""
Standalone Codex submission file for Kaggle Kaggriculture.
Generated automatically by scripts/build_submission_codex.py
Strategy: E12-X1.15 Codex independent candidate, variant X115D.
"""

from typing import Dict, Any, List, Optional, Tuple, Set

# --- Core State Wrapper ---
{state_code}

# --- Action Builder ---
{actions_code}

# --- Shared Config & Telemetry ---
{telemetry_code}

# --- Productive Mass ROI Agent Strategy ---
{strategy_code}

# --- Kaggle Entrypoint ---
_config = ProductiveMassConfig(
    productive_core_mode="E12_X115_CODEX_INDEPENDENT",
    enable_land_expansion=True,
    target_cows=12,
    target_sheep=3,
    max_workers=6,
    stop_hire_day=1,
    x115_variant="D",
    x115_max_hands=12,
)
_agent_instance = ProductiveMassROIAgent(config=_config)


def agent(observation: Dict[str, Any], configuration: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Kaggle submission entry point for the Codex-owned candidate."""
    try:
        state = GameState(observation)
        return _agent_instance.act(state)
    except Exception:
        return {{"farmer": ["PASS"], "hands": [], "market": []}}
'''


def clean_imports(code: str, remove_internal_imports: list[str]) -> str:
    """Strip imports that are already bundled in the standalone file."""
    cleaned = []
    for line in code.split("\n"):
        if any(imp in line for imp in remove_internal_imports):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def remove_method(code: str, method_name: str) -> str:
    """Remove a class-level method block from bundled standalone code."""
    lines = code.split("\n")
    output = []
    skipping = False
    target = f"    def {method_name}("
    for line in lines:
        if line.startswith(target):
            skipping = True
            continue
        if skipping and line.startswith("    def "):
            skipping = False
        if not skipping:
            output.append(line)
    return "\n".join(output)


def clean_codex_strategy(code: str) -> str:
    """Remove unrelated agent branches from the Codex standalone bundle."""
    code = remove_method(code, "_decide_e12_x115_antigravity_independent")
    code = remove_method(code, "_decide_e12_x115_copilot_independent")

    cleaned = []
    skip_next_return = False
    blocked_markers = (
        "x115_antigravity",
        "E12_X115_ANTIGRAVITY_INDEPENDENT",
        "E12_X115_COPILOT_INDEPENDENT",
    )
    for line in code.split("\n"):
        if skip_next_return and "return self._decide_e12_x115_" in line:
            skip_next_return = False
            continue
        skip_next_return = False
        if any(marker in line for marker in blocked_markers):
            if line.lstrip().startswith("if self.config.productive_core_mode"):
                skip_next_return = True
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def build_submission_codex(output_path: str = "submission/submission_codex.py") -> Path:
    """Bundle the Codex candidate into the fixed Kaggle submission artifact."""
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src" / "agricola"

    with (src_dir / "core" / "state.py").open("r", encoding="utf-8") as fh:
        state_code = clean_imports(fh.read(), ["from typing import"])

    with (src_dir / "core" / "actions.py").open("r", encoding="utf-8") as fh:
        actions_code = clean_imports(fh.read(), ["from typing import"])

    with (src_dir / "strategy" / "hybrid_livestock_cluster_roi.py").open("r", encoding="utf-8") as fh:
        hybrid_code = fh.read()
        config_end_idx = hybrid_code.find("class HybridLivestockClusterROIAgent:")
        telemetry_code = clean_imports(
            hybrid_code[:config_end_idx],
            [
                "from typing import",
                "from agricola.core.state",
                "from agricola.core.actions",
            ],
        )

    with (src_dir / "strategy" / "productive_mass_roi.py").open("r", encoding="utf-8") as fh:
        strategy_code = clean_codex_strategy(clean_imports(
            fh.read(),
            [
                "from typing import",
                "from agricola.core.state",
                "from agricola.core.actions",
                "from agricola.strategy.hybrid_livestock_cluster_roi",
            ],
        ))

    bundled_code = SUBMISSION_TEMPLATE.format(
        state_code=state_code.strip(),
        actions_code=actions_code.strip(),
        telemetry_code=telemetry_code.strip(),
        strategy_code=strategy_code.strip(),
    )
    bundled_code = "\n".join(line.rstrip() for line in bundled_code.splitlines()) + "\n"

    out_file = project_root / output_path
    if out_file.name != "submission_codex.py":
        raise ValueError("Codex submission output must be named submission_codex.py")
    if out_file.parent != project_root / "submission":
        raise ValueError("Codex submission output must be in the submission directory")

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(bundled_code, encoding="utf-8")
    print(f"Successfully generated Codex standalone submission at: {out_file}")
    return out_file


if __name__ == "__main__":
    build_submission_codex()
