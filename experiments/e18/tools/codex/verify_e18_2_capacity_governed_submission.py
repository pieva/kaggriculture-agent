#!/usr/bin/env python3
"""Verify isolation and full-episode parity of the E18.2 submission."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.codex.codex_e17_batched_cluster_routing_v4 import (
    create_codex_e17_batched_cluster_routing_v4,
)
from agricola.strategy.codex.codex_e18_capacity_governed_v4d import (
    create_codex_e18_capacity_governed_v4d,
)

ROOT = Path(__file__).resolve().parents[4]
TARGET = ROOT / "submission/submission_codex_e18_2_capacity_governed_v4d.py"
SEED = 180903003


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _load_submission():
    spec = importlib.util.spec_from_file_location("codex_e18_2_submission", TARGET)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load E18.2 standalone submission")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _capture(policy, actions: list[dict[str, Any]]):
    def wrapped(observation, configuration=None):
        action = policy(observation, configuration)
        actions.append(deepcopy(action))
        return action

    return wrapped


def _run(policy_factory, seat: int) -> tuple[list[dict[str, Any]], Any, Any]:
    context = {
        "run_id": f"E18-2-STANDALONE-PARITY-S{SEED}-P{seat}",
        "episode_id": f"E18-2-STANDALONE-PARITY-S{SEED}-P{seat}",
        "seed": SEED,
        "player_position": seat,
    }
    policy = policy_factory(context)
    opponent = create_codex_e17_batched_cluster_routing_v4(
        run_context={**context, "player_position": 1 - seat}
    )
    actions: list[dict[str, Any]] = []
    agents = (
        [_capture(policy, actions), opponent]
        if seat == 0
        else [opponent, _capture(policy, actions)]
    )
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": SEED, "turnsPerDay": 24},
        debug=False,
    )
    env.run(agents)
    return actions, policy, env.steps[-1][seat]


def main() -> int:
    text = TARGET.read_text(encoding="utf-8")
    if "from agricola." in text:
        raise AssertionError("standalone contains a live repository import")
    module = _load_submission()
    if module.MODEL_SPEC_VERSION != "CODEX-E18.2-CAPACITY-GOVERNED-V4D-V1":
        raise AssertionError("unexpected standalone model spec")
    if module.BUILD_METADATA.get("topology_reclaim_enabled") is not False:
        raise AssertionError("standalone must preserve the V4D topology")

    def source_factory(context):
        return create_codex_e18_capacity_governed_v4d(run_context=context)

    def standalone_factory(context):
        return module.create_agent(run_context=context)

    for seat in (0, 1):
        source_actions, source, source_terminal = _run(source_factory, seat)
        bundled_actions, bundled, bundled_terminal = _run(
            standalone_factory, seat
        )
        if source_actions != bundled_actions:
            mismatch = next(
                index
                for index, (left, right) in enumerate(
                    zip(source_actions, bundled_actions, strict=True)
                )
                if left != right
            )
            raise AssertionError(f"action parity mismatch at seat={seat} step={mismatch}")
        if source_terminal.get("reward") != bundled_terminal.get("reward"):
            raise AssertionError(f"terminal reward mismatch at seat={seat}")
        for policy in (source, bundled):
            telemetry = policy.codex_e18_capacity_governed_instance.telemetry_snapshot()
            if telemetry["technical_errors"] or telemetry["fallbacks"]:
                raise AssertionError(f"unsafe telemetry at seat={seat}: {telemetry}")
            if telemetry["committed_reclaims"]:
                raise AssertionError("default E18.2 unexpectedly changed topology")
    print(
        f"verified {TARGET} sha256={_sha256(TARGET)} "
        "seats=2 holdout_consumed=false final_confirmation_consumed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
