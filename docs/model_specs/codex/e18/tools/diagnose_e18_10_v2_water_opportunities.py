#!/usr/bin/env python3
"""Measure topology-preserving WATER opportunities left by E18.10 V2.

The diagnostic observes the public state and the final policy action before the
engine applies it.  It never changes an action.  Development seeds only.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy
from pathlib import Path
from typing import Any

from kaggle_environments import make

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agricola.strategy.codex.codex_e17_reactive_service_routing import (
    _is_feasible,
)
from agricola.strategy.codex.codex_e17_topology_cap_662 import (
    _farm,
    _inventories,
    _positions,
    _tile,
    _unit_actions,
)
from agricola.strategy.codex.codex_e18_770_water_before_dig_guard_v2 import (
    create_codex_e18_770_water_before_dig_guard_v2,
)

MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"
OUTPUT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_10_V2_770_WATER_OPPORTUNITY_DIAGNOSTIC_V1.json"
)
SHED_ACCESS = frozenset({(4, 4), (5, 4), (4, 5), (5, 5)})
PROTECTED_ROTATION = frozenset({(3, 5), (4, 5), (3, 6), (4, 6), (4, 7)})
MOVES = frozenset({"NORTH", "SOUTH", "EAST", "WEST"})
KNOWN_LOCAL_COMMANDS = frozenset(
    {
        "BUILD_COOP",
        "BUILD_PASTURE",
        "CARE",
        "COLLECT_FERTILIZER",
        "DROP",
        "FEED",
        "FERTILIZE",
        "HARVEST",
        "PICKUP",
        "PLACE",
        "PLANT",
    }
)


def _quadrant(position: tuple[int, int]) -> str:
    x, y = position
    return f"Q{int(x >= 5) + 2 * int(y >= 5)}"


class WaterOpportunityProbe:
    """Passive wrapper around E18.10 V2."""

    def __init__(self, *, seed: int, seat: int) -> None:
        context = {
            "run_id": f"E18-10-V2-WATER-DIAG-S{seed}-P{seat}",
            "episode_id": f"E18-10-V2-WATER-DIAG-S{seed}-P{seat}",
            "seed": seed,
            "player_position": seat,
        }
        self.policy = create_codex_e18_770_water_before_dig_guard_v2(
            run_context=context
        )
        self.controller = (
            self.policy.codex_e18_770_water_before_dig_guard_v2_instance
        )
        self.counts: Counter[str] = Counter()
        self.by_display_day: dict[int, Counter[str]] = {}
        self.by_position: Counter[str] = Counter()
        self.by_crop: Counter[str] = Counter()

    def __call__(
        self, observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        action = self.policy(observation, configuration)
        farm = _farm(observation)
        positions = _positions(farm)
        private = observation.get("private", {}) or {}
        inventories = _inventories(private, len(positions))
        commands = _unit_actions(action, len(positions))
        display_day = int(observation.get("day", 0)) + 1
        daily = self.by_display_day.setdefault(display_day, Counter())
        for worker, position in enumerate(positions):
            tile = _tile(farm, position)
            command = commands[worker] if worker < len(commands) else ["PASS"]
            opcode = str(command[0]) if command else "PASS"
            if not (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and int(tile.get("yield_units", 0) or 0) <= 0
                and not bool(tile.get("watered_today", False))
            ):
                continue
            self.counts["worker_turns_on_actionable_unwatered_crop"] += 1
            self.counts[f"final_opcode_{opcode}"] += 1
            daily[f"final_opcode_{opcode}"] += 1
            crop = str(tile.get("crop", "UNKNOWN"))
            self.by_crop[f"{crop}:{opcode}"] += 1
            self.by_position[
                f"{_quadrant(position)}:{position[0]},{position[1]}:{opcode}"
            ] += 1
            if opcode == "PASS":
                self.counts["pass_water_opportunities_all"] += 1
                daily["pass_water_opportunities_all"] += 1
                if position not in SHED_ACCESS:
                    self.counts["pass_water_opportunities_non_shed"] += 1
                    daily["pass_water_opportunities_non_shed"] += 1
                if position not in SHED_ACCESS and position not in PROTECTED_ROTATION:
                    self.counts["pass_water_opportunities_incremental_vs_v2"] += 1
                    daily["pass_water_opportunities_incremental_vs_v2"] += 1
            elif opcode in MOVES:
                self.counts["move_departures_from_unwatered_crop"] += 1
                daily["move_departures_from_unwatered_crop"] += 1
            elif (
                position not in SHED_ACCESS
                and opcode in KNOWN_LOCAL_COMMANDS
                and not _is_feasible(
                    command,
                    position=position,
                    inventory=inventories[worker],
                    farm=farm,
                    private=private,
                    board_size=10,
                )
            ):
                self.counts["safe_invalid_command_to_water"] += 1
                self.counts[f"safe_invalid_{opcode}_to_water"] += 1
                daily["safe_invalid_command_to_water"] += 1
                daily[f"safe_invalid_{opcode}_to_water"] += 1
        return deepcopy(action)

    def snapshot(self) -> dict[str, Any]:
        telemetry = self.controller.telemetry_snapshot()
        return {
            "counts": dict(sorted(self.counts.items())),
            "by_display_day": {
                str(day): dict(sorted(values.items()))
                for day, values in sorted(self.by_display_day.items())
            },
            "by_crop_and_opcode": dict(sorted(self.by_crop.items())),
            "by_position_and_opcode": dict(sorted(self.by_position.items())),
            "technical_errors": int(self.controller.error_count),
            "fallbacks": int(self.controller.fallback_count),
            "final_topology": telemetry.get("target_pastures_by_quadrant"),
        }


def _run(seed: int, candidate_seat: int) -> dict[str, Any]:
    candidate = WaterOpportunityProbe(seed=seed, seat=candidate_seat)
    opponent = create_codex_e18_770_water_before_dig_guard_v2(
        run_context={
            "run_id": f"E18-10-V2-WATER-DIAG-OPP-S{seed}-P{1-candidate_seat}",
            "episode_id": f"E18-10-V2-WATER-DIAG-OPP-S{seed}-P{1-candidate_seat}",
            "seed": seed,
            "player_position": 1 - candidate_seat,
        }
    )
    policies = [opponent, opponent]
    policies[candidate_seat] = candidate
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=False,
    )
    env.run(policies)
    result = candidate.snapshot()
    result.update(
        {
            "seed": seed,
            "seat": candidate_seat,
            "final_money": float(
                env.steps[-1][candidate_seat]["observation"]["farms"]
                [candidate_seat]["money"]
            ),
        }
    )
    return result


def _run_spec(spec: tuple[int, int]) -> dict[str, Any]:
    return _run(*spec)


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    seeds = [int(value) for value in manifest["seed_policy"]["development"]]
    reserved = {
        *map(int, manifest["seed_policy"]["holdout"]["seeds"]),
        *map(int, manifest["seed_policy"]["final_confirmation"]["seeds"]),
    }
    if set(seeds).intersection(reserved):
        raise RuntimeError("development matrix overlaps a reserved seed")
    specs = [(seed, seat) for seed in seeds for seat in (0, 1)]
    with ProcessPoolExecutor(max_workers=6) as executor:
        runs = list(executor.map(_run_spec, specs))
    totals: Counter[str] = Counter()
    daily: dict[int, Counter[str]] = {}
    crop: Counter[str] = Counter()
    position: Counter[str] = Counter()
    for run in runs:
        totals.update(run["counts"])
        crop.update(run["by_crop_and_opcode"])
        position.update(run["by_position_and_opcode"])
        for day, values in run["by_display_day"].items():
            daily.setdefault(int(day), Counter()).update(values)
    payload = {
        "schema_version": "E18_10_V2_770_WATER_OPPORTUNITY_DIAGNOSTIC_V1",
        "date": "2026-09-04",
        "epistemic_role": "DEVELOPMENT_ONLY_PASSIVE_POLICY_DIAGNOSTIC",
        "policy": "CODEX_E18_10_770_WATER_BEFORE_DIG_GUARD_V2",
        "topology": {"Q0": 7, "Q1": 7, "Q2": 0},
        "seeds": seeds,
        "seats": [0, 1],
        "run_count": len(runs),
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_upload_authorized": False,
        "definitions": {
            "actionable_unwatered_crop": (
                "live PLANT with yield_units <= 0 and watered_today false"
            ),
            "incremental_vs_v2": (
                "final PASS on actionable crop outside four shed-access cells "
                "and outside the five protected rotation cells"
            ),
        },
        "totals": dict(sorted(totals.items())),
        "mean_per_run": {
            key: value / len(runs) for key, value in sorted(totals.items())
        },
        "by_display_day": {
            str(day): dict(sorted(values.items()))
            for day, values in sorted(daily.items())
        },
        "by_crop_and_opcode": dict(sorted(crop.items())),
        "by_position_and_opcode": dict(sorted(position.items())),
        "runs": runs,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload["mean_per_run"], indent=2, sort_keys=True))
    print(f"wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
