"""Frozen 38-game external update: explicit PASS, available slots and verified services."""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from statistics import mean
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d20_trajectories import snapshot

B=ROOT/'docs/model_specs/codex/e19'
OUT=B/'reports/v48_external_pass_update_20260908'
OUT.mkdir(exist_ok=True)
NEW=[106869264,106868764,106862857,106861918,106860962,106860010,106859058,106858137,106857232,106857153,106856182,106855230,106854284,106853559,106852347,106851424,106850363,106849499,106848550,106847646,106846593,106845542,106844755,106843637,106842664,106841692,106840717,106839772,106838819,106837859]
first=json.loads((B/'artifacts/derived/v48_external_20260908/first_cohort.json').read_text(encoding='utf-8'))
OLD=[g['episode'] for g in first['games']]

def dump(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

def slots(replay,seat):
    days=[dict(day=d,slots=0,explicit_pass=0,implicit_idle=0,move=0,
       pass_hours=[0]*24,slot_hours=[0]*24,worker_pass={},pass_critical_water=0,
       pass_unfed_animals=0,pass_current_tile_service=0) for d in range(1,31)]
    for i in range(1,len(replay['steps'])):
        o=replay['steps'][i-1][seat]['observation'];day=o['day'];hour=o['hour']
        farm=o['farms'][seat];priv=o['private'];a=replay['steps'][i][seat].get('action') or {}
        positions=[farm['farmer'],*farm['hands']]
        commands=[a.get('farmer',['PASS']),*a.get('hands',[])]
        tiles=[t for row in farm['tiles'] for t in row if isinstance(t,dict)]
        critical=any(t.get('kind')=='PLANT' and not t.get('watered_today') and t.get('consecutive_unwatered',0)>=1 for t in tiles)
        unfed=any(t.get('animal') and not t.get('fed_today') for t in tiles)
        active_positions={tuple(positions[w]) for w,c in enumerate(commands[:len(positions)]) if isinstance(c,list) and c and c[0]!='PASS'}
        z=days[day]
        for w,pos in enumerate(positions):
            z['slots']+=1;z['slot_hours'][hour]+=1
            c=commands[w] if w<len(commands) else None
            if not isinstance(c,list) or not c:
                z['implicit_idle']+=1;continue
            op=c[0]
            if op in {'NORTH','SOUTH','EAST','WEST'}:z['move']+=1
            if op!='PASS':continue
            z['explicit_pass']+=1;z['pass_hours'][hour]+=1
            z['worker_pass'][str(w)]=z['worker_pass'].get(str(w),0)+1
            z['pass_critical_water']+=critical;z['pass_unfed_animals']+=unfed
            x,y=pos;t=farm['tiles'][y][x];inv=priv['inventories'][w]
            local=isinstance(t,dict) and (t.get('kind')=='PLANT' and not t.get('watered_today') or t.get('animal') and (not t.get('cared_today') or not t.get('fed_today') and inv.get('WHEAT',0)>0))
            z['pass_current_tile_service']+=bool(local and tuple(pos) not in active_positions)
    return days

profiles=[];catalog=[]
for ep in sorted(OLD+NEW):
    path=(ROOT/'data/replays/json/v48_update_20260908'/f'{ep}.json') if ep in NEW else B/'artifacts/derived/v48_external_20260908'/f'{ep}.json'
    raw=path.read_bytes();r=json.loads(raw)
    assert r['info']['EpisodeId']==ep and r['statuses']==['DONE','DONE'] and len(r['steps'])==720
    seat=r['info']['TeamNames'].index('Pietro Valocchi')
    entry=dict(episode=ep,seat=seat,opponent=r['info']['TeamNames'][1-seat],cohort='new' if ep in NEW else 'first',cash=r['rewards'][seat],opponent_cash=r['rewards'][1-seat],raw_path=str(path.relative_to(ROOT)).replace('\\','/'),sha256=hashlib.sha256(raw).hexdigest())
    catalog.append(entry)
    cache=OUT/f'profile_{ep}.json'
    if cache.exists():
        p=json.loads(cache.read_text(encoding='utf-8'));assert p['sha256']==entry['sha256']
    else:
        p=dict(entry)
        for side,s in [('candidate',seat),('opponent',1-seat)]:
            ledger=audit(r,s)
            assert ledger['cash_parity_errors']==0
            ds=slots(r,s)
            for d,z in enumerate(ds):
                l=ledger['daily'][d];snap=snapshot(r,d+1,s)
                z['requested_actions']=l['requested_actions'];z['executed_actions']=l['executed_actions']
                z['crop_tiles']=snap['crop_tiles'];z['people_h24']=snap['people']
                z['cash_h24']=r['steps'][24*(d+1)-1][s]['observation']['farms'][s]['money'];z['hire_cash']=l['hire_cash']
                z['animals']=snap['occupied_livestock_tiles']
                z['extra_requested_pass']=l['requested_actions'].get('PASS',0)-z['explicit_pass']
                assert z['extra_requested_pass']>=0,(ep,s,d,z['explicit_pass'],l['requested_actions'])
            p[side]=ds
        dump(cache,p)
    p['opponent_name']=entry['opponent']
    dump(cache,p)
    profiles.append(p);print(ep,'audited',flush=True)

def aggregate(ps,side):
    daily=[]
    for d in range(30):
        rows=[p[side][d] for p in ps]
        z={k:mean(r[k] for r in rows) for k in ['explicit_pass','slots','implicit_idle','move','crop_tiles','people_h24','animals','hire_cash','pass_critical_water','pass_unfed_animals','pass_current_tile_service']}
        z['day']=d+1;z['pass_share']=sum(r['explicit_pass'] for r in rows)/sum(r['slots'] for r in rows)
        for op in ['WATER','FEED','CARE','HARVEST','PLANT']:
            z[op]=mean(r['executed_actions'].get(op,0) for r in rows)
        z['pass_min']=min(r['explicit_pass'] for r in rows);z['pass_max']=max(r['explicit_pass'] for r in rows)
        z['pass_hours']=[mean(r['pass_hours'][h] for r in rows) for h in range(24)]
        daily.append(z)
    phases={}
    for a,b in [(1,11),(12,15),(16,25),(26,30),(1,30)]:
        rows=[r for p in ps for r in p[side][a-1:b]]
        phases[f'D{a}-D{b}']={k:mean(r[k] for r in rows) for k in ['explicit_pass','slots','move','crop_tiles','people_h24','pass_current_tile_service','pass_critical_water','pass_unfed_animals']}
        phases[f'D{a}-D{b}']['pass_share']=sum(r['explicit_pass'] for r in rows)/sum(r['slots'] for r in rows)
    return dict(n=len(ps),daily=daily,phases=phases)

summary={}
for name,ps,side in [('first8',[p for p in profiles if p['cohort']=='first'],'candidate'),('new30',[p for p in profiles if p['cohort']=='new'],'candidate'),('all38',profiles,'candidate'),('opponents38',profiles,'opponent'),('wins',[p for p in profiles if p['cash']>p['opponent_cash']],'candidate'),('losses',[p for p in profiles if p['cash']<p['opponent_cash']],'candidate')]:
    summary[name]=aggregate(ps,side)
    own='cash' if side=='candidate' else 'opponent_cash'
    other='opponent_cash' if side=='candidate' else 'cash'
    summary[name].update(wins=sum(p[own]>p[other] for p in ps),losses=sum(p[own]<p[other] for p in ps),cash_mean=mean(p[own] for p in ps),opponent_cash_mean=mean(p[other] for p in ps))
dump(OUT/'summary.json',summary)
dump(OUT/'cohort.json',dict(submission_id=56101593,rating_observed=972.5,previous_rating_observed=822.1,observation_note='Rating read from submission UI at start of acquisition; not refreshed during analysis.',selection='All 38 completed non-self games visible at start, latest episode 106869264. 30 new plus original 8. One self-play excluded. No outcome filtering.',compiled_utc=datetime.now(timezone.utc).isoformat(),games=catalog))
print(json.dumps({k:{q:v[q] for q in ['n','wins','losses','cash_mean']} for k,v in summary.items()},indent=2))
