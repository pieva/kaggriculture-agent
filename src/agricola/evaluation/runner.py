"""Evaluation runner for benchmarking agents in local Kaggriculture matches.

Provides precise tracking of:
- Agent-specific decision latency per turn (ms)
- Overall simulation step duration (ms)
- Disqualification / invalid episode rate (%)
- Win, loss, tie rates and final money metrics across opponents
"""

import time
import json
from typing import Dict, Any, List, Union, Callable
import numpy as np
import kaggle_environments


class TimedAgentWrapper:
    """Wrapper around an agent function to measure exact per-turn execution latency."""

    def __init__(self, agent_fn: Callable):
        self.agent_fn = agent_fn
        self.latencies_ms: List[float] = []

    def __call__(self, observation: Dict[str, Any], configuration: Any = None) -> Dict[str, Any]:
        t0 = time.perf_counter()
        action = self.agent_fn(observation, configuration)
        t1 = time.perf_counter()
        self.latencies_ms.append((t1 - t0) * 1000.0)
        return action


def resolve_agent(agent_arg: Union[str, Callable]) -> Union[str, Callable]:
    """Convert agent string path or callable into an agent executable by kaggle_environments."""
    if callable(agent_arg):
        return agent_arg
    if isinstance(agent_arg, str) and (agent_arg.endswith(".py") or "/" in agent_arg or "\\" in agent_arg):
        # Load custom python file as an executable agent function
        import importlib.util
        spec = importlib.util.spec_from_file_location("dynamic_agent", agent_arg)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "agent"):
                return mod.agent
    return agent_arg


def run_episode(
    agent_p0: Union[str, Callable],
    agent_p1: Union[str, Callable],
    steps: int = 720,
    seed: int = None,
    track_p0: bool = True,
    track_p1: bool = False,
) -> Dict[str, Any]:
    """Run a single episode between two agents and return detailed statistics.

    If track_p0 is True, wraps agent_p0 in TimedAgentWrapper to measure exact agent latency.
    """
    resolved_p0 = resolve_agent(agent_p0)
    resolved_p1 = resolve_agent(agent_p1)

    wrapper_p0 = TimedAgentWrapper(resolved_p0) if (track_p0 and callable(resolved_p0)) else None
    wrapper_p1 = TimedAgentWrapper(resolved_p1) if (track_p1 and callable(resolved_p1)) else None

    exec_p0 = wrapper_p0 if wrapper_p0 else resolved_p0
    exec_p1 = wrapper_p1 if wrapper_p1 else resolved_p1

    env_config = {"episodeSteps": steps}
    if seed is not None:
        env_config["seed"] = seed

    env = kaggle_environments.make("kaggriculture", configuration=env_config)

    start_time = time.perf_counter()
    env.run([exec_p0, exec_p1])
    total_time = time.perf_counter() - start_time

    last_step = env.steps[-1]
    p0_reward = last_step[0].get("reward", 0.0) or 0.0
    p1_reward = last_step[1].get("reward", 0.0) or 0.0

    p0_status = last_step[0].get("status", "DONE")
    p1_status = last_step[1].get("status", "DONE")

    num_steps = len(env.steps)
    completed = num_steps == steps and p0_status == "DONE" and p1_status == "DONE"
    disqualified_p0 = p0_status == "INVALID" or p0_status == "ERROR" or p0_reward is None
    disqualified_p1 = p1_status == "INVALID" or p1_status == "ERROR" or p1_reward is None

    p0_latencies = wrapper_p0.latencies_ms if wrapper_p0 else []
    p1_latencies = wrapper_p1.latencies_ms if wrapper_p1 else []

    return {
        "p0_reward": float(p0_reward),
        "p1_reward": float(p1_reward),
        "p0_status": p0_status,
        "p1_status": p1_status,
        "total_steps": num_steps,
        "completed": completed,
        "disqualified_p0": disqualified_p0,
        "disqualified_p1": disqualified_p1,
        "total_time_sec": total_time,
        "simulation_mean_step_time_ms": (total_time / max(1, num_steps)) * 1000.0,
        "p0_agent_mean_latency_ms": float(np.mean(p0_latencies)) if p0_latencies else 0.0,
        "p0_agent_max_latency_ms": float(np.max(p0_latencies)) if p0_latencies else 0.0,
        "p1_agent_mean_latency_ms": float(np.mean(p1_latencies)) if p1_latencies else 0.0,
        "p1_agent_max_latency_ms": float(np.max(p1_latencies)) if p1_latencies else 0.0,
    }


def evaluate_agent(
    agent_under_test: Union[str, Callable],
    opponents: List[str],
    episodes_per_opponent: int = 10,
    steps_per_episode: int = 720,
) -> Dict[str, Any]:
    """Evaluate an agent against multiple opponents and aggregate performance metrics."""
    results: Dict[str, Any] = {
        "summary": {},
        "opponents": {},
    }

    all_rewards = []
    all_wins = 0
    all_losses = 0
    all_ties = 0
    all_episodes_count = 0
    all_completed_count = 0
    all_disqualified_count = 0
    all_agent_latencies = []
    all_sim_step_times = []

    for opponent in opponents:
        print(f"Evaluating vs '{opponent}' ({episodes_per_opponent} episodes)...", flush=True)
        opp_results = {
            "episodes": [],
            "wins": 0,
            "losses": 0,
            "ties": 0,
            "rewards": [],
        }

        # Half playing as P0, half as P1 to eliminate turn order advantage
        p0_count = episodes_per_opponent // 2

        for i in range(episodes_per_opponent):
            playing_as_p0 = i < p0_count
            if playing_as_p0:
                ep = run_episode(
                    agent_under_test, opponent, steps=steps_per_episode, seed=i * 100, track_p0=True, track_p1=False
                )
                my_reward = ep["p0_reward"]
                opp_reward = ep["p1_reward"]
                my_disqualified = ep["disqualified_p0"]
                my_latency = ep["p0_agent_mean_latency_ms"]
            else:
                ep = run_episode(
                    opponent, agent_under_test, steps=steps_per_episode, seed=i * 100, track_p0=False, track_p1=True
                )
                my_reward = ep["p1_reward"]
                opp_reward = ep["p0_reward"]
                my_disqualified = ep["disqualified_p1"]
                my_latency = ep["p1_agent_mean_latency_ms"]

            all_episodes_count += 1
            if ep["completed"]:
                all_completed_count += 1
            if my_disqualified:
                all_disqualified_count += 1

            if my_latency > 0:
                all_agent_latencies.append(my_latency)
            all_sim_step_times.append(ep["simulation_mean_step_time_ms"])

            opp_results["rewards"].append(my_reward)
            all_rewards.append(my_reward)

            if my_reward > opp_reward:
                opp_results["wins"] += 1
                all_wins += 1
            elif my_reward < opp_reward:
                opp_results["losses"] += 1
                all_losses += 1
            else:
                opp_results["ties"] += 1
                all_ties += 1

            opp_results["episodes"].append({
                "as_player": 0 if playing_as_p0 else 1,
                "my_reward": my_reward,
                "opp_reward": opp_reward,
                "completed": ep["completed"],
                "disqualified": my_disqualified,
                "agent_mean_latency_ms": my_latency,
            })

        opp_rewards_arr = np.array(opp_results["rewards"])
        opp_results["win_rate_pct"] = (opp_results["wins"] / episodes_per_opponent) * 100.0
        opp_results["mean_reward"] = float(np.mean(opp_rewards_arr))
        opp_results["std_reward"] = float(np.std(opp_rewards_arr))
        opp_results["median_reward"] = float(np.median(opp_rewards_arr))

        results["opponents"][opponent] = opp_results

    all_rewards_arr = np.array(all_rewards)
    results["summary"] = {
        "total_episodes": all_episodes_count,
        "completion_rate_pct": (all_completed_count / all_episodes_count) * 100.0 if all_episodes_count > 0 else 0.0,
        "disqualification_rate_pct": (all_disqualified_count / all_episodes_count) * 100.0 if all_episodes_count > 0 else 0.0,
        "overall_win_rate_pct": (all_wins / all_episodes_count) * 100.0 if all_episodes_count > 0 else 0.0,
        "overall_wins": all_wins,
        "overall_losses": all_losses,
        "overall_ties": all_ties,
        "mean_final_money": float(np.mean(all_rewards_arr)),
        "std_final_money": float(np.std(all_rewards_arr)),
        "median_final_money": float(np.median(all_rewards_arr)),
        "min_final_money": float(np.min(all_rewards_arr)),
        "max_final_money": float(np.max(all_rewards_arr)),
        "agent_mean_turn_latency_ms": float(np.mean(all_agent_latencies)) if all_agent_latencies else 0.0,
        "simulation_mean_step_time_ms": float(np.mean(all_sim_step_times)) if all_sim_step_times else 0.0,
    }

    return results
