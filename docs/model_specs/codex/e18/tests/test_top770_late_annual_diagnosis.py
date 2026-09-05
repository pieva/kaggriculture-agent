"""Frozen-evidence and engine checks behind the D25-D30 diagnosis."""

import importlib
import json
from pathlib import Path

import pytest

BASE = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def engine():
    return importlib.import_module(
        "kaggle_environments.envs.kaggriculture.kaggriculture"
    )


def crop_cycle(engine, crop, harvest_age, fertilized=False):
    farm = {
        "tiles": [[None] * 10 for _ in range(10)],
        "farmer": [0, 0],
        "hands": [],
        "money": 1000,
    }
    private = {
        "seeds": {crop: 1},
        "inventories": [{"FERTILIZER": 1} if fertilized else {}],
        "shed": {},
    }

    def act(command, day):
        engine._apply_unit_action(farm, private, 0, command, 10, day, 24, 100)

    act(["PLANT", crop], 0)
    for age in range(harvest_age + 1):
        if fertilized and age == 2:
            act(["FERTILIZE"], age)
        act(["WATER"], age)
        if age < harvest_age:
            engine._daily_refresh_plants(farm, age, 24)
    act(["HARVEST"], harvest_age)
    return farm, private


@pytest.mark.parametrize(
    "crop,age,fertilized,units",
    [
        ("CARROT", 1, False, 0),
        ("WHEAT", 1, False, 0),
        ("CARROT", 2, False, 2),
        ("WHEAT", 2, False, 2),
        ("CARROT", 3, False, 3),
        ("WHEAT", 3, False, 3),
        ("CARROT", 2, True, 3),
        ("CARROT", 3, True, 4),
        ("WHEAT", 4, False, 4),
        ("WHEAT", 4, True, 6),
    ],
)
def test_actual_yield_not_nominal_cap(engine, crop, age, fertilized, units):
    _, private = crop_cycle(engine, crop, age, fertilized)
    assert private["inventories"][0].get(crop, 0) == units


def test_carrot_decay_starts_at_age_four(engine):
    farm = {"tiles": [[None] * 10 for _ in range(10)]}
    tile = engine._new_plant("CARROT", 0, 24)
    tile["yield_units"] = 3
    farm["tiles"][0][0] = tile
    engine._decay_plants(farm, 95)
    assert tile["yield_units"] == 3
    engine._decay_plants(farm, 96)
    assert tile["yield_units"] == 2


def test_frozen_late_choice_and_cash_reconciliation():
    payload = json.loads(
        (
            BASE / "artifacts/derived/E18_27_TOP770_D25_D30_CARROT_DIAGNOSIS.json"
        ).read_text()
    )
    choice = payload["late_species_choice"]
    assert (
        choice["same_late_slots"],
        choice["always_carrot_slots"],
        choice["switchable_slots"],
        choice["switchable_harvest_units"],
    ) == (42, 6, 36, 87)
    top = [p for p in payload["profiles"] if p["cohort"] == "Top770"]
    assert len(top) == 5
    for p in top:
        window = p["D25_D30"]
        assert window["harvested"]["WHEAT"] + window["harvested"]["CARROT"] == 260
        assert (
            sum(d["sold"] for d in p["carrot_daily"]) == window["sold_units"]["CARROT"]
        )
        assert (
            sum(d["cash"] for d in p["carrot_daily"]) == window["sales_cash"]["CARROT"]
        )
        assert p["carrot_cycles"]["fertilizer_applications"] == 0
        assert all(c["plant"]["day"] == 29 for c in p["carrot_cycles"]["unharvested"])


def test_no_legacy_named_markdown_files():
    root = BASE.parents[3]
    assert not [p for p in (root / "docs").rglob("*.md") if "jesse" in p.name.lower()]
