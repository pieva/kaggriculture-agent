"""Reporting only: keep source regimes distinct and successful care separate."""
import json
from statistics import median

import pytest

from docs.model_specs.codex.e18.tools.build_e18_31_desktop_report import (
    DERIVED, STANDARD, build_dataset, render,
)
from docs.model_specs.codex.e18.tools.analyze_e18_31_external_corpus import exact770


@pytest.fixture(scope='module')
def historical():
    return build_dataset(DERIVED/'E18_31_ASSIGNMENT_GATE_UNIFIED_V11_DEVELOPMENT_20260906.json')


def test_v4_is_two_cohorts_and_22_metrics(historical):
    assert len(STANDARD)==22
    assert set(historical['series'])=={'candidate','top770'}
    assert historical['counts']=={'candidate':14,'top770':5}
    assert 'interne' in historical['candidate_regime']
    for cohort in historical['series'].values():
        assert set(cohort)==set(STANDARD)
        assert all(len(points)==30 for points in cohort.values())
        assert all(lo<=mid<=hi for points in cohort.values() for mid,lo,hi in points)


def test_successful_feed_care_water_from_ledger(historical):
    source=json.loads((DERIVED/'E18_31_ASSIGNMENT_GATE_UNIFIED_V11_DEVELOPMENT_20260906.json').read_text(encoding='utf-8'))
    profiles=[p for p in source['matches'] if p['opponent']=='E18.16']
    for op in ('WATER','FEED','CARE'):
        for day in range(30):
            expected=median(p['ledger']['daily'][day]['executed_actions'].get(op,0) for p in profiles)
            assert historical['series']['candidate'][op][day][0]==expected


def test_render_has_distinct_care_and_feed_panels(historical):
    fragment=render(historical,'e31-test-d30')
    assert fragment.count('<section data-metric=')==22
    assert 'data-metric="CARE"' in fragment and 'data-metric="FEED"' in fragment
    assert 'Cause PASS' not in fragment
    assert 'E18.29 B3' not in fragment
    assert len(fragment.encode())<1_000_000


def test_exact770_does_not_accept_1070_or_four_quadrants():
    row={'pasture_topology':{'Q0':7,'Q1':7,'Q2':0,'Q3':0},'unlocked_tiles':75}
    assert exact770(row)
    assert not exact770(row|{'unlocked_tiles':100})
    assert not exact770(row|{'pasture_topology':{'Q0':10,'Q1':7,'Q2':0,'Q3':0}})


def test_public_cohort_includes_loss_but_not_non770_benchmark():
    candidate=DERIVED/'E18_31_EXTERNAL_SUBMISSION_FIRST6_20260906.json'
    top=DERIVED/'E18_31_EXTERNAL_TOP002_FULL_20260906.json'
    data=build_dataset(candidate,top,'Top770-002')
    assert data['counts']=={'candidate':6,'top770':4}
    assert 'pubblici' in data['candidate_regime']
    assert data['top_screen_count']==5
    assert data['top_excluded_episodes']==[106068545]
    assert 106073291 in {p['episode_id'] for p in data['profile_daily']['candidate']}
    for path in (candidate,top):
        profiles=json.loads(path.read_text(encoding='utf-8'))['profiles']
        assert all(p['ledger']['cash_parity_errors']==0 and p['statuses']==['DONE','DONE'] for p in profiles)


def test_land_overlay_keeps_crop_metric_and_frozen_cohorts():
    candidate=DERIVED/'E18_31_EXTERNAL_SUBMISSION_FIRST6_20260906.json'
    top=DERIVED/'E18_31_EXTERNAL_TOP002_FULL_20260906.json'
    old=build_dataset(candidate,top,'Top770-002')
    data=build_dataset(candidate,top,'Top770-002',land_overlay=True)
    assert data['standard']=='V4.1' and data['counts']==old['counts']
    for group in data['series']:
        for metric in STANDARD:
            assert data['series'][group][metric]==old['series'][group][metric]
        expected=([25]*6+[50]*4+[75]*20) if group=='candidate' else ([25]*6+[50]*5+[75]*19)
        assert data['series'][group]['unlocked_tiles']==[[v,v,v] for v in expected]
        for profile in data['profile_daily'][group]:
            assert all(day['crop_tiles']<=day['unlocked_tiles'] for day in profile['daily'])
    assert len(data['land_purchase_events']['candidate'])==6
    assert len(data['land_purchase_events']['top770'])==4
    for group,profiles in data['land_purchase_events'].items():
        for profile in profiles:
            q1,q2=profile['events']
            assert (q1['quadrant'],q1['day'],q1['hour'])==('Q1',7,7)
            assert q2['quadrant']=='Q2'
            if group=='candidate':
                assert q2['day']==11 and q2['hour'] in (2,17)
            else:
                assert (q2['day'],q2['hour'])==(12,2)
    fragment=render(data,'e31-land-test-d30')
    assert fragment.count('<section data-metric=')==22
    assert 'Tile coltivate e totali sbloccate' in fragment
    assert 'data-land-panel' in fragment
