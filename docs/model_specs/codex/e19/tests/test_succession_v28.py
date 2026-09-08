import json,runpy
from pathlib import Path
from docs.model_specs.codex.e19.tools.daily_route_scheduler_770_v28 import install
ROOT=Path(__file__).resolve().parents[5]

def test_observed_harvest_creates_replant_route_without_changing_opening():
    r=json.loads((ROOT/'docs/model_specs/codex/e19/artifacts/derived/daily_routes_v26_audit_20260908/replay.json').read_text())
    p=runpy.run_path(str(ROOT/'submission/submission_codex_e18_770_assisted_start_v1_candidate.py'))['create_agent']({'player_position':0});install(p.core)
    for i in range(1,529):
        obs=r['steps'][i-1][0]['observation'];action=p(obs,r['configuration'])
        if i<=264:assert action==r['steps'][i][0]['action']
    log=p.core.succession_log
    assert any(x['event']=='reserved' for x in log)
    assert any(x['event']=='observed_replant' for x in log)
    plans=[x for x in p.core.daily_route_log if x['day']==21]
    visits=[v for plan in plans for route in plan['routes'] for v in route['visits']]
    assert any(v['kind']=='NEW_CROP' and ['PLANT','WHEAT'] in v['commands'] for v in visits)
    for plan in plans:
        targets=[tuple(v['target']) for route in plan['routes'] for v in route['visits']]
        assert len(targets)==len(set(targets))
