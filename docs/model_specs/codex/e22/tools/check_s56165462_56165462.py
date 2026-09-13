"""Frozen 20-replay sample: exact command and daily topology consistency."""
import json,hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests
from within_opponent_variability import signature
ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/model_specs/codex/e22/reports/e209_s56165462_kpi_20260913'
RAW=ROOT/'data/replays/json/e22_s56165462_56165462';RAW.mkdir(exist_ok=True)
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 h=json.loads((OUT/'history_56165462.json').read_text(encoding='utf-8'))
 eligible=sorted([e for e in h['episodes'] if e['state']=='COMPLETED' and e['type']=='EPISODE_TYPE_PUBLIC' and len({a['teamId'] for a in e['agents']})==2],key=lambda e:(e['createTime'],e['id']),reverse=True)
 anchor=next(e for e in eligible if e['id']==108518933)
 selected=[anchor]+[e for e in eligible if e['id']!=anchor['id']][:19]
 (OUT/'CONSISTENCY_PROTOCOL.json').write_text(json.dumps({'submission':56165462,'eligible':len(eligible),'selection':'User episode plus 19 latest other complete public non-self episodes, no outcome filter','episodes':[e['id'] for e in selected]},indent=2),encoding='utf-8')
 def fetch(e):
  eid=e['id'];path=RAW/f'{eid}.json'
  if not path.exists():
   z=requests.get(f'https://www.kaggle.com/competitions/episodes/{eid}/replay.json',timeout=60);z.raise_for_status();path.write_bytes(z.content)
  raw=path.read_bytes();r=json.loads(raw);assert len(r['steps'])==720
  a=next(a for a in e['agents'] if a['submissionId']==56165462);seat=a.get('index',0);s=signature(r,seat)
  result={'episode':eid,'seat':seat,'sha256':hashlib.sha256(raw).hexdigest(),'reward':r['rewards'][seat],'commands':[digest(x) for x in s['commands']],'market':[digest(x) for x in s['market']],'topology':[digest(x['topology']) for x in s['daily']],'crops':[digest(x['crops']) for x in s['daily']],'animals':[digest(x['animals']) for x in s['daily']]}
  print('CHECKED',eid,flush=True);return result
 with ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(fetch,selected))
 ref=rows[0];comparison=[]
 for r in rows:
  comparison.append({'episode':r['episode'],'reward':r['reward'],**{k:sum(a==b for a,b in zip(ref[k],r[k])) for k in ['commands','market','topology','crops','animals']}})
 result={'submission':56165462,'reference':108518933,'n':len(rows),'eligible':len(eligible),'comparisons':comparison,'records':rows}
 (OUT/'CONSISTENCY_56165462.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(comparison))
if __name__=='__main__':main()
