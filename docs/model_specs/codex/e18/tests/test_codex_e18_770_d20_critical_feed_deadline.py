"""Contract tests for E18.13 critical FEED deadline."""

from copy import deepcopy

from agricola.strategy.codex.codex_e18_770_d20_critical_feed_deadline import (
    create_codex_e18_770_d20_critical_feed_deadline,
    load_e18_770_d20_critical_feed_deadline_config,
)


def _observation(
    *,
    day: int = 19,
    hour: int = 20,
    fed: bool = False,
    stress: int = 1,
    wheat: int = 1,
) -> dict:
    farm = {
        "money": 10_000,
        "tiles": [[None for _ in range(10)] for _ in range(10)],
        "farmer": [2, 4],
        "hands": [],
        "unlocked_quadrants": ["NW", "NE", "SW"],
    }
    farm["tiles"][4][2] = {
        "kind": "PASTURE",
        "animal": "COW",
        "fed_today": fed,
        "consecutive_unfed": stress,
    }
    return {
        "step": day * 24 + hour,
        "day": day,
        "hour": hour,
        "player": 0,
        "farms": [farm, deepcopy(farm)],
        "private": {"shed": {}, "inventories": [{"WHEAT": wheat}]},
        "market": {"prices": {}},
    }


def _provider(command: list[str]):
    def provider(observation, configuration=None):
        del observation, configuration
        return {"farmer": deepcopy(command), "hands": [], "market": []}

    return provider


def test_eligible_move_becomes_in_place_feed() -> None:
    policy = create_codex_e18_770_d20_critical_feed_deadline(
        base_policy=_provider(["EAST"])
    )
    action = {"farmer": ["EAST"], "hands": [], "market": []}
    agent = policy.codex_e18_770_d20_critical_feed_deadline_instance
    agent._apply_d20_critical_feed(action, _observation())
    assert action["farmer"] == ["FEED"]
    assert agent.move_to_critical_feed_overrides == 1


def test_noncritical_infeasible_or_outside_window_is_immutable() -> None:
    config = load_e18_770_d20_critical_feed_deadline_config()
    assert config["allowed_override"] == "MOVE_TO_IN_PLACE_FEED_ONLY"
    cases = (
        (_observation(hour=19), ["EAST"]),
        (_observation(fed=True), ["EAST"]),
        (_observation(stress=0), ["EAST"]),
        (_observation(wheat=0), ["EAST"]),
        (_observation(), ["PASS"]),
        (_observation(day=20), ["EAST"]),
    )
    for observation, command in cases:
        policy = create_codex_e18_770_d20_critical_feed_deadline(
            base_policy=_provider(command)
        )
        action = {"farmer": deepcopy(command), "hands": [], "market": []}
        agent = policy.codex_e18_770_d20_critical_feed_deadline_instance
        agent._apply_d20_critical_feed(action, observation)
        assert action["farmer"] == command
