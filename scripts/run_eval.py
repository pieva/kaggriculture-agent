"""CLI tool to execute local evaluation benchmarks for Kaggriculture agents."""

import sys
import argparse
import json
from pathlib import Path

# Add src directory to python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agricola.agent import agent as default_agent
from agricola.evaluation.runner import evaluate_agent


def main():
    parser = argparse.ArgumentParser(description="Run local evaluation benchmark for Kaggriculture agent.")
    parser.add_argument(
        "--opponents",
        type=str,
        default="pass,random,starter",
        help="Comma-separated list of opponent agents (default: pass,random,starter)",
    )
    parser.add_argument(
        "--episodes",
        type=int,
        default=10,
        help="Number of episodes to run per opponent (default: 10)",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=720,
        help="Number of steps per episode (default: 720)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results/e01_baseline.json",
        help="Output JSON file path for metric report (default: results/e01_baseline.json)",
    )

    args = parser.parse_args()
    opponent_list = [op.strip() for op in args.opponents.split(",") if op.strip()]

    print(f"Starting evaluation of default agent against opponents: {opponent_list}", flush=True)
    print(f"Episodes per opponent: {args.episodes}, Steps per episode: {args.steps}\n", flush=True)

    results = evaluate_agent(
        agent_under_test=default_agent,
        opponents=opponent_list,
        episodes_per_opponent=args.episodes,
        steps_per_episode=args.steps,
    )

    print("=== SUMMARY RESULTS ===", flush=True)
    summary = results["summary"]
    print(f"Total Episodes:            {summary['total_episodes']}", flush=True)
    print(f"Completion Rate:           {summary['completion_rate_pct']:.2f}%", flush=True)
    print(f"Disqualification Rate:     {summary['disqualification_rate_pct']:.2f}%", flush=True)
    print(f"Overall Win Rate:          {summary['overall_win_rate_pct']:.2f}% ({summary['overall_wins']}W / {summary['overall_losses']}L / {summary['overall_ties']}D)", flush=True)
    print(f"Mean Final Money:          ${summary['mean_final_money']:.2f} +/- ${summary['std_final_money']:.2f}", flush=True)
    print(f"Median Final Money:        ${summary['median_final_money']:.2f}", flush=True)
    print(f"Agent Mean Turn Latency:   {summary['agent_mean_turn_latency_ms']:.4f} ms/turn", flush=True)
    print(f"Sim Mean Step Time:        {summary['simulation_mean_step_time_ms']:.2f} ms/step\n", flush=True)

    print("=== OPPONENT BREAKDOWN ===", flush=True)
    for opp, opp_res in results["opponents"].items():
        print(f"Opponent: {opp:10s} | Win Rate: {opp_res['win_rate_pct']:6.2f}% | Mean Money: ${opp_res['mean_reward']:.2f}", flush=True)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved benchmark metrics to: {output_path}")


if __name__ == "__main__":
    main()
