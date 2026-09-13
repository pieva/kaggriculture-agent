"""Freeze a shop-presence hypothesis, then inspect nine previously unused replays."""
import hashlib,json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/model_specs/codex/e22/reports/top_trigger_pilot_20260913'
RAW=ROOT/'data/replays/json/e22_trigger_holdout_20260913'
RULES=[('Olympus',56184881,8,2),('kiki yi2',56137379,8,2),('Majkel1337',56156662,7,7)]


def main():
    source=json.loads((OUT/'COHORT.json').read_text(encoding='utf-8'));seen={g['episode'] for g in source['games']};jobs=[]
    for name,sid,day,hour in RULES:
        h=json.loads((OUT/f'history_{sid}.json').read_text(encoding='utf-8'))
        es=sorted([e for e in h['episodes'] if e['state']=='COMPLETED' and e['type']=='EPISODE_TYPE_PUBLIC' and len({a['teamId'] for a in e['agents']})==2 and e['id'] not in seen],key=lambda e:(e['createTime'],e['id']),reverse=True)[:3]
        assert len(es)==3
        for e in es:jobs.append(dict(name=name,submission=sid,day=day,hour=hour,episode=e['id'],seat=next(a.get('index',0) for a in e['agents'] if a['submissionId']==sid)))
    protocol=OUT/'YARN_HYPOTHESIS.json'
    if not protocol.exists():protocol.write_text(json.dumps(dict(frozen_utc=datetime.now(timezone.utc).isoformat(),rule='At D8 H2 for Olympus/kiki yi2 and D7 H7 for Majkel1337, the requested animal purchase contains SHEEP iff YARN_STORE is already unlocked in the previous observation. Evaluate requests, not successful purchases. No threshold fitting. Nine most recent earlier unused public competitive replays, three per exact submission.',limitation='Exploratory replication after hypothesis discovery; shops and prices are correlated. Does not identify internal causal code.',jobs=jobs),indent=2)+'\n',encoding='utf-8')
    RAW.mkdir(parents=True,exist_ok=True)
    def get(j):
        p=RAW/f"{j['episode']}.json"
        if not p.exists():
            response=requests.get(f"https://www.kaggle.com/competitions/episodes/{j['episode']}/replay.json",timeout=45);response.raise_for_status();r=response.json();assert r['info']['EpisodeId']==j['episode'];p.write_bytes(response.content)
        raw=p.read_bytes();r=json.loads(raw);assert len(r['steps'])==720
        i=(j['day']-1)*24+j['hour']-1;o=r['steps'][i][j['seat']]['observation'];a=r['steps'][i+1][j['seat']]['action']
        orders=[a for a in a.get('market',[]) if a and a[0]=='BUY_ANIMAL'];yarn='YARN_STORE' in o['town']['unlocked_shops'];sheep=any(a[1]=='SHEEP' and a[2]>0 for a in orders)
        result=dict(**j,path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(raw).hexdigest(),
                    requested=orders,yarn=yarn,sheep=sheep,match=yarn==sheep,shops=o['town']['unlocked_shops'],
                    prices=o['market']['prices'],cash=o['farms'][j['seat']]['money'])
        print(j['name'],j['episode'],orders,'yarn',yarn,'match',result['match'],flush=True)
        return result
    with ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(get,jobs))
    (OUT/'YARN_REPLICATION.json').write_text(json.dumps(dict(rows=rows,matches=sum(r['match'] for r in rows),n=len(rows),positive_yarn=sum(r['yarn'] for r in rows)),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
