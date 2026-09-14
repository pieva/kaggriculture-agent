"""Frozen E22 cohort and serial replay audits. Public observations, numeric IDs only."""
import json,hashlib,sys,runpy,requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
OUT=ROOT/'docs/model_specs/codex/e22/reports/external_e22_20260913';RAW=ROOT/'data/replays/json/e22_external_20260913';RAW.mkdir(parents=True,exist_ok=True)
def main():
 h=json.loads((OUT/'history.json').read_text());games=[]
 for e in h['episodes']:
  if e['state']!='COMPLETED' or e['type']!='EPISODE_TYPE_PUBLIC' or len({a['teamId'] for a in e['agents']})!=2:continue
  a=next(a for a in e['agents'] if a['submissionId']==56206528);b=next(b for b in e['agents'] if b['teamId']!=a['teamId'])
  games.append(dict(episode=e['id'],time=e['endTime'],seat=a.get('index',0),opponent_submission=b['submissionId'],cash=a['reward'],opponent_cash=b['reward'],margin=a['reward']-b['reward'],rating_before=a['initialScore'],rating_after=a['updatedScore']))
 games.sort(key=lambda g:g['time']);selected={games[round(i*(len(games)-1)/15)]['episode'] for i in range(16)}|{108561064,108559326,108551697,min(games,key=lambda g:g['margin'])['episode'],max(games,key=lambda g:g['margin'])['episode']}
 (OUT/'COHORT.json').write_text(json.dumps(dict(frozen_utc=datetime.now(timezone.utc).isoformat(),submission=56206528,selection='All completed public non-self-play episodes for outcomes; deep audit: 16 equally spaced chronological ranks plus three user episodes and margin extremes. Diagnostic sample, not unbiased outcome estimate.',selected=sorted(selected),games=games),indent=2)+'\n')
 def fetch(g):
  p=RAW/f"{g['episode']}.json"
  if not p.exists():
   rr=requests.get(f"https://www.kaggle.com/competitions/episodes/{g['episode']}/replay.json",timeout=55);rr.raise_for_status();d=rr.json();assert d['info']['EpisodeId']==g['episode'];p.write_bytes(rr.content)
  return g,p
 with ThreadPoolExecutor(max_workers=3) as pool:paths=list(pool.map(fetch,[g for g in games if g['episode'] in selected]))
 from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit,end_state
 plan=runpy.run_path(str(ROOT/'submission/submission_codex_e22_s56165462_observed_v1.py'))['_PLAN']
 dest=OUT/'profiles';dest.mkdir(exist_ok=True)
 for g,p in paths:
  result=dest/f"{g['episode']}.json"
  if result.exists():continue
  r=json.loads(p.read_text());assert len(r['steps'])==720 and all(s['status']=='DONE' for s in r['steps'][-1]);sides=[]
  for seat in (g['seat'],1-g['seat']):
   ledger=audit(r,seat);daily=[]
   for day in range(1,31):
    obs=r['steps'][day*24-1][seat]['observation'];f=obs['farms'][seat]
    cells=[dict(x=x,y=y,quadrant=f'Q{2*(y//5)+x//5}',**t) for y,row in enumerate(f['tiles']) for x,t in enumerate(row) if isinstance(t,dict)]
    daily.append(dict(day=day,money=f['money'],cells=cells,hands=len(f['hands']),prices=obs['market']['prices']))
   acts=[s[seat]['action'] for s in r['steps'][1:]];events=[]
   for i in range(1,720):
    before=r['steps'][i-1][seat]['observation'];after=r['steps'][i][seat]['observation']
    for y,row in enumerate(after['farms'][seat]['tiles']):
     for x,t in enumerate(row):
      old=before['farms'][seat]['tiles'][y][x]
      if isinstance(t,dict) and t['kind'] in ('COOP','PASTURE') and (not isinstance(old,dict) or (old.get('kind'),old.get('animal'))!=(t.get('kind'),t.get('animal'))):events.append(dict(day=before['day']+1,hour=before['hour']+1,x=x,y=y,kind=t['kind'],animal=t.get('animal'),cash_before=before['farms'][seat]['money']))
   sides.append(dict(seat=seat,daily=daily,ledger=ledger,terminal=end_state(r,seat),events=events,full_matches=sum(x==y for x,y in zip(acts,plan)),worker_matches=sum((x.get('farmer'),x.get('hands'))==(y.get('farmer'),y.get('hands')) for x,y in zip(acts,plan))))
  result.write_text(json.dumps(dict(**g,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),raw=p.relative_to(ROOT).as_posix(),sides=sides),separators=(',',':'))+'\n')
  print('AUDITED',g['episode'],g['margin'],flush=True)
 print('DONE',len(paths),flush=True)
if __name__=='__main__':main()
