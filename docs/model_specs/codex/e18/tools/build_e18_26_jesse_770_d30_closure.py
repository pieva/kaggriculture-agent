"""Daily D1-D30 trajectories and cash-verified replay settlement audit."""
from __future__ import annotations

import importlib
import json
import statistics
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d20_trajectories import (
    ANIMALS, BASE, CROPS, EPISODES, SEED, digest, snapshot,
)

OUTPUT = BASE / "artifacts/derived/E18_26_JESSE_770_D01_D30_CLOSURE.json"
REPORT = BASE / "reports/E18_26_TOP770_D01_D30_CLOSURE_IT.md"


def nonzero(values):
    return {k: v for k, v in values.items() if v}


def end_state(replay, seat):
    observation = replay["steps"][-1][seat]["observation"]
    private = observation["private"]
    carried = Counter()
    for inventory in private["inventories"]:
        carried.update(inventory)
    yields = Counter()
    animals = {"COW": "MILK", "SHEEP": "WOOL", "GOOSE": "EGG"}
    for row in observation["farms"][seat]["tiles"]:
        for tile in row:
            if isinstance(tile, dict) and tile.get("yield_units", 0):
                item = tile.get("crop") or animals.get(tile.get("animal"))
                if item:
                    yields[item] += tile["yield_units"]
    return {"cash": observation["farms"][seat]["money"], "reward": replay["rewards"][seat],
            "shed": nonzero(private["shed"]), "carried": nonzero(carried),
            "seeds": nonzero(private["seeds"]), "tile_yield_units": nonzero(yields),
            "spot_prices": observation["market"]["prices"]}


def audit(replay, seat):
    """Execute recorded unit/market batches on isolated copies; verify cash each step.

    Quotes are replayed in both-player lockstep. No random events or policy calls
    are needed: each step starts from its own immutable recorded observation.
    """
    engine = importlib.import_module("kaggle_environments.envs.kaggriculture.kaggriculture")
    days = [{"day": d, **{key: Counter() for key in (
        "requested_actions", "executed_actions", "planted", "harvested", "sold_units", "sales_cash",
        "bought_units", "purchase_cash", "dig_removed", "animal_placed")},
        "hire_cash": 0, "hires": 0, "land_cash": 0, "unit_cash_delta": 0} for d in range(1, 31)]
    cfg = SimpleNamespace(**replay["configuration"])
    board = int(replay["configuration"].get("boardSize", 10))
    cap = int(replay["configuration"].get("shedCapacity", 100))
    original_commit, original_hire, original_land = engine._commit_unit, engine._do_hire, engine._do_buy_land
    active_farms, ledger = [], None
    cash_errors = []
    losses = []

    def commit(op, item, price, farm, private, market, capacity=100):
        ok = original_commit(op, item, price, farm, private, market, capacity)
        if ok and farm is active_farms[seat]:
            if op == "SELL":
                ledger["sold_units"][item] += 1
                ledger["sales_cash"][item] += price
            else:
                ledger["bought_units"][f"{op}:{item}"] += 1
                ledger["purchase_cash"][f"{op}:{item}"] += price
        return ok

    def hire(farm, private, board_size, mult=1):
        before, hands = farm["money"], len(farm["hands"])
        original_hire(farm, private, board_size, mult)
        if farm is active_farms[seat]:
            ledger["hire_cash"] += before - farm["money"]
            ledger["hires"] += len(farm["hands"]) - hands

    def land(farm, board_size):
        before = farm["money"]
        original_land(farm, board_size)
        if farm is active_farms[seat]:
            ledger["land_cash"] += before - farm["money"]

    engine._commit_unit, engine._do_hire, engine._do_buy_land = commit, hire, land
    try:
        for index in range(1, len(replay["steps"])):
            previous, recorded = replay["steps"][index - 1], replay["steps"][index]
            day = int(previous[0]["observation"]["day"])
            ledger = days[day]
            active_farms = deepcopy(previous[0]["observation"]["farms"])
            market = deepcopy(previous[0]["observation"]["market"])
            states = [SimpleNamespace(action=row.get("action") or {}, observation=SimpleNamespace(
                farms=active_farms, market=market, private=deepcopy(previous[i]["observation"]["private"])))
                for i, row in enumerate(recorded)]
            before_unit_money = active_farms[seat]["money"]
            for player, state in enumerate(states):
                farm, private = active_farms[player], state.observation.private
                commands = [state.action.get("farmer", ["PASS"]), *state.action.get("hands", [])]
                demand = Counter(cmd[1] for cmd in commands if isinstance(cmd, list) and len(cmd) >= 2 and cmd[0] == "PLANT")
                blocked = {crop for crop, count in demand.items() if count > private["seeds"].get(crop, 0)}
                for worker, command in enumerate(commands):
                    if not isinstance(command, list) or not command:
                        continue
                    op = command[0]
                    if player == seat:
                        ledger["requested_actions"]["MOVE" if op in engine.FARMER_MOVES else op] += 1
                    pos = engine._farmer_position(farm, worker)
                    old_tile = deepcopy(farm["tiles"][pos[1]][pos[0]]) if pos else None
                    old_inv = deepcopy(private["inventories"][worker]) if worker < len(private["inventories"]) else {}
                    allowed = ["PASS"] if op == "PLANT" and len(command) > 1 and command[1] in blocked else command
                    engine._apply_unit_action(farm, private, worker, allowed, board, day, 24, cap)
                    if player != seat or not pos:
                        continue
                    tile = farm["tiles"][pos[1]][pos[0]]
                    inventory = private["inventories"][worker] if worker < len(private["inventories"]) else {}
                    changed = old_tile != tile
                    if op in ("PLANT", "WATER", "FEED", "CARE", "FERTILIZE", "DIG", "BUILD_PASTURE", "BUILD_COOP") and changed:
                        ledger["executed_actions"][op] += 1
                    if op == "PLANT" and changed and isinstance(tile, dict) and tile.get("kind") == "PLANT":
                        ledger["planted"][tile["crop"]] += 1
                    if op == "DIG" and changed and isinstance(old_tile, dict):
                        ledger["dig_removed"][old_tile.get("crop", old_tile["kind"])] += 1
                    if op == "HARVEST":
                        gain = Counter({item: value-old_inv.get(item, 0) for item, value in inventory.items() if value > old_inv.get(item, 0)})
                        if gain:
                            ledger["harvested"].update(gain)
                            ledger["executed_actions"][op] += 1
                    if op == "PLACE" and changed and isinstance(tile, dict) and tile.get("animal"):
                        ledger["animal_placed"][tile["animal"]] += 1
            ledger["unit_cash_delta"] += active_farms[seat]["money"] - before_unit_money
            engine._process_market(states, SimpleNamespace(configuration=cfg))
            for player in (0, 1):
                expected = recorded[player]["observation"]["farms"][player]["money"]
                if active_farms[player]["money"] != expected:
                    cash_errors.append({"index": index, "seat": player, "expected": expected, "reconstructed": active_farms[player]["money"]})
            actual_after = recorded[seat]["observation"]["farms"][seat]
            for y, row in enumerate(active_farms[seat]["tiles"]):
                for x, tile in enumerate(row):
                    after = actual_after["tiles"][y][x]
                    if isinstance(tile, dict) and tile.get("animal") and isinstance(after, dict) and not after.get("animal"):
                        losses.append({"recorded_step": index, "display_day_after": recorded[seat]["observation"]["day"]+1,
                                       "x": x, "y": y, "animal": tile["animal"], "fed_today_before_refresh": tile["fed_today"],
                                       "consecutive_unfed_before_refresh": tile["consecutive_unfed"],
                                       "actual_before_animals": sum(bool(t.get("animal")) for row in previous[seat]["observation"]["farms"][seat]["tiles"] for t in row if isinstance(t, dict)),
                                       "pre_refresh_animals": sum(bool(t.get("animal")) for row in active_farms[seat]["tiles"] for t in row if isinstance(t, dict)),
                                       "actual_after_animals": sum(bool(t.get("animal")) for row in actual_after["tiles"] for t in row if isinstance(t, dict)),
                                       "candidate_batch": recorded[seat].get("action")})
    finally:
        engine._commit_unit, engine._do_hire, engine._do_buy_land = original_commit, original_hire, original_land
    assert not cash_errors, cash_errors[:4]
    initial = replay["steps"][0][seat]["observation"]["farms"][seat]["money"]
    net = sum(sum(d["sales_cash"].values()) - sum(d["purchase_cash"].values()) - d["hire_cash"] - d["land_cash"] + d["unit_cash_delta"] for d in days)
    assert initial + net == replay["rewards"][seat], (initial, net, replay["rewards"][seat])
    return {"daily": days, "cash_parity_steps_both_players": 719, "cash_parity_errors": 0,
            "initial_cash": initial, "net_cash_flow": net, "animal_escapes": losses}


def summarize(replay, seat, identity):
    assert len(replay["steps"]) == 720
    assert all(row["status"] == "DONE" for row in replay["steps"][-1])
    daily = [snapshot(replay, day, seat) for day in range(1, 31)]
    assert daily[-1]["pasture_topology"] == {"Q0": 7, "Q1": 7, "Q2": 0, "Q3": 0}
    ledger = audit(replay, seat)
    print(f"{identity}: 30 checkpoints, 719 two-player cash settlements verified", flush=True)
    return {"identity": identity, "seat": seat, "daily": daily, "ledger": ledger, "terminal": end_state(replay, seat)}


def flattened(row):
    pasture_count = sum(row["pasture_topology"].values())
    occupied_pastures = row["animals"]["COW"] + row["animals"]["SHEEP"]
    return ({key: row[key] for key in ("people", "hands", "money", "crop_tiles", "empty_livestock_tiles", "livestock_structures", "occupied_livestock_tiles")}
            | row["crops"] | row["animals"]
            | {"empty_pastures": pasture_count-occupied_pastures,
               "empty_coops": row["livestock_structures"]-pasture_count-row["animals"]["GOOSE"]})


def aggregates(profiles):
    result = []
    for day in range(30):
        values = [flattened(p["daily"][day]) for p in profiles]
        result.append({"day": day+1, "metrics": {key: {"median": statistics.median(row[key] for row in values),
                       "min": min(row[key] for row in values), "max": max(row[key] for row in values)} for key in values[0]}})
    return result


def main():
    from kaggle_environments import make
    from docs.model_specs.codex.e18.tools.e18_26_jesse_boost_d10_controller import JesseBoostD10Controller
    from docs.model_specs.codex.e18.tools.run_e18_26_770_jesse_boost_d10_gate import _incumbent
    old = json.loads((BASE / "artifacts/derived/E18_26_JESSE_770_D01_D20_TRAJECTORIES.json").read_text())
    plan_path = BASE / "artifacts/derived/E18_26_770_JESSE_BOOST_D10_PLAN_V1.json"
    assert digest(plan_path) == old["sources"]["plan_sha256"]
    plan = json.loads(plan_path.read_text())
    profiles = {"jesse": [], "codex": []}
    for episode in EPISODES:
        path = ROOT / f"data/replays/json/{episode}.json"
        source = next(p for p in old["jesse"] if p["episode_id"] == episode)
        assert digest(path) == source["sha256"]
        replay = json.loads(path.read_text(encoding="utf-8"))
        assert replay["info"]["EpisodeId"] == episode
        profile = summarize(replay, source["seat"], f"Jesse {episode}")
        assert profile["daily"][:20] == source["daily"]
        profile.update({key: value for key, value in source.items() if key != "daily"})
        profiles["jesse"].append(profile)
    for seat in (0, 1):
        candidate = JesseBoostD10Controller(plan, seat=seat)
        opponent = _incumbent({}, 1-seat)
        env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": SEED, "turnsPerDay": 24}, debug=False)
        env.run([candidate, opponent] if seat == 0 else [opponent, candidate])
        candidate.finalize_metrics()
        replay = env.toJSON()
        assert candidate.error_count == 0
        source = next(p for p in old["codex"] if p["seat"] == seat)
        assert replay["rewards"][seat] == source["reward"]
        profile = summarize(replay, seat, f"E18.26 P{seat}")
        assert profile["daily"][:20] == source["daily"]
        profile.update({key: value for key, value in source.items() if key != "daily"})
        profiles["codex"].append(profile)
    payload = {"schema_version": 1, "analysis_id": OUTPUT.stem, "observed_at": "2026-09-05",
        "methodology": old["methodology"] | {
            "sample": "D1-D30 H24, index 24*day-1; D30 is terminal and money equals game reward.",
            "settlement": "Re-execute recorded unit actions then exact two-player lockstep market against isolated pre-step state copies. Verify each player's cash against the recorded post-step state. Count successful fills, not requested orders.",
            "action_day": "Action ledgers use the pre-action calendar day. An action recorded at next-day H1 belongs to the previous day's final action; daily H24 cash deltas and action-day cash flows therefore have slightly different boundaries.",
            "terminal": "Only cash contributes to game reward. Stored/carried products and tile yields are item counts, not automatically monetized assets. Tile yield may not yet be mature.",
            "variability": "Pointwise medians and observed min-max. The median curve is descriptive and can switch episodes; no paired causal comparison of cash across public and local cohorts."},
        "sources": old["sources"], **profiles, "aggregates": {key: aggregates(rows) for key, rows in profiles.items()}}
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    from docs.model_specs.codex.e18.tools.summarize_e18_26_jesse_770_d30_closure import write_report
    write_report(payload)
    print(OUTPUT, flush=True)


if __name__ == "__main__":
    main()
