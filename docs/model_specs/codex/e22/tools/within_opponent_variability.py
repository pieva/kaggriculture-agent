"""Three replays per exact submission in five observed strategy families."""
import hashlib
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/model_specs/codex/e22/reports/opponent_strategy_20260913'
RAW=ROOT/'data/replays/json/e22_variability_20260913'
NAMES=['Sam-wiz','s56165462','Denis Revenko','EnricRovira','Rheinmetall']


def signature(r,seat):
    commands=[];market=[];plant_commands=[];daily=[]
    for i,step in enumerate(r['steps'][1:],1):
        a=step[seat]['action'];cmds=[a.get('farmer'),*a.get('hands',[])]
        commands.append(cmds);market.append(a.get('market',[]))
        for w,c in enumerate(cmds):
            if c and c[0] in ('PLANT','DIG','BUILD_PASTURE','BUILD_COOP','PLACE'):
                before=r['steps'][i-1][seat]['observation']['farms'][seat]
                pos=([before['farmer']]+before['hands'])
                plant_commands.append([i,w,pos[w] if w<len(pos) else None,c])
    for d in range(1,31):
        f=r['steps'][d*24-1][seat]['observation']['farms'][seat]
        tiles=[(x,y,t) for y,row in enumerate(f['tiles']) for x,t in enumerate(row) if isinstance(t,dict)]
        topology=[[x,y,t['kind']] for x,y,t in tiles if t['kind'] in ('PASTURE','COOP')]
        crops=[[x,y,t['crop'],t['planted_day']] for x,y,t in tiles if t.get('crop')]
        animals=[[x,y,t['animal']] for x,y,t in tiles if t.get('animal')]
        daily.append(dict(day=d,topology=topology,crops=crops,animals=animals,people=1+len(f['hands']),
                          land=f['unlocked_quadrants'],prices=r['steps'][d*24-1][seat]['observation']['market']['prices']))
    return dict(commands=commands,market=market,plant_commands=plant_commands,daily=daily)


def main():
    RAW.mkdir(parents=True,exist_ok=True)
    cohort=json.loads((OUT/'COHORT.json').read_text(encoding='utf-8'))
    anchors=[next(g for g in cohort['games'] if g['outcome']=='loss' and g['name']==name) for name in NAMES]
    jobs=[]
    for anchor in anchors:
        sid=anchor['opponent_submission'];p=OUT/f'history_opponent_{sid}.json'
        if not p.exists():
            response=requests.post('https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes',json={'submissionId':sid},timeout=30)
            response.raise_for_status();p.write_text(json.dumps(response.json(),indent=2),encoding='utf-8')
        hist=json.loads(p.read_text());episodes=hist['episodes']
        focal=next(e for e in episodes if e['id']==anchor['episode'])
        earlier=sorted([e for e in episodes if e['state']=='COMPLETED' and e['type']=='EPISODE_TYPE_PUBLIC'
                        and e['createTime']<focal['createTime'] and len({a['teamId'] for a in e['agents']})==2],
                       key=lambda e:(e['createTime'],e['id']),reverse=True)[:2]
        assert len(earlier)==2,(anchor['name'],len(earlier))
        for e in [focal,*earlier]:
            agent=next(a for a in e['agents'] if a['submissionId']==sid)
            path=ROOT/anchor['path'] if e['id']==anchor['episode'] else RAW/f"{e['id']}.json"
            jobs.append(dict(name=anchor['name'],submission=sid,episode=e['id'],seat=agent.get('index',0),path=str(path),
                             focal=e['id']==anchor['episode'],metadata=e))
    def fetch(j):
        p=Path(j['path'])
        if not p.exists():
            response=requests.get(f"https://www.kaggle.com/competitions/episodes/{j['episode']}/replay.json",timeout=45)
            response.raise_for_status();r=response.json();assert r['info']['EpisodeId']==j['episode'];p.write_bytes(response.content)
        return j
    with ThreadPoolExecutor(max_workers=3) as pool:jobs=list(pool.map(fetch,jobs))
    results=[]
    for anchor in anchors:
        members=[j for j in jobs if j['name']==anchor['name']];profiles=[]
        for j in members:
            raw=Path(j['path']).read_bytes();r=json.loads(raw)
            assert len(r['steps'])==720 and all(x['status']=='DONE' for x in r['steps'][-1])
            profiles.append(signature(r,j['seat']))
            j.update(sha256=hashlib.sha256(raw).hexdigest(),teams=r['info']['TeamNames'],rewards=r['rewards'],seed=r['info']['seed'])
        pairs=[]
        for i in range(3):
            for k in range(i+1,3):
                a,b=profiles[i],profiles[k]
                pairs.append(dict(episodes=[members[i]['episode'],members[k]['episode']],
                                  identical_worker_frames=sum(x==y for x,y in zip(a['commands'],b['commands'])),
                                  identical_market_frames=sum(x==y for x,y in zip(a['market'],b['market'])),
                                  identical_topology_days=sum(x['topology']==y['topology'] for x,y in zip(a['daily'],b['daily'])),
                                  identical_crop_days=sum(x['crops']==y['crops'] for x,y in zip(a['daily'],b['daily'])),
                                  identical_animal_days=sum(x['animals']==y['animals'] for x,y in zip(a['daily'],b['daily'])),
                                  identical_people_days=sum(x['people']==y['people'] for x,y in zip(a['daily'],b['daily'])),
                                  same_plant_build_commands=a['plant_commands']==b['plant_commands']))
        result=dict(name=anchor['name'],submission=anchor['opponent_submission'],members=members,pairs=pairs,
                    d20=[p['daily'][19] for p in profiles],daily=[p['daily'] for p in profiles])
        results.append(result)
        print(anchor['name'],json.dumps(pairs),flush=True)
    (OUT/'VARIABILITY.json').write_text(json.dumps(dict(protocol='Exploratory five representatives of observed geometry/portfolio families. Exact same submission: focal loss plus two immediately preceding completed public non-self-play games. No outcome filtering on additional games. Three replays do not identify the internal policy.',groups=results),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
