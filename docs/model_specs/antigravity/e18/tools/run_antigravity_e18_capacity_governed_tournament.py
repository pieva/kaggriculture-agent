#!/usr/bin/env python3
"""Run the Antigravity E18.2 Capacity Governed development benchmark.

Runs 28 development matches (7 seeds x 2 seats) against Claude E18.2 and Copilot E18.2.
Includes paired ablation comparing capacity_governor_enabled=True vs False on identical matchups.
Outputs JSON and CSV artifacts into docs/model_specs/antigravity/e18/artifacts/derived/.
"""

from __future__ import annotations

import csv
import hashlib
import json
import statistics
import sys
import time
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from kaggle_environments import make

from agricola.strategy.antigravity.antigravity_e18_capacity_governed_v2 import (
    DEFAULT_CONFIG_PATH as ANTIGRAVITY_V2_CONFIG,
    create_antigravity_e18_capacity_governed_agent,
)
from agricola.strategy.claude.e18_opponent_reactive_v2 import (
    DEFAULT_CONFIG_PATH as CLAUDE_CONFIG,
    create_claude_e18_agent_v2,
)
from agricola.strategy.copilot.e18_opponent_reactive_v2 import (
    DEFAULT_CONFIG_PATH as COPILOT_CONFIG,
    create_copilot_e18_opponent_reactive_v2,
)
from experiments.e17.tools.common import (
    run_e17_three_agent_development_tournament_v2 as base,
)
from experiments.e18.tools.common import (
    run_e18_dynamic_architecture_tournament_v1 as prior,
)

DEVELOPMENT_SEEDS = [
    180903001,
    180903002,
    180903003,
    180903004,
    180903005,
    180903006,
    180903007,
]

OUTPUT_DIR = (
    ROOT
    / "docs"
    / "model_specs"
    / "antigravity"
    / "e18"
    / "artifacts"
    / "derived"
)
OUTPUT_JSON = OUTPUT_DIR / "E18_ANTIGRAVITY_CAPACITY_GOVERNED_V1.json"
OUTPUT_CSV = OUTPUT_DIR / "E18_ANTIGRAVITY_CAPACITY_GOVERNED_V1.csv"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _payload_hash(payload: Any) -> str:
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest().upper()


def _run_single_match(
    seed: int,
    antigravity_seat: int,
    opponent_name: str,
    *,
    governor_enabled: bool = True,
) -> dict[str, Any]:
    opp_seat = 1 - antigravity_seat
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed})

    # Contexts
    tag = "V2_GOVERNED" if governor_enabled else "V2_ABLATION_OFF"
    ctx_ag = {
        "run_id": f"E18-AG-{tag}-S{seed}-P{antigravity_seat}",
        "episode_id": f"E18-AG-{tag}-S{seed}-P{antigravity_seat}",
        "seed": seed,
        "player_position": antigravity_seat,
    }
    ctx_opp = {
        "run_id": f"E18-OPP-S{seed}-P{opp_seat}-{opponent_name}",
        "episode_id": f"E18-OPP-S{seed}-P{opp_seat}-{opponent_name}",
        "seed": seed,
        "player_position": opp_seat,
    }

    cfg_ag = json.loads(Path(ANTIGRAVITY_V2_CONFIG).read_text(encoding="utf-8"))
    cfg_ag["capacity_governor_enabled"] = governor_enabled
    ag_callable = create_antigravity_e18_capacity_governed_agent(
        config=cfg_ag,
        run_context=ctx_ag,
    )
    ag_controller = ag_callable.antigravity_e18_instance

    if opponent_name == "CLAUDE_E18_2":
        opp_callable = create_claude_e18_agent_v2(run_context=ctx_opp)
        opp_controller = opp_callable
    elif opponent_name == "COPILOT_E18_2":
        opp_callable = create_copilot_e18_opponent_reactive_v2(run_context=ctx_opp)
        opp_controller = opp_callable
    else:
        raise ValueError(opponent_name)

    agents = [None, None]
    agents[antigravity_seat] = ag_callable
    agents[opp_seat] = opp_callable

    env.run(agents)

    # Telemetry and metrics
    ag_reward = float(env.steps[-1][antigravity_seat].reward or 0.0)
    opp_reward = float(env.steps[-1][opp_seat].reward or 0.0)

    ag_metrics = base._seat_metrics(env, antigravity_seat, "E18_ANTIGRAVITY", ag_controller)
    opp_metrics = base._seat_metrics(env, opp_seat, opponent_name, opp_controller)

    ag_telem = ag_controller.telemetry_snapshot()
    opp_telem = (
        opp_controller.telemetry_snapshot()
        if hasattr(opp_controller, "telemetry_snapshot")
        else {}
    )

    ag_errors = int(getattr(ag_controller, "technical_errors", 0))
    ag_fallbacks = int(getattr(ag_controller, "fallback_count", 0))
    ag_losses = prior._verified_livestock_losses(env, antigravity_seat)

    stream_hash = prior._action_stream_hash(env, antigravity_seat)

    result_type = (
        "WIN"
        if ag_reward > opp_reward
        else ("LOSS" if ag_reward < opp_reward else "TIE")
    )

    return {
        "seed": seed,
        "antigravity_seat": antigravity_seat,
        "opponent_seat": opp_seat,
        "opponent_name": opponent_name,
        "governor_enabled": governor_enabled,
        "result_type": result_type,
        "antigravity_money": ag_reward,
        "opponent_money": opp_reward,
        "margin": ag_reward - opp_reward,
        "ag_technical_errors": ag_errors,
        "ag_fallbacks": ag_fallbacks,
        "ag_verified_livestock_losses": ag_losses,
        "ag_recovery_service_commands": ag_telem.get("recovery_service_commands", 0),
        "ag_recovery_breakdown": ag_telem.get("recovery_breakdown", {}),
        "ag_final_regime": ag_telem.get("final_regime"),
        "ag_peak_crops": ag_metrics.get("peak_crops", 0),
        "ag_peak_hands": ag_metrics.get("peak_hands", 0),
        "ag_action_counts": ag_metrics.get("action_counts", {}),
        "ag_action_stream_hash": stream_hash,
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    opponents = ["CLAUDE_E18_2", "COPILOT_E18_2"]

    print("=================================================================")
    print("Running Antigravity E18.2 Capacity Governed Tournament & Ablation")
    print(f"Seeds: {DEVELOPMENT_SEEDS}")
    print(f"Opponents: {opponents}")
    print("=================================================================\n")

    t0 = time.time()
    governed_matches: list[dict[str, Any]] = []
    ablation_matches: list[dict[str, Any]] = []

    total_pairs = len(DEVELOPMENT_SEEDS) * 2 * len(opponents)
    completed = 0

    for opp in opponents:
        for seed in DEVELOPMENT_SEEDS:
            for seat in [0, 1]:
                completed += 1
                print(f"[{completed}/{total_pairs}] Running S{seed} P{seat} vs {opp} (Governed)...")
                res_gov = _run_single_match(seed, seat, opp, governor_enabled=True)
                governed_matches.append(res_gov)

                print(f"       -> Governed Money: ${res_gov['antigravity_money']:.2f} vs ${res_gov['opponent_money']:.2f} ({res_gov['result_type']}) | Recoveries: {res_gov['ag_recovery_service_commands']}")

                print(f"       Running paired ablation (Governor OFF)...")
                res_abl = _run_single_match(seed, seat, opp, governor_enabled=False)
                ablation_matches.append(res_abl)
                delta = res_gov['antigravity_money'] - res_abl['antigravity_money']
                print(f"       -> Ablation Money: ${res_abl['antigravity_money']:.2f} | Delta: ${delta:+.2f}")

    elapsed = time.time() - t0
    print(f"\nCompleted {completed*2} total matches in {elapsed:.1f}s.")

    # Aggregate Statistics
    gov_money = [m["antigravity_money"] for m in governed_matches]
    abl_money = [m["antigravity_money"] for m in ablation_matches]

    vs_claude_gov = [m for m in governed_matches if m["opponent_name"] == "CLAUDE_E18_2"]
    vs_copilot_gov = [m for m in governed_matches if m["opponent_name"] == "COPILOT_E18_2"]

    vs_claude_abl = [m for m in ablation_matches if m["opponent_name"] == "CLAUDE_E18_2"]
    vs_copilot_abl = [m for m in ablation_matches if m["opponent_name"] == "COPILOT_E18_2"]

    wins = sum(1 for m in governed_matches if m["result_type"] == "WIN")
    losses = sum(1 for m in governed_matches if m["result_type"] == "LOSS")
    ties = sum(1 for m in governed_matches if m["result_type"] == "TIE")

    claude_wins = sum(1 for m in vs_claude_gov if m["result_type"] == "WIN")
    claude_losses = sum(1 for m in vs_claude_gov if m["result_type"] == "LOSS")

    copilot_wins = sum(1 for m in vs_copilot_gov if m["result_type"] == "WIN")
    copilot_losses = sum(1 for m in vs_copilot_gov if m["result_type"] == "LOSS")

    # Direct Paired Comparison
    claude_beat_v1 = sum(
        1 for g, a in zip(vs_claude_gov, vs_claude_abl) if g["antigravity_money"] > a["antigravity_money"]
    )
    copilot_beat_v1 = sum(
        1 for g, a in zip(vs_copilot_gov, vs_copilot_abl) if g["antigravity_money"] > a["antigravity_money"]
    )

    mean_gov = statistics.mean(gov_money)
    min_gov = min(gov_money)
    max_gov = max(gov_money)
    stdev_gov = statistics.stdev(gov_money)

    mean_abl = statistics.mean(abl_money)

    tot_recoveries = sum(m["ag_recovery_service_commands"] for m in governed_matches)
    errors_tot = sum(m["ag_technical_errors"] for m in governed_matches)
    fallbacks_tot = sum(m["ag_fallbacks"] for m in governed_matches)
    livestock_losses_tot = sum(m["ag_verified_livestock_losses"] for m in governed_matches)

    unique_streams = len({m["ag_action_stream_hash"] for m in governed_matches})

    # Save CSV
    fieldnames = [
        "seed",
        "antigravity_seat",
        "opponent_name",
        "governor_enabled",
        "result_type",
        "antigravity_money",
        "opponent_money",
        "margin",
        "ag_technical_errors",
        "ag_fallbacks",
        "ag_verified_livestock_losses",
        "ag_recovery_service_commands",
        "ag_final_regime",
        "ag_peak_crops",
        "ag_peak_hands",
        "ag_action_stream_hash",
    ]
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for m in governed_matches:
            writer.writerow(m)

    # Save JSON
    summary_payload = {
        "candidate_id": "ANTIGRAVITY_E18_2_CAPACITY_GOVERNED_V1",
        "model_spec_version": "ANTIGRAVITY-E18.2-CAPACITY-GOVERNED-V1",
        "matches_count": len(governed_matches),
        "record": f"{wins}-{losses}-{ties}",
        "vs_claude_record": f"{claude_wins}-{claude_losses}-0",
        "vs_copilot_record": f"{copilot_wins}-{copilot_losses}-0",
        "money_mean_governed": round(mean_gov, 2),
        "money_min_governed": round(min_gov, 2),
        "money_max_governed": round(max_gov, 2),
        "money_stdev_governed": round(stdev_gov, 2),
        "money_mean_ablation_off": round(mean_abl, 2),
        "net_capacity_delta": round(mean_gov - mean_abl, 2),
        "claude_higher_than_v1_matches": f"{claude_beat_v1}/14",
        "copilot_higher_than_v1_matches": f"{copilot_beat_v1}/14",
        "total_recovery_service_commands": tot_recoveries,
        "technical_errors": errors_tot,
        "fallbacks": fallbacks_tot,
        "verified_livestock_losses": livestock_losses_tot,
        "unique_action_streams": f"{unique_streams}/{len(governed_matches)}",
        "governed_matches": governed_matches,
        "ablation_matches": ablation_matches,
    }
    OUTPUT_JSON.write_text(json.dumps(summary_payload, indent=2), encoding="utf-8")

    print("\n======================= RESULTS SUMMARY =======================")
    print(f"Overall Record: {wins}-{losses}-{ties}")
    print(f"vs Claude E18.2: {claude_wins}-{claude_losses}-0")
    print(f"vs Copilot E18.2: {copilot_wins}-{copilot_losses}-0")
    print(f"Mean Money (Governed): ${mean_gov:.2f} (min: ${min_gov:.2f}, max: ${max_gov:.2f})")
    print(f"Mean Money (Ablation OFF): ${mean_abl:.2f} | Net Delta: ${mean_gov - mean_abl:+.2f}")
    print(f"Total Recovery Service Commands: {tot_recoveries}")
    print(f"Technical Errors: {errors_tot}, Fallbacks: {fallbacks_tot}, Livestock Losses: {livestock_losses_tot}")
    print(f"Saved artifacts to {OUTPUT_JSON} and {OUTPUT_CSV}")
    print("===============================================================\n")


if __name__ == "__main__":
    main()
