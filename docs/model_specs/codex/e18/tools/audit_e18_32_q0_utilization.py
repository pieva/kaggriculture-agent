"""Read-only diagnosis of the frozen plan and six already-consumed public replays.

No opponent selection, tuning, policy mutation, or counterfactual profit claims.
Daily snapshots use observation Dn H24, as the existing comparison reports do.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path
from statistics import mean

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[3]
DERIVED = BASE / "artifacts/derived"


def quadrant(x, y):
    return f"Q{int(x >= 5) + 2 * int(y >= 5)}"


def summarize_farm(farm):
    rows = {f"Q{q}": Counter() for q in range(4)}
    for y, line in enumerate(farm["tiles"]):
        for x, tile in enumerate(line):
            row = rows[quadrant(x, y)]
            if tile == "LOCKED":
                row["locked"] += 1
                continue
            row["unlocked"] += 1
            if tile is None:
                row["empty"] += 1
            elif isinstance(tile, dict):
                kind = tile.get("kind")
                if kind == "PLANT":
                    row["crops"] += 1
                    row[tile["crop"]] += 1
                elif kind == "PASTURE":
                    row["pastures"] += 1
                    if tile.get("animal"):
                        row["occupied_pastures"] += 1
                        row[tile["animal"]] += 1
                    else:
                        row["empty_pastures"] += 1
                elif kind == "WEED":
                    row["weeds"] += 1
                else:
                    raise AssertionError(tile)
            else:
                raise AssertionError(tile)
    for row in rows.values():
        assert row["unlocked"] + row["locked"] == 25
        assert row["crops"] + row["pastures"] + row["empty"] + row["weeds"] == row["unlocked"]
    return rows


def span(values):
    return dict(mean=mean(values), minimum=min(values), maximum=max(values))


def main():
    plan_path = DERIVED / "E18_28_FULL_SEASON_C_PLAN_V1.json"
    plan = json.loads(plan_path.read_text())
    corpus = json.loads((DERIVED / "E18_31_EXTERNAL_SUBMISSION_FIRST6_20260906.json").read_text())
    profiles = []
    for profile in corpus["profiles"]:
        path = ROOT / f"data/replays/json/{profile['episode_id']}.json"
        assert hashlib.sha256(path.read_bytes()).hexdigest() == profile["sha256"]
        replay = json.loads(path.read_text())
        seat = profile["seat"]
        days = []
        tile_events = []
        for day in range(1, 31):
            obs = replay["steps"][day * 24 - 1][seat]["observation"]
            assert (obs["day"] + 1, obs["hour"] + 1) == (day, 24)
            farm = obs["farms"][seat]
            actions, pass_at, exposure = Counter(), Counter(), Counter()
            for index in range((day - 1) * 24, min(day * 24, 719)):
                before = replay["steps"][index][seat]["observation"]
                old_farm = before["farms"][seat]
                state = summarize_farm(old_farm)
                action = replay["steps"][index + 1][seat]["action"]
                for worker, cmd in enumerate([action["farmer"], *action["hands"]]):
                    actions[cmd[0]] += 1
                    position = old_farm["farmer"] if worker == 0 else old_farm["hands"][worker - 1]
                    if cmd[0] == "PASS":
                        pass_at[quadrant(*position)] += 1
                        if state["Q0"]["crops"] + state["Q0"]["occupied_pastures"] == 25:
                            exposure["passes_with_q0_fully_occupied"] += 1
                for q in ("Q0", "Q1", "Q2"):
                    exposure[f"{q}_empty_tile_hours"] += state[q]["empty"]
                after = replay["steps"][index + 1][seat]["observation"]["farms"][seat]
                for x, y in ((3, 4), (4, 4), (2, 4), (0, 0)):
                    previous, current = old_farm["tiles"][y][x], after["tiles"][y][x]
                    def label(tile):
                        return (tile.get("kind"), tile.get("animal"), tile.get("crop")) if isinstance(tile, dict) else tile
                    if label(previous) != label(current):
                        tile_events.append(dict(day=before["day"] + 1, hour=before["hour"] + 1,
                                                coord=[x, y], before=label(previous), after=label(current)))
            days.append(dict(day=day, cash=farm["money"], hands=len(farm["hands"]),
                             quadrants=summarize_farm(farm), actions=actions,
                             pass_worker_location=pass_at, exposure=exposure))
        profiles.append(dict(episode_id=profile["episode_id"], seed=profile["seed"],
                             replay_sha256=profile["sha256"], daily=days, tile_events=tile_events))
    metrics = ("pastures", "occupied_pastures", "crops", "empty", "weeds", "COW", "SHEEP", "MELON", "WHEAT", "STRAWBERRY")
    daily = []
    for day in range(1, 31):
        rows = [p["daily"][day - 1] for p in profiles]
        daily.append(dict(day=day,
            quadrants={q: {m: span([r["quadrants"][q][m] for r in rows]) for m in metrics} for q in ("Q0", "Q1", "Q2")},
            cash=span([r["cash"] for r in rows]), PASS=span([r["actions"]["PASS"] for r in rows]),
            passes_with_q0_fully_occupied=span([r["exposure"]["passes_with_q0_fully_occupied"] for r in rows])))
    # Replay the planner's intended tile state without claiming engine execution parity.
    intended, plan_days = {}, []
    for day in range(1, 17):
        rows = [r for r in plan["trajectory"] if r["day"] == day]
        for r in sorted(rows, key=lambda r: (r["turn"], r["worker"])):
            c, op, args = tuple(r["position"]), r["opcode"], r["arguments"]
            if op == "PLANT":
                intended[c] = ("PLANT", args["crop"])
            elif op == "BUILD_PASTURE":
                intended[c] = ("PASTURE", None)
            elif op == "PLACE":
                intended[c] = ("PASTURE", args["animal"])
            elif op == "DIG" or (op == "HARVEST" and intended.get(c, (None, None))[1] in {"WHEAT", "MELON", "CARROT"}):
                intended.pop(c, None)
        counts = Counter(s[0] for c, s in intended.items() if quadrant(*c) == "Q0")
        plan_days.append(dict(day=day, crops=counts["PLANT"], pastures=counts["PASTURE"], empty=25-sum(counts.values())))
    output = DERIVED / "E18_32_Q0_UTILIZATION_AUDIT_20260906.json"
    assert not output.exists()
    payload = dict(submission_id=56050866, source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   plan_sha256=hashlib.sha256(plan_path.read_bytes()).hexdigest(),
                   screenshot_seed=1541058082, screenshot_seed_present_in_corpus=False,
                   snapshot_convention="Observation Dn H24 (index 24*n-1), before the final action of that day; D30 H24 is terminal.",
                   role="DIAGNOSTIC_ONLY_NOT_COUNTERFACTUAL", daily=daily, profiles=profiles, intended_plan_q0=plan_days)
    assert all(p["seed"] != payload["screenshot_seed"] for p in profiles)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    for d in daily[:16]:
        print(d["day"], {q: {k: d["quadrants"][q][k] for k in ("pastures", "crops", "empty")} for q in ("Q0", "Q1", "Q2")}, "PASS", d["PASS"])
    rows = [d for p in profiles for d in p["daily"][4:10]]
    print("D5-D10", sum(d["actions"]["PASS"] for d in rows), "PASS; full Q0 at emission", sum(d["exposure"]["passes_with_q0_fully_occupied"] for d in rows))
    print("INTENDED", plan_days)
    print(output)


if __name__ == "__main__":
    main()
