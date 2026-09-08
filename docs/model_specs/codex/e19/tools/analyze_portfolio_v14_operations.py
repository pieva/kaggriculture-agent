"""Reconcile idle workers, failed harvests and weed origins on a frozen rerun."""
import importlib
import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
OUT=ROOT/'docs/model_specs/codex/e19/artifacts/derived/portfolio_v14_operations_audit_20260907'


def main():
    engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    replay=json.loads((OUT/'replay.json').read_text())
    audit=json.loads((OUT/'portfolio_v14_audit_180903001_0.json').read_text())
    original=json.loads((OUT.parent/'portfolio_succession_20260907/portfolio_v14_180903001_0.json').read_text())
    assert audit['sides']==original['sides'], 'Diagnostic rerun changed the result'
    trace={(t['day'],t['hour']):t for t in audit['trace'] if t.get('audit')}
    totals=Counter(); weeds=Counter(); failures=Counter(); examples=[]
    for i in range(1,len(replay['steps'])):
        before=replay['steps'][i-1][0]['observation']
        recorded=replay['steps'][i][0]
        day,hour=before['day']+1,before['hour']+1
        farm,private=deepcopy(before['farms'][0]),deepcopy(before['private'])
        action=recorded['action'] or {}
        commands=[action.get('farmer',['PASS']),*action.get('hands',[])]
        demand=Counter(c[1] for c in commands if c[0]=='PLANT')
        blocked={c for c,n in demand.items() if n>private['seeds'].get(c,0)}
        for worker,command in enumerate(commands):
            positions=[farm['farmer'],*farm['hands']]
            x,y=positions[worker]
            tile=farm['tiles'][y][x]
            if day>=16 and command[0]=='PASS':
                t=trace[(day,hour)]
                job=t['active'].get(str(worker))
                totals['PASS_active' if job else 'PASS_unassigned']+=1
                if not job and t['metric_delta'].get('portfolio_certificate_budget_exhausted'):
                    totals['PASS_unassigned_with_exhausted_search']+=1
                if not job and isinstance(tile,dict) and tile.get('animal') and not tile.get('cared_today'):
                    totals['PASS_unassigned_on_uncared_animal']+=1
                    if day<=27:
                        totals['PASS_unassigned_on_uncared_animal_D16_D27']+=1
            inv_before=sum(private['inventories'][worker].values())
            allowed=['PASS'] if command[0]=='PLANT' and command[1] in blocked else command
            engine._apply_unit_action(farm,private,worker,allowed,10,before['day'],24,100)
            if day>=16 and command[0]=='HARVEST' and sum(private['inventories'][worker].values())<=inv_before:
                reason='empty_tile' if tile is None else tile if isinstance(tile,str) else tile.get('kind','unknown')+':yield='+str(tile.get('yield_units',0))
                failures[reason]+=1
                if len(examples)<8:examples.append(dict(day=day,hour=hour,worker=worker,tile=tile))
        def weed_positions(f):return {(x,y) for y,row in enumerate(f['tiles']) for x,t in enumerate(row) if isinstance(t,dict) and t.get('kind')=='WEED'}
        pre=weed_positions(farm)
        crops={(x,y):t.get('crop') for y,row in enumerate(farm['tiles']) for x,t in enumerate(row) if isinstance(t,dict) and t.get('kind')=='PLANT'}
        engine._decay_plants(farm,i-1)
        post=weed_positions(farm)
        weeds['crop_decay']+=len(post-pre)
        for pos in post-pre:weeds['decay_'+str(crops.get(pos))]+=1
        if (i)%24==0:
            engine._daily_refresh_plants(farm,before['day'],24)
            refreshed=weed_positions(farm)
            weeds['missed_water']+=len(refreshed-post)
            weeds['spawn_on_empty']+=len(weed_positions(recorded['observation']['farms'][0])-refreshed)
    result=dict(case='180903001 seat0',exact_kpi_ledger_parity=True,period='D16-D30',pass_counts=dict(totals),failed_harvests=dict(failures),weed_origins_full_game=dict(weeds),examples=examples)
    (OUT/'operations_analysis.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
