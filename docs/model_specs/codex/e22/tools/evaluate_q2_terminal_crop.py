"""Paired D28-D30 counterfactuals using actual engine and frozen opponent actions."""
import contextlib
import copy
import hashlib
import io
import json
import statistics
from collections import Counter
from pathlib import Path
from types import SimpleNamespace as NS

ROOT = Path(__file__).resolve().parents[5]
OUT = ROOT/'docs/model_specs/codex/e22/reports/e22_1_q2_coop_20260914'
SOURCE = OUT.parent/'external_e22_2_20260914'


def run(game, seat, crop=None):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        import kaggle_environments.envs.kaggriculture.kaggriculture as e
    initial = copy.deepcopy(game['steps'][648])
    states = [NS(observation=NS(**s['observation']), action={}, status='ACTIVE', reward=0) for s in initial]
    env = NS(configuration=NS(**game['configuration']), info=game['info'], done=False)
    states[1].observation.farms = states[0].observation.farms
    states[1].observation.market = states[0].observation.market
    states[1].observation.town = states[0].observation.town
    changes=[]; harvests=[]; neighborhood=[]; all_harvests=Counter()
    for i in range(648,719):
        d,h=i//24+1,i%24+1
        for j in range(2):
            states[j].observation.step=i
            states[j].action=copy.deepcopy(game['steps'][i+1][j]['action'])
        a=states[seat].action
        if crop:
            if d==28 and h==7:
                assert len(a['market'])<10
                a['market'].append(['BUY_SEED',crop,1])
            if d==28 and h>=8:
                original=[game['steps'][648+k][seat]['action']['hands'][9] for k in range(8,25) if k not in (10,15)]
                a['hands'][9]=([['PLANT',crop],['WATER']]+original)[h-8]
            if d==29 and h==5: a['hands'][5]=['WATER']
            if d==30 and h>=3:
                commands=[]
                for k in range(3,24):
                    if k in (5,11,22,23):continue
                    commands.append(game['steps'][696+k][seat]['action']['hands'][9])
                    if k==8:commands.extend([['WEST'],['WATER'],['HARVEST'],['EAST']])
                a['hands'][9]=commands[h-3]
        if a!=game['steps'][i+1][seat]['action']:changes.append(dict(day=d,hour=h,action=a))
        farm=states[seat].observation.farms[seat]
        prior=copy.deepcopy(states[seat].observation.private)
        locations=copy.deepcopy([farm['farmer']]+farm['hands'])
        actions=[a['farmer']]+a['hands']
        if h==1:
            neighborhood.append(dict(day=d,tiles={f'{x},{y}':copy.deepcopy(farm['tiles'][y][x]) for x,y in [(3,7),(3,6),(2,7),(4,7),(3,8),(2,6),(2,8)]}))
        e.interpreter(states,env)
        for w,(pos,cmd) in enumerate(zip(locations,actions)):
            if cmd==['HARVEST'] and i%24!=23:
                before=prior['inventories'][w];after=states[seat].observation.private['inventories'][w]
                gain={k:v-before.get(k,0) for k,v in after.items() if v>before.get(k,0)}
                all_harvests.update(gain)
                if pos==[3,7]:harvests.append(dict(day=d,hour=h,worker=w,gain=gain))
        if crop is None:
            expected=game['steps'][i+1]
            for j in range(2):
                assert states[j].observation.farms==expected[j]['observation']['farms'],('farms',i,j)
                assert states[j].observation.private==expected[j]['observation']['private'],('private',i,j)
                assert states[j].observation.market==expected[j]['observation']['market'],('market',i,j)
    return dict(crop=crop or 'baseline',cash=states[seat].observation.farms[seat]['money'],
                opponent_cash=states[seat].observation.farms[1-seat]['money'],
                final_private=states[seat].observation.private,harvests=harvests,changes=changes,neighborhood=neighborhood,
                harvest_totals_excluding_h24=dict(all_harvests),
                target_terminal=states[seat].observation.farms[seat]['tiles'][7][3])


def main():
    cohort=[g for g in json.loads((SOURCE/'COHORT.json').read_text()) if g['submission']==56206528]
    results=[]
    for g in cohort:
        raw=(ROOT/g['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==g['sha256']
        game=json.loads(raw)
        arms=[run(game,g['seat'],c) for c in (None,'WHEAT','CARROT')]
        for a in arms:
            a['cash_delta']=a['cash']-arms[0]['cash']
            if a['crop']!='baseline':
                expected=Counter(arms[0]['harvest_totals_excluding_h24']);expected[a['crop']]+=2
                assert Counter(a['harvest_totals_excluding_h24'])==expected
                assert a['final_private']==arms[0]['final_private']
        results.append(dict(episode=g['episode'],seat=g['seat'],replay_sha256=g['sha256'],arms=arms))
        print(g['episode'],[(a['crop'],a['cash_delta'],a['harvests'][-1]) for a in arms],flush=True)
    (OUT/'CROP_COUNTERFACTUALS.json').write_text(json.dumps(results,indent=2))
    summary={c:dict(n=len(results),mean=statistics.mean(r['arms'][idx]['cash_delta'] for r in results),
        min=min(r['arms'][idx]['cash_delta'] for r in results),max=max(r['arms'][idx]['cash_delta'] for r in results),
        positive=sum(r['arms'][idx]['cash_delta']>0 for r in results)) for idx,c in [(1,'WHEAT'),(2,'CARROT')]}
    (OUT/'CROP_SUMMARY.json').write_text(json.dumps(summary,indent=2))
    print(summary,flush=True)


if __name__=='__main__':main()
