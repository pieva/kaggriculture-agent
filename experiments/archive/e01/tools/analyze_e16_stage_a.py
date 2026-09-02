"""Analyze the complete frozen Stage A matrix and compute C*."""

from __future__ import annotations

import json

from agricola.e16.analysis import (
    compute_stage_b_gate,
    file_sha256,
    load_episode_results,
    render_analysis_markdown,
    validate_complete_matrix,
)
from agricola.e16.config import REPO_ROOT, build_run_matrix, load_frozen_config
from agricola.e16.runner import RESULTS_ROOT


def main() -> int:
    config = load_frozen_config()
    rows, hashes = load_episode_results(RESULTS_ROOT / "stage_a")
    validate_complete_matrix(rows, build_run_matrix(config, "stage_a"))
    timestamp = max(row["completed_at"] for row in rows)
    analysis_path = REPO_ROOT / "src" / "agricola" / "e16" / "analysis.py"
    gate = compute_stage_b_gate(rows, hashes, file_sha256(analysis_path), timestamp)
    output_dir = RESULTS_ROOT / "analysis"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "E16_STAGE_A_ANALYSIS.md").write_text(
        render_analysis_markdown(rows, "stage_a"), encoding="utf-8"
    )
    (output_dir / "E16_STAGE_B_GATE.json").write_text(
        json.dumps(gate, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if gate["gate_status"] != "STAGE_B_AUTHORIZED":
        (output_dir / "E16_TRAINING_REPORT.md").write_text(
            "# E16 Training Report\n\nSTAGE_B_BLOCKED_NO_CAPACITY_ANCHOR\n\nNo HIGH-watering capacity cell met all four frozen advancement criteria.\n",
            encoding="utf-8",
        )
    print(json.dumps(gate, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
