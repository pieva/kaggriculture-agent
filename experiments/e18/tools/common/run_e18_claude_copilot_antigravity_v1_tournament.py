#!/usr/bin/env python3
"""Run a short Claude/Copilot/Antigravity E18 development tournament.

Codex is intentionally absent: this round robin exists to give Antigravity's
freshly-gated E18.1 reboot a real-engine comparison point against the two
peer candidates it has never faced (Claude E18.2, Copilot E18.2), so their
next development iteration can be directed by evidence instead of guesswork.
This is diagnostic-only: no holdout or final-confirmation seed is consumed,
and no candidate is promoted or submitted from this run.
"""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import statistics
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.antigravity.antigravity_e18_reactive_reboot_v1 import (
    DEFAULT_CONFIG_PATH as ANTIGRAVITY_CONFIG,
)
from agricola.strategy.antigravity.antigravity_e18_reactive_reboot_v1 import (
    create_antigravity_e18_agent,
)
from agricola.strategy.claude.e18_opponent_reactive_v2 import (
    DEFAULT_CONFIG_PATH as CLAUDE_CONFIG,
)
from agricola.strategy.claude.e18_opponent_reactive_v2 import (
    create_claude_e18_agent_v2,
)
from agricola.strategy.copilot.e18_opponent_reactive_v2 import (
    DEFAULT_CONFIG_PATH as COPILOT_CONFIG,
)
from agricola.strategy.copilot.e18_opponent_reactive_v2 import (
    create_copilot_e18_opponent_reactive_v2,
)
from experiments.e17.tools.common import (
    run_e17_three_agent_development_tournament_v2 as base,
)
from experiments.e18.tools.common import (
    run_e18_dynamic_architecture_tournament_v1 as prior,
)

ROOT = Path(__file__).resolve().parents[4]
MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"
OUTPUT_JSON = (
    ROOT
    / "experiments/e18/artifacts/derived/common/"
    / "E18_CLAUDE_COPILOT_ANTIGRAVITY_TOURNAMENT_V1.json"
)
OUTPUT_CSV = OUTPUT_JSON.with_suffix(".csv")
TARGET_MONEY = 100_000.0

CLAUDE = "CLAUDE_E18_2"
COPILOT = "COPILOT_E18_2"
ANTIGRAVITY = "ANTIGRAVITY_E18_1"
PARTICIPANTS = (CLAUDE, COPILOT, ANTIGRAVITY)
PAIRS = tuple(itertools.combinations(PARTICIPANTS, 2))

SOURCES = {
    CLAUDE: ROOT / "src/agricola/strategy/claude/e18_opponent_reactive_v2.py",
    COPILOT: ROOT / "src/agricola/strategy/copilot/e18_opponent_reactive_v2.py",
    ANTIGRAVITY: ROOT
    / "src/agricola/strategy/antigravity/antigravity_e18_reactive_reboot_v1.py",
}
CONFIGS = {
    CLAUDE: Path(CLAUDE_CONFIG),
    COPILOT: Path(COPILOT_CONFIG),
    ANTIGRAVITY: Path(ANTIGRAVITY_CONFIG),
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


def _factory(name: str, seed: int, seat: int) -> tuple[Callable[..., Any], Any]:
    context = {
        "run_id": f"E18-CCA-V1-S{seed}-P{seat}-{name}",
        "episode_id": f"E18-CCA-V1-S{seed}-P{seat}-{name}",
        "seed": seed,
        "player_position": seat,
    }
    if name == CLAUDE:
        policy = create_claude_e18_agent_v2(run_context=context)
        return policy, policy
    if name == COPILOT:
        policy = create_copilot_e18_opponent_reactive_v2(run_context=context)
        return policy, policy
    if name == ANTIGRAVITY:
        policy = create_antigravity_e18_agent(run_context=context)
        return policy, policy.antigravity_e18_instance
    raise ValueError(name)


def _controller_diagnostics(_name: str, controller: Any) -> tuple[int, int]:
    errors = int(
        getattr(controller, "error_count", getattr(controller, "technical_errors", 0))
    )
    return errors, int(getattr(controller, "fallback_count", 0))


def _regime_metrics(name: str, controller: Any) -> dict[str, Any]:
    telemetry = controller.telemetry_snapshot()
    if name == CLAUDE:
        mode = telemetry.get("regime")
        history = [
            item.get("regime")
            for item in telemetry.get("regime_transitions", [])
            if isinstance(item, dict) and item.get("regime")
        ]
        regimes = sorted({*history, *([mode] if mode else [])})
        return {
            "final_regime": mode,
            "regime_signature": regimes,
            "mode_decisions": int(telemetry.get("mode_decisions", 0)),
            "regime_transitions": len(telemetry.get("regime_transitions", [])),
            "decision_day": telemetry.get("regime_decision_day"),
            "decision_pressure": telemetry.get("regime_decision_pressure"),
        }
    if name == COPILOT:
        mode = telemetry.get("current_regime")
        history = [str(value) for value in telemetry.get("regime_history", [])]
        regimes = sorted({*history, *([str(mode)] if mode else [])})
        return {
            "final_regime": mode,
            "regime_signature": regimes,
            "mode_decisions": int(telemetry.get("transition_count", len(history))),
            "regime_transitions": int(telemetry.get("transition_count", len(history))),
            "decision_day": telemetry.get("decision_day"),
            "decision_pressure": telemetry.get("decision_pressure"),
        }
    # ANTIGRAVITY
    mode = telemetry.get("final_regime")
    signature = [str(item) for item in telemetry.get("regime_signature", [])]
    regimes = sorted({*signature, *([str(mode)] if mode else [])})
    return {
        "final_regime": mode,
        "regime_signature": regimes,
        "mode_decisions": int(telemetry.get("mode_decisions", 0)),
        "regime_transitions": int(telemetry.get("regime_transitions", 0)),
        "decision_day": telemetry.get("decision_day"),
        "decision_pressure": telemetry.get("decision_pressure"),
    }


def _seat_metrics(env: Any, seat: int, name: str, controller: Any) -> dict[str, Any]:
    metrics = base._seat_metrics(env, seat, "E18_GENERIC", controller)
    errors, fallbacks = _controller_diagnostics(name, controller)
    metrics["technical_errors"] = errors
    metrics["fallbacks"] = fallbacks
    metrics["tile_animal_day_drops"] = metrics["animal_escapes"]
    metrics["verified_livestock_losses"] = prior._verified_livestock_losses(env, seat)
    metrics["animal_escapes"] = metrics["verified_livestock_losses"]
    terminal_farm = base._farm(env.steps[-1], seat)
    pasture_profile = prior._pasture_profile(terminal_farm)
    metrics["final_pasture_profile"] = pasture_profile
    metrics["final_pasture_profile_hash"] = _payload_hash(pasture_profile)
    metrics["action_stream_hash"] = prior._action_stream_hash(env, seat)
    metrics["action_count_profile_hash"] = _payload_hash(metrics["action_counts"])
    metrics.update(_regime_metrics(name, controller))
    metrics["regime_signature_hash"] = _payload_hash(metrics["regime_signature"])
    architecture_profile = {
        "pastures": pasture_profile,
        "final_quadrants": metrics["final_quadrants"],
        "peak_hands": metrics["peak_hands"],
        "peak_crops": metrics["peak_crops"],
        "peak_animals": metrics["peak_animals"],
        "final_crops": metrics["final_crops"],
        "final_animals": metrics["final_animals"],
        "final_weeds": metrics["final_weeds"],
        "regimes": metrics["regime_signature"],
    }
    metrics["architecture_profile_hash"] = _payload_hash(architecture_profile)
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


def _records(matches: list[dict[str, Any]], participant: str) -> list[dict[str, Any]]:
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


def _conditioned_divergence(records: list[dict[str, Any]], key: str) -> dict[str, int]:
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
        final_modes = Counter(
            str(record["metrics"]["final_regime"])
            for record in records
            if record["metrics"].get("final_regime")
        )
        activated_regimes = sorted(
            {
                regime
                for record in records
                for regime in record["metrics"].get("regime_signature", [])
            }
        )
        mode_by_opponent: dict[str, dict[str, int]] = {}
        for opponent in sorted({record["opponent"] for record in records}):
            mode_by_opponent[opponent] = dict(
                Counter(
                    str(record["metrics"]["final_regime"])
                    for record in records
                    if record["opponent"] == opponent
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
            "peak_hands_mean": _mean(records, "peak_hands"),
            "peak_crops_mean": _mean(records, "peak_crops"),
            "peak_animals_mean": _mean(records, "peak_animals"),
            "peak_weeds_mean": _mean(records, "peak_weeds"),
            "final_crops_mean": _mean(records, "final_crops"),
            "final_animals_mean": _mean(records, "final_animals"),
            "final_weeds_mean": _mean(records, "final_weeds"),
            "verified_livestock_losses": sum(
                int(record["metrics"]["verified_livestock_losses"])
                for record in records
            ),
            "tile_animal_day_drops": sum(
                int(record["metrics"]["tile_animal_day_drops"]) for record in records
            ),
            "technical_errors": sum(
                int(record["metrics"]["technical_errors"]) for record in records
            ),
            "fallbacks": sum(
                int(record["metrics"]["fallbacks"]) for record in records
            ),
            "unique_action_streams": len(
                {record["metrics"]["action_stream_hash"] for record in records}
            ),
            "unique_action_count_profiles": len(
                {record["metrics"]["action_count_profile_hash"] for record in records}
            ),
            "unique_architecture_profiles": len(
                {record["metrics"]["architecture_profile_hash"] for record in records}
            ),
            "activated_regimes": activated_regimes,
            "final_regimes": dict(final_modes),
            "mode_by_opponent": mode_by_opponent,
            "mode_decisions_mean": _mean(records, "mode_decisions"),
            "regime_transitions_mean": _mean(records, "regime_transitions"),
            "action_divergence": _conditioned_divergence(records, "action_stream_hash"),
            "architecture_divergence": _conditioned_divergence(
                records, "architecture_profile_hash"
            ),
            "regime_divergence": _conditioned_divergence(
                records, "regime_signature_hash"
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
            right_money.append(float(match[f"p{1 - left_seat}_metrics"]["money"]))
        result[f"{left}_vs_{right}"] = {
            "matches": len(rows),
            f"{left}_wins": sum(match["winner"] == left for match in rows),
            f"{right}_wins": sum(match["winner"] == right for match in rows),
            "ties": sum(match["winner"] == "TIE" for match in rows),
            f"{left}_money_mean": statistics.mean(left_money),
            f"{right}_money_mean": statistics.mean(right_money),
            f"{left}_mean_money_delta": statistics.mean(
                left_value - right_value
                for left_value, right_value in zip(left_money, right_money, strict=True)
            ),
        }
    return result


def _gates(standings: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Diagnostic-only checks: this run does not qualify or promote anyone."""

    result: dict[str, Any] = {}
    for participant in PARTICIPANTS:
        row = standings[participant]
        checks = {
            "zero_technical_errors": row["technical_errors"] == 0,
            "zero_fallbacks": row["fallbacks"] == 0,
            "zero_verified_livestock_losses": row["verified_livestock_losses"] == 0,
            "economic_m1_15k": row["money_mean"] >= 15_000.0,
        }
        result[participant] = {
            "scope": "DIAGNOSTIC_ONLY_NO_PROMOTION",
            "checks": checks,
            "passed": all(checks.values()),
        }
    return result


def _write_csv(matches: list[dict[str, Any]]) -> None:
    fields = [
        "seed",
        "seat",
        "participant",
        "opponent",
        "winner",
        "money",
        "final_regime",
        "regime_signature",
        "mode_decisions",
        "regime_transitions",
        "peak_hands",
        "peak_crops",
        "peak_animals",
        "peak_weeds",
        "final_crops",
        "final_animals",
        "final_weeds",
        "verified_livestock_losses",
        "technical_errors",
        "fallbacks",
        "action_stream_hash",
        "architecture_profile_hash",
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for match in matches:
            for seat in (0, 1):
                metrics = match[f"p{seat}_metrics"]
                row = {
                    "seed": match["seed"],
                    "seat": seat,
                    "participant": match[f"p{seat}"],
                    "opponent": match[f"p{1 - seat}"],
                    "winner": match["winner"],
                }
                row.update({field: metrics.get(field) for field in fields[5:]})
                row["regime_signature"] = "|".join(metrics.get("regime_signature", []))
                writer.writerow(row)


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    seeds = [int(value) for value in manifest["seed_policy"]["development"]]
    reserved = {
        *map(int, manifest["seed_policy"]["holdout"]["seeds"]),
        *map(int, manifest["seed_policy"]["final_confirmation"]["seeds"]),
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
        "schema_version": "E18_CLAUDE_COPILOT_ANTIGRAVITY_TOURNAMENT_V1",
        "epistemic_role": "DEVELOPMENT_ONLY_DIRECTIONAL_COMPARATOR",
        "purpose": "BASELINE_TO_DIRECT_NEXT_DEVELOPMENT_ITERATION_NOT_QUALIFICATION",
        "date": "2026-09-04",
        "engine": "kaggle_environments/kaggriculture",
        "target_money": TARGET_MONEY,
        "participants": list(PARTICIPANTS),
        "excluded_participants": {"CODEX_E18_2": "REFERENCE_LEVEL_NOT_A_PEER_IN_THIS_ROUND"},
        "pairs": [list(pair) for pair in PAIRS],
        "seeds": seeds,
        "seats": [0, 1],
        "match_count": len(matches),
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "provenance": provenance,
        "standings": standings,
        "head_to_head": _head_to_head(matches),
        "gates": _gates(standings),
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
