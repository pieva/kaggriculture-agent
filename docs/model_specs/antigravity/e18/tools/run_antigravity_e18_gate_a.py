#!/usr/bin/env python3
"""Run Gate A for ANTIGRAVITY-E18.1-REACTIVE-REBOOT-V1.

Audit of engine contract:
- 3 development seeds (180903001, 180903002, 180903003)
- Both seats (P0 and P1)
- 720 steps per match
- Verifies zero technical errors/fallbacks
- Verifies observed DIG -> PLANT -> WATER -> HARVEST -> SELL chain
- Verifies productive_actions > 0, peak_crops > 0, money > 2840 at least once
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from kaggle_environments import make

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
    / "E18_ANTIGRAVITY_REACTIVE_V1_GATE_A.json"
)

SEEDS = [180903001, 180903002, 180903003]
SEATS = [0, 1]


def run_gate_a() -> dict[str, Any]:
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    runs: list[dict[str, Any]] = []

    passed_all = True
    chain_observed = True
    money_threshold_met = False

    for seed in SEEDS:
        for seat in SEATS:
            context = {
                "run_id": f"E18-ANTIGRAVITY-GATE-A-S{seed}-P{seat}",
                "episode_id": f"E18-ANTIGRAVITY-GATE-A-S{seed}-P{seat}",
                "seed": seed,
                "player_position": seat,
            }
            agent_fn = create_antigravity_e18_agent(run_context=context)
            controller = agent_fn.antigravity_e18_instance

            env = make(
                "kaggriculture",
                configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
                debug=False,
            )

            players: list[Any] = [None, None]
            players[seat] = agent_fn
            players[1 - seat] = "random"

            env.run(players)

            steps_completed = len(env.steps)  # 720 steps total (step 0 to 719)
            final_step = env.steps[-1][seat]
            final_money = float(final_step.observation["farms"][seat]["money"])
            telemetry = controller.telemetry_snapshot()

            act_counts = telemetry.get("action_counts", {})
            sale_reqs = telemetry.get("sale_requests", {})

            dig_count = act_counts.get("DIG", 0)
            plant_count = act_counts.get("PLANT", 0)
            water_count = act_counts.get("WATER", 0)
            harvest_count = act_counts.get("HARVEST", 0)
            sell_count = sum(sale_reqs.values())

            run_chain = (
                dig_count > 0
                and plant_count > 0
                and water_count > 0
                and harvest_count > 0
                and sell_count > 0
            )
            if not run_chain:
                chain_observed = False

            if final_money > 2840.0:
                money_threshold_met = True

            run_pass = (
                steps_completed == 720
                and telemetry.get("technical_errors", 0) == 0
                and telemetry.get("fallbacks", 0) == 0
                and telemetry.get("productive_actions", 0) > 0
                and telemetry.get("peak_crops", 0) > 0
                and run_chain
            )

            if not run_pass:
                passed_all = False

            runs.append(
                {
                    "seed": seed,
                    "seat": seat,
                    "steps_completed": steps_completed,
                    "final_money": final_money,
                    "technical_errors": telemetry.get("technical_errors", 0),
                    "fallbacks": telemetry.get("fallbacks", 0),
                    "productive_actions": telemetry.get("productive_actions", 0),
                    "peak_crops": telemetry.get("peak_crops", 0),
                    "peak_hands": telemetry.get("peak_hands", 0),
                    "actions": {
                        "DIG": dig_count,
                        "PLANT": plant_count,
                        "WATER": water_count,
                        "HARVEST": harvest_count,
                        "DROP": act_counts.get("DROP", 0),
                        "SELL_UNITS": sell_count,
                    },
                    "chain_complete": run_chain,
                    "gate_pass": run_pass,
                }
            )

    gate_verdict = passed_all and money_threshold_met

    result = {
        "candidate_id": "ANTIGRAVITY_E18_1_REACTIVE_REBOOT_V1",
        "gate": "GATE_A_ENGINE_CONTRACT_AUDIT",
        "passed": gate_verdict,
        "checks": {
            "all_runs_720_steps": all(r["steps_completed"] == 720 for r in runs),
            "zero_errors": all(r["technical_errors"] == 0 for r in runs),
            "zero_fallbacks": all(r["fallbacks"] == 0 for r in runs),
            "chain_observed_all_runs": chain_observed,
            "productive_actions_positive": all(r["productive_actions"] > 0 for r in runs),
            "peak_crops_positive": all(r["peak_crops"] > 0 for r in runs),
            "money_gt_2840_at_least_once": money_threshold_met,
        },
        "runs": runs,
    }

    OUTPUT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Gate A result written to {OUTPUT_JSON}")
    print(f"Gate A Verdict: {'PASS' if gate_verdict else 'FAIL'}")
    return result


if __name__ == "__main__":
    run_gate_a()
