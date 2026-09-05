"""Read-only paired diagnostic: distinguish water deaths from weed checkpoints."""

import importlib
import argparse
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

from kaggle_environments import make

from docs.model_specs.codex.e18.tools.e18_29_anti_pass_controller import (
    AntiPassController,
)
from docs.model_specs.codex.e18.tools.run_e18_29_anti_pass_gate import (
    DERIVED,
    PLAN,
    FullSeasonController,
    opponent_policy,
)


def run(variant):
    seed, seat = 180903001, 0
    plan = json.loads(PLAN.read_text())
    agent = FullSeasonController(plan, seat) if variant == "PARENT" else AntiPassController(plan, seat, variant)
    other = opponent_policy("E18.16", seed, 1)
    engine = importlib.import_module("kaggle_environments.envs.kaggriculture.kaggriculture")
    original = engine._daily_refresh_plants
    calls = 0
    events = []

    def refresh(farm, day, turns):
        nonlocal calls
        current_seat = calls % 2
        calls += 1
        plants = {(x, y): deepcopy(tile) for y, row in enumerate(farm["tiles"]) for x, tile in enumerate(row)
                  if isinstance(tile, dict) and tile.get("kind") == "PLANT"} if current_seat == seat else {}
        original(farm, day, turns)
        for (x, y), before in plants.items():
            after = farm["tiles"][y][x]
            if isinstance(after, dict) and after.get("kind") == "WEED":
                events.append(dict(service_day=day+1, displayed_after_day=day+2, position=[x, y], before=before,
                                   water_starvation=not before.get("watered_today") and before.get("consecutive_unwatered", 0) >= 1))

    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24}, debug=False)
    engine._daily_refresh_plants = refresh
    try:
        env.run([agent, other])
    finally:
        engine._daily_refresh_plants = original
    replay = env.toJSON()
    for event in events:
        coord, day = event["position"], event["service_day"]
        event["planned_on_tile"] = [r for r in plan["trajectory"] if day-1 <= r["day"] <= day and r["position"] == coord and r["opcode"] not in ("NORTH", "SOUTH", "EAST", "WEST", "PASS")]
        event["requested_on_tile"] = []
        for idx in range(max(1, (day-2)*24+1), min(day*24+1, len(replay["steps"]))):
            obs = replay["steps"][idx-1][seat]["observation"]
            action = replay["steps"][idx][seat]["action"] or {}
            farm = obs["farms"][seat]
            commands = [action.get("farmer", ["PASS"]), *action.get("hands", [])]
            for worker, (pos, command) in enumerate(zip([farm["farmer"], *farm["hands"]], commands)):
                if pos == coord and command[0] not in ("NORTH", "SOUTH", "EAST", "WEST", "PASS"):
                    event["requested_on_tile"].append(dict(day=obs["day"]+1, turn=obs["hour"]+1, worker=worker, command=command))
    worker_trace = []
    for index in range(1, len(replay["steps"])):
        obs = replay["steps"][index-1][seat]["observation"]
        if obs["day"] != 20:
            continue
        action = replay["steps"][index][seat]["action"] or {}
        farm, private = obs["farms"][seat], obs["private"]
        worker_trace.append(dict(day=21, turn=obs["hour"]+1, farmer_position=farm["farmer"],
                                hands=farm["hands"], shed_wheat=private["shed"].get("WHEAT", 0),
                                worker11_inventory=private["inventories"][11] if len(private["inventories"])>11 else None,
                                worker11_command=action.get("hands", [])[10] if len(action.get("hands", []))>10 else None,
                                market=action.get("market", [])))
    return dict(variant=variant, seed=seed, seat=seat, reward=replay["rewards"][seat], refresh_calls=calls, crop_deaths=events, worker11_d21=worker_trace)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="CROP_SERVICE_DIAGNOSIS")
    args = parser.parse_args()
    assert args.label.replace("_", "").isalnum()
    output = DERIVED / f"E18_29_ANTI_PASS_{args.label}.json"
    assert not output.exists(), output
    with ProcessPoolExecutor(max_workers=2) as pool:
        profiles = list(pool.map(run, ["PARENT", "B"]))
    output.write_text(json.dumps(dict(complete=True, matches=profiles), indent=2)+"\n", encoding="utf-8")
    print(json.dumps([{k:v for k,v in p.items() if k not in ("worker11_d21", "crop_deaths")} for p in profiles]), flush=True)
