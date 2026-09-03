#!/usr/bin/env python3
"""Run the E17.3 Codex/Claude/Copilot development tournament."""

from __future__ import annotations

import csv
import hashlib
import json
import statistics
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.claude.e17_reactive_3q_v3 import (
    DEFAULT_CONFIG_PATH as CLAUDE_CONFIG,
)
from agricola.strategy.claude.e17_reactive_3q_v3 import (
    create_claude_e17_agent_v3,
)
from agricola.strategy.codex.codex_e17_topology_cap_662 import (
    DEFAULT_TOPOLOGY_662_CONFIG_PATH as CODEX_CONFIG,
)
from agricola.strategy.codex.codex_e17_topology_cap_662 import (
    create_codex_e17_topology_cap_662,
)
from agricola.strategy.copilot.e17_native_3q import (
    DEFAULT_CONFIG_PATH as COPILOT_CONFIG,
)
from agricola.strategy.copilot.e17_native_3q import create_native_agent

ROOT = Path(__file__).resolve().parents[4]
MANIFEST = ROOT / "experiments/e17/manifest/E17_COMMON_MANIFEST_V1.json"
OUTPUT_JSON = (
    ROOT
    / "experiments/e17/artifacts/derived/common/"
    / "E17_THREE_AGENT_DEVELOPMENT_TOURNAMENT_V2.json"
)
OUTPUT_CSV = OUTPUT_JSON.with_suffix(".csv")
PARTICIPANTS = ("CODEX_662", "CLAUDE_V3", "COPILOT_NATIVE")
PAIRS = (
    ("CODEX_662", "CLAUDE_V3"),
    ("CODEX_662", "COPILOT_NATIVE"),
    ("CLAUDE_V3", "COPILOT_NATIVE"),
)
SOURCES = {
    "CODEX_662": ROOT
    / "src/agricola/strategy/codex/codex_e17_topology_cap_662.py",
    "CLAUDE_V3": ROOT / "src/agricola/strategy/claude/e17_reactive_3q_v3.py",
    "COPILOT_NATIVE": ROOT / "src/agricola/strategy/copilot/e17_native_3q.py",
}
CONFIGS = {
    "CODEX_662": CODEX_CONFIG,
    "CLAUDE_V3": CLAUDE_CONFIG,
    "COPILOT_NATIVE": COPILOT_CONFIG,
}
MOVES = frozenset({"NORTH", "SOUTH", "EAST", "WEST"})
PRODUCTIVE = frozenset(
    {
        "PLANT",
        "WATER",
        "HARVEST",
        "DIG",
        "BUILD_PASTURE",
        "BUILD_COOP",
        "FEED",
        "CARE",
        "COLLECT_FERTILIZER",
        "FERTILIZE",
    }
)
QUADRANTS = {
    "Q0_NW": (range(5), range(5)),
    "Q1_NE": (range(5, 10), range(5)),
    "Q2_SW": (range(5), range(5, 10)),
    "Q3_SE": (range(5, 10), range(5, 10)),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _farm(state: list[Any], seat: int) -> dict[str, Any]:
    observation = state[seat].get("observation", {}) or {}
    farms = observation.get("farms", []) or []
    return farms[seat] if seat < len(farms) else {}


def _tile_counts(farm: dict[str, Any]) -> Counter[str]:
    result: Counter[str] = Counter()
    for row in farm.get("tiles", []) or []:
        for tile in row:
            if not isinstance(tile, dict):
                result["EMPTY"] += 1
                continue
            kind = str(tile.get("kind") or "OTHER")
            if tile.get("animal"):
                result["ANIMAL"] += 1
                result[f"ANIMAL:{tile['animal']}"] += 1
            elif kind == "PLANT":
                result["CROP"] += 1
                result[f"CROP:{tile.get('crop') or 'UNKNOWN'}"] += 1
            elif kind in {"PASTURE", "COOP"}:
                result["EMPTY_LIVESTOCK"] += 1
                result[f"EMPTY_{kind}"] += 1
            elif kind == "WEED":
                result["WEED"] += 1
            else:
                result["OTHER"] += 1
    return result


def _quadrant_profile(farm: dict[str, Any]) -> dict[str, dict[str, int]]:
    tiles = farm.get("tiles", []) or []
    result: dict[str, dict[str, int]] = {}
    for name, (xs, ys) in QUADRANTS.items():
        counts: Counter[str] = Counter()
        for y in ys:
            for x in xs:
                tile = tiles[y][x] if y < len(tiles) and x < len(tiles[y]) else None
                if not isinstance(tile, dict):
                    counts["EMPTY"] += 1
                elif tile.get("animal"):
                    counts["ANIMAL"] += 1
                elif tile.get("kind") == "PLANT":
                    counts["CROP"] += 1
                elif tile.get("kind") in {"PASTURE", "COOP"}:
                    counts["EMPTY_LIVESTOCK"] += 1
                elif tile.get("kind") == "WEED":
                    counts["WEED"] += 1
                else:
                    counts["OTHER"] += 1
        result[name] = dict(sorted(counts.items()))
    return result


def _factory(name: str, seed: int, seat: int) -> tuple[Callable[..., Any], Any]:
    context = {
        "run_id": f"E17-3AGENT-V2-S{seed}-P{seat}-{name}",
        "episode_id": f"E17-3AGENT-V2-S{seed}-P{seat}-{name}",
        "seed": seed,
        "player_position": seat,
    }
    if name == "CODEX_662":
        policy = create_codex_e17_topology_cap_662(run_context=context)
        return policy, policy.codex_e17_topology_662_instance
    if name == "CLAUDE_V3":
        policy = create_claude_e17_agent_v3(run_context=context)
        return policy, policy
    if name == "COPILOT_NATIVE":
        policy = create_native_agent()
        return policy, policy
    raise ValueError(name)


def _controller_diagnostics(name: str, controller: Any) -> dict[str, Any]:
    if name == "CODEX_662":
        telemetry = controller.telemetry_snapshot()
        return {
            "technical_errors": int(controller.error_count),
            "fallbacks": int(controller.fallback_count),
            "target_pastures_built": telemetry["latest_target_pastures_built"],
            "target_pastures_filled": telemetry["latest_target_pastures_filled"],
            "empty_target_pastures": telemetry["latest_empty_target_pastures"],
            "max_reclaimed_crops": telemetry["max_active_reclaimed_crops"],
            "max_q2_pastures": telemetry["max_observed_q2_pastures"],
            "topology_cap_breaches": telemetry["topology_cap_breaches"],
        }
    return {
        "technical_errors": int(getattr(controller, "technical_errors", 0)),
        "fallbacks": int(getattr(controller, "fallback_count", 0)),
    }


def _seat_metrics(
    env: Any,
    seat: int,
    name: str,
    controller: Any,
) -> dict[str, Any]:
    action_counts: Counter[str] = Counter()
    q1_day = None
    q2_day = None
    peak_hands = peak_crops = peak_animals = peak_weeds = 0
    animal_escapes = 0
    previous_day = None
    previous_animals = 0
    for state in env.steps:
        record = state[seat]
        observation = record.get("observation", {}) or {}
        farm = _farm(state, seat)
        counts = _tile_counts(farm)
        day = int(observation.get("day", 0))
        quadrants = len(farm.get("unlocked_quadrants", []) or [])
        if previous_day is not None and day > previous_day:
            animal_escapes += max(0, previous_animals - counts["ANIMAL"])
        previous_day = day
        previous_animals = counts["ANIMAL"]
        if quadrants >= 2 and q1_day is None:
            q1_day = day
        if quadrants >= 3 and q2_day is None:
            q2_day = day
        peak_hands = max(peak_hands, len(farm.get("hands", []) or []))
        peak_crops = max(peak_crops, counts["CROP"])
        peak_animals = max(peak_animals, counts["ANIMAL"])
        peak_weeds = max(peak_weeds, counts["WEED"])
        action = record.get("action", {}) or {}
        commands = [action.get("farmer", ["PASS"]), *(action.get("hands", []) or [])]
        for command in commands:
            if command:
                action_counts[str(command[0])] += 1
    terminal = env.steps[-1][seat]
    farm = _farm(env.steps[-1], seat)
    counts = _tile_counts(farm)
    productive = sum(action_counts[command] for command in PRODUCTIVE)
    moves = sum(action_counts[command] for command in MOVES)
    return {
        "status": str(terminal.get("status", "UNKNOWN")),
        "reward": float(terminal.get("reward") or 0.0),
        "money": float(farm.get("money", 0.0) or 0.0),
        "q1_activation_day": q1_day,
        "q2_activation_day": q2_day,
        "final_quadrants": len(farm.get("unlocked_quadrants", []) or []),
        "peak_hands": peak_hands,
        "peak_crops": peak_crops,
        "peak_animals": peak_animals,
        "peak_weeds": peak_weeds,
        "animal_escapes": animal_escapes,
        "final_crops": counts["CROP"],
        "final_animals": counts["ANIMAL"],
        "final_empty_livestock_tiles": counts["EMPTY_LIVESTOCK"],
        "final_weeds": counts["WEED"],
        "quadrant_profile": _quadrant_profile(farm),
        "move_actions": moves,
        "productive_actions": productive,
        "pass_actions": action_counts["PASS"],
        "move_per_productive": moves / productive if productive else None,
        "action_counts": dict(sorted(action_counts.items())),
        **_controller_diagnostics(name, controller),
    }


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


def _participant_rows(
    matches: list[dict[str, Any]], participant: str
) -> list[tuple[int, dict[str, Any], str]]:
    rows = []
    for match in matches:
        if match["p0"] == participant:
            rows.append((0, match["p0_metrics"], match["winner"]))
        elif match["p1"] == participant:
            rows.append((1, match["p1_metrics"], match["winner"]))
    return rows


def _mean_present(rows: list[dict[str, Any]], key: str) -> float | None:
    values = [float(row[key]) for row in rows if row.get(key) is not None]
    return statistics.mean(values) if values else None


def _aggregate(matches: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    standings: dict[str, dict[str, Any]] = {}
    for participant in PARTICIPANTS:
        records = _participant_rows(matches, participant)
        rows = [record[1] for record in records]
        money = [float(row["money"]) for row in rows]
        seat_money = {
            str(seat): [float(row["money"]) for row_seat, row, _ in records if row_seat == seat]
            for seat in (0, 1)
        }
        wins = sum(winner == participant for _, _, winner in records)
        ties = sum(winner == "TIE" for _, _, winner in records)
        diagnostics = {
            key: _mean_present(rows, key)
            for key in (
                "target_pastures_built",
                "target_pastures_filled",
                "empty_target_pastures",
                "max_reclaimed_crops",
                "max_q2_pastures",
                "topology_cap_breaches",
            )
            if any(key in row for row in rows)
        }
        standings[participant] = {
            "matches": len(rows),
            "wins": wins,
            "losses": len(rows) - wins - ties,
            "ties": ties,
            "money_mean": statistics.mean(money),
            "money_median": statistics.median(money),
            "money_min": min(money),
            "money_max": max(money),
            "money_stdev": statistics.pstdev(money),
            "seat0_money_mean": statistics.mean(seat_money["0"]),
            "seat1_money_mean": statistics.mean(seat_money["1"]),
            "seat_delta": statistics.mean(seat_money["0"])
            - statistics.mean(seat_money["1"]),
            "q1_activation_day_mean": _mean_present(rows, "q1_activation_day"),
            "q2_activation_day_mean": _mean_present(rows, "q2_activation_day"),
            "three_quadrant_runs": sum(row["final_quadrants"] >= 3 for row in rows),
            "peak_hands_mean": _mean_present(rows, "peak_hands"),
            "peak_crops_mean": _mean_present(rows, "peak_crops"),
            "peak_animals_mean": _mean_present(rows, "peak_animals"),
            "peak_weeds_mean": _mean_present(rows, "peak_weeds"),
            "animal_escapes": sum(int(row["animal_escapes"]) for row in rows),
            "technical_errors": sum(int(row["technical_errors"]) for row in rows),
            "fallbacks": sum(int(row["fallbacks"]) for row in rows),
            "final_crops_mean": _mean_present(rows, "final_crops"),
            "final_animals_mean": _mean_present(rows, "final_animals"),
            "final_empty_livestock_tiles_mean": _mean_present(
                rows, "final_empty_livestock_tiles"
            ),
            "move_actions_mean": _mean_present(rows, "move_actions"),
            "productive_actions_mean": _mean_present(rows, "productive_actions"),
            "pass_actions_mean": _mean_present(rows, "pass_actions"),
            "move_per_productive_mean": _mean_present(rows, "move_per_productive"),
            **diagnostics,
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
        margins = []
        for match in rows:
            if match["p0"] == left:
                margins.append(float(match["margin_p0"]))
            else:
                margins.append(-float(match["margin_p0"]))
        result[f"{left}_vs_{right}"] = {
            "matches": len(rows),
            f"{left}_wins": sum(match["winner"] == left for match in rows),
            f"{right}_wins": sum(match["winner"] == right for match in rows),
            "ties": sum(match["winner"] == "TIE" for match in rows),
            f"{left}_mean_money_delta": statistics.mean(margins),
            f"{left}_min_money_delta": min(margins),
            f"{left}_max_money_delta": max(margins),
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
        "animal_escapes",
        "move_actions",
        "productive_actions",
        "move_per_productive",
        "technical_errors",
        "fallbacks",
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for match in matches:
            for seat in (0, 1):
                participant = match[f"p{seat}"]
                metrics = match[f"p{seat}_metrics"]
                writer.writerow(
                    {
                        "seed": match["seed"],
                        "seat": seat,
                        "participant": participant,
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
            "config": str(Path(CONFIGS[name]).relative_to(ROOT)).replace("\\", "/"),
            "config_sha256": _sha256(Path(CONFIGS[name])),
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
        "schema_version": "E17_THREE_AGENT_DEVELOPMENT_TOURNAMENT_V2",
        "epistemic_role": "DEVELOPMENT_ONLY_NON_QUALIFYING",
        "date": "2026-09-03",
        "participants": list(PARTICIPANTS),
        "excluded_participants": {"ANTIGRAVITY": "OWNER_UNAVAILABLE_UNTIL_2026-09-04"},
        "seeds": seeds,
        "seats": [0, 1],
        "match_count": len(matches),
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "provenance": provenance,
        "standings": _aggregate(matches),
        "head_to_head": _head_to_head(matches),
        "matches": matches,
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_csv(matches)
    print(f"wrote {OUTPUT_JSON}")
    print(f"wrote {OUTPUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
