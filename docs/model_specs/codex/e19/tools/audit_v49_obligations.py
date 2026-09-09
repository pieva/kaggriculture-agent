"""Post-action obligations and lost stock, measured with the pinned engine."""
from collections import Counter
from copy import deepcopy
import importlib


def productive(tile,day,rules):
    r=rules[tile['crop']]
    last=tile['planted_day']+r['first_yield_day']+(r['max_yield']-1)*r['interval'] if r['ongoing'] else tile['planted_day']+r['max_yield_day']
    return bool(tile.get('yield_units',0)>0 or last>day)


def audit_obligations(replay,seat):
    engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    from docs.model_specs.codex.e19.tools.portfolio_workforce_v16 import care_value
    cfg=replay['configuration'];turns=cfg.get('turnsPerDay',24)
    final=(cfg.get('episodeSteps',720)-2)//turns
    days=[dict(day=d+1,missed_feed=0,missed_useful_care=0,missed_critical_water=0,
        decay_lost_units=0,productive_water_loss_units=0,obligations=[]) for d in range(final+1)]
    for i in range(1,len(replay['steps'])):
        obs=replay['steps'][i-1][seat]['observation'];day=obs['day']
        farm=deepcopy(obs['farms'][seat]);private=deepcopy(obs['private'])
        a=replay['steps'][i][seat]['action']
        cmds=[a['farmer'],*a['hands']]
        demand=Counter(c[1] for c in cmds if c and c[0]=='PLANT')
        blocked={c for c,n in demand.items() if n>private['seeds'].get(c,0)}
        for w,c in enumerate(cmds):
            if c[0]=='PLANT' and c[1] in blocked:c=['PASS']
            engine._apply_unit_action(farm,private,w,c,cfg.get('boardSize',10),day,turns,cfg.get('shedCapacity',100))
        before=deepcopy(farm['tiles'])
        engine._decay_plants(farm,day*turns+obs['hour'])
        row=days[day]
        for y,tiles in enumerate(before):
            for x,t in enumerate(tiles):
                if not isinstance(t,dict) or t.get('kind')!='PLANT':continue
                after=farm['tiles'][y][x]
                row['decay_lost_units']+=max(0,t.get('yield_units',0)-(after.get('yield_units',0) if isinstance(after,dict) else 0))
        if obs['hour']!=turns-1:continue
        for y,tiles in enumerate(farm['tiles']):
            for x,t in enumerate(tiles):
                if not isinstance(t,dict):continue
                missing=[]
                if t.get('animal'):
                    if not t.get('fed_today'):row['missed_feed']+=1;missing.append('FEED')
                    if care_value(t,day,final,engine.ANIMALS[t['animal']],lambda *args:1)>0:
                        row['missed_useful_care']+=1;missing.append('CARE')
                elif t.get('kind')=='PLANT' and productive(t,day,engine.CROPS):
                    if not t.get('watered_today') and t.get('consecutive_unwatered',0)>=1:
                        row['missed_critical_water']+=1
                        row['productive_water_loss_units']+=t.get('yield_units',0)
                        missing.append('WATER')
                if missing:row['obligations'].append(dict(position=[x,y],missing=missing))
    return days


def route_capacity(replay,seat,routes):
    result=[]
    for route in routes:
        day,hour=route['day'],route['hour']
        n=route['workers'];per_worker=[]
        for w in range(n):
            count=Counter()
            for i in range(1,len(replay['steps'])):
                obs=replay['steps'][i-1][seat]['observation']
                if obs['day']!=day-1 or obs['hour']<hour-1:continue
                a=replay['steps'][i][seat]['action'];cmds=[a['farmer'],*a['hands']]
                if w<len(cmds):count[cmds[w][0]]+=1
            planned=route['routes'][w]
            per_worker.append(dict(worker=w,planned_route=planned['cost'],
                committed=max(0,route['budget']-planned['available']),
                available=planned['available'],realized=dict(count)))
        result.append(dict(day=day,hour=hour,workers=n,unassigned=len(route['unassigned']),people=per_worker))
    return result
