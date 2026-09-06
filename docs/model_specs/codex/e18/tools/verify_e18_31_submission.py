"""Verify source/bundle equality, then actual Kaggle file-loader equality."""

import hashlib
import json
import runpy
import statistics
import time
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy

from kaggle_environments import make

from docs.model_specs.codex.e18.tools.build_e18_31_submission import DERIVED, OUTPUT
from docs.model_specs.codex.e18.tools.e18_31_unified_investment_controller import UnifiedInvestmentController
from docs.model_specs.codex.e18.tools.run_e18_30_mission_gate import (
    PLAN,
    opponent_policy,
)


def verify_case(case):
    seed, seat = case
    plan = json.loads(PLAN.read_text())
    start = time.perf_counter()
    module = runpy.run_path(str(OUTPUT))
    load_seconds = time.perf_counter() - start
    source = UnifiedInvestmentController(deepcopy(plan), seat)
    timings, actions = [], []

    def checked(obs, config):
        expected = source(obs, config)
        start = time.perf_counter()
        actual = module["agent"](obs, config)
        timings.append(time.perf_counter() - start)
        assert actual == expected, (seed, seat, obs.get("step"), actual, expected)
        actions.append(actual)
        return actual

    config = {"seed": seed, "episodeSteps": 720, "turnsPerDay": 24}
    other = opponent_policy("E18.16", seed, 1 - seat)
    env = make("kaggriculture", configuration=config, debug=False)
    env.run([checked, other] if seat == 0 else [other, checked])
    assert len(actions) == 719 and source.error_count == 0
    assert module["_ACTIVE"][seat][1].error_count == 0
    assert all(s.status == "DONE" for s in env.state)
    terminal_obs = env.steps[-1][seat].observation
    for policy in (source, module["_ACTIVE"][seat][1]):
        policy.acknowledge_terminal(terminal_obs)
        assert policy.incomplete_missions == 0
    other = opponent_policy("E18.16", seed, 1 - seat)
    env_file = make("kaggriculture", configuration=config, debug=False)
    env_file.run([str(OUTPUT), other] if seat == 0 else [other, str(OUTPUT)])
    assert [s[seat].action for s in env_file.steps[1:]] == actions
    assert all(s.status == "DONE" for s in env_file.state)
    assert env_file.state[seat].reward == env.state[seat].reward
    row = {
        "seed": seed,
        "seat": seat,
        "identical_actions": len(actions),
        "reward": env.state[seat].reward,
        "load_seconds": load_seconds,
        "max_call_seconds": max(timings),
        "median_call_seconds": statistics.median(timings),
        "errors": 0,
        "incomplete_missions": 0,
        "kaggle_file_loader_parity": True,
    }
    print(json.dumps(row), flush=True)
    return row


def main():
    target = DERIVED / "E18_31_SUBMISSION_PARITY_V11.json"
    assert not target.exists(), "Preserve previous evidence"
    cases = [(seed, seat) for seed in (180903001, 180903005) for seat in (0, 1)]
    with ProcessPoolExecutor(max_workers=2) as executor:
        rows = list(executor.map(verify_case, cases))
    report = {
        "passed": True,
        "submission_sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        "matches": rows,
        "holdout_consumed": False,
        "new_submission": False,
    }
    target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(str(target), flush=True)


if __name__ == "__main__":
    main()
