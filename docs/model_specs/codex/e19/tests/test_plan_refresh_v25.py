"""Observed-event regression using the real assisted transition observations."""
import json,runpy
from collections import Counter
from pathlib import Path
from docs.model_specs.codex.e19.tools.daily_route_scheduler_770_v25 import install
ROOT=Path(__file__).resolve().parents[5]
def test_new_land_and_hires_refresh_intentions_and_owners_same_day():
    r=json.loads((ROOT/'docs/model_specs/codex/e19/artifacts/derived/daily_routes_v22_audit_20260907/replay.json').read_text())
    p=runpy.run_path(str(ROOT/'submission/submission_codex_e18_770_assisted_start_v1_candidate.py'))['create_agent']({'player_position':0})
    install(p.core)
    old_intentions=None
    for i in range(1,269):
        obs=r['steps'][i-1][0]['observation']
        action=p(obs,r['configuration'])
        if i<=264:assert action==r['steps'][i][0]['action']
        else:
            c=p.core
            intentions={tuple(x['position']):x['crop'] for x in c.biological_plan['crop_intentions']}
            if obs['hour']==0:
                assert len(intentions)==36
                old_intentions=intentions
            if obs['hour']>=2:
                assert len(intentions)==61
                assert all(intentions[k]==v for k,v in old_intentions.items())
            if len(c.positions)>1:
                owners={x['worker'] for x in c.biological_plan['areas']}
                assert len(owners)>1
                assert max(owners)<len(c.positions)
            before=dict(intentions)
            c._services()
            assert before=={tuple(x['position']):x['crop'] for x in c.biological_plan['crop_intentions']}
