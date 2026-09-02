#!/usr/bin/env python3
"""Verify isolation and exact action parity of the E17 external submission."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

from agricola.strategy.codex.codex_3q_mixed_high_density import create_v9_agent


ROOT = Path(__file__).resolve().parents[4]
TARGET = ROOT / "submission" / "submission_codex.py"
EXPECTED_RELEASE = "CODEX-E17.0-EXTERNAL-CONTROL-V1"


def _load():
    spec = importlib.util.spec_from_file_location("codex_e17_external", TARGET)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {TARGET}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _observation(step: int) -> dict:
    farm = {
        "money": 3000.0,
        "farmer": [4, 4],
        "hands": [],
        "tiles": [[None for _ in range(10)] for _ in range(10)],
        "unlocked_quadrants": ["NW"],
    }
    return {
        "step": step,
        "day": step // 24,
        "hour": step % 24,
        "player": 0,
        "farms": [farm, farm],
        "private": {"inventories": [{}], "seeds": {}, "shed": {}},
        "market": {"prices": {}, "inventory": {}},
    }


def main() -> int:
    isolated = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            (
                "import importlib.util;"
                f"p={str(TARGET)!r};"
                "s=importlib.util.spec_from_file_location('iso',p);"
                "m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"
                "assert callable(m.agent);assert callable(m.create_agent)"
            ),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if isolated.returncode != 0:
        raise RuntimeError(isolated.stderr)

    module = _load()
    if module.MODEL_SPEC_VERSION != EXPECTED_RELEASE:
        raise AssertionError("unexpected E17 release metadata")

    source = create_v9_agent()
    external = module.create_agent()
    for step in range(719):
        observation = _observation(step)
        expected = source(observation, {"episodeSteps": 720, "turnsPerDay": 24})
        observed = external(observation, {"episodeSteps": 720, "turnsPerDay": 24})
        if expected != observed:
            raise AssertionError(f"action mismatch at step {step}")

    print(
        "isolated_import=PASS release_metadata=PASS "
        "behavioral_parity=719/719"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
