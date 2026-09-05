"""Report checks run on frozen summaries, never invoking either game agent."""

from statistics import mean, median

import pytest

from docs.model_specs.codex.e18.tools.build_e18_29_simulation_report import (
    EXTRA, REASONS, STANDARD, build_dataset, ratio, render_fragment,
)


@pytest.fixture(scope="module")
def report():
    return build_dataset()


def test_cohorts_and_standard_coverage(report):
    assert [report["cohorts"][k]["n"] for k in ("candidate", "parent", "top770")] == [14, 14, 5]
    assert len(STANDARD) == 21 and len(EXTRA) == 4
    for series in report["series"].values():
        assert set(STANDARD) <= series.keys()
        assert all(len(rows) == 30 for rows in series.values())
        assert all(lo <= mid <= hi for rows in series.values() for mid, lo, hi in rows)


def test_no_missing_as_zero(report):
    assert "fertilizer_collected" not in report["series"]["top770"]
    assert report["operational"]["top770"]["fertilizer_collected_mean"] is None
    assert report["series"]["top770"]["GOOSE"] == [[0, 0, 0]] * 30
    assert ratio(2, 0) is None


def test_matched_profiles_and_aggregation(report):
    candidate = report["profile_daily"]["candidate"]
    parent = report["profile_daily"]["parent"]
    assert {p["identity"] for p in candidate} == {p["identity"] for p in parent}
    for i in range(30):
        assert report["series"]["candidate"]["money"][i][0] == median(p["daily"][i]["money"] for p in candidate)


def test_pass_partition_daily_and_cumulative(report):
    profiles = report["profile_daily"]["candidate"]
    for i, row in enumerate(report["pass_reasons"]["daily_mean"]):
        assert sum(row[k] for k in REASONS) == pytest.approx(mean(p["daily"][i]["PASS"] for p in profiles))
    assert sum(report["pass_reasons"]["total_mean"].values()) == pytest.approx(report["operational"]["candidate"]["pass_mean"])
    assert report["pass_reasons"]["unrecoverable_not_proven"] is True


def test_economic_reconciliation(report):
    candidate, parent = (report["operational"][k] for k in ("candidate", "parent"))
    assert candidate["cash_mean"] - parent["cash_mean"] == pytest.approx(5721)
    assert candidate["pass_mean"] - parent["pass_mean"] == pytest.approx(-420)
    assert candidate["commands_mean"] == parent["commands_mean"] == 7389
    assert candidate["commands_mean"] == pytest.approx(candidate["move_mean"] + candidate["pass_mean"] + candidate["operational_requested_mean"])
    assert candidate["water_mean"] == parent["water_mean"]
    assert candidate["feed_mean"] == parent["feed_mean"]


def test_exceptions_and_release_hold_remain_visible(report):
    assert report["economic_gate_passed"] is True
    assert report["release_gate_passed"] is False
    assert report["crop_exceptions"] == [{"seed": 180903005, "seat": 1, "service_day": 12, "position": [4, 8], "crop": "STRAWBERRY"}]
    assert report["checked_parent_crop_events"] == [{"service_day": 12, "position": [4, 8], "crop": "STRAWBERRY"}]
    assert report["extra_missions"]["started"] == report["extra_missions"]["completed"] == 900
    assert report["extra_missions"]["completion_rate"] == 1


def test_provenance_hashes(report):
    assert len(report["sources"]) == 8
    assert all(len(sha) == 64 for sha in report["sources"].values())
    assert report["cohorts"]["top770"]["frozen"] is True


def test_water_feed_reconcile_with_executed_totals(report):
    for name, profiles in report["profile_daily"].items():
        for opcode in ("WATER", "FEED"):
            total_mean = mean(sum(d[opcode] for d in p["daily"]) for p in profiles)
            assert total_mean == pytest.approx(report["operational"][name][opcode.lower()+"_mean"])
            assert all(isinstance(d[opcode], int) and d[opcode] >= 0 for p in profiles for d in p["daily"])


def test_exactly_two_chart_cohorts_and_no_pass_reasons(report):
    fragment = render_fragment(report)
    assert report["chart_cohorts"] == ("candidate", "top770")
    assert 'data-series="parent"' not in fragment
    assert '"parent":' not in fragment
    assert 'Cause PASS' not in fragment and 'data-reasons' not in fragment
    assert fragment.count('<section data-metric=') == 25
    assert fragment.count('aria-pressed="true"') == 2
    assert 'data-metric="WATER"' in fragment and 'data-metric="FEED"' in fragment


def test_post_d15_gap_not_declared_resolved(report):
    window = report["pass_windows"]["D15-D30"]
    assert window["candidate"]["pass_mean"] == pytest.approx(347.2857142857143)
    assert window["parent"]["pass_mean"] == pytest.approx(734.7142857142857)
    assert window["top770"]["pass_mean"] == 209
    assert window["candidate"]["pass_share_pooled"] > window["top770"]["pass_share_pooled"]


def test_no_validated_early_cash_or_cow_improvement(report):
    cows = report["progressive_cows"]
    assert cows["candidate_parent_cash_d1_d11_identical"] is True
    assert cows["candidate_cows_d1_d10"] == [2,2,2,2,4,4,4,4,4,9]
    assert cows["solution_validated"] is False
    assert len(cows["rejected_trials"]) == 4
    assert all(p["animal_losses"] == 1 and p["cows_d1_d10"][-1] == 8 for p in cows["rejected_trials"])
