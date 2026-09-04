"""Contract tests for E18.16 coherent livestock safety."""

from agricola.strategy.codex.codex_e18_770_exact_cap_critical_feed import (
    E18_770_EXACT_CAP_CRITICAL_FEED_MODEL_SPEC_VERSION,
    create_codex_e18_770_exact_cap_critical_feed,
    load_e18_770_exact_cap_critical_feed_config,
)


def test_config_binds_fourteen_slots_to_the_d20_feed_guard() -> None:
    config = load_e18_770_exact_cap_critical_feed_config()
    assert config["model_spec_version"] == (
        E18_770_EXACT_CAP_CRITICAL_FEED_MODEL_SPEC_VERSION
    )
    assert config["pasture_topology"] == {"Q0": 7, "Q1": 7, "Q2": 0}
    assert config["livestock_resource_cap"] == 14
    assert config["in_transit_buffer"] == 0
    assert config["critical_feed_activation_day"] == 19


def test_agent_applies_exact_cap_without_changing_crop_or_workers() -> None:
    policy = create_codex_e18_770_exact_cap_critical_feed()
    agent = policy.codex_e18_770_exact_cap_critical_feed_instance
    telemetry = agent.telemetry_snapshot()
    assert agent.config["pre_q2_livestock_resource_cap"] == 14
    assert agent.config["livestock_resource_cap"] == 14
    assert telemetry["livestock_resource_cap"] == 14
    assert telemetry["market_mutation"] == "BUY_ANIMAL_CLAMP_ONLY"
    assert telemetry["livestock_cap_mutation"] is True
    assert telemetry["worker_count_mutation"] is False
    assert telemetry["crop_lifecycle_mutation"] is False
