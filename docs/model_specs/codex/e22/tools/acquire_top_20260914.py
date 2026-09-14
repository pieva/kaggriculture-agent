"""Freeze five score-spaced leaderboard submissions and five latest games each."""
from pathlib import Path
import json,requests,hashlib,datetime,sys,contextlib,io
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT));OUT=ROOT/'docs/model_specs/codex/e22/reports/top_2750_3000_20260914';RAW=ROOT/'data/replays/json/top_2750_3000_20260914'
def main():
 OUT.mkdir(parents=True,exist_ok=True);RAW.mkdir(parents=True,exist_ok=True)
 selections=[dict(submission=s,score=v,rank=r) for s,v,r in [(56212183,2750.9,197),(56220723,2814.1,98),(56204870,2875.1,46),(56218579,2937.3,13),(56173067,2992.0,6)]]
 protocol=dict(frozen_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source='https://www.kaggle.com/competitions/kaggriculture/leaderboard',selection='Five displayed best-team submissions nearest target scores 2750/2812.5/2875/2937.5/3000 within [2750,3000], observed via leaderboard UI and View episodes URL. Five latest completed public non-self-play per exact submission; no outcome or topology filter. Exploratory score-spaced sample, not census of all top teams.',selections=selections)
 (OUT/'PROTOCOL.json').write_text(json.dumps(protocol,indent=2));jobs=[]
 for s in selections:
  sid=s['submission'];p=OUT/f'history_{sid}.json'
  if not p.exists():
   response=requests.post('https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes',json={'submissionId':sid},timeout=40);response.raise_for_status();p.write_text(json.dumps(response.json(),indent=2))
  h=json.loads(p.read_text());eps=sorted([e for e in h['episodes'] if e['state']=='COMPLETED' and e['type']=='EPISODE_TYPE_PUBLIC' and len({a['teamId'] for a in e['agents']})==2],key=lambda e:(e['createTime'],e['id']),reverse=True)[:5]
  assert len(eps)==5
  for e in eps:
   a=next(a for a in e['agents'] if a['submissionId']==sid);jobs.append(dict(**s,episode=e['id'],seat=a.get('index',0),metadata=e))
 def fetch(eid):
  p=RAW/f'{eid}.json'
  if not p.exists():
   r=requests.get(f'https://www.kaggle.com/competitions/episodes/{eid}/replay.json',timeout=60);r.raise_for_status();d=r.json();assert d['info']['EpisodeId']==eid;p.write_bytes(r.content)
  raw=p.read_bytes();r=json.loads(raw);assert len(r['steps'])==720 and all(a['status']=='DONE' for a in r['steps'][-1]);print('FETCH',eid,flush=True);return eid,dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(raw).hexdigest(),rewards=r['rewards'])
 with ThreadPoolExecutor(max_workers=3) as ex:files=dict(ex.map(fetch,sorted({j['episode'] for j in jobs})))
 for j in jobs:j.update(files[j['episode']])
 (OUT/'COHORT.json').write_text(json.dumps(jobs,indent=2))
 with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
  from docs.model_specs.codex.e22.tools.analyze_external_20260914 import enrich
  import kaggle_environments
 dest=OUT/'profiles';dest.mkdir(exist_ok=True)
 for j in jobs:
  p=dest/f"{j['submission']}_{j['episode']}.json.gz"
  if p.exists():continue
  r=json.loads((ROOT/j['path']).read_text())
  for i,step in enumerate(r['steps']):step[0]['observation']['step']=i
  profile=enrich(r,j['seat'],trace=True)
  import gzip
  with gzip.open(p,'wt',encoding='utf-8') as f:json.dump(dict(meta=j,profile=profile),f,separators=(',',':'))
  print('TOP AUDITED',j['submission'],j['episode'],flush=True)
if __name__=='__main__':main()
