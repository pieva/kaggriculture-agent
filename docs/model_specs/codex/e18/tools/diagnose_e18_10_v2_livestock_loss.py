#!/usr/bin/env python3
"""Locate the day-boundary livestock loss in E18.10 V2 (development seed)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from kaggle_environments import make

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agricola.strategy.codex.codex_e18_770_water_before_dig_guard_v2 import (
    create_codex_e18_770_water_before_dig_guard_v2,
)

OUTPUT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_10_V2_770_LIVESTOCK_LOSS_DIAGNOSTIC_V1.json"
)
SEED = 180903001
SPECIES = ("COW", "SHEEP")


def _snapshot(state: list[dict[str, Any]], seat: int) -> dict[str, Any]:
    observation = state[seat].get("observation", {}) or {}
    farm = observation["farms"][seat]
    private = observation.get("private", {}) or {}
    animals = []
    for y, row in enumerate(farm.get("tiles", []) or []):
        for x, tile in enumerate(row):
            if not isinstance(tile, dict) or tile.get("animal") not in SPECIES:
                continue
            animals.append(
                {
                    "position": [x, y],
                    "species": str(tile["animal"]),
                    "fed_today": bool(tile.get("fed_today", False)),
                    "cared_today": bool(tile.get("cared_today", False)),
                    "consecutive_unfed": int(
                        tile.get("consecutive_unfed", 0) or 0
                    ),
                }
            )
    shed = private.get("shed", {}) or {}
    inventories = private.get("inventories", []) or []
    positions = [
        tuple(farm.get("farmer", [4, 4])),
        *(tuple(value) for value in farm.get("hands", []) or []),
    ]
    action = state[seat].get("action", {}) or {}
    commands = [
        action.get("farmer", ["PASS"]),
        *(action.get("hands", []) or []),
    ]
    stored = sum(max(0, int(shed.get(item, 0) or 0)) for item in SPECIES)
    carried = sum(
        max(0, int(inventory.get(item, 0) or 0))
        for inventory in inventories
        if isinstance(inventory, dict)
        for item in SPECIES
    )
    return {
        "step": int(observation.get("step", 0)),
        "display_day": int(observation.get("day", 0)) + 1,
        "hour": int(observation.get("hour", 0)),
        "resources": len(animals) + stored + carried,
        "placed": len(animals),
        "stored": stored,
        "carried": carried,
        "unfed": sum(not value["fed_today"] for value in animals),
        "max_consecutive_unfed": max(
            (value["consecutive_unfed"] for value in animals), default=0
        ),
        "animals": animals,
        "workers": [
            {
                "worker": worker,
                "position": list(position),
                "inventory": (
                    inventories[worker]
                    if worker < len(inventories)
                    and isinstance(inventories[worker], dict)
                    else {}
                ),
                "command": commands[worker] if worker < len(commands) else ["PASS"],
            }
            for worker, position in enumerate(positions)
        ],
    }


def main() -> int:
    policies = [
        create_codex_e18_770_water_before_dig_guard_v2(
            run_context={"seed": SEED, "player_position": seat}
        )
        for seat in (0, 1)
    ]
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": SEED, "turnsPerDay": 24},
        debug=False,
    )
    env.run(policies)
    timeline = [
        _snapshot(state, 0)
        for state in env.steps
        if (
            int((state[0].get("observation", {}) or {}).get("hour", -1))
            in {0, 23}
            or int((state[0].get("observation", {}) or {}).get("day", -1))
            == 19
        )
    ]
    losses = []
    previous_eod = None
    for row in timeline:
        if row["hour"] == 23:
            previous_eod = row
        elif previous_eod is not None and row["resources"] < previous_eod["resources"]:
            lost_positions = [
                value
                for value in previous_eod["animals"]
                if tuple(value["position"])
                not in {tuple(item["position"]) for item in row["animals"]}
            ]
            losses.append(
                {
                    "from": previous_eod,
                    "to": row,
                    "lost_positions": lost_positions,
                }
            )
    payload = {
        "schema_version": "E18_10_V2_770_LIVESTOCK_LOSS_DIAGNOSTIC_V1",
        "date": "2026-09-04",
        "epistemic_role": "DEVELOPMENT_ONLY_PASSIVE_DIAGNOSTIC",
        "seed": SEED,
        "seat": 0,
        "holdout_consumed": False,
        "losses": losses,
        "timeline": timeline,
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(losses, indent=2, sort_keys=True))
    print(f"wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
