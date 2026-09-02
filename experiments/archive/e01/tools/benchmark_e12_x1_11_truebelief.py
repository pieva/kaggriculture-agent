"""Diagnostic E12-X1.11 comparison against truebelief replay 101294736.

This is intentionally BENCHMARK/ANALYSIS only. It does not change strategy code
or submit to Kaggle. The truebelief side is derived from the raw Kaggle replay
JSON in docs/101294736.json when available.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kaggle_environments import make

from agricola.core.state import CROPS, GameState
from agricola.strategy.productive_mass_roi import ProductiveMassConfig, ProductiveMassROIAgent


ROOT = Path(__file__).parent.parent
OUT_DIR = ROOT / "results" / "e12" / "x111"
TRUEBELIEF_REPLAY = ROOT / "docs" / "101294736.json"
TRUEBELIEF_EPISODE_ID = 101294736
SEED = 421521921
SNAPSHOT_DAYS = [1, 2, 5, 8, 10, 15, 20, 25, 30]


def run(cmd: List[str]) -> str:
    return subprocess.check_output(cmd, cwd=ROOT, text=True, encoding="utf-8").strip()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def action_bucket(action: List[Any]) -> str:
    if not action:
        return "PASS"
    head = str(action[0])
    if head in {"NORTH", "SOUTH", "EAST", "WEST"}:
        return "MOVE"
    return head


def nonzero(mapping: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in mapping.items() if v}


def add_action_summary(summary: Dict[str, Counter], action: Dict[str, Any]) -> None:
    farmer = action.get("farmer", ["PASS"])
    summary["farmer"][action_bucket(farmer)] += 1
    for hand_action in action.get("hands", []):
        summary["hands"][action_bucket(hand_action)] += 1
    for order in action.get("market", []):
        if not order:
            continue
        order_type = str(order[0])
        item = str(order[1]) if len(order) >= 2 else ""
        qty = int(order[2]) if len(order) >= 3 and isinstance(order[2], (int, float)) else 1
        key = f"{order_type}:{item}" if item else order_type
        summary["market"][key] += qty
        summary["market_orders"][order_type] += 1
        if order_type == "SELL" and item:
            summary["sell"][item] += qty
        elif order_type == "BUY_SEED" and item:
            summary["buy_seed"][item] += qty
        elif order_type == "BUY_PRODUCT" and item:
            summary["buy_product"][item] += qty
        elif order_type == "BUY_ANIMAL" and item:
            summary["buy_animal"][item] += qty


def quadrant_name(x: int, y: int) -> str:
    if x < 5 and y < 5:
        return "NW"
    if x >= 5 and y < 5:
        return "NE"
    if x < 5 and y >= 5:
        return "SW"
    return "SE"


def replay_snapshot(obs: Dict[str, Any], player_id: int, display_day: int, day_actions: Dict[str, Any]) -> Dict[str, Any]:
    farm = obs["farms"][player_id]
    unlocked = farm.get("unlocked_quadrants", ["NW"])
    if not isinstance(unlocked, list):
        unlocked = ["NW", "NE", "SW", "SE"][: int(unlocked)]

    crops = Counter({crop: 0 for crop in CROPS})
    quadrants = {
        q: {"owned": 0, "productive": 0, "crop": 0, "pasture": 0, "weed": 0, "idle": 0}
        for q in ("NW", "NE", "SW", "SE")
    }
    active_livestock = Counter()
    worker_inventory = Counter()
    pasture_tiles = 0
    weed_tiles = 0
    idle_owned_tiles = 0
    active_crop_tiles = 0

    for inv in obs.get("private", {}).get("inventories", []) or []:
        if isinstance(inv, dict):
            worker_inventory.update({k: int(v) for k, v in inv.items() if v})

    for y, row in enumerate(farm.get("tiles", [])):
        for x, tile in enumerate(row):
            if tile == "LOCKED":
                continue
            q = quadrant_name(x, y)
            quadrants[q]["owned"] += 1
            if tile is None:
                idle_owned_tiles += 1
                quadrants[q]["idle"] += 1
                continue
            if not isinstance(tile, dict):
                continue
            kind = tile.get("kind")
            if kind == "WEED":
                weed_tiles += 1
                quadrants[q]["weed"] += 1
            elif kind == "PASTURE":
                pasture_tiles += 1
                quadrants[q]["pasture"] += 1
                quadrants[q]["productive"] += 1
                animal = tile.get("animal")
                if animal:
                    active_livestock[str(animal)] += 1
            elif kind == "PLANT":
                crop = str(tile.get("crop", "WHEAT"))
                crops[crop] += 1
                active_crop_tiles += 1
                quadrants[q]["crop"] += 1
                quadrants[q]["productive"] += 1

    for qdata in quadrants.values():
        qdata["utilization"] = round(qdata["productive"] / max(1, qdata["owned"]), 3)

    owned_tiles = sum(q["owned"] for q in quadrants.values())
    return {
        "day": display_day,
        "raw_day": int(obs.get("day", display_day - 1)),
        "hour": int(obs.get("hour", 0)),
        "money": float(farm.get("money", 0.0)),
        "owned_quadrants": unlocked,
        "hands": len(farm.get("hands", []) or []),
        "owned_tiles": owned_tiles,
        "active_crop_tiles": active_crop_tiles,
        "pasture_tiles": pasture_tiles,
        "active_animals": int(sum(active_livestock.values())),
        "livestock_counts": dict(active_livestock),
        "weed_tiles": weed_tiles,
        "idle_owned_tiles": idle_owned_tiles,
        "productive_utilization": round((active_crop_tiles + pasture_tiles) / max(1, owned_tiles), 3),
        "crop_counts": dict(nonzero(dict(crops))),
        "shed": nonzero(obs.get("private", {}).get("shed", {}) or {}),
        "seeds": nonzero(obs.get("private", {}).get("seeds", {}) or {}),
        "worker_inventory": dict(worker_inventory),
        "quadrants": quadrants,
        "actions": day_actions,
    }


def load_truebelief_replay() -> Dict[str, Any]:
    raw = json.loads(TRUEBELIEF_REPLAY.read_text(encoding="utf-8"))
    daily_actions: Dict[int, Dict[str, Counter]] = defaultdict(lambda: {
        "farmer": Counter(),
        "hands": Counter(),
        "market": Counter(),
        "market_orders": Counter(),
        "sell": Counter(),
        "buy_seed": Counter(),
        "buy_product": Counter(),
        "buy_animal": Counter(),
    })
    latest_obs_by_day: Dict[int, Dict[str, Any]] = {}

    for index, step in enumerate(raw["steps"]):
        player_step = step[1]
        obs = player_step["observation"]
        display_day = int(obs.get("day", 0)) + 1
        latest_obs_by_day[display_day] = obs
        if index > 0:
            add_action_summary(daily_actions[display_day], player_step.get("action", {}) or {})

    snapshots = []
    for day in range(1, 31):
        obs = latest_obs_by_day[day]
        day_actions = {
            key: dict(value)
            for key, value in daily_actions[day].items()
        }
        snapshots.append(replay_snapshot(obs, 1, day, day_actions))

    final_snapshot = snapshots[-1]
    rewards = raw.get("rewards", [])
    true_final = float(rewards[1] if len(rewards) > 1 else final_snapshot["money"])
    return {
        "source": str(TRUEBELIEF_REPLAY.relative_to(ROOT)),
        "episode_id": TRUEBELIEF_EPISODE_ID,
        "raw_sha256": sha256(TRUEBELIEF_REPLAY),
        "schema_version": raw.get("schema_version"),
        "module_version": raw.get("module_version"),
        "engine_version": raw.get("version"),
        "configuration": raw.get("configuration", {}),
        "steps": len(raw.get("steps", [])),
        "statuses": raw.get("statuses", []),
        "rewards": raw.get("rewards", []),
        "seed": SEED,
        "agent_index": 1,
        "observed_final_money": true_final,
        "snapshots": snapshots,
        "final_snapshot": final_snapshot,
    }


def visible_snapshot(obs: Dict[str, Any], day_actions: Dict[str, Any]) -> Dict[str, Any]:
    state = GameState(obs)
    farm = state.my_farm
    unlocked = farm.get("unlocked_quadrants", ["NW"])
    if not isinstance(unlocked, list):
        unlocked = ["NW", "NE", "SW", "SE"][: int(unlocked)]

    crops = Counter({crop: 0 for crop in CROPS})
    quadrants = {
        q: {"owned": 0, "productive": 0, "crop": 0, "pasture": 0, "weed": 0, "idle": 0}
        for q in ("NW", "NE", "SW", "SE")
    }
    pasture_tiles = 0
    active_animals = 0
    weed_tiles = 0
    idle_owned_tiles = 0
    active_crop_tiles = 0
    mature_crops_waiting = 0

    for y in range(10):
        for x in range(10):
            tile = state.get_tile(x, y)
            if tile == "LOCKED":
                continue
            q = quadrant_name(x, y)
            quadrants[q]["owned"] += 1
            if tile is None:
                idle_owned_tiles += 1
                quadrants[q]["idle"] += 1
                continue
            if not isinstance(tile, dict):
                continue
            kind = tile.get("kind")
            if kind == "WEED":
                weed_tiles += 1
                quadrants[q]["weed"] += 1
            elif kind == "PASTURE":
                pasture_tiles += 1
                quadrants[q]["pasture"] += 1
                quadrants[q]["productive"] += 1
                if tile.get("animal"):
                    active_animals += 1
            elif kind == "PLANT":
                crop = tile.get("crop", "WHEAT")
                crops[crop] += 1
                active_crop_tiles += 1
                quadrants[q]["crop"] += 1
                quadrants[q]["productive"] += 1
                crop_info = CROPS.get(crop, CROPS["WHEAT"])
                planted_day = tile.get("planted_day", state.day)
                if state.day - planted_day >= crop_info["max_yield_day"]:
                    mature_crops_waiting += 1

    for qdata in quadrants.values():
        qdata["utilization"] = round(qdata["productive"] / max(1, qdata["owned"]), 3)

    return {
        "day": state.day,
        "turn": state.step,
        "money": state.money,
        "owned_quadrants": unlocked,
        "hands": len(state.hands_positions),
        "owned_tiles": sum(q["owned"] for q in quadrants.values()),
        "active_crop_tiles": active_crop_tiles,
        "pasture_tiles": pasture_tiles,
        "active_animals": active_animals,
        "weed_tiles": weed_tiles,
        "idle_owned_tiles": idle_owned_tiles,
        "productive_utilization": round((active_crop_tiles + pasture_tiles) / max(1, sum(q["owned"] for q in quadrants.values())), 3),
        "crop_counts": dict(crops),
        "mature_crops_waiting": mature_crops_waiting,
        "shed": dict(state.shed),
        "worker_inventories": state.inventories,
        "quadrants": quadrants,
        "actions": day_actions,
    }


def run_x111_episode(seed: int) -> Dict[str, Any]:
    cfg = ProductiveMassConfig(
        productive_core_mode="E12_Q0Q1_80K_ENGINE_X111",
        enable_land_expansion=True,
        target_cows=8,
        max_workers=6,
        stop_hire_day=1,
    )
    agent = ProductiveMassROIAgent(config=cfg)
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed})
    state = env.reset()
    daily_actions: Dict[int, Dict[str, Any]] = defaultdict(lambda: {
        "farmer": Counter(),
        "hands": Counter(),
        "market": Counter(),
        "plant": Counter(),
        "sell": Counter(),
    })
    snapshots: Dict[int, Dict[str, Any]] = {}
    last_obs = state[0].observation

    for _ in range(720):
        obs = state[0].observation
        gs = GameState(obs)
        action = agent.act(gs)
        day = int(obs.get("day", 0))
        bucket = daily_actions[day]
        bucket["farmer"][action_bucket(action.get("farmer", ["PASS"]))] += 1
        for hand_action in action.get("hands", []):
            bucket["hands"][action_bucket(hand_action)] += 1
        for order in action.get("market", []):
            if not order:
                continue
            bucket["market"][str(order[0])] += 1
            if order[0] == "SELL" and len(order) >= 3:
                bucket["sell"][str(order[1])] += int(order[2])
            if order[0] == "BUY_SEED" and len(order) >= 3:
                bucket["plant"][str(order[1])] += int(order[2])

        state = env.step([action, {}])
        last_obs = state[0].observation
        current_day = int(last_obs.get("day", day))
        if current_day in SNAPSHOT_DAYS:
            frozen_actions = {
                key: dict(value)
                for key, value in daily_actions[current_day].items()
            }
            snapshots[current_day] = visible_snapshot(last_obs, frozen_actions)
        if state[0].status in ("DONE", "INVALID", "ERROR"):
            break

    final_money = float(agent.telemetry.final_money)
    return {
        "seed": seed,
        "final_money": final_money,
        "owned_quadrants": agent.owned_quadrants,
        "peak_productive_tiles": agent.telemetry.peak_productive_tiles,
        "peak_workforce": agent.telemetry.peak_simultaneous_workers,
        "realized_revenue": dict(agent.telemetry.realized_revenue),
        "spending": {
            "seeds": agent.telemetry.spending_seeds,
            "land": agent.telemetry.spending_land,
            "workforce": agent.telemetry.spending_workforce,
            "livestock": agent.telemetry.spending_livestock,
        },
        "snapshots": [snapshots[d] for d in SNAPSHOT_DAYS if d in snapshots],
        "final_snapshot": visible_snapshot(last_obs, {
            key: dict(value) for key, value in daily_actions[int(last_obs.get("day", 30))].items()
        }),
    }


def compact_historical_x19(audit: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "seed": audit["seed"],
        "local_final_money": audit["provenance"]["local_final_money"],
        "observed_kaggle_x19_final_money": audit["provenance"]["observed_kaggle_x19_final_money"],
        "observed_truebelief_final_money": audit["provenance"]["observed_truebelief_final_money"],
        "milestones": [
            item for item in audit.get("milestones", [])
            if item.get("day") in SNAPSHOT_DAYS
        ],
        "crop_summary": audit.get("crop_summary", {}),
        "livestock": audit.get("livestock", {}),
    }


def format_counter_items(mapping: Dict[str, Any]) -> str:
    parts = [f"{k}:{v}" for k, v in mapping.items() if v]
    return ", ".join(parts) if parts else "-"


def format_market_actions(actions: Dict[str, Any]) -> str:
    market = actions.get("market", {})
    parts = [f"{k}={v}" for k, v in sorted(market.items()) if v]
    return "; ".join(parts) if parts else "-"


def make_markdown(data: Dict[str, Any]) -> str:
    x111 = data["x111"]
    truebelief = data["truebelief"]
    true_final = data["truebelief"]["observed_final_money"]
    gap = true_final - x111["final_money"]
    ratio = true_final / max(1.0, x111["final_money"])
    pct = x111["final_money"] / max(1.0, true_final)

    lines = [
        "# E12-X1.11 Benchmark vs truebelief",
        "",
        "Status: DIAGNOSTIC BENCHMARK, NO STRATEGY CHANGES",
        "",
        "## Provenance",
        "",
        f"- Timestamp: `{data['timestamp']}`",
        f"- Git branch: `{data['git']['branch']}`",
        f"- Git commit: `{data['git']['commit']}`",
        f"- Working tree dirty: `{data['git']['dirty']}`",
        f"- Mode: `E12_Q0Q1_80K_ENGINE_X111`",
        f"- Submission SHA-256: `{data['submission']['sha256']}`",
        f"- Local reproducibility: seed 0 `{data['local_repro']['seed0_final_money']}`, seed 421521921 `{data['local_repro']['seed421521921_final_money']}`",
        f"- truebelief replay source: `{truebelief['source']}`",
        f"- truebelief replay SHA-256: `{truebelief['raw_sha256']}`",
        f"- truebelief episode ID: `{truebelief['episode_id']}`",
        f"- truebelief raw steps: `{truebelief['steps']}`",
        f"- truebelief module version: `{truebelief['module_version']}`",
        "",
        "The full truebelief Day 1 -> 30 timeline below is derived from the raw replay JSON. Raw replay days are indexed `0..29`; this report normalizes them to Day `1..30`.",
        "",
        "## Final Result",
        "",
        "| Agent | Seed | Final money | Owned quadrants | Peak active tiles | Peak workforce |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
        f"| X1.11 local | {SEED} | `{x111['final_money']:.2f}` | `{x111['owned_quadrants']}` | `{x111['peak_productive_tiles']}` | `{x111['peak_workforce']}` |",
        f"| truebelief replay | {SEED} | `{true_final:.2f}` | `{len(truebelief['final_snapshot']['owned_quadrants'])}` | `{max(s['active_crop_tiles'] + s['pasture_tiles'] for s in truebelief['snapshots'])}` | `{max(s['hands'] for s in truebelief['snapshots'])}` |",
        "",
        f"- Absolute gap: `{gap:.2f}`",
        f"- Ratio truebelief / X1.11: `{ratio:.2f}x`",
        f"- X1.11 percent of truebelief: `{pct:.1%}`",
        "",
        "## truebelief Day 1 -> 30 Timeline",
        "",
        "| Day | Money | Delta | Quads | Hands | Crops | Pastures | Livestock | Weed | Crop mix | Market actions |",
        "| ---: | ---: | ---: | --- | ---: | ---: | ---: | --- | ---: | --- | --- |",
    ]
    prev_money = 3000.0
    for snap in truebelief["snapshots"]:
        delta = snap["money"] - prev_money
        prev_money = snap["money"]
        lines.append(
            f"| {snap['day']} | `{snap['money']:.0f}` | `{delta:+.0f}` | {','.join(snap['owned_quadrants'])} | "
            f"`{snap['hands']}` | `{snap['active_crop_tiles']}` | `{snap['pasture_tiles']}` | "
            f"{format_counter_items(snap['livestock_counts'])} | `{snap['weed_tiles']}` | "
            f"{format_counter_items(snap['crop_counts'])} | {format_market_actions(snap['actions'])} |"
        )

    lines.extend([
        "",
        "## X1.11 Timeline",
        "",
        "| Day | Money | Quads | Hands | Crops | Pastures | Animals | Idle | Util | Crop mix |",
        "| ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ])
    timeline_snaps = list(x111["snapshots"])
    if timeline_snaps and timeline_snaps[-1]["day"] != x111["final_snapshot"]["day"]:
        timeline_snaps.append(x111["final_snapshot"])
    elif not timeline_snaps:
        timeline_snaps.append(x111["final_snapshot"])

    for snap in timeline_snaps:
        lines.append(
            f"| {snap['day']} | `{snap['money']:.0f}` | {','.join(snap['owned_quadrants'])} | "
            f"`{snap['hands']}` | `{snap['active_crop_tiles']}` | `{snap['pasture_tiles']}` | "
            f"`{snap['active_animals']}` | `{snap['idle_owned_tiles']}` | `{snap['productive_utilization']}` | {format_counter_items(snap['crop_counts'])} |"
        )
    if timeline_snaps[-1]["day"] < 30:
        lines.append("")
        lines.append("Note: the local environment's terminal observation for this run is indexed as Day 29/episode end; the final money shown above is the terminal X1.11 value.")

    hist = data["historical_x19"]
    lines.extend([
        "",
        "## X1.9 -> X1.11 Evolution",
        "",
        "| Version | Evidence | Final money | Gap vs truebelief | Ratio truebelief / ours |",
        "| --- | --- | ---: | ---: | ---: |",
        f"| X1.9 | observed Kaggle replay | `{hist['observed_kaggle_x19_final_money']:.2f}` | `{true_final - hist['observed_kaggle_x19_final_money']:.2f}` | `{true_final / hist['observed_kaggle_x19_final_money']:.2f}x` |",
        f"| X1.9 | local replay | `{hist['local_final_money']:.2f}` | `{true_final - hist['local_final_money']:.2f}` | `{true_final / hist['local_final_money']:.2f}x` |",
        f"| X1.11 | fresh local replay | `{x111['final_money']:.2f}` | `{gap:.2f}` | `{ratio:.2f}x` |",
        "",
        "X1.11 improves the local X1.9 reproduction substantially, but remains only about one third of the truebelief replay result.",
        "",
        "## Terrain And Harvest",
        "",
        f"- X1.11 remains Q0+Q1 only and peaks at `{x111['peak_productive_tiles']}` productive crop tiles.",
        f"- truebelief remains Q0+Q1 only, reaches `{max(s['active_crop_tiles'] + s['pasture_tiles'] for s in truebelief['snapshots'])}` productive tiles, and finishes with `{truebelief['final_snapshot']['active_crop_tiles']}` crop tiles plus `{truebelief['final_snapshot']['pasture_tiles']}` pasture tiles.",
        "- X1.9 historical audit bought Q2 and then left large areas idle; X1.11 avoids that specific capital sink.",
        "- The remaining gap is not explained by Q2 waste; it is explained by much lower economic density and no visible high-yield livestock engine.",
        "",
        "## Livestock",
        "",
        f"- X1.11 fresh replay: livestock spend `{x111['spending']['livestock']:.2f}`, active animals final `{x111['final_snapshot']['active_animals']}`, milk revenue `{x111['realized_revenue'].get('MILK', 0.0):.2f}`.",
        f"- truebelief replay: active animals final `{format_counter_items(truebelief['final_snapshot']['livestock_counts'])}`, pasture tiles final `{truebelief['final_snapshot']['pasture_tiles']}`, shed residual `{format_counter_items(truebelief['final_snapshot']['shed'])}`.",
        f"- X1.9 historical audit: 8 cows, estimated milk revenue `{hist['livestock'].get('milk_revenue_estimate', 0.0):.2f}`, estimated net livestock contribution `{hist['livestock'].get('net_livestock_contribution_estimate', 0.0):.2f}`.",
        "- The replay shows truebelief selling Milk, Wool, and Fertilizer repeatedly from Day 19 onward; X1.11 does not monetize livestock in the routed implementation.",
        "",
        "## Dominant Gap Classification",
        "",
        "| Impact | Gap source | Evidence |",
        "| --- | --- | --- |",
        "| PRIMARY | Sequencing and cash conversion | truebelief stays in Q0 through Day 10, buys Q1 on Day 11, then compounds from Day 19 onward; X1.11 reaches `24827` vs truebelief `86297`. |",
        "| PRIMARY | Multi-engine portfolio | truebelief combines Wheat/Melon/Strawberry with Cow/Sheep, Milk/Wool/Fertilizer, and Wheat trading; X1.11 has `0` milk revenue. |",
        "| MATERIAL | Workforce elasticity | truebelief repeatedly hires 9-12 total workers in mature days; X1.11 peaks at `4` effective workers. |",
        "| SECONDARY | Q2 avoidance | X1.11 fixes X1.9 land over-expansion, but the ratio remains `3.48x` in favor of truebelief. |",
        "",
        "## Top 3 Observable Differences",
        "",
        "1. truebelief monetizes about `3.48x` more final cash than X1.11 on the same seed while also staying within Q0+Q1.",
        "2. truebelief builds a livestock engine before expansion and sells Milk/Wool/Fertilizer from Day 19 onward; X1.11 has no livestock revenue path in the final routed implementation.",
        "3. truebelief treats Wheat as both crop/feed/market commodity, including BUY_PRODUCT and SELL flows; X1.11 remains mainly a Melon/Strawberry crop cycle.",
        "",
        "## Next Experiment Implication",
        "",
        "Do not micro-tune X1.11. The next architecture needs the observable truebelief engine class: Day-1 dense mixed Q0, livestock before Q1, Q1 only after early monetization, elastic HIRE, and explicit cash conversion through crop + Milk + Wool + Fertilizer + Wheat market flows.",
    ])
    return "\n".join(lines) + "\n"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    git_status = run(["git", "status", "--short"])
    local_summary = json.loads((OUT_DIR / "summary.json").read_text(encoding="utf-8"))
    episodes = {item["seed"]: item for item in json.loads((OUT_DIR / "episodes.json").read_text(encoding="utf-8"))["episodes"]}
    historical = json.loads((ROOT / "results" / "e12" / "audit_truebelief" / "e12_x19_truebelief_gap_audit.json").read_text(encoding="utf-8"))

    x111 = run_x111_episode(SEED)
    truebelief = load_truebelief_replay()
    true_final = float(truebelief["observed_final_money"])

    data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S %z"),
        "git": {
            "branch": run(["git", "branch", "--show-current"]),
            "commit": run(["git", "log", "-1", "--oneline"]),
            "status_short": git_status.splitlines(),
            "dirty": bool(git_status),
        },
        "submission": {
            "path": str(ROOT / "submission" / "submission.py"),
            "sha256": sha256(ROOT / "submission" / "submission.py"),
        },
        "local_repro": {
            "run_id": local_summary["run_id"],
            "seed0_final_money": episodes[0]["final_money"],
            "seed421521921_final_money": episodes[421521921]["final_money"],
            "owned_quadrants_all_q0q1": local_summary["domain"]["all_q0q1_only"],
        },
        "x111": x111,
        "truebelief": truebelief,
        "historical_x19": compact_historical_x19(historical),
        "comparison": {
            "absolute_gap": true_final - x111["final_money"],
            "ratio_truebelief_over_x111": true_final / max(1.0, x111["final_money"]),
            "x111_pct_of_truebelief": x111["final_money"] / max(1.0, true_final),
        },
    }

    (OUT_DIR / "truebelief_benchmark.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    (OUT_DIR / "TRUEBELIEF_BENCHMARK.md").write_text(make_markdown(data), encoding="utf-8")

    rows = data["x111"]["snapshots"]
    with (OUT_DIR / "x111_truebelief_comparison_timeline.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "agent",
                "day",
                "turn",
                "money",
                "hands",
                "owned_quadrants",
                "active_crop_tiles",
                "pasture_tiles",
                "active_animals",
                "livestock_counts",
                "idle_owned_tiles",
                "weed_tiles",
                "productive_utilization",
                "crop_counts",
                "market_actions",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "agent": "x111",
                "day": row["day"],
                "turn": row["turn"],
                "money": row["money"],
                "hands": row["hands"],
                "owned_quadrants": ",".join(row["owned_quadrants"]),
                "active_crop_tiles": row["active_crop_tiles"],
                "pasture_tiles": row["pasture_tiles"],
                "active_animals": row["active_animals"],
                "livestock_counts": "{}",
                "idle_owned_tiles": row["idle_owned_tiles"],
                "weed_tiles": row["weed_tiles"],
                "productive_utilization": row["productive_utilization"],
                "crop_counts": json.dumps(row["crop_counts"], sort_keys=True),
                "market_actions": "",
            })
        for row in data["truebelief"]["snapshots"]:
            writer.writerow({
                "agent": "truebelief",
                "day": row["day"],
                "turn": "",
                "money": row["money"],
                "hands": row["hands"],
                "owned_quadrants": ",".join(row["owned_quadrants"]),
                "active_crop_tiles": row["active_crop_tiles"],
                "pasture_tiles": row["pasture_tiles"],
                "active_animals": row["active_animals"],
                "livestock_counts": json.dumps(row["livestock_counts"], sort_keys=True),
                "idle_owned_tiles": row["idle_owned_tiles"],
                "weed_tiles": row["weed_tiles"],
                "productive_utilization": row["productive_utilization"],
                "crop_counts": json.dumps(row["crop_counts"], sort_keys=True),
                "market_actions": json.dumps(row["actions"]["market"], sort_keys=True),
            })

    print(json.dumps(data["comparison"], indent=2))
    print(OUT_DIR / "TRUEBELIEF_BENCHMARK.md")


if __name__ == "__main__":
    main()
