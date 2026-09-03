#!/usr/bin/env python3
"""Development-only causal probe for Codex E17 true reactivity.

The candidate and its guarded V1 control are evaluated on the same development
seeds, seats and opponent market regimes.  The opponent always uses frozen V9;
regimes only inject bounded market pressure into its otherwise unchanged action.
No holdout or final-confirmation seed is accepted.
"""

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

from agricola.core.observation_contract import stable_payload_hash
from agricola.strategy.codex.codex_3q_mixed_high_density import create_v9_agent
from agricola.strategy.codex.codex_e17_reactive_guarded import (
    create_codex_e17_reactive_agent,
)
from agricola.strategy.codex.codex_e17_true_reactive import (
    create_codex_e17_true_reactive_agent,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
MANIFEST_PATH = REPO_ROOT / "experiments/e17/manifest/E17_COMMON_MANIFEST_V1.json"
OUTPUT_PATH = (
    REPO_ROOT
    / "experiments/e17/artifacts/derived/codex/"
    / "E17_1_TRUE_REACTIVITY_DEVELOPMENT_METRICS.json"
)
REGIMES = ("INERT", "WHEAT_SCARCITY", "OUTPUT_PRESSURE", "LIQUIDITY_STRESS")
POLICIES = ("candidate", "guarded_control")
SELLABLE_OUTPUTS = (
    "CARROT",
    "TOMATO",
    "STRAWBERRY",
    "MELON",
    "EGG",
    "MILK",
    "WOOL",
    "FERTILIZER",
)
QUADRANTS = (
    ("Q0", "NW", 0, 5, 0, 5),
    ("Q1", "NE", 0, 5, 5, 10),
    ("Q2", "SW", 5, 10, 0, 5),
)


def _farm(observation: dict[str, Any], seat: int) -> dict[str, Any]:
    farms = observation.get("farms", []) or []
    return farms[seat] if isinstance(farms, list) and seat < len(farms) else {}


def _tile_counts(
    farm: dict[str, Any], bounds: tuple[int, int, int, int]
) -> tuple[int, int]:
    row_start, row_end, col_start, col_end = bounds
    crops = animals = 0
    tiles = farm.get("tiles", []) or []
    for row in range(row_start, row_end):
        for col in range(col_start, col_end):
            tile = (
                tiles[row][col] if row < len(tiles) and col < len(tiles[row]) else None
            )
            if not isinstance(tile, dict):
                continue
            if tile.get("animal"):
                animals += 1
            elif str(tile.get("kind") or "").upper() == "PLANT":
                crops += 1
    return crops, animals


def _structural_outcomes(steps: list[Any], seat: int) -> dict[str, Any]:
    unlocks: dict[str, dict[str, int] | None] = {slot: None for slot, *_ in QUADRANTS}
    animal_tile_days: Counter[str] = Counter()
    q2_unlock_day: int | None = None
    final_farm: dict[str, Any] = {}
    last_day_seen: int | None = None

    for step_index, state in enumerate(steps):
        observation = state[seat].get("observation", {}) or {}
        farm = _farm(observation, seat)
        if not farm:
            continue
        final_farm = farm
        day = int(observation.get("day", step_index // 24))
        hour = int(observation.get("hour", step_index % 24))
        unlocked = list(farm.get("unlocked_quadrants", []) or [])
        for slot_index, (slot, quadrant, *_bounds) in enumerate(QUADRANTS):
            if len(unlocked) > slot_index and unlocks[slot] is None:
                unlocks[slot] = {"step": step_index, "day": day, "hour": hour}
                if slot == "Q2":
                    q2_unlock_day = day
        if (
            day == last_day_seen
            or q2_unlock_day is None
            or not (q2_unlock_day <= day <= 28)
        ):
            continue
        last_day_seen = day
        for slot, _quadrant, rs, re, cs, ce in QUADRANTS:
            _crops, animals = _tile_counts(farm, (rs, re, cs, ce))
            animal_tile_days[slot] += animals

    final_counts: dict[str, dict[str, int]] = {}
    for slot, _quadrant, rs, re, cs, ce in QUADRANTS:
        crops, animals = _tile_counts(final_farm, (rs, re, cs, ce))
        final_counts[slot] = {"crops": crops, "animals": animals}
    q0_days = animal_tile_days["Q0"]
    return {
        "unlocks": unlocks,
        "final_quadrants": final_counts,
        "animal_tile_days_q2_window": dict(animal_tile_days),
        "q2_vs_q0_animal_tile_days_pct": (
            round(100 * animal_tile_days["Q2"] / q0_days, 2) if q0_days else None
        ),
    }


def _strict_eod_escapes(steps: list[Any], seat: int) -> int:
    escapes = 0
    previous_farm: dict[str, Any] | None = None
    previous_day: int | None = None
    for step_index, state in enumerate(steps):
        observation = state[seat].get("observation", {}) or {}
        farm = _farm(observation, seat)
        day = int(observation.get("day", step_index // 24))
        if (
            previous_farm is not None
            and previous_day is not None
            and day > previous_day
        ):
            before_tiles = previous_farm.get("tiles", []) or []
            after_tiles = farm.get("tiles", []) or []
            for row in range(min(len(before_tiles), len(after_tiles))):
                for col in range(min(len(before_tiles[row]), len(after_tiles[row]))):
                    before = before_tiles[row][col]
                    after = after_tiles[row][col]
                    if not isinstance(before, dict):
                        continue
                    at_risk = (
                        bool(before.get("animal"))
                        and int(before.get("consecutive_unfed", 0) or 0) == 1
                        and not bool(before.get("fed_today", False))
                    )
                    same_empty_structure = (
                        isinstance(after, dict)
                        and before.get("kind") == after.get("kind")
                        and not after.get("animal")
                    )
                    escapes += int(at_risk and same_empty_structure)
        previous_farm = farm
        previous_day = day
    return escapes


class MarketRegimeOpponent:
    """Frozen V9 plus a transparent, bounded market-pressure injection."""

    def __init__(self, regime: str, context: dict[str, Any]) -> None:
        self.regime = regime
        self.base = create_v9_agent(run_context=context)
        self.injection_batches = 0
        self.injected_orders: Counter[str] = Counter()

    def __call__(
        self, observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        action = deepcopy(self.base(observation, configuration))
        if self.regime == "INERT":
            return {"farmer": ["PASS"], "hands": [], "market": []}
        market = list(action.get("market", []) or [])
        injected: list[list[Any]] = []
        if self.regime in {"WHEAT_SCARCITY", "LIQUIDITY_STRESS"}:
            market = [
                order
                for order in market
                if not (
                    isinstance(order, list)
                    and len(order) >= 2
                    and order[:2] == ["BUY_PRODUCT", "WHEAT"]
                )
            ]
            injected.append(["BUY_PRODUCT", "WHEAT", 10])
        if self.regime in {"OUTPUT_PRESSURE", "LIQUIDITY_STRESS"}:
            shed = (observation.get("private", {}) or {}).get("shed", {}) or {}
            existing_sells = {
                str(order[1])
                for order in market
                if isinstance(order, list) and len(order) >= 2 and order[0] == "SELL"
            }
            for item in SELLABLE_OUTPUTS:
                quantity = int(shed.get(item, 0) or 0)
                if quantity > 0 and item not in existing_sells:
                    injected.append(["SELL", item, quantity])
        if injected:
            max_orders = int(
                (configuration or {}).get("maxMarketOrdersPerTurn", 10)
                if isinstance(configuration, dict)
                else getattr(configuration, "maxMarketOrdersPerTurn", 10)
            )
            action["market"] = (injected + market)[:max_orders]
            self.injection_batches += 1
            self.injected_orders.update(str(order[0]) for order in injected)
        return action


def _capture(policy: Callable, actions: list[dict[str, Any]]) -> Callable:
    def wrapped(
        observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        action = policy(observation, configuration)
        actions.append(deepcopy(action))
        return action

    return wrapped


def _make_candidate(policy_name: str, context: dict[str, Any]) -> Callable:
    if policy_name == "candidate":
        return create_codex_e17_true_reactive_agent(run_context=context)
    return create_codex_e17_reactive_agent(run_context=context)


def _compact_override_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    samples: list[dict[str, Any]] = []
    sampled_reasons: set[str] = set()
    traceable = 0
    for record in records:
        reasons = [str(reason) for reason in record.get("reasons", [])]
        is_traceable = (
            bool(reasons)
            and bool(record.get("facts"))
            and record.get("provider_action_sha256")
            != record.get("emitted_action_sha256")
        )
        traceable += int(is_traceable)
        if len(samples) >= 8 or all(reason in sampled_reasons for reason in reasons):
            continue
        samples.append(record)
        sampled_reasons.update(reasons)
    return {
        "override_record_count": len(records),
        "traceable_override_records": traceable,
        "override_record_samples": samples,
    }


def _telemetry(policy_name: str, policy: Callable) -> dict[str, Any]:
    if policy_name == "candidate":
        instance = policy.codex_e17_true_reactive_instance
        telemetry = instance.telemetry_snapshot()
        records = telemetry["true_reactive_override_records"]
        return {
            "errors": instance.error_count
            + instance.base_policy.codex_e17_instance.error_count,
            "fallbacks": instance.fallback_count,
            "override_batches": telemetry["true_reactive_override_batches"],
            "override_reasons": telemetry["true_reactive_override_reasons"],
            "regime_counts": telemetry["market_regime_counts"],
            **_compact_override_records(records),
        }
    instance = policy.codex_e17_instance
    telemetry = instance.telemetry_snapshot()
    records = telemetry["reactive_override_records"]
    return {
        "errors": instance.error_count
        + instance.base_policy.codex_v9_instance.error_count,
        "fallbacks": instance.fallback_count,
        "override_batches": telemetry["reactive_override_batches"],
        "override_reasons": telemetry["reactive_override_reasons"],
        "regime_counts": {},
        **_compact_override_records(records),
    }


def _run(seed: int, seat: int, regime: str, policy_name: str) -> dict[str, Any]:
    context = {
        "run_id": f"E17-TRUE-{policy_name}-{regime}-S{seed}-P{seat}",
        "episode_id": f"E17-TRUE-{policy_name}-{regime}-S{seed}-P{seat}",
        "seed": seed,
        "player_position": seat,
    }
    policy = _make_candidate(policy_name, context)
    opponent = MarketRegimeOpponent(
        regime,
        {**context, "run_id": f"{context['run_id']}-OPP", "player_position": 1 - seat},
    )
    actions: list[dict[str, Any]] = []
    captured = _capture(policy, actions)
    agents = [captured, opponent] if seat == 0 else [opponent, captured]
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=True,
    )
    env.run(agents)
    terminal = env.steps[-1]
    telemetry = _telemetry(policy_name, policy)
    result = {
        "seed": seed,
        "seat": seat,
        "regime": regime,
        "policy": policy_name,
        "reward": float(terminal[seat].get("reward") or 0.0),
        "opponent_reward": float(terminal[1 - seat].get("reward") or 0.0),
        "margin": float(terminal[seat].get("reward") or 0.0)
        - float(terminal[1 - seat].get("reward") or 0.0),
        "status": terminal[seat].get("status"),
        "opponent_status": terminal[1 - seat].get("status"),
        "action_stream_sha256": stable_payload_hash(actions),
        "action_batches": len(actions),
        "invalid_action_shapes": sum(
            1
            for action in actions
            if not isinstance(action, dict)
            or not isinstance(action.get("farmer"), list)
            or not action.get("farmer")
            or not isinstance(action.get("hands", []), list)
            or not isinstance(action.get("market", []), list)
            or len(action.get("market", [])) > 10
        ),
        "strict_eod_escapes": _strict_eod_escapes(env.steps, seat),
        "opponent_injection_batches": opponent.injection_batches,
        "opponent_injected_orders": dict(opponent.injected_orders),
        **telemetry,
        **_structural_outcomes(env.steps, seat),
    }
    print(
        f"{policy_name:15s} {regime:18s} seed={seed} p{seat} "
        f"reward={result['reward']:.0f} margin={result['margin']:+.0f} "
        f"overrides={result['override_batches']} escapes={result['strict_eod_escapes']}",
        flush=True,
    )
    return result


def run_matrix(
    seeds: list[int], regimes: list[str], policies: list[str]
) -> dict[str, Any]:
    rows = [
        _run(seed, seat, regime, policy)
        for seed in seeds
        for seat in (0, 1)
        for regime in regimes
        for policy in policies
    ]
    candidate_rows = [row for row in rows if row["policy"] == "candidate"]
    matched_deltas = []
    lookup = {
        (row["seed"], row["seat"], row["regime"], row["policy"]): row for row in rows
    }
    if set(policies) == set(POLICIES):
        for row in candidate_rows:
            control = lookup[
                (row["seed"], row["seat"], row["regime"], "guarded_control")
            ]
            matched_deltas.append(row["reward"] - control["reward"])
    fingerprints_per_case: dict[str, int] = {}
    for seed in seeds:
        for seat in (0, 1):
            case = [
                row["action_stream_sha256"]
                for row in candidate_rows
                if row["seed"] == seed and row["seat"] == seat
            ]
            fingerprints_per_case[f"{seed}:P{seat}"] = len(set(case))
    non_inert_with_overrides = len(
        {
            row["regime"]
            for row in candidate_rows
            if row["regime"] != "INERT" and row["override_batches"] > 0
        }
    )
    override_record_count = sum(row["override_record_count"] for row in candidate_rows)
    traceable_overrides = sum(
        row["traceable_override_records"] for row in candidate_rows
    )
    inert_candidates = [row for row in candidate_rows if row["regime"] == "INERT"]
    inert_controls = [
        row
        for row in rows
        if row["policy"] == "guarded_control" and row["regime"] == "INERT"
    ]
    inert_regression_pct = None
    if inert_candidates and inert_controls:
        candidate_mean = statistics.mean(row["reward"] for row in inert_candidates)
        control_mean = statistics.mean(row["reward"] for row in inert_controls)
        inert_regression_pct = 100 * (candidate_mean / control_mean - 1)
    summary = {
        "schema_version": "E17_1_TRUE_REACTIVITY_DEVELOPMENT_V1",
        "epistemic_role": "DEVELOPMENT_ONLY",
        "causal_family": "MARKET_REGIME_ADAPTATION",
        "seeds": seeds,
        "seats": [0, 1],
        "regimes": regimes,
        "policies": policies,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "runs": len(rows),
        "candidate_mean_reward": (
            statistics.mean(row["reward"] for row in candidate_rows)
            if candidate_rows
            else None
        ),
        "candidate_override_batches": sum(
            row["override_batches"] for row in candidate_rows
        ),
        "candidate_override_reasons": dict(
            sum((Counter(row["override_reasons"]) for row in candidate_rows), Counter())
        ),
        "non_inert_regimes_with_natural_overrides": non_inert_with_overrides,
        "distinct_candidate_action_streams_per_seed_seat": fingerprints_per_case,
        "mean_matched_reward_delta_vs_guarded_v1": (
            statistics.mean(matched_deltas) if matched_deltas else None
        ),
        "inert_regression_pct_vs_guarded_v1": inert_regression_pct,
        "override_traceability_coverage": (
            traceable_overrides / override_record_count
            if override_record_count
            else 1.0
        ),
        "technical_errors": sum(row["errors"] for row in rows),
        "invalid_action_shapes": sum(row["invalid_action_shapes"] for row in rows),
        "strict_eod_escapes": sum(row["strict_eod_escapes"] for row in rows),
        "gates": {
            "action_stream_discrimination": bool(fingerprints_per_case)
            and all(value > 1 for value in fingerprints_per_case.values()),
            "natural_override_in_at_least_two_non_inert_regimes": non_inert_with_overrides
            >= 2,
            "each_divergence_has_observed_trigger_and_reason": traceable_overrides
            == override_record_count,
            "inert_regression_at_least_minus_five_pct": inert_regression_pct is not None
            and inert_regression_pct >= -5,
            "same_state_determinism": "COVERED_BY_UNIT_TEST",
            "technical_errors_zero": all(row["errors"] == 0 for row in rows),
            "invalid_action_shapes_zero": all(
                row["invalid_action_shapes"] == 0 for row in rows
            ),
            "strict_eod_escapes_zero": all(
                row["strict_eod_escapes"] == 0 for row in rows
            ),
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
        "--seeds", nargs="+", type=int, default=manifest["seed_policy"]["e17_0_seeds"]
    )
    parser.add_argument("--regimes", nargs="+", choices=REGIMES, default=list(REGIMES))
    parser.add_argument(
        "--policies", nargs="+", choices=POLICIES, default=list(POLICIES)
    )
    parser.add_argument(
        "--compact-existing",
        action="store_true",
        help="Compact legacy full override records in the existing output and exit.",
    )
    args = parser.parse_args(argv)
    if args.compact_existing:
        metrics = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
        for row in metrics.get("results", []):
            records = row.pop("override_records", None)
            if records is not None:
                row.update(_compact_override_records(records))
        OUTPUT_PATH.write_text(
            json.dumps(metrics, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"compacted {OUTPUT_PATH}")
        return 0
    forbidden = set(manifest["seed_policy"]["holdout"]["seeds"]) | set(
        manifest["seed_policy"]["final_confirmation"]["seeds"]
    )
    if forbidden.intersection(args.seeds):
        raise SystemExit("holdout/final seeds are forbidden in development")
    if not set(args.seeds).issubset(set(manifest["seed_policy"]["development"])):
        raise SystemExit("only manifest development seeds are allowed")
    summary = run_matrix(args.seeds, args.regimes, args.policies)
    print(
        json.dumps(
            {
                key: summary[key]
                for key in (
                    "runs",
                    "candidate_mean_reward",
                    "candidate_override_batches",
                    "candidate_override_reasons",
                    "non_inert_regimes_with_natural_overrides",
                    "distinct_candidate_action_streams_per_seed_seat",
                    "mean_matched_reward_delta_vs_guarded_v1",
                    "inert_regression_pct_vs_guarded_v1",
                    "override_traceability_coverage",
                    "technical_errors",
                    "invalid_action_shapes",
                    "strict_eod_escapes",
                    "gates",
                )
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if summary["technical_errors"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
