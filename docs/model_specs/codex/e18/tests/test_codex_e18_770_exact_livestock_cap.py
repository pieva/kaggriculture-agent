"""Contract tests for E18.12 exact livestock cap."""

from agricola.strategy.codex.codex_e18_770_exact_livestock_cap import (
    E18_770_EXACT_LIVESTOCK_CAP_MODEL_SPEC_VERSION,
    create_codex_e18_770_exact_livestock_cap,
    load_e18_770_exact_livestock_cap_config,
)


def test_config_is_exact_14_for_exact_770() -> None:
    config = load_e18_770_exact_livestock_cap_config()
    assert config["model_spec_version"] == (
        E18_770_EXACT_LIVESTOCK_CAP_MODEL_SPEC_VERSION
    )
    assert config["pasture_topology"] == {"Q0": 7, "Q1": 7, "Q2": 0}
    assert config["pasture_fill_target"] == 14
    assert config["livestock_resource_cap"] == 14
    assert config["in_transit_buffer"] == 0


def test_agent_applies_exact_cap_to_market_filters() -> None:
    policy = create_codex_e18_770_exact_livestock_cap()
    agent = policy.codex_e18_770_exact_livestock_cap_instance
    assert agent.livestock_resource_cap == 14
    assert agent.config["pre_q2_livestock_resource_cap"] == 14
    assert agent.config["livestock_resource_cap"] == 14
    telemetry = agent.telemetry_snapshot()
    assert telemetry["livestock_resource_cap"] == 14
    assert telemetry["worker_route_mutations"] == 0
    assert telemetry["crop_lifecycle_mutation"] is False


def test_market_filter_rejects_fifteenth_livestock_resource() -> None:
    policy = create_codex_e18_770_exact_livestock_cap()
    agent = policy.codex_e18_770_exact_livestock_cap_instance
    tiles = [[None for _ in range(10)] for _ in range(10)]
    for index in range(14):
        x, y = index % 10, index // 10
        tiles[y][x] = {"kind": "PASTURE", "animal": "SHEEP"}
    observation = {
        "player": 0,
        "farms": [
            {
                "tiles": tiles,
                "unlocked_quadrants": ["NW", "NE", "SW"],
            }
        ],
        "private": {"shed": {}, "inventories": []},
    }
    action = {
        "market": [
            ["BUY_ANIMAL", "SHEEP", 1],
            ["BUY_SEED", "WHEAT", 1],
        ]
    }

    agent._filter_market(action, observation)

    assert action["market"] == [["BUY_SEED", "WHEAT", 1]]
    assert agent.clamped_animal_units == {"SHEEP": 1}
