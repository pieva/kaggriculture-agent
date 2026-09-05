#!/usr/bin/env python3
"""Classify E18.22 PLANT/HARVEST guard rejections against E18.16."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from kaggle_environments import make

ROOT = Path(__file__).resolve().parents[5]
TOOLS = ROOT / "docs/model_specs/codex/e18/tools"
for import_root in (ROOT, TOOLS):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from agricola.strategy.codex.codex_e18_770_exact_cap_critical_feed import (
    create_codex_e18_770_exact_cap_critical_feed,
)
from docs.model_specs.codex.e18.tools.e18_19_retrying_trajectory_controller import (
    _farm,
)
from docs.model_specs.codex.e18.tools.e18_22_wheat_jit_d1_controller import (
    WheatJitD1Controller,
)

SEED = 180903001
PLAN = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_18_770_CAPACITY_TRAJECTORY_GATE_0A_V1.json"
)
OUTPUT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_22_CROP_REJECTION_DIAGNOSTIC_V1.json"
)
REPORT = (
    ROOT
    / "docs/model_specs/codex/e18/reports/"
    / "E18_22_CROP_REJECTION_DIAGNOSTIC_REPORT_IT.md"
)


class CropRejectionDiagnosticController(WheatJitD1Controller):
    """Observe crop guard failures without changing E18.22 decisions."""

    def __init__(self, plan: dict[str, Any], seat: int = 0) -> None:
        super().__init__(plan, seat=seat)
        self.crop_rejection_events: dict[tuple[int, int, int], dict[str, Any]] = {}
        self.unlock_first_seen: dict[str, dict[str, int]] = {}

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        day = int(observation.get("day", 0)) + 1
        turn = int(observation.get("hour", 0)) + 1
        farm = _farm(observation, self.seat)
        for quadrant in farm.get("unlocked_quadrants", []) or []:
            self.unlock_first_seen.setdefault(
                str(quadrant), {"day": day, "turn": turn}
            )
        return super().__call__(observation, configuration)

    @staticmethod
    def _tile_reason(tile: Any) -> str:
        if tile is None:
            return "TILE_EMPTY"
        if not isinstance(tile, dict):
            return f"TILE_{str(tile).upper()}"
        kind = str(tile.get("kind", "UNKNOWN")).upper()
        if kind != "PLANT":
            return f"TILE_{kind}"
        crop = str(tile.get("crop", "UNKNOWN")).upper()
        yield_units = int(tile.get("yield_units", 0) or 0)
        return f"TILE_PLANT_{crop}_YIELD_{yield_units}"

    def _planned_or_recovery(
        self,
        row: dict[str, Any],
        farm: dict[str, Any],
        private: dict[str, Any],
        worker: int,
        key: tuple[int, int],
    ) -> tuple[list[Any], dict[str, Any] | None]:
        opcode = str(row["opcode"])
        position = self._position(farm, worker)
        target = tuple(int(value) for value in row.get("position", position))
        if position == target and opcode in {"PLANT", "HARVEST"}:
            tile = self._tile(farm, position)
            args = row.get("arguments", {}) or {}
            reason: str | None = None
            if opcode == "PLANT":
                crop = str(args["crop"])
                seeds = int((private.get("seeds", {}) or {}).get(crop, 0))
                if not (isinstance(tile, dict) and tile.get("kind") == "WEED"):
                    if tile is not None:
                        reason = self._tile_reason(tile)
                    elif seeds <= 0:
                        reason = f"NO_SEED_{crop}"
            elif not isinstance(tile, dict) or int(
                tile.get("yield_units", 0) or 0
            ) <= 0:
                reason = self._tile_reason(tile)
            if reason is not None:
                event_key = (key[0], worker, self.cursors[key])
                event = self.crop_rejection_events.setdefault(
                    event_key,
                    {
                        "day": key[0],
                        "turn": int(row["turn"]),
                        "worker": worker,
                        "route_index": self.cursors[key],
                        "opcode": opcode,
                        "position": list(target),
                        "arguments": args,
                        "reason": reason,
                        "attempts": 0,
                        "tile": tile,
                    },
                )
                event["attempts"] += 1
        return super()._planned_or_recovery(row, farm, private, worker, key)


def _run(plan: dict[str, Any], seat: int) -> dict[str, Any]:
    candidate = CropRejectionDiagnosticController(plan, seat=seat)
    opponent_seat = 1 - seat
    opponent = create_codex_e18_770_exact_cap_critical_feed(
        run_context={
            "run_id": f"E18-22-CROP-DIAG-S{SEED}-P{opponent_seat}",
            "episode_id": f"E18-22-CROP-DIAG-S{SEED}-P{opponent_seat}",
            "seed": SEED,
            "player_position": opponent_seat,
        }
    )
    policies = [None, None]
    policies[seat] = candidate
    policies[opponent_seat] = opponent
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": SEED, "turnsPerDay": 24},
        debug=False,
    )
    env.run(policies)
    replay = env.toJSON()
    events = list(candidate.crop_rejection_events.values())
    reasons = Counter(f"{event['opcode']}:{event['reason']}" for event in events)
    by_day = Counter(f"D{event['day']}:{event['opcode']}" for event in events)
    return {
        "candidate_seat": seat,
        "candidate_reward": float(replay["rewards"][seat] or 0),
        "opponent_reward": float(replay["rewards"][opponent_seat] or 0),
        "unique_rejections": len(events),
        "reason_counts": dict(sorted(reasons.items())),
        "day_counts": dict(sorted(by_day.items())),
        "skipped_stale": dict(sorted(candidate.skipped_stale.items())),
        "unlock_first_seen": candidate.unlock_first_seen,
        "market_trace": candidate.market_trace,
        "events": events,
        "candidate_errors": candidate.error_count,
    }


def _write_report(payload: dict[str, Any]) -> None:
    aggregate = payload["aggregate_reason_counts"]
    rows = "\n".join(
        f"| `{reason}` | {count} |" for reason, count in aggregate.items()
    )
    report = f"""# E18.22 — Diagnosi rifiuti crop

Seed `{SEED}`, entrambi i seat, comportamento E18.22 invariato.

| Causa | Eventi unici sui due seat |
|---|---:|
{rows}

Gli eventi completi conservano giorno, turno, worker, posizione, argomenti e
snapshot della tile per selezionare l'ablation E18.23 senza confondere cause.
"""
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")


def main() -> int:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    matches = [_run(plan, seat) for seat in (0, 1)]
    aggregate = Counter(
        {
            reason: sum(match["reason_counts"].get(reason, 0) for match in matches)
            for reason in {
                reason
                for match in matches
                for reason in match["reason_counts"]
            }
        }
    )
    payload = {
        "schema_version": "e18.codex.crop_rejection_diagnostic.v1",
        "subject": "CODEX_E18_22_770_WHEAT_JIT_D1_V1",
        "opponent": "CODEX_E18_16_770_EXACT_CAP_CRITICAL_FEED_V1",
        "seed": SEED,
        "seats": [0, 1],
        "aggregate_reason_counts": dict(sorted(aggregate.items())),
        "matches": matches,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    _write_report(payload)
    print(json.dumps(payload["aggregate_reason_counts"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
