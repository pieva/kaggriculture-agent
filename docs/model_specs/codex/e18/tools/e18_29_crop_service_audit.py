"""Verify crop water deaths at actual day refresh, not H24 snapshots."""

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
        after = recorded["observation"]["farms"][seat]
        for y, row in enumerate(farm["tiles"]):
            for x, tile in enumerate(row):
                if (
                    isinstance(tile, dict)
                    and tile.get("kind") == "PLANT"
                    and not tile.get("watered_today")
                    and tile.get("consecutive_unwatered", 0) >= 1
                    and isinstance(after["tiles"][y][x], dict)
                    and after["tiles"][y][x].get("kind") == "WEED"
                ):
                    events.append(
                        dict(
                            service_day=previous["day"] + 1,
                            position=[x, y],
                            crop=tile["crop"],
                        )
                    )
    return events
