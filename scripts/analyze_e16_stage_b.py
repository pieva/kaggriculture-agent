"""Analyze Stage B after a positive frozen capacity gate."""

from __future__ import annotations

import json

from agricola.e16.analysis import (
    load_episode_results,
    render_analysis_markdown,
    validate_complete_matrix,
)
from agricola.e16.config import ConfigError, build_run_matrix, load_frozen_config
from agricola.e16.runner import RESULTS_ROOT


def main() -> int:
    config = load_frozen_config()
    gate_path = RESULTS_ROOT / "analysis" / "E16_STAGE_B_GATE.json"
    gate = json.loads(gate_path.read_text(encoding="utf-8"))
    if gate.get("gate_status") != "STAGE_B_AUTHORIZED":
        raise ConfigError("Stage B analysis is blocked without a positive gate")
    c_star = gate.get("selected_C_star")
    rows, _ = load_episode_results(RESULTS_ROOT / "stage_b")
    validate_complete_matrix(rows, build_run_matrix(config, "stage_b", c_star=c_star))
    output = render_analysis_markdown(rows, "stage_b")
    output_dir = RESULTS_ROOT / "analysis"
    (output_dir / "E16_STAGE_B_ANALYSIS.md").write_text(output, encoding="utf-8")
    (output_dir / "E16_TRAINING_REPORT.md").write_text(
        "# E16 Training Report\n\nStage A and Stage B frozen matrices completed. See the two stage analysis artifacts and gate JSON.\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
