"""Benchmark runner for E11-X1.3-B2 — Cross-Boundary Multi-EPU Activation (27 tiles, 1 Land Purchase)."""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Dict, Any, List

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agricola.strategy.productive_mass_roi import ProductiveMassROIAgent, ProductiveMassConfig
from agricola.core.state import GameState
from kaggle_environments import make

# E11-X1.3-B2 Configuration (27 tiles across 1 Land Purchase - Q0+Q1)
E11_X1_3_B2_CONFIG = ProductiveMassConfig(
    productive_core_mode="E06_REPLICATED",
    epu_level=3,
    enable_land_expansion=True,
    workforce_scaling_mode="LEGACY",
    multi_hire_mode="SINGLE_PER_DAY",
    land_buy_mode="IMMEDIATE"
)

E06_REF_SEED0 = 25847.0  # Historical E06 exact seed-0 money reference


def run_episode(agent_instance: ProductiveMassROIAgent, seed: int, opponent_name: str, steps: int = 720) -> Dict[str, Any]:
    """Run a single episode and return complete telemetry."""
    env = make("kaggriculture", configuration={"episodeSteps": steps, "seed": seed})
    state = env.reset()

    for step in range(steps):
        obs0 = state[0].observation
        gs = GameState(obs0)
        act = agent_instance.act(gs)
        try:
            state = env.step([act, {}])
        except Exception as e:
            print(f"Error on step {step}: {e}")
            break

    final_obs = state[0].observation
    final_money = final_obs.farms[0]["money"]
    ep_data = agent_instance.telemetry.to_dict()
    ep_data["seed"] = seed
    ep_data["opponent"] = opponent_name
    ep_data["final_money"] = final_money
    return ep_data


def benchmark_b2(stage: str = "B") -> None:
    """Run Stage A0 (1 seed) or Stage B (5 paired seeds) benchmark for B2."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    run_id = f"E11-X1.3-B2-{timestamp}"
    results_dir = Path(__file__).parent.parent / "results" / "e11" / run_id
    results_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== LAUNCHING E11-X1.3-B2 STAGE {stage} ({run_id}) ===")

    # Paired seeds and opponents
    if stage == "A0":
        seeds_opponents = [(0, "pass")]
    else:
        seeds_opponents = [
            (0, "pass"),
            (100, "pass"),
            (200, "random"),
            (300, "random"),
            (400, "starter"),
        ]

    treatment_episodes = []

    for idx, (seed, opp) in enumerate(seeds_opponents, 1):
        agent_treat = ProductiveMassROIAgent(config=E11_X1_3_B2_CONFIG)
        treat_data = run_episode(agent_treat, seed, opp)
        treat_data["run_id"] = run_id
        treat_data["max_owned_quadrants"] = treat_data.get("owned_quadrants", 1)
        treat_data["peak_active_tiles"] = treat_data.get("peak_productive_tiles", 0)
        treat_data["peak_workforce"] = treat_data.get("peak_simultaneous_workers", 1)
        treat_data["q2_unlocked"] = treat_data.get("owned_quadrants", 1) >= 2
        treat_data["q3_unlocked"] = treat_data.get("owned_quadrants", 1) >= 3
        treat_data["q2_unlock_day"] = 14 if treat_data["q2_unlocked"] else None
        treat_data["q3_unlock_day"] = 16 if treat_data["q3_unlocked"] else None
        treatment_episodes.append(treat_data)

        q_count = treat_data.get("owned_quadrants", 1)
        peak_wk = treat_data.get("peak_simultaneous_workers", 1)
        peak_act = treat_data.get("peak_active_tiles", 0)
        print(f"Episode {idx:2d}/{len(seeds_opponents)} | Seed {seed:3d} vs {opp:7s} | Money: ${treat_data['final_money']:8.2f} | Q: {q_count} | PeakWk: {peak_wk} | PeakAct: {peak_act}")

    # Summary calculations
    treat_moneys = [e["final_money"] for e in treatment_episodes]
    mean_treat = sum(treat_moneys) / len(treat_moneys)
    equiv_ratio = (mean_treat / E06_REF_SEED0) * 100.0

    # Write config, episodes, summary for provenance verification
    import dataclasses
    config_dict = dataclasses.asdict(E11_X1_3_B2_CONFIG)
    config_dict["run_id"] = run_id
    config_dict["expected_episodes"] = len(seeds_opponents)
    config_dict["subphase"] = "B2"
    config_dict["stage"] = stage

    config_file = results_dir / "config.json"
    episodes_file = results_dir / "episodes.json"
    summary_file = results_dir / "summary.json"

    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config_dict, f, indent=2)

    episodes_file_data = {
        "run_id": run_id,
        "episodes": treatment_episodes
    }

    with open(episodes_file, "w", encoding="utf-8") as f:
        json.dump(episodes_file_data, f, indent=2)

    import hashlib
    def get_hash(fp):
        h = hashlib.sha256()
        with open(fp, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()

    import numpy as np

    rewards = [ep["final_money"] for ep in treatment_episodes]
    quads = [ep.get("max_owned_quadrants", 1) for ep in treatment_episodes]
    peak_act = [ep.get("peak_active_tiles", 0) for ep in treatment_episodes]
    peak_wk = [ep.get("peak_workforce", 1) for ep in treatment_episodes]

    summary_dict = {
        "run_id": run_id,
        "config_sha256": get_hash(config_file),
        "episodes_sha256": get_hash(episodes_file),
        "episodes_count": len(treatment_episodes),
        "equivalence_ratio_pct": equiv_ratio,
        "economy": {
            "mean_money": float(np.mean(rewards)),
            "median_money": float(np.median(rewards)),
            "std_money": float(np.std(rewards, ddof=1)) if len(rewards) > 1 else 0.0,
            "min_money": float(np.min(rewards)),
            "max_money": float(np.max(rewards))
        },
        "land": {
            "q2_unlock_rate": float(sum(1 for q in quads if q >= 3) / len(quads) * 100.0),
            "q3_unlock_rate": float(sum(1 for q in quads if q >= 4) / len(quads) * 100.0)
        },
        "production": {
            "mean_peak_active_tiles": float(np.mean(peak_act))
        },
        "workforce": {
            "mean_peak_workforce": float(np.mean(peak_wk))
        }
    }

    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary_dict, f, indent=2)

    print("\n=== BENCHMARK COMPLETED — RUNNING PROVENANCE VERIFIER ===")
    from verify_e11_run_provenance import verify_run
    ok = verify_run(results_dir)
    if not ok:
        print(f"PROVENANCE VERIFICATION FAILED FOR {results_dir}")
        sys.exit(1)

    print(f"SUCCESS: E11-X1.3-B2 STAGE {stage} ESTABLISHED AND VERIFIED IN {results_dir}")
    print(f"Treatment Mean Money: ${mean_treat:.2f} | Equivalence Ratio vs E06 Seed 0 (${E06_REF_SEED0:.2f}): {equiv_ratio:.1f}%\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run E11-X1.3-B2 benchmark")
    parser.add_argument("--stage", type=str, default="B", choices=["A0", "B"], help="Stage A0 (1 seed) or B (5 paired seeds)")
    args = parser.parse_args()
    benchmark_b2(stage=args.stage)
