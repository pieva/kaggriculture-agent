"""Build benchmark registry and daily timelines from Kaggriculture replay JSON.

This is an analysis-only tool: it reads replay files and writes benchmark
artifacts under results/benchmark without touching strategy or submission code.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_DIR = ROOT / "docs" / "benchmark"
OUT_DIR = ROOT / "results" / "benchmark"

PRODUCTIVE_ACTIONS = {
    "PLANT",
    "WATER",
    "DIG",
    "HARVEST",
    "FEED",
    "CARE",
    "COLLECT_FERTILIZER",
    "BUILD_PASTURE",
    "BUILD_COOP",
    "PICKUP",
    "PLACE",
    "DROP",
    "FERTILIZE",
}
MOVEMENT_ACTIONS = {"NORTH", "SOUTH", "EAST", "WEST"}
MARKET_ACTIONS = {"SELL", "BUY", "HIRE", "BUY_LAND"}
LIVESTOCK = {"COW", "SHEEP", "GOOSE"}
INVENTORY_KEYS = {
    "WHEAT",
    "MELON",
    "STRAWBERRY",
    "MILK",
    "WOOL",
    "EGG",
    "FERTILIZER",
    "COW",
    "SHEEP",
    "GOOSE",
}


def stable_dumps(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def scalar_name(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("type", "name", "kind", "item"):
            if key in value:
                return scalar_name(value[key])
    return str(value)


def iter_positions(container: Any) -> list[Any]:
    if container is None:
        return []
    if isinstance(container, dict):
        return list(container.values())
    if isinstance(container, list):
        if container and all(isinstance(row, list) for row in container):
            return [item for row in container for item in row]
        return container
    return []


def tile_kind(tile: Any) -> str:
    if not isinstance(tile, dict):
        return ""
    for key in ("type", "kind", "item", "object", "entity"):
        name = scalar_name(tile.get(key)).upper()
        if name:
            return name
    return ""


def item_counter(value: Any) -> Counter:
    counts: Counter = Counter()
    if not value:
        return counts
    if isinstance(value, dict):
        for key, raw in value.items():
            name = scalar_name(key).upper()
            if isinstance(raw, (int, float)):
                counts[name] += int(raw)
            elif isinstance(raw, list):
                counts[name] += len(raw)
            elif isinstance(raw, dict):
                nested_name = scalar_name(raw.get("type") or raw.get("kind") or raw.get("item")).upper()
                if nested_name:
                    counts[nested_name] += int(raw.get("amount", raw.get("quantity", raw.get("count", 1))))
                elif name:
                    counts[name] += 1
            elif raw is not None and name:
                counts[name] += 1
        return counts
    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                name = scalar_name(item.get("type") or item.get("kind") or item.get("item")).upper()
                qty = item.get("amount", item.get("quantity", item.get("count", 1)))
                if name:
                    counts[name] += int(qty)
            else:
                name = scalar_name(item).upper()
                if name:
                    counts[name] += 1
    return counts


def farm_for(obs: dict[str, Any], player_id: int) -> dict[str, Any]:
    farms = obs.get("farms", [])
    if isinstance(farms, dict):
        return farms.get(str(player_id), farms.get(player_id, {})) or {}
    if isinstance(farms, list) and player_id < len(farms):
        return farms[player_id] or {}
    return {}


def private_for(player_step: dict[str, Any]) -> dict[str, Any]:
    obs = player_step.get("observation") or {}
    private = obs.get("private") or obs.get("player") or {}
    return private if isinstance(private, dict) else {}


def farm_metrics(farm: dict[str, Any], private: dict[str, Any] | None = None) -> dict[str, Any]:
    tiles = iter_positions(farm.get("tiles") or farm.get("field") or farm.get("map"))
    kind_counts: Counter = Counter()
    for tile in tiles:
        if isinstance(tile, dict):
            kind = tile_kind(tile).upper()
            if kind:
                kind_counts[kind] += 1
            for key in ("crop", "plant", "animal"):
                nested = scalar_name(tile.get(key)).upper()
                if nested:
                    kind_counts[nested] += 1
        else:
            kind = scalar_name(tile).upper()
            if kind:
                kind_counts[kind] += 1

    hands = farm.get("hands", [])
    if isinstance(hands, dict):
        hand_count = len(hands)
    elif isinstance(hands, list):
        hand_count = len(hands)
    else:
        hand_count = int(farm.get("hand_count", farm.get("hands_count", 0)) or 0)

    quadrants = farm.get("unlocked_quadrants") or farm.get("quadrants") or []
    if isinstance(quadrants, dict):
        quadrants = [key for key, enabled in quadrants.items() if enabled]

    inventory = Counter()
    if private:
        for key in ("inventory", "inventories", "shed", "storage", "seeds"):
            inventory.update(item_counter(private.get(key)))

    livestock = Counter()
    for animal in LIVESTOCK:
        livestock[animal] += kind_counts.get(animal, 0) + inventory.get(animal, 0)

    crop_tiles = sum(kind_counts[item] for item in ("WHEAT", "MELON", "STRAWBERRY", "PUMPKIN", "CORN"))
    pasture_tiles = kind_counts.get("PASTURE", 0)
    coop_tiles = kind_counts.get("COOP", 0)
    productive_tiles = crop_tiles + pasture_tiles + coop_tiles
    weeds = kind_counts.get("WEED", 0) + kind_counts.get("WEEDS", 0)

    visible_inventory = {key: inventory[key] for key in sorted(INVENTORY_KEYS) if inventory[key]}
    return {
        "cash": int(farm.get("money", farm.get("cash", 0)) or 0),
        "hands": hand_count,
        "quadrants": list(quadrants) if isinstance(quadrants, list) else [],
        "crop_tiles": crop_tiles,
        "pasture_tiles": pasture_tiles,
        "coop_tiles": coop_tiles,
        "productive_tiles": productive_tiles,
        "weeds": weeds,
        "livestock": {key: livestock[key] for key in sorted(LIVESTOCK) if livestock[key]},
        "inventory": visible_inventory,
    }


def parse_action(action: Any) -> list[dict[str, Any]]:
    if action in (None, "", []):
        return []
    if isinstance(action, str):
        return [{"verb": action.upper(), "item": "", "qty": 1}]
    if isinstance(action, dict):
        if any(key in action for key in ("farmer", "hands", "market")):
            parsed: list[dict[str, Any]] = []
            for key in ("farmer", "hands", "market"):
                parsed.extend(parse_action(action.get(key)))
            return parsed
        raw_actions = action.get("actions") or action.get("orders") or action.get("commands")
        if isinstance(raw_actions, list):
            return [parsed for item in raw_actions for parsed in parse_action(item)]
        verb = scalar_name(action.get("type") or action.get("action") or action.get("command") or action.get("verb")).upper()
        item = scalar_name(action.get("item") or action.get("resource") or action.get("crop") or action.get("animal")).upper()
        qty = action.get("quantity", action.get("amount", action.get("count", 1)))
        try:
            qty = int(qty)
        except (TypeError, ValueError):
            qty = 1
        return [{"verb": verb, "item": item, "qty": qty, "raw": action}]
    if isinstance(action, list):
        parsed: list[dict[str, Any]] = []
        if action and isinstance(action[0], str):
            verb = action[0].upper()
            item = scalar_name(action[1]).upper() if len(action) > 1 else ""
            qty = action[2] if len(action) > 2 and isinstance(action[2], int) else 1
            return [{"verb": verb, "item": item, "qty": qty, "raw": action}]
        for item in action:
            parsed.extend(parse_action(item))
        return parsed
    return []


def summarize_actions(actions: list[dict[str, Any]]) -> dict[str, Any]:
    categories = Counter()
    sells = Counter()
    buys = Counter()
    hires = 0
    land_buys = 0
    for action in actions:
        verb = action.get("verb", "")
        item = action.get("item", "")
        qty = int(action.get("qty", 1) or 1)
        if verb in PRODUCTIVE_ACTIONS:
            categories["productive"] += 1
        elif verb in MOVEMENT_ACTIONS:
            categories["movement"] += 1
        elif verb == "PASS":
            categories["pass"] += 1
        elif verb in MARKET_ACTIONS or verb == "BUY_SEED":
            categories[verb.lower()] += 1
        else:
            categories["other"] += 1
        if verb == "SELL":
            sells[item or "UNKNOWN"] += qty
        elif verb in {"BUY", "BUY_SEED"}:
            buys[item or "UNKNOWN"] += qty
        elif verb == "HIRE":
            hires += qty
        elif verb == "BUY_LAND":
            land_buys += qty
    return {
        "productive_actions": categories["productive"],
        "movement_actions": categories["movement"],
        "pass_actions": categories["pass"],
        "hires": hires,
        "land_buys": land_buys,
        "sells": dict(sells),
        "buys": dict(buys),
        "categories": dict(categories),
    }


def player_names(info: dict[str, Any]) -> list[str]:
    names = info.get("TeamNames") or []
    if not names and isinstance(info.get("Agents"), list):
        names = [agent.get("Name", "") for agent in info["Agents"]]
    return [scalar_name(name) for name in names]


def analyze_replay(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    info = raw.get("info", {})
    names = player_names(info)
    rewards = raw.get("rewards", [])
    steps = raw.get("steps", [])

    per_player_daily: dict[tuple[int, int], dict[str, Any]] = {}
    player_rollups: dict[int, dict[str, Any]] = defaultdict(
        lambda: {
            "peak_hands": 0,
            "peak_crop_tiles": 0,
            "peak_productive_tiles": 0,
            "weed_tile_days": 0,
            "sells": Counter(),
            "buys": Counter(),
            "actions": Counter(),
            "first_q2": None,
            "q2_pre_state": None,
            "q2_post_cash": None,
            "final_metrics": {},
        }
    )
    timeline: list[dict[str, Any]] = []
    q2_events: list[dict[str, Any]] = []

    previous_quadrants: dict[int, int] = defaultdict(int)
    for step_index, step in enumerate(steps):
        if not isinstance(step, list):
            continue
        day = step_index // 24 + 1
        hour = step_index % 24
        for player_id, player_step in enumerate(step):
            if not isinstance(player_step, dict):
                continue
            obs = player_step.get("observation") or {}
            farm = farm_for(obs, player_id)
            private = private_for(player_step)
            metrics = farm_metrics(farm, private)
            parsed_actions = parse_action(player_step.get("action"))
            action_summary = summarize_actions(parsed_actions)
            rollup = player_rollups[player_id]
            rollup["peak_hands"] = max(rollup["peak_hands"], metrics["hands"])
            rollup["peak_crop_tiles"] = max(rollup["peak_crop_tiles"], metrics["crop_tiles"])
            rollup["peak_productive_tiles"] = max(rollup["peak_productive_tiles"], metrics["productive_tiles"])
            rollup["sells"].update(action_summary["sells"])
            rollup["buys"].update(action_summary["buys"])
            rollup["actions"].update(action_summary["categories"])
            if hour == 23:
                rollup["weed_tile_days"] += metrics["weeds"]

            quadrant_count = len(metrics["quadrants"])
            if quadrant_count >= 3 and previous_quadrants[player_id] < 3 and rollup["first_q2"] is None:
                rollup["first_q2"] = day
                rollup["q2_pre_state"] = {
                    "day": day,
                    "hour": hour,
                    "cash": metrics["cash"],
                    "hands": metrics["hands"],
                    "quadrants": metrics["quadrants"],
                    "crop_tiles": metrics["crop_tiles"],
                    "pasture_tiles": metrics["pasture_tiles"],
                    "productive_tiles": metrics["productive_tiles"],
                    "weeds": metrics["weeds"],
                }
                rollup["q2_post_cash"] = metrics["cash"]
                q2_events.append({"player_id": player_id, "name": names[player_id] if player_id < len(names) else str(player_id), **rollup["q2_pre_state"]})
            previous_quadrants[player_id] = max(previous_quadrants[player_id], quadrant_count)

            day_key = (day, player_id)
            per_player_daily[day_key] = {
                "episode_id": info.get("EpisodeId", raw.get("id", path.stem)),
                "seed": info.get("seed"),
                "day": day,
                "hour": hour,
                "player_id": player_id,
                "player_name": names[player_id] if player_id < len(names) else str(player_id),
                **metrics,
                **action_summary,
            }
            rollup["final_metrics"] = metrics

    for (day, player_id), row in sorted(per_player_daily.items()):
        timeline.append(row)

    our_id = 0
    for idx, name in enumerate(names):
        if "pietro" in name.lower() or "valocchi" in name.lower():
            our_id = idx
            break
    competitor_id = 1 - our_id if len(names) >= 2 else 1
    our_reward = int(rewards[our_id]) if our_id < len(rewards) else None
    competitor_reward = int(rewards[competitor_id]) if competitor_id < len(rewards) else None
    our_rollup = player_rollups[our_id]
    comp_rollup = player_rollups[competitor_id]
    comp_final = comp_rollup["final_metrics"]
    our_final = our_rollup["final_metrics"]
    registry = {
        "file": str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha256": sha256_file(path),
        "episode_id": info.get("EpisodeId", raw.get("id", path.stem)),
        "seed": info.get("seed"),
        "module_version": raw.get("module_version"),
        "agents": names,
        "our_agent": names[our_id] if our_id < len(names) else str(our_id),
        "competitor": names[competitor_id] if competitor_id < len(names) else str(competitor_id),
        "our_reward": our_reward,
        "competitor_reward": competitor_reward,
        "absolute_gap": (competitor_reward - our_reward) if None not in (competitor_reward, our_reward) else None,
        "score_ratio": round(competitor_reward / our_reward, 3) if our_reward else None,
        "our": rollup_summary(our_rollup, our_final),
        "competitor_summary": rollup_summary(comp_rollup, comp_final),
        "q2_events": q2_events,
        "statuses": raw.get("statuses"),
    }
    return registry, timeline, q2_events


def rollup_summary(rollup: dict[str, Any], final_metrics: dict[str, Any]) -> dict[str, Any]:
    return {
        "final_quadrants": final_metrics.get("quadrants", []),
        "final_livestock": final_metrics.get("livestock", {}),
        "final_cash": final_metrics.get("cash"),
        "peak_hands": rollup["peak_hands"],
        "peak_crop_tiles": rollup["peak_crop_tiles"],
        "peak_productive_tiles": rollup["peak_productive_tiles"],
        "weed_tile_days": rollup["weed_tile_days"],
        "sold_products": dict(rollup["sells"].most_common()),
        "bought_products": dict(rollup["buys"].most_common()),
        "action_categories": dict(rollup["actions"].most_common()),
        "q2_day": rollup["first_q2"],
        "q2_pre_state": rollup["q2_pre_state"],
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=keys)
        writer.writeheader()
        for row in rows:
            encoded = {}
            for key, value in row.items():
                encoded[key] = stable_dumps(value) if isinstance(value, (dict, list)) else value
            writer.writerow(encoded)


def markdown_registry(registries: list[dict[str, Any]]) -> str:
    lines = [
        "# Benchmark Registry",
        "",
        "Analysis-only registry built from raw Kaggriculture replay JSON files in `docs/benchmark`.",
        "",
        "| Episode | Seed | Competitor | Our reward | Competitor reward | Gap | Ratio | Q2 competitor | Final quadrants | Livestock | Peak hands | Peak crop | Peak productive | Weed tile-days | Main sells | SHA-256 |",
        "|---|---:|---|---:|---:|---:|---:|---|---|---|---:|---:|---:|---:|---|---|",
    ]
    for reg in registries:
        comp = reg["competitor_summary"]
        livestock = ", ".join(f"{k}:{v}" for k, v in comp.get("final_livestock", {}).items()) or "none"
        sells = ", ".join(f"{k}:{v}" for k, v in list(comp.get("sold_products", {}).items())[:5]) or "none observed"
        lines.append(
            "| {episode} | {seed} | {competitor} | {our} | {comp_reward} | {gap} | {ratio} | {q2} | {quads} | {livestock} | {hands} | {crop} | {productive} | {weeds} | {sells} | `{sha}` |".format(
                episode=reg["episode_id"],
                seed=reg["seed"],
                competitor=reg["competitor"],
                our=reg["our_reward"],
                comp_reward=reg["competitor_reward"],
                gap=reg["absolute_gap"],
                ratio=reg["score_ratio"],
                q2=comp.get("q2_day") or "no",
                quads=",".join(comp.get("final_quadrants", [])),
                livestock=livestock,
                hands=comp.get("peak_hands"),
                crop=comp.get("peak_crop_tiles"),
                productive=comp.get("peak_productive_tiles"),
                weeds=comp.get("weed_tile_days"),
                sells=sells,
                sha=reg["sha256"],
            )
        )
    lines.extend(["", "## Notes", ""])
    for reg in registries:
        comp = reg["competitor_summary"]
        our = reg["our"]
        q2 = comp.get("q2_day")
        lines.append(
            "- Episode {episode}: {competitor} reaches {score} vs {ours}; Q2={q2}; peak hands {hands}; peak crop/productive {crop}/{productive}; livestock {livestock}; weed tile-days {weeds}. Our side peak hands {our_hands}, peak crop/productive {our_crop}/{our_productive}, weed tile-days {our_weeds}.".format(
                episode=reg["episode_id"],
                competitor=reg["competitor"],
                score=reg["competitor_reward"],
                ours=reg["our_reward"],
                q2=q2 or "no",
                hands=comp.get("peak_hands"),
                crop=comp.get("peak_crop_tiles"),
                productive=comp.get("peak_productive_tiles"),
                livestock=stable_dumps(comp.get("final_livestock", {})),
                weeds=comp.get("weed_tile_days"),
                our_hands=our.get("peak_hands"),
                our_crop=our.get("peak_crop_tiles"),
                our_productive=our.get("peak_productive_tiles"),
                our_weeds=our.get("weed_tile_days"),
            )
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    replay_files = sorted(BENCHMARK_DIR.glob("*.json"))
    registries: list[dict[str, Any]] = []
    all_timeline: list[dict[str, Any]] = []
    all_q2: list[dict[str, Any]] = []
    for replay in replay_files:
        registry, timeline, q2_events = analyze_replay(replay)
        registries.append(registry)
        all_timeline.extend(timeline)
        all_q2.extend({"episode_id": registry["episode_id"], **event} for event in q2_events)
        stem = str(registry["episode_id"])
        (OUT_DIR / f"{stem}_daily_timeline.json").write_text(json.dumps(timeline, indent=2, sort_keys=True), encoding="utf-8")
        write_csv(OUT_DIR / f"{stem}_daily_timeline.csv", timeline)

    (OUT_DIR / "benchmark_registry.json").write_text(json.dumps(registries, indent=2, sort_keys=True), encoding="utf-8")
    (OUT_DIR / "BENCHMARK_REGISTRY.md").write_text(markdown_registry(registries), encoding="utf-8")
    (OUT_DIR / "benchmark_daily_timeline.json").write_text(json.dumps(all_timeline, indent=2, sort_keys=True), encoding="utf-8")
    write_csv(OUT_DIR / "benchmark_daily_timeline.csv", all_timeline)
    (OUT_DIR / "q2_evidence.json").write_text(json.dumps(all_q2, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"replays": len(registries), "output": str(OUT_DIR)}, indent=2))


if __name__ == "__main__":
    main()
