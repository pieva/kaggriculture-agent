from __future__ import annotations

import csv
import itertools
import json
import statistics
from collections.abc import Callable
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.copilot.e18_economic_recovery_v5 import (
    create_copilot_e18_economic_recovery_v5,
)
from agricola.strategy.copilot.e18_step_driven_v1 import (
    create_copilot_e18_step_driven_v1,
)

ROOT = Path(__file__).resolve().parents[5]
OUT_JSON = ROOT / "docs/model_specs/copilot/e18/artifacts/derived/E18_COPILOT_STATE_VS_STEP_TOURNAMENT.json"
OUT_CSV = ROOT / "docs/model_specs/copilot/e18/artifacts/derived/E18_COPILOT_STATE_VS_STEP_TOURNAMENT.csv"

PARTICIPANTS = ("COPILOT_E18_8_STATE_DRIVEN_V5", "COPILOT_E18_9_STEP_DRIVEN_V1")
PAIRS = tuple(itertools.combinations(PARTICIPANTS, 2))


def _factory(name: str, seed: int, seat: int) -> tuple[Callable[..., Any], Any]:
    context = {"run_id": f"COPILOT-STATE-VS-STEP-S{seed}-P{seat}-{name}", "episode_id": f"COPILOT-STATE-VS-STEP-S{seed}-P{seat}-{name}", "seed": seed, "player_position": seat}
    if name == "COPILOT_E18_8_STATE_DRIVEN_V5":
        policy = create_copilot_e18_economic_recovery_v5(run_context=context)
        return policy, policy
    if name == "COPILOT_E18_9_STEP_DRIVEN_V1":
        policy = create_copilot_e18_step_driven_v1(run_context=context)
        return policy, policy
    raise ValueError(f"unknown participant: {name}")


def _seat_money(env: Any, seat: int) -> float:
    final = env.steps[-1]
    return float(final[seat]["observation"]["farms"][seat]["money"])


def _run_match(seed: int, p0: str, p1: str) -> dict[str, Any]:
    policy0, _ = _factory(p0, seed, 0)
    policy1, _ = _factory(p1, seed, 1)
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24}, debug=False)
    env.run([policy0, policy1])
    money0 = _seat_money(env, 0)
    money1 = _seat_money(env, 1)
    winner = p0 if money0 > money1 else p1 if money1 > money0 else "TIE"
    return {
        "seed": seed,
        "p0": p0,
        "p1": p1,
        "winner": winner,
        "money_p0": money0,
        "money_p1": money1,
        "margin_p0": money0 - money1,
    }


def _aggregate(matches: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    summary: dict[str, dict[str, Any]] = {}
    for participant in PARTICIPANTS:
        rows = []
        for match in matches:
            for seat, label in ((0, "p0"), (1, "p1")):
                if match[label] == participant:
                    rows.append({
                        "seed": match["seed"],
                        "money": match[f"money_{label}"],
                        "won": match["winner"] == participant,
                    })
        money = [float(row["money"]) for row in rows]
        wins = sum(1 for row in rows if row["won"])
        losses = len(rows) - wins
        summary[participant] = {
            "matches": len(rows),
            "wins": wins,
            "losses": losses,
            "money_mean": statistics.mean(money),
            "money_min": min(money),
            "money_max": max(money),
            "money_stdev": statistics.pstdev(money),
        }
    return summary


def main() -> None:
    matches = []
    seeds = tuple(range(180903001, 180903008))
    for seed in seeds:
        for left, right in PAIRS:
            matches.append(_run_match(seed, left, right))
    summary = _aggregate(matches)
    payload = {
        "date": "2026-09-09",
        "seed_range": [min(seeds), max(seeds)],
        "participants": PARTICIPANTS,
        "summary": summary,
        "matches": matches,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["seed", "p0", "p1", "winner", "money_p0", "money_p1", "margin_p0"])
        writer.writeheader()
        for match in matches:
            writer.writerow(match)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
