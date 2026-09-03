#!/usr/bin/env python3
"""Run the E17 development tournament for the two post-tournament candidates.

The matrix contains each new candidate, its direct predecessor, every pair,
all seven development seeds and mirrored seats. Reserved seeds are rejected.
"""

from __future__ import annotations

import csv
import hashlib
import json
import statistics
from itertools import combinations
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.claude.e17_reactive_3q_v3 import (
    DEFAULT_CONFIG_PATH as CLAUDE_V3_CONFIG,
)
from agricola.strategy.claude.e17_reactive_3q_v3 import (
    create_claude_e17_agent_v3,
)
from agricola.strategy.claude.e17_reactive_3q_v5 import (
    DEFAULT_CONFIG_PATH as CLAUDE_V5_CONFIG,
)
from agricola.strategy.claude.e17_reactive_3q_v5 import (
    create_claude_e17_agent_v5,
)
from agricola.strategy.codex.codex_e17_topology_cap_662 import (
    DEFAULT_TOPOLOGY_662_CONFIG_PATH as CODEX_V2_CONFIG,
)
from agricola.strategy.codex.codex_e17_topology_cap_662 import (
    create_codex_e17_topology_cap_662,
)
from agricola.strategy.copilot.e17_topology_662_candidates import (
    create_codex_e17_topology_cap_662_v3,
)
from experiments.e17.tools.common import (
    run_e17_three_agent_development_tournament_v2 as base,
)

ROOT = Path(__file__).resolve().parents[4]
MANIFEST = ROOT / "experiments/e17/manifest/E17_COMMON_MANIFEST_V1.json"
CODEX_V3_CONFIG = (
    ROOT / "experiments/e17/configs/codex/CODEX_E17_3_TOPOLOGY_CAP_662_V3.json"
)
OUTPUT_JSON = (
    ROOT
    / "experiments/e17/artifacts/derived/common/"
    / "E17_TWO_CANDIDATE_DELTA_TOURNAMENT_V3.json"
)
OUTPUT_CSV = OUTPUT_JSON.with_suffix(".csv")
TARGET_MONEY = 100_000.0

PARTICIPANTS = (
    "CLAUDE_V5",
    "CLAUDE_V3_CONTROL",
    "COPILOT_662_V3",
    "CODEX_662_V2_CONTROL",
)
PAIRS = tuple(combinations(PARTICIPANTS, 2))
CANDIDATE_PREDECESSORS = {
    "CLAUDE_V5": "CLAUDE_V3_CONTROL",
    "COPILOT_662_V3": "CODEX_662_V2_CONTROL",
}
SOURCES = {
    "CLAUDE_V5": ROOT / "src/agricola/strategy/claude/e17_reactive_3q_v5.py",
    "CLAUDE_V3_CONTROL": ROOT
    / "src/agricola/strategy/claude/e17_reactive_3q_v3.py",
    "COPILOT_662_V3": ROOT
    / "src/agricola/strategy/codex/codex_e17_topology_cap_662.py",
    "CODEX_662_V2_CONTROL": ROOT
    / "src/agricola/strategy/codex/codex_e17_topology_cap_662.py",
}
CONFIGS = {
    "CLAUDE_V5": Path(CLAUDE_V5_CONFIG),
    "CLAUDE_V3_CONTROL": Path(CLAUDE_V3_CONFIG),
    "COPILOT_662_V3": CODEX_V3_CONFIG,
    "CODEX_662_V2_CONTROL": Path(CODEX_V2_CONFIG),
}
DELTA_METRICS = (
    "money",
    "peak_hands",
    "peak_crops",
    "peak_animals",
    "peak_weeds",
    "animal_escapes",
    "final_crops",
    "final_animals",
    "final_empty_livestock_tiles",
    "move_actions",
    "productive_actions",
    "pass_actions",
    "move_per_productive",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _factory(name: str, seed: int, seat: int) -> tuple[Any, Any]:
    context = {
        "run_id": f"E17-DELTA-V3-S{seed}-P{seat}-{name}",
        "episode_id": f"E17-DELTA-V3-S{seed}-P{seat}-{name}",
        "seed": seed,
        "player_position": seat,
    }
    if name == "CLAUDE_V5":
        policy = create_claude_e17_agent_v5(
            run_context=context, config_path=CLAUDE_V5_CONFIG
        )
        return policy, policy
    if name == "CLAUDE_V3_CONTROL":
        policy = create_claude_e17_agent_v3(
            run_context=context, config_path=CLAUDE_V3_CONFIG
        )
        return policy, policy
    if name == "COPILOT_662_V3":
        policy = create_codex_e17_topology_cap_662_v3(
            run_context=context, config_path=CODEX_V3_CONFIG
        )
        return policy, policy.codex_e17_topology_662_v3_instance
    if name == "CODEX_662_V2_CONTROL":
        policy = create_codex_e17_topology_cap_662(
            run_context=context, config_path=CODEX_V2_CONFIG
        )
        return policy, policy.codex_e17_topology_662_instance
    raise ValueError(name)


def _run_match(seed: int, p0: str, p1: str) -> dict[str, Any]:
    policy0, controller0 = _factory(p0, seed, 0)
    policy1, controller1 = _factory(p1, seed, 1)
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=False,
    )
    env.run([policy0, policy1])
    diagnostic0 = "CODEX_662" if "662" in p0 else p0
    diagnostic1 = "CODEX_662" if "662" in p1 else p1
    metrics0 = base._seat_metrics(env, 0, diagnostic0, controller0)
    metrics1 = base._seat_metrics(env, 1, diagnostic1, controller1)
    if metrics0["money"] > metrics1["money"]:
        winner = p0
    elif metrics1["money"] > metrics0["money"]:
        winner = p1
    else:
        winner = "TIE"
    return {
        "seed": seed,
        "p0": p0,
        "p1": p1,
        "winner": winner,
        "margin_p0": metrics0["money"] - metrics1["money"],
        "p0_metrics": metrics0,
        "p1_metrics": metrics1,
    }


def _records(matches: list[dict[str, Any]], participant: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for match in matches:
        for seat in (0, 1):
            if match[f"p{seat}"] != participant:
                continue
            records.append(
                {
                    "seed": match["seed"],
                    "seat": seat,
                    "opponent": match[f"p{1 - seat}"],
                    "winner": match["winner"],
                    "metrics": match[f"p{seat}_metrics"],
                }
            )
    return records


def _mean(records: list[dict[str, Any]], key: str) -> float | None:
    values = [
        float(record["metrics"][key])
        for record in records
        if record["metrics"].get(key) is not None
    ]
    return statistics.mean(values) if values else None


def _aggregate(matches: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    standings: dict[str, dict[str, Any]] = {}
    for participant in PARTICIPANTS:
        records = _records(matches, participant)
        money = [float(record["metrics"]["money"]) for record in records]
        seat_money = {
            seat: [
                float(record["metrics"]["money"])
                for record in records
                if record["seat"] == seat
            ]
            for seat in (0, 1)
        }
        wins = sum(record["winner"] == participant for record in records)
        ties = sum(record["winner"] == "TIE" for record in records)
        standings[participant] = {
            "matches": len(records),
            "wins": wins,
            "losses": len(records) - wins - ties,
            "ties": ties,
            "money_mean": statistics.mean(money),
            "money_median": statistics.median(money),
            "money_min": min(money),
            "money_max": max(money),
            "money_stdev": statistics.pstdev(money),
            "seat0_money_mean": statistics.mean(seat_money[0]),
            "seat1_money_mean": statistics.mean(seat_money[1]),
            "seat_delta": statistics.mean(seat_money[0])
            - statistics.mean(seat_money[1]),
            "q1_activation_day_mean": _mean(records, "q1_activation_day"),
            "q2_activation_day_mean": _mean(records, "q2_activation_day"),
            "three_quadrant_runs": sum(
                record["metrics"]["final_quadrants"] >= 3 for record in records
            ),
            "peak_hands_mean": _mean(records, "peak_hands"),
            "peak_crops_mean": _mean(records, "peak_crops"),
            "peak_animals_mean": _mean(records, "peak_animals"),
            "peak_weeds_mean": _mean(records, "peak_weeds"),
            "animal_escapes": sum(
                int(record["metrics"]["animal_escapes"]) for record in records
            ),
            "technical_errors": sum(
                int(record["metrics"]["technical_errors"]) for record in records
            ),
            "fallbacks": sum(
                int(record["metrics"]["fallbacks"]) for record in records
            ),
            "final_crops_mean": _mean(records, "final_crops"),
            "final_animals_mean": _mean(records, "final_animals"),
            "final_empty_livestock_tiles_mean": _mean(
                records, "final_empty_livestock_tiles"
            ),
            "move_actions_mean": _mean(records, "move_actions"),
            "productive_actions_mean": _mean(records, "productive_actions"),
            "pass_actions_mean": _mean(records, "pass_actions"),
            "move_per_productive_mean": _mean(records, "move_per_productive"),
            "target_pastures_built_mean": _mean(records, "target_pastures_built"),
            "target_pastures_filled_mean": _mean(records, "target_pastures_filled"),
            "empty_target_pastures_mean": _mean(records, "empty_target_pastures"),
            "max_reclaimed_crops_mean": _mean(records, "max_reclaimed_crops"),
            "max_q2_pastures_mean": _mean(records, "max_q2_pastures"),
            "topology_cap_breaches": sum(
                int(record["metrics"].get("topology_cap_breaches", 0))
                for record in records
            ),
        }
    return standings


def _head_to_head(matches: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for left, right in PAIRS:
        rows = [
            match
            for match in matches
            if {match["p0"], match["p1"]} == {left, right}
        ]
        left_money: list[float] = []
        right_money: list[float] = []
        margins: list[float] = []
        for match in rows:
            left_seat = 0 if match["p0"] == left else 1
            left_value = float(match[f"p{left_seat}_metrics"]["money"])
            right_value = float(match[f"p{1 - left_seat}_metrics"]["money"])
            left_money.append(left_value)
            right_money.append(right_value)
            margins.append(left_value - right_value)
        result[f"{left}_vs_{right}"] = {
            "matches": len(rows),
            f"{left}_wins": sum(match["winner"] == left for match in rows),
            f"{right}_wins": sum(match["winner"] == right for match in rows),
            "ties": sum(match["winner"] == "TIE" for match in rows),
            f"{left}_money_mean": statistics.mean(left_money),
            f"{right}_money_mean": statistics.mean(right_money),
            f"{left}_mean_money_delta": statistics.mean(margins),
        }
    return result


def _metric_delta(
    candidate_records: list[dict[str, Any]],
    predecessor_records: list[dict[str, Any]],
    metric: str,
) -> dict[str, float | None]:
    candidate = _mean(candidate_records, metric)
    predecessor = _mean(predecessor_records, metric)
    if candidate is None or predecessor is None:
        return {"candidate": candidate, "predecessor": predecessor, "delta": None, "delta_pct": None}
    delta = candidate - predecessor
    return {
        "candidate": candidate,
        "predecessor": predecessor,
        "delta": delta,
        "delta_pct": 100.0 * delta / predecessor if predecessor else None,
    }


def _candidate_deltas(matches: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    all_participants = set(PARTICIPANTS)
    for candidate, predecessor in CANDIDATE_PREDECESSORS.items():
        shared_opponents = sorted(all_participants - {candidate, predecessor})
        candidate_all = _records(matches, candidate)
        predecessor_all = _records(matches, predecessor)
        candidate_shared = [
            record for record in candidate_all if record["opponent"] in shared_opponents
        ]
        predecessor_shared = [
            record
            for record in predecessor_all
            if record["opponent"] in shared_opponents
        ]
        candidate_direct = [
            record for record in candidate_all if record["opponent"] == predecessor
        ]
        predecessor_direct = [
            record for record in predecessor_all if record["opponent"] == candidate
        ]
        shared_money = _mean(candidate_shared, "money") or 0.0
        result[candidate] = {
            "predecessor": predecessor,
            "shared_opponents": shared_opponents,
            "shared_opponent_samples_per_agent": len(candidate_shared),
            "direct_samples_per_agent": len(candidate_direct),
            "shared_opponent_metrics": {
                metric: _metric_delta(candidate_shared, predecessor_shared, metric)
                for metric in DELTA_METRICS
            },
            "direct_head_to_head_money": _metric_delta(
                candidate_direct, predecessor_direct, "money"
            ),
            "direct_wins": sum(
                record["winner"] == candidate for record in candidate_direct
            ),
            "direct_losses": sum(
                record["winner"] == predecessor for record in candidate_direct
            ),
            "direct_ties": sum(
                record["winner"] == "TIE" for record in candidate_direct
            ),
            "target_money": TARGET_MONEY,
            "target_attainment_pct": 100.0 * shared_money / TARGET_MONEY,
            "target_gap": TARGET_MONEY - shared_money,
            "multiplier_to_target": TARGET_MONEY / shared_money if shared_money else None,
        }
    return result


def _write_csv(matches: list[dict[str, Any]]) -> None:
    fields = [
        "seed",
        "seat",
        "participant",
        "opponent",
        "winner",
        "money",
        "q1_activation_day",
        "q2_activation_day",
        "final_quadrants",
        "peak_hands",
        "peak_crops",
        "peak_animals",
        "peak_weeds",
        "animal_escapes",
        "final_crops",
        "final_animals",
        "final_empty_livestock_tiles",
        "move_actions",
        "productive_actions",
        "pass_actions",
        "move_per_productive",
        "technical_errors",
        "fallbacks",
    ]
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
                        **{field: metrics.get(field) for field in fields[5:]},
                    }
                )


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    seeds = [int(value) for value in manifest["seed_policy"]["development"]]
    reserved = {
        *manifest["seed_policy"]["holdout"]["seeds"],
        *manifest["seed_policy"]["final_confirmation"]["seeds"],
    }
    if set(seeds).intersection(reserved):
        raise RuntimeError("development matrix overlaps a reserved seed")
    provenance = {
        name: {
            "source": str(SOURCES[name].relative_to(ROOT)).replace("\\", "/"),
            "source_sha256": _sha256(SOURCES[name]),
            "config": str(CONFIGS[name].relative_to(ROOT)).replace("\\", "/"),
            "config_sha256": _sha256(CONFIGS[name]),
        }
        for name in PARTICIPANTS
    }
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
    payload = {
        "schema_version": "E17_TWO_CANDIDATE_DELTA_TOURNAMENT_V3",
        "epistemic_role": "DEVELOPMENT_ONLY_NON_QUALIFYING",
        "date": "2026-09-03",
        "target_money": TARGET_MONEY,
        "participants": list(PARTICIPANTS),
        "candidate_predecessors": CANDIDATE_PREDECESSORS,
        "seeds": seeds,
        "seats": [0, 1],
        "match_count": len(matches),
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "provenance": provenance,
        "standings": _aggregate(matches),
        "head_to_head": _head_to_head(matches),
        "candidate_deltas": _candidate_deltas(matches),
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
