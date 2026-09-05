"""Exact 719-action source/standalone parity, then Kaggle file-loader replay."""

import hashlib
import importlib.util
import json
import statistics
import time
from copy import deepcopy

from kaggle_environments import make

from docs.model_specs.codex.e18.tools.build_e18_28_submission import DERIVED, ROOT
from docs.model_specs.codex.e18.tools.e18_28_full_season_controller import (
    FullSeasonController,
)
from docs.model_specs.codex.e18.tools.run_e18_27_d10_d15_cashflow_gate import (
    opponent_policy,
)


def main():
    path = ROOT / "submission/submission_codex_e18_28_770.py"
    plan = json.loads((DERIVED / "E18_28_FULL_SEASON_C_PLAN_V1.json").read_text())
    rows = []
    for seat in (0, 1):
        spec = importlib.util.spec_from_file_location(f"e28_p{seat}", path)
        module = importlib.util.module_from_spec(spec)
        start = time.perf_counter()
        spec.loader.exec_module(module)
        load_seconds = time.perf_counter() - start
        source = FullSeasonController(deepcopy(plan), seat)
        timings, actions = [], []

        def checked(obs, config):
            expected = source(obs, config)
            start = time.perf_counter()
            actual = module.agent(obs, config)
            timings.append(time.perf_counter() - start)
            assert actual == expected, (seat, obs.get("step"), actual, expected)
            actions.append(actual)
            return actual

        other = opponent_policy("E18.16", 180903001, 1 - seat)
        env = make(
            "kaggriculture",
            configuration={"seed": 180903001, "episodeSteps": 720, "turnsPerDay": 24},
            debug=False,
        )
        env.run([checked, other] if seat == 0 else [other, checked])
        assert len(actions) == 719 and source.error_count == 0
        assert module._ACTIVE[seat][1].error_count == 0
        assert all(s.status == "DONE" for s in env.state)
        row = {
            "seat": seat,
            "seed": 180903001,
            "identical_actions": len(actions),
            "reward": env.state[seat].reward,
            "load_seconds": load_seconds,
            "max_call_seconds": max(timings),
            "median_call_seconds": statistics.median(timings),
            "errors": 0,
        }
        # Exercise Kaggle's actual .py-file loader and last-function discovery.
        other = opponent_policy("E18.16", 180903001, 1 - seat)
        env_file = make(
            "kaggriculture",
            configuration={"seed": 180903001, "episodeSteps": 720, "turnsPerDay": 24},
            debug=False,
        )
        env_file.run([str(path), other] if seat == 0 else [other, str(path)])
        file_actions = [s[seat].action for s in env_file.steps[1:]]
        assert file_actions == actions
        assert all(s.status == "DONE" for s in env_file.state)
        assert env_file.state[seat].reward == row["reward"]
        row["kaggle_file_loader_parity"] = True
        rows.append(row)
        print(json.dumps(row), flush=True)
    report = {
        "passed": True,
        "submission_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "matches": rows,
        "holdout_consumed": False,
    }
    (DERIVED / "E18_28_SUBMISSION_PARITY.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
