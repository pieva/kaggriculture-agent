#!/usr/bin/env python3
"""E15 Pairwise Tournament Runner for Kaggriculture.

Enforces strict freeze integrity:
- Executes ONLY frozen standalone submissions from results/e15/freeze/
- Verifies SHA256 hashes against experiments/archive/e15/artifacts/freeze/FREEZE_MANIFEST.md before execution
- Fails closed if any frozen artifact is missing or altered
- Matches:
    M1: Antigravity (P0) vs Codex (P1)      [Seed: 1113294977]
    M2: Codex (P0) vs Copilot (P1)          [Seed: 3033283457]
    M3: Copilot (P0) vs Antigravity (P1)    [Seed: 3122977751]

Usage:
  python experiments/archive/e01/tools/run_e15_tournament.py --validate
  python experiments/archive/e01/tools/run_e15_tournament.py --match M1
  python experiments/archive/e01/tools/run_e15_tournament.py --match M2
  python experiments/archive/e01/tools/run_e15_tournament.py --match M3
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


FREEZE_MANIFEST_PATH = "experiments/archive/e15/artifacts/freeze/FREEZE_MANIFEST.md"
FROZEN_ONTOLOGY_PATH = "experiments/archive/e15/artifacts/freeze/ONTOLOGY_E15_FROZEN.md"

# Immutable pre-declared tournament match configurations
MATCH_CONFIGS = {
    "M1": {
        "match_id": "M1",
        "name": "M1_antigravity_vs_codex",
        "p0_name": "Antigravity",
        "p1_name": "Codex",
        "p0_frozen_submission": "experiments/archive/e15/artifacts/freeze/submission_antigravity_E15_FROZEN.py",
        "p1_frozen_submission": "experiments/archive/e15/artifacts/freeze/submission_codex_E15_FROZEN.py",
        "p0_frozen_model_spec": "experiments/archive/e15/artifacts/freeze/MODEL_SPEC_ANTIGRAVITY_E15_FROZEN.md",
        "p1_frozen_model_spec": "experiments/archive/e15/artifacts/freeze/MODEL_SPEC_CODEX_E15_FROZEN.md",
        "seed": 1113294977,
        "output_dir": "results/e15/M1_antigravity_vs_codex",
    },
    "M2": {
        "match_id": "M2",
        "name": "M2_codex_vs_copilot",
        "p0_name": "Codex",
        "p1_name": "Copilot",
        "p0_frozen_submission": "experiments/archive/e15/artifacts/freeze/submission_codex_E15_FROZEN.py",
        "p1_frozen_submission": "experiments/archive/e15/artifacts/freeze/submission_copilot_E15_FROZEN.py",
        "p0_frozen_model_spec": "experiments/archive/e15/artifacts/freeze/MODEL_SPEC_CODEX_E15_FROZEN.md",
        "p1_frozen_model_spec": "experiments/archive/e15/artifacts/freeze/MODEL_SPEC_COPILOT_E15_FROZEN.md",
        "seed": 3033283457,
        "output_dir": "results/e15/M2_codex_vs_copilot",
    },
    "M3": {
        "match_id": "M3",
        "name": "M3_copilot_vs_antigravity",
        "p0_name": "Copilot",
        "p1_name": "Antigravity",
        "p0_frozen_submission": "experiments/archive/e15/artifacts/freeze/submission_copilot_E15_FROZEN.py",
        "p1_frozen_submission": "experiments/archive/e15/artifacts/freeze/submission_antigravity_E15_FROZEN.py",
        "p0_frozen_model_spec": "experiments/archive/e15/artifacts/freeze/MODEL_SPEC_COPILOT_E15_FROZEN.md",
        "p1_frozen_model_spec": "experiments/archive/e15/artifacts/freeze/MODEL_SPEC_ANTIGRAVITY_E15_FROZEN.md",
        "seed": 3122977751,
        "output_dir": "results/e15/M3_copilot_vs_antigravity",
    },
}


def compute_sha256(filepath: str) -> str:
    """Compute SHA256 hex digest of a file."""
    p = Path(filepath)
    if not p.exists():
        return "FILE_NOT_FOUND"
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load_freeze_manifest(manifest_path: str = FREEZE_MANIFEST_PATH) -> Dict[str, Dict[str, str]]:
    """Parse expected frozen artifact paths and SHA256 checksums from FREEZE_MANIFEST.md."""
    p = Path(manifest_path)
    if not p.exists():
        raise FileNotFoundError(f"Freeze manifest not found at: {manifest_path}")

    manifest_data: Dict[str, Dict[str, str]] = {}
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("|") and not line.startswith("|---") and not "Artifact Name" in line:
                cols = [c.strip().strip("`") for c in line.split("|")[1:-1]]
                if len(cols) >= 4:
                    art_name, src_path, frozen_path, expected_sha = cols[0], cols[1], cols[2], cols[3]
                    manifest_data[frozen_path] = {
                        "artifact_name": art_name,
                        "source_path": src_path,
                        "frozen_path": frozen_path,
                        "expected_sha256": expected_sha,
                    }
    return manifest_data


def verify_freeze_integrity(manifest_path: str = FREEZE_MANIFEST_PATH) -> Tuple[bool, Dict[str, Dict[str, str]], List[str]]:
    """Verify on-disk SHA256 hashes of all 7 frozen artifacts against FREEZE_MANIFEST.md.

    Fails closed if manifest is missing, if any artifact is missing, or if any SHA256 mismatches.
    """
    errors: List[str] = []
    try:
        manifest_data = load_freeze_manifest(manifest_path)
    except Exception as e:
        return False, {}, [f"Failed to load freeze manifest: {e}"]

    if len(manifest_data) != 7:
        errors.append(f"Expected 7 frozen artifacts in manifest, found {len(manifest_data)}")

    for frozen_path, item in manifest_data.items():
        actual_sha = compute_sha256(frozen_path)
        item["actual_sha256"] = actual_sha

        if actual_sha == "FILE_NOT_FOUND":
            errors.append(f"MISSING FROZEN ARTIFACT: {frozen_path} ({item['artifact_name']})")
        elif actual_sha != item["expected_sha256"]:
            errors.append(
                f"INTEGRITY MISMATCH: {frozen_path}\n"
                f"  Expected: {item['expected_sha256']}\n"
                f"  Actual:   {actual_sha}"
            )

    is_ok = len(errors) == 0
    return is_ok, manifest_data, errors


def validate_setup() -> bool:
    """Validate frozen artifacts, match mappings, seeds, and Kaggle environment without running matches."""
    print("=== E15 Pre-Match Freeze Integrity & Setup Validation ===")

    # 1. Verify Freeze Manifest and SHA256 of all 7 frozen artifacts
    freeze_ok, manifest_data, errors = verify_freeze_integrity()
    if freeze_ok:
        print("FREEZE INTEGRITY: PASS (7/7 Frozen Artifacts Verified by SHA256)")
        for path, item in manifest_data.items():
            print(f"  [OK] {item['artifact_name']:<35} -> {path} ({item['expected_sha256'][:16]}...)")
    else:
        print("FREEZE INTEGRITY: FAIL")
        for err in errors:
            print(f"  [ERROR] {err}")
        return False

    # 2. Validate Tournament Match Mappings and Frozen Submissions
    print("\nTournament Match Mapping & Seed Verification:")
    all_matches_ok = True
    for match_id, cfg in MATCH_CONFIGS.items():
        p0_sub = cfg["p0_frozen_submission"]
        p1_sub = cfg["p1_frozen_submission"]
        p0_spec = cfg["p0_frozen_model_spec"]
        p1_spec = cfg["p1_frozen_model_spec"]

        p0_sub_sha = compute_sha256(p0_sub)
        p1_sub_sha = compute_sha256(p1_sub)
        p0_spec_sha = compute_sha256(p0_spec)
        p1_spec_sha = compute_sha256(p1_spec)

        print(f"\n  Match {match_id}: {cfg['p0_name']} (P0) vs {cfg['p1_name']} (P1)")
        print(f"    Pre-Declared Seed: {cfg['seed']}")
        print(f"    P0 Frozen Submission: {p0_sub} (SHA: {p0_sub_sha[:16]}...)")
        print(f"    P1 Frozen Submission: {p1_sub} (SHA: {p1_sub_sha[:16]}...)")
        print(f"    P0 Frozen MODEL_SPEC: {p0_spec} (SHA: {p0_spec_sha[:16]}...)")
        print(f"    P1 Frozen MODEL_SPEC: {p1_spec} (SHA: {p1_spec_sha[:16]}...)")
        print(f"    Output Directory:     {cfg['output_dir']}")

        if p0_sub not in manifest_data or p0_sub_sha != manifest_data[p0_sub]["expected_sha256"]:
            print(f"    [FAIL] P0 submission {p0_sub} does not match freeze manifest!")
            all_matches_ok = False
        if p1_sub not in manifest_data or p1_sub_sha != manifest_data[p1_sub]["expected_sha256"]:
            print(f"    [FAIL] P1 submission {p1_sub} does not match freeze manifest!")
            all_matches_ok = False

    # 3. Validate Kaggle Environment Availability
    try:
        from kaggle_environments import make
        env = make("kaggriculture")
        print(f"\nKaggle Environments Engine: kaggriculture available (v{getattr(env, 'version', '0.1.0')}).")
    except Exception as e:
        print(f"\n[FAIL] Kaggle environments import error: {e}")
        all_matches_ok = False

    if freeze_ok and all_matches_ok:
        print("\n==========================================")
        print("M1: READY")
        print("M2: READY")
        print("M3: READY")
        print("ALL PRE-MATCH CHECKS PASSED — READY FOR AUTHORIZED EXECUTION")
        print("NO MATCH EXECUTED")
        print("==========================================")
        return True
    else:
        print("\n[FAIL] Setup validation failed. Cannot execute tournament.")
        return False


def extract_match_telemetry(env, match_cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Extract step-by-step and aggregate telemetry from completed episode."""
    steps = env.steps
    telemetry: Dict[str, Any] = {
        "match_id": match_cfg["match_id"],
        "seed": match_cfg["seed"],
        "total_steps": len(steps),
        "player_0": match_cfg["p0_name"],
        "player_1": match_cfg["p1_name"],
        "action_counts": {
            "p0": {"WATER": 0, "PLANT": 0, "HARVEST": 0, "CARE": 0, "FEED": 0, "COLLECT_FERTILIZER": 0, "DIG": 0, "MOVE": 0, "PASS": 0, "OTHER": 0},
            "p1": {"WATER": 0, "PLANT": 0, "HARVEST": 0, "CARE": 0, "FEED": 0, "COLLECT_FERTILIZER": 0, "DIG": 0, "MOVE": 0, "PASS": 0, "OTHER": 0},
        },
        "market_orders": {
            "p0": {"HIRE": 0, "BUY_LAND": 0, "BUY_SEED": 0, "BUY_ANIMAL": 0, "BUY_PRODUCT": 0, "SELL": 0},
            "p1": {"HIRE": 0, "BUY_LAND": 0, "BUY_SEED": 0, "BUY_ANIMAL": 0, "BUY_PRODUCT": 0, "SELL": 0},
        },
        "money_trajectory": {"p0": [], "p1": []},
    }

    moves = {"NORTH", "SOUTH", "EAST", "WEST"}

    for step_idx, step_data in enumerate(steps):
        for p_idx, p_key in [(0, "p0"), (1, "p1")]:
            agent_step = step_data[p_idx]
            action = agent_step.get("action", {}) or {}
            farmer_act = action.get("farmer", ["PASS"]) if isinstance(action, dict) else ["PASS"]
            hands_acts = action.get("hands", []) if isinstance(action, dict) else []
            market_acts = action.get("market", []) if isinstance(action, dict) else []

            all_unit_acts = [farmer_act] + (hands_acts if isinstance(hands_acts, list) else [])
            for u_act in all_unit_acts:
                if isinstance(u_act, list) and u_act:
                    op = u_act[0]
                    if op in moves:
                        telemetry["action_counts"][p_key]["MOVE"] += 1
                    elif op in telemetry["action_counts"][p_key]:
                        telemetry["action_counts"][p_key][op] += 1
                    else:
                        telemetry["action_counts"][p_key]["OTHER"] += 1

            if isinstance(market_acts, list):
                for m_act in market_acts:
                    if isinstance(m_act, list) and m_act:
                        m_op = m_act[0]
                        if m_op in telemetry["market_orders"][p_key]:
                            telemetry["market_orders"][p_key][m_op] += 1

            obs = agent_step.get("observation", {}) or {}
            farms = obs.get("farms", [])
            if farms and len(farms) > p_idx:
                telemetry["money_trajectory"][p_key].append(farms[p_idx].get("money", 0))

    return telemetry


def run_match(match_id: str) -> None:
    """Execute a single tournament match strictly using verified frozen submissions (Fail-Closed)."""
    # 1. Strict pre-match freeze verification
    freeze_ok, manifest_data, errors = verify_freeze_integrity()
    if not freeze_ok:
        print("FATAL: Cannot execute match due to Freeze Integrity Violation:")
        for err in errors:
            print(f"  [ERROR] {err}")
        print("\nExecution ABORTED before environment initialization (Fail-Closed).")
        sys.exit(1)

    if match_id not in MATCH_CONFIGS:
        print(f"FATAL: Unknown match ID '{match_id}'. Available matches: M1, M2, M3")
        sys.exit(1)

    cfg = MATCH_CONFIGS[match_id]
    p0_frozen_sub = cfg["p0_frozen_submission"]
    p1_frozen_sub = cfg["p1_frozen_submission"]

    # Ensure frozen submission files exist and match manifest
    if not Path(p0_frozen_sub).exists() or not Path(p1_frozen_sub).exists():
        print(f"FATAL: Frozen submission files missing for match {match_id}.")
        sys.exit(1)

    out_dir = Path(cfg["output_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)

    start_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print(f"\n==========================================")
    print(f"Executing Match {match_id}: {cfg['p0_name']} (P0) vs {cfg['p1_name']} (P1)")
    print(f"Seed: {cfg['seed']}")
    print(f"P0 Frozen Submission: {p0_frozen_sub}")
    print(f"P1 Frozen Submission: {p1_frozen_sub}")
    print(f"Output Directory: {out_dir}")
    print(f"==========================================\n")

    # Import kaggle environments
    from kaggle_environments import make

    # Run strictly with frozen submission filepaths
    env = make("kaggriculture", configuration={"seed": cfg["seed"], "episodeSteps": 720}, debug=True)
    env.run([p0_frozen_sub, p1_frozen_sub])
    end_time = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Final rewards
    final_step = env.steps[-1]
    p0_reward = float(final_step[0].get("reward", 0.0) or 0.0)
    p1_reward = float(final_step[1].get("reward", 0.0) or 0.0)

    if p0_reward > p1_reward:
        winner = cfg["p0_name"]
    elif p1_reward > p0_reward:
        winner = cfg["p1_name"]
    else:
        winner = "TIE"

    print(f"\nMatch {match_id} Completed!")
    print(f"  {cfg['p0_name']} (P0): ${p0_reward:,.2f}")
    print(f"  {cfg['p1_name']} (P1): ${p1_reward:,.2f}")
    print(f"  Winner: {winner} (Delta: ${abs(p0_reward - p1_reward):,.2f})")

    # Match Metadata recording exact frozen artifact provenance
    metadata = {
        "match_id": match_id,
        "name": cfg["name"],
        "seed": cfg["seed"],
        "player_0": cfg["p0_name"],
        "player_1": cfg["p1_name"],
        "freeze_manifest_path": FREEZE_MANIFEST_PATH,
        "frozen_submission_0_path": p0_frozen_sub,
        "frozen_submission_1_path": p1_frozen_sub,
        "submission_0_sha256": compute_sha256(p0_frozen_sub),
        "submission_1_sha256": compute_sha256(p1_frozen_sub),
        "ontology_sha256": compute_sha256(FROZEN_ONTOLOGY_PATH),
        "model_spec_0_sha256": compute_sha256(cfg["p0_frozen_model_spec"]),
        "model_spec_1_sha256": compute_sha256(cfg["p1_frozen_model_spec"]),
        "environment_version": getattr(env, "version", "kaggriculture_default"),
        "start_timestamp": start_time,
        "end_timestamp": end_time,
        "p0_final_reward": p0_reward,
        "p1_final_reward": p1_reward,
        "winner": winner,
    }

    # Summary
    summary = {
        "match_id": match_id,
        "seed": cfg["seed"],
        "winner": winner,
        "p0": {"name": cfg["p0_name"], "final_money": p0_reward},
        "p1": {"name": cfg["p1_name"], "final_money": p1_reward},
        "money_delta": p0_reward - p1_reward,
        "total_steps": len(env.steps),
    }

    # Extract detailed telemetry
    telemetry = extract_match_telemetry(env, cfg)

    # Save outputs
    (out_dir / "match_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out_dir / "telemetry.json").write_text(json.dumps(telemetry, indent=2), encoding="utf-8")
    (out_dir / "raw_replay.json").write_text(json.dumps(env.toJSON(), indent=2), encoding="utf-8")

    print(f"\nAll match artifacts saved to {out_dir}/")


def main():
    parser = argparse.ArgumentParser(description="E15 Tournament Runner (Freeze-Enforced)")
    parser.add_argument("--validate", action="store_true", help="Run pre-match validation without starting any match")
    parser.add_argument("--match", choices=["M1", "M2", "M3"], help="Execute a specific match (M1, M2, or M3)")

    args = parser.parse_args()

    if args.validate or (not args.match):
        ok = validate_setup()
        if not args.match:
            sys.exit(0 if ok else 1)

    if args.match:
        run_match(args.match)


if __name__ == "__main__":
    main()
