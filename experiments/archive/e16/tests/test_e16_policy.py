"""Treatment-boundary and hard-cap tests for the shared E16 policy."""

from __future__ import annotations

from copy import deepcopy

import pytest

from agricola.e16.config import load_frozen_config, resolve_cell
from agricola.e16.policy import (
    CROP_POSITIONS,
    PASTURE_POSITIONS,
    E16TrainingAgent,
    _quota_counts,
    _water_dispatch_rank,
)


def make_observation(quadrants=("NW",), step=0):
    tiles = []
    for y in range(10):
        row = []
        for x in range(10):
            owned = (x < 5 and y < 5) or ("NE" in quadrants and x >= 5 and y < 5)
            row.append(None if owned else "LOCKED")
        tiles.append(row)
    farm = {
        "money": 3000,
        "farmer": [4, 4],
        "hands": [],
        "hires_today": 0,
        "unlocked_quadrants": list(quadrants),
        "tiles": tiles,
    }
    return {
        "step": step,
        "day": step // 24,
        "hour": step % 24,
        "player": 0,
        "farms": [farm, deepcopy(farm)],
        "private": {"shed": {}, "seeds": {}, "inventories": [{}]},
        "market": {"prices": {"WHEAT": 10}, "inventory": {"WHEAT": 100}},
    }


def cell(cell_id="A04"):
    return resolve_cell(load_frozen_config(), "stage_a", cell_id)


def test_e16_common_opening_forbids_pasture_and_livestock():
    action = E16TrainingAgent(cell())(make_observation())
    flattened = [action["farmer"], *action["hands"], *action["market"]]
    assert not any(
        item and item[0] in {"BUILD_PASTURE", "BUY_ANIMAL"} for item in flattened
    )
    assert ["BUY_LAND"] in action["market"]


def test_e16_common_opening_identical_between_cells():
    assert E16TrainingAgent(cell("A01"))(make_observation()) == E16TrainingAgent(
        cell("A04")
    )(make_observation())


def test_e16_t0_is_first_verified_two_quadrant_state():
    agent = E16TrainingAgent(cell())
    agent(make_observation(step=0))
    action = agent(make_observation(("NW", "NE"), step=1))
    assert agent.t0_step == 1
    assert ["BUY_LAND"] not in action["market"]


def test_e16_third_quadrant_order_is_forbidden_after_t0():
    agent = E16TrainingAgent(cell())
    agent(make_observation(step=0))
    agent(make_observation(("NW", "NE"), step=1))
    action = agent(make_observation(("NW", "NE"), step=2))
    assert all(order[0] != "BUY_LAND" for order in action["market"])


def test_e16_observed_third_quadrant_fails_closed():
    agent = E16TrainingAgent(cell())
    with pytest.raises(RuntimeError):
        agent(make_observation(("NW", "NE", "SW"), step=2))


def test_e16_crop_mix_uses_largest_remainder():
    assert _quota_counts(10) == {"WHEAT": 4, "STRAWBERRY": 4, "MELON": 2}
    assert _quota_counts(17) == {"WHEAT": 7, "STRAWBERRY": 7, "MELON": 3}
    assert _quota_counts(25) == {"WHEAT": 10, "STRAWBERRY": 10, "MELON": 5}


def _watering_state(count: int, worker_positions: list[tuple[int, int]]):
    observation = make_observation(("NW", "NE"), step=24)
    farm = observation["farms"][0]
    for x, y in CROP_POSITIONS[:count]:
        farm["tiles"][y][x] = {
            "kind": "PLANT",
            "crop": "WHEAT",
            "watered_today": False,
            "consecutive_unwatered": 0,
            "yield_units": 0,
        }
    for x, y in PASTURE_POSITIONS[:5]:
        farm["tiles"][y][x] = {"kind": "PASTURE"}
    farm["farmer"] = list(worker_positions[0])
    farm["hands"] = [list(position) for position in worker_positions[1:]]
    observation["farms"][1] = deepcopy(farm)
    observation["private"]["inventories"] = [{} for _ in worker_positions]
    return observation


def test_e16_water_dispatch_priority_orders_high_mid_low():
    assert _water_dispatch_rank(0.70) < _water_dispatch_rank(0.45)
    assert _water_dispatch_rank(0.45) < _water_dispatch_rank(0.20)


@pytest.mark.parametrize("cell_id", ["A01", "A05", "A02"])
def test_e16_all_water_needs_are_eligible_with_sufficient_capacity(cell_id):
    positions = list(CROP_POSITIONS[:4])
    action = E16TrainingAgent(cell(cell_id))(_watering_state(4, positions))
    assert [action["farmer"], *action["hands"]] == [["WATER"]] * 4


def test_e16_water_selection_has_no_fixed_prefix_exclusion():
    suffix = CROP_POSITIONS[3]
    action = E16TrainingAgent(cell("A01"))(_watering_state(4, [suffix]))
    assert action["farmer"] == ["WATER"]


def test_e16_water_dispatch_is_deterministic():
    observation = _watering_state(4, list(CROP_POSITIONS[:4]))
    left = E16TrainingAgent(cell("A05"))(deepcopy(observation))
    right = E16TrainingAgent(cell("A05"))(deepcopy(observation))
    assert left == right
