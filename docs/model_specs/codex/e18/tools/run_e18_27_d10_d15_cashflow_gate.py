"""Reproducible matched development comparisons, with executed cash/FEED audit."""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from kaggle_environments import make

from agricola.strategy.codex.codex_e18_770_exact_cap_critical_feed import (
    create_codex_e18_770_exact_cap_critical_feed,
)
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d20_trajectories import (
    snapshot,
)
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import (
    audit,
    end_state,
)
from docs.model_specs.codex.e18.tools.e18_25_d10_labor_step_controller import (
    D10LaborStepController,
)
from docs.model_specs.codex.e18.tools.e18_26_jesse_boost_d10_controller import (
    JesseBoostD10Controller,
)
from docs.model_specs.codex.e18.tools.e18_27_d10_d15_cashflow_controller import (
    BASE,
    CONFIG,
    PARENT_PLAN,
    PLAN,
    D10D15CashflowController,
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def opponent_policy(name, seed, seat):
    if name == "E18.2/V4D":
        import runpy

        bundle = runpy.run_path(
            str(ROOT / "submission/submission_codex_e18_2_capacity_governed_v4d.py")
        )
        return bundle["create_agent"](
            run_context={
                "run_id": f"E18-27-V4D-S{seed}-P{seat}",
                "seed": seed,
                "player_position": seat,
            }
        )
    if name == "E18.16":
        return create_codex_e18_770_exact_cap_critical_feed(
            run_context={
                "run_id": f"E18-27-S{seed}-P{seat}",
                "episode_id": f"E18-27-S{seed}-P{seat}",
                "seed": seed,
                "player_position": seat,
            }
        )
    if name == "E18.25":
        plan = json.loads(
            (
                BASE / "artifacts/derived/E18_25_770_D10_LABOR_STEP_PLAN_V1.json"
            ).read_text()
        )
        return D10LaborStepController(plan, seat=seat)
    raise ValueError(name)


def run_match(version, plan, opponent, seed, seat):
    cls = D10D15CashflowController if version == "E18.27" else JesseBoostD10Controller
    candidate = cls(plan, seat=seat)
    other = opponent_policy(opponent, seed, 1 - seat)
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=False,
    )
    env.run([candidate, other] if seat == 0 else [other, candidate])
    candidate.finalize_metrics()
    replay = env.toJSON()
    ledger = audit(replay, seat)
    daily = [snapshot(replay, d, seat) for d in range(1, 31)]
    max_resources, max_hands, breaches = 0, 0, 0
    cash_min = {d: float("inf") for d in range(10, 16)}
    for step in replay["steps"]:
        obs = step[seat]["observation"]
        farm, private = obs["farms"][seat], obs["private"]
        placed = sum(
            bool(t.get("animal"))
            for row in farm["tiles"]
            for t in row
            if isinstance(t, dict)
        )
        inventory = Counter(private["shed"])
        for inv in private["inventories"]:
            inventory.update(inv)
        max_resources = max(
            max_resources,
            placed + inventory["COW"] + inventory["SHEEP"] + inventory["GOOSE"],
        )
        max_hands = max(max_hands, len(farm["hands"]))
        breaches += sum(
            t.get("kind") in {"PASTURE", "COOP"}
            for y, row in enumerate(farm["tiles"])
            for x, t in enumerate(row)
            if isinstance(t, dict) and y >= 5
        )
        day = obs["day"] + 1
        if day in cash_min:
            cash_min[day] = min(cash_min[day], farm["money"])
    feed = {}
    for day in range(11, 16):
        start_farm = replay["steps"][(day - 1) * 24][seat]["observation"]["farms"][seat]
        start_animals = sum(
            bool(t.get("animal"))
            for row in start_farm["tiles"]
            for t in row
            if isinstance(t, dict)
        )
        required = start_animals + sum(
            ledger["daily"][day - 1]["animal_placed"].values()
        )
        actual = ledger["daily"][day - 1]["executed_actions"].get("FEED", 0)
        feed[str(day)] = {
            "required": required,
            "executed": actual,
            "complete": actual >= required,
        }
    prefix = [step[seat]["action"] for step in replay["steps"][1:217]]
    result = {
        "version": version,
        "opponent": opponent,
        "seed": seed,
        "seat": seat,
        "reward": replay["rewards"][seat],
        "opponent_reward": replay["rewards"][1 - seat],
        "prefix_d1_d9_sha256": hashlib.sha256(
            json.dumps(prefix, sort_keys=True).encode()
        ).hexdigest(),
        "daily": daily,
        "ledger": ledger,
        "terminal": end_state(replay, seat),
        "max_resources": max_resources,
        "max_hands": max_hands,
        "lower_quadrant_structure_observations": breaches,
        "cash_min_d10_d15": cash_min,
        "feed_d11_d15": feed,
        "errors": candidate.error_count,
        "opponent_errors": getattr(other, "error_count", 0),
        "last_error": candidate.last_error,
        "skipped": dict(candidate.skipped_stale),
        "market_trace_d10_d15": [
            r for r in candidate.market_trace if 10 <= r["day"] <= 15
        ],
    }
    print(
        json.dumps(
            {
                "version": version,
                "opponent": opponent,
                "seed": seed,
                "seat": seat,
                "reward": result["reward"],
                "cash_d11": daily[10]["money"],
                "animals_d15": daily[14]["animals"],
                "escapes": len(ledger["animal_escapes"]),
                "feed": feed,
                "errors": result["errors"],
            }
        ),
        flush=True,
    )
    return result


def checks_for(candidate, parent):
    mix = {"COW": 9, "SHEEP": 5, "GOOSE": 0}
    topology = {"Q0": 7, "Q1": 7, "Q2": 0, "Q3": 0}
    return {
        "prefix_d1_d9_identical": candidate["prefix_d1_d9_sha256"]
        == parent["prefix_d1_d9_sha256"],
        "zero_errors": candidate["errors"] == candidate["opponent_errors"] == 0,
        "zero_escapes": not candidate["ledger"]["animal_escapes"],
        "feed_d11_d15_complete": all(
            r["complete"] for r in candidate["feed_d11_d15"].values()
        ),
        "resources_cap_14": candidate["max_resources"] <= 14,
        "hands_cap_12": candidate["max_hands"] <= 12,
        "topology_770_d15_d30": all(
            candidate["daily"][d - 1]["pasture_topology"] == topology for d in (15, 30)
        )
        and candidate["lower_quadrant_structure_observations"] == 0,
        "mix_9_5_d15_d30": all(
            candidate["daily"][d - 1]["animals"] == mix for d in (15, 30)
        ),
        "crops_d15_38_23": candidate["daily"][14]["crops"]
        == {"MELON": 0, "WHEAT": 23, "STRAWBERRY": 38, "CARROT": 0, "TOMATO": 0},
        "melon_sold_by_d12": sum(
            r["sold_units"].get("MELON", 0) for r in candidate["ledger"]["daily"][:12]
        )
        == sum(r["harvested"].get("MELON", 0) for r in candidate["ledger"]["daily"]),
        "matched_parent_positive": candidate["reward"] > parent["reward"],
        "incumbent_margin_nonnegative": candidate["reward"]
        >= candidate["opponent_reward"],
    }


def run_pair_job(plans, opponent, seed, seat):
    parent = run_match("E18.26", plans["E18.26"], opponent, seed, seat)
    candidate = run_match("E18.27", plans["E18.27"], opponent, seed, seat)
    return [parent, candidate], {
        "opponent": opponent,
        "seed": seed,
        "seat": seat,
        "parent_reward": parent["reward"],
        "candidate_reward": candidate["reward"],
        "delta": candidate["reward"] - parent["reward"],
        "checks": checks_for(candidate, parent),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", nargs="+", type=int, default=[180903001])
    parser.add_argument("--seats", nargs="+", type=int, choices=(0, 1), default=[0, 1])
    parser.add_argument(
        "--opponents",
        nargs="+",
        choices=("E18.16", "E18.25", "E18.2/V4D"),
        default=["E18.16", "E18.25"],
    )
    parser.add_argument("--label", default="SMOKE")
    parser.add_argument("--jobs", type=int, choices=(1, 2), default=1)
    parser.add_argument("--variant", choices=("V1", "V2", "V3"), default="V1")
    args = parser.parse_args()
    assert args.label.replace("_", "").isalnum()
    config_path = CONFIG.with_name(CONFIG.name.replace("V1", args.variant))
    plan_path = PLAN.with_name(PLAN.name.replace("V1", args.variant))
    allowed = json.loads(config_path.read_text())["development_seeds"]
    assert set(args.seeds) <= set(allowed)
    plans = {
        "E18.27": json.loads(plan_path.read_text()),
        "E18.26": json.loads(PARENT_PLAN.read_text()),
    }
    safety = (
        "exact_770_layout",
        "zero_shadow_crop_starvation",
        "zero_shadow_animal_escape",
        "zero_shadow_illegal_actions",
        "all_daily_routes_feasible",
        "daily_reserve_target_met",
    )
    assert all(plans["E18.27"]["gate_0a_checks"][k] for k in safety), (
        "Unsafe plan; do not simulate."
    )
    output = BASE / f"artifacts/derived/E18_27_D10_D15_{args.label}_{args.variant}.json"
    report = BASE / f"reports/E18_27_D10_D15_{args.label}_{args.variant}_REPORT_IT.md"
    payload = {
        "candidate": "E18.27",
        "parent": "E18.26",
        "phase": "DEVELOPMENT_ONLY",
        "variant": args.variant,
        "candidate_plan_file_sha256": digest(plan_path),
        "parent_plan_file_sha256": digest(PARENT_PLAN),
        "controller_source_sha256": digest(
            BASE / "tools/e18_27_d10_d15_cashflow_controller.py"
        ),
        "config_sha256": digest(config_path),
        "seeds": args.seeds,
        "seats": args.seats,
        "opponents": args.opponents,
        "legacy_plan_checks": plans["E18.27"]["gate_0a_checks"],
        "matches": [],
        "pairs": [],
        "complete": False,
        "holdout_consumed": False,
        "kaggle_upload_authorized": False,
    }
    jobs = [
        (plans, opponent, seed, seat)
        for opponent in args.opponents
        for seed in args.seeds
        for seat in args.seats
    ]

    def save_pair(result):
        matches, pair = result
        payload["matches"].extend(matches)
        payload["pairs"].append(pair)
        output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    if args.jobs == 1:
        for job in jobs:
            save_pair(run_pair_job(*job))
    else:
        # The settlement audit patches engine callbacks: isolate processes,
        # never threads, and keep the sole artifact writer in this process.
        with ProcessPoolExecutor(max_workers=args.jobs) as executor:
            futures = [executor.submit(run_pair_job, *job) for job in jobs]
            for future in as_completed(futures):
                save_pair(future.result())
    payload["pairs"].sort(key=lambda p: (p["opponent"], p["seed"], p["seat"]))
    payload["matches"].sort(
        key=lambda p: (p["opponent"], p["seed"], p["seat"], p["version"])
    )
    payload["complete"] = True
    payload["checks"] = {
        k: all(p["checks"][k] for p in payload["pairs"])
        for k in payload["pairs"][0]["checks"]
    }
    payload["matched_delta_median"] = statistics.median(
        p["delta"] for p in payload["pairs"]
    )
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# E18.27 — confronto interno D10-D15",
        "",
        "Confronti matched sul parent E18.26; seed e seat identici contro lo stesso avversario. Nessun holdout o upload.",
        "",
        "| Avversario | Seed | Seat | E18.26 | E18.27 | Delta |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for p in payload["pairs"]:
        lines.append(
            f"| {p['opponent']} | {p['seed']} | {p['seat']} | {p['parent_reward']} | {p['candidate_reward']} | {p['delta']:+} |"
        )
    lines.extend(
        [
            "",
            "## Gate aggregati",
            "",
            "```json",
            json.dumps(payload["checks"], indent=2),
            "```",
            "",
            "## Gate planner legacy",
            "",
            "```json",
            json.dumps(payload["legacy_plan_checks"], indent=2),
            "```",
            "",
            f"Dataset: `{output.name}`.",
            "",
        ]
    )
    report.write_text("\n".join(lines), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(output),
                "checks": payload["checks"],
                "matched_delta_median": payload["matched_delta_median"],
            },
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
