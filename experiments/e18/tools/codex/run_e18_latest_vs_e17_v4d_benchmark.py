#!/usr/bin/env python3
"""Benchmark the exact E18.1 Kaggle bundle against the frozen E17 V4D bundle.

The new matrix runs a direct 14-match comparison and evaluates V4D against
the three opponents already used by the frozen E18 four-agent tournament.
Only preregistered E18 development seeds are used.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import statistics
import sys
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.antigravity.antigravity_e17_native_3q import (
    create_e17_native_agent as create_antigravity_agent,
)
from agricola.strategy.claude.e18_opponent_reactive_v1 import (
    create_claude_e18_agent_v1,
)
from agricola.strategy.copilot.e18_opponent_reactive_v1 import (
    create_copilot_e18_opponent_reactive_v1,
)
from experiments.e17.tools.common import (
    run_e17_three_agent_development_tournament_v2 as base,
)
from experiments.e18.tools.common import (
    run_e18_dynamic_architecture_tournament_v1 as prior,
)
from experiments.e18.tools.common import (
    run_e18_four_agent_reactive_tournament_v2 as four_agent,
)

ROOT = Path(__file__).resolve().parents[4]
MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"
LATEST_SOURCE = ROOT / "submission/submission_codex_e18_opponent_reactive_662_770.py"
V4D_SOURCE = ROOT / "submission/submission_codex_e17_v4d.py"
FOUR_AGENT_ARTIFACT = (
    ROOT
    / "experiments/e18/artifacts/derived/common/"
    / "E18_FOUR_AGENT_REACTIVE_TOURNAMENT_V2.json"
)
OUTPUT_JSON = (
    ROOT
    / "experiments/e18/artifacts/derived/codex/"
    / "E18_CODEX_LATEST_VS_E17_V4D_BENCHMARK_V1.json"
)
OUTPUT_CSV = OUTPUT_JSON.with_suffix(".csv")

LATEST = "CODEX_E18_1_STANDALONE"
V4D = "CODEX_E17_V4D_STANDALONE"
CLAUDE = four_agent.CLAUDE
COPILOT = four_agent.COPILOT
ANTIGRAVITY = four_agent.ANTIGRAVITY
COMMON_OPPONENTS = (CLAUDE, COPILOT, ANTIGRAVITY)
PARTICIPANTS = (LATEST, V4D, *COMMON_OPPONENTS)
PAIRS = (
    (LATEST, V4D),
    (V4D, CLAUDE),
    (V4D, COPILOT),
    (V4D, ANTIGRAVITY),
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _load_submission(path: Path, module_name: str) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load standalone submission: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


LATEST_MODULE = _load_submission(LATEST_SOURCE, "_benchmark_e18_latest")
V4D_MODULE = _load_submission(V4D_SOURCE, "_benchmark_e17_v4d")


def _factory(name: str, seed: int, seat: int) -> tuple[Callable[..., Any], Any]:
    context = {
        "run_id": f"E18-LATEST-V4D-S{seed}-P{seat}-{name}",
        "episode_id": f"E18-LATEST-V4D-S{seed}-P{seat}-{name}",
        "seed": seed,
        "player_position": seat,
    }
    if name == LATEST:
        policy = LATEST_MODULE.create_agent(run_context=context)
        return policy, policy.codex_e18_opponent_reactive_instance
    if name == V4D:
        policy = V4D_MODULE.create_agent(run_context=context)
        return policy, policy.codex_e17_batched_cluster_routing_instance
    if name == CLAUDE:
        policy = create_claude_e18_agent_v1(run_context=context)
        return policy, policy
    if name == COPILOT:
        policy = create_copilot_e18_opponent_reactive_v1(run_context=context)
        return policy, policy
    if name == ANTIGRAVITY:
        policy = create_antigravity_agent(run_context=context)
        return policy, policy.antigravity_e17_native_instance
    raise ValueError(name)


def _controller_diagnostics(name: str, controller: Any) -> tuple[int, int]:
    errors = int(
        getattr(
            controller,
            "error_count" if name in {LATEST, V4D, ANTIGRAVITY} else "technical_errors",
            0,
        )
    )
    return errors, int(getattr(controller, "fallback_count", 0))


def _regime_metrics(name: str, controller: Any) -> dict[str, Any]:
    if name == LATEST:
        return four_agent._regime_metrics(four_agent.CODEX, controller)
    if name == V4D:
        return {
            "final_regime": "STATIC_V4D",
            "regime_signature": ["STATIC_V4D"],
            "mode_decisions": 0,
            "regime_transitions": 0,
            "decision_day": None,
            "decision_pressure": None,
        }
    return four_agent._regime_metrics(name, controller)


def _farm_surface(farm: dict[str, Any]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for row in farm.get("tiles", []) or []:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            kind = str(tile.get("kind", ""))
            if kind == "PLANT":
                counts["crops"] += 1
                if not bool(tile.get("watered_today", False)):
                    counts["unwatered"] += 1
                if int(tile.get("consecutive_unwatered", 0) or 0) > 0:
                    counts["water_stressed"] += 1
                if int(tile.get("yield_units", 0) or 0) > 0:
                    counts["harvest_ready"] += 1
            elif kind == "WEED":
                counts["weeds"] += 1
            elif kind == "PASTURE":
                counts["pastures"] += 1
                if tile.get("animal"):
                    counts["animals"] += 1
    return {key: int(value) for key, value in counts.items()}


def _lifecycle_metrics(env: Any, seat: int) -> dict[str, Any]:
    daily: list[dict[str, int]] = []
    sell_units: Counter[str] = Counter()
    sell_value: Counter[str] = Counter()
    market_orders: Counter[str] = Counter()
    for state in env.steps:
        record = state[seat]
        observation = record.get("observation", {}) or {}
        farm = base._farm(state, seat)
        for order in (record.get("action", {}) or {}).get("market", []) or []:
            if not order:
                continue
            opcode = str(order[0])
            market_orders[opcode] += 1
            if opcode != "SELL" or len(order) < 3:
                continue
            item = str(order[1])
            quantity = max(0, int(order[2]))
            prices = (observation.get("market", {}) or {}).get("prices", {}) or {}
            sell_units[item] += quantity
            sell_value[item] += quantity * float(prices.get(item, 0.0) or 0.0)
        if int(observation.get("hour", -1)) != 23:
            continue
        surface = _farm_surface(farm)
        daily.append(
            {
                "display_day": int(observation.get("day", 0)) + 1,
                "crops": surface.get("crops", 0),
                "unwatered": surface.get("unwatered", 0),
                "water_stressed": surface.get("water_stressed", 0),
                "harvest_ready": surface.get("harvest_ready", 0),
                "weeds": surface.get("weeds", 0),
                "pastures": surface.get("pastures", 0),
                "animals": surface.get("animals", 0),
            }
        )
    late = [row for row in daily if row["display_day"] >= 21]
    return {
        "crop_tile_days_total": sum(row["crops"] for row in daily),
        "crop_tile_days_d21_d30": sum(row["crops"] for row in late),
        "unwatered_tile_days_total": sum(row["unwatered"] for row in daily),
        "unwatered_tile_days_d21_d30": sum(row["unwatered"] for row in late),
        "water_stressed_tile_days_total": sum(row["water_stressed"] for row in daily),
        "harvest_ready_tile_days_total": sum(row["harvest_ready"] for row in daily),
        "weed_tile_days_total": sum(row["weeds"] for row in daily),
        "weed_tile_days_d21_d30": sum(row["weeds"] for row in late),
        "sell_units": dict(sorted(sell_units.items())),
        "sell_units_total": sum(sell_units.values()),
        "sell_value": dict(sorted(sell_value.items())),
        "sell_value_total": float(sum(sell_value.values())),
        "market_order_counts": dict(sorted(market_orders.items())),
    }


def _seat_metrics(
    env: Any,
    seat: int,
    name: str,
    controller: Any,
) -> dict[str, Any]:
    metrics = base._seat_metrics(env, seat, "E18_GENERIC", controller)
    errors, fallbacks = _controller_diagnostics(name, controller)
    metrics["technical_errors"] = errors
    metrics["fallbacks"] = fallbacks
    metrics["tile_animal_day_drops"] = metrics["animal_escapes"]
    metrics["verified_livestock_losses"] = prior._verified_livestock_losses(env, seat)
    metrics["animal_escapes"] = metrics["verified_livestock_losses"]
    pasture_profile = prior._pasture_profile(base._farm(env.steps[-1], seat))
    metrics["final_pasture_profile"] = pasture_profile
    metrics["final_pasture_profile_hash"] = four_agent._payload_hash(pasture_profile)
    metrics["action_stream_hash"] = prior._action_stream_hash(env, seat)
    metrics["action_count_profile_hash"] = four_agent._payload_hash(
        metrics["action_counts"]
    )
    metrics.update(_regime_metrics(name, controller))
    metrics.update(_lifecycle_metrics(env, seat))
    architecture = {
        "pastures": pasture_profile,
        "final_quadrants": metrics["final_quadrants"],
        "peak_hands": metrics["peak_hands"],
        "peak_crops": metrics["peak_crops"],
        "peak_animals": metrics["peak_animals"],
        "final_crops": metrics["final_crops"],
        "final_animals": metrics["final_animals"],
        "final_weeds": metrics["final_weeds"],
        "regimes": metrics["regime_signature"],
    }
    metrics["architecture_profile_hash"] = four_agent._payload_hash(architecture)
    return metrics


def _run_match(seed: int, p0: str, p1: str) -> dict[str, Any]:
    policy0, controller0 = _factory(p0, seed, 0)
    policy1, controller1 = _factory(p1, seed, 1)
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=False,
    )
    env.run([policy0, policy1])
    metrics0 = _seat_metrics(env, 0, p0, controller0)
    metrics1 = _seat_metrics(env, 1, p1, controller1)
    winner = (
        p0
        if metrics0["money"] > metrics1["money"]
        else p1
        if metrics1["money"] > metrics0["money"]
        else "TIE"
    )
    return {
        "seed": seed,
        "p0": p0,
        "p1": p1,
        "winner": winner,
        "margin_p0": metrics0["money"] - metrics1["money"],
        "p0_metrics": metrics0,
        "p1_metrics": metrics1,
    }


def _records(
    matches: list[dict[str, Any]], participant: str, opponents: set[str] | None = None
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for match in matches:
        for seat in (0, 1):
            if match[f"p{seat}"] != participant:
                continue
            opponent = str(match[f"p{1 - seat}"])
            if opponents is not None and opponent not in opponents:
                continue
            rows.append(
                {
                    "seed": int(match["seed"]),
                    "seat": seat,
                    "opponent": opponent,
                    "winner": match["winner"],
                    "metrics": match[f"p{seat}_metrics"],
                }
            )
    return rows


SUMMARY_METRICS = (
    "money",
    "peak_hands",
    "peak_crops",
    "peak_animals",
    "peak_weeds",
    "final_crops",
    "final_animals",
    "final_weeds",
    "move_actions",
    "productive_actions",
    "pass_actions",
    "move_per_productive",
    "crop_tile_days_total",
    "crop_tile_days_d21_d30",
    "unwatered_tile_days_total",
    "unwatered_tile_days_d21_d30",
    "water_stressed_tile_days_total",
    "weed_tile_days_total",
    "weed_tile_days_d21_d30",
    "sell_units_total",
    "sell_value_total",
)


def _summary(records: list[dict[str, Any]], participant: str) -> dict[str, Any]:
    money = [float(record["metrics"]["money"]) for record in records]
    result: dict[str, Any] = {
        "matches": len(records),
        "wins": sum(record["winner"] == participant for record in records),
        "money_mean": statistics.mean(money),
        "money_median": statistics.median(money),
        "money_min": min(money),
        "money_max": max(money),
        "money_stdev": statistics.pstdev(money),
        "verified_livestock_losses": sum(
            int(record["metrics"].get("verified_livestock_losses", 0))
            for record in records
        ),
        "technical_errors": sum(
            int(record["metrics"].get("technical_errors", 0)) for record in records
        ),
        "fallbacks": sum(
            int(record["metrics"].get("fallbacks", 0)) for record in records
        ),
        "regimes": dict(
            Counter(str(record["metrics"].get("final_regime")) for record in records)
        ),
        "pasture_profiles": dict(
            Counter(
                record["metrics"]["final_pasture_profile_hash"] for record in records
            )
        ),
    }
    for key in SUMMARY_METRICS:
        values = [
            float(record["metrics"][key])
            for record in records
            if record["metrics"].get(key) is not None
        ]
        if values:
            result[f"{key}_mean"] = statistics.mean(values)
    return result


def _delta(latest: dict[str, Any], v4d: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key in sorted(set(latest).intersection(v4d)):
        if not key.endswith("_mean") or not isinstance(latest[key], (int, float)):
            continue
        left = float(latest[key])
        right = float(v4d[key])
        result[key] = {
            "latest": left,
            "v4d": right,
            "absolute": left - right,
            "percent_vs_v4d": ((left - right) / right * 100) if right else None,
        }
    return result


def _write_csv(matches: list[dict[str, Any]]) -> None:
    fields = [
        "seed",
        "seat",
        "participant",
        "opponent",
        "winner",
        *SUMMARY_METRICS,
        "final_regime",
        "verified_livestock_losses",
        "technical_errors",
        "fallbacks",
    ]
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for match in matches:
            for seat in (0, 1):
                metrics = match[f"p{seat}_metrics"]
                writer.writerow(
                    {
                        "seed": match["seed"],
                        "seat": seat,
                        "participant": match[f"p{seat}"],
                        "opponent": match[f"p{1 - seat}"],
                        "winner": match["winner"],
                        **{key: metrics.get(key) for key in fields[5:]},
                    }
                )


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    seeds = [int(value) for value in manifest["seed_policy"]["development"]]
    reserved = {
        *map(int, manifest["seed_policy"]["holdout"]["seeds"]),
        *map(int, manifest["seed_policy"]["final_confirmation"]["seeds"]),
    }
    if set(seeds).intersection(reserved):
        raise RuntimeError("development matrix overlaps reserved seeds")

    matches: list[dict[str, Any]] = []
    total = len(PAIRS) * len(seeds) * 2
    for left, right in PAIRS:
        for seed in seeds:
            for p0, p1 in ((left, right), (right, left)):
                match = _run_match(seed, p0, p1)
                matches.append(match)
                print(
                    f"[{len(matches):02d}/{total}] seed={seed} {p0} vs {p1} "
                    f"winner={match['winner']} margin_p0={match['margin_p0']:.0f}",
                    flush=True,
                )

    direct_latest = _summary(_records(matches, LATEST, {V4D}), LATEST)
    direct_v4d = _summary(_records(matches, V4D, {LATEST}), V4D)
    v4d_common = _summary(_records(matches, V4D, set(COMMON_OPPONENTS)), V4D)

    frozen = json.loads(FOUR_AGENT_ARTIFACT.read_text(encoding="utf-8"))
    latest_common_records = _records(
        frozen["matches"], four_agent.CODEX, set(COMMON_OPPONENTS)
    )
    latest_common = _summary(latest_common_records, four_agent.CODEX)
    common_money_delta = {
        "latest_mean": latest_common["money_mean"],
        "v4d_mean": v4d_common["money_mean"],
        "absolute": latest_common["money_mean"] - v4d_common["money_mean"],
        "percent_vs_v4d": (
            (latest_common["money_mean"] - v4d_common["money_mean"])
            / v4d_common["money_mean"]
            * 100
        ),
    }

    payload = {
        "schema_version": "E18_CODEX_LATEST_VS_E17_V4D_BENCHMARK_V1",
        "epistemic_role": "DEVELOPMENT_ONLY_NON_QUALIFYING",
        "date": "2026-09-03",
        "seeds": seeds,
        "seats": [0, 1],
        "new_match_count": len(matches),
        "pairs": [list(pair) for pair in PAIRS],
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "provenance": {
            LATEST: {
                "path": str(LATEST_SOURCE.relative_to(ROOT)).replace("\\", "/"),
                "sha256": _sha256(LATEST_SOURCE),
            },
            V4D: {
                "path": str(V4D_SOURCE.relative_to(ROOT)).replace("\\", "/"),
                "sha256": _sha256(V4D_SOURCE),
            },
            "reused_e18_four_agent_artifact": {
                "path": str(FOUR_AGENT_ARTIFACT.relative_to(ROOT)).replace("\\", "/"),
                "sha256": _sha256(FOUR_AGENT_ARTIFACT),
            },
        },
        "direct_head_to_head": {
            "latest": direct_latest,
            "v4d": direct_v4d,
            "delta_latest_minus_v4d": _delta(direct_latest, direct_v4d),
        },
        "common_opponent_pool": {
            "opponents": list(COMMON_OPPONENTS),
            "latest_reused_from_frozen_v2": latest_common,
            "v4d_new": v4d_common,
            "money_delta_latest_minus_v4d": common_money_delta,
            "comparability": "SAME_SEEDS_SEATS_AND_FROZEN_OPPONENT_FACTORIES",
        },
        "matches": matches,
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    _write_csv(matches)
    print(f"wrote {OUTPUT_JSON}")
    print(f"wrote {OUTPUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
