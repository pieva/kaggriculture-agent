"""Bounded public topology screen; no strategy simulation or submission."""
import hashlib,json,time
from pathlib import Path
import requests
OUT=Path(__file__).resolve().parent/'reports/top774_search';OUT.mkdir(parents=True,exist_ok=True)
def top(r,seat,index):
 c=[0]*4
 for y,row in enumerate(r['steps'][index][seat]['observation']['farms'][seat]['tiles']):
  for x,t in enumerate(row):
   if isinstance(t,dict) and t.get('kind')=='PASTURE':c[int(x>=5)+2*int(y>=5)]+=1
 return c
def main():
 protocol=dict(start_submission=56156662,minimum_observed_rating=2700,max_submission_histories=30,
  selection='Descending observed agent score from public episode metadata, not cash; latest completed competitive episode per history',
  qualification='If exact final 7-7-4-0 found, inspect five consecutive completed non-selfplay episodes from same submission; at least 4/5 final 774 and >=80% D15-30 daily checkpoints 774 on qualifying episodes',
  scope='Network sample of strong agents, not exhaustive leaderboard or independent validation')
 (OUT/'SEARCH_PROTOCOL.json').write_text(json.dumps(protocol,indent=2)+'\n')
 queue={56156662:3223.2};checked=set();episodes={};profiles=[];histories=[];errors=[]
 for n in range(30):
  choices=[(score,sid) for sid,score in queue.items() if sid not in checked and score>=2700]
  if not choices:break
  score,sid=max(choices);checked.add(sid)
  try:
   response=requests.post('https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes',json={'submissionId':sid},timeout=30);response.raise_for_status();data=response.json()
   (OUT/f'history_{sid}.json').write_text(json.dumps(data,separators=(',',':')))
   es=[e for e in data.get('episodes',[]) if e.get('state')=='COMPLETED' and len({a['submissionId'] for a in e['agents']})==2]
   for e in es:
    for a in e['agents']:queue[a['submissionId']]=max(queue.get(a['submissionId'],0),a.get('updatedScore',a.get('initialScore',0)))
   if not es:continue
   e=es[0];eid=e['id'];histories.append(dict(submission=sid,observed_score=score,episode=eid))
   if eid in episodes:continue
   path=OUT/f'{eid}.json'
   if path.exists():raw=path.read_bytes()
   else:
    response=requests.get(f'https://www.kaggle.com/competitions/episodes/{eid}/replay.json',timeout=45);response.raise_for_status();raw=response.content;path.write_bytes(raw)
   r=json.loads(raw);assert len(r['steps'])==720 and all(x['status']=='DONE' for x in r['steps'][-1])
   episodes[eid]=hashlib.sha256(raw).hexdigest()
   for a in e['agents']:
    seat=a.get('index',0);daily=[top(r,seat,24*d-1) for d in range(1,31)]
    name=r['info']['TeamNames'][seat]
    p=dict(name=name,submission=a['submissionId'],episode=eid,seat=seat,score=a.get('initialScore'),final=daily[-1],daily=daily,
      matches774=sum(t==[7,7,4,0] for t in daily[14:]),url=f'https://www.kaggle.com/competitions/episodes/{eid}')
    profiles.append(p);print(json.dumps({k:p[k] for k in ['name','submission','episode','score','final','matches774']},ensure_ascii=True),flush=True)
   if any(p['final']==[7,7,4,0] for p in profiles):break
  except Exception as exc:errors.append(dict(submission=sid,error=str(exc)));print('ERROR '+str(exc),flush=True)
  finally:
   (OUT/'SCREEN.json').write_text(json.dumps(dict(histories=histories,profiles=profiles,replay_sha256=episodes,errors=errors),indent=2)+'\n')
 print('DONE '+str(len(profiles))+' profiles',flush=True)
if __name__=='__main__':main()
