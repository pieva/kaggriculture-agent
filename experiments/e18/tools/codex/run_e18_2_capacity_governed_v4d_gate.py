#!/usr/bin/env python3
"""Development gate for Codex E18.2 against the active peer-V2 roster.

The matrix is real-engine only and uses the seven preregistered development
seeds in both seats.  Antigravity, holdout seeds and final-confirmation seeds
are intentionally excluded.
"""

from __future__ import annotations

import csv
import json
import statistics
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agricola.strategy.claude.e18_opponent_reactive_v2 import (
    DEFAULT_CONFIG_PATH as CLAUDE_CONFIG,
)
from agricola.strategy.claude.e18_opponent_reactive_v2 import (
    create_claude_e18_agent_v2,
)
from agricola.strategy.codex.codex_e17_batched_cluster_routing_v4 import (
    DEFAULT_V4D_CONFIG_PATH,
    create_codex_e17_batched_cluster_routing_v4,
)
from agricola.strategy.codex.codex_e18_capacity_governed_v4d import (
    DEFAULT_E18_CAPACITY_GOVERNED_CONFIG_PATH,
    create_codex_e18_capacity_governed_v4d,
)
from agricola.strategy.codex.codex_e18_opponent_reactive_topology import (
    DEFAULT_E18_OPPONENT_REACTIVE_CONFIG_PATH,
    create_codex_e18_opponent_reactive_topology,
)
from agricola.strategy.copilot.e18_opponent_reactive_v2 import (
    DEFAULT_CONFIG_PATH as COPILOT_CONFIG,
)
from agricola.strategy.copilot.e18_opponent_reactive_v2 import (
    create_copilot_e18_opponent_reactive_v2,
)
from experiments.e18.tools.common import (
    run_e18_four_agent_reactive_tournament_v2 as common,
)
from experiments.e18.tools.common import (
    run_e18_peer_v2_real_engine_intake as intake,
)

BASE_SEAT_METRICS = common._seat_metrics

MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"
OUTPUT_JSON = (
    ROOT
    / "experiments/e18/artifacts/derived/codex/"
    / "E18_2_CAPACITY_GOVERNED_V4D_DEV_GATE_V1.json"
)
OUTPUT_CSV = OUTPUT_JSON.with_suffix(".csv")

CANDIDATE = "CODEX_E18_2_CAPACITY_GOVERNED_V4D"
V4D = "CODEX_E17_V4D_CONTROL"
E18_1 = "CODEX_E18_1_ABLATION"
CLAUDE = "CLAUDE_E18_2"
COPILOT = "COPILOT_E18_2"
PARTICIPANTS = (CANDIDATE, V4D, E18_1, CLAUDE, COPILOT)
PAIRS = tuple((CANDIDATE, opponent) for opponent in PARTICIPANTS[1:])
TARGET_MONEY = 100_000.0

SOURCES = {
    CANDIDATE: ROOT
    / "src/agricola/strategy/codex/codex_e18_capacity_governed_v4d.py",
    V4D: intake.SOURCES[intake.V4D],
    E18_1: intake.SOURCES[intake.E18],
    CLAUDE: intake.SOURCES[intake.CLAUDE],
    COPILOT: intake.SOURCES[intake.COPILOT],
}
CONFIGS = {
    CANDIDATE: Path(DEFAULT_E18_CAPACITY_GOVERNED_CONFIG_PATH),
    V4D: Path(DEFAULT_V4D_CONFIG_PATH),
    E18_1: Path(DEFAULT_E18_OPPONENT_REACTIVE_CONFIG_PATH),
    CLAUDE: Path(CLAUDE_CONFIG),
    COPILOT: Path(COPILOT_CONFIG),
}


def _factory(name: str, seed: int, seat: int) -> tuple[Any, Any]:
    context = {
        "run_id": f"E18-2-DEV-GATE-S{seed}-P{seat}-{name}",
        "episode_id": f"E18-2-DEV-GATE-S{seed}-P{seat}-{name}",
        "seed": seed,
        "player_position": seat,
    }
    if name == CANDIDATE:
        policy = create_codex_e18_capacity_governed_v4d(run_context=context)
        return policy, policy.codex_e18_capacity_governed_instance
    if name == V4D:
        policy = create_codex_e17_batched_cluster_routing_v4(run_context=context)
        return policy, policy.codex_e17_batched_cluster_routing_instance
    if name == E18_1:
        policy = create_codex_e18_opponent_reactive_topology(run_context=context)
        return policy, policy.codex_e18_opponent_reactive_instance
    if name == CLAUDE:
        policy = create_claude_e18_agent_v2(run_context=context)
        return policy, policy
    if name == COPILOT:
        policy = create_copilot_e18_opponent_reactive_v2(run_context=context)
        return policy, policy
    raise ValueError(name)


def _controller_diagnostics(name: str, controller: Any) -> tuple[int, int]:
    if name in {CANDIDATE, V4D, E18_1}:
        return int(getattr(controller, "error_count", 0)), int(
            getattr(controller, "fallback_count", 0)
        )
    return intake._controller_diagnostics(name, controller)


def _regime_metrics(name: str, controller: Any) -> dict[str, Any]:
    if name == CANDIDATE:
        telemetry = controller.telemetry_snapshot()
        modes = sorted(
            {
                str(item["to"])
                for item in telemetry.get("mode_history", [])
                if isinstance(item, dict) and item.get("to")
            }
        )
        action_modes = list(telemetry.get("action_effect_modes", []))
        return {
            "final_regime": telemetry.get("mode"),
            "regime_signature": modes,
            "mode_decisions": max(0, len(telemetry.get("mode_history", [])) - 1),
            "regime_transitions": max(
                0, len(telemetry.get("mode_history", [])) - 1
            ),
            "decision_day": next(
                (
                    item.get("day")
                    for item in telemetry.get("mode_history", [])
                    if item.get("to") == "RECLAIM_CROP"
                ),
                None,
            ),
            "decision_pressure": telemetry.get("latest_opponent_pressure"),
            "action_effect_modes": action_modes,
            "no_freed_work_violations": int(
                telemetry.get("no_freed_work_violations", 0)
            ),
            "aborted_reclaim_batches": int(
                telemetry.get("aborted_reclaim_batches", 0)
            ),
        }
    if name == V4D:
        return intake._regime_metrics(intake.V4D, controller)
    if name == E18_1:
        return intake._regime_metrics(intake.E18, controller)
    if name == CLAUDE:
        return intake._regime_metrics(intake.CLAUDE, controller)
    return intake._regime_metrics(intake.COPILOT, controller)


def _farm_surface(farm: dict[str, Any]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for row in farm.get("tiles", []) or []:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            kind = str(tile.get("kind", ""))
            if kind == "PLANT":
                counts["crops"] += 1
                if not bool(tile.get("watered_today", False)):
                    counts["unwatered"] += 1
            elif kind == "WEED":
                counts["weeds"] += 1
    return {key: int(value) for key, value in counts.items()}


def _lifecycle_metrics(env: Any, seat: int) -> dict[str, int]:
    daily: list[dict[str, int]] = []
    for state in env.steps:
        observation = state[seat].get("observation", {}) or {}
        if int(observation.get("hour", -1)) != 23:
            continue
        surface = _farm_surface(common.base._farm(state, seat))
        daily.append(surface)
    return {
        "crop_tile_days_total": sum(row.get("crops", 0) for row in daily),
        "unwatered_tile_days_total": sum(
            row.get("unwatered", 0) for row in daily
        ),
        "weed_tile_days_total": sum(row.get("weeds", 0) for row in daily),
    }


def _seat_metrics(env: Any, seat: int, name: str, controller: Any) -> dict[str, Any]:
    metrics = BASE_SEAT_METRICS(env, seat, name, controller)
    metrics.update(_lifecycle_metrics(env, seat))
    if name == CANDIDATE:
        metrics.update(
            {
                key: value
                for key, value in _regime_metrics(name, controller).items()
                if key in {
                    "action_effect_modes",
                    "no_freed_work_violations",
                    "aborted_reclaim_batches",
                }
            }
        )
    return metrics


def _configure_common() -> None:
    common.PARTICIPANTS = PARTICIPANTS
    common.PAIRS = PAIRS
    common.TARGET_MONEY = TARGET_MONEY
    common.OUTPUT_JSON = OUTPUT_JSON
    common.OUTPUT_CSV = OUTPUT_CSV
    common._factory = _factory
    common._controller_diagnostics = _controller_diagnostics
    common._regime_metrics = _regime_metrics
    common._seat_metrics = _seat_metrics


def _run_spec(index: int, seed: int, p0: str, p1: str) -> tuple[int, dict[str, Any]]:
    _configure_common()
    return index, common._run_match(seed, p0, p1)


def _records(
    matches: list[dict[str, Any]], participant: str, opponent: str | None = None
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for match in matches:
        for seat in (0, 1):
            if match[f"p{seat}"] != participant:
                continue
            other = str(match[f"p{1 - seat}"])
            if opponent is not None and other != opponent:
                continue
            records.append(match[f"p{seat}_metrics"])
    return records


def _mean(records: list[dict[str, Any]], key: str) -> float:
    return statistics.mean(float(record[key]) for record in records)


def _development_gates(
    matches: list[dict[str, Any]], standings: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    candidate = _records(matches, CANDIDATE)
    candidate_direct = _records(matches, CANDIDATE, V4D)
    v4d_direct = _records(matches, V4D, CANDIDATE)
    candidate_money = _mean(candidate_direct, "money")
    v4d_money = _mean(v4d_direct, "money")
    candidate_pass = _mean(candidate_direct, "pass_actions")
    v4d_pass = _mean(v4d_direct, "pass_actions")
    candidate_weeds = _mean(candidate_direct, "weed_tile_days_total")
    v4d_weeds = _mean(v4d_direct, "weed_tile_days_total")
    action_modes = sorted(
        {
            mode
            for record in candidate
            for mode in record.get("action_effect_modes", [])
        }
    )
    checks = {
        "zero_technical_errors": standings[CANDIDATE]["technical_errors"] == 0,
        "zero_fallbacks": standings[CANDIDATE]["fallbacks"] == 0,
        "zero_verified_livestock_losses": standings[CANDIDATE][
            "verified_livestock_losses"
        ]
        == 0,
        "overall_economic_100k": standings[CANDIDATE]["money_mean"]
        >= TARGET_MONEY,
        "direct_money_not_below_v4d_minus_5pct": candidate_money
        >= v4d_money * 0.95,
        "direct_pass_not_above_v4d_plus_5pct": candidate_pass
        <= v4d_pass * 1.05,
        "direct_weed_tile_days_not_above_v4d_plus_10pct": candidate_weeds
        <= v4d_weeds * 1.10,
        "at_least_two_action_effect_modes": len(action_modes) >= 2,
        "no_freed_work_to_pass": sum(
            int(record.get("no_freed_work_violations", 0)) for record in candidate
        )
        == 0,
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "action_effect_modes": action_modes,
        "direct_vs_v4d": {
            "candidate_money_mean": candidate_money,
            "v4d_money_mean": v4d_money,
            "money_percent_vs_v4d": (candidate_money - v4d_money)
            / v4d_money
            * 100,
            "candidate_pass_mean": candidate_pass,
            "v4d_pass_mean": v4d_pass,
            "candidate_weed_tile_days_mean": candidate_weeds,
            "v4d_weed_tile_days_mean": v4d_weeds,
        },
    }


def _write_csv(matches: list[dict[str, Any]]) -> None:
    fields = [
        "seed",
        "seat",
        "participant",
        "opponent",
        "winner",
        "money",
        "pass_actions",
        "productive_actions",
        "weed_tile_days_total",
        "unwatered_tile_days_total",
        "final_regime",
        "regime_signature",
        "verified_livestock_losses",
        "technical_errors",
        "fallbacks",
    ]
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for match in matches:
            for seat in (0, 1):
                metrics = match[f"p{seat}_metrics"]
                writer.writerow(
                    {
                        "seed": match["seed"],
                        "seat": seat,
                        "participant": match[f"p{seat}"],
                        "opponent": match[f"p{1 - seat}"],
                        "winner": match["winner"],
                        **{key: metrics.get(key) for key in fields[5:]},
                        "regime_signature": "|".join(
                            metrics.get("regime_signature", [])
                        ),
                    }
                )


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    seeds = [int(value) for value in manifest["seed_policy"]["development"]]
    reserved = {
        *map(int, manifest["seed_policy"]["holdout"]["seeds"]),
        *map(int, manifest["seed_policy"]["final_confirmation"]["seeds"]),
    }
    if set(seeds).intersection(reserved):
        raise RuntimeError("development matrix overlaps a reserved seed")
    _configure_common()
    specs: list[tuple[int, int, str, str]] = []
    for left, right in PAIRS:
        for seed in seeds:
            for p0, p1 in ((left, right), (right, left)):
                specs.append((len(specs), seed, p0, p1))
    completed: dict[int, dict[str, Any]] = {}
    with ProcessPoolExecutor(max_workers=6) as executor:
        futures = {
            executor.submit(_run_spec, index, seed, p0, p1): (
                index,
                seed,
                p0,
                p1,
            )
            for index, seed, p0, p1 in specs
        }
        for future in as_completed(futures):
            index, seed, p0, p1 = futures[future]
            returned_index, match = future.result()
            if returned_index != index:
                raise RuntimeError("worker returned a mismatched matrix index")
            completed[index] = match
            print(
                f"[{len(completed):02d}/{len(specs)}] seed={seed} {p0} vs {p1} "
                f"winner={match['winner']} margin_p0={match['margin_p0']:.0f}",
                flush=True,
            )
    matches = [completed[index] for index in range(len(specs))]
    standings = common._aggregate(matches)
    provenance = {
        name: {
            "source": str(SOURCES[name].relative_to(ROOT)).replace("\\", "/"),
            "source_sha256": common._sha256(SOURCES[name]),
            "config": str(CONFIGS[name].relative_to(ROOT)).replace("\\", "/"),
            "config_sha256": common._sha256(CONFIGS[name]),
        }
        for name in PARTICIPANTS
    }
    payload = {
        "schema_version": "E18_2_CAPACITY_GOVERNED_V4D_DEV_GATE_V1",
        "epistemic_role": "DEVELOPMENT_ONLY_NON_QUALIFYING",
        "date": "2026-09-03",
        "target_money": TARGET_MONEY,
        "participants": list(PARTICIPANTS),
        "pairs": [list(pair) for pair in PAIRS],
        "seeds": seeds,
        "seats": [0, 1],
        "match_count": len(matches),
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "antigravity_excluded": True,
        "provenance": provenance,
        "standings": standings,
        "head_to_head": common._head_to_head(matches),
        "candidate_gate": _development_gates(matches, standings),
        "matches": matches,
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    _write_csv(matches)
    print(f"wrote {OUTPUT_JSON}")
    print(f"wrote {OUTPUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
