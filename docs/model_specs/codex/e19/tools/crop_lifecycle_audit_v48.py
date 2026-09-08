"""Classify legacy dry-to-weed events by lifecycle; does not change policy."""

import importlib
from collections import Counter
from copy import deepcopy


def crop_service_audit(replay, seat):
    engine = importlib.import_module(
        "kaggle_environments.envs.kaggriculture.kaggriculture"
    )
    board = int(replay["configuration"].get("boardSize", 10))
    capacity = int(replay["configuration"].get("shedCapacity", 100))
    events = []
    for index in range(1, len(replay["steps"])):
        previous = replay["steps"][index - 1][seat]["observation"]
        recorded = replay["steps"][index][seat]
        if recorded["observation"]["day"] == previous["day"]:
            continue
        farm, private = deepcopy(previous["farms"][seat]), deepcopy(previous["private"])
        action = recorded.get("action") or {}
        commands = [action.get("farmer", ["PASS"]), *action.get("hands", [])]
        demand = Counter(
            cmd[1]
            for cmd in commands
            if isinstance(cmd, list) and len(cmd) >= 2 and cmd[0] == "PLANT"
        )
        blocked = {
            crop
            for crop, count in demand.items()
            if count > private["seeds"].get(crop, 0)
        }
        for worker, command in enumerate(commands):
            if not isinstance(command, list) or not command:
                continue
            allowed = (
                ["PASS"]
                if command[0] == "PLANT" and len(command) > 1 and command[1] in blocked
                else command
            )
            engine._apply_unit_action(
                farm, private, worker, allowed, board, previous["day"], 24, capacity
            )
        post_units = deepcopy(farm)
        step = previous['day'] * 24 + previous['hour']
        engine._decay_plants(farm, step)
        after = recorded["observation"]["farms"][seat]
        for y, row in enumerate(post_units["tiles"]):
            for x, tile in enumerate(row):
                if (
                    isinstance(tile, dict)
                    and tile.get("kind") == "PLANT"
                    and not tile.get("watered_today")
                    and tile.get("consecutive_unwatered", 0) >= 1
                    and isinstance(after["tiles"][y][x], dict)
                    and after["tiles"][y][x].get("kind") == "WEED"
                ):
                    rules = engine.CROPS[tile['crop']]
                    last_day = (tile['planted_day'] + rules['first_yield_day']
                                + (rules['max_yield'] - 1) * rules['interval']) if rules['ongoing'] else None
                    future = (last_day > previous['day']) if last_day is not None else bool(
                        previous['day'] - tile['planted_day'] <= rules['max_yield_day']
                        and tile['yield_units'] < rules['max_yield'])
                    decayed = farm['tiles'][y][x].get('kind') == 'WEED'
                    events.append(
                        dict(
                            service_day=previous["day"] + 1,
                            position=[x, y],
                            crop=tile["crop"],
                            held_units_after_actions=tile['yield_units'],
                            future_production=future,
                            last_production_day=None if last_day is None else last_day+1,
                            physical_cause='decay' if decayed else 'water_refresh',
                            productive_loss=bool(tile['yield_units']>0 or future),
                            tile_after_actions=deepcopy(tile),
                        )
                    )
    return events
