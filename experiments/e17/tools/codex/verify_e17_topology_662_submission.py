#!/usr/bin/env python3
"""Verify isolation and full-episode parity of the E17.3 6-6-2 submission."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

from kaggle_environments import make

from agricola.core.benchmark_opponents import inert_pass_policy
from agricola.strategy.codex.codex_e17_topology_cap_662 import (
    TOPOLOGY_662_MODEL_SPEC_VERSION,
    create_codex_e17_topology_cap_662,
)

ROOT = Path(__file__).resolve().parents[4]
TARGET = ROOT / "submission/submission_codex_e17_topology_662.py"
EXPECTED_RELEASE = "CODEX-E17.3-TOPOLOGY-FILL-662-KAGGLE-CANDIDATE-V2"
SEED = 26090102


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _action_hash(actions: list[dict]) -> str:
    payload = json.dumps(
        actions,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest().upper()


def _load_submission():
    spec = importlib.util.spec_from_file_location("codex_e17_topology_662", TARGET)
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
                f"{TOPOLOGY_662_MODEL_SPEC_VERSION!r}"
            ),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout)


def _capture(policy, actions: list[dict]):
    def wrapped(observation, configuration=None):
        action = policy(observation, configuration)
        actions.append(deepcopy(action))
        return action

    return wrapped


def main() -> int:
    _isolated_import()
    module = _load_submission()
    context = {
        "run_id": f"E17-TOPOLOGY-662-PARITY-S{SEED}",
        "episode_id": f"E17-TOPOLOGY-662-PARITY-S{SEED}",
        "seed": SEED,
        "player_position": 0,
    }
    source = create_codex_e17_topology_cap_662(run_context=context)
    standalone = module.create_agent(run_context=deepcopy(context))
    source_actions: list[dict] = []
    standalone_actions: list[dict] = []
    environments = [
        make(
            "kaggriculture",
            configuration={"episodeSteps": 720, "seed": SEED, "turnsPerDay": 24},
            debug=True,
        )
        for _ in range(2)
    ]
    environments[0].run([_capture(source, source_actions), inert_pass_policy])
    environments[1].run(
        [_capture(standalone, standalone_actions), inert_pass_policy]
    )
    if source_actions != standalone_actions:
        raise AssertionError("source and standalone action streams differ")
    if len(source_actions) != 719:
        raise AssertionError(f"unexpected action count: {len(source_actions)}")
    source_terminal = environments[0].steps[-1][0]
    standalone_terminal = environments[1].steps[-1][0]
    if source_terminal.get("reward") != standalone_terminal.get("reward"):
        raise AssertionError("source and standalone rewards differ")
    source_instance = source.codex_e17_topology_662_instance
    standalone_instance = standalone.codex_e17_topology_662_instance
    if source_instance.error_count or standalone_instance.error_count:
        raise AssertionError("technical error observed during parity run")
    if source_instance.fallback_count or standalone_instance.fallback_count:
        raise AssertionError("fallback observed during parity run")
    telemetry = standalone_instance.telemetry_snapshot()
    if (
        telemetry["latest_target_pastures_built"] != 14
        or telemetry["latest_target_pastures_filled"] != 14
        or telemetry["latest_empty_target_pastures"] != 0
        or telemetry["max_active_reclaimed_crops"] != 5
        or telemetry["max_observed_q2_pastures"] != 2
        or telemetry["topology_cap_breaches"] != 0
    ):
        raise AssertionError(f"unexpected terminal topology: {telemetry!r}")
    print(
        f"isolated_import=PASS action_parity=719/719 seed={SEED} "
        f"reward={float(source_terminal.get('reward') or 0):.0f} "
        f"action_sha256={_action_hash(source_actions)} "
        f"submission_sha256={_sha256(TARGET)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
