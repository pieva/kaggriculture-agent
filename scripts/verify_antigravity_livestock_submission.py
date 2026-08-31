"""Verification script for Antigravity C2 Livestock Diagnostic standalone submission."""

import importlib.util
from pathlib import Path
from typing import Any, Dict, List
from kaggle_environments import make

from agricola.strategy.antigravity_livestock import (
    AntigravityC2LivestockAgent,
    AntigravityC2LivestockConfig,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUBMISSION_PATH = PROJECT_ROOT / "submission" / "submission_antigravity_livestock.py"


def load_submission_agent():
    import sys
    spec = importlib.util.spec_from_file_location("submission_antigravity_livestock", SUBMISSION_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["submission_antigravity_livestock"] = mod
    spec.loader.exec_module(mod)
    return mod.agent


def run_equivalence_test(seed: int, steps: int = 720) -> Dict[str, Any]:
    submission_agent_fn = load_submission_agent()
    source_agent = AntigravityC2LivestockAgent(config=AntigravityC2LivestockConfig())

    source_actions_log: List[Dict[str, Any]] = []
    sub_actions_log: List[Dict[str, Any]] = []

    class LoggingSourceAgent:
        def __call__(self, obs, cfg=None):
            act = source_agent(obs, cfg)
            source_actions_log.append(act)
            return act

    class LoggingSubAgent:
        def __call__(self, obs, cfg=None):
            act = submission_agent_fn(obs, cfg)
            sub_actions_log.append(act)
            return act

    # Run Source Candidate
    env_source = make("kaggriculture", configuration={"seed": seed, "episodeSteps": steps})
    env_source.run([LoggingSourceAgent(), "pass"])
    source_final_money = env_source.state[0].observation.farms[0]["money"]

    # Run Standalone Bundle
    env_sub = make("kaggriculture", configuration={"seed": seed, "episodeSteps": steps})
    env_sub.run([LoggingSubAgent(), "pass"])
    sub_final_money = env_sub.state[0].observation.farms[0]["money"]

    assert len(source_actions_log) == len(sub_actions_log), (
        f"Length mismatch: {len(source_actions_log)} vs {len(sub_actions_log)}"
    )

    diff_count = 0
    for idx, (a1, a2) in enumerate(zip(source_actions_log, sub_actions_log)):
        if a1 != a2:
            diff_count += 1
            print(f"Step {idx} divergence: Source={a1} vs Sub={a2}")

    return {
        "seed": seed,
        "source_money": source_final_money,
        "sub_money": sub_final_money,
        "step_diffs": diff_count,
        "equivalent": (diff_count == 0 and source_final_money == sub_final_money),
    }


def main():
    seeds = [1838889274, 1619968655, 710418712]
    print("=" * 75)
    print("VERIFYING BEHAVIORAL EQUIVALENCE: ANTIGRAVITY C2 LIVESTOCK vs SUBMISSION")
    print("=" * 75)

    all_passed = True
    for s in seeds:
        print(f"\n--- Testing Seed {s} ---")
        res = run_equivalence_test(s)
        if res["equivalent"]:
            print(f"PASS: 100% Exact Step-by-Step Equivalence! Final Money: ${res['sub_money']:,.2f}")
        else:
            print(f"FAIL: Discrepancies detected on seed {s}: {res}")
            all_passed = False

    print("\n" + "=" * 75)
    if all_passed:
        print("RESULT: ALL EQUIVALENCE TESTS PASSED! STANDALONE IS 100% CERTIFIED.")
    else:
        print("RESULT: EQUIVALENCE TEST FAILED!")
    print("=" * 75)


if __name__ == "__main__":
    main()
