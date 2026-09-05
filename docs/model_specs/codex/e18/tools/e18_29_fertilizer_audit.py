"""Reconstruct fertilizer collection/delivery without relying on DROP intent."""

import importlib
from collections import Counter
from copy import deepcopy


def fertilizer_audit(replay, seat):
    engine = importlib.import_module(
        "kaggle_environments.envs.kaggriculture.kaggriculture"
    )
    board = int(replay["configuration"].get("boardSize", 10))
    capacity = int(replay["configuration"].get("shedCapacity", 100))
    days = [Counter() for _ in range(30)]
    for index in range(1, len(replay["steps"])):
        previous = replay["steps"][index - 1][seat]["observation"]
        day = previous["day"]
        stats = days[day]
        farm, private = deepcopy(previous["farms"][seat]), deepcopy(previous["private"])
        action = replay["steps"][index][seat].get("action") or {}
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
            if (
                not isinstance(command, list)
                or not command
                or worker >= len(private["inventories"])
            ):
                continue
            op = command[0]
            before_inv = private["inventories"][worker].get("FERTILIZER", 0)
            before_shed = private["shed"].get("FERTILIZER", 0)
            allowed = (
                ["PASS"]
                if op == "PLANT" and len(command) > 1 and command[1] in blocked
                else command
            )
            engine._apply_unit_action(
                farm, private, worker, allowed, board, day, 24, capacity
            )
            after_inv = private["inventories"][worker].get("FERTILIZER", 0)
            after_shed = private["shed"].get("FERTILIZER", 0)
            if op == "COLLECT_FERTILIZER":
                stats["collected"] += max(0, after_inv - before_inv)
            if op == "DROP":
                stats["delivered"] += max(0, after_shed - before_shed)
                stats["drop_destroyed"] += max(
                    0, before_inv - after_inv - (after_shed - before_shed)
                )
            if op == "FERTILIZE":
                stats["used"] += max(0, before_inv - after_inv)
    return [dict(day=i + 1, **stats) for i, stats in enumerate(days)]
