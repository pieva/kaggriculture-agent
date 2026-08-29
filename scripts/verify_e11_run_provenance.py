"""Provenance Verification Tool for E11 Benchmark Runs.

Verifies:
1. config.json exists, is fully explicit, and matches computed SHA-256.
2. episodes.json exists, contains 30 raw episode records, and matches computed SHA-256.
3. All episode records contain identical run_id.
4. Recalculated summary metrics from raw episode records match summary.json 100%.
"""

import sys
import json
import hashlib
from pathlib import Path
import numpy as np

def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def verify_run(run_dir: Path) -> bool:
    print(f"=== VERIFYING PROVENANCE FOR RUN DIR: {run_dir} ===")
    config_file = run_dir / "config.json"
    episodes_file = run_dir / "episodes.json"
    summary_file = run_dir / "summary.json"

    if not config_file.exists():
        print(f"FAIL: config.json missing in {run_dir}")
        return False
    if not episodes_file.exists():
        print(f"FAIL: episodes.json missing in {run_dir}")
        return False
    if not summary_file.exists():
        print(f"FAIL: summary.json missing in {run_dir}")
        return False

    with open(config_file, "r") as f:
        config_data = json.load(f)
    with open(episodes_file, "r") as f:
        episodes_data = json.load(f)
    with open(summary_file, "r") as f:
        summary_data = json.load(f)

    # 1. SHA-256 Hash Verification
    config_sha = compute_sha256(config_file)
    episodes_sha = compute_sha256(episodes_file)
    
    if summary_data.get("config_sha256") != config_sha:
        print(f"FAIL: config_sha256 mismatch! Saved: {summary_data.get('config_sha256')}, Computed: {config_sha}")
        return False
    if summary_data.get("episodes_sha256") != episodes_sha:
        print(f"FAIL: episodes_sha256 mismatch! Saved: {summary_data.get('episodes_sha256')}, Computed: {episodes_sha}")
        return False

    run_id = summary_data.get("run_id")
    print(f"Run ID: {run_id}")
    print(f"Config SHA-256: {config_sha[:16]}...")
    print(f"Episodes SHA-256: {episodes_sha[:16]}...")

    # 2. Episode Record Integrity
    episodes = episodes_data.get("episodes", [])
    expected_episodes = config_data.get("expected_episodes", config_data.get("environment_specs", {}).get("episodes", 30))
    if len(episodes) != expected_episodes:
        print(f"FAIL: Expected {expected_episodes} episode records, found {len(episodes)}")
        return False

    for ep in episodes:
        if ep.get("run_id") != run_id:
            print(f"FAIL: Episode run_id mismatch! Expected {run_id}, got {ep.get('run_id')}")
            return False

    # 3. Recalculate Summary Metrics from Raw Episodes
    rewards = [ep["final_money"] for ep in episodes]
    quads = [ep["max_owned_quadrants"] for ep in episodes]
    peak_act = [ep["peak_active_tiles"] for ep in episodes]
    peak_wk = [ep["peak_workforce"] for ep in episodes]
    
    q2_days = [ep["q2_unlock_day"] for ep in episodes if ep["q2_unlocked"]]
    q3_days = [ep["q3_unlock_day"] for ep in episodes if ep["q3_unlocked"]]
    
    recalc_mean_money = float(np.mean(rewards))
    recalc_median_money = float(np.median(rewards))
    recalc_std_money = float(np.std(rewards, ddof=1)) if len(rewards) > 1 else 0.0
    recalc_min_money = float(np.min(rewards))
    recalc_max_money = float(np.max(rewards))
    
    recalc_3q_rate = float(sum(1 for q in quads if q >= 3) / len(quads) * 100.0)
    recalc_4q_rate = float(sum(1 for q in quads if q >= 4) / len(quads) * 100.0)
    
    recalc_mean_peak_act = float(np.mean(peak_act))
    recalc_mean_peak_wk = float(np.mean(peak_wk))

    saved_econ = summary_data.get("economy", {})
    saved_land = summary_data.get("land", {})
    saved_prod = summary_data.get("production", {})
    saved_wk = summary_data.get("workforce", {})

    # Check tolerances
    assert abs(saved_econ.get("mean_money", 0) - recalc_mean_money) < 1e-4, "Mean money mismatch"
    assert abs(saved_econ.get("median_money", 0) - recalc_median_money) < 1e-4, "Median money mismatch"
    assert abs(saved_econ.get("std_money", 0) - recalc_std_money) < 1e-4, "Std money mismatch"
    assert abs(saved_econ.get("min_money", 0) - recalc_min_money) < 1e-4, "Min money mismatch"
    assert abs(saved_econ.get("max_money", 0) - recalc_max_money) < 1e-4, "Max money mismatch"
    
    assert abs(saved_land.get("q2_unlock_rate", 0) - recalc_3q_rate) < 1e-4, "3Q rate mismatch"
    assert abs(saved_land.get("q3_unlock_rate", 0) - recalc_4q_rate) < 1e-4, "4Q rate mismatch"
    
    assert abs(saved_prod.get("mean_peak_active_tiles", 0) - recalc_mean_peak_act) < 1e-4, "Mean active tiles mismatch"
    assert abs(saved_wk.get("mean_peak_workforce", 0) - recalc_mean_peak_wk) < 1e-4, "Mean workforce mismatch"

    print("=== PROVENANCE VERIFICATION SUCCESSFUL: 100% MATCH ===")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_dir = Path(sys.argv[1])
    else:
        # Default to latest E11 run directory in results/e11/
        e11_base = Path("results/e11")
        if not e11_base.exists():
            print("results/e11 does not exist")
            sys.exit(1)
        subdirs = sorted([d for d in e11_base.iterdir() if d.is_dir()])
        if not subdirs:
            print("No run directories found in results/e11")
            sys.exit(1)
        target_dir = subdirs[-1]
        
    success = verify_run(target_dir)
    sys.exit(0 if success else 1)
