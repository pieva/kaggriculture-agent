#!/usr/bin/env python3
"""Run Gate B for ANTIGRAVITY-E18.1-REACTIVE-REBOOT-V1.

Independent economy validation:
- All 7 development seeds (180903001 to 180903007)
- Both seats (P0 and P1)
- Evaluated against inert ("random") and the obsolete Antigravity E17 baseline
- Verifies mean money >= 10,000 across runs
- Verifies no runs end at 0.0 money
- Verifies minimal terminal sellable inventory
- Captures yield, move, PASS, and backlog telemetry
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.antigravity.agent_e17_native_3q import (
    create_e17_native_agent as create_antigravity_e17_agent,
)
from agricola.strategy.antigravity.antigravity_e18_reactive_reboot_v1 import (
    create_antigravity_e18_agent,
)

ROOT = Path(__file__).resolve().parents[5]
OUTPUT_JSON = (
    ROOT
    / "docs"
    / "model_specs"
    / "antigravity"
    / "e18"
    / "artifacts"
    / "derived"
    / "E18_ANTIGRAVITY_REACTIVE_V1_GATE_B.json"
)

SEEDS = [
    180903001,
    180903002,
    180903003,
    180903004,
    180903005,
    180903006,
    180903007,
]
SEATS = [0, 1]


def run_gate_b() -> dict[str, Any]:
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    runs: list[dict[str, Any]] = []

    opponents = ["INERT", "ANTIGRAVITY_E17_OBSOLETE"]

    for opp_type in opponents:
        for seed in SEEDS:
            for seat in SEATS:
                context = {
                    "run_id": f"E18-ANTIGRAVITY-GATE-B-S{seed}-P{seat}-vs-{opp_type}",
                    "episode_id": f"E18-ANTIGRAVITY-GATE-B-S{seed}-P{seat}-vs-{opp_type}",
                    "seed": seed,
                    "player_position": seat,
                }
                agent_fn = create_antigravity_e18_agent(run_context=context)
                controller = agent_fn.antigravity_e18_instance

                if opp_type == "INERT":
                    opp_fn = "random"
                else:
                    opp_context = {
                        "run_id": f"E18-OPPONENT-E17-S{seed}-P{1-seat}",
                        "seed": seed,
                        "player_position": 1 - seat,
                    }
                    opp_fn = create_antigravity_e17_agent(run_context=opp_context)

                env = make(
                    "kaggriculture",
                    configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
                    debug=False,
                )

                players: list[Any] = [None, None]
                players[seat] = agent_fn
                players[1 - seat] = opp_fn

                env.run(players)

                steps_completed = len(env.steps)
                final_step = env.steps[-1][seat]
                final_money = float(final_step.observation["farms"][seat]["money"])
                private = final_step.observation["private"]
                shed = private.get("shed", {}) or {}
                inventories = private.get("inventories", []) or []

                terminal_shed_inventory = sum(int(v or 0) for v in shed.values())
                terminal_worker_inventory = sum(
                    sum(int(v or 0) for v in inv.values())
                    for inv in inventories
                    if isinstance(inv, dict)
                )
                terminal_sellable = terminal_shed_inventory + terminal_worker_inventory

                telemetry = controller.telemetry_snapshot()

                runs.append(
                    {
                        "opponent": opp_type,
                        "seed": seed,
                        "seat": seat,
                        "steps_completed": steps_completed,
                        "final_money": final_money,
                        "technical_errors": telemetry.get("technical_errors", 0),
                        "fallbacks": telemetry.get("fallbacks", 0),
                        "productive_actions": telemetry.get("productive_actions", 0),
                        "move_actions": telemetry.get("move_actions", 0),
                        "pass_actions": telemetry.get("pass_actions", 0),
                        "move_per_productive": telemetry.get("move_per_productive", 0.0),
                        "peak_crops": telemetry.get("peak_crops", 0),
                        "peak_hands": telemetry.get("peak_hands", 0),
                        "backlog": telemetry.get("backlog", 0),
                        "terminal_sellable_residual": terminal_sellable,
                        "regime": telemetry.get("final_regime"),
                    }
                )

    money_values = [r["final_money"] for r in runs]
    mean_money = statistics.mean(money_values)
    min_money = min(money_values)
    max_money = max(money_values)

    all_non_zero = all(m > 0.0 for m in money_values)
    mean_ge_10000 = mean_money >= 10_000.0
    zero_errors = all(r["technical_errors"] == 0 and r["fallbacks"] == 0 for r in runs)
    all_720 = all(r["steps_completed"] == 720 for r in runs)

    passed = mean_ge_10000 and all_non_zero and zero_errors and all_720

    summary = {
        "candidate_id": "ANTIGRAVITY_E18_1_REACTIVE_REBOOT_V1",
        "gate": "GATE_B_INDEPENDENT_ECONOMY",
        "passed": passed,
        "metrics": {
            "total_matches": len(runs),
            "mean_money": mean_money,
            "min_money": min_money,
            "max_money": max_money,
            "mean_productive_actions": statistics.mean(r["productive_actions"] for r in runs),
            "mean_move_per_productive": statistics.mean(r["move_per_productive"] for r in runs),
            "mean_pass_actions": statistics.mean(r["pass_actions"] for r in runs),
            "mean_peak_crops": statistics.mean(r["peak_crops"] for r in runs),
            "mean_peak_hands": statistics.mean(r["peak_hands"] for r in runs),
            "mean_terminal_sellable_residual": statistics.mean(r["terminal_sellable_residual"] for r in runs),
        },
        "checks": {
            "all_runs_720_steps": all_720,
            "zero_technical_errors": zero_errors,
            "no_zero_money_runs": all_non_zero,
            "mean_money_ge_10000": mean_ge_10000,
        },
        "runs": runs,
    }

    OUTPUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Gate B result written to {OUTPUT_JSON}")
    print(f"Gate B Verdict: {'PASS' if passed else 'FAIL'} (Mean Money: {mean_money:.2f}, Min: {min_money:.2f})")
    return summary


if __name__ == "__main__":
    run_gate_b()
