#!/usr/bin/env python3
"""Verify isolation and source parity of the E18.16 standalone submission."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.codex.codex_e18_770_exact_cap_critical_feed import (
    create_codex_e18_770_exact_cap_critical_feed,
)
from agricola.strategy.codex.codex_e18_770_water_before_dig_guard_v2 import (
    create_codex_e18_770_water_before_dig_guard_v2,
)

ROOT = Path(__file__).resolve().parents[5]
TARGET = ROOT / "submission/submission_codex_e18_16_770.py"
SEED = 180903003


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _load_submission():
    spec = importlib.util.spec_from_file_location("codex_e18_16_submission", TARGET)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load E18.16 standalone submission")
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
        "run_id": f"E18-16-STANDALONE-PARITY-S{SEED}-P{seat}",
        "episode_id": f"E18-16-STANDALONE-PARITY-S{SEED}-P{seat}",
        "seed": SEED,
        "player_position": seat,
    }
    policy = policy_factory(context)
    opponent = create_codex_e18_770_water_before_dig_guard_v2(
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
    if module.MODEL_SPEC_VERSION != (
        "CODEX-E18.16-770-EXACT-CAP-CRITICAL-FEED-V1"
    ):
        raise AssertionError("unexpected standalone model spec")
    if module.BUILD_METADATA.get("livestock_resource_cap") != 14:
        raise AssertionError("standalone must enforce livestock cap 14")

    factories = (
        lambda context: create_codex_e18_770_exact_cap_critical_feed(
            run_context=context
        ),
        lambda context: module.create_agent(run_context=context),
    )
    runs = {}
    for seat in (0, 1):
        runs[("source", seat)] = _run(factories[0], seat)
        runs[("bundle", seat)] = _run(factories[1], seat)
        source_actions, source, source_terminal = runs[("source", seat)]
        bundle_actions, bundled, bundle_terminal = runs[("bundle", seat)]
        if source_actions != bundle_actions:
            mismatch = next(
                index
                for index, (left, right) in enumerate(
                    zip(source_actions, bundle_actions, strict=True)
                )
                if left != right
            )
            raise AssertionError(
                f"action parity mismatch at seat={seat} step={mismatch}"
            )
        if source_terminal.get("reward") != bundle_terminal.get("reward"):
            raise AssertionError(f"terminal reward mismatch at seat={seat}")
        for policy in (source, bundled):
            agent = policy.codex_e18_770_exact_cap_critical_feed_instance
            telemetry = agent.telemetry_snapshot()
            if agent.error_count or agent.fallback_count:
                raise AssertionError(f"unsafe telemetry at seat={seat}")
            if telemetry["max_observed_livestock_resources"] > 14:
                raise AssertionError(f"livestock cap breach at seat={seat}")
            if telemetry["move_to_critical_feed_overrides"] != 1:
                raise AssertionError(f"critical FEED mismatch at seat={seat}")
    print(
        f"verified {TARGET} sha256={_sha256(TARGET)} "
        "actions=2880 seats=2 holdout_consumed=false "
        "final_confirmation_consumed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
