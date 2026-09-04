#!/usr/bin/env python3
"""Verify isolation and two-regime parity of the E18 standalone submission."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.claude.e17_reactive_3q_v3 import (
    create_claude_e17_agent_v3,
)
from agricola.strategy.codex.codex_e18_opponent_reactive_topology import (
    E18_OPPONENT_REACTIVE_MODEL_SPEC_VERSION,
    create_codex_e18_opponent_reactive_topology,
)
from agricola.strategy.copilot.e17_native_3q import create_native_agent

ROOT = Path(__file__).resolve().parents[5]
TARGET = ROOT / "submission/submission_codex_e18_opponent_reactive_662_770.py"
EXPECTED_RELEASE = "CODEX-E18.1-OPPONENT-REACTIVE-662-770-KAGGLE-V1"
SEED = 180903001


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _action_hash(actions: list[dict[str, Any]]) -> str:
    payload = json.dumps(
        actions,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest().upper()


def _load_submission():
    spec = importlib.util.spec_from_file_location("codex_e18_submission", TARGET)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {TARGET}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _isolated_import() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            (
                "import importlib.util;"
                f"p={str(TARGET)!r};"
                "s=importlib.util.spec_from_file_location('iso',p);"
                "m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"
                "assert callable(m.agent);assert callable(m.create_agent);"
                f"assert m.RELEASE_ID=={EXPECTED_RELEASE!r};"
                "assert m.MODEL_SPEC_VERSION=="
                f"{E18_OPPONENT_REACTIVE_MODEL_SPEC_VERSION!r}"
            ),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout)


def _capture(policy, actions: list[dict[str, Any]]):
    def wrapped(observation, configuration=None):
        action = policy(observation, configuration)
        actions.append(deepcopy(action))
        return action

    return wrapped


def _run_pair(module, opponent_name: str, opponent_factory, expected_mode: str):
    context = {
        "run_id": f"E18-SUBMISSION-PARITY-{opponent_name}-S{SEED}",
        "episode_id": f"E18-SUBMISSION-PARITY-{opponent_name}-S{SEED}",
        "seed": SEED,
        "player_position": 0,
    }
    source = create_codex_e18_opponent_reactive_topology(
        run_context=deepcopy(context)
    )
    standalone = module.create_agent(run_context=deepcopy(context))
    source_actions: list[dict[str, Any]] = []
    standalone_actions: list[dict[str, Any]] = []
    environments = [
        make(
            "kaggriculture",
            configuration={"episodeSteps": 720, "seed": SEED, "turnsPerDay": 24},
            debug=False,
        )
        for _ in range(2)
    ]
    environments[0].run(
        [_capture(source, source_actions), opponent_factory()]
    )
    environments[1].run(
        [_capture(standalone, standalone_actions), opponent_factory()]
    )
    if source_actions != standalone_actions:
        raise AssertionError(f"{opponent_name}: action streams differ")
    if len(source_actions) != 719:
        raise AssertionError(f"{opponent_name}: unexpected action count")
    source_telemetry = (
        source.codex_e18_opponent_reactive_instance.telemetry_snapshot()
    )
    standalone_telemetry = (
        standalone.codex_e18_opponent_reactive_instance.telemetry_snapshot()
    )
    for telemetry in (source_telemetry, standalone_telemetry):
        if telemetry["topology_mode"] != expected_mode:
            raise AssertionError(f"{opponent_name}: wrong topology mode")
        if (
            telemetry["latest_target_pastures_built"] != 14
            or telemetry["latest_target_pastures_filled"] != 14
            or telemetry["latest_empty_target_pastures"] != 0
            or telemetry["topology_cap_breaches"] != 0
        ):
            raise AssertionError(f"{opponent_name}: invalid terminal topology")
    return {
        "opponent": opponent_name,
        "mode": expected_mode,
        "action_sha256": _action_hash(source_actions),
        "reward": float(environments[0].steps[-1][0].get("reward") or 0),
    }


def main() -> int:
    _isolated_import()
    module = _load_submission()
    results = [
        _run_pair(module, "CLAUDE_V3", create_claude_e17_agent_v3, "6-6-2"),
        _run_pair(module, "COPILOT_NATIVE", create_native_agent, "7-7-0"),
    ]
    print(
        "isolated_import=PASS parity=PASS "
        f"results={json.dumps(results, sort_keys=True)} "
        f"submission_sha256={_sha256(TARGET)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
