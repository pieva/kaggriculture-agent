"""V48 ledger algorithm with explicit residual reporting for external engine differences."""
import importlib
from collections import Counter
from copy import deepcopy
from types import SimpleNamespace

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
    # Discrepancies are retained, never silently accepted as parity.
    initial = replay["steps"][0][seat]["observation"]["farms"][seat]["money"]
    net = sum(sum(d["sales_cash"].values()) - sum(d["purchase_cash"].values()) - d["hire_cash"] - d["land_cash"] + d["unit_cash_delta"] for d in days)
    residual = replay["rewards"][seat] - initial - net
    return {"daily": days, "cash_parity_steps_both_players": 719, "cash_parity_errors": len(cash_errors), "cash_discrepancies": cash_errors, "net_cash_residual": residual,
            "initial_cash": initial, "net_cash_flow": net, "animal_escapes": losses}
