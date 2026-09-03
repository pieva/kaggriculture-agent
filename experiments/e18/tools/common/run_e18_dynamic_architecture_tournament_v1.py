#!/usr/bin/env python3
"""Run the preregistered E18 dynamic-architecture development tournament.

The matrix uses development seeds only.  It measures economic and operational
KPIs together with opponent-conditioned action/topology divergence; no static
score alone can satisfy the architecture gate.
"""

from __future__ import annotations

import csv
import hashlib
import json
import statistics
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.claude.e17_reactive_3q_v3 import (
    DEFAULT_CONFIG_PATH as CLAUDE_CONFIG,
)
from agricola.strategy.claude.e17_reactive_3q_v3 import (
    create_claude_e17_agent_v3,
)
from agricola.strategy.codex.codex_e17_topology_cap_662 import (
    DEFAULT_TOPOLOGY_662_CONFIG_PATH,
    create_codex_e17_topology_cap_662,
)
from agricola.strategy.codex.codex_e18_opponent_reactive_topology import (
    DEFAULT_E18_OPPONENT_REACTIVE_CONFIG_PATH,
    create_codex_e18_opponent_reactive_topology,
)
from agricola.strategy.copilot.e17_native_3q import (
    DEFAULT_CONFIG_PATH as COPILOT_CONFIG,
)
from agricola.strategy.copilot.e17_native_3q import create_native_agent
from experiments.e17.tools.common import (
    run_e17_three_agent_development_tournament_v2 as base,
)

ROOT = Path(__file__).resolve().parents[4]
MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"
OUTPUT_JSON = (
    ROOT
    / "experiments/e18/artifacts/derived/common/"
    / "E18_DYNAMIC_ARCHITECTURE_TOURNAMENT_V1.json"
)
OUTPUT_CSV = OUTPUT_JSON.with_suffix(".csv")
TARGET_MONEY = 100_000.0

CODEX_E18 = "CODEX_E18_REACTIVE_662_770"
CODEX_CONTROL = "CODEX_662_CONTROL"
CLAUDE = "CLAUDE_V3"
COPILOT = "COPILOT_NATIVE"
PARTICIPANTS = (CODEX_E18, CODEX_CONTROL, CLAUDE, COPILOT)
PAIRS = (
    (CODEX_E18, CODEX_CONTROL),
    (CODEX_E18, CLAUDE),
    (CODEX_E18, COPILOT),
    (CLAUDE, COPILOT),
)
SOURCES = {
    CODEX_E18: ROOT
    / "src/agricola/strategy/codex/codex_e18_opponent_reactive_topology.py",
    CODEX_CONTROL: ROOT
    / "src/agricola/strategy/codex/codex_e17_topology_cap_662.py",
    CLAUDE: ROOT / "src/agricola/strategy/claude/e17_reactive_3q_v3.py",
    COPILOT: ROOT / "src/agricola/strategy/copilot/e17_native_3q.py",
}
CONFIGS = {
    CODEX_E18: Path(DEFAULT_E18_OPPONENT_REACTIVE_CONFIG_PATH),
    CODEX_CONTROL: Path(DEFAULT_TOPOLOGY_662_CONFIG_PATH),
    CLAUDE: Path(CLAUDE_CONFIG),
    COPILOT: Path(COPILOT_CONFIG),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _payload_hash(payload: Any) -> str:
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest().upper()


def _factory(
    name: str,
    seed: int,
    seat: int,
) -> tuple[Callable[..., Any], Any]:
    context = {
        "run_id": f"E18-DYNAMIC-V1-S{seed}-P{seat}-{name}",
        "episode_id": f"E18-DYNAMIC-V1-S{seed}-P{seat}-{name}",
        "seed": seed,
        "player_position": seat,
    }
    if name == CODEX_E18:
        policy = create_codex_e18_opponent_reactive_topology(
            run_context=context
        )
        return policy, policy.codex_e18_opponent_reactive_instance
    if name == CODEX_CONTROL:
        policy = create_codex_e17_topology_cap_662(run_context=context)
        return policy, policy.codex_e17_topology_662_instance
    if name == CLAUDE:
        policy = create_claude_e17_agent_v3(run_context=context)
        return policy, policy
    if name == COPILOT:
        policy = create_native_agent()
        return policy, policy
    raise ValueError(name)


def _quadrant(position: tuple[int, int]) -> str:
    x, y = position
    if x < 5 and y < 5:
        return "Q0"
    if x >= 5 and y < 5:
        return "Q1"
    if x < 5 and y >= 5:
        return "Q2"
    return "Q3"


def _pasture_profile(farm: dict[str, Any]) -> dict[str, dict[str, int]]:
    built: Counter[str] = Counter()
    filled: Counter[str] = Counter()
    for y, row in enumerate(farm.get("tiles", []) or []):
        for x, tile in enumerate(row):
            if not isinstance(tile, dict) or tile.get("kind") != "PASTURE":
                continue
            quadrant = _quadrant((x, y))
            built[quadrant] += 1
            if tile.get("animal"):
                filled[quadrant] += 1
    return {
        "built": {key: built[key] for key in ("Q0", "Q1", "Q2", "Q3")},
        "filled": {key: filled[key] for key in ("Q0", "Q1", "Q2", "Q3")},
    }


def _action_stream_hash(env: Any, seat: int) -> str:
    actions = [
        state[seat].get("action")
        for state in env.steps
        if state[seat].get("action") is not None
    ]
    return _payload_hash(actions)


def _verified_livestock_losses(env: Any, seat: int) -> int:
    """Count day-boundary resource losses, including shed and inventories."""

    losses = 0
    previous_day: int | None = None
    previous_resources = 0
    for state in env.steps:
        observation = state[seat].get("observation", {}) or {}
        day = int(observation.get("day", 0))
        if day == previous_day:
            continue
        farm = base._farm(state, seat)
        private = observation.get("private", {}) or {}
        resources = sum(
            1
            for row in farm.get("tiles", []) or []
            for tile in row
            if isinstance(tile, dict) and tile.get("animal") in {"COW", "SHEEP"}
        )
        shed = private.get("shed", {}) or {}
        resources += sum(max(0, int(shed.get(item, 0))) for item in ("COW", "SHEEP"))
        for inventory in private.get("inventories", []) or []:
            if not isinstance(inventory, dict):
                continue
            resources += sum(
                max(0, int(inventory.get(item, 0)))
                for item in ("COW", "SHEEP")
            )
        if previous_day is not None:
            losses += max(0, previous_resources - resources)
        previous_day = day
        previous_resources = resources
    return losses


def _seat_metrics(
    env: Any,
    seat: int,
    name: str,
    controller: Any,
) -> dict[str, Any]:
    diagnostic = "CODEX_662" if name == CODEX_CONTROL else name
    metrics = base._seat_metrics(env, seat, diagnostic, controller)
    metrics["tile_animal_day_drops"] = metrics["animal_escapes"]
    metrics["verified_livestock_losses"] = _verified_livestock_losses(env, seat)
    metrics["animal_escapes"] = metrics["verified_livestock_losses"]
    terminal_farm = base._farm(env.steps[-1], seat)
    metrics["final_pasture_profile"] = _pasture_profile(terminal_farm)
    metrics["final_pasture_profile_hash"] = _payload_hash(
        metrics["final_pasture_profile"]
    )
    metrics["action_stream_hash"] = _action_stream_hash(env, seat)
    metrics["action_count_profile_hash"] = _payload_hash(
        metrics["action_counts"]
    )
    if name == CODEX_E18:
        telemetry = controller.telemetry_snapshot()
        metrics.update(
            {
                "topology_mode": telemetry["topology_mode"],
                "mode_decision_day": telemetry["mode_decision_day"],
                "mode_decision_pressure": telemetry[
                    "mode_decision_pressure"
                ],
                "mode_decision_features": telemetry[
                    "mode_decision_features"
                ],
                "mode_decisions": telemetry["mode_decisions"],
                "unique_regimes": telemetry["unique_regimes"],
                "regime_transition_count": len(
                    telemetry["regime_transitions"]
                ),
                "unique_public_opponent_snapshots": telemetry[
                    "unique_public_opponent_snapshots"
                ],
                "target_pastures_built": telemetry[
                    "latest_target_pastures_built"
                ],
                "target_pastures_filled": telemetry[
                    "latest_target_pastures_filled"
                ],
                "empty_target_pastures": telemetry[
                    "latest_empty_target_pastures"
                ],
                "max_q2_pastures": telemetry["max_observed_q2_pastures"],
                "topology_cap_breaches": telemetry[
                    "topology_cap_breaches"
                ],
                "persistent_fill_batches": telemetry[
                    "persistent_fill_batches"
                ],
            }
        )
    return metrics


def _run_match(seed: int, p0: str, p1: str) -> dict[str, Any]:
    policy0, controller0 = _factory(p0, seed, 0)
    policy1, controller1 = _factory(p1, seed, 1)
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=False,
    )
    env.run([policy0, policy1])
    metrics0 = _seat_metrics(env, 0, p0, controller0)
    metrics1 = _seat_metrics(env, 1, p1, controller1)
    if metrics0["money"] > metrics1["money"]:
        winner = p0
    elif metrics1["money"] > metrics0["money"]:
        winner = p1
    else:
        winner = "TIE"
    return {
        "seed": seed,
        "p0": p0,
        "p1": p1,
        "winner": winner,
        "margin_p0": metrics0["money"] - metrics1["money"],
        "p0_metrics": metrics0,
        "p1_metrics": metrics1,
    }


def _records(
    matches: list[dict[str, Any]],
    participant: str,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for match in matches:
        for seat in (0, 1):
            if match[f"p{seat}"] != participant:
                continue
            records.append(
                {
                    "seed": match["seed"],
                    "seat": seat,
                    "opponent": match[f"p{1 - seat}"],
                    "winner": match["winner"],
                    "metrics": match[f"p{seat}_metrics"],
                }
            )
    return records


def _mean(records: list[dict[str, Any]], key: str) -> float | None:
    values = [
        float(record["metrics"][key])
        for record in records
        if record["metrics"].get(key) is not None
    ]
    return statistics.mean(values) if values else None


def _conditioned_divergence(
    records: list[dict[str, Any]],
    key: str,
) -> dict[str, int]:
    groups: dict[tuple[int, int], list[dict[str, Any]]] = {}
    for record in records:
        groups.setdefault((record["seed"], record["seat"]), []).append(record)
    eligible = [values for values in groups.values() if len(values) > 1]
    divergent = [
        values
        for values in eligible
        if len({record["metrics"].get(key) for record in values}) > 1
    ]
    return {
        "eligible_seed_seat_groups": len(eligible),
        "divergent_groups": len(divergent),
    }


def _aggregate(matches: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    standings: dict[str, dict[str, Any]] = {}
    for participant in PARTICIPANTS:
        records = _records(matches, participant)
        money = [float(record["metrics"]["money"]) for record in records]
        wins = sum(record["winner"] == participant for record in records)
        ties = sum(record["winner"] == "TIE" for record in records)
        modes = Counter(
            str(record["metrics"]["topology_mode"])
            for record in records
            if record["metrics"].get("topology_mode")
        )
        mode_by_opponent: dict[str, dict[str, int]] = {}
        for opponent in sorted({record["opponent"] for record in records}):
            mode_by_opponent[opponent] = dict(
                Counter(
                    str(record["metrics"]["topology_mode"])
                    for record in records
                    if record["opponent"] == opponent
                    and record["metrics"].get("topology_mode")
                )
            )
        standings[participant] = {
            "matches": len(records),
            "wins": wins,
            "losses": len(records) - wins - ties,
            "ties": ties,
            "money_mean": statistics.mean(money),
            "money_median": statistics.median(money),
            "money_min": min(money),
            "money_max": max(money),
            "money_stdev": statistics.pstdev(money),
            "target_attainment_pct": statistics.mean(money) / TARGET_MONEY * 100,
            "target_gap": TARGET_MONEY - statistics.mean(money),
            "peak_crops_mean": _mean(records, "peak_crops"),
            "peak_animals_mean": _mean(records, "peak_animals"),
            "peak_weeds_mean": _mean(records, "peak_weeds"),
            "animal_escapes": sum(
                int(record["metrics"]["animal_escapes"])
                for record in records
            ),
            "tile_animal_day_drops": sum(
                int(record["metrics"]["tile_animal_day_drops"])
                for record in records
            ),
            "verified_livestock_losses": sum(
                int(record["metrics"]["verified_livestock_losses"])
                for record in records
            ),
            "technical_errors": sum(
                int(record["metrics"]["technical_errors"])
                for record in records
            ),
            "fallbacks": sum(
                int(record["metrics"]["fallbacks"])
                for record in records
            ),
            "unique_action_streams": len(
                {
                    record["metrics"]["action_stream_hash"]
                    for record in records
                }
            ),
            "unique_action_count_profiles": len(
                {
                    record["metrics"]["action_count_profile_hash"]
                    for record in records
                }
            ),
            "unique_final_pasture_profiles": len(
                {
                    record["metrics"]["final_pasture_profile_hash"]
                    for record in records
                }
            ),
            "opponent_conditioned_action_divergence": _conditioned_divergence(
                records, "action_stream_hash"
            ),
            "opponent_conditioned_topology_divergence": _conditioned_divergence(
                records, "final_pasture_profile_hash"
            ),
            "topology_modes": dict(modes),
            "mode_by_opponent": mode_by_opponent,
            "mode_decision_rate": (
                sum(int(record["metrics"].get("mode_decisions", 0)) for record in records)
                / len(records)
                if records
                else None
            ),
            "unique_regimes_mean": _mean(records, "unique_regimes"),
            "regime_transitions_mean": _mean(
                records, "regime_transition_count"
            ),
            "unique_public_opponent_snapshots_mean": _mean(
                records, "unique_public_opponent_snapshots"
            ),
            "target_pastures_built_mean": _mean(
                records, "target_pastures_built"
            ),
            "target_pastures_filled_mean": _mean(
                records, "target_pastures_filled"
            ),
            "empty_target_pastures_mean": _mean(
                records, "empty_target_pastures"
            ),
            "topology_cap_breaches": sum(
                int(record["metrics"].get("topology_cap_breaches", 0))
                for record in records
            ),
        }
    return standings


def _head_to_head(matches: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for left, right in PAIRS:
        rows = [
            match
            for match in matches
            if {match["p0"], match["p1"]} == {left, right}
        ]
        left_money: list[float] = []
        right_money: list[float] = []
        for match in rows:
            left_seat = 0 if match["p0"] == left else 1
            left_money.append(float(match[f"p{left_seat}_metrics"]["money"]))
            right_money.append(
                float(match[f"p{1 - left_seat}_metrics"]["money"])
            )
        result[f"{left}_vs_{right}"] = {
            "matches": len(rows),
            f"{left}_wins": sum(match["winner"] == left for match in rows),
            f"{right}_wins": sum(match["winner"] == right for match in rows),
            "ties": sum(match["winner"] == "TIE" for match in rows),
            f"{left}_money_mean": statistics.mean(left_money),
            f"{right}_money_mean": statistics.mean(right_money),
            f"{left}_mean_money_delta": statistics.mean(
                a - b for a, b in zip(left_money, right_money, strict=True)
            ),
        }
    return result


def _architecture_gate(standings: dict[str, dict[str, Any]]) -> dict[str, Any]:
    candidate = standings[CODEX_E18]
    action = candidate["opponent_conditioned_action_divergence"]
    topology = candidate["opponent_conditioned_topology_divergence"]
    checks = {
        "zero_technical_errors": candidate["technical_errors"] == 0,
        "zero_fallbacks": candidate["fallbacks"] == 0,
        "one_decision_per_run": candidate["mode_decision_rate"] == 1.0,
        "both_topology_modes_activated": set(candidate["topology_modes"])
        == {"6-6-2", "7-7-0"},
        "opponent_conditioned_action_divergence": action["divergent_groups"]
        == action["eligible_seed_seat_groups"],
        "opponent_conditioned_topology_divergence": topology[
            "divergent_groups"
        ]
        > 0,
        "fourteen_pastures_built_mean": candidate[
            "target_pastures_built_mean"
        ]
        == 14.0,
        "fourteen_pastures_filled_mean": candidate[
            "target_pastures_filled_mean"
        ]
        == 14.0,
        "zero_topology_breaches": candidate["topology_cap_breaches"] == 0,
        "zero_verified_livestock_losses": candidate[
            "verified_livestock_losses"
        ]
        == 0,
    }
    return {"checks": checks, "passed": all(checks.values())}


def _write_csv(matches: list[dict[str, Any]]) -> None:
    fields = [
        "seed",
        "seat",
        "participant",
        "opponent",
        "winner",
        "money",
        "topology_mode",
        "mode_decision_pressure",
        "target_pastures_built",
        "target_pastures_filled",
        "empty_target_pastures",
        "peak_crops",
        "peak_animals",
        "peak_weeds",
        "animal_escapes",
        "tile_animal_day_drops",
        "verified_livestock_losses",
        "move_actions",
        "productive_actions",
        "pass_actions",
        "technical_errors",
        "fallbacks",
        "action_stream_hash",
        "final_pasture_profile_hash",
    ]
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
                        **{field: metrics.get(field) for field in fields[5:]},
                    }
                )


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    seeds = [int(value) for value in manifest["seed_policy"]["development"]]
    reserved = {
        *map(int, manifest["seed_policy"]["holdout"]["seeds"]),
        *map(
            int,
            manifest["seed_policy"]["final_confirmation"]["seeds"],
        ),
    }
    if set(seeds).intersection(reserved):
        raise RuntimeError("development matrix overlaps a reserved seed")
    provenance = {
        name: {
            "source": str(SOURCES[name].relative_to(ROOT)).replace("\\", "/"),
            "source_sha256": _sha256(SOURCES[name]),
            "config": str(CONFIGS[name].relative_to(ROOT)).replace("\\", "/"),
            "config_sha256": _sha256(CONFIGS[name]),
        }
        for name in PARTICIPANTS
    }
    matches: list[dict[str, Any]] = []
    total = len(PAIRS) * len(seeds) * 2
    for left, right in PAIRS:
        for seed in seeds:
            for p0, p1 in ((left, right), (right, left)):
                match = _run_match(seed, p0, p1)
                matches.append(match)
                print(
                    f"[{len(matches):02d}/{total}] seed={seed} {p0} vs {p1} "
                    f"winner={match['winner']} margin_p0={match['margin_p0']:.0f}",
                    flush=True,
                )
    standings = _aggregate(matches)
    payload = {
        "schema_version": "E18_DYNAMIC_ARCHITECTURE_TOURNAMENT_V1",
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
        "provenance": provenance,
        "standings": standings,
        "head_to_head": _head_to_head(matches),
        "architecture_gate": _architecture_gate(standings),
        "matches": matches,
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_csv(matches)
    print(f"wrote {OUTPUT_JSON}")
    print(f"wrote {OUTPUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
