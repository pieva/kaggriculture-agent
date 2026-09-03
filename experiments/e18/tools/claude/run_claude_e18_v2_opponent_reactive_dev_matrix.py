#!/usr/bin/env python3
"""Development matrix: Claude E18.2 opponent-reactive V2 vs the three frozen
E18 opponents required by the remediation prompt: Codex E18.1, Copilot
E18.1, Antigravity E17 (obsolete).

Per ``E18_CLAUDE_OPPONENT_REACTIVE_V2_REMEDIATION_PROMPT_IT.md``: the seven
E18 development seeds (``180903001``-``180903007``), both seats, no
failed-run replacement, matchups reported separately (never summed into one
aggregate). All three opponents are faced only as black-box opponents (their
public factory entry points, imported the same way the common E18
four-agent tournament runner already does -- never their source, config or
MODEL_SPEC).
"""

from __future__ import annotations

import csv
import hashlib
import json
import statistics
import sys
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
SRC_ROOT = REPOSITORY_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from kaggle_environments import make

from agricola.strategy.antigravity.antigravity_e17_native_3q import (
    DEFAULT_CONFIG_PATH as ANTIGRAVITY_CONFIG,
)
from agricola.strategy.antigravity.antigravity_e17_native_3q import (
    create_e17_native_agent as create_antigravity_agent,
)
from agricola.strategy.claude.e18_opponent_reactive_v2 import (
    DEFAULT_CONFIG_PATH as CANDIDATE_CONFIG,
)
from agricola.strategy.claude.e18_opponent_reactive_v2 import (
    claude_policy_fingerprint,
    create_claude_e18_agent_v2,
)
from agricola.strategy.codex.codex_e18_opponent_reactive_topology import (
    DEFAULT_E18_OPPONENT_REACTIVE_CONFIG_PATH as CODEX_CONFIG,
)
from agricola.strategy.codex.codex_e18_opponent_reactive_topology import (
    create_codex_e18_opponent_reactive_topology,
)
from agricola.strategy.copilot.e18_opponent_reactive_v1 import (
    DEFAULT_CONFIG_PATH as COPILOT_CONFIG,
)
from agricola.strategy.copilot.e18_opponent_reactive_v1 import (
    create_copilot_e18_opponent_reactive_v1,
)
from experiments.e17.tools.common import (
    run_e17_three_agent_development_tournament_v2 as base,
)

CANDIDATE = "CLAUDE_E18_2_V2"
CODEX = "CODEX_E18_1"
COPILOT = "COPILOT_E18_1"
ANTIGRAVITY = "ANTIGRAVITY_E17_OBSOLETE"
OPPONENTS = (CODEX, COPILOT, ANTIGRAVITY)

MANIFEST_PATH = REPOSITORY_ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"
OUTPUT_JSON = (
    REPOSITORY_ROOT
    / "experiments/e18/artifacts/derived/claude/E18_CLAUDE_OPPONENT_REACTIVE_V2_DEV_MATRIX.json"
)
OUTPUT_CSV = OUTPUT_JSON.with_suffix(".csv")
TARGET_MONEY = 100_000.0
M1_MEAN_FLOOR = 16_000.0
M1_PER_MATCHUP_FLOOR = 10_000.0
M2_MEAN_FLOOR = 25_000.0

SOURCES = {
    CANDIDATE: REPOSITORY_ROOT / "src/agricola/strategy/claude/e18_opponent_reactive_v2.py",
}
CONFIGS = {
    CANDIDATE: Path(CANDIDATE_CONFIG),
    CODEX: Path(CODEX_CONFIG),
    COPILOT: Path(COPILOT_CONFIG),
    ANTIGRAVITY: Path(ANTIGRAVITY_CONFIG),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _payload_hash(payload: Any) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest().upper()


def _factory(name: str, seed: int, seat: int) -> tuple[Any, Any]:
    context = {
        "run_id": f"E18-CLAUDE-V2-S{seed}-P{seat}-{name}",
        "episode_id": f"E18-CLAUDE-V2-S{seed}-P{seat}-{name}",
        "seed": seed,
        "player_position": seat,
    }
    if name == CANDIDATE:
        policy = create_claude_e18_agent_v2(run_context=context)
        return policy, policy
    if name == CODEX:
        policy = create_codex_e18_opponent_reactive_topology(run_context=context)
        return policy, policy.codex_e18_opponent_reactive_instance
    if name == COPILOT:
        policy = create_copilot_e18_opponent_reactive_v1(run_context=context)
        return policy, policy
    if name == ANTIGRAVITY:
        policy = create_antigravity_agent(run_context=context)
        return policy, policy.antigravity_e17_native_instance
    raise ValueError(name)


def _action_stream_hash(env: Any, seat: int) -> str:
    actions = [
        state[seat].get("action") for state in env.steps if state[seat].get("action") is not None
    ]
    return _payload_hash(actions)


def _verified_livestock_losses(env: Any, seat: int) -> int:
    """Day-boundary resource losses across tile + shed + inventories, not
    just tile-level drops (which can be a tile-to-shed transfer, not a
    real loss) -- same definition the E18 common tournament runners use."""

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
            if isinstance(tile, dict) and tile.get("animal") in {"COW", "SHEEP", "GOOSE"}
        )
        shed = private.get("shed", {}) or {}
        resources += sum(max(0, int(shed.get(item, 0))) for item in ("COW", "SHEEP", "GOOSE"))
        for inventory in private.get("inventories", []) or []:
            if not isinstance(inventory, dict):
                continue
            resources += sum(
                max(0, int(inventory.get(item, 0))) for item in ("COW", "SHEEP", "GOOSE")
            )
        if previous_day is not None:
            losses += max(0, previous_resources - resources)
        previous_day = day
        previous_resources = resources
    return losses


def _terminal_sellable_residual(env: Any, seat: int) -> int:
    observation = env.steps[-1][seat].get("observation", {}) or {}
    private = observation.get("private", {}) or {}
    shed = private.get("shed", {}) or {}
    sellable = ("CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "WHEAT")
    residual = sum(max(0, int(shed.get(item, 0))) for item in sellable)
    for inventory in private.get("inventories", []) or []:
        if not isinstance(inventory, dict):
            continue
        residual += sum(max(0, int(inventory.get(item, 0))) for item in sellable)
    return residual


def _run_match(seed: int, candidate_seat: int, opponent: str) -> dict[str, Any]:
    p0, p1 = (CANDIDATE, opponent) if candidate_seat == 0 else (opponent, CANDIDATE)
    policy0, controller0 = _factory(p0, seed, 0)
    policy1, controller1 = _factory(p1, seed, 1)
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=False,
    )
    env.run([policy0, policy1])
    metrics0 = base._seat_metrics(env, 0, p0, controller0)
    metrics1 = base._seat_metrics(env, 1, p1, controller1)
    metrics0["verified_livestock_losses"] = _verified_livestock_losses(env, 0)
    metrics1["verified_livestock_losses"] = _verified_livestock_losses(env, 1)
    metrics0["action_stream_hash"] = _action_stream_hash(env, 0)
    metrics1["action_stream_hash"] = _action_stream_hash(env, 1)
    metrics0["terminal_sellable_residual"] = _terminal_sellable_residual(env, 0)
    metrics1["terminal_sellable_residual"] = _terminal_sellable_residual(env, 1)
    candidate_controller = controller0 if candidate_seat == 0 else controller1
    telemetry = candidate_controller.telemetry_snapshot()
    winner = p0 if metrics0["money"] > metrics1["money"] else (
        p1 if metrics1["money"] > metrics0["money"] else "TIE"
    )
    return {
        "seed": seed,
        "opponent": opponent,
        "candidate_seat": candidate_seat,
        "winner": winner,
        "candidate_metrics": metrics0 if candidate_seat == 0 else metrics1,
        "opponent_metrics": metrics1 if candidate_seat == 0 else metrics0,
        "candidate_telemetry": telemetry,
    }


def _mean(values: list[float]) -> float:
    return statistics.mean(values) if values else 0.0


def _matchup_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    candidate_money = [float(r["candidate_metrics"]["money"]) for r in records]
    opponent_money = [float(r["opponent_metrics"]["money"]) for r in records]
    paired_delta = [c - o for c, o in zip(candidate_money, opponent_money, strict=True)]
    return {
        "matches": len(records),
        "wins": sum(r["winner"] == CANDIDATE for r in records),
        "losses": sum(r["winner"] not in (CANDIDATE, "TIE") for r in records),
        "ties": sum(r["winner"] == "TIE" for r in records),
        "candidate_money_mean": _mean(candidate_money),
        "candidate_money_median": statistics.median(candidate_money) if candidate_money else 0.0,
        "candidate_money_min": min(candidate_money) if candidate_money else 0.0,
        "candidate_money_max": max(candidate_money) if candidate_money else 0.0,
        "opponent_money_mean": _mean(opponent_money),
        "paired_delta_mean": _mean(paired_delta),
        "runs_below_10000": sum(1 for m in candidate_money if m < 10000.0),
        "verified_livestock_losses": sum(
            int(r["candidate_metrics"]["verified_livestock_losses"]) for r in records
        ),
        "technical_errors": sum(
            int(r["candidate_metrics"].get("technical_errors", 0) or 0) for r in records
        ),
        "fallbacks": sum(
            int(r["candidate_metrics"].get("fallbacks", 0) or 0) for r in records
        ),
        "unique_action_streams": len({r["candidate_metrics"]["action_stream_hash"] for r in records}),
        "unique_regimes": sorted({r["candidate_telemetry"]["regime"] for r in records}),
        "mode_decision_rate": _mean(
            [float(r["candidate_telemetry"]["mode_decisions"]) for r in records]
        ),
        "terminal_sellable_residual_mean": _mean(
            [float(r["candidate_metrics"]["terminal_sellable_residual"]) for r in records]
        ),
        "peak_crops_mean": _mean([float(r["candidate_metrics"]["peak_crops"]) for r in records]),
        "peak_animals_mean": _mean(
            [float(r["candidate_metrics"]["peak_animals"]) for r in records]
        ),
        "move_actions_mean": _mean(
            [float(r["candidate_metrics"]["move_actions"]) for r in records]
        ),
        "pass_actions_mean": _mean(
            [float(r["candidate_metrics"]["pass_actions"]) for r in records]
        ),
        "productive_actions_mean": _mean(
            [float(r["candidate_metrics"]["productive_actions"]) for r in records]
        ),
    }


def _conditioned_divergence(records: list[dict[str, Any]], key_fn) -> dict[str, int]:
    groups: dict[tuple[int, int], list[dict[str, Any]]] = {}
    for record in records:
        groups.setdefault((record["seed"], record["candidate_seat"]), []).append(record)
    eligible = [values for values in groups.values() if len(values) > 1]
    divergent = [values for values in eligible if len({key_fn(r) for r in values}) > 1]
    return {"eligible_seed_seat_groups": len(eligible), "divergent_groups": len(divergent)}


def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    seeds = [int(v) for v in manifest["seed_policy"]["development"]]
    reserved = {
        *map(int, manifest["seed_policy"]["holdout"]["seeds"]),
        *map(int, manifest["seed_policy"]["final_confirmation"]["seeds"]),
    }
    if set(seeds).intersection(reserved):
        raise RuntimeError("development matrix overlaps a reserved seed")

    provenance = {
        CANDIDATE: {
            "source": str(SOURCES[CANDIDATE].relative_to(REPOSITORY_ROOT)).replace("\\", "/"),
            "source_sha256": _sha256(SOURCES[CANDIDATE]),
            "config": str(CONFIGS[CANDIDATE].relative_to(REPOSITORY_ROOT)).replace("\\", "/"),
            "config_sha256": _sha256(CONFIGS[CANDIDATE]),
            "policy_fingerprint": claude_policy_fingerprint(),
        },
        CODEX: {
            "config": str(CONFIGS[CODEX].relative_to(REPOSITORY_ROOT)).replace("\\", "/"),
            "config_sha256": _sha256(CONFIGS[CODEX]),
            "note": "black-box opponent: source not read by this runner or this session",
        },
        COPILOT: {
            "config": str(CONFIGS[COPILOT].relative_to(REPOSITORY_ROOT)).replace("\\", "/"),
            "config_sha256": _sha256(CONFIGS[COPILOT]),
            "note": "black-box opponent: source not read by this runner or this session",
        },
        ANTIGRAVITY: {
            "config": str(CONFIGS[ANTIGRAVITY].relative_to(REPOSITORY_ROOT)).replace("\\", "/"),
            "config_sha256": _sha256(CONFIGS[ANTIGRAVITY]),
            "note": "black-box opponent: source not read by this runner or this session",
        },
    }

    matches: list[dict[str, Any]] = []
    total = len(OPPONENTS) * len(seeds) * 2
    for opponent in OPPONENTS:
        for seed in seeds:
            for candidate_seat in (0, 1):
                record = _run_match(seed, candidate_seat, opponent)
                matches.append(record)
                cm = record["candidate_metrics"]
                om = record["opponent_metrics"]
                print(
                    f"[{len(matches):02d}/{total}] seed={seed} vs {opponent} "
                    f"seat={candidate_seat} candidate={cm['money']:.0f} "
                    f"opponent={om['money']:.0f} winner={record['winner']} "
                    f"regime={record['candidate_telemetry']['regime']} "
                    f"3Q={cm['final_quadrants']} vll={cm['verified_livestock_losses']} "
                    f"residual={cm['terminal_sellable_residual']}",
                    flush=True,
                )

    by_opponent = {
        opponent: [m for m in matches if m["opponent"] == opponent] for opponent in OPPONENTS
    }
    matchups = {opponent: _matchup_summary(records) for opponent, records in by_opponent.items()}
    overall_candidate_money = [float(m["candidate_metrics"]["money"]) for m in matches]

    action_divergence = _conditioned_divergence(
        matches, lambda r: r["candidate_metrics"]["action_stream_hash"]
    )
    architecture_divergence = _conditioned_divergence(
        matches,
        lambda r: (
            r["candidate_metrics"]["final_quadrants"],
            r["candidate_metrics"]["peak_animals"],
        ),
    )

    gates = {
        "technical_zero_errors": sum(m["technical_errors"] for m in matchups.values()) == 0,
        "technical_zero_fallbacks": sum(m["fallbacks"] for m in matchups.values()) == 0,
        "safety_zero_verified_livestock_losses": sum(
            m["verified_livestock_losses"] for m in matchups.values()
        )
        == 0,
        "verified_livestock_losses_total": sum(
            m["verified_livestock_losses"] for m in matchups.values()
        ),
        "dynamic_two_regimes_activated": len(
            {r for m in matchups.values() for r in m["unique_regimes"]}
        )
        >= 2,
        "dynamic_one_decision_per_run": all(
            m["mode_decision_rate"] == 1.0 for m in matchups.values()
        ),
        "dynamic_action_divergence": action_divergence,
        "dynamic_action_divergence_gate": (
            action_divergence["divergent_groups"] >= 12
            if action_divergence["eligible_seed_seat_groups"] >= 12
            else action_divergence["divergent_groups"] == action_divergence["eligible_seed_seat_groups"]
        ),
        "dynamic_architecture_divergence": architecture_divergence,
        "economic_m1_mean_ge_16000": _mean(overall_candidate_money) >= M1_MEAN_FLOOR,
        "economic_m1_no_matchup_below_10000": all(
            m["candidate_money_mean"] >= M1_PER_MATCHUP_FLOOR for m in matchups.values()
        ),
        "economic_m2_mean_ge_25000": _mean(overall_candidate_money) >= M2_MEAN_FLOOR,
        "economic_overall_mean": _mean(overall_candidate_money),
        "economic_target_100000_gap": TARGET_MONEY - _mean(overall_candidate_money),
        "efficiency_terminal_sellable_residual_mean": _mean(
            [m["terminal_sellable_residual_mean"] for m in matchups.values()]
        ),
    }

    payload = {
        "schema_version": "E18_CLAUDE_OPPONENT_REACTIVE_V2_DEV_MATRIX",
        "epistemic_role": "DEVELOPMENT_ONLY_NON_QUALIFYING",
        "date": "2026-09-03",
        "candidate": CANDIDATE,
        "opponents": list(OPPONENTS),
        "seeds": seeds,
        "seats": [0, 1],
        "match_count": len(matches),
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "provenance": provenance,
        "matchups": matchups,
        "gates": gates,
        "matches": matches,
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    fields = [
        "seed",
        "opponent",
        "candidate_seat",
        "winner",
        "candidate_money",
        "opponent_money",
        "regime",
        "final_quadrants",
        "peak_crops",
        "peak_animals",
        "peak_weeds",
        "verified_livestock_losses",
        "terminal_sellable_residual",
        "move_actions",
        "productive_actions",
        "pass_actions",
        "technical_errors",
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for m in matches:
            cm = m["candidate_metrics"]
            om = m["opponent_metrics"]
            writer.writerow(
                {
                    "seed": m["seed"],
                    "opponent": m["opponent"],
                    "candidate_seat": m["candidate_seat"],
                    "winner": m["winner"],
                    "candidate_money": cm["money"],
                    "opponent_money": om["money"],
                    "regime": m["candidate_telemetry"]["regime"],
                    "final_quadrants": cm["final_quadrants"],
                    "peak_crops": cm["peak_crops"],
                    "peak_animals": cm["peak_animals"],
                    "peak_weeds": cm["peak_weeds"],
                    "verified_livestock_losses": cm["verified_livestock_losses"],
                    "terminal_sellable_residual": cm["terminal_sellable_residual"],
                    "move_actions": cm["move_actions"],
                    "productive_actions": cm["productive_actions"],
                    "pass_actions": cm["pass_actions"],
                    "technical_errors": cm.get("technical_errors", 0),
                }
            )

    print(f"wrote {OUTPUT_JSON}")
    print(f"wrote {OUTPUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
