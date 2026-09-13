"""Time-spread deterministic sample of one submission's public replay history."""
import json,hashlib,sys
from pathlib import Path
from collections import Counter,defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import requests
import e209_s56165462_charts as charts
ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/model_specs/codex/e22/reports/kiki_variability_extended_20260913'
RAW=ROOT/'data/replays/json/kiki_variability_extended_20260913'

def main():
    history=json.loads((OUT/'history.json').read_text(encoding='utf-8'))
    public=[e for e in history['episodes'] if e['state']=='COMPLETED' and e['type']=='EPISODE_TYPE_PUBLIC' and len({a['teamId'] for a in e['agents']})==2 and any(a['submissionId']==56137379 for a in e['agents'])]
    public.sort(key=lambda e:(e['createTime'],e['id']))
    old=json.loads((ROOT/'docs/model_specs/codex/e22/reports/kiki_rotation_20260913/ANALYSIS.json').read_text(encoding='utf-8'))['rows']
    oldpaths={r['episode']:ROOT/r['path'] for r in old}
    selected={public[round(i*(len(public)-1)/31)]['id'] for i in range(32)}|set(oldpaths)
    jobs=[e for e in public if e['id'] in selected]
    protocol=dict(frozen_utc=datetime.now(timezone.utc).isoformat(),submission=56137379,history_total=len(history['episodes']),eligible_public=len(public),selection='32 evenly spaced chronological indices spanning eligible history, union with the 8 previously analyzed episodes. No outcome or topology filtering; descriptive time-spread sample, not random or a census.',selected=len(jobs),episode_ids=[e['id'] for e in jobs])
    (OUT/'PROTOCOL.json').write_text(json.dumps(protocol,indent=2),encoding='utf-8');RAW.mkdir(exist_ok=True)
    def fetch(e):
        p=oldpaths.get(e['id'],RAW/f"{e['id']}.json")
        if not p.exists():
            resp=requests.get(f"https://www.kaggle.com/competitions/episodes/{e['id']}/replay.json",timeout=45);resp.raise_for_status();r=resp.json();assert r['info']['EpisodeId']==e['id'];p.write_bytes(resp.content)
        return e['id'],p
    with ThreadPoolExecutor(max_workers=3) as pool:paths=dict(pool.map(fetch,jobs))
    rows=[]
    for e in jobs:
        p=paths[e['id']];raw=p.read_bytes();r=json.loads(raw);assert len(r['steps'])==720 and all(s['status']=='DONE' for s in r['steps'][-1])
        seat=next(a.get('index',0) for a in e['agents'] if a['submissionId']==56137379)
        def count(f):return dict(Counter(t.get('animal') or t.get('crop') for row in f['tiles'] for t in row if isinstance(t,dict) and (t.get('animal') or t.get('crop'))))
        daily=[];placements=[];removals=[];crop_events=[];seen={};buys=[]
        for i in range(719):
            b=r['steps'][i][seat]['observation'];a=r['steps'][i+1][seat]['observation'];action=r['steps'][i+1][seat]['action']
            for order in action.get('market',[]):
                if order and order[0]=='BUY_ANIMAL':buys.append(dict(day=b['day']+1,hour=b['hour']+1,order=order,shops=dict(Counter(b['town']['unlocked_shops'])),prices=b['market']['prices']))
            for y,row in enumerate(b['farms'][seat]['tiles']):
                for x,oldtile in enumerate(row):
                    t=oldtile if isinstance(oldtile,dict) else {};nt=a['farms'][seat]['tiles'][y][x];n=nt if isinstance(nt,dict) else {}
                    if t.get('animal') and t.get('animal')!=n.get('animal'):removals.append(dict(day=b['day']+1,cell=[x,y],animal=t['animal']))
                    if n.get('animal') and (n.get('animal'),n.get('placed_day'))!=(t.get('animal'),t.get('placed_day')):
                        placements.append(dict(day=b['day']+1,cell=[x,y],animal=n['animal'],previous=seen.get((x,y))));seen[(x,y)]=n['animal']
                    if n.get('crop') and (n.get('crop'),n.get('planted_day'))!=(t.get('crop'),t.get('planted_day')):crop_events.append(dict(day=b['day']+1,cell=[x,y],crop=n['crop']))
        for day in range(1,31):
            o=r['steps'][day*24-1][seat]['observation'];f=o['farms'][seat]
            structures=[[x,y,t['kind']] for y,row in enumerate(f['tiles']) for x,t in enumerate(row) if isinstance(t,dict) and t.get('kind') in ['PASTURE','COOP']]
            daily.append(dict(day=day,counts=count(f),structures=structures,prices=o['market']['prices'],cash=f['money']))
        animals={k:v for k,v in daily[19]['counts'].items() if k in ['COW','SHEEP','GOOSE']}
        row=dict(episode=e['id'],created=e['createTime'],seat=seat,path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(raw).hexdigest(),previous_sample=e['id'] in oldpaths,daily=daily,d20_animals=animals,purchases=buys,placements=placements,removals=removals,replacements=[a for a in placements if a['previous'] and a['previous']!=a['animal']],crop_events=crop_events,rewards=r['rewards'])
        rows.append(row);print('ANALYZED',e['id'],animals,'removals',len(removals),flush=True)
    result=dict(protocol=protocol,rows=rows)
    (OUT/'ANALYSIS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print('DONE',len(rows),flush=True)
if __name__=='__main__':main()
