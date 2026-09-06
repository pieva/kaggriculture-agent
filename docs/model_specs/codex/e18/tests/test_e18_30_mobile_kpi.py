"""The mobile charts use current V2 candidates and frozen Top770 only."""

from statistics import mean, median

import pytest

from docs.model_specs.codex.e18.tools.build_e18_30_mobile_kpi import (
    PANELS,
    build_dataset,
)


@pytest.fixture(scope="module")
def data():
    return build_dataset()


def test_two_cohorts_21_metrics_and_observed_ranges(data):
    assert data["chart_cohorts"] == ["candidate", "top770"]
    assert set(data["series"]) == {"candidate", "top770"}
    assert len(PANELS) == 21
    for group in data["series"].values():
        assert set(group) == {p[0] for p in PANELS}
        assert all(len(points) == 30 for points in group.values())
        assert all(
            lo <= mid <= hi for points in group.values() for mid, lo, hi in points
        )


def test_v2_not_prior_agent_and_no_new_simulation(data):
    assert data["cohorts"]["candidate"]["version"] == "E18.30 CROP_POOL V2"
    assert data["cohorts"]["candidate"]["n"] == 14
    assert data["cohorts"]["top770"]["n"] == 5
    assert data["cohorts"]["top770"]["frozen"] is True
    assert not data["new_simulation"] and not data["holdout_consumed"]
    assert data["summary"]["candidate"]["cash_mean"] == 81976
    assert data["summary"]["candidate"]["cash_median"] == 79523


def test_medians_and_audited_flow_totals(data):
    for name, profiles in data["profile_daily"].items():
        for metric, _, _ in PANELS:
            for i in range(30):
                assert data["series"][name][metric][i][0] == median(
                    p["daily"][i][metric] for p in profiles
                )
        for op in ("WATER", "FEED", "MOVE", "PASS"):
            assert data["summary"][name][op + "_mean"] == mean(
                sum(d[op] for d in p["daily"]) for p in profiles
            )


def test_zero_species_safety_and_post_d15_gap_visible(data):
    for name in data["series"]:
        assert data["series"][name]["GOOSE"] == [[0, 0, 0]] * 30
        assert data["series"][name]["verified_animal_losses"] == [[0, 0, 0]] * 30
    assert data["summary"]["candidate"]["pass_d15_d30_mean"] == pytest.approx(
        303.57142857142856
    )
    assert data["summary"]["top770"]["pass_d15_d30_mean"] == 209


def test_frozen_sources_and_all_profile_days_present(data):
    assert len(data["sources"]) == 4
    assert all(len(value) == 64 for value in data["sources"].values())
    for group in data["profile_daily"].values():
        assert all(len(p["daily"]) == 30 for p in group)
