"""Unit test to verify 100% behavioral equivalence between canonical source strategy and generated standalone submission."""

import importlib.util
from pathlib import Path
from kaggle_environments import make
from agricola.core.state import GameState
from agricola.strategy.productive_mass_roi import ProductiveMassROIAgent, ProductiveMassConfig
from scripts.build_submission import build_submission


def test_submission_behavioral_equivalence_x112_required_seeds(tmp_path):
    """Verify standalone submission matches X1.12 source on required seeds."""
    sub_path = tmp_path / "submission.py"
    build_submission(str(sub_path))
    assert sub_path.exists(), "submission/submission.py does not exist!"

    config_src = ProductiveMassConfig(
        productive_core_mode="E12_TRUEBELIEF_ENGINE_X112",
        enable_land_expansion=True,
        target_cows=7,
        target_sheep=4,
        max_workers=6,
        stop_hire_day=1,
    )

    for seed in (0, 421521921):
        spec = importlib.util.spec_from_file_location(f"standalone_sub_{seed}", sub_path)
        sub_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sub_mod)

        agent_src = ProductiveMassROIAgent(config=config_src)
        env_src = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed})
        obs_src = env_src.reset()

        env_sub = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed})
        obs_sub = env_sub.reset()

        for s in range(720):
            gs_src = GameState(obs_src[0].observation)
            act_src = agent_src.act(gs_src)
            act_sub = sub_mod.agent(obs_sub[0].observation)

            assert act_src == act_sub, (
                f"Behavioral discrepancy on seed {seed}, turn {s + 1}: "
                f"Canonical={act_src} vs Standalone={act_sub}"
            )

            obs_src = env_src.step([act_src, {}])
            obs_sub = env_sub.step([act_sub, {}])
            assert obs_src[0].status == obs_sub[0].status
            if obs_src[0].status in ("DONE", "INVALID", "ERROR"):
                break

        assert (obs_src[0].reward or 0.0) == (obs_sub[0].reward or 0.0)
        assert obs_sub[0].reward in (42491.0, 48313.0)
