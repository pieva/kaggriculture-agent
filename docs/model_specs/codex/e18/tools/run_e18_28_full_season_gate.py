"""Bounded development-only ablation runner; keep all failed cases visible."""

import argparse
import hashlib
import json
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

from kaggle_environments import make

from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d20_trajectories import (
    snapshot,
)
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import (
    audit,
    end_state,
)
from docs.model_specs.codex.e18.tools.e18_27_d10_d15_cashflow_controller import (
    D10D15CashflowController,
)
from docs.model_specs.codex.e18.tools.e18_28_full_season_controller import (
    DERIVED,
    PARENT,
    FullSeasonController,
)
from docs.model_specs.codex.e18.tools.run_e18_27_d10_d15_cashflow_gate import (
    opponent_policy,
)
from experiments.e18.tools.common.replay_daily_operational_kpi import (
    daily_operational_kpi,
)


def run_one(variant, opponent, seed, seat):
    path = (
        PARENT
        if variant == "PARENT"
        else DERIVED / f"E18_28_FULL_SEASON_{variant}_PLAN_V1.json"
    )
    plan = json.loads(path.read_text())
    safety = (
        "exact_770_layout",
        "zero_shadow_crop_starvation",
        "zero_shadow_animal_escape",
        "zero_shadow_illegal_actions",
        "all_daily_routes_feasible",
        "daily_reserve_target_met",
    )
    assert all(plan["gate_0a_checks"][k] for k in safety), plan["gate_0a_checks"]
    candidate = (
        D10D15CashflowController(plan, seat)
        if variant == "PARENT"
        else FullSeasonController(plan, seat)
    )
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
    diagnostics = daily_operational_kpi(replay, seat, ledger)
    max_resources = max_hands = breaches = 0
    for step in replay["steps"]:
        obs = step[seat]["observation"]
        farm, private = obs["farms"][seat], obs["private"]
        placed = sum(
            bool(t.get("animal"))
            for row in farm["tiles"]
            for t in row
            if isinstance(t, dict)
        )
        owned = sum(
            private["shed"].get(s, 0)
            + sum(inv.get(s, 0) for inv in private["inventories"])
            for s in ("COW", "SHEEP", "GOOSE")
        )
        max_resources = max(max_resources, placed + owned)
        max_hands = max(max_hands, len(farm["hands"]))
        breaches += sum(
            t.get("kind") in ("PASTURE", "COOP")
            for y, row in enumerate(farm["tiles"])
            for t in row
            if y >= 5 and isinstance(t, dict)
        )
    prefix = [s[seat]["action"] for s in replay["steps"][1:577]]
    result = {
        "version": "E18.27 V3" if variant == "PARENT" else f"E18.28 {variant}",
        "variant": variant,
        "opponent": opponent,
        "seed": seed,
        "seat": seat,
        "reward": replay["rewards"][seat],
        "opponent_reward": replay["rewards"][1 - seat],
        "statuses": [s["status"] for s in replay["steps"][-1]],
        "daily": daily,
        "operational_daily": diagnostics,
        "ledger": ledger,
        "terminal": end_state(replay, seat),
        "max_resources": max_resources,
        "max_hands": max_hands,
        "lower_quadrant_structure_observations": breaches,
        "errors": candidate.error_count,
        "last_error": candidate.last_error,
        "opponent_errors": getattr(other, "error_count", 0),
        "skipped": dict(candidate.skipped_stale),
        "prefix_d1_d24_sha256": hashlib.sha256(
            json.dumps(prefix, sort_keys=True).encode()
        ).hexdigest(),
        "plan_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "controller_sha256": hashlib.sha256(
            (DERIVED.parent.parent / "tools/e18_28_full_season_controller.py").read_bytes()
        ).hexdigest(),
    }
    print(
        json.dumps(
            {
                k: result[k]
                for k in (
                    "variant",
                    "opponent",
                    "seed",
                    "seat",
                    "reward",
                    "opponent_reward",
                    "errors",
                    "max_resources",
                )
            }
            | {
                "losses": len(ledger["animal_escapes"]),
                "cows": [r["animals"]["COW"] for r in daily[:10]],
                "crop_late": [r["crop_tiles"] for r in daily[24:]],
                "people_late": [r["people"] for r in daily[24:]],
            }
        ),
        flush=True,
    )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--variants", nargs="+", default=["PARENT", "A", "B", "C"])
    parser.add_argument("--seeds", nargs="+", type=int, default=[180903001])
    parser.add_argument("--seats", nargs="+", type=int, default=[0, 1])
    parser.add_argument("--opponents", nargs="+", default=["E18.16"])
    parser.add_argument("--label", required=True)
    parser.add_argument("--jobs", type=int, choices=[1, 2], default=2)
    args = parser.parse_args()
    assert set(args.seeds) <= set(range(180903001, 180903008))
    assert set(args.seats) <= {0, 1} and args.label.replace("_", "").isalnum()
    output = DERIVED / f"E18_28_FULL_SEASON_{args.label}.json"
    assert not output.exists(), f"Preserve previous evidence: {output}"
    payload = {
        "analysis_id": output.stem,
        "phase": "DEVELOPMENT_ONLY",
        "holdout_consumed": False,
        "complete": False,
        "matches": [],
    }
    jobs = [
        (v, o, s, p)
        for v in args.variants
        for o in args.opponents
        for s in args.seeds
        for p in args.seats
    ]
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(run_one, *job) for job in jobs]
        for future in as_completed(futures):
            payload["matches"].append(future.result())
            output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    payload["matches"].sort(
        key=lambda p: (p["variant"], p["opponent"], p["seed"], p["seat"])
    )
    payload["complete"] = True
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(str(output), flush=True)


if __name__ == "__main__":
    main()
