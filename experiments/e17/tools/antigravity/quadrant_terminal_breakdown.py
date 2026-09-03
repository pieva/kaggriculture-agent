import json
from pathlib import Path

BENCHMARK_REPLAYS = [
    "data/replays/json/104527555.json",
    "data/replays/json/104541810.json",
    "data/replays/json/104543983.json",
    "data/replays/json/104547425.json",
    "data/replays/json/104564762.json",
    "data/replays/json/104577270.json",
    "data/replays/json/104578185.json",
    "data/replays/json/104586335.json",
    "data/replays/json/104586487.json",
]

def get_quad_name(x: int, y: int) -> str:
    if x < 5 and y < 5:
        return "Q0_NW"
    elif x >= 5 and y < 5:
        return "Q1_NE"
    elif x < 5 and y >= 5:
        return "Q2_SW"
    else:
        return "Q3_SE"

def extract_episode_quadrants(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        raw = json.load(f)

    ep_id = raw["info"]["EpisodeId"]
    seed = raw["info"]["seed"]
    team_names = raw["info"]["TeamNames"]
    final_rewards = [raw["steps"][-1][p]["reward"] for p in (0, 1)]

    res = {
        "episode_id": ep_id,
        "seed": seed,
        "players": []
    }

    for p in (0, 1):
        ag = team_names[p]
        rew = final_rewards[p]
        farm = raw["steps"][-1][p]["observation"]["farms"][p]
        tiles = farm["tiles"]

        # Quadrant unlock steps / days
        q1_step = None
        q1_day = None
        q2_step = None
        q2_day = None

        for st in range(len(raw["steps"])):
            uq = raw["steps"][st][p]["observation"]["farms"][p].get("unlocked_quadrants", [])
            uq_set = set(uq)
            if q1_step is None and ("NE" in uq_set or 1 in uq_set):
                q1_step = st
                q1_day = st // 24
            if q2_step is None and ("SW" in uq_set or 2 in uq_set):
                q2_step = st
                q2_day = st // 24

        quad_details = {}
        for q_target in ["Q0_NW", "Q1_NE", "Q2_SW"]:
            quad_details[q_target] = {
                "empty_uncultivated": 0,
                "weeds": 0,
                "crops": {},
                "total_crops": 0,
                "animals": {},
                "total_animals": 0,
                "empty_structures": {},
                "total_empty_structures": 0,
                "total_tiles": 25
            }

        for y in range(10):
            for x in range(10):
                q = get_quad_name(x, y)
                if q == "Q3_SE":
                    continue
                t = tiles[y][x]
                qd = quad_details[q]
                if t is None:
                    qd["empty_uncultivated"] += 1
                elif isinstance(t, dict):
                    k = t.get("kind")
                    if k == "PLANT":
                        c = t.get("crop", "UNKNOWN")
                        qd["crops"][c] = qd["crops"].get(c, 0) + 1
                        qd["total_crops"] += 1
                    elif k in ("COOP", "PASTURE"):
                        a = t.get("animal")
                        if a:
                            qd["animals"][a] = qd["animals"].get(a, 0) + 1
                            qd["total_animals"] += 1
                        else:
                            qd["empty_structures"][k] = qd["empty_structures"].get(k, 0) + 1
                            qd["total_empty_structures"] += 1
                    elif k == "WEED":
                        qd["weeds"] += 1

        res["players"].append({
            "player_index": p,
            "agent_name": ag,
            "final_reward": rew,
            "q1_unlock_day": q1_day,
            "q1_unlock_step": q1_step,
            "q2_unlock_day": q2_day,
            "q2_unlock_step": q2_step,
            "quadrants": quad_details
        })
    return res

def main():
    all_episodes = []
    for fp in BENCHMARK_REPLAYS:
        ep_data = extract_episode_quadrants(fp)
        all_episodes.append(ep_data)

    out_path = "experiments/e17/artifacts/discovery/antigravity/quadrant_terminal_breakdown.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_episodes, f, indent=2)
    print(f"Generated {out_path}")

if __name__ == "__main__":
    main()
