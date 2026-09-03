#!/usr/bin/env python3
"""Development matrix: Claude E18.1 opponent-reactive V1 vs Claude V3,
Codex E18 black-box, and Copilot Native.

Per ``E18_CLAUDE_OPPONENT_REACTIVE_V1_BUILD_PROMPT_IT.md``: the E18
development seeds (``180903001``-``180903007``), both seats, no failed-run
replacement, matchups reported separately (never summed into one
aggregate). Codex E18 is faced only as a black-box opponent (its public
factory entry point, imported the same way the common E18 tournament
runner already does -- never its source, config or MODEL_SPEC). Claude V3
and the shared metrics helpers (`_farm`, `_seat_metrics`,
`verified_livestock_losses`) are this project's own non-strategic
infrastructure, reused the same way the common E18 runner reuses them.
"""

from __future__ import annotations

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

from agricola.strategy.claude.e17_reactive_3q_v3 import (
    DEFAULT_CONFIG_PATH as CLAUDE_V3_CONFIG,
)
from agricola.strategy.claude.e17_reactive_3q_v3 import create_claude_e17_agent_v3
from agricola.strategy.claude.e18_opponent_reactive_v1 import (
    DEFAULT_CONFIG_PATH as CANDIDATE_CONFIG,
)
from agricola.strategy.claude.e18_opponent_reactive_v1 import (
    claude_policy_fingerprint,
    create_claude_e18_agent_v1,
)
from agricola.strategy.codex.codex_e18_opponent_reactive_topology import (
    DEFAULT_E18_OPPONENT_REACTIVE_CONFIG_PATH as CODEX_E18_CONFIG,
)
from agricola.strategy.codex.codex_e18_opponent_reactive_topology import (
    create_codex_e18_opponent_reactive_topology,
)
from agricola.strategy.copilot.e17_native_3q import (
    DEFAULT_CONFIG_PATH as COPILOT_CONFIG,
)
from agricola.strategy.copilot.e17_native_3q import create_native_agent
from experiments.e17.tools.common import (
    run_e17_three_agent_development_tournament_v2 as base,
)

CANDIDATE = "CLAUDE_E18_V1"
CLAUDE_V3 = "CLAUDE_V3_CONTROL"
CODEX_E18 = "CODEX_E18_REACTIVE_662_770"
COPILOT = "COPILOT_NATIVE"
OPPONENTS = (CLAUDE_V3, CODEX_E18, COPILOT)

MANIFEST_PATH = REPOSITORY_ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"
OUTPUT_JSON = (
    REPOSITORY_ROOT
    / "experiments/e18/artifacts/derived/claude/E18_CLAUDE_OPPONENT_REACTIVE_V1_DEV_MATRIX.json"
)
OUTPUT_CSV = OUTPUT_JSON.with_suffix(".csv")
TARGET_MONEY = 100_000.0
V3_BASELINE_MEAN = 12850.17857142857
V3_BASELINE_VS_CODEX_MEAN = 10292.86

SOURCES = {
    CANDIDATE: REPOSITORY_ROOT / "src/agricola/strategy/claude/e18_opponent_reactive_v1.py",
    CLAUDE_V3: REPOSITORY_ROOT / "src/agricola/strategy/claude/e17_reactive_3q_v3.py",
}
CONFIGS = {
    CANDIDATE: Path(CANDIDATE_CONFIG),
    CLAUDE_V3: Path(CLAUDE_V3_CONFIG),
    CODEX_E18: Path(CODEX_E18_CONFIG),
    COPILOT: Path(COPILOT_CONFIG),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _payload_hash(payload: Any) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest().upper()


def _factory(name: str, seed: int, seat: int) -> tuple[Any, Any]:
    context = {
        "run_id": f"E18-CLAUDE-V1-S{seed}-P{seat}-{name}",
        "episode_id": f"E18-CLAUDE-V1-S{seed}-P{seat}-{name}",
        "seed": seed,
        "player_position": seat,
    }
    if name == CANDIDATE:
        policy = create_claude_e18_agent_v1(run_context=context)
        return policy, policy
    if name == CLAUDE_V3:
        policy = create_claude_e17_agent_v3(run_context=context)
        return policy, policy
    if name == CODEX_E18:
        policy = create_codex_e18_opponent_reactive_topology(run_context=context)
        return policy, policy.codex_e18_opponent_reactive_instance
    if name == COPILOT:
        policy = create_native_agent()
        return policy, policy
    raise ValueError(name)


def _action_stream_hash(env: Any, seat: int) -> str:
    actions = [
        state[seat].get("action") for state in env.steps if state[seat].get("action") is not None
    ]
    return _payload_hash(actions)


def _verified_livestock_losses(env: Any, seat: int) -> int:
    """Day-boundary resource losses across tile + shed + inventories, not
    just tile-level drops (which can be a tile-to-shed transfer, not a
    real loss) -- same definition the E18 common tournament runner uses."""

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
        "losses": sum(
            r["winner"] not in (CANDIDATE, "TIE") for r in records
        ),
        "ties": sum(r["winner"] == "TIE" for r in records),
        "candidate_money_mean": _mean(candidate_money),
        "candidate_money_median": statistics.median(candidate_money) if candidate_money else 0.0,
        "candidate_money_min": min(candidate_money) if candidate_money else 0.0,
        "candidate_money_max": max(candidate_money) if candidate_money else 0.0,
        "opponent_money_mean": _mean(opponent_money),
        "paired_delta_mean": _mean(paired_delta),
        "runs_below_5000": sum(1 for m in candidate_money if m < 5000.0),
        "verified_livestock_losses": sum(
            int(r["candidate_metrics"]["verified_livestock_losses"]) for r in records
        ),
        "technical_errors": sum(int(r["candidate_metrics"].get("technical_errors", 0) or 0) for r in records),
        "unique_action_streams": len({r["candidate_metrics"]["action_stream_hash"] for r in records}),
        "unique_regimes": sorted({r["candidate_telemetry"]["regime"] for r in records}),
        "mode_decision_rate": _mean(
            [float(r["candidate_telemetry"]["mode_decisions"]) for r in records]
        ),
    }


def _conditioned_action_divergence(records: list[dict[str, Any]]) -> dict[str, int]:
    groups: dict[tuple[int, int], list[dict[str, Any]]] = {}
    for record in records:
        groups.setdefault((record["seed"], record["candidate_seat"]), []).append(record)
    eligible = [values for values in groups.values() if len(values) > 1]
    divergent = [
        values
        for values in eligible
        if len({r["candidate_metrics"]["action_stream_hash"] for r in values}) > 1
    ]
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
        CLAUDE_V3: {
            "source": str(SOURCES[CLAUDE_V3].relative_to(REPOSITORY_ROOT)).replace("\\", "/"),
            "source_sha256": _sha256(SOURCES[CLAUDE_V3]),
            "config": str(CONFIGS[CLAUDE_V3].relative_to(REPOSITORY_ROOT)).replace("\\", "/"),
            "config_sha256": _sha256(CONFIGS[CLAUDE_V3]),
        },
        CODEX_E18: {
            "config": str(CONFIGS[CODEX_E18].relative_to(REPOSITORY_ROOT)).replace("\\", "/"),
            "config_sha256": _sha256(CONFIGS[CODEX_E18]),
            "note": "black-box opponent: source not read by this runner or this session",
        },
        COPILOT: {
            "config": str(CONFIGS[COPILOT].relative_to(REPOSITORY_ROOT)).replace("\\", "/"),
            "config_sha256": _sha256(CONFIGS[COPILOT]),
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
                    f"3Q={cm['final_quadrants']} vll={cm['verified_livestock_losses']}",
                    flush=True,
                )

    by_opponent = {
        opponent: [m for m in matches if m["opponent"] == opponent] for opponent in OPPONENTS
    }
    matchups = {opponent: _matchup_summary(records) for opponent, records in by_opponent.items()}
    overall_candidate_money = [float(m["candidate_metrics"]["money"]) for m in matches]

    gates = {
        "vs_v3_improvement_pct": (
            (matchups[CLAUDE_V3]["candidate_money_mean"] - V3_BASELINE_MEAN) / V3_BASELINE_MEAN * 100
            if V3_BASELINE_MEAN
            else None
        ),
        "vs_codex_improvement_pct": (
            (matchups[CODEX_E18]["candidate_money_mean"] - V3_BASELINE_VS_CODEX_MEAN)
            / V3_BASELINE_VS_CODEX_MEAN
            * 100
            if V3_BASELINE_VS_CODEX_MEAN
            else None
        ),
        "no_runs_below_5000": sum(m["runs_below_5000"] for m in matchups.values()) == 0,
        "verified_livestock_losses_total": sum(
            m["verified_livestock_losses"] for m in matchups.values()
        ),
        "overall_money_mean": _mean(overall_candidate_money),
        "m1_milestone_16000_met": _mean(overall_candidate_money) >= 16000.0,
        "m2_milestone_25000_gap": 25000.0 - _mean(overall_candidate_money),
        "m3_milestone_50000_gap": 50000.0 - _mean(overall_candidate_money),
        "target_100000_gap": TARGET_MONEY - _mean(overall_candidate_money),
        "opponent_conditioned_action_divergence": _conditioned_action_divergence(matches),
    }

    payload = {
        "schema_version": "E18_CLAUDE_OPPONENT_REACTIVE_V1_DEV_MATRIX",
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
        "technical_errors",
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        import csv

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
                    "technical_errors": cm.get("technical_errors", 0),
                }
            )

    print(f"wrote {OUTPUT_JSON}")
    print(f"wrote {OUTPUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
