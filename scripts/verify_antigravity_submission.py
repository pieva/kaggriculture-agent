"""Verification script for Antigravity C2 standalone candidate.
Verifies exact behavioral equivalence between frozen source and standalone submission.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from kaggle_environments import make

from agricola.strategy.antigravity.agent_c2 import AntigravityC2Agent

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUBMISSION_PATH = PROJECT_ROOT / "submission" / "submission_antigravity.py"


def verify_equivalence(seeds=(1838889274, 1619968655, 710418712)) -> bool:
    print("=" * 75)
    print("VERIFYING BEHAVIORAL EQUIVALENCE: ANTIGRAVITY C2 SOURCE vs SUBMISSION")
    print("=" * 75)

    all_passed = True
    for seed in seeds:
        print(f"\n--- Testing Seed {seed} ---")

        # Load fresh submission module into sys.modules
        mod_name = f"submission_antigravity_test_{seed}"
        spec = importlib.util.spec_from_file_location(mod_name, SUBMISSION_PATH)
        sub_mod = importlib.util.module_from_spec(spec)
        sys.modules[mod_name] = sub_mod
        spec.loader.exec_module(sub_mod)

        src_agent = AntigravityC2Agent()

        env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed})
        steps = env.reset()

        seed_passed = True
        for step_idx in range(720):
            obs = steps[0].observation

            src_action = src_agent(obs)
            sub_action = sub_mod.agent(obs)

            if src_action != sub_action:
                print(f"FAILED on Step {step_idx}!")
                print(f"  Source Action:     {src_action}")
                print(f"  Submission Action: {sub_action}")
                seed_passed = False
                all_passed = False
                break

            steps = env.step([src_action, {"farmer": ["PASS"], "hands": [], "market": []}])
            if steps[0].status in ("DONE", "INVALID", "ERROR"):
                break

        if seed_passed:
            final_money = float(steps[0].observation.get("farms", [{}])[0].get("money", 0.0))
            print(f"PASS: 100% Exact Step-by-Step Action Equivalence! Final Money: ${final_money:,.2f}")

    print("\n" + "=" * 75)
    if all_passed:
        print("RESULT: ALL EQUIVALENCE TESTS PASSED! STANDALONE IS 100% CERTIFIED.")
    else:
        print("RESULT: EQUIVALENCE TEST FAILED.")
    print("=" * 75)
    return all_passed


if __name__ == "__main__":
    success = verify_equivalence()
    sys.exit(0 if success else 1)
