#!/usr/bin/env python3
"""Frozen V4D-vs-V3 stress test across the controlled E17.1 market regimes."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.core.observation_contract import stable_payload_hash
from experiments.e17.tools.codex.run_codex_e17_batched_cluster_routing_v4_development import (
    _aggregate,
    _common_gates,
    _make_policy,
    _telemetry,
)
from experiments.e17.tools.codex.run_codex_e17_service_routing_v3_development import (
    _capture,
    _counts,
    _eod_losses,
    _farm,
    _terminal_residual,
    _unlock_timing,
)
from experiments.e17.tools.codex.run_codex_e17_true_reactivity_development import (
    REGIMES,
    MarketRegimeOpponent,
    _structural_outcomes,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
MANIFEST_PATH = REPO_ROOT / "experiments/e17/manifest/E17_COMMON_MANIFEST_V1.json"
OUTPUT_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e17/artifacts/derived/"
    / "E17_2_V4D_CONTROLLED_MARKET_STRESS_METRICS.json"
)
V4_SOURCE_PATH = (
    REPO_ROOT / "src/agricola/strategy/codex/codex_e17_batched_cluster_routing_v4.py"
)
V3_SOURCE_PATH = (
    REPO_ROOT / "src/agricola/strategy/codex/codex_e17_reactive_service_routing_v3.py"
)
V4_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e17/configs/"
    / "CODEX_E17_2_POST_FEED_CAPACITY_BATCHED_ROUTING_V4D_D28.json"
)
V3_CONFIG_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e17/configs/"
    / "CODEX_E17_2_REACTIVE_SERVICE_ROUTING_CORE_V3_D28.json"
)
REGIME_SOURCE_PATH = (
    REPO_ROOT
    / "docs/model_specs/codex/e17/tools/"
    / "run_codex_e17_true_reactivity_development.py"
)
POLICIES = ("post_feed_v4d", "service_routing_v3")
EXPECTED_FREEZE = {
    "v4_source": "9350F8B327B972C703136EB6411F03C74B2A80F6A75A9D99C3E4CA614A60B2A4",
    "v4_config": "CA7A6E13CF991185E823325D8220E0682388AC18EB446BB206C0A30ACAB45595",
    "v3_source": "80D909104402473503E1945A6F9EE200DF1CEA5ABA9C66B43C5F6A8AA61A6E91",
    "v3_config": "AD2A79602A610D35C2D44F200AEA36B9949F41D1EA67EC43EAB873B007A2EF8D",
    "regime_source": "5B80BE31181F9A681D85884C5F62DA0E4208E6219429434885F9CD859857B212",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _freeze_hashes() -> dict[str, str]:
    return {
        "v4_source": _sha256(V4_SOURCE_PATH),
        "v4_config": _sha256(V4_CONFIG_PATH),
        "v3_source": _sha256(V3_SOURCE_PATH),
        "v3_config": _sha256(V3_CONFIG_PATH),
        "regime_source": _sha256(REGIME_SOURCE_PATH),
    }


def _run(seed: int, seat: int, regime: str, policy_name: str) -> dict[str, Any]:
    context = {
        "run_id": f"E17-V4D-STRESS-{policy_name}-{regime}-S{seed}-P{seat}",
        "episode_id": f"E17-V4D-STRESS-{policy_name}-{regime}-S{seed}-P{seat}",
        "seed": seed,
        "player_position": seat,
    }
    policy = _make_policy(policy_name, context)
    opponent = MarketRegimeOpponent(
        regime,
        {**context, "run_id": f"{context['run_id']}-OPP", "player_position": 1 - seat},
    )
    actions: list[dict[str, Any]] = []
    captured = _capture(policy, actions)
    agents = [captured, opponent] if seat == 0 else [opponent, captured]
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=True,
    )
    env.run(agents)
    terminal = env.steps[-1]
    observation = terminal[seat].get("observation", {}) or {}
    farm = _farm(observation, seat)
    escapes, crop_losses = _eod_losses(env.steps, seat)
    telemetry = _telemetry(policy_name, policy)
    row = {
        "seed": seed,
        "seat": seat,
        "regime": regime,
        "policy": policy_name,
        "reward": float(terminal[seat].get("reward") or 0.0),
        "status": terminal[seat].get("status"),
        "opponent_reward": float(terminal[1 - seat].get("reward") or 0.0),
        "margin": float(terminal[seat].get("reward") or 0.0)
        - float(terminal[1 - seat].get("reward") or 0.0),
        "action_batches": len(actions),
        "action_stream_sha256": stable_payload_hash(actions),
        "invalid_action_shapes": sum(
            1
            for action in actions
            if not isinstance(action, dict)
            or not isinstance(action.get("farmer"), list)
            or not action.get("farmer")
            or not isinstance(action.get("hands", []), list)
            or not isinstance(action.get("market", []), list)
            or len(action.get("market", []) or []) > 10
        ),
        "strict_eod_escapes": escapes,
        "strict_eod_crop_losses": crop_losses,
        "max_hands": max(
            len(
                _farm(state[seat].get("observation", {}) or {}, seat).get("hands", [])
                or []
            )
            for state in env.steps
        ),
        "unlock_timing": _unlock_timing(env.steps, seat),
        "final_quadrants": _counts(farm),
        "terminal_residual": _terminal_residual(observation.get("private", {}) or {}),
        "opponent_injection_batches": opponent.injection_batches,
        "opponent_injected_orders": dict(opponent.injected_orders),
        "structural_outcomes": _structural_outcomes(env.steps, seat),
        **telemetry,
    }
    print(
        f"{policy_name:20s} {regime:18s} seed={seed} p{seat} "
        f"reward={row['reward']:.0f} move/service={row['move_per_service']:.3f} "
        f"release={row['post_feed_wheat_carrier_releases']} "
        f"escapes={row['strict_eod_escapes']}",
        flush=True,
    )
    return row


def run_matrix(seeds: list[int], regimes: list[str]) -> dict[str, Any]:
    freeze_hashes = _freeze_hashes()
    if freeze_hashes != EXPECTED_FREEZE:
        raise RuntimeError(
            "freeze mismatch; preregister a new plan before execution: "
            f"expected={EXPECTED_FREEZE}, actual={freeze_hashes}"
        )
    rows = [
        _run(seed, seat, regime, policy)
        for seed in seeds
        for seat in (0, 1)
        for regime in regimes
        for policy in POLICIES
    ]
    by_regime: dict[str, dict[str, Any]] = {}
    lookup = {
        (row["seed"], row["seat"], row["regime"], row["policy"]): row
        for row in rows
    }
    matched: list[dict[str, Any]] = []
    for regime in regimes:
        candidate_rows = [
            row
            for row in rows
            if row["regime"] == regime and row["policy"] == "post_feed_v4d"
        ]
        control_rows = [
            row
            for row in rows
            if row["regime"] == regime and row["policy"] == "service_routing_v3"
        ]
        candidate = _aggregate(candidate_rows)
        control = _aggregate(control_rows)
        delta = candidate["mean_reward"] - control["mean_reward"]
        delta_pct = 100 * (candidate["mean_reward"] / control["mean_reward"] - 1)
        for seed in seeds:
            for seat in (0, 1):
                candidate_row = lookup[(seed, seat, regime, "post_feed_v4d")]
                control_row = lookup[(seed, seat, regime, "service_routing_v3")]
                matched.append(
                    {
                        "seed": seed,
                        "seat": seat,
                        "regime": regime,
                        "candidate_reward": candidate_row["reward"],
                        "control_reward": control_row["reward"],
                        "delta": candidate_row["reward"] - control_row["reward"],
                    }
                )
        by_regime[regime] = {
            "candidate": candidate,
            "control": control,
            "mean_reward_delta": delta,
            "mean_reward_delta_pct": delta_pct,
            "candidate_common_gates": _common_gates(candidate),
        }

    candidate_all = _aggregate(
        [row for row in rows if row["policy"] == "post_feed_v4d"]
    )
    control_all = _aggregate(
        [row for row in rows if row["policy"] == "service_routing_v3"]
    )
    regime_deltas = {
        regime: by_regime[regime]["mean_reward_delta_pct"] for regime in regimes
    }
    nonnegative_matched = sum(item["delta"] >= 0 for item in matched)
    nonnegative_regimes = sum(value >= 0 for value in regime_deltas.values())
    gates = {
        "all_regime_common_safety": all(
            all(by_regime[regime]["candidate_common_gates"].values())
            for regime in regimes
        ),
        "overall_mean_reward_not_below_v3": (
            candidate_all["mean_reward"] >= control_all["mean_reward"]
        ),
        "inert_mean_reward_not_below_v3": (
            by_regime["INERT"]["mean_reward_delta"] >= 0
        ),
        "at_least_three_nonnegative_regimes": nonnegative_regimes >= 3,
        "worst_regime_delta_pct_at_least_minus_one": min(regime_deltas.values())
        >= -1.0,
        "matched_nonnegative_share_at_least_75pct": (
            nonnegative_matched / len(matched) >= 0.75
        ),
        "overall_move_per_service_below_v3": (
            candidate_all["move_per_service"] < control_all["move_per_service"]
        ),
        "capacity_mechanism_observed_each_regime": all(
            by_regime[regime]["candidate"]["capacity_flush_trigger_events"] > 0
            and by_regime[regime]["candidate"]["post_feed_wheat_carrier_releases"]
            > 0
            for regime in regimes
        ),
    }
    summary = {
        "schema_version": "E17_2_V4D_CONTROLLED_MARKET_STRESS_V1",
        "epistemic_role": "DEVELOPMENT_ONLY",
        "causal_family": "V4D_ROBUSTNESS_ACROSS_CONTROLLED_MARKET_REGIMES",
        "candidate": "CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28",
        "control": "CODEX-E17.2-REACTIVE-SERVICE-ROUTING-CORE-V3-D28",
        "freeze_hashes": freeze_hashes,
        "seeds": seeds,
        "seats": [0, 1],
        "regimes": regimes,
        "policies": list(POLICIES),
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "runs": len(rows),
        "overall": {
            "candidate": candidate_all,
            "control": control_all,
            "mean_reward_delta": candidate_all["mean_reward"]
            - control_all["mean_reward"],
            "mean_reward_delta_pct": 100
            * (candidate_all["mean_reward"] / control_all["mean_reward"] - 1),
            "matched_nonnegative": nonnegative_matched,
            "matched_total": len(matched),
            "matched_nonnegative_share": nonnegative_matched / len(matched),
            "nonnegative_regimes": nonnegative_regimes,
            "regime_count": len(regimes),
            "worst_regime_delta_pct": min(regime_deltas.values()),
        },
        "by_regime": by_regime,
        "matched_comparisons": matched,
        "gates": gates,
        "all_gates_pass": all(gates.values()),
        "d27_admission": "PASS" if all(gates.values()) else "BLOCKED",
        "results": rows,
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--seeds", nargs="+", type=int, default=manifest["seed_policy"]["e17_0_seeds"]
    )
    parser.add_argument("--regimes", nargs="+", choices=REGIMES, default=list(REGIMES))
    args = parser.parse_args(argv)
    forbidden = set(manifest["seed_policy"]["holdout"]["seeds"]) | set(
        manifest["seed_policy"]["final_confirmation"]["seeds"]
    )
    if forbidden.intersection(args.seeds):
        raise SystemExit("holdout/final seeds are forbidden in development")
    if not set(args.seeds).issubset(set(manifest["seed_policy"]["development"])):
        raise SystemExit("only manifest development seeds are allowed")
    if set(args.regimes) != set(REGIMES):
        raise SystemExit("the preregistered gate requires all four controlled regimes")
    summary = run_matrix(args.seeds, args.regimes)
    print(
        json.dumps(
            {
                "runs": summary["runs"],
                "overall": summary["overall"],
                "by_regime": {
                    regime: {
                        "candidate_mean_reward": values["candidate"]["mean_reward"],
                        "control_mean_reward": values["control"]["mean_reward"],
                        "mean_reward_delta": values["mean_reward_delta"],
                        "mean_reward_delta_pct": values["mean_reward_delta_pct"],
                    }
                    for regime, values in summary["by_regime"].items()
                },
                "gates": summary["gates"],
                "all_gates_pass": summary["all_gates_pass"],
                "d27_admission": summary["d27_admission"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if all(
        aggregate["technical_errors"] == 0
        for aggregate in (summary["overall"]["candidate"], summary["overall"]["control"])
    ) else 1


if __name__ == "__main__":
    sys.exit(main())
