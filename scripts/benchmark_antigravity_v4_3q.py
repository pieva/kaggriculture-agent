#!/usr/bin/env python3
"""Canonical, holdout, and replay verification for Antigravity V4.0 3Q High-Density."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections.abc import Callable
from copy import deepcopy
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.antigravity.agent_c2_3q_v4 import create_agent as create_v4_agent
from agricola.strategy.antigravity.antigravity_3q_high_density_v4 import (
    V4_SPEC_VERSION,
)

ROOT = Path(__file__).resolve().parents[1]
RESULT_DIR = ROOT / "docs" / "governance" / "history" / "model_spec_c2" / "antigravity"
RESULT_JSON = RESULT_DIR / "ANTIGRAVITY_V4_0_RESULTS.json"
RESULT_CSV = RESULT_DIR / "ANTIGRAVITY_V4_0_RESULTS.csv"
HOLDOUT_JSON = RESULT_DIR / "ANTIGRAVITY_V4_0_HOLDOUT_RESULTS.json"
HOLDOUT_CSV = RESULT_DIR / "ANTIGRAVITY_V4_0_HOLDOUT_RESULTS.csv"
REPLAY_PATH = ROOT / "data" / "replays" / "reference" / "104498819.json"
SEEDS = (26090101, 26090102, 26090103)
PHASE_C_SEEDS = (1838889274, 1619968655, 710418712)
SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}
AgentFactory = Callable[[dict[str, Any]], Callable]


def inert_policy(observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
    del observation, configuration
    return deepcopy(SAFE_PASS)


def _instance(policy: Callable) -> Any:
    for attribute in ("antigravity_v4_instance", "antigravity_instance"):
        value = getattr(policy, attribute, None)
        if value is not None:
            return value
    raise RuntimeError("benchmark policy does not expose its instance")


def _farm_counts(farm: dict[str, Any]) -> dict[str, int]:
    counts = {
        "q0_crops": 0,
        "q1_crops": 0,
        "q2_crops": 0,
        "q0_animals": 0,
        "q1_animals": 0,
        "q2_animals": 0,
    }
    for y, row in enumerate(farm.get("tiles", []) or []):
        for x, tile in enumerate(row):
            if not isinstance(tile, dict):
                continue
            module = "q0" if x < 5 and y < 5 else "q1" if x >= 5 and y < 5 else "q2" if x < 5 else None
            if module is None:
                continue
            if tile.get("kind") == "PLANT":
                counts[f"{module}_crops"] += 1
            if tile.get("animal"):
                counts[f"{module}_animals"] += 1
    return counts


def run_episode(
    *,
    factory: AgentFactory,
    seed: int,
    seat: int,
    opponent: Callable = inert_policy,
    label: str,
) -> dict[str, Any]:
    policy = factory(
        {
            "run_id": label,
            "episode_id": f"{label}-{seed}-{seat}",
            "seed": seed,
            "opponent_id": getattr(opponent, "__name__", "RECORDED_POLICY"),
            "player_position": seat,
        }
    )
    agents = [policy, opponent] if seat == 0 else [opponent, policy]
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=True,
    )
    env.run(agents)
    terminal = env.steps[-1][seat]
    farm = terminal["observation"]["farms"][seat]
    instance = _instance(policy)
    telemetry = instance.telemetry_snapshot()
    return {
        "label": label,
        "seed": seed,
        "seat": seat,
        "status": terminal.get("status"),
        "final_money": float(farm.get("money", 0.0)),
        "owned_quadrants": len(farm.get("unlocked_quadrants", []) or []),
        "errors": int(instance.error_count),
        "fallbacks": int(instance.fallback_count),
        "last_exception": instance.last_exception,
        "q1_activation_day": telemetry.get("Q1_activation_day"),
        "q2_activation_day": telemetry.get("Q2_activation_day"),
        "q2_full_module_day": telemetry.get("Q2_full_module_day"),
        "q2_first_output_day": telemetry.get("Q2_first_output_day"),
        "milk_units": int(telemetry.get("MILK_units", 0)),
        "wool_units": int(telemetry.get("WOOL_units", 0)),
        "melon_units": int(telemetry.get("MELON_units", 0)),
        "strawberry_units": int(telemetry.get("STRAWBERRY_units", 0)),
        "wheat_sold": int(telemetry.get("WHEAT_sold", 0)),
        "fertilizer_collected": int(telemetry.get("fertilizer_collected", 0)),
        "animal_escapes": int(telemetry.get("ANIMAL_ESCAPE", 0)),
        "move_actions": int(telemetry.get("MOVE_actions", 0)),
        "productive_actions": int(telemetry.get("productive_actions", 0)),
        "pass_actions": int(telemetry.get("PASS_actions", 0)),
        "move_per_productive": telemetry.get("MOVE_PER_PRODUCTIVE_ACTION"),
        **_farm_counts(farm),
    }


def recorded_keiz_policy() -> Callable:
    payload = json.loads(REPLAY_PATH.read_text(encoding="utf-8"))
    steps = payload["steps"]
    actions = {
        int(steps[index][0]["observation"]["step"]): deepcopy(
            steps[index + 1][0].get("action") or SAFE_PASS
        )
        for index in range(len(steps) - 1)
    }

    def policy(observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
        del configuration
        return deepcopy(actions.get(int(observation.get("step", 0)), SAFE_PASS))

    policy.__name__ = "RECORDED_KEIZ_104498819"
    return policy


def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    scores = [float(row["final_money"]) for row in rows]
    return {
        "candidate_version": V4_SPEC_VERSION,
        "episode_count": len(rows),
        "final_money_mean": statistics.fmean(scores),
        "final_money_median": statistics.median(scores),
        "final_money_min": min(scores),
        "final_money_max": max(scores),
        "final_money_std": statistics.pstdev(scores),
        "animal_escapes_total": sum(int(row["animal_escapes"]) for row in rows),
        "errors_total": sum(int(row["errors"]) for row in rows),
        "fallbacks_total": sum(int(row["fallbacks"]) for row in rows),
        "move_per_productive_mean": statistics.fmean(
            float(row["move_per_productive"]) for row in rows
        ),
        "technical_pass": all(
            row["status"] == "DONE"
            and int(row["errors"]) == 0
            and int(row["fallbacks"]) == 0
            for row in rows
        ),
    }


def canonical(include_replay: bool) -> int:
    rows = [
        run_episode(
            factory=lambda ctx: create_v4_agent(run_context=ctx),
            seed=seed,
            seat=seat,
            label="ANTIGRAVITY_V4_CANONICAL",
        )
        for seed in SEEDS
        for seat in (0, 1)
    ]
    replay_row = None
    if include_replay:
        replay_row = run_episode(
            factory=lambda ctx: create_v4_agent(run_context=ctx),
            seed=562040596,
            seat=1,
            opponent=recorded_keiz_policy(),
            label="ANTIGRAVITY_V4_REPLAY_104498819",
        )
    summary = aggregate(rows)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    with RESULT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    RESULT_JSON.write_text(
        json.dumps(
            {
                "protocol": "ANTIGRAVITY_V4_0_CANONICAL_AND_COMPETITIVE_REPLAY",
                "post_hoc_seed_selection": False,
                "rows": rows,
                "aggregate": summary,
                "competitive_replay": replay_row,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"aggregate": summary, "competitive_replay": replay_row}, indent=2))
    return 0 if summary["technical_pass"] else 1


def holdout() -> int:
    rows = [
        run_episode(
            factory=lambda ctx: create_v4_agent(run_context=ctx),
            seed=seed,
            seat=seat,
            label="ANTIGRAVITY_V4_FROZEN_PHASE_B_C",
        )
        for seed in (*SEEDS, *PHASE_C_SEEDS)
        for seat in (0, 1)
    ]
    summary = aggregate(rows)
    with HOLDOUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    HOLDOUT_JSON.write_text(
        json.dumps(
            {
                "protocol": "ANTIGRAVITY_V4_0_FROZEN_PHASE_B_PLUS_PHASE_C",
                "manifest": "ANTIGRAVITY_V4_0_HOLDOUT_MANIFEST.md",
                "post_hoc_seed_selection": False,
                "rows": rows,
                "aggregate": summary,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    return 0 if summary["technical_pass"] else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--holdout", action="store_true")
    parser.add_argument("--no-replay", action="store_true")
    args = parser.parse_args()
    if args.holdout:
        return holdout()
    return canonical(include_replay=not args.no_replay)


if __name__ == "__main__":
    raise SystemExit(main())
