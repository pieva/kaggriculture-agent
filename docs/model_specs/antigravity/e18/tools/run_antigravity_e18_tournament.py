#!/usr/bin/env python3
"""Run development tournament for ANTIGRAVITY-E18.1-REACTIVE-REBOOT-V1.

Evaluates Antigravity against the three E18.1 peers:
- CODEX_E18_1
- CLAUDE_E18_1
- COPILOT_E18_1

Matrix:
- 7 development seeds (180903001 to 180903007)
- 2 seats (P0 and P1)
- 14 matches per opponent = 42 matches total
"""

from __future__ import annotations

import csv
import hashlib
import json
import statistics
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.antigravity.antigravity_e18_reactive_reboot_v1 import (
    create_antigravity_e18_agent,
)
from agricola.strategy.claude.e18_opponent_reactive_v1 import (
    create_claude_e18_agent_v1,
)
from agricola.strategy.codex.codex_e18_opponent_reactive_topology import (
    create_codex_e18_opponent_reactive_topology,
)
from agricola.strategy.copilot.e18_opponent_reactive_v1 import (
    create_copilot_e18_opponent_reactive_v1,
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
    / "E18_ANTIGRAVITY_REACTIVE_V1_TOURNAMENT.json"
)
OUTPUT_CSV = OUTPUT_JSON.with_suffix(".csv")

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
OPPONENTS = ["CODEX_E18_1", "CLAUDE_E18_1", "COPILOT_E18_1"]


def _peer_factory(name: str, seed: int, seat: int) -> tuple[Any, Any]:
    context = {
        "run_id": f"E18-TOURNAMENT-S{seed}-P{seat}-{name}",
        "episode_id": f"E18-TOURNAMENT-S{seed}-P{seat}-{name}",
        "seed": seed,
        "player_position": seat,
    }
    if name == "CODEX_E18_1":
        p = create_codex_e18_opponent_reactive_topology(run_context=context)
        return p, p.codex_e18_opponent_reactive_instance
    if name == "CLAUDE_E18_1":
        p = create_claude_e18_agent_v1(run_context=context)
        return p, p
    if name == "COPILOT_E18_1":
        p = create_copilot_e18_opponent_reactive_v1(run_context=context)
        return p, p
    raise ValueError(f"Unknown opponent: {name}")


def _action_stream_hash(env: Any, seat: int) -> str:
    stream = [step[seat].action for step in env.steps if step[seat].action]
    canonical = json.dumps(stream, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest().upper()


def run_tournament() -> dict[str, Any]:
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    matches: list[dict[str, Any]] = []

    h2h: dict[str, dict[str, Any]] = {
        opp: {"wins": 0, "losses": 0, "ties": 0, "antigravity_money": [], "opp_money": []}
        for opp in OPPONENTS
    }

    regimes_activated: set[str] = set()

    for opp_name in OPPONENTS:
        for seed in SEEDS:
            for seat in SEATS:
                antigravity_context = {
                    "run_id": f"E18-ANTIGRAVITY-TOURNAMENT-S{seed}-P{seat}-vs-{opp_name}",
                    "episode_id": f"E18-ANTIGRAVITY-TOURNAMENT-S{seed}-P{seat}-vs-{opp_name}",
                    "seed": seed,
                    "player_position": seat,
                }
                ag_policy = create_antigravity_e18_agent(run_context=antigravity_context)
                ag_controller = ag_policy.antigravity_e18_instance

                opp_policy, opp_controller = _peer_factory(opp_name, seed, 1 - seat)

                env = make(
                    "kaggriculture",
                    configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
                    debug=False,
                )

                players: list[Any] = [None, None]
                players[seat] = ag_policy
                players[1 - seat] = opp_policy

                env.run(players)

                ag_final = env.steps[-1][seat]
                opp_final = env.steps[-1][1 - seat]

                ag_money = float(ag_final.observation["farms"][seat]["money"])
                opp_money = float(opp_final.observation["farms"][1 - seat]["money"])

                if ag_money > opp_money:
                    winner = "ANTIGRAVITY_E18_1"
                    h2h[opp_name]["wins"] += 1
                elif opp_money > ag_money:
                    winner = opp_name
                    h2h[opp_name]["losses"] += 1
                else:
                    winner = "TIE"
                    h2h[opp_name]["ties"] += 1

                h2h[opp_name]["antigravity_money"].append(ag_money)
                h2h[opp_name]["opp_money"].append(opp_money)

                ag_telemetry = ag_controller.telemetry_snapshot()
                regime = ag_telemetry.get("final_regime", "UNKNOWN")
                regimes_activated.add(regime)

                ag_stream_hash = _action_stream_hash(env, seat)

                match_record = {
                    "opponent": opp_name,
                    "seed": seed,
                    "antigravity_seat": seat,
                    "antigravity_money": ag_money,
                    "opponent_money": opp_money,
                    "winner": winner,
                    "technical_errors": ag_telemetry.get("technical_errors", 0),
                    "fallbacks": ag_telemetry.get("fallbacks", 0),
                    "regime": regime,
                    "decision_day": ag_telemetry.get("decision_day"),
                    "decision_pressure": ag_telemetry.get("decision_pressure"),
                    "action_stream_hash": ag_stream_hash,
                    "productive_actions": ag_telemetry.get("productive_actions", 0),
                    "move_actions": ag_telemetry.get("move_actions", 0),
                    "pass_actions": ag_telemetry.get("pass_actions", 0),
                    "move_per_productive": ag_telemetry.get("move_per_productive", 0.0),
                    "peak_crops": ag_telemetry.get("peak_crops", 0),
                    "peak_hands": ag_telemetry.get("peak_hands", 0),
                    "actions": ag_telemetry.get("action_counts", {}),
                }
                matches.append(match_record)

    all_ag_money = [m["antigravity_money"] for m in matches]
    total_wins = sum(h2h[opp]["wins"] for opp in OPPONENTS)
    total_losses = sum(h2h[opp]["losses"] for opp in OPPONENTS)
    total_ties = sum(h2h[opp]["ties"] for opp in OPPONENTS)

    mean_money = statistics.mean(all_ag_money)
    min_money = min(all_ag_money)
    max_money = max(all_ag_money)

    # Check divergence: unique action streams across runs
    unique_streams = len({m["action_stream_hash"] for m in matches})
    zero_errors = all(m["technical_errors"] == 0 and m["fallbacks"] == 0 for m in matches)
    no_zero_money = all(m > 0.0 for m in all_ag_money)

    m1_passed = mean_money >= 15_000.0

    summary = {
        "candidate_id": "ANTIGRAVITY_E18_1_REACTIVE_REBOOT_V1",
        "experiment": "E18",
        "date": "2026-09-04",
        "epistemic_role": "DEVELOPMENT_ONLY_NON_QUALIFYING",
        "standings": {
            "record": f"{total_wins}-{total_losses}-{total_ties}",
            "matches_total": len(matches),
            "mean_money": mean_money,
            "min_money": min_money,
            "max_money": max_money,
        },
        "head_to_head": {
            opp: {
                "record": f"{h2h[opp]['wins']}-{h2h[opp]['losses']}-{h2h[opp]['ties']}",
                "antigravity_mean_money": statistics.mean(h2h[opp]["antigravity_money"]),
                "opponent_mean_money": statistics.mean(h2h[opp]["opp_money"]),
                "delta": statistics.mean(h2h[opp]["antigravity_money"]) - statistics.mean(h2h[opp]["opp_money"]),
            }
            for opp in OPPONENTS
        },
        "checks": {
            "zero_technical_errors": zero_errors,
            "zero_zero_money_runs": no_zero_money,
            "multiple_regimes_activated": len(regimes_activated) >= 2,
            "regimes_observed": list(sorted(regimes_activated)),
            "action_stream_divergence": f"{unique_streams}_OF_{len(matches)}",
            "economic_m1_ge_15000": m1_passed,
        },
        "matches": matches,
    }

    OUTPUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # CSV write
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "opponent", "seed", "antigravity_seat", "antigravity_money", "opponent_money",
            "winner", "regime", "productive_actions", "move_per_productive", "peak_crops", "peak_hands"
        ])
        for m in matches:
            writer.writerow([
                m["opponent"], m["seed"], m["antigravity_seat"], m["antigravity_money"], m["opponent_money"],
                m["winner"], m["regime"], m["productive_actions"], f"{m['move_per_productive']:.2f}",
                m["peak_crops"], m["peak_hands"]
            ])

    print(f"Tournament results written to {OUTPUT_JSON} and {OUTPUT_CSV}")
    print(f"Record: {total_wins}-{total_losses}-{total_ties} | Mean Money: {mean_money:.2f}")
    return summary


if __name__ == "__main__":
    run_tournament()
