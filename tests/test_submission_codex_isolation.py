"""Codex-specific standalone submission isolation tests."""

import importlib.util
from pathlib import Path

from kaggle_environments import make

from agricola.core.state import GameState
from agricola.strategy.productive_mass_roi import ProductiveMassConfig, ProductiveMassROIAgent
from scripts.build_submission_codex import build_submission_codex


def test_build_submission_codex_fixed_canonical_artifact():
    out_path = build_submission_codex()

    assert out_path == Path.cwd() / "submission" / "submission_codex.py"
    assert out_path.exists()
    assert not (Path.cwd() / "submission_codex.py").exists()

    bundled = out_path.read_text(encoding="utf-8")
    assert 'productive_core_mode="E12_X115_CODEX_INDEPENDENT"' in bundled
    assert 'x115_variant="D"' in bundled
    assert "antigravity" not in bundled.lower()
    assert "copilot" not in bundled.lower()


def test_submission_codex_behavioral_equivalence_required_seeds():
    sub_path = build_submission_codex()
    config_src = ProductiveMassConfig(
        productive_core_mode="E12_X115_CODEX_INDEPENDENT",
        enable_land_expansion=True,
        target_cows=12,
        target_sheep=3,
        max_workers=6,
        stop_hire_day=1,
        x115_variant="D",
        x115_max_hands=12,
    )

    for seed in (0, 421521921):
        spec = importlib.util.spec_from_file_location(f"submission_codex_{seed}", sub_path)
        sub_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sub_mod)

        agent_src = ProductiveMassROIAgent(config=config_src)
        env_src = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed})
        obs_src = env_src.reset()

        env_sub = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed})
        obs_sub = env_sub.reset()

        for turn in range(720):
            state_src = GameState(obs_src[0].observation)
            act_src = agent_src.act(state_src)
            act_sub = sub_mod.agent(obs_sub[0].observation)

            assert act_src == act_sub, (
                f"Codex submission mismatch on seed {seed}, turn {turn + 1}: "
                f"source={act_src} vs standalone={act_sub}"
            )

            obs_src = env_src.step([act_src, {}])
            obs_sub = env_sub.step([act_sub, {}])
            assert obs_src[0].status == obs_sub[0].status
            if obs_src[0].status in ("DONE", "INVALID", "ERROR"):
                break

        assert (obs_src[0].reward or 0.0) == (obs_sub[0].reward or 0.0)
