"""Matched development-only E18.29 gate. Never overwrite earlier evidence."""

import argparse
import hashlib
import json
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

from kaggle_environments import make

from docs.model_specs.codex.e18.tools.e18_29_anti_pass_controller import (
    AntiPassController,
)
from docs.model_specs.codex.e18.tools.e18_29_crop_service_audit import (
    crop_service_audit,
)
from docs.model_specs.codex.e18.tools.e18_29_fertilizer_audit import fertilizer_audit
from docs.model_specs.codex.e18.tools.e18_29_service_safe_anti_pass_controller import (
    ServiceSafeAntiPassController,
)
from docs.model_specs.codex.e18.tools.e18_29_spawn_matched_anti_pass_controller import (
    SpawnMatchedAntiPassController,
)
from docs.model_specs.codex.e18.tools.run_e18_28_full_season_gate import (
    DERIVED,
    FullSeasonController,
    audit,
    daily_operational_kpi,
    end_state,
    opponent_policy,
    snapshot,
)

PLAN = DERIVED / "E18_28_FULL_SEASON_C_PLAN_V1.json"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def run_one(variant, opponent, seed, seat):
    plan = json.loads(PLAN.read_text())
    agent = (
        FullSeasonController(plan, seat)
        if variant == "PARENT"
        else ServiceSafeAntiPassController(plan, seat)
        if variant == "B2"
        else SpawnMatchedAntiPassController(plan, seat)
        if variant == "B3"
        else AntiPassController(plan, seat, variant)
    )
    other = opponent_policy(opponent, seed, 1 - seat)
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=False,
    )
    env.run([agent, other] if seat == 0 else [other, agent])
    replay = env.toJSON()
    if variant != "PARENT":
        agent.acknowledge_terminal(replay["steps"][-1][seat]["observation"])
    agent.finalize_metrics()
    ledger = audit(replay, seat)
    daily = [snapshot(replay, d, seat) for d in range(1, 31)]
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
            private["shed"].get(s, 0) + sum(i.get(s, 0) for i in private["inventories"])
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
    actions = [s[seat]["action"] for s in replay["steps"][1:]]
    result = dict(
        version="E18.28 C" if variant == "PARENT" else f"E18.29 {variant}",
        variant=variant,
        opponent=opponent,
        seed=seed,
        seat=seat,
        reward=replay["rewards"][seat],
        opponent_reward=replay["rewards"][1 - seat],
        statuses=[s["status"] for s in replay["steps"][-1]],
        daily=daily,
        operational_daily=daily_operational_kpi(replay, seat, ledger),
        ledger=ledger,
        terminal=end_state(replay, seat),
        max_resources=max_resources,
        max_hands=max_hands,
        lower_quadrant_structure_observations=breaches,
        errors=agent.error_count,
        last_error=agent.last_error,
        opponent_errors=getattr(other, "error_count", 0),
        skipped=dict(agent.skipped_stale),
        actions_sha256=digest(actions),
        prefix_d1_d6_sha256=digest(actions[:144]),
        action_day_sha256=[
            digest(actions[d * 24 : min((d + 1) * 24, 719)]) for d in range(30)
        ],
        plan_sha256=hashlib.sha256(PLAN.read_bytes()).hexdigest(),
        anti_daily={
            str(d): dict(c) for d, c in getattr(agent, "anti_daily", {}).items()
        },
        missions=getattr(agent, "mission_log", []),
        incomplete_missions=len(getattr(agent, "missions", {})),
        fertilizer_daily=fertilizer_audit(replay, seat),
        crop_starvation=crop_service_audit(replay, seat),
        reassignments=getattr(agent, "reassignments", []),
    )
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
                    "incomplete_missions",
                )
            }
            | {"losses": len(ledger["animal_escapes"])}
        ),
        flush=True,
    )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--variants",
        nargs="+",
        choices=["PARENT", "OFF", "A", "B", "B2", "B3"],
        default=["PARENT", "OFF", "A", "B"],
    )
    parser.add_argument("--seeds", nargs="+", type=int, default=[180903001])
    parser.add_argument("--seats", nargs="+", type=int, default=[0, 1])
    parser.add_argument(
        "--opponents", nargs="+", choices=["E18.16", "E18.2/V4D"], default=["E18.16"]
    )
    parser.add_argument("--label", required=True)
    parser.add_argument("--jobs", type=int, choices=[1, 2], default=2)
    args = parser.parse_args()
    assert set(args.seeds) <= set(range(180903001, 180903008)) and set(args.seats) <= {
        0,
        1,
    }
    assert args.label.replace("_", "").isalnum()
    output = DERIVED / f"E18_29_ANTI_PASS_{args.label}.json"
    assert not output.exists(), f"Preserve previous evidence: {output}"
    source_files = [
        p
        for p in Path(__file__).parent.glob("*.py")
        if p.name.startswith(("e18_", "run_e18_"))
    ]
    payload = dict(
        analysis_id=output.stem,
        phase="DEVELOPMENT_ONLY",
        holdout_consumed=False,
        complete=False,
        jobs_expected=len(args.variants)
        * len(args.opponents)
        * len(args.seeds)
        * len(args.seats),
        source_sha256={
            p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files
        },
        matches=[],
        failures=[],
    )
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = {
            executor.submit(run_one, v, o, s, p): (v, o, s, p)
            for v in args.variants
            for o in args.opponents
            for s in args.seeds
            for p in args.seats
        }
        for future in as_completed(futures):
            try:
                payload["matches"].append(future.result())
            except Exception as exc:
                payload["failures"].append(dict(case=futures[future], error=repr(exc)))
                print(repr(exc), flush=True)
            output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    payload["matches"].sort(
        key=lambda p: (p["variant"], p["opponent"], p["seed"], p["seat"])
    )
    payload["complete"] = (
        not payload["failures"] and len(payload["matches"]) == payload["jobs_expected"]
    )
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(str(output), flush=True)
    if not payload["complete"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
