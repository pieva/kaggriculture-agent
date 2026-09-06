import json

import pytest

from docs.model_specs.codex.e18.tools.analyze_e18_30_pass_phases import build
from docs.model_specs.codex.e18.tools.build_e18_30_desktop_kpi import (
    DATASET,
    render_fragment,
)


def test_desktop_has_21_panels_and_exactly_two_current_cohorts():
    data = json.loads(DATASET.read_text(encoding="utf-8"))
    fragment = render_fragment(data)
    assert fragment.count('<section data-metric="') == 21
    assert fragment.count('aria-pressed="true"') == 2
    assert "E18.29" not in fragment and "Cause PASS" not in fragment
    assert '"parent":' not in fragment
    assert "grid-template-columns:repeat(2,minmax(0,1fr))" in fragment
    assert 'data-metric="WATER"' in fragment and 'data-metric="FEED"' in fragment
    assert "__REPORT_" not in fragment


def test_desktop_series_preserve_mobile_numbers():
    data = json.loads(DATASET.read_text(encoding="utf-8"))
    fragment = render_fragment(data)
    serialized = fragment.split("const data=", 1)[1].split(";", 1)[0]
    assert json.loads(serialized) == data["series"]


def test_phase_evidence_is_not_a_d15_pool_switch():
    data = build()
    assert all(r["pool_missions_started_mean"] == 0 for r in data["daily"][:11])
    assert data["windows"]["D1-D15"]["candidate"] == 801
    assert data["windows"]["D16-D30"]["candidate"] == pytest.approx(289.2857142857143)
    assert data["legacy_calendar_rules"]["fertilizer_collection_caps_by_day"]["16"] == 3
    assert data["legacy_calendar_rules"]["fertilizer_collection_caps_by_day"]["17"] == 0
    assert not data["new_simulation"] and not data["policy_changed"]
