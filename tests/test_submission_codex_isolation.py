"""Codex-specific standalone submission isolation tests."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from kaggle_environments import make

from agricola.strategy.codex_c2 import create_agent
from scripts.build_submission_codex import build_submission_codex


def test_build_submission_codex_fixed_canonical_artifact():
    out_path = build_submission_codex()

    assert out_path == Path.cwd() / "submission" / "submission_codex.py"
    assert out_path.exists()
    assert not (Path.cwd() / "submission_codex.py").exists()

    bundled = out_path.read_text(encoding="utf-8")
    assert 'candidate_id": "CODEX_C2"' in bundled
    assert "class CodexC2Agent" in bundled
    assert "class CodexDecisionLifecycle" in bundled
    assert "CODEX-C2-COMPACT-Q0-ROUTINE-V7" in bundled
    assert "antigravity" not in bundled.lower()
    assert "copilot" not in bundled.lower()


def test_submission_codex_behavioral_equivalence_required_seeds():
    sub_path = build_submission_codex()

    for episode_sequence, seed in enumerate((26090101, 26090102), start=1):
        mod_name = f"submission_codex_test_iso_{seed}"
        spec = importlib.util.spec_from_file_location(mod_name, sub_path)
        sub_mod = importlib.util.module_from_spec(spec)
        sys.modules[mod_name] = sub_mod
        spec.loader.exec_module(sub_mod)

        agent_src = create_agent(
            run_context={
                "run_id": "codex-c2-compact-q0-standalone-parity",
                "episode_id": f"codex-parity-{episode_sequence:04d}",
                "seed": seed,
                "opponent_id": "INERT_PASS_POLICY",
                "player_position": 0,
            }
        )
        env_src = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed})
        obs_src = env_src.reset()

        env_sub = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed})
        obs_sub = env_sub.reset()

        # Technical prefix parity only.  Economic 720-step evaluation is gated
        # until the complete technical suite passes.
        for turn in range(120):
            act_src = agent_src(obs_src[0].observation)
            act_sub = sub_mod.agent(obs_sub[0].observation)

            assert act_src == act_sub, (
                f"Codex submission mismatch on seed {seed}, turn {turn + 1}: "
                f"source={act_src} vs standalone={act_sub}"
            )

            obs_src = env_src.step([act_src, {"farmer": ["PASS"], "hands": [], "market": []}])
            obs_sub = env_sub.step([act_sub, {"farmer": ["PASS"], "hands": [], "market": []}])
            assert obs_src[0].status == obs_sub[0].status
            if obs_src[0].status in ("DONE", "INVALID", "ERROR"):
                break

        assert obs_src[0].status == obs_sub[0].status
