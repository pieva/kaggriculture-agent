from __future__ import annotations

from kaggle_environments import make

from agricola.strategy.codex.codex_3q_mixed_high_density import (
    Q2_CROP_POSITIONS,
    Q2_SHEEP_PASTURES,
    V9_MODEL_SPEC_VERSION,
    create_v9_agent,
    load_v9_config,
)
from agricola.strategy.codex.codex_v9_routine_data import ROUTINE_ACTIONS, ROUTINE_SHA256


def _pass_agent(observation, configuration=None):
    del observation, configuration
    return {"farmer": ["PASS"], "hands": [], "market": []}


def test_v9_config_and_footprint_are_bounded() -> None:
    config = load_v9_config()
    assert config["model_spec_version"] == V9_MODEL_SPEC_VERSION
    assert config["workforce_total"] == 13
    assert config["endgame_shutdown_days"] == 0
    assert len(Q2_SHEEP_PASTURES) == 5
    assert len(Q2_CROP_POSITIONS) == 20
    assert not set(Q2_SHEEP_PASTURES) & set(Q2_CROP_POSITIONS)
    assert len(ROUTINE_ACTIONS) == 719
    assert ROUTINE_SHA256 == "C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4"


def test_v9_short_smoke_is_fail_closed() -> None:
    candidate = create_v9_agent()
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 72, "seed": 26090101, "turnsPerDay": 24},
        debug=True,
    )
    env.run([candidate, _pass_agent])
    assert candidate.codex_v9_instance.error_count == 0
    assert candidate.codex_v9_instance.fallback_count == 0
