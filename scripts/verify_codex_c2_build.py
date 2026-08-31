#!/usr/bin/env python3
"""Technical verification for the Codex compact-Q0 routine candidate."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from kaggle_environments import make

from agricola.strategy.codex_c2 import (
    FOUNDATION_CHECKPOINT,
    MODEL_SPEC_VERSION,
    create_agent,
)
from scripts.build_submission_codex import build_submission_codex

DEFAULT_OUTPUT = (
    REPO_ROOT
    / "results"
    / "model_spec_c2"
    / "codex"
    / "CODEX_V7_1_SERVICEABILITY_TECHNICAL_SMOKE.json"
)
SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}


def inert_policy(
    observation: dict[str, Any], configuration: Any = None
) -> dict[str, Any]:
    del observation, configuration
    return dict(SAFE_PASS)


def _agent_action_stream(env: Any, seat: int) -> list[dict[str, Any]]:
    return [
        (joint_step[seat].get("action", {}) or {})
        for joint_step in env.steps
        if joint_step[seat].get("action")
    ]


def _forbidden_actions(actions: list[dict[str, Any]]) -> list[str]:
    forbidden: list[str] = []
    for action in actions:
        units = [action.get("farmer", ["PASS"]), *(action.get("hands", []) or [])]
        for unit in units:
            if unit and unit[0] == "DROP":
                forbidden.append("DROP")
        for order in action.get("market", []) or []:
            if order and order[0] == "BUY_LAND":
                forbidden.append("BUY_LAND")
    return forbidden


def _run_prefix(*, seat: int, seed: int, steps: int) -> dict[str, Any]:
    episode_agent = create_agent(
        run_context={
            "run_id": "codex-compact-q0-technical",
            "episode_id": f"technical-prefix-seat-{seat}",
            "seed": seed,
            "opponent_id": "INERT_PASS_POLICY",
            "player_position": seat,
        }
    )
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=True,
    )
    observations = env.reset()
    agents = [episode_agent, inert_policy] if seat == 0 else [inert_policy, episode_agent]
    for _ in range(steps):
        shared_step = int(env.steps[-1][0]["observation"]["step"])
        visible = [
            dict(env.steps[-1][index].get("observation", {}) or {})
            for index in range(2)
        ]
        # kaggle-environments' direct step API omits the shared `step` field
        # from seat 1 (env.run injects it before invoking the callable).
        # Restore that public clock field so this prefix harness exercises the
        # same observation contract as a normal two-seat episode.
        visible[1].setdefault("step", shared_step)
        actions = [
            agents[index](visible[index])
            for index in range(2)
        ]
        observations = env.step(actions)
        if observations[seat].status in {"DONE", "INVALID", "ERROR"}:
            break
    instance = episode_agent.codex_c2_instance
    telemetry = instance.telemetry_snapshot()
    action_stream = _agent_action_stream(env, seat)
    farm = observations[seat].observation["farms"][seat]
    failures: list[str] = []
    if observations[seat].status in {"INVALID", "ERROR"}:
        failures.append(f"engine status {observations[seat].status}")
    if instance.error_count or instance.fallback_count:
        failures.append(
            f"agent errors/fallbacks {instance.error_count}/{instance.fallback_count}"
        )
    forbidden = _forbidden_actions(action_stream)
    if forbidden:
        failures.append(f"forbidden actions: {sorted(set(forbidden))}")
    if len(farm.get("unlocked_quadrants", []) or []) != 1:
        failures.append("candidate left Q0")
    if steps >= 24 and len(farm.get("hands", []) or []) not in {0, 6}:
        failures.append("workforce is neither EOD-expired nor six active hands")
    return {
        "seat": seat,
        "seed": seed,
        "steps_requested": steps,
        "status": observations[seat].status,
        "errors": instance.error_count,
        "fallbacks": instance.fallback_count,
        "last_exception": instance.last_exception,
        "forbidden_actions": forbidden,
        "roles": telemetry["current_roles"],
        "technical_pass": not failures,
        "failures": failures,
    }


def _run_terminal(*, seat: int, seed: int) -> dict[str, Any]:
    episode_agent = create_agent(
        run_context={
            "run_id": "codex-compact-q0-terminal",
            "episode_id": f"terminal-seat-{seat}",
            "seed": seed,
            "opponent_id": "INERT_PASS_POLICY",
            "player_position": seat,
        }
    )
    agents = [episode_agent, inert_policy] if seat == 0 else [inert_policy, episode_agent]
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 48, "seed": seed, "turnsPerDay": 24},
        debug=True,
    )
    env.run(agents)
    instance = episode_agent.codex_c2_instance
    status = env.steps[-1][seat].get("status", "UNKNOWN")
    lifecycle_state = instance.telemetry_snapshot()["lifecycle"]["state"]
    failures: list[str] = []
    if status != "DONE":
        failures.append(f"terminal status {status}")
    if lifecycle_state != "TERMINAL_CLOSED":
        failures.append(f"terminal lifecycle {lifecycle_state}")
    if instance.error_count or instance.fallback_count:
        failures.append(
            f"agent errors/fallbacks {instance.error_count}/{instance.fallback_count}"
        )
    return {
        "seat": seat,
        "seed": seed,
        "status": status,
        "lifecycle_state": lifecycle_state,
        "technical_pass": not failures,
        "failures": failures,
    }


def _isolated_import() -> dict[str, Any]:
    path = build_submission_codex()
    module_name = "submission_codex_compact_q0_technical"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        return {"technical_pass": False, "failure": "spec creation failed"}
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return {
        "technical_pass": callable(getattr(module, "agent", None)),
        "path": str(path),
    }


def run_verification(*, seed: int, prefix_steps: int) -> dict[str, Any]:
    prefixes = [
        _run_prefix(seat=seat, seed=seed, steps=prefix_steps)
        for seat in (0, 1)
    ]
    terminals = [
        _run_terminal(seat=seat, seed=seed + 1)
        for seat in (0, 1)
    ]
    isolated = _isolated_import()
    technical_pass = (
        all(row["technical_pass"] for row in prefixes)
        and all(row["technical_pass"] for row in terminals)
        and bool(isolated["technical_pass"])
    )
    return {
        "protocol": "CODEX_COMPACT_Q0_ROUTINE_TECHNICAL_VERIFICATION",
        "agent_version": MODEL_SPEC_VERSION,
        "foundation_checkpoint": FOUNDATION_CHECKPOINT,
        "economic_benchmark_executed": False,
        "prefixes": prefixes,
        "terminal_checks": terminals,
        "isolated_submission": isolated,
        "technical_pass": technical_pass,
        "TOURNAMENT_AUTHORIZED": "NO",
        "KAGGLE_AUTHORIZED": "NO",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=26090100)
    parser.add_argument("--prefix-steps", type=int, default=120)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    payload = run_verification(seed=args.seed, prefix_steps=args.prefix_steps)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"technical_pass": payload["technical_pass"]}, indent=2))
    print(f"wrote {args.output}")
    return 0 if payload["technical_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
