"""Integrity gates for the frozen public diagnostic, not policy selection."""

import json
from collections import Counter
from pathlib import Path

from docs.model_specs.codex.e18.tools.analyze_e18_28_external_pass import commands, MOVES, pass_summary

BASE = Path(__file__).resolve().parents[1]


def profiles():
    return [json.loads(p.read_text(encoding='utf-8')) for p in
            sorted((BASE / 'artifacts/derived/e18_28_external_pass_20260905_v2').glob('*.json'))]


def test_real_slots_and_omitted_pass():
    farm = {'hands': [[1,1],[2,2]]}
    assert commands({'farmer':['NORTH'],'hands':[['WATER']]},farm) == [['NORTH'],['WATER'],['PASS']]
    assert len(commands({'hands':[['PASS']]*8},farm)) == 3
    assert MOVES == {'NORTH','SOUTH','EAST','WEST'}


def test_full_sample_and_shadow_parity():
    ps = profiles()
    assert len(ps) == 30
    assert len({p['source']['episode_id'] for p in ps}) == 30
    assert len({p['opponent'] for p in ps}) == 30
    assert Counter(p['result'] for p in ps) == {'LOSS':17,'WIN':13}
    for p in ps:
        assert p['shadow_parity_batches'] == 719 and not p['shadow_errors']
        assert p['daily'][-1]['pasture_topology'] == {'Q0':7,'Q1':7,'Q2':0,'Q3':0}


def test_actions_reasons_windows_reconcile():
    for p in profiles():
        assert sum(p['totals'].values()) == sum(p['capacity_daily'])
        assert p['totals']['MOVE'] > 2000
        assert p['totals']['PASS'] == len(p['pass_events'])
        assert sum(p['pass_summary']['reasons'].values()) == p['totals']['PASS']
        for day in range(1,31):
            rows = [e for e in p['pass_events'] if e['day']==day]
            assert len(rows) == p['action_daily'][day-1].get('PASS',0)
            assert p['pass_daily'][day-1] == pass_summary(rows)
        assert sum(d.get('PASS',0) for d in p['action_daily'][14:]) == p['pass_windows']['D15_D30']['total']
        assert not any(e['reason'].startswith('BLOCKED') for e in p['pass_events'] if e['day']>=15)


def test_audit_failure_is_not_zero_or_excluded_episode():
    ps=profiles()
    failed=[p for p in ps if p['ledger_error']]
    assert [p['source']['episode_id'] for p in failed] == [105852748]
    assert failed[0]['ledger'] is None and failed[0]['opponent_ledger'] is None
    for p in ps:
        if p['result']=='LOSS':
            assert p['ledger']['cash_parity_errors']==0
            assert p['ledger']['cash_parity_steps_both_players']==719


def test_idle_proxy_is_deduplicated_and_unfinished_excludes_padding():
    for p in profiles():
        for op,n in p['pass_summary']['unique_tile_days_by_op'].items():
            assert n<=p['pass_summary']['local_opportunity_slots'][op]
        assert all(r['opcode']!='PASS' for e in p['productive_unfinished'] for r in e['rows'])


def test_loss_diagnosis_aggregate_and_safety():
    report=json.loads((BASE/'artifacts/derived/E18_28_EXTERNAL_PASS_DIAGNOSIS_20260905_V2.json').read_text(encoding='utf-8'))
    losses=report['groups']['LOSS']
    assert losses['cash_verified_n']==17
    assert losses['crop_deaths']==32 and losses['crop_death_matches']==2
    assert losses['animal_losses']==0
    assert round(losses['windows']['D15_D30']['ours'],1)==746.3
    assert round(losses['windows']['D15_D30']['queue_finished'],1)==622.8
