"""Forensic lifecycle analysis for Kaggle episode 105080066.

The raw replay is immutable training evidence.  This script derives a compact
JSON summary and two CSV ledgers without importing or executing either policy.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
RAW = ROOT / "data" / "replays" / "json" / "105080066.json"
OUT = ROOT / "experiments" / "e18" / "artifacts" / "discovery"
SUMMARY = OUT / "E18_EPISODE_105080066_LIFECYCLE_ANALYSIS_V1.json"
DAILY = OUT / "E18_EPISODE_105080066_DAILY_TIMELINE_V1.csv"
ACTIONS = OUT / "E18_EPISODE_105080066_ACTIONS_BY_DAY_V1.csv"

EXPECTED_EPISODE_ID = 105080066
EXPECTED_SHA256 = "7AAEE0B4F43FFA5187C37FE8AEFF3FB9892D482CA20506C69B0C905552513F2C"
CROPS = frozenset({"WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON"})
LIVESTOCK_PRODUCTS = frozenset({"MILK", "WOOL", "EGG", "FERTILIZER"})
MOVES = frozenset({"NORTH", "SOUTH", "EAST", "WEST"})
CROP_SERVICE = frozenset({"PLANT", "WATER", "HARVEST", "DIG"})


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _quadrant(x: int, y: int) -> str:
    if x < 5 and y < 5:
        return "Q0"
    if x >= 5 and y < 5:
        return "Q1"
    if x < 5 and y >= 5:
        return "Q2"
    return "Q3"


def _unit_commands(action: dict[str, Any]) -> Iterable[tuple[int, list[Any]]]:
    farmer = action.get("farmer", ["PASS"]) or ["PASS"]
    yield 0, list(farmer)
    for index, command in enumerate(action.get("hands", []) or [], start=1):
        yield index, list(command or ["PASS"])


def _positions(farm: dict[str, Any]) -> list[tuple[int, int]]:
    return [
        tuple(farm.get("farmer", [4, 4])),
        *(tuple(value) for value in (farm.get("hands", []) or [])),
    ]


def _tile(farm: dict[str, Any], position: tuple[int, int]) -> Any:
    x, y = position
    rows = farm.get("tiles", []) or []
    if 0 <= y < len(rows) and 0 <= x < len(rows[y]):
        return rows[y][x]
    return "LOCKED"


def _farm_metrics(farm: dict[str, Any]) -> dict[str, Any]:
    surface = Counter()
    crops = Counter()
    crop_by_quadrant: dict[str, Counter[str]] = defaultdict(Counter)
    pasture_by_quadrant = Counter()
    animals_by_quadrant = Counter()
    for y, row in enumerate(farm.get("tiles", []) or []):
        for x, tile in enumerate(row):
            if tile == "LOCKED":
                continue
            quadrant = _quadrant(x, y)
            if tile is None:
                surface["empty"] += 1
                continue
            if not isinstance(tile, dict):
                continue
            kind = str(tile.get("kind", ""))
            if kind == "WEED":
                surface["weeds"] += 1
                continue
            if kind == "PLANT":
                crop = str(tile.get("crop", "UNKNOWN"))
                surface["crops"] += 1
                crops[crop] += 1
                crop_by_quadrant[quadrant][crop] += 1
                if not bool(tile.get("watered_today", False)):
                    surface["unwatered"] += 1
                if int(tile.get("consecutive_unwatered", 0) or 0) > 0:
                    surface["water_stressed"] += 1
                if int(tile.get("yield_units", 0) or 0) > 0:
                    surface["harvest_ready"] += 1
                continue
            if kind == "PASTURE":
                surface["pastures"] += 1
                pasture_by_quadrant[quadrant] += 1
                if tile.get("animal"):
                    animal = str(tile["animal"])
                    surface["animals"] += 1
                    animals_by_quadrant[quadrant] += 1
                    surface[f"animal_{animal.lower()}"] += 1
    return {
        **{key: int(value) for key, value in surface.items()},
        "crop_mix": dict(sorted(crops.items())),
        "crop_by_quadrant": {
            quadrant: dict(sorted(values.items()))
            for quadrant, values in sorted(crop_by_quadrant.items())
        },
        "pasture_by_quadrant": dict(sorted(pasture_by_quadrant.items())),
        "animals_by_quadrant": dict(sorted(animals_by_quadrant.items())),
    }


def _actionable_opcode(tile: Any) -> str | None:
    if not isinstance(tile, dict):
        return None
    if tile.get("kind") == "WEED":
        return "DIG"
    if tile.get("kind") != "PLANT":
        return None
    if int(tile.get("yield_units", 0) or 0) > 0:
        return "HARVEST"
    if not bool(tile.get("watered_today", False)):
        return "WATER"
    return None


def _transition_metrics(
    steps: list[list[dict[str, Any]]], player: int
) -> dict[str, Any]:
    transitions = Counter()
    by_display_day: dict[int, Counter[str]] = defaultdict(Counter)
    by_quadrant: dict[str, Counter[str]] = defaultdict(Counter)
    by_crop: dict[str, Counter[str]] = defaultdict(Counter)
    examples: list[dict[str, Any]] = []
    for step in range(len(steps) - 1):
        before = steps[step][player]["observation"]["farms"][player]
        after = steps[step + 1][player]["observation"]["farms"][player]
        positions = _positions(after)
        actions_at_position: dict[tuple[int, int], list[str]] = defaultdict(list)
        # Kaggle stores the command that produced an observation on that same
        # record.  Therefore the transition t -> t+1 is attributed to the
        # action attached to record t+1, not record t.
        for unit, command in _unit_commands(
            steps[step + 1][player].get("action", {})
        ):
            if unit < len(positions) and command:
                actions_at_position[positions[unit]].append(str(command[0]))
        for y, row in enumerate(before.get("tiles", []) or []):
            for x, old in enumerate(row):
                if not isinstance(old, dict) or old.get("kind") != "PLANT":
                    continue
                new = after["tiles"][y][x]
                if isinstance(new, dict) and new.get("kind") == "PLANT":
                    continue
                position = (x, y)
                opcodes = actions_at_position.get(position, [])
                max_lifespan = int(old.get("max_lifespan_step", 10**9) or 10**9)
                if "HARVEST" in opcodes:
                    reason = "harvested"
                elif "DIG" in opcodes and new is None:
                    reason = "dug_up_crop"
                elif isinstance(new, dict) and new.get("kind") == "WEED":
                    reason = (
                        "starved_to_weed"
                        if max_lifespan < 0 or step + 1 < max_lifespan
                        else "expired_to_weed"
                    )
                elif new is None and max_lifespan >= 0 and step + 1 >= max_lifespan:
                    reason = "expired_cleanly"
                elif new is None:
                    reason = "disappeared_without_observed_harvest"
                else:
                    reason = "other_exit"
                transitions[reason] += 1
                display_day = (step + 1) // 24 + 1
                quadrant = _quadrant(x, y)
                by_display_day[display_day][reason] += 1
                by_quadrant[quadrant][reason] += 1
                by_crop[str(old.get("crop", "UNKNOWN"))][reason] += 1
                if reason != "harvested" and len(examples) < 12:
                    examples.append(
                        {
                            "step": step + 1,
                            "display_day": display_day,
                            "position": [x, y],
                            "quadrant": quadrant,
                            "crop": old.get("crop"),
                            "consecutive_unwatered": int(
                                old.get("consecutive_unwatered", 0) or 0
                            ),
                            "max_lifespan_step": max_lifespan,
                            "actions_at_position": opcodes,
                            "classification": reason,
                        }
                    )
    return {
        "counts": dict(sorted(transitions.items())),
        "by_display_day": {
            str(day): dict(sorted(values.items()))
            for day, values in sorted(by_display_day.items())
        },
        "by_quadrant": {
            quadrant: dict(sorted(values.items()))
            for quadrant, values in sorted(by_quadrant.items())
        },
        "by_crop": {
            crop: dict(sorted(values.items()))
            for crop, values in sorted(by_crop.items())
        },
        "examples": examples,
    }


def _execution_metrics(
    steps: list[list[dict[str, Any]]], player: int
) -> dict[str, Any]:
    requested = Counter()
    acknowledged = Counter()
    harvested_units = Counter()
    harvest_events = Counter()
    planted_units = Counter()
    acknowledged_by_day: dict[int, Counter[str]] = defaultdict(Counter)
    planted_by_day: dict[int, Counter[str]] = defaultdict(Counter)
    harvested_units_by_day: dict[int, Counter[str]] = defaultdict(Counter)
    for step in range(1, len(steps)):
        before = steps[step - 1][player]["observation"]["farms"][player]
        record = steps[step][player]
        after = record["observation"]["farms"][player]
        positions = _positions(after)
        display_day = int(record["observation"]["day"]) + 1
        for unit, command in _unit_commands(record.get("action", {})):
            if unit >= len(positions) or not command:
                continue
            opcode = str(command[0])
            if opcode not in CROP_SERVICE:
                continue
            requested[opcode] += 1
            position = positions[unit]
            old = _tile(before, position)
            new = _tile(after, position)
            executed = False
            if opcode == "PLANT":
                executed = (
                    isinstance(new, dict)
                    and new.get("kind") == "PLANT"
                    and (not isinstance(old, dict) or old.get("kind") != "PLANT")
                )
            elif opcode == "WATER":
                executed = (
                    isinstance(old, dict)
                    and old.get("kind") == "PLANT"
                    and isinstance(new, dict)
                    and new.get("kind") == "PLANT"
                    and bool(new.get("watered_today", False))
                )
            elif opcode == "HARVEST":
                if isinstance(old, dict) and old.get("kind") == "PLANT":
                    old_units = int(old.get("yield_units", 0) or 0)
                    new_units = (
                        int(new.get("yield_units", 0) or 0)
                        if isinstance(new, dict) and new.get("kind") == "PLANT"
                        else 0
                    )
                    executed = old_units > new_units
                    if executed:
                        harvested_units[str(old.get("crop", "UNKNOWN"))] += (
                            old_units - new_units
                        )
            elif opcode == "DIG":
                executed = (
                    isinstance(old, dict)
                    and old.get("kind") in {"WEED", "PLANT"}
                    and new is None
                )
            if executed:
                acknowledged[opcode] += 1
                acknowledged_by_day[display_day][opcode] += 1
                if opcode == "PLANT" and isinstance(new, dict):
                    crop = str(new.get("crop", "UNKNOWN"))
                    planted_units[crop] += 1
                    planted_by_day[display_day][crop] += 1
                elif opcode == "HARVEST" and isinstance(old, dict):
                    crop = str(old.get("crop", "UNKNOWN"))
                    harvest_events[crop] += 1
                    old_units = int(old.get("yield_units", 0) or 0)
                    new_units = (
                        int(new.get("yield_units", 0) or 0)
                        if isinstance(new, dict) and new.get("kind") == "PLANT"
                        else 0
                    )
                    harvested_units_by_day[display_day][crop] += old_units - new_units
    return {
        "requested": dict(sorted(requested.items())),
        "acknowledged": dict(sorted(acknowledged.items())),
        "acknowledgement_rate_pct": {
            opcode: round(100.0 * acknowledged[opcode] / requested[opcode], 3)
            for opcode in sorted(requested)
        },
        "acknowledged_by_display_day": {
            str(day): dict(sorted(values.items()))
            for day, values in sorted(acknowledged_by_day.items())
        },
        "harvested_units": dict(sorted(harvested_units.items())),
        "harvested_units_total": int(sum(harvested_units.values())),
        "harvest_events": dict(sorted(harvest_events.items())),
        "mean_units_per_harvest": {
            crop: round(harvested_units[crop] / harvest_events[crop], 3)
            for crop in sorted(harvest_events)
        },
        "planted_units": dict(sorted(planted_units.items())),
        "planted_by_display_day": {
            str(day): dict(sorted(values.items()))
            for day, values in sorted(planted_by_day.items())
        },
        "harvested_units_by_display_day": {
            str(day): dict(sorted(values.items()))
            for day, values in sorted(harvested_units_by_day.items())
        },
    }


def _last_day(counts: dict[int, Counter[str]], opcode: str) -> int | None:
    values = [day for day, counter in counts.items() if counter[opcode] > 0]
    return max(values) if values else None


def _money_at(daily: list[dict[str, Any]], display_day: int) -> float:
    return float(next(row["money"] for row in daily if row["display_day"] == display_day))


def analyze(
    raw: Path = RAW,
    *,
    expected_sha256: str | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    raw_sha = _sha256(raw)
    data = json.loads(raw.read_text(encoding="utf-8"))
    steps = data["steps"]
    episode_id = int(data["info"]["EpisodeId"])
    players = [str(agent["Name"]) for agent in data["info"]["Agents"]]
    if raw.stem != str(episode_id):
        raise ValueError("replay filename and EpisodeId do not match")
    if raw.resolve() == RAW.resolve() and episode_id != EXPECTED_EPISODE_ID:
        raise ValueError(f"unexpected canonical EpisodeId: {episode_id}")
    required_sha = (
        expected_sha256
        if expected_sha256 is not None
        else EXPECTED_SHA256
        if raw.resolve() == RAW.resolve()
        else None
    )
    if required_sha is not None and raw_sha != required_sha:
        raise ValueError(f"unexpected replay SHA-256: {raw_sha}")
    if len(steps) != 720 or data.get("statuses") != ["DONE", "DONE"]:
        raise ValueError("expected a complete 720-step DONE/DONE replay")

    action_counts = [defaultdict(Counter) for _ in players]
    action_groups = [defaultdict(Counter) for _ in players]
    action_digests = [hashlib.sha256() for _ in players]
    pass_on_actionable = [Counter() for _ in players]
    sell_value = [Counter() for _ in players]
    sell_quantity = [Counter() for _ in players]
    daily: list[list[dict[str, Any]]] = [[] for _ in players]

    for step, records in enumerate(steps):
        for player, record in enumerate(records):
            action_digests[player].update(
                json.dumps(
                    record.get("action", {}),
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            )
            action_digests[player].update(b"\n")
            obs = record["observation"]
            farm = obs["farms"][player]
            positions = _positions(farm)
            display_day = int(obs["day"]) + 1
            for unit, command in _unit_commands(record.get("action", {})):
                opcode = str(command[0]) if command else "PASS"
                action_counts[player][display_day][opcode] += 1
                group = (
                    "MOVE"
                    if opcode in MOVES
                    else "CROP_SERVICE"
                    if opcode in CROP_SERVICE
                    else "PASS"
                    if opcode == "PASS"
                    else "OTHER_PRODUCTIVE"
                )
                action_groups[player][display_day][group] += 1
                if unit < len(positions):
                    needed = _actionable_opcode(_tile(farm, positions[unit]))
                    if opcode == "PASS" and needed is not None:
                        pass_on_actionable[player][needed] += 1
            for order in record.get("action", {}).get("market", []) or []:
                if not order or str(order[0]) != "SELL" or len(order) < 3:
                    continue
                item = str(order[1])
                quantity = int(order[2])
                price = float(obs["market"]["prices"].get(item, 0.0) or 0.0)
                sell_quantity[player][item] += quantity
                sell_value[player][item] += quantity * price
            if int(obs["hour"]) == 23:
                metrics = _farm_metrics(farm)
                daily[player].append(
                    {
                        "player_index": player,
                        "player": players[player],
                        "display_day": display_day,
                        "observation_day": int(obs["day"]),
                        "step": step,
                        "money": float(farm.get("money", 0.0) or 0.0),
                        "hands": len(farm.get("hands", []) or []),
                        "worker_slots": len(farm.get("hands", []) or []) + 1,
                        "quadrants": " ".join(farm.get("unlocked_quadrants", []) or []),
                        "crops": int(metrics.get("crops", 0)),
                        "unwatered": int(metrics.get("unwatered", 0)),
                        "water_stressed": int(metrics.get("water_stressed", 0)),
                        "harvest_ready": int(metrics.get("harvest_ready", 0)),
                        "weeds": int(metrics.get("weeds", 0)),
                        "pastures": int(metrics.get("pastures", 0)),
                        "animals": int(metrics.get("animals", 0)),
                        "empty": int(metrics.get("empty", 0)),
                        "crop_mix": metrics["crop_mix"],
                        "crop_by_quadrant": metrics["crop_by_quadrant"],
                        "pasture_by_quadrant": metrics["pasture_by_quadrant"],
                        "animals_by_quadrant": metrics["animals_by_quadrant"],
                    }
                )

    daily_rows = [row for player_rows in daily for row in player_rows]
    action_rows: list[dict[str, Any]] = []
    for player, name in enumerate(players):
        for display_day in range(1, 31):
            counts = action_counts[player][display_day]
            groups = action_groups[player][display_day]
            action_rows.append(
                {
                    "player_index": player,
                    "player": name,
                    "display_day": display_day,
                    "plant": counts["PLANT"],
                    "water": counts["WATER"],
                    "harvest": counts["HARVEST"],
                    "dig": counts["DIG"],
                    "move": groups["MOVE"],
                    "pass": groups["PASS"],
                    "other_productive": groups["OTHER_PRODUCTIVE"],
                    "unit_actions": sum(groups.values()),
                }
            )

    player_summaries = []
    for player, name in enumerate(players):
        player_daily = daily[player]
        peak_crops = max(row["crops"] for row in player_daily)
        peak_crop_days = [
            row["display_day"] for row in player_daily if row["crops"] == peak_crops
        ]
        late = [row for row in player_daily if row["display_day"] >= 21]
        late_actions = [
            row
            for row in action_rows
            if row["player_index"] == player and row["display_day"] >= 21
        ]
        first_three_quadrants = next(
            (
                row["display_day"]
                for row in player_daily
                if len(row["quadrants"].split()) >= 3
            ),
            None,
        )
        total_sell = float(sum(sell_value[player].values()))
        crop_sell = float(sum(sell_value[player][crop] for crop in CROPS))
        livestock_sell = float(
            sum(sell_value[player][item] for item in LIVESTOCK_PRODUCTS)
        )
        player_summaries.append(
            {
                "player_index": player,
                "player": name,
                "final_reward": float(data["rewards"][player]),
                "action_stream_sha256": action_digests[player].hexdigest().upper(),
                "first_three_quadrants_display_day": first_three_quadrants,
                "peak_crops": peak_crops,
                "peak_crop_display_days": peak_crop_days,
                "crop_tile_days_total": sum(row["crops"] for row in player_daily),
                "crop_tile_days_d21_d30": sum(row["crops"] for row in late),
                "unwatered_tile_days_total": sum(
                    row["unwatered"] for row in player_daily
                ),
                "unwatered_tile_days_d21_d30": sum(
                    row["unwatered"] for row in late
                ),
                "water_stressed_tile_days_total": sum(
                    row["water_stressed"] for row in player_daily
                ),
                "last_action_display_day": {
                    opcode: _last_day(action_counts[player], opcode)
                    for opcode in ("PLANT", "WATER", "HARVEST", "DIG")
                },
                "d21_d30_actions": {
                    key: sum(int(row[key]) for row in late_actions)
                    for key in (
                        "plant",
                        "water",
                        "harvest",
                        "dig",
                        "move",
                        "pass",
                        "other_productive",
                        "unit_actions",
                    )
                },
                "pass_on_actionable_tile": dict(pass_on_actionable[player]),
                "requested_sell_quantity": dict(
                    sorted(sell_quantity[player].items())
                ),
                "requested_sell_value": dict(sorted(sell_value[player].items())),
                "requested_crop_sell_value": crop_sell,
                "requested_livestock_product_sell_value": livestock_sell,
                "total_requested_sell_value": total_sell,
                "requested_crop_sell_share_pct": round(
                    100.0 * crop_sell / total_sell if total_sell else 0.0, 3
                ),
                "crop_action_execution": _execution_metrics(steps, player),
                "transition_metrics": _transition_metrics(steps, player),
                "late_daily": [
                    {
                        key: row[key]
                        for key in (
                            "display_day",
                            "money",
                            "hands",
                            "crops",
                            "unwatered",
                            "water_stressed",
                            "harvest_ready",
                            "weeds",
                            "pastures",
                            "animals",
                            "crop_mix",
                            "crop_by_quadrant",
                        )
                    }
                    for row in late
                ],
                "final_topology": {
                    key: player_daily[-1][key]
                    for key in (
                        "quadrants",
                        "pastures",
                        "animals",
                        "pasture_by_quadrant",
                        "animals_by_quadrant",
                    )
                },
            }
        )

    summary = {
        "schema_version": 1,
        "analysis_id": f"E18_EPISODE_{episode_id}_LIFECYCLE_ANALYSIS_V1",
        "epistemic_role": "E18_TRAINING_EVIDENCE",
        "identity": {
            "episode_id": episode_id,
            "seed": int(data["info"]["seed"]),
            "players": players,
            "rewards": [float(value) for value in data["rewards"]],
            "steps": len(steps),
            "statuses": data["statuses"],
            "schema_version": data.get("schema_version"),
            "game_version": data.get("version"),
            "module_version": data.get("module_version"),
            "raw_sha256": raw_sha,
            "raw_size_bytes": raw.stat().st_size,
        },
        "comparison": {
            "opponent_lead_final": float(data["rewards"][1] - data["rewards"][0]),
            "opponent_reward_ratio": round(
                float(data["rewards"][1] / data["rewards"][0]), 6
            ),
            "money_gap_by_display_day": {
                str(day): _money_at(daily[1], day) - _money_at(daily[0], day)
                for day in range(1, 31)
            },
        },
        "players": player_summaries,
        "observability": {
            "display_day_is_observation_day_plus_one": True,
            "sell_values_are_action_quantity_times_observed_market_price": True,
            "sell_values_are_requests_not_execution_verified": True,
            "causal_counterfactual_not_identifiable": True,
            "pass_on_actionable_tile_is_a_local_proxy_not_global_idle_time": True,
        },
    }
    return summary, daily_rows, action_rows


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    serializable = []
    for row in rows:
        serializable.append(
            {
                key: json.dumps(value, sort_keys=True) if isinstance(value, dict) else value
                for key, value in row.items()
            }
        )
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(serializable[0]))
        writer.writeheader()
        writer.writerows(serializable)


def main() -> None:
    summary, daily_rows, action_rows = analyze()
    OUT.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    _write_csv(DAILY, daily_rows)
    _write_csv(ACTIONS, action_rows)
    print(SUMMARY.relative_to(ROOT))
    for player in summary["players"]:
        last = player["last_action_display_day"]
        print(
            f"{player['player']}: reward={player['final_reward']:.0f} "
            f"peak_crops={player['peak_crops']} last_plant=D{last['PLANT']} "
            f"last_water=D{last['WATER']} "
            f"requested_crop_sell={player['requested_crop_sell_value']:.0f}"
        )


if __name__ == "__main__":
    main()
