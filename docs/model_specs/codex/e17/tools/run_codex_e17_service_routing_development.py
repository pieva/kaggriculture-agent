#!/usr/bin/env python3
"""Matched development benchmark for the E17.2 service/routing core."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter
from collections.abc import Callable
from copy import deepcopy
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.core.benchmark_opponents import inert_pass_policy
from agricola.core.observation_contract import stable_payload_hash
from agricola.strategy.codex.codex_e17_reactive_service_routing_core import (
    create_codex_e17_reactive_service_routing_core,
)
from agricola.strategy.codex.codex_e17_true_reactive import (
    create_codex_e17_true_reactive_agent,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
MANIFEST_PATH = REPO_ROOT / "experiments/e17/manifest/E17_COMMON_MANIFEST_V1.json"
OUTPUT_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e17/artifacts/derived/"
    / "E17_2_REACTIVE_SERVICE_ROUTING_DEVELOPMENT_METRICS.json"
)
POLICIES = ("service_routing_core", "true_reactive_v2_control")
QUADRANTS = (
    ("Q0", 0, 5, 0, 5),
    ("Q1", 0, 5, 5, 10),
    ("Q2", 5, 10, 0, 5),
)


def _farm(observation: dict[str, Any], seat: int) -> dict[str, Any]:
    farms = observation.get("farms", []) or []
    return farms[seat] if isinstance(farms, list) and seat < len(farms) else {}


def _counts(farm: dict[str, Any]) -> dict[str, Any]:
    final: dict[str, Any] = {}
    for name, row_start, row_end, col_start, col_end in QUADRANTS:
        crops: Counter[str] = Counter()
        animals: Counter[str] = Counter()
        for y in range(row_start, row_end):
            for x in range(col_start, col_end):
                tile = _farm_tile(farm, x, y)
                if not isinstance(tile, dict):
                    continue
                if tile.get("animal"):
                    animals[str(tile["animal"])] += 1
                elif tile.get("kind") == "PLANT":
                    crops[str(tile.get("crop", "UNKNOWN"))] += 1
        final[name] = {
            "animals": sum(animals.values()),
            "animal_species": dict(animals),
            "crops": sum(crops.values()),
            "crop_species": dict(crops),
        }
    return final


def _farm_tile(farm: dict[str, Any], x: int, y: int) -> Any:
    rows = farm.get("tiles", []) or []
    if 0 <= y < len(rows) and 0 <= x < len(rows[y]):
        return rows[y][x]
    return None


def _eod_losses(steps: list[Any], seat: int) -> tuple[int, int]:
    escapes = crop_losses = 0
    previous_farm: dict[str, Any] | None = None
    previous_day: int | None = None
    for step_index, state in enumerate(steps):
        observation = state[seat].get("observation", {}) or {}
        farm = _farm(observation, seat)
        day = int(observation.get("day", step_index // 24))
        if previous_farm is not None and previous_day is not None and day > previous_day:
            for y, row in enumerate(previous_farm.get("tiles", []) or []):
                for x, before in enumerate(row):
                    after = _farm_tile(farm, x, y)
                    if not isinstance(before, dict):
                        continue
                    if before.get("animal"):
                        at_risk = (
                            int(before.get("consecutive_unfed", 0) or 0) == 1
                            and not bool(before.get("fed_today", False))
                        )
                        empty_structure = (
                            isinstance(after, dict)
                            and before.get("kind") == after.get("kind")
                            and not after.get("animal")
                        )
                        escapes += int(at_risk and empty_structure)
                    elif before.get("kind") == "PLANT":
                        at_risk = (
                            int(before.get("consecutive_unwatered", 0) or 0) == 1
                            and not bool(before.get("watered_today", False))
                        )
                        crop_losses += int(
                            at_risk
                            and isinstance(after, dict)
                            and after.get("kind") == "WEED"
                        )
        previous_farm = farm
        previous_day = day
    return escapes, crop_losses


def _unlock_timing(steps: list[Any], seat: int) -> dict[str, Any]:
    result: dict[str, Any] = {"Q0": None, "Q1": None, "Q2": None}
    for step_index, state in enumerate(steps):
        observation = state[seat].get("observation", {}) or {}
        unlocked = list(_farm(observation, seat).get("unlocked_quadrants", []) or [])
        for index, name in enumerate(("Q0", "Q1", "Q2")):
            if result[name] is None and len(unlocked) > index:
                result[name] = {
                    "step": step_index,
                    "day": int(observation.get("day", step_index // 24)),
                    "hour": int(observation.get("hour", step_index % 24)),
                }
    return result


def _capture(policy: Callable, actions: list[dict[str, Any]]) -> Callable:
    def wrapped(observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
        action = policy(observation, configuration)
        actions.append(deepcopy(action))
        return action

    return wrapped


def _make_policy(name: str, context: dict[str, Any]) -> Callable:
    if name == "service_routing_core":
        return create_codex_e17_reactive_service_routing_core(run_context=context)
    return create_codex_e17_true_reactive_agent(run_context=context)


def _telemetry(name: str, policy: Callable) -> dict[str, Any]:
    if name != "service_routing_core":
        instance = policy.codex_e17_true_reactive_instance
        return {
            "errors": instance.error_count,
            "fallbacks": instance.fallback_count,
            "routing_commands": 0,
            "service_commands": 0,
            "move_per_service": None,
            "market_mutations": 0,
            "ledger_record_count": 0,
            "ledger_classified_count": 0,
            "execution_outcomes": {},
            "action_counts": {},
            "task_counts": {},
            "decision_samples": [],
            "ledger_samples": [],
        }
    instance = policy.codex_e17_service_routing_core_instance
    telemetry = instance.telemetry_snapshot()
    records = telemetry["ledger_records"]
    classified = sum(
        1
        for record in records
        if record.get("outcome") in {"EXECUTED", "NOT_EXECUTED", "UNKNOWN"}
    )
    return {
        "errors": instance.error_count,
        "fallbacks": instance.fallback_count,
        "routing_commands": telemetry["routing_commands"],
        "service_commands": telemetry["service_commands"],
        "move_per_service": telemetry["move_per_service"],
        "market_mutations": telemetry["market_mutations"],
        "ledger_record_count": len(records),
        "ledger_classified_count": classified,
        "execution_outcomes": telemetry["execution_outcomes"],
        "action_counts": telemetry["action_counts"],
        "task_counts": telemetry["task_counts"],
        "decision_samples": telemetry["decision_samples"][:8],
        "ledger_samples": records[:8],
    }


def _run(seed: int, seat: int, policy_name: str) -> dict[str, Any]:
    context = {
        "run_id": f"E17-SERVICE-{policy_name}-S{seed}-P{seat}",
        "episode_id": f"E17-SERVICE-{policy_name}-S{seed}-P{seat}",
        "seed": seed,
        "player_position": seat,
    }
    policy = _make_policy(policy_name, context)
    actions: list[dict[str, Any]] = []
    agents = (
        [_capture(policy, actions), inert_pass_policy]
        if seat == 0
        else [inert_pass_policy, _capture(policy, actions)]
    )
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=True,
    )
    env.run(agents)
    terminal = env.steps[-1]
    final_observation = terminal[seat].get("observation", {}) or {}
    final_farm = _farm(final_observation, seat)
    escapes, crop_losses = _eod_losses(env.steps, seat)
    telemetry = _telemetry(policy_name, policy)
    row = {
        "seed": seed,
        "seat": seat,
        "policy": policy_name,
        "reward": float(terminal[seat].get("reward") or 0.0),
        "status": terminal[seat].get("status"),
        "opponent_reward": float(terminal[1 - seat].get("reward") or 0.0),
        "action_batches": len(actions),
        "action_stream_sha256": stable_payload_hash(actions),
        "invalid_action_shapes": sum(
            1
            for action in actions
            if not isinstance(action, dict)
            or not isinstance(action.get("farmer"), list)
            or not action.get("farmer")
            or not isinstance(action.get("hands", []), list)
            or not isinstance(action.get("market", []), list)
            or len(action.get("market", []) or []) > 10
        ),
        "strict_eod_escapes": escapes,
        "strict_eod_crop_losses": crop_losses,
        "max_hands": max(
            len(_farm(state[seat].get("observation", {}) or {}, seat).get("hands", []) or [])
            for state in env.steps
        ),
        "unlock_timing": _unlock_timing(env.steps, seat),
        "final_quadrants": _counts(final_farm),
        **telemetry,
    }
    print(
        f"{policy_name:24s} seed={seed} p{seat} reward={row['reward']:.0f} "
        f"route={row['routing_commands']} service={row['service_commands']} "
        f"escapes={escapes}",
        flush=True,
    )
    return row


def run_matrix(seeds: list[int]) -> dict[str, Any]:
    rows = [
        _run(seed, seat, policy_name)
        for seed in seeds
        for seat in (0, 1)
        for policy_name in POLICIES
    ]
    lookup = {
        (row["seed"], row["seat"], row["policy"]): row
        for row in rows
    }
    candidates = [row for row in rows if row["policy"] == "service_routing_core"]
    controls = [row for row in rows if row["policy"] == "true_reactive_v2_control"]
    deltas = [
        row["reward"]
        - lookup[(row["seed"], row["seat"], "true_reactive_v2_control")]["reward"]
        for row in candidates
    ]
    candidate_mean = statistics.mean(row["reward"] for row in candidates)
    control_mean = statistics.mean(row["reward"] for row in controls)
    regression_pct = 100 * (candidate_mean / control_mean - 1)
    ledger_records = sum(row["ledger_record_count"] for row in candidates)
    ledger_classified = sum(row["ledger_classified_count"] for row in candidates)
    summary = {
        "schema_version": "E17_2_REACTIVE_SERVICE_ROUTING_DEVELOPMENT_V1",
        "epistemic_role": "DEVELOPMENT_ONLY",
        "candidate": "CODEX-E17.2-REACTIVE-SERVICE-ROUTING-CORE-V2",
        "control": "CODEX-E17.1-TRUE-REACTIVE-V2",
        "causal_family": "REACTIVE_SERVICE_AND_ROUTING_CORE",
        "activation_day": 29,
        "seeds": seeds,
        "seats": [0, 1],
        "opponent": "INERT_PASS_POLICY",
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "runs": len(rows),
        "candidate_mean_reward": candidate_mean,
        "control_mean_reward": control_mean,
        "mean_matched_delta": statistics.mean(deltas),
        "min_matched_delta": min(deltas),
        "inert_regression_pct_vs_control": regression_pct,
        "routing_commands": sum(row["routing_commands"] for row in candidates),
        "service_commands": sum(row["service_commands"] for row in candidates),
        "market_mutations": sum(row["market_mutations"] for row in candidates),
        "ledger_record_count": ledger_records,
        "ledger_classification_coverage": (
            ledger_classified / ledger_records if ledger_records else 1.0
        ),
        "execution_outcomes": dict(
            sum((Counter(row["execution_outcomes"]) for row in candidates), Counter())
        ),
        "technical_errors": sum(row["errors"] for row in rows),
        "fallbacks": sum(row["fallbacks"] for row in rows),
        "invalid_action_shapes": sum(row["invalid_action_shapes"] for row in rows),
        "strict_eod_escapes": sum(row["strict_eod_escapes"] for row in candidates),
        "strict_eod_crop_losses": sum(
            row["strict_eod_crop_losses"] for row in candidates
        ),
        "gates": {
            "technical_errors_zero": all(row["errors"] == 0 for row in rows),
            "fallbacks_zero": all(row["fallbacks"] == 0 for row in rows),
            "invalid_action_shapes_zero": all(
                row["invalid_action_shapes"] == 0 for row in rows
            ),
            "market_mutations_zero": all(
                row["market_mutations"] == 0 for row in candidates
            ),
            "ledger_classification_coverage_one": ledger_classified == ledger_records,
            "animal_escapes_zero": all(
                row["strict_eod_escapes"] == 0 for row in candidates
            ),
            "inert_regression_at_least_minus_five_pct": regression_pct >= -5,
            "natural_routing_present": sum(
                row["routing_commands"] for row in candidates
            )
            > 0,
            "natural_service_present": sum(
                row["service_commands"] for row in candidates
            )
            > 0,
            "same_initial_state_determinism": "COVERED_BY_UNIT_TEST",
        },
        "results": rows,
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--seeds",
        nargs="+",
        type=int,
        default=manifest["seed_policy"]["e17_0_seeds"],
    )
    args = parser.parse_args(argv)
    forbidden = set(manifest["seed_policy"]["holdout"]["seeds"]) | set(
        manifest["seed_policy"]["final_confirmation"]["seeds"]
    )
    if forbidden.intersection(args.seeds):
        raise SystemExit("holdout/final seeds are forbidden in development")
    if not set(args.seeds).issubset(set(manifest["seed_policy"]["development"])):
        raise SystemExit("only manifest development seeds are allowed")
    summary = run_matrix(args.seeds)
    print(
        json.dumps(
            {key: value for key, value in summary.items() if key != "results"},
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if summary["technical_errors"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
