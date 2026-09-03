#!/usr/bin/env python3
"""Verify isolated import and full-episode parity of the V4D submission."""

from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

from kaggle_environments import make

from agricola.core.benchmark_opponents import inert_pass_policy
from agricola.strategy.codex.codex_e17_batched_cluster_routing_v4 import (
    DEFAULT_V4D_CONFIG_PATH,
    V4D_MODEL_SPEC_VERSION,
    create_codex_e17_batched_cluster_routing_v4,
)

ROOT = Path(__file__).resolve().parents[4]
TARGET = ROOT / "submission/submission_codex_e17_v4d.py"
EXPECTED_RELEASE = "CODEX-E17.2-V4D-D28-KAGGLE-CANDIDATE-V1"
SEEDS = (26090101, 26090102, 26090103)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _load():
    spec = importlib.util.spec_from_file_location("codex_e17_v4d_submission", TARGET)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {TARGET}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _isolated_import() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            (
                "import importlib.util;"
                f"p={str(TARGET)!r};"
                "s=importlib.util.spec_from_file_location('iso',p);"
                "m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"
                "assert callable(m.agent);assert callable(m.create_agent);"
                f"assert m.RELEASE_ID=={EXPECTED_RELEASE!r};"
                f"assert m.MODEL_SPEC_VERSION=={V4D_MODEL_SPEC_VERSION!r}"
            ),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout)


def _full_episode_parity(module, seed: int, seat: int) -> int:
    context = {
        "run_id": f"E17-V4D-SUBMISSION-PARITY-S{seed}-P{seat}",
        "episode_id": f"E17-V4D-SUBMISSION-PARITY-S{seed}-P{seat}",
        "seed": seed,
        "player_position": seat,
    }
    source = create_codex_e17_batched_cluster_routing_v4(
        run_context=context,
        config_path=DEFAULT_V4D_CONFIG_PATH,
    )
    standalone = module.create_agent(run_context=deepcopy(context))
    source_actions: list[dict] = []
    standalone_actions: list[dict] = []

    def capture(policy, actions):
        def wrapped(observation, configuration=None):
            action = policy(observation, configuration)
            actions.append(deepcopy(action))
            return action

        return wrapped

    env_source = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=True,
    )
    env_standalone = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=True,
    )
    source_agents = (
        [capture(source, source_actions), inert_pass_policy]
        if seat == 0
        else [inert_pass_policy, capture(source, source_actions)]
    )
    standalone_agents = (
        [capture(standalone, standalone_actions), inert_pass_policy]
        if seat == 0
        else [inert_pass_policy, capture(standalone, standalone_actions)]
    )
    env_source.run(source_agents)
    env_standalone.run(standalone_agents)
    if len(source_actions) != len(standalone_actions):
        raise AssertionError(
            f"action count mismatch seed={seed} seat={seat}: "
            f"source={len(source_actions)} standalone={len(standalone_actions)}"
        )
    if source_actions != standalone_actions:
        mismatch = next(
            index
            for index, (source_action, standalone_action) in enumerate(
                zip(source_actions, standalone_actions, strict=False)
            )
            if source_action != standalone_action
        )
        raise AssertionError(
            f"action mismatch seed={seed} seat={seat} turn={mismatch}: "
            f"source={source_actions[mismatch]!r} "
            f"standalone={standalone_actions[mismatch]!r}"
        )
    source_terminal = env_source.steps[-1][seat]
    standalone_terminal = env_standalone.steps[-1][seat]
    if source_terminal.get("status") != standalone_terminal.get("status"):
        raise AssertionError("terminal status mismatch")
    if source_terminal.get("reward") != standalone_terminal.get("reward"):
        raise AssertionError("terminal reward mismatch")
    source_instance = source.codex_e17_batched_cluster_routing_instance
    standalone_instance = standalone.codex_e17_batched_cluster_routing_instance
    if source_instance.error_count or standalone_instance.error_count:
        raise AssertionError(
            "technical error observed during parity: "
            f"seed={seed} seat={seat} "
            f"source_errors={source_instance.error_count} "
            f"source_last={source_instance.last_exception!r} "
            f"standalone_errors={standalone_instance.error_count} "
            f"standalone_last={standalone_instance.last_exception!r}"
        )
    if source_instance.fallback_count or standalone_instance.fallback_count:
        raise AssertionError("fallback observed during parity")
    print(
        f"seed={seed} seat={seat} comparisons={len(source_actions)} "
        f"reward={float(source_terminal.get('reward') or 0):.0f} parity=PASS",
        flush=True,
    )
    return len(source_actions)


def main() -> int:
    _isolated_import()
    module = _load()
    if module.RELEASE_ID != EXPECTED_RELEASE:
        raise AssertionError("unexpected release metadata")
    if module.MODEL_SPEC_VERSION != V4D_MODEL_SPEC_VERSION:
        raise AssertionError("unexpected model spec metadata")
    comparisons = sum(
        _full_episode_parity(module, seed, seat)
        for seed in SEEDS
        for seat in (0, 1)
    )
    if comparisons != 719 * len(SEEDS) * 2:
        raise AssertionError(f"unexpected comparison count: {comparisons}")
    print(
        f"isolated_import=PASS action_parity={comparisons}/{comparisons} "
        f"submission_sha256={_sha256(TARGET)} holdout_consumed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
