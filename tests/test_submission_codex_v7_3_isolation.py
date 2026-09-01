"""Standalone build and parity checks for Codex V7.3."""

from __future__ import annotations

from pathlib import Path

from scripts.build_submission_codex_v7_3 import (
    build_submission_codex_v7_3,
)
from scripts.verify_submission_codex_v7_3 import verify_equivalence


def test_v7_3_builder_writes_separate_standalone_artifact():
    canonical = Path.cwd() / "submission" / "submission_codex.py"
    canonical_before = canonical.read_bytes()
    output = build_submission_codex_v7_3()

    assert output == (
        Path.cwd()
        / "submission"
        / "submission_codex_v7_3_dual_q1_cadence.py"
    )
    assert output.exists()
    assert canonical.read_bytes() == canonical_before
    bundled = output.read_text(encoding="utf-8")
    assert "CODEX-C2-V7.3-DUAL-Q1-CADENCE" in bundled
    assert "class CodexDualQ1CadenceAgent" in bundled
    assert "from agricola" not in bundled
    assert "import agricola" not in bundled
    assert "DEFAULT_CADENCE_CONFIG_PATH" not in bundled


def test_v7_3_submission_exact_prefix_parity():
    build_submission_codex_v7_3()
    assert verify_equivalence(
        seeds=(26090101,),
        seats=(0,),
        max_steps=240,
    )

