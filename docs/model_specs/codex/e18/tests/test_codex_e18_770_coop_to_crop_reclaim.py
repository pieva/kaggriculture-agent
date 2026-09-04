from __future__ import annotations

from agricola.strategy.codex.codex_e18_770_coop_to_crop_reclaim import (
    CodexE18770CoopToCropReclaimAgent,
    load_e18_770_coop_to_crop_reclaim_config,
)


def _observation(*, position: list[int], day: int = 10) -> dict:
    tiles = [[None for _ in range(10)] for _ in range(10)]
    return {
        "day": day,
        "hour": 14,
        "player": 0,
        "farms": [
            {
                "farmer": position,
                "hands": [],
                "tiles": tiles,
                "unlocked_quadrants": [0, 1, 2],
            }
        ],
        "private": {
            "seeds": {"STRAWBERRY": 1},
            "inventories": [{}],
            "shed": {},
        },
    }


def test_config_freezes_exact_770_and_no_rerouting() -> None:
    config = load_e18_770_coop_to_crop_reclaim_config()
    assert config["pasture_topology"] == {"Q0": 7, "Q1": 7, "Q2": 0}
    assert config["reclaimed_coop_target"] == [4, 1]
    assert config["provider_move_authoritative"] is True
    assert config["allow_worker_rerouting"] is False


def test_build_and_goose_purchase_become_crop_only() -> None:
    agent = CodexE18770CoopToCropReclaimAgent()
    action = {
        "farmer": ["BUILD_COOP"],
        "hands": [],
        "market": [
            ["BUY_ANIMAL", "GOOSE", 1],
            ["BUY_PRODUCT", "WHEAT", 5],
        ],
    }
    agent._apply_coop_reclaim(action, _observation(position=[4, 1]))
    assert action["farmer"] == ["PLANT", "STRAWBERRY"]
    assert action["market"] == [["BUY_PRODUCT", "WHEAT", 5]]
    assert agent.coop_builds_converted_to_crop == 1
    assert agent.goose_market_orders_removed == 1
    assert agent.provider_move_overrides == 0


def test_goose_pickup_is_suppressed_without_moving_worker() -> None:
    agent = CodexE18770CoopToCropReclaimAgent()
    action = {
        "farmer": ["PICKUP", "GOOSE", 1],
        "hands": [],
        "market": [],
    }
    agent._apply_coop_reclaim(action, _observation(position=[4, 4], day=11))
    assert action["farmer"] == ["PASS"]
    assert agent.goose_logistics_suppressed == 1
    assert agent.provider_move_overrides == 0
