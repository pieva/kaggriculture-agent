"""Verify source/standalone parity for the Antigravity C2 75K Dual-Quadrant package."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from kaggle_environments import make

from agricola.strategy.antigravity.agent_c2_75k import create_agent

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUBMISSION_PATH = PROJECT_ROOT / "submission" / "submission_antigravity.py"


def verify_equivalence(seeds=(26090101, 26090102, 1838889274), max_steps: int = 120) -> bool:
    print("=" * 75)
    print("VERIFYING BEHAVIORAL EQUIVALENCE: ANTIGRAVITY 75K SOURCE vs SUBMISSION")
    print("=" * 75)

    all_passed = True
    for episode_sequence, seed in enumerate(seeds, start=1):
        print(f"\n--- Testing Seed {seed} ---")

        # Load fresh submission module into sys.modules
        mod_name = f"submission_antigravity_75k_test_{seed}"
        spec = importlib.util.spec_from_file_location(mod_name, SUBMISSION_PATH)
        sub_mod = importlib.util.module_from_spec(spec)
        sys.modules[mod_name] = sub_mod
        spec.loader.exec_module(sub_mod)

        src_agent = create_agent(
            run_context={
                "run_id": "antigravity-c2-75k-parity-20260831",
                "episode_id": f"antigravity-parity-{episode_sequence:04d}",
                "seed": seed,
                "opponent_id": "INERT_PASS_POLICY",
                "player_position": 0,
            }
        )

        env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24})
        steps = env.reset()

        seed_passed = True
        for step_idx in range(max_steps):
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
            print(f"PASS: exact action equivalence across {max_steps} technical steps")

    print("\n" + "=" * 75)
    if all_passed:
        print("RESULT: ALL EQUIVALENCE TESTS PASSED! ANTIGRAVITY 75K STANDALONE IS 100% CERTIFIED.")
    else:
        print("RESULT: ANTIGRAVITY 75K EQUIVALENCE TEST FAILED.")
    print("=" * 75)
    return all_passed


if __name__ == "__main__":
    success = verify_equivalence()
    sys.exit(0 if success else 1)
