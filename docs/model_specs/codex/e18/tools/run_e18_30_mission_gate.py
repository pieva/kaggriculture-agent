"""Matched runtime integration gate; preserve failed runs, never touch holdout."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from pathlib import Path

from kaggle_environments import make

from docs.model_specs.codex.e18.tools.e18_28_full_season_controller import (
    DERIVED,
    FullSeasonController,
)
from docs.model_specs.codex.e18.tools.e18_29_crop_service_audit import (
    crop_service_audit,
)
from docs.model_specs.codex.e18.tools.e18_30_mission_runtime import (
    MissionRuntimeController,
)
from docs.model_specs.codex.e18.tools.run_e18_28_full_season_gate import (
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
    candidate = (
        FullSeasonController(plan, seat)
        if variant == "PARENT"
        else MissionRuntimeController(plan, seat, variant)
    )
    other = opponent_policy(opponent, seed, 1 - seat)
    parity = FullSeasonController(deepcopy(plan), seat) if variant == "OFF" else None
    parity_batches = 0

    def policy(obs, config):
        nonlocal parity_batches
        actual = candidate(obs, config)
        if parity is not None:
            expected = parity(obs, config)
            assert actual == expected, (obs["day"], obs["hour"], actual, expected)
            parity_batches += 1
        return actual

    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "turnsPerDay": 24, "seed": seed},
        debug=False,
    )
    env.run([policy, other] if seat == 0 else [other, policy])
    replay = env.toJSON()
    if variant != "PARENT":
        candidate.acknowledge_terminal(replay["steps"][-1][seat]["observation"])
    candidate.finalize_metrics()
    ledger = audit(replay, seat)
    actions = [step[seat]["action"] for step in replay["steps"][1:]]
    daily_actions = [Counter() for _ in range(30)]
    minimum_cash, max_hands, max_resources, wrong_structure = 10**9, 0, 0, 0
    for index, step in enumerate(replay["steps"]):
        obs = step[seat]["observation"]
        farm, private = obs["farms"][seat], obs["private"]
        minimum_cash = min(minimum_cash, farm["money"])
        max_hands = max(max_hands, len(farm["hands"]))
        owned = Counter(private["shed"])
        for inv in private["inventories"]:
            owned.update(inv)
        for y, row in enumerate(farm["tiles"]):
            for tile in row:
                if isinstance(tile, dict) and tile.get("animal"):
                    owned[tile["animal"]] += 1
                if (
                    y >= 5
                    and isinstance(tile, dict)
                    and tile.get("kind") in {"PASTURE", "COOP"}
                ):
                    wrong_structure += 1
        max_resources = max(
            max_resources, sum(owned[s] for s in ("COW", "SHEEP", "GOOSE"))
        )
        if index == len(replay["steps"]) - 1:
            continue
        action = actions[index] or {}
        commands = [action.get("farmer", ["PASS"]), *action.get("hands", [])]
        commands += [["PASS"]] * max(0, len(farm["hands"]) + 1 - len(commands))
        for command in commands[: len(farm["hands"]) + 1]:
            op = command[0] if isinstance(command, list) and command else "PASS"
            daily_actions[obs["day"]][
                "MOVE" if op in {"NORTH", "SOUTH", "EAST", "WEST"} else op
            ] += 1
    totals = sum(daily_actions, Counter())
    result = {
        "variant": variant,
        "version": "E18.28 C" if variant == "PARENT" else "E18.30 " + variant,
        "opponent": opponent,
        "seed": seed,
        "seat": seat,
        "reward": replay["rewards"][seat],
        "opponent_reward": replay["rewards"][1 - seat],
        "statuses": [s["status"] for s in replay["steps"][-1]],
        "errors": candidate.error_count,
        "last_error": candidate.last_error,
        "opponent_errors": getattr(other, "error_count", 0),
        "parity_batches": parity_batches,
        "actions_sha256": digest(actions),
        "prefix_d1_d6_sha256": digest(actions[:144]),
        "daily": [snapshot(replay, d, seat) for d in range(1, 31)],
        "operational_daily": daily_operational_kpi(replay, seat, ledger),
        "ledger": ledger,
        "terminal": end_state(replay, seat),
        "action_daily": [dict(d) for d in daily_actions],
        "totals": dict(totals),
        "pass_d15_d30": sum(d.get("PASS", 0) for d in daily_actions[14:]),
        "min_cash": minimum_cash,
        "max_hands": max_hands,
        "max_resources": max_resources,
        "lower_quadrant_structure_observations": wrong_structure,
        "crop_starvation": crop_service_audit(replay, seat),
        "runtime_daily": {
            str(d): dict(s) for d, s in getattr(candidate, "runtime_daily", {}).items()
        },
        "missions": getattr(candidate, "mission_log", []),
        "incomplete_missions": getattr(candidate, "incomplete_missions", 0),
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
                    "incomplete_missions",
                    "parity_batches",
                )
            }
            | {
                "PASS": totals["PASS"],
                "MOVE": totals["MOVE"],
                "crop_deaths": len(result["crop_starvation"]),
                "animal_losses": len(ledger["animal_escapes"]),
            }
        ),
        flush=True,
    )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--variants",
        nargs="+",
        choices=["PARENT", "OFF", "RESCUE", "POOL", "CROP_POOL"],
        default=["PARENT", "OFF", "RESCUE", "POOL"],
    )
    parser.add_argument(
        "--opponents",
        nargs="+",
        choices=["E18.16", "E18.2/V4D"],
        default=["E18.16", "E18.2/V4D"],
    )
    parser.add_argument("--seeds", nargs="+", type=int, default=[180903001])
    parser.add_argument("--seats", nargs="+", type=int, default=[0, 1])
    parser.add_argument("--label", required=True)
    parser.add_argument("--jobs", type=int, choices=[1, 2], default=2)
    args = parser.parse_args()
    assert set(args.seeds) <= set(range(180903001, 180903008)) and set(args.seats) <= {
        0,
        1,
    }
    assert args.label.replace("_", "").isalnum()
    output = DERIVED / f"E18_30_MISSION_GATE_{args.label}.json"
    assert not output.exists(), f"Preserve previous evidence: {output}"
    engine = importlib.import_module(
        "kaggle_environments.envs.kaggriculture.kaggriculture"
    )
    sources = [
        Path(__file__),
        Path(__file__).with_name("e18_30_mission_runtime.py"),
        Path(__file__).with_name("e18_30_mission_dispatcher.py"),
        PLAN,
        Path(engine.__file__),
    ]
    payload = {
        "analysis_id": output.stem,
        "phase": "DEVELOPMENT_ONLY",
        "holdout_consumed": False,
        "complete": False,
        "source_sha256": {
            str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources
        },
        "matches": [],
        "failures": [],
    }
    cases = [
        (v, o, s, p)
        for v in args.variants
        for o in args.opponents
        for s in args.seeds
        for p in args.seats
    ]
    payload["jobs_expected"] = len(cases)
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = {executor.submit(run_one, *case): case for case in cases}
        for future in as_completed(futures):
            try:
                payload["matches"].append(future.result())
            except Exception as exc:  # noqa: BLE001 - preserve failed cases
                payload["failures"].append(
                    {"case": futures[future], "error": repr(exc)}
                )
                print(repr(exc), flush=True)
            output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    payload["complete"] = not payload["failures"] and len(payload["matches"]) == len(
        cases
    )
    payload["matches"].sort(
        key=lambda r: (r["variant"], r["opponent"], r["seed"], r["seat"])
    )
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(str(output), flush=True)
    if not payload["complete"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
