"""Observe decisions and preceding public/private state; never infer future inputs."""
import hashlib,json,sys
from collections import Counter,defaultdict
from itertools import combinations
from pathlib import Path
from statistics import mean

ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
OUT=ROOT/'docs/model_specs/codex/e22/reports/top_trigger_pilot_20260913'
ANIMALS=['COW','SHEEP','GOOSE'];CROPS=['MELON','STRAWBERRY','TOMATO','WHEAT','CARROT']
PRODUCT={'COW':'MILK','SHEEP':'WOOL','GOOSE':'EGG',**{x:x for x in CROPS}}


def counts(farm):
    return dict(Counter(t.get('animal') or t.get('crop') for row in farm['tiles'] for t in row if isinstance(t,dict) and (t.get('animal') or t.get('crop'))))


def features(r,i,seat):
    o=r['steps'][i][seat]['observation'];f=o['farms'][seat];prices=o['market']['prices']
    a=counts(f);b=counts(o['farms'][1-seat]);shops=Counter(o['town']['unlocked_shops'])
    old=r['steps'][max(0,i-72)][seat]['observation']['market']['prices']
    return dict(day=o['day']+1,hour=o['hour']+1,cash=f['money'],people=1+len(f['hands']),
                prices=prices,price_change_3days={p:prices[p]-old[p] for p in prices},
                own=a,opponent=b,shops=dict(shops),shed=o['private']['shed'],seeds=o['private']['seeds'],
                land=f['unlocked_quadrants'])


def extract(g):
    raw=(ROOT/g['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==g['sha256'];r=json.loads(raw);seat=g['seat']
    events=[];commands=[];occ=Counter();daily=[];market_commands=[]
    for i in range(719):
        before=r['steps'][i][seat]['observation'];after=r['steps'][i+1][seat]['observation'];a=r['steps'][i+1][seat]['action']
        commands.append([a.get('farmer'),a.get('hands',[])])
        market_commands.append(a.get('market',[]))
        ps=[before['farms'][seat]['farmer']]+before['farms'][seat]['hands']
        fs=None
        for w,c in enumerate([a.get('farmer'),*a.get('hands',[])]):
            if not c or w>=len(ps):continue
            kind=c[0]
            if kind not in ['PLANT','PLACE','BUILD_PASTURE','BUILD_COOP']:continue
            if kind=='PLACE' and (len(c)<2 or c[1] not in ANIMALS):continue
            x,y=ps[w];old=before['farms'][seat]['tiles'][y][x];new=after['farms'][seat]['tiles'][y][x]
            choice=c[1] if kind in ['PLANT','PLACE'] else kind[6:]
            success=isinstance(new,dict) and ((kind=='PLANT' and new.get('crop')==choice and new.get('planted_day')==before['day'] and (not isinstance(old,dict) or old.get('crop')!=choice or old.get('planted_day')!=new.get('planted_day'))) or
                (kind=='PLACE' and new.get('animal')==choice and (not isinstance(old,dict) or old.get('animal')!=choice)) or
                (kind.startswith('BUILD') and new.get('kind')==choice and (not isinstance(old,dict) or old.get('kind')!=choice)))
            if not success:continue
            family='ANIMAL' if kind=='PLACE' else 'CROP' if kind=='PLANT' else 'STRUCTURE'
            key=f'{family}:{x},{y}';occ[key]+=1
            if fs is None:fs=features(r,i,seat)
            events.append(dict(step=i,kind=family,cell=[x,y],ordinal=occ[key],choice=choice,features=fs,worker=w))
        for kind in ['BUY_ANIMAL','BUY_SEED','BUY_LAND','HIRE']:
            orders=[c for c in a.get('market',[]) if c and c[0]==kind]
            if not orders:continue
            if fs is None:fs=features(r,i,seat)
            events.append(dict(step=i,kind=kind,choice=orders,features=fs))
    for day in range(1,31):
        o=r['steps'][24*day-1][seat]['observation'];f=o['farms'][seat]
        tiles=[[x,y,t.get('kind'),t.get('animal'),t.get('crop')] for y,row in enumerate(f['tiles']) for x,t in enumerate(row) if isinstance(t,dict)]
        daily.append(dict(day=day,money=f['money'],people=1+len(f['hands']),counts=counts(f),
                          structure=[[x,y,k] for x,y,k,a,c in tiles if k in ('PASTURE','COOP')],
                          crops=[[x,y,c] for x,y,k,a,c in tiles if c],animals=[[x,y,a] for x,y,k,a,c in tiles if a]))
    return dict(**g,extraction_version=2,events=events,commands=commands,market_commands=market_commands,daily=daily)


def main():
    cohort=json.loads((OUT/'COHORT.json').read_text(encoding='utf-8'));dest=OUT/'profiles';dest.mkdir(exist_ok=True)
    profiles=[]
    for g in cohort['games']:
        path=dest/f"{g['submission']}_{g['episode']}.json"
        p=json.loads(path.read_text(encoding='utf-8')) if path.exists() else None
        if not p or p.get('extraction_version')!=2:
            p=extract(g);path.write_text(json.dumps(p,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
        profiles.append(p);print('EXTRACTED',g['name'],g['episode'],len(p['events']),flush=True)
    models=[]
    for sid in dict.fromkeys(p['submission'] for p in profiles):
        ps=[p for p in profiles if p['submission']==sid];pairs=[];slots=defaultdict(list)
        for a,b in combinations(ps,2):
            pairs.append(dict(episodes=[a['episode'],b['episode']],worker_share=sum(x==y for x,y in zip(a['commands'],b['commands']))/719,
                              structure_days=sum(x['structure']==y['structure'] for x,y in zip(a['daily'],b['daily'])),
                              crop_days=sum(x['crops']==y['crops'] for x,y in zip(a['daily'],b['daily']))))
        for p in ps:
            for e in p['events']:
                if e['kind'] in ('ANIMAL','CROP','STRUCTURE'):
                    slots[(e['kind'],tuple(e['cell']),e['ordinal'])].append(dict(episode=p['episode'],**e))
        branches=[]
        for key,es in slots.items():
            if len(es)>=3 and len({e['choice'] for e in es})>1:
                branches.append(dict(kind=key[0],cell=key[1],ordinal=key[2],n=len(es),
                                     day_range=[min(e['features']['day'] for e in es),max(e['features']['day'] for e in es)],events=es))
        models.append(dict(name=ps[0]['name'],submission=sid,band=ps[0]['band'],rating=ps[0]['display_score'],
                           episodes=[p['episode'] for p in ps],mean_worker_share=mean(p['worker_share'] for p in pairs),
                           min_worker_share=min(p['worker_share'] for p in pairs),max_worker_share=max(p['worker_share'] for p in pairs),
                           mean_structure_days=mean(p['structure_days'] for p in pairs),mean_crop_days=mean(p['crop_days'] for p in pairs),
                           d20=[p['daily'][19] for p in ps],pairs=pairs,branches=branches,
                           n_animal_branches=sum(b['kind']=='ANIMAL' for b in branches),n_crop_branches=sum(b['kind']=='CROP' for b in branches),
                           n_structure_branches=sum(b['kind']=='STRUCTURE' for b in branches)))
    (OUT/'ANALYSIS.json').write_text(json.dumps(dict(models=models,caveat='Successful tile transitions align by cell and occurrence, not by internal decision opportunity. Pre-action features only. Variability may reflect failure or previous commitments; not causal attribution.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for m in models:print(json.dumps({k:v for k,v in m.items() if k not in ['branches','pairs','d20','episodes']},ensure_ascii=True),flush=True)


if __name__=='__main__':main()
