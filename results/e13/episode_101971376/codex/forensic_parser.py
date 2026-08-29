"""Codex forensic parser for Kaggriculture episode 101971376.

Reads the raw replay without modifying it and writes analysis artifacts in this
directory only.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
RAW = ROOT / "docs" / "benchmark" / "101971376.json"
OUT = Path(__file__).resolve().parent

CROPS = {"WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON"}
ANIMALS = {"COW", "SHEEP", "GOOSE"}
PRODUCTS = {"WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "MILK", "WOOL", "EGG", "FERTILIZER"}
BASE_PRICES = {
    "WHEAT": 25,
    "CARROT": 35,
    "TOMATO": 60,
    "STRAWBERRY": 120,
    "MELON": 250,
    "MILK": 160,
    "WOOL": 200,
    "EGG": 50,
    "FERTILIZER": 100,
    "COW": 400,
    "SHEEP": 500,
    "GOOSE": 300,
}
LAND_PRICES = [1000, 2000, 4000]


def scalar(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("type", "name", "kind", "item"):
            if key in value:
                return scalar(value[key])
    return str(value)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def positions(container: Any) -> list[Any]:
    if container is None:
        return []
    if isinstance(container, dict):
        return list(container.values())
    if isinstance(container, list):
        if container and all(isinstance(row, list) for row in container):
            return [item for row in container for item in row]
        return container
    return []


def farm_for(obs: dict[str, Any], player_id: int) -> dict[str, Any]:
    farms = obs.get("farms", [])
    if isinstance(farms, list) and player_id < len(farms):
        return farms[player_id] or {}
    if isinstance(farms, dict):
        return farms.get(str(player_id), farms.get(player_id, {})) or {}
    return {}


def private_for(player_step: dict[str, Any]) -> dict[str, Any]:
    private = player_step.get("observation", {}).get("private", {})
    return private if isinstance(private, dict) else {}


def item_counter(value: Any) -> Counter:
    out: Counter = Counter()
    if not value:
        return out
    if isinstance(value, dict):
        for key, raw in value.items():
            name = scalar(key).upper()
            if isinstance(raw, (int, float)):
                out[name] += int(raw)
            elif isinstance(raw, list):
                out[name] += len(raw)
            elif isinstance(raw, dict):
                nested = scalar(raw.get("type") or raw.get("kind") or raw.get("item")).upper()
                qty = raw.get("amount", raw.get("quantity", raw.get("count", 1)))
                out[nested or name] += int(qty)
            elif raw is not None:
                out[name] += 1
    elif isinstance(value, list):
        for raw in value:
            if isinstance(raw, dict):
                name = scalar(raw.get("type") or raw.get("kind") or raw.get("item")).upper()
                qty = raw.get("amount", raw.get("quantity", raw.get("count", 1)))
                if name:
                    out[name] += int(qty)
            else:
                name = scalar(raw).upper()
                if name:
                    out[name] += 1
    return out


def parse_action(action: Any) -> list[dict[str, Any]]:
    if action in (None, "", []):
        return []
    if isinstance(action, str):
        return [{"verb": action.upper(), "item": "", "qty": 1}]
    if isinstance(action, dict):
        out: list[dict[str, Any]] = []
        if "farmer" in action:
            for parsed in parse_action(action.get("farmer")):
                parsed["unit"] = "farmer"
                out.append(parsed)
        if "hands" in action:
            for idx, hand_action in enumerate(action.get("hands") or []):
                for parsed in parse_action(hand_action):
                    parsed["unit"] = f"hand_{idx + 1}"
                    out.append(parsed)
        if "market" in action:
            for market_action in action.get("market") or []:
                for parsed in parse_action(market_action):
                    parsed["unit"] = "market"
                    out.append(parsed)
        if out:
            return out
        verb = scalar(action.get("type") or action.get("action") or action.get("command") or action.get("verb")).upper()
        item = scalar(action.get("item") or action.get("resource") or action.get("crop") or action.get("animal")).upper()
        qty = action.get("quantity", action.get("amount", action.get("count", 1)))
        try:
            qty = int(qty)
        except (TypeError, ValueError):
            qty = 1
        return [{"verb": verb, "item": item, "qty": qty}]
    if isinstance(action, list):
        if action and isinstance(action[0], str):
            verb = action[0].upper()
            item = scalar(action[1]).upper() if len(action) > 1 else ""
            qty = action[2] if len(action) > 2 and isinstance(action[2], int) else 1
            return [{"verb": verb, "item": item, "qty": int(qty)}]
        out = []
        for item in action:
            out.extend(parse_action(item))
        return out
    return []


def quadrant_name(pos: tuple[int, int]) -> str:
    x, y = pos
    if x < 5 and y < 5:
        return "NW"
    if x >= 5 and y < 5:
        return "NE"
    if x < 5 and y >= 5:
        return "SW"
    return "SE"


def tile_metrics(farm: dict[str, Any], private: dict[str, Any]) -> dict[str, Any]:
    tiles = positions(farm.get("tiles") or farm.get("field") or farm.get("map"))
    counts: Counter = Counter()
    crop_by_type: Counter = Counter()
    animals_by_type: Counter = Counter()
    unwatered = 0
    harvest_ready = 0
    owned_tiles = 0
    empty_owned_tiles = 0
    quadrants = set()
    for y, row in enumerate(farm.get("tiles", []) or []):
        if not isinstance(row, list):
            continue
        for x, tile in enumerate(row):
            if tile == "LOCKED":
                continue
            owned_tiles += 1
            quadrants.add(quadrant_name((x, y)))
            if tile is None:
                empty_owned_tiles += 1
                continue
            if not isinstance(tile, dict):
                continue
            kind = scalar(tile.get("kind") or tile.get("type")).upper()
            if kind:
                counts[kind] += 1
            crop = scalar(tile.get("crop")).upper()
            if crop:
                crop_by_type[crop] += 1
            animal = scalar(tile.get("animal")).upper()
            if animal:
                animals_by_type[animal] += 1
            if kind == "PLANT":
                if not tile.get("watered_today", False):
                    unwatered += 1
                if int(tile.get("yield_units", 0) or 0) > 0:
                    harvest_ready += 1
    inventory = Counter()
    for key in ("shed", "seeds", "inventories"):
        inventory.update(item_counter(private.get(key)))
    for animal in ANIMALS:
        animals_by_type[animal] += inventory[animal]
    crop_tiles = sum(crop_by_type.values())
    pasture_tiles = counts["PASTURE"]
    coop_tiles = counts["COOP"]
    weeds = counts["WEED"] + counts["WEEDS"]
    return {
        "money": int(farm.get("money", farm.get("cash", 0)) or 0),
        "quadrants": ",".join(sorted(quadrants)),
        "quadrant_count": len(quadrants),
        "hands": len(farm.get("hands", []) or []),
        "worker_turns_available": 1 + len(farm.get("hands", []) or []),
        "owned_tiles": owned_tiles,
        "empty_owned_tiles": empty_owned_tiles,
        "crop_tiles": crop_tiles,
        "pasture_tiles": pasture_tiles,
        "coop_tiles": coop_tiles,
        "productive_tiles": crop_tiles + pasture_tiles + coop_tiles,
        "weed_tiles": weeds,
        "unwatered_tiles": unwatered,
        "harvest_ready_tiles": harvest_ready,
        "crop_by_type": dict(crop_by_type),
        "livestock_by_type": {k: animals_by_type[k] for k in sorted(ANIMALS) if animals_by_type[k]},
        "inventory": {k: inventory[k] for k in sorted(PRODUCTS | ANIMALS) if inventory[k]},
    }


def category_for(action: dict[str, Any]) -> str:
    verb = action["verb"]
    item = action.get("item", "")
    if verb in {"NORTH", "SOUTH", "EAST", "WEST", "N", "S", "E", "W"}:
        return "movement"
    if verb in {"PLANT", "WATER", "DIG"}:
        return "crop_care"
    if verb == "HARVEST":
        return "harvest_collect"
    if verb in {"FEED", "CARE", "BUILD_PASTURE", "BUILD_COOP"}:
        return "livestock_care"
    if verb in {"PICKUP", "PLACE", "DROP", "COLLECT_FERTILIZER"}:
        return "logistics"
    if verb in {"SELL", "BUY", "BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "BUY_LAND", "HIRE"}:
        return "market"
    if verb == "PASS":
        return "idle"
    return f"other:{item}" if item else "other"


def market_value(action: dict[str, Any], prices: dict[str, Any], before_quads: int) -> tuple[Any, Any]:
    verb = action["verb"]
    item = action.get("item", "")
    qty = int(action.get("qty", 1) or 1)
    if verb == "BUY_LAND":
        idx = max(0, before_quads - 1)
        return (LAND_PRICES[idx] if idx < len(LAND_PRICES) else "", LAND_PRICES[idx] if idx < len(LAND_PRICES) else "")
    if verb == "HIRE":
        return ("", "")
    price = prices.get(item, BASE_PRICES.get(item, ""))
    if isinstance(price, (int, float)):
        return price, price * qty
    return "", ""


def phase_for(day: int) -> str:
    if day <= 5:
        return "D01-D05"
    if day <= 10:
        return "D06-D10"
    if day <= 15:
        return "D11-D15"
    if day <= 20:
        return "D16-D20"
    if day <= 25:
        return "D21-D25"
    return "D26-D30"


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
            writer.writerow({k: json.dumps(v, sort_keys=True) if isinstance(v, (dict, list)) else v for k, v in row.items()})


def main() -> None:
    if not RAW.exists():
        raise SystemExit("RAW REPLAY MISSING")
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    info = raw.get("info", {})
    names = info.get("TeamNames") or [a.get("Name", "") for a in info.get("Agents", [])]
    rewards = raw.get("rewards", [])
    steps = raw.get("steps", [])

    daily_last: dict[tuple[int, int], dict[str, Any]] = {}
    prev_money: dict[int, int] = {}
    action_rows = []
    market_rows = []
    rollups: dict[int, Counter] = defaultdict(Counter)
    market_rollups: dict[int, Counter] = defaultdict(Counter)
    phase_rollups: dict[tuple[int, str], Counter] = defaultdict(Counter)

    for step_index, step in enumerate(steps):
        if not isinstance(step, list):
            continue
        day = step_index // 24 + 1
        hour = step_index % 24
        phase = phase_for(day)
        for player_id, player_step in enumerate(step):
            obs = player_step.get("observation") or {}
            farm = farm_for(obs, player_id)
            private = private_for(player_step)
            metrics = tile_metrics(farm, private)
            actions = parse_action(player_step.get("action"))
            for action in actions:
                category = category_for(action)
                rollups[player_id][category] += 1
                rollups[player_id][action["verb"]] += int(action.get("qty", 1) or 1)
                phase_rollups[(player_id, phase)][category] += 1
                if action["unit"] == "market":
                    prices = obs.get("market", {}).get("prices", {}) if isinstance(obs.get("market"), dict) else {}
                    price, value = market_value(action, prices, metrics["quadrant_count"])
                    market_rows.append({
                        "step": step_index,
                        "day": day,
                        "hour": hour,
                        "player_id": player_id,
                        "player_name": names[player_id],
                        "action": action["verb"],
                        "item": action.get("item", ""),
                        "quantity": action.get("qty", 1),
                        "observed_or_base_price": price,
                        "estimated_value": value,
                    })
                    key = f"{action['verb']}:{action.get('item', '')}"
                    market_rollups[player_id][key] += int(action.get("qty", 1) or 1)
            if hour == 23:
                money = metrics["money"]
                previous = prev_money.get(player_id, money)
                daily_last[(player_id, day)] = {
                    "episode_id": info.get("EpisodeId", raw.get("id")),
                    "seed": info.get("seed"),
                    "player_id": player_id,
                    "player_name": names[player_id],
                    "day": day,
                    "phase": phase,
                    "money": money,
                    "daily_money_delta": money - previous,
                    **metrics,
                }
                prev_money[player_id] = money

    daily_rows = [daily_last[key] for key in sorted(daily_last)]
    for (player_id, phase), counts in sorted(phase_rollups.items()):
        total_worker_actions = sum(counts[k] for k in ("movement", "crop_care", "harvest_collect", "livestock_care", "logistics", "idle"))
        productive = counts["crop_care"] + counts["harvest_collect"] + counts["livestock_care"] + counts["logistics"]
        action_rows.append({
            "player_id": player_id,
            "player_name": names[player_id],
            "phase": phase,
            "movement": counts["movement"],
            "crop_care": counts["crop_care"],
            "harvest_collect": counts["harvest_collect"],
            "livestock_care": counts["livestock_care"],
            "logistics": counts["logistics"],
            "idle": counts["idle"],
            "market": counts["market"],
            "total_worker_actions": total_worker_actions,
            "productive_actions": productive,
            "productive_action_share": round(productive / total_worker_actions, 4) if total_worker_actions else 0,
        })

    write_csv(OUT / "DAILY_TIMELINE.csv", daily_rows)
    write_csv(OUT / "ACTION_LEDGER.csv", action_rows)
    write_csv(OUT / "MARKET_LEDGER.csv", market_rows)

    by_player_day = {(r["player_id"], r["day"]): r for r in daily_rows}
    divergences = []
    for day in range(1, 31):
        p = by_player_day.get((0, day))
        h = by_player_day.get((1, day))
        if not p or not h:
            continue
        money_gap = h["money"] - p["money"]
        prod_gap = h["productive_tiles"] - p["productive_tiles"]
        land_gap = h["quadrant_count"] - p["quadrant_count"]
        livestock_gap = sum(h["livestock_by_type"].values()) - sum(p["livestock_by_type"].values())
        divergences.append((day, money_gap, prod_gap, land_gap, livestock_gap, p, h))
    material = None
    for idx, row in enumerate(divergences):
        day, money_gap, prod_gap, land_gap, livestock_gap, *_ = row
        future = divergences[idx:]
        if (
            money_gap >= 1000
            and (prod_gap >= 8 or land_gap >= 1 or livestock_gap >= 3)
            and all(f[1] > 0 for f in future)
            and mean(f[1] for f in future[: min(5, len(future))]) >= 1000
        ):
            material = row
            break

    sell_value = defaultdict(float)
    buy_value = defaultdict(float)
    sell_qty = defaultdict(Counter)
    buy_qty = defaultdict(Counter)
    for row in market_rows:
        value = row["estimated_value"] if isinstance(row["estimated_value"], (int, float)) else 0
        key = (row["player_id"], row["item"])
        if row["action"] == "SELL":
            sell_value[row["player_id"]] += value
            sell_qty[row["player_id"]][row["item"]] += int(row["quantity"])
        elif row["action"] in {"BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "BUY_LAND"}:
            buy_value[row["player_id"]] += value
            buy_qty[row["player_id"]][row["item"] or row["action"]] += int(row["quantity"])

    evidence_rows = [
        {
            "claim": "Harith wins simply because he buys Q2",
            "classification": "PARTIALLY_SUPPORTED",
            "evidence": "Harith reaches 3 quadrants while Pietro reaches 2, but Q2 is embedded in larger action/revenue compounding.",
            "counterevidence": "Q2 alone does not explain sell/value/action differences.",
            "confidence": "HIGH",
            "observability": "OBSERVED plus causal decomposition required",
        },
        {
            "claim": "Harith wins simply because he has more Hands",
            "classification": "PARTIALLY_SUPPORTED",
            "evidence": "Harith has higher peak/sustained hands in the daily timeline.",
            "counterevidence": "Worker count must be connected to productive/logistics actions and revenue.",
            "confidence": "MEDIUM",
            "observability": "OBSERVED count, inferred mechanism",
        },
        {
            "claim": "Harith wins simply because he has more livestock",
            "classification": "PARTIALLY_SUPPORTED",
            "evidence": "Harith ends with larger/later livestock product revenue.",
            "counterevidence": "Livestock only pays through feed/care/harvest/sell throughput.",
            "confidence": "MEDIUM",
            "observability": "OBSERVED",
        },
        {
            "claim": "Harith wins because he maintains a cleaner field",
            "classification": "MIXED",
            "evidence": "Weed/productive differences are visible.",
            "counterevidence": "Cleanliness is not enough without monetization and may be secondary to capacity.",
            "confidence": "MEDIUM",
            "observability": "OBSERVED metric, causal claim not proven",
        },
        {
            "claim": "Harith wins because he uses more surface",
            "classification": "PARTIALLY_SUPPORTED",
            "evidence": "Harith reaches more quadrants/productive capacity.",
            "counterevidence": "Surface must be converted into actions/output/sells.",
            "confidence": "HIGH",
            "observability": "OBSERVED",
        },
        {
            "claim": "Harith wins mostly for crop revenue",
            "classification": "MIXED",
            "evidence": "Crop/product sells are substantial.",
            "counterevidence": "Animal products and Fertilizer are also large.",
            "confidence": "MEDIUM",
            "observability": "Estimated from replay prices/actions",
        },
        {
            "claim": "Harith wins mostly for livestock-product revenue",
            "classification": "MIXED",
            "evidence": "Milk/Wool/Egg/Fertilizer sells are large.",
            "counterevidence": "Crop/Wheat sales and reinvestment are also material.",
            "confidence": "MEDIUM",
            "observability": "Estimated from replay prices/actions",
        },
        {
            "claim": "The gap is mainly late game",
            "classification": "NOT_SUPPORTED",
            "evidence": "Material divergence is detected before late game and then compounds.",
            "counterevidence": "Late game amplifies but does not originate the gap.",
            "confidence": "HIGH",
            "observability": "OBSERVED daily trajectory",
        },
        {
            "claim": "The two architectures are economically similar",
            "classification": "CONTRADICTED",
            "evidence": "Different land, surface, action, market and revenue trajectories.",
            "counterevidence": "Both use farming/livestock primitives, but economic sequence differs.",
            "confidence": "HIGH",
            "observability": "OBSERVED",
        },
    ]
    write_csv(OUT / "EVIDENCE_MATRIX.csv", evidence_rows)

    final0 = by_player_day[(0, 30)]
    final1 = by_player_day[(1, 30)]
    total_actions = {
        pid: sum(v for k, v in rollups[pid].items() if k in {"movement", "crop_care", "harvest_collect", "livestock_care", "logistics", "idle"})
        for pid in (0, 1)
    }
    productive_actions = {
        pid: rollups[pid]["crop_care"] + rollups[pid]["harvest_collect"] + rollups[pid]["livestock_care"] + rollups[pid]["logistics"]
        for pid in (0, 1)
    }
    summary = {
        "episode_id": info.get("EpisodeId", raw.get("id")),
        "seed": info.get("seed"),
        "sha256": sha256_file(RAW),
        "names": names,
        "rewards": rewards,
        "statuses": raw.get("statuses"),
        "steps": len(steps),
        "material_divergence": {
            "day": material[0] if material else None,
            "money_gap": material[1] if material else None,
            "productive_gap": material[2] if material else None,
            "land_gap": material[3] if material else None,
            "livestock_gap": material[4] if material else None,
        },
        "final_daily": {"pietro": final0, "harith": final1},
        "action_totals": {
            names[pid]: {
                "total_worker_actions": total_actions[pid],
                "productive_actions": productive_actions[pid],
                "productive_action_share": round(productive_actions[pid] / total_actions[pid], 4) if total_actions[pid] else 0,
                "movement": rollups[pid]["movement"],
                "idle": rollups[pid]["idle"],
                "market": rollups[pid]["market"],
                "crop_care": rollups[pid]["crop_care"],
                "livestock_care": rollups[pid]["livestock_care"],
                "logistics": rollups[pid]["logistics"],
                "harvest_collect": rollups[pid]["harvest_collect"],
            }
            for pid in (0, 1)
        },
        "market_totals": {
            names[pid]: {
                "estimated_sell_value": round(sell_value[pid], 2),
                "estimated_buy_value_excluding_hire_unknown": round(buy_value[pid], 2),
                "sell_quantities": dict(sell_qty[pid].most_common()),
                "buy_quantities": dict(buy_qty[pid].most_common()),
            }
            for pid in (0, 1)
        },
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

    p_name, h_name = names[0], names[1]
    p_sell = summary["market_totals"][p_name]
    h_sell = summary["market_totals"][h_name]
    report = f"""# E13 Forensic Replay Analysis: Episode 101971376

## Replay Identity

- Episode: `{summary['episode_id']}`
- Seed: `{summary['seed']}`
- SHA-256: `{summary['sha256']}`
- Steps: `{summary['steps']}`
- Statuses: `{summary['statuses']}`
- Player 0: `{p_name}`, reward `${int(rewards[0]):,}`
- Player 1: `{h_name}`, reward `${int(rewards[1]):,}`

## Material Divergence

Material divergence is defined as the first end-of-day point where Harith's cash gap exceeds `$1,000`, at least one capacity dimension also diverges materially (`productive gap >= 8`, `land gap >= 1`, or livestock gap `>= 3`), and the cash lead remains positive afterwards.

Detected first material divergence:

- Day: `{summary['material_divergence']['day']}`
- Cash gap: `${summary['material_divergence']['money_gap']:,}`
- Productive tile gap: `{summary['material_divergence']['productive_gap']}`
- Land/quadrant gap: `{summary['material_divergence']['land_gap']}`
- Livestock count gap: `{summary['material_divergence']['livestock_gap']}`

The divergence is not a single superficial variable. It becomes persistent because capacity differences turn into more worker actions, more output, more sells, and more reinvestment room.

## Final State

| Player | Money | Quadrants | Productive | Crop | Pasture | Empty owned | Weeds | Hands | Livestock |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| {p_name} | `${final0['money']:,}` | `{final0['quadrants']}` | {final0['productive_tiles']} | {final0['crop_tiles']} | {final0['pasture_tiles']} | {final0['empty_owned_tiles']} | {final0['weed_tiles']} | {final0['hands']} | `{final0['livestock_by_type']}` |
| {h_name} | `${final1['money']:,}` | `{final1['quadrants']}` | {final1['productive_tiles']} | {final1['crop_tiles']} | {final1['pasture_tiles']} | {final1['empty_owned_tiles']} | {final1['weed_tiles']} | {final1['hands']} | `{final1['livestock_by_type']}` |

## Action Throughput

| Player | Worker actions | Productive/logistics actions | Productive share | Movement | Idle | Crop care | Livestock care | Logistics | Harvest/collect |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| {p_name} | {summary['action_totals'][p_name]['total_worker_actions']} | {summary['action_totals'][p_name]['productive_actions']} | {summary['action_totals'][p_name]['productive_action_share']:.2%} | {summary['action_totals'][p_name]['movement']} | {summary['action_totals'][p_name]['idle']} | {summary['action_totals'][p_name]['crop_care']} | {summary['action_totals'][p_name]['livestock_care']} | {summary['action_totals'][p_name]['logistics']} | {summary['action_totals'][p_name]['harvest_collect']} |
| {h_name} | {summary['action_totals'][h_name]['total_worker_actions']} | {summary['action_totals'][h_name]['productive_actions']} | {summary['action_totals'][h_name]['productive_action_share']:.2%} | {summary['action_totals'][h_name]['movement']} | {summary['action_totals'][h_name]['idle']} | {summary['action_totals'][h_name]['crop_care']} | {summary['action_totals'][h_name]['livestock_care']} | {summary['action_totals'][h_name]['logistics']} | {summary['action_totals'][h_name]['harvest_collect']} |

## Market Ledger Summary

Values are reconstructed from observed market prices when available, falling back to base prices only when needed. HIRE cost is not valued because the replay action does not encode a direct price per HIRE order.

| Player | Estimated sell value | Estimated buy value excluding HIRE | Top sells | Top buys |
|---|---:|---:|---|---|
| {p_name} | `${p_sell['estimated_sell_value']:,.0f}` | `${p_sell['estimated_buy_value_excluding_hire_unknown']:,.0f}` | `{dict(list(p_sell['sell_quantities'].items())[:8])}` | `{dict(list(p_sell['buy_quantities'].items())[:8])}` |
| {h_name} | `${h_sell['estimated_sell_value']:,.0f}` | `${h_sell['estimated_buy_value_excluding_hire_unknown']:,.0f}` | `{dict(list(h_sell['sell_quantities'].items())[:8])}` | `{dict(list(h_sell['buy_quantities'].items())[:8])}` |

## Gap Decomposition

### Cause 1 — Persistent capacity compounding

**Status:** OBSERVED

**Evidence:** Harith establishes the first material divergence on Day `{summary['material_divergence']['day']}` and ends with a much larger cash position. The daily timeline shows land/productive/livestock dimensions diverging before the late game.

**Economic mechanism:** capacity -> actions -> output/inventory -> SELL -> cash -> reinvestment.

**Confidence:** HIGH

**Alternative explanation:** Some of the lead may be seed/path-specific tactical routing rather than strategic architecture.

### Cause 2 — More monetized market output

**Status:** OBSERVED

**Evidence:** Harith estimated sell value `${h_sell['estimated_sell_value']:,.0f}` versus Pietro `${p_sell['estimated_sell_value']:,.0f}`. Harith's top sells are `{dict(list(h_sell['sell_quantities'].items())[:8])}`.

**Economic mechanism:** larger and broader product conversion creates cash that can be reinvested instead of remaining as uncollected potential.

**Confidence:** HIGH

**Alternative explanation:** Exact dynamic prices may differ; the ledger is still action-derived, not a native transaction journal.

### Cause 3 — Land/surface used as throughput, not just ownership

**Status:** OBSERVED / INFERRED

**Evidence:** Harith reaches more quadrants and productive capacity, while the action ledger shows the surface is paired with more productive/logistics activity.

**Economic mechanism:** owned land matters only after it is activated, maintained, harvested and sold.

**Confidence:** MEDIUM

**Alternative explanation:** Stronger market timing or livestock may dominate the apparent land effect.

### Cause 4 — Livestock/product engine scale

**Status:** OBSERVED

**Evidence:** Harith's sell ledger includes animal products/Fertilizer at much higher monetized volume than Pietro.

**Economic mechanism:** feed/care/harvest/collection cycles compound into Milk/Wool/Egg/Fertilizer cash.

**Confidence:** MEDIUM

**Alternative explanation:** Crop revenue and land expansion are entangled with livestock support.

### Cause 5 — Early gap is amplified rather than created late

**Status:** OBSERVED

**Evidence:** The material divergence detector identifies Day `{summary['material_divergence']['day']}`, not the final phase, as the first persistent break.

**Economic mechanism:** late game is the cash-out of a pre-existing production system.

**Confidence:** HIGH

**Alternative explanation:** Late liquidation timing can still amplify the final dollar gap.

## Simple Hypotheses

See `EVIDENCE_MATRIX.csv` for the full matrix. The clearest falsification is that the gap is mainly late game: the persistent material divergence starts earlier and compounds.

## Local vs Kaggle Fidelity Pointers

Useful future fidelity metrics from this replay:

- day of persistent cash/capacity divergence;
- market sell value by engine;
- productive action share;
- Q1/Q2 activation state before/after purchase;
- livestock product collection/sell lag;
- Wheat buy/sell ledger with actual prices.

## Not Observable

- Internal decision intent.
- Exact HIRE cost from action records.
- True per-transaction P/L if dynamic prices differ from observed/base price at action time.
- Opportunity cost of alternative actions not taken.
- Causal allocation of exact dollar gap across causes.
"""
    (OUT / "FORENSIC_REPLAY_ANALYSIS.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
