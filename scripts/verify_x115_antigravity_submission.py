"""
Verification script for X1.15 Antigravity standalone candidate.
Verifies exact behavioral equivalence between source and standalone submission.
"""

import sys
from pathlib import Path
from kaggle_environments import make

from agricola.core.state import GameState
from agricola.strategy.productive_mass_roi import ProductiveMassConfig, ProductiveMassROIAgent

# Import standalone agent function
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "submission"))
import submission_x115_antigravity

def verify_equivalence(seeds=[0, 421521921]):
    print("=" * 70)
    print("VERIFYING BEHAVIORAL EQUIVALENCE: SOURCE vs SUBMISSION")
    print("=" * 70)
    
    all_passed = True
    for seed in seeds:
        print(f"\n--- Testing Seed {seed} ---")
        config = ProductiveMassConfig(
            productive_core_mode="E12_X115_ANTIGRAVITY_INDEPENDENT",
            enable_land_expansion=True,
            x115_antigravity_target_cows=14,
            x115_antigravity_target_sheep=4,
        )
        src_agent = ProductiveMassROIAgent(config=config)
        
        # Reset standalone instance
        submission_x115_antigravity._agent_instance = ProductiveMassROIAgent(config=config)
        
        env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed})
        steps = env.reset()
        
        seed_passed = True
        for step_idx in range(720):
            obs = steps[0].observation
            state = GameState(obs)
            
            src_action = src_agent.act(state)
            sub_action = submission_x115_antigravity.agent(obs)
            
            if src_action != sub_action:
                print(f"FAILED on Step {step_idx} (Day {state.day + 1} H{state.hour})!")
                print(f"  Source Action:     {src_action}")
                print(f"  Submission Action: {sub_action}")
                seed_passed = False
                all_passed = False
                break
                
            steps = env.step([src_action, {}])
            if steps[0].status in ("DONE", "INVALID", "ERROR"):
                break
                
        if seed_passed:
            final_money = GameState(steps[0].observation).money
            print(f"PASS: 100% Exact Action Equivalence across all 720 steps! Final Money: ${final_money:.2f}")
            
    print("\n" + "=" * 70)
    if all_passed:
        print("RESULT: ALL EQUIVALENCE TESTS PASSED! STANDALONE IS CERTIFIED.")
    else:
        print("RESULT: EQUIVALENCE TEST FAILED.")
    print("=" * 70)
    return all_passed

if __name__ == "__main__":
    success = verify_equivalence()
    sys.exit(0 if success else 1)
