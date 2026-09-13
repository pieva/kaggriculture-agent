"""Rating-stratified pilot, five consecutive games per exact submission."""
import hashlib,json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/model_specs/codex/e22/reports/top_trigger_pilot_20260913'
RAW=ROOT/'data/replays/json/e22_trigger_pilot_20260913'


def main():
    lb=json.loads((OUT/'leaderboard.json').read_text(encoding='utf-8'));rows=lb['publicLeaderboard']
    names={t['teamId']:t['teamName'] for t in lb['teams']}
    mid=[r for r in rows if 2000<=float(r['displayScore'])<=2500]
    selections=[dict(min(mid,key=lambda r:abs(float(r['displayScore'])-target)),band='2000-2500') for target in [2000,2250,2500]]
    selections += [dict(r,band='3000+') for r in rows if float(r['displayScore'])>=3000][:3]
    for s in selections:s['name']=names[s['teamId']]
    protocol=dict(frozen_utc=datetime.now(timezone.utc).isoformat(),selection='Three nearest displayed ratings to 2000/2250/2500 within that band and three highest ranked >=3000. Five latest completed public non-self-play episodes per exact selected submission; no outcome or topology filtering. Exploratory sample, not representative estimate.',selections=selections)
    (OUT/'PROTOCOL.json').write_text(json.dumps(protocol,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    RAW.mkdir(parents=True,exist_ok=True);jobs=[]
    for s in selections:
        sid=s['submissionId'];p=OUT/f'history_{sid}.json'
        if not p.exists():
            response=requests.post('https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes',json={'submissionId':sid},timeout=30);response.raise_for_status();p.write_text(json.dumps(response.json(),indent=2),encoding='utf-8')
        h=json.loads(p.read_text());games=sorted([e for e in h['episodes'] if e['state']=='COMPLETED' and e['type']=='EPISODE_TYPE_PUBLIC' and len({a['teamId'] for a in e['agents']})==2],key=lambda e:(e['createTime'],e['id']),reverse=True)[:5]
        assert len(games)==5,(sid,len(games))
        for e in games:
            a=next(a for a in e['agents'] if a['submissionId']==sid)
            jobs.append(dict(name=s['name'],submission=sid,band=s['band'],display_score=float(s['displayScore']),
                             episode=e['id'],seat=a.get('index',0),rating=a['initialScore'],metadata=e))
    unique={j['episode'] for j in jobs}
    def fetch(eid):
        p=RAW/f'{eid}.json'
        if not p.exists():
            response=requests.get(f'https://www.kaggle.com/competitions/episodes/{eid}/replay.json',timeout=45);response.raise_for_status();r=response.json();assert r['info']['EpisodeId']==eid;p.write_bytes(response.content)
        raw=p.read_bytes();r=json.loads(raw);assert len(r['steps'])==720 and all(x['status']=='DONE' for x in r['steps'][-1])
        print('ACQUIRED',eid,flush=True)
        return eid,dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(raw).hexdigest(),teams=r['info']['TeamNames'],rewards=r['rewards'],seed=r['info']['seed'])
    with ThreadPoolExecutor(max_workers=3) as pool:files=dict(pool.map(fetch,sorted(unique)))
    for j in jobs:j.update(files[j['episode']])
    (OUT/'COHORT.json').write_text(json.dumps(dict(protocol=protocol,games=jobs),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('DONE',len(jobs),'player-replays',len(unique),'unique games',flush=True)


if __name__=='__main__':main()
