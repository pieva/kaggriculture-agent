"""Read-only diagnosis of late annual cycles, actual cash fills and terminal capacity."""

from __future__ import annotations

import hashlib
import importlib
import json
import statistics
from collections import Counter
from copy import deepcopy
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[3]
DERIVED = BASE / "artifacts/derived"
OUTPUT = DERIVED / "E18_27_TOP770_D25_D30_CARROT_DIAGNOSIS.json"
REPORT = BASE / "reports/E18_27_TOP770_D25_D30_CARROT_DIAGNOSIS_IT.md"
ITEMS = ("CARROT", "WHEAT", "STRAWBERRY", "MILK", "WOOL", "FERTILIZER")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def stats(values):
    return {
        "median": statistics.median(values),
        "min": min(values),
        "max": max(values),
        "mean": statistics.mean(values),
    }


def cash_flow(row):
    return (
        sum(row["sales_cash"].values())
        - sum(row["purchase_cash"].values())
        - row["hire_cash"]
        - row["land_cash"]
        + row["unit_cash_delta"]
    )


def profile_window(profile, first=25, last=30):
    rows = profile["ledger"]["daily"][first - 1 : last]
    assert profile["ledger"]["cash_parity_errors"] == 0
    groups = (
        "planted",
        "harvested",
        "sold_units",
        "sales_cash",
        "purchase_cash",
        "requested_actions",
        "executed_actions",
        "dig_removed",
    )
    result = {
        key: dict(sum((Counter(row[key]) for row in rows), Counter())) for key in groups
    }
    result.update(
        {
            "hire_cash": sum(r["hire_cash"] for r in rows),
            "net_cash": sum(cash_flow(r) for r in rows),
            "terminal": profile["terminal"],
        }
    )
    result["realized_prices"] = {
        k: result["sales_cash"].get(k, 0) / result["sold_units"][k]
        for k in ITEMS
        if result["sold_units"].get(k)
    }
    return result


def trace_annuals(replay, seat, engine):
    """Apply unit actions to isolated recorded pre-states, retaining successful crop lifecycles."""
    cycles = {}
    late_orders = []
    for index in range(1, len(replay["steps"])):
        before = replay["steps"][index - 1][seat]["observation"]
        day = before["day"] + 1
        if day < 20:
            continue
        farm = deepcopy(before["farms"][seat])
        private = deepcopy(before["private"])
        action = replay["steps"][index][seat].get("action") or {}
        commands = [action.get("farmer", ["PASS"]), *action.get("hands", [])]
        demand = Counter(
            c[1]
            for c in commands
            if isinstance(c, list) and len(c) > 1 and c[0] == "PLANT"
        )
        blocked = {c for c, n in demand.items() if n > private["seeds"].get(c, 0)}
        for worker, command in enumerate(commands):
            if not isinstance(command, list) or not command:
                continue
            pos = engine._farmer_position(farm, worker)
            if not pos:
                continue
            x, y = pos
            old = deepcopy(farm["tiles"][y][x])
            inv = deepcopy(private["inventories"][worker])
            op = command[0]
            allowed = ["PASS"] if op == "PLANT" and command[1] in blocked else command
            engine._apply_unit_action(
                farm, private, worker, allowed, 10, day - 1, 24, 100
            )
            tile = farm["tiles"][y][x]
            event = {
                "day": day,
                "hour": before["hour"] + 1,
                "recorded_step": index,
                "worker": worker,
            }
            if (
                op == "PLANT"
                and old is None
                and isinstance(tile, dict)
                and tile.get("crop") in ("CARROT", "WHEAT")
            ):
                crop = tile["crop"]
                key = (x, y, crop, tile["planted_day"])
                cycles[key] = {
                    "x": x,
                    "y": y,
                    "crop": crop,
                    "plant": event,
                    "plant_prices": before["market"]["prices"],
                    "town_shops": before["town"]["unlocked_shops"],
                    "water": [],
                    "fertilize": [],
                    "harvest": None,
                }
            if isinstance(old, dict) and old.get("crop") in ("CARROT", "WHEAT"):
                key = (x, y, old["crop"], old["planted_day"])
                if key in cycles:
                    cycle = cycles[key]
                    if op == "WATER" and old != tile:
                        cycle["water"].append(
                            event | {"age": day - 1 - old["planted_day"]}
                        )
                    if op == "FERTILIZE" and private["inventories"][worker].get(
                        "FERTILIZER", 0
                    ) < inv.get("FERTILIZER", 0):
                        cycle["fertilize"].append(event)
                    if op == "HARVEST":
                        units = private["inventories"][worker].get(
                            old["crop"], 0
                        ) - inv.get(old["crop"], 0)
                        if units > 0:
                            cycle["harvest"] = event | {
                                "age": day - 1 - old["planted_day"],
                                "units": units,
                                "watered_before": old["watered_today"],
                            }
        if day >= 25:
            for order in action.get("market", []):
                if order[0] in ("SELL", "BUY_SEED") and order[1] in ("WHEAT", "CARROT"):
                    late_orders.append(
                        {
                            "day": day,
                            "hour": before["hour"] + 1,
                            "recorded_step": index,
                            "order": order,
                            "quote_before_batch": before["market"]["prices"][order[1]],
                        }
                    )
    return {"cycles": list(cycles.values()), "requested_market_orders": late_orders}


def main():
    top_path = DERIVED / "E18_26_JESSE_770_D01_D30_CLOSURE.json"
    local_path = DERIVED / "E18_27_D10_D15_DEVELOPMENT_V3.json"
    top = read(top_path)["jesse"]
    local = read(local_path)
    assert local["complete"]
    cohorts = {
        "Top770": top,
        "E18.27 V3": [m for m in local["matches"] if m["version"] == "E18.27"],
        "E18.26": [m for m in local["matches"] if m["version"] == "E18.26"],
    }
    assert len(top) == 5 and len(cohorts["E18.27 V3"]) == len(cohorts["E18.26"]) == 14
    engine = importlib.import_module(
        "kaggle_environments.envs.kaggriculture.kaggriculture"
    )
    profiles = []
    for name, members in cohorts.items():
        for p in members:
            identity = {
                "cohort": name,
                "seat": p["seat"],
                "seed": p.get("seed"),
                "episode_id": p.get("episode_id"),
            }
            result = identity | {
                "D25_D30": profile_window(p),
                "D26_D30": profile_window(p, 26),
            }
            if name == "Top770":
                path = ROOT / f"data/replays/json/{p['episode_id']}.json"
                assert digest(path) == p["sha256"]
                replay = read(path)
                result["annual_trace"] = trace_annuals(replay, p["seat"], engine)
                carrots = [
                    c for c in result["annual_trace"]["cycles"] if c["crop"] == "CARROT"
                ]
                assert sum(
                    c["harvest"]["units"] for c in carrots if c["harvest"]
                ) == result["D25_D30"]["harvested"].get("CARROT", 0)
                result["carrot_cycles"] = {
                    "plants": len(carrots),
                    "harvested_tiles": sum(c["harvest"] is not None for c in carrots),
                    "unharvested": [c for c in carrots if c["harvest"] is None],
                    "harvest_age_counts": dict(
                        Counter(c["harvest"]["age"] for c in carrots if c["harvest"])
                    ),
                    "harvest_yield_counts": dict(
                        Counter(c["harvest"]["units"] for c in carrots if c["harvest"])
                    ),
                    "fertilizer_applications": sum(
                        len(c["fertilize"]) for c in carrots
                    ),
                    "water_actions": sum(len(c["water"]) for c in carrots),
                }
                result["carrot_daily"] = [
                    {
                        "day": d,
                        "planted": p["ledger"]["daily"][d - 1]["planted"].get(
                            "CARROT", 0
                        ),
                        "harvested": p["ledger"]["daily"][d - 1]["harvested"].get(
                            "CARROT", 0
                        ),
                        "sold": p["ledger"]["daily"][d - 1]["sold_units"].get(
                            "CARROT", 0
                        ),
                        "cash": p["ledger"]["daily"][d - 1]["sales_cash"].get(
                            "CARROT", 0
                        ),
                    }
                    for d in range(25, 31)
                ]
                print(
                    f"Top770 {p['episode_id']}: {result['carrot_cycles']}", flush=True
                )
            profiles.append(result)
    daily = {}
    for name, members in cohorts.items():
        daily[name] = []
        for day in range(25, 31):
            values = []
            for p in members:
                snapshot = p["daily"][day - 1]
                ledger = p["ledger"]["daily"][day - 1]
                values.append(
                    {
                        "people": snapshot["people"],
                        "crop_tiles": snapshot["crop_tiles"],
                        **snapshot["crops"],
                        "cash_h24": snapshot["money"],
                        "cash_after_day_actions": p["ledger"]["initial_cash"]
                        + sum(cash_flow(r) for r in p["ledger"]["daily"][:day]),
                        "daily_net_cash": cash_flow(ledger),
                        "harvest_actions": ledger["executed_actions"].get("HARVEST", 0),
                        "move_requested": ledger["requested_actions"].get("MOVE", 0),
                        "pass_requested": ledger["requested_actions"].get("PASS", 0),
                    }
                )
            daily[name].append(
                {
                    "day": day,
                    "metrics": {k: stats([v[k] for v in values]) for k in values[0]},
                }
            )
    summary = {}
    for name in cohorts:
        selected = [p["D25_D30"] for p in profiles if p["cohort"] == name]
        metrics = {}
        for category in ("planted", "harvested", "sold_units", "sales_cash"):
            metrics[category] = {
                k: stats([p[category].get(k, 0) for p in selected]) for k in ITEMS
            }
        for key in ("hire_cash", "net_cash"):
            metrics[key] = stats([p[key] for p in selected])
        summary[name] = metrics
    top_profiles = [p for p in profiles if p["cohort"] == "Top770"]
    late_by_episode = [
        {
            (c["plant"]["recorded_step"], c["x"], c["y"]): c
            for c in p["annual_trace"]["cycles"]
            if c["plant"]["day"] >= 26
        }
        for p in top_profiles
    ]
    assert all(set(p) == set(late_by_episode[0]) for p in late_by_episode)
    common_slots = []
    for key in sorted(late_by_episode[0]):
        cycles = [p[key] for p in late_by_episode]
        assert all(
            c["water"] == cycles[0]["water"] and c["harvest"] == cycles[0]["harvest"]
            for c in cycles
        )
        common_slots.append(
            {
                "recorded_step": key[0],
                "x": key[1],
                "y": key[2],
                "day": cycles[0]["plant"]["day"],
                "choices": {
                    str(p["episode_id"]): c["crop"]
                    for p, c in zip(top_profiles, cycles)
                },
                "units": cycles[0]["harvest"]["units"] if cycles[0]["harvest"] else 0,
                "always_carrot": all(c["crop"] == "CARROT" for c in cycles),
            }
        )
    decisions = []
    for p, slots in zip(top_profiles, late_by_episode):
        first_cycle = min(slots.values(), key=lambda c: c["plant"]["recorded_step"])
        decisions.append(
            {
                "episode_id": p["episode_id"],
                "carrot_plants": p["carrot_cycles"]["plants"],
                "carrot_quote_first_plant": first_cycle["plant_prices"]["CARROT"],
                "wheat_quote_first_plant": first_cycle["plant_prices"]["WHEAT"],
                "town_shops": first_cycle["town_shops"],
            }
        )
    choice = {
        "same_late_slots": len(common_slots),
        "always_carrot_slots": sum(c["always_carrot"] for c in common_slots),
        "switchable_slots": sum(not c["always_carrot"] for c in common_slots),
        "switchable_harvest_units": sum(
            c["units"] for c in common_slots if not c["always_carrot"]
        ),
        "water_and_harvest_events_identical": True,
        "slots": common_slots,
        "initial_conditions": decisions,
    }
    payload = {
        "analysis_id": OUTPUT.stem,
        "source_hashes": {
            top_path.name: digest(top_path),
            local_path.name: digest(local_path),
            "installed_engine": digest(Path(engine.__file__)),
        },
        "methodology": "D25-D30 actual action-day cash fills; H24 snapshots separately labelled. Public cohort descriptive, not matched to local. No counterfactual price inference.",
        "crop_rules": {k: engine.CROPS[k] for k in ("CARROT", "WHEAT")},
        "profiles": profiles,
        "daily": daily,
        "summary": summary,
        "late_species_choice": choice,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "late_species_choice": {
                    k: v for k, v in choice.items() if k != "slots"
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
