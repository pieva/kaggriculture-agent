"""Validate the frozen replay report, summaries and publication provenance."""
import hashlib
import json
import re
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[5]
O=ROOT/'docs/model_specs/codex/e19/reports/v48_external_pass_update_20260908'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
cohort=read(O/'cohort.json');summary=read(O/'summary.json');m=read(O/'manifest.json')
assert len(cohort['games'])==38 and len({r['episode'] for r in cohort['games']})==38
assert sum(r['cohort']=='new' for r in cohort['games'])==30
profiles=[]
for row in cohort['games']:
    assert hashlib.sha256((ROOT/row['raw_path']).read_bytes()).hexdigest()==row['sha256']
    p=read(O/f"profile_{row['episode']}.json");profiles.append(p)
    assert p['opponent_name']==row['opponent'] and p['cash']==row['cash'] and p['seat']==row['seat']
    for side in ['candidate','opponent']:
        assert len(p[side])==30
        for d in p[side]:
            assert sum(d['pass_hours'])==d['explicit_pass']==sum(d['worker_pass'].values())
            assert sum(d['slot_hours'])==d['slots']
            assert d['explicit_pass']+d['implicit_idle']<=d['slots']
            assert d['explicit_pass']+d.get('extra_requested_pass',0)==d['requested_actions'].get('PASS',0)
            assert 0<=d['pass_current_tile_service']<=d['explicit_pass']
for name,ps,side in [('first8',[p for p in profiles if p['cohort']=='first'],'candidate'),('new30',[p for p in profiles if p['cohort']=='new'],'candidate'),('all38',profiles,'candidate'),('opponents38',profiles,'opponent')]:
    rows=[d for p in ps for d in p[side]]
    assert abs(mean(d['explicit_pass'] for d in rows)-summary[name]['phases']['D1-D30']['explicit_pass'])<1e-9
    assert abs(sum(d['explicit_pass'] for d in rows)/sum(d['slots'] for d in rows)-summary[name]['phases']['D1-D30']['pass_share'])<1e-9
assert sum(p['cash']>p['opponent_cash'] for p in profiles)==23
assert all(p['candidate'][1]['explicit_pass']==69 for p in profiles)
for name,h in m['outputs'].items():assert hashlib.sha256((O/name).read_bytes()).hexdigest()==h,name
for name,h in m['sources'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,name
s=(O/'REPORT_V48_REPLAY_PASS_IT.html').read_text(encoding='utf-8')
assert s.count('<svg ')==8 and s.count('<circle ')==720
assert '\ufffd' not in s and '972,5' in s and '35,71' in s
for url in re.findall(r'href="([^"]+)"',s):
    if not url.startswith('https:'):assert (O/url).exists(),url
print('Verified: 38 raw hashes, 76 daily profiles, action accounting, cohort totals, 8 SVG charts, report links and manifest.')
