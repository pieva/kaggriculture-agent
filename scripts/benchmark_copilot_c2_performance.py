"""Full-episode (720-step) real-engine benchmark for the Copilot C2 candidate.

Read-only diagnostic script. Does not modify strategy. Records per-run telemetry
required by KAGGRICULTURE_C2_COPILOT_PERFORMANCE_CORRECTION_PROMPT.md Section 2.
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agricola.strategy.copilot.agent_c2 import CopilotC2Agent
from agricola.strategy.copilot.c2_config import CopilotC2Config
from kaggle_environments import make

SEEDS = [1838889274, 1619968655, 710418712]
STEPS = 720


def inert_action(obs, configuration=None):
    return {"farmer": ["PASS"], "hands": [], "market": []}


def run_episode(seed: int, player_position: int):
    agent = CopilotC2Agent(CopilotC2Config())
    env = make("kaggriculture", configuration={"episodeSteps": STEPS, "seed": seed}, debug=False)
    agents = [None, None]
    agents[player_position] = agent
    agents[1 - player_position] = inert_action
    env.reset()
    action_counts = {}
    no_op_count = 0
    last_obs = None

    def agent_fn(idx):
        def _fn(obs, configuration=None):
            nonlocal no_op_count
            if idx == player_position:
                acts = agent.policy.decide_actions(obs, player_index=idx)
                for a in acts:
                    key = a[0] if a else "PASS"
                    action_counts[key] = action_counts.get(key, 0) + 1
                    if key == "PASS":
                        no_op_count += 1
                farm = obs.get("farms", [])[idx] if isinstance(obs.get("farms"), list) else {}
                private = obs.get("private", {})
                if isinstance(private, list):
                    private = private[idx] if 0 <= idx < len(private) else {}
                tiles = farm.get("tiles", []) if isinstance(farm, dict) else []
                return {
                    "farmer": acts[0],
                    "hands": acts[1:],
                    "market": agent.policy.market_orders(farm, private, tiles, obs.get("day", 0)) if isinstance(farm, dict) else [],
                }
            return inert_action(obs, configuration)
        return _fn

    state = env.run([agent_fn(0), agent_fn(1)])
    final = state[-1]
    obs0 = final[player_position].observation
    farm = obs0.get("farms", [])[player_position]
    private = obs0.get("private", {})
    if isinstance(private, list):
        private = private[player_position] if 0 <= player_position < len(private) else {}
    tiles = farm.get("tiles", [])
    shed = private.get("shed", {}) if isinstance(private, dict) else {}

    productive_tiles = 0
    total_working_tiles = 0
    for row in tiles:
        for tile in row:
            if tile == "LOCKED":
                continue
            total_working_tiles += 1
            if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                productive_tiles += 1

    return {
        "seed": seed,
        "player_position": player_position,
        "status": final[player_position].status,
        "final_money": farm.get("money", 0.0),
        "productive_tiles": productive_tiles,
        "total_working_tiles": total_working_tiles,
        "land_utilization_pct": round(100.0 * productive_tiles / total_working_tiles, 2) if total_working_tiles else 0.0,
        "workers": 1 + len(farm.get("hands", []) or []),
        "shed_contents": shed,
        "action_counts": action_counts,
        "no_op_count": no_op_count,
        "day": obs0.get("day"),
        "step": obs0.get("step"),
    }


def main():
    results = []
    for seed in SEEDS:
        for pos in (0, 1):
            r = run_episode(seed, pos)
            results.append(r)
            print(json.dumps(r, indent=2))
    out_path = Path(__file__).parent.parent / "results" / "model_spec_c2" / "copilot" / "PERFORMANCE_BENCHMARK_720_RAW.json"
    out_path.write_text(json.dumps(results, indent=2))
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
