from pathlib import Path
import json,requests,hashlib,datetime
from concurrent.futures import ThreadPoolExecutor
out=Path('docs/model_specs/codex/e22/reports/external_e22_2_20260914');raw=Path('data/replays/json/e22_external_20260914');raw.mkdir(parents=True,exist_ok=True)
jobs=[];hist={}
for sid in [56212495,56206528]:
 history_path=out/f'history_{sid}.json'
 if not history_path.exists():
  response=requests.post('https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes',json={'submissionId':sid},timeout=40);response.raise_for_status();history_path.write_text(json.dumps(response.json(),indent=2))
 h=json.loads(history_path.read_text()); eps=[]
 for e in h['episodes']:
  a=next(a for a in e['agents'] if a['submissionId']==sid);b=next((x for x in e['agents'] if x['id']!=a['id']),None)
  eps.append(dict(episode=e['id'],state=e['state'],type=e['type'],created=e['createTime'],ended=e.get('endTime'),seat=a.get('index',0),own=a,opponent=b,selfplay=b is not None and b['teamId']==a['teamId']))
 competitive=sorted([e for e in eps if e['state']=='COMPLETED' and e['type']=='EPISODE_TYPE_PUBLIC' and not e['selfplay']],key=lambda x:(x['created'],x['episode']))
 hist[str(sid)]={'submission':next(s for s in h['submissions'] if s['id']==sid),'episodes':eps,'competitive_n':len(competitive),'latest_rating':competitive[-1]['own']['updatedScore'],'wins':sum(e['own']['reward']>e['opponent']['reward'] for e in competitive),'losses':sum(e['own']['reward']<e['opponent']['reward'] for e in competitive)}
 for e in competitive[-20:]:jobs.append(dict(e,submission=sid))
(out/'HISTORY_SUMMARY.json').write_text(json.dumps(hist,indent=2))
(out/'PROTOCOL.json').write_text(json.dumps({'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'history':'All returned episodes; incomplete and self-play reported separately','replay_selection':'20 latest completed public non-self-play per exact submission, no outcome/topology filter. Descriptive independent external cohorts, not paired experiment.','selected':[{k:j[k] for k in ['episode','submission','seat']} for j in jobs]},indent=2))
def fetch(eid):
 p=raw/f'{eid}.json'
 if not p.exists():
  r=requests.get(f'https://www.kaggle.com/competitions/episodes/{eid}/replay.json',timeout=60);r.raise_for_status();d=r.json();assert d['info']['EpisodeId']==eid;p.write_bytes(r.content)
 bs=p.read_bytes();d=json.loads(bs);print('FETCH',eid,len(d['steps']),flush=True);return eid,dict(path=p.as_posix(),sha256=hashlib.sha256(bs).hexdigest(),steps=len(d['steps']),statuses=d.get('statuses'),rewards=d['rewards'])
with ThreadPoolExecutor(max_workers=3) as ex:files=dict(ex.map(fetch,sorted({j['episode'] for j in jobs})))
for j in jobs:j.update(files[j['episode']]);assert j['rewards'][j['seat']]==j['own']['reward']
(out/'COHORT.json').write_text(json.dumps(jobs,indent=2));print('DONE',len(jobs),flush=True)
