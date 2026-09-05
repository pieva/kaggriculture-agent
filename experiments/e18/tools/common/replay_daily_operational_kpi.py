"""Common daily operational KPI, with explicit action/checkpoint boundaries."""

from collections import Counter


def daily_operational_kpi(replay, seat, ledger):
    losses = Counter()
    for event in ledger["animal_escapes"]:
        # Events were verified by comparing post-unit state with refresh state.
        # Report on the day whose missed service caused the refresh loss.
        before = replay["steps"][event["recorded_step"] - 1][seat]["observation"]
        losses[before["day"] + 1] += 1
    result = []
    for day in range(1, 31):
        observation = replay["steps"][24 * day - 1][seat]["observation"]
        tiles = [
            t
            for row in observation["farms"][seat]["tiles"]
            for t in row
            if isinstance(t, dict)
        ]
        commands = ledger["daily"][day - 1]["requested_actions"]
        result.append(
            {
                "day": day,
                "MOVE": commands.get("MOVE", 0),
                "PASS": commands.get("PASS", 0),
                "unwatered_tiles_h24": sum(
                    t.get("kind") == "PLANT" and not t.get("watered_today", False)
                    for t in tiles
                ),
                "water_stressed_tiles_h24": sum(
                    t.get("kind") == "PLANT" and t.get("consecutive_unwatered", 0) > 0
                    for t in tiles
                ),
                "verified_animal_losses": losses[day],
                "weed_tiles": sum(t.get("kind") == "WEED" for t in tiles),
            }
        )
    return result
