"""Verify isolation and exact source parity of the Codex V7.3 submission."""

from __future__ import annotations

import builtins
import importlib.util
import re
import sys
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.codex_dual_q1_cadence import create_cadence_agent

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUBMISSION_PATH = (
    PROJECT_ROOT / "submission" / "submission_codex_v7_3_dual_q1_cadence.py"
)
SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}


def _load_submission(module_name: str):
    source = SUBMISSION_PATH.read_text(encoding="utf-8")
    if re.search(r"^\s*(?:from|import)\s+agricola(?:\.|\s|$)", source, re.MULTILINE):
        raise AssertionError("standalone submission contains a local agricola import")
    if "DEFAULT_DUAL_CONFIG_PATH" in source or "DEFAULT_CADENCE_CONFIG_PATH" in source:
        raise AssertionError("standalone submission contains an external config path")

    spec = importlib.util.spec_from_file_location(module_name, SUBMISSION_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot create submission module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    real_import = builtins.__import__

    def blocked_import(
        name: str,
        globals: dict[str, Any] | None = None,
        locals: dict[str, Any] | None = None,
        fromlist: tuple[str, ...] = (),
        level: int = 0,
    ):
        if name == "agricola" or name.startswith("agricola."):
            raise ImportError("repository-local imports are blocked")
        return real_import(name, globals, locals, fromlist, level)

    builtins.__import__ = blocked_import
    try:
        spec.loader.exec_module(module)
    finally:
        builtins.__import__ = real_import
    return module


def verify_equivalence(
    seeds: tuple[int, ...] = (26090101, 26090102, 26090103),
    seats: tuple[int, ...] = (0, 1),
    max_steps: int = 720,
) -> bool:
    for sequence, (seed, seat) in enumerate(
        ((seed, seat) for seed in seeds for seat in seats), start=1
    ):
        module = _load_submission(f"codex_v73_submission_{seed}_{seat}")
        if module.CADENCE_MODEL_SPEC_VERSION != "CODEX-C2-V7.3-DUAL-Q1-CADENCE":
            raise AssertionError("wrong embedded candidate version")
        source_agent = create_cadence_agent(
            run_context={
                "run_id": "codex-v7-3-submission-parity",
                "episode_id": f"codex-v7-3-parity-{sequence:04d}",
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
        steps = env.reset()
        for turn in range(max_steps):
            observation = steps[seat].observation
            source_action = source_agent(observation)
            standalone_action = module.agent(observation)
            if source_action != standalone_action:
                raise AssertionError(
                    f"parity mismatch seed={seed} seat={seat} turn={turn}: "
                    f"source={source_action!r} standalone={standalone_action!r}"
                )
            joint_action = (
                [source_action, SAFE_PASS]
                if seat == 0
                else [SAFE_PASS, source_action]
            )
            steps = env.step(joint_action)
            if steps[seat].status in {"DONE", "INVALID", "ERROR"}:
                break
        if steps[seat].status in {"INVALID", "ERROR"}:
            raise AssertionError(
                f"illegal terminal status seed={seed} seat={seat}: "
                f"{steps[seat].status}"
            )
        print(
            f"PASS seed={seed} seat={seat}: "
            f"{min(max_steps, turn + 1)} exact-action steps"
        )
    print("PASS: standalone isolation and exact V7.3 source parity")
    return True


if __name__ == "__main__":
    raise SystemExit(0 if verify_equivalence() else 1)

