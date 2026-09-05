#!/usr/bin/env python3
"""Seat-balanced component ablation and pre-gate for E18.21."""

from __future__ import annotations

import json
import statistics
import sys
from collections.abc import Callable
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
from docs.model_specs.codex.e18.tools.e18_20_wheat_market_netting_controller import (
    WheatMarketNettingController,
)
from docs.model_specs.codex.e18.tools.e18_21_wheat_obligation_ledger_controller import (
    WheatObligationLedgerController,
)
from docs.model_specs.codex.e18.tools.run_e18_18_770_capacity_trajectory_gate_0b import (
    _snapshot,
)
from docs.model_specs.codex.e18.tools.run_e18_20_770_wheat_market_netting_gate import (
    _wheat_orders,
)

SEED = 180903001
EXPECTED_PLAN_SHA256 = (
    "844113c8971ccf3840758cd9d35449e01bc766a1d4b890c7fd8ab29c177410a1"
)
PLAN = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_18_770_CAPACITY_TRAJECTORY_GATE_0A_V1.json"
)
OUTPUT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_21_770_WHEAT_OBLIGATION_LEDGER_PRE_GATE_V1.json"
)
REPORT = (
    ROOT
    / "docs/model_specs/codex/e18/reports/"
    / "E18_21_770_WHEAT_OBLIGATION_LEDGER_PRE_GATE_REPORT_IT.md"
)

VARIANTS = {
    "INFLIGHT_ONLY": (True, False),
    "CONTRACTS_ONLY": (False, True),
    "INFLIGHT_AND_CONTRACTS": (True, True),
}
SELECTED_VARIANT = "INFLIGHT_ONLY"


def _candidate(
    plan: dict[str, Any],
    seat: int,
    *,
    protect_inflight: bool,
    protect_contracts: bool,
) -> WheatObligationLedgerController:
    controller = WheatObligationLedgerController(plan, seat=seat)
    controller.protect_inflight_pickups = protect_inflight
    controller.protect_procurement_contracts = protect_contracts
    return controller


def _parent(plan: dict[str, Any], seat: int) -> WheatMarketNettingController:
    return WheatMarketNettingController(plan, seat=seat)


def _incumbent(plan: dict[str, Any], seat: int):
    del plan
    return create_codex_e18_770_exact_cap_critical_feed(
        run_context={
            "run_id": f"E18-21-PRE-GATE-S{SEED}-P{seat}-INCUMBENT",
            "episode_id": f"E18-21-PRE-GATE-S{SEED}-P{seat}-INCUMBENT",
            "seed": SEED,
            "player_position": seat,
        }
    )


def _run_match(
    plan: dict[str, Any],
    candidate_seat: int,
    variant: str,
    opponent_name: str,
    opponent_factory: Callable[[dict[str, Any], int], Any],
) -> dict[str, Any]:
    protect_inflight, protect_contracts = VARIANTS[variant]
    candidate = _candidate(
        plan,
        candidate_seat,
        protect_inflight=protect_inflight,
        protect_contracts=protect_contracts,
    )
    opponent_seat = 1 - candidate_seat
    opponent = opponent_factory(plan, opponent_seat)
    policies = [None, None]
    policies[candidate_seat] = candidate
    policies[opponent_seat] = opponent
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": SEED, "turnsPerDay": 24},
        debug=False,
    )
    env.run(policies)
    candidate.finalize_metrics()
    replay = env.toJSON()
    rewards = [float(value or 0.0) for value in replay.get("rewards", [0, 0])]
    candidate_reward = rewards[candidate_seat]
    opponent_reward = rewards[opponent_seat]
    return {
        "variant": variant,
        "opponent": opponent_name,
        "candidate_seat": candidate_seat,
        "candidate_reward": candidate_reward,
        "opponent_reward": opponent_reward,
        "margin": candidate_reward - opponent_reward,
        "candidate_final": _snapshot(replay, 30, candidate_seat),
        "opponent_final": _snapshot(replay, 30, opponent_seat),
        "candidate_wheat_orders": _wheat_orders(replay, candidate_seat),
        "opponent_wheat_orders": _wheat_orders(replay, opponent_seat),
        "ledger_metrics": dict(sorted(candidate.wheat_ledger_metrics.items())),
        "feed_skips": int(candidate.skipped_stale.get("FEED", 0)),
        "unfinished_actions": sum(candidate.unfinished_by_day.values()),
        "candidate_errors": candidate.error_count,
        "opponent_errors": int(getattr(opponent, "error_count", 0)),
    }


def _median(matches: list[dict[str, Any]], field: str) -> float:
    return float(statistics.median(match[field] for match in matches))


def _comparison(matches: list[dict[str, Any]]) -> dict[str, Any]:
    candidate = _median(matches, "candidate_reward")
    opponent = _median(matches, "opponent_reward")
    return {
        "candidate_median": candidate,
        "opponent_median": opponent,
        "median_margin": candidate - opponent,
        "matches": matches,
    }


def _variant_is_valid(comparison: dict[str, Any]) -> bool:
    return all(
        match["candidate_errors"] == match["opponent_errors"] == 0
        and match["candidate_final"]["topology"] == {"Q0": 7, "Q1": 7}
        and match["candidate_final"]["animals"] == {"COW": 9, "SHEEP": 5}
        for match in comparison["matches"]
    )


def run() -> dict[str, Any]:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    if plan.get("plan_sha256") != EXPECTED_PLAN_SHA256:
        raise ValueError("frozen E18.18 plan hash mismatch")

    component_ablation: dict[str, dict[str, Any]] = {}
    for variant in VARIANTS:
        matches = [
            _run_match(plan, seat, variant, "E18.20", _parent)
            for seat in (0, 1)
        ]
        component_ablation[variant] = _comparison(matches)

    selected_variant = SELECTED_VARIANT
    incumbent_component_ablation: dict[str, dict[str, Any]] = {}
    for variant in VARIANTS:
        matches = [
            _run_match(plan, seat, variant, "E18.16", _incumbent)
            for seat in (0, 1)
        ]
        incumbent_component_ablation[variant] = _comparison(matches)
    incumbent = incumbent_component_ablation[selected_variant]
    incumbent_matches = incumbent["matches"]
    selected = component_ablation[selected_variant]
    all_selected = [*selected["matches"], *incumbent_matches]
    checks = {
        "zero_errors": all(
            match["candidate_errors"] == match["opponent_errors"] == 0
            for match in all_selected
        ),
        "candidate_exact_770": all(
            match["candidate_final"]["topology"] == {"Q0": 7, "Q1": 7}
            for match in all_selected
        ),
        "candidate_exact_9_cow_5_sheep": all(
            match["candidate_final"]["animals"] == {"COW": 9, "SHEEP": 5}
            for match in all_selected
        ),
        "zero_candidate_same_batch_wheat_overlap_from_activation": all(
            match["candidate_wheat_orders"][
                "same_batch_overlap_units_from_activation"
            ]
            == 0
            for match in all_selected
        ),
        "parent_delta_nonnegative_both_seats": all(
            match["margin"] >= 0 for match in selected["matches"]
        ),
        "incumbent_gate_nonnegative_both_seats": all(
            match["margin"] >= 0 for match in incumbent_matches
        ),
    }
    causal_delta_passed = all(
        checks[key]
        for key in (
            "zero_errors",
            "candidate_exact_770",
            "candidate_exact_9_cow_5_sheep",
            "zero_candidate_same_batch_wheat_overlap_from_activation",
            "parent_delta_nonnegative_both_seats",
        )
    )
    return {
        "schema_version": "e18.codex.770_wheat_obligation_ledger_pre_gate.v1",
        "candidate": "CODEX_E18_21_770_WHEAT_OBLIGATION_LEDGER_V1",
        "parent": "CODEX_E18_20_770_WHEAT_MARKET_NETTING_V1",
        "incumbent": "CODEX_E18_16_770_EXACT_CAP_CRITICAL_FEED_V1",
        "seed": SEED,
        "seats": [0, 1],
        "epistemic_role": "DEVELOPMENT_COMPONENT_ABLATION_AND_PRE_GATE",
        "plan_sha256": EXPECTED_PLAN_SHA256,
        "selection_rule": (
            "select only the in-flight pickup guard; variants containing a "
            "D+2 procurement reserve are diagnostic and remain rejected"
        ),
        "selected_variant": selected_variant,
        "component_ablation": component_ablation,
        "incumbent_component_ablation": incumbent_component_ablation,
        "parent_comparison": selected,
        "incumbent_comparison": incumbent,
        "causal_delta_passed": causal_delta_passed,
        "incumbent_gate_passed": checks[
            "incumbent_gate_nonnegative_both_seats"
        ],
        "checks": checks,
        "full_gate_1_authorized": False,
        "holdout_consumed": False,
        "final_confirmation_consumed": False,
        "kaggle_upload_authorized": False,
    }


def _rows(matches: list[dict[str, Any]]) -> str:
    return "\n".join(
        "| {candidate_seat} | {candidate_reward:.0f} | {opponent_reward:.0f} | "
        "{margin:+.0f} | {sell} | {buy} | {feed_skips} | {protected} |".format(
            **match,
            sell=match["candidate_wheat_orders"]["sell_requested_units"],
            buy=match["candidate_wheat_orders"]["buy_requested_units"],
            protected=match["ledger_metrics"].get("protected_sale_units", 0),
        )
        for match in matches
    )


def _write_report(payload: dict[str, Any]) -> None:
    component_rows = "\n".join(
        f"| {variant} | {comparison['candidate_median']:.1f} | "
        f"{comparison['opponent_median']:.1f} | "
        f"{comparison['median_margin']:+.1f} |"
        for variant, comparison in payload["component_ablation"].items()
    )
    incumbent_component_rows = "\n".join(
        f"| {variant} | {comparison['candidate_median']:.1f} | "
        f"{comparison['opponent_median']:.1f} | "
        f"{comparison['median_margin']:+.1f} |"
        for variant, comparison in payload[
            "incumbent_component_ablation"
        ].items()
    )
    parent = payload["parent_comparison"]
    incumbent = payload["incumbent_comparison"]
    report = f"""# E18.21 — Wheat obligation ledger pre-gate

## Verdetto

Variante selezionata: `{payload['selected_variant']}`.
Delta causale E18.20:
`{'PASS' if payload['causal_delta_passed'] else 'FAIL'}`.
Gate incumbent E18.16:
`{'PASS' if payload['incumbent_gate_passed'] else 'FAIL'}`.

Le varianti con contratti D+2 sono riportate soltanto come diagnosi: reiterano
la riserva multi-day già respinta in E18.20 e non fanno parte del candidato.

## Ablation dei componenti contro E18.20

| Variante | E18.21 | E18.20 | Delta mediano |
|---|---:|---:|---:|
{component_rows}

### Controllo delle varianti contro E18.16

| Variante | E18.21 | E18.16 | Delta mediano |
|---|---:|---:|---:|
{incumbent_component_rows}

## Variante selezionata contro E18.20

| Seat E18.21 | E18.21 | E18.20 | Margine | SELL W | BUY W | FEED skip | W protetto |
|---:|---:|---:|---:|---:|---:|---:|---:|
{_rows(parent['matches'])}

Mediana `{parent['candidate_median']:.1f}` contro
`{parent['opponent_median']:.1f}`, delta `{parent['median_margin']:+.1f}`.

## Variante selezionata contro E18.16

| Seat E18.21 | E18.21 | E18.16 | Margine | SELL W | BUY W | FEED skip | W protetto |
|---:|---:|---:|---:|---:|---:|---:|---:|
{_rows(incumbent['matches'])}

Mediana `{incumbent['candidate_median']:.1f}` contro
`{incumbent['opponent_median']:.1f}`, delta
`{incumbent['median_margin']:+.1f}`.

## Check

```json
{json.dumps(payload['checks'], indent=2, sort_keys=True)}
```
"""
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")


def main() -> int:
    payload = run()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    _write_report(payload)
    print(json.dumps(payload, indent=2))
    return 0 if payload["causal_delta_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
