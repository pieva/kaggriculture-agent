#!/usr/bin/env python3
"""Verify the standalone Codex E17.1 reactive Kaggle probe."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

from kaggle_environments import make

from agricola.core.benchmark_opponents import inert_pass_policy
from agricola.strategy.codex.codex_e17_reactive_guarded import (
    create_codex_e17_reactive_agent,
)

ROOT = Path(__file__).resolve().parents[4]
TARGET = ROOT / "submission" / "submission_codex_e17_reactive.py"
REPLAY = ROOT / "data" / "replays" / "json" / "104498819.json"
EXPECTED_RELEASE = "CODEX-E17.1-3Q-REACTIVE-GUARDED-V1"


def _load(path: Path = TARGET):
    spec = importlib.util.spec_from_file_location("codex_e17_reactive_submission", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _set_wheat(private: dict, quantity: int) -> None:
    private.setdefault("shed", {})["WHEAT"] = quantity
    for inventory in private.get("inventories", []) or []:
        if isinstance(inventory, dict):
            inventory["WHEAT"] = 0


def _targeted_reactivity_parity(module) -> None:
    replay = json.loads(REPLAY.read_text(encoding="utf-8"))
    configuration = deepcopy(replay["configuration"])
    before = deepcopy(replay["steps"][195][0]["observation"])
    after = deepcopy(replay["steps"][196][0]["observation"])
    _set_wheat(before["private"], 0)
    _set_wheat(after["private"], 0)
    source = create_codex_e17_reactive_agent()
    standalone = module.create_agent()
    assert source(deepcopy(before), configuration) == standalone(
        deepcopy(before), configuration
    )
    expected = source(deepcopy(after), configuration)
    observed = standalone(deepcopy(after), configuration)
    assert expected == observed
    assert standalone.codex_e17_instance.override_count == 1


def _full_episode_parity(module, seed: int = 26090101) -> None:
    source = create_codex_e17_reactive_agent()
    standalone = module.create_agent()
    env_source = make(
        "kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=True
    )
    env_standalone = make(
        "kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=True
    )
    observations_source = env_source.reset()
    observations_standalone = env_standalone.reset()
    for turn in range(719):
        action_source = source(observations_source[0].observation)
        action_standalone = standalone(observations_standalone[0].observation)
        if action_source != action_standalone:
            raise AssertionError(f"action mismatch at turn {turn}")
        observations_source = env_source.step([action_source, inert_pass_policy({}, {})])
        observations_standalone = env_standalone.step(
            [action_standalone, inert_pass_policy({}, {})]
        )
        if observations_source[0].status in {"DONE", "INVALID", "ERROR"}:
            break
    assert observations_source[0].status == observations_standalone[0].status
    assert observations_source[0].reward == observations_standalone[0].reward
    assert source.codex_e17_instance.error_count == 0
    assert standalone.codex_e17_instance.error_count == 0


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
        raise AssertionError("unexpected reactive release metadata")
    _targeted_reactivity_parity(module)
    _full_episode_parity(module)
    print(
        "isolated_import=PASS targeted_reactivity_parity=PASS "
        "full_episode_parity=PASS holdout_consumed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
