"""Serial, resumable four-policy tournament with frozen files and replay audits."""
import argparse,contextlib,gzip,hashlib,io,itertools,json,shutil,sys,time
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
SOURCE=Path('C:/Users/pietr/.codex/worktrees/756c/kaggriculture-agent')
sys.path.insert(0,str(SOURCE))
OUT=ROOT/'docs/model_specs/codex/e23/reports/tournament4_v1'

def main():
 global OUT
 p=argparse.ArgumentParser();p.add_argument('--pilot',action='store_true');p.add_argument('--limit',type=int);p.add_argument('--five',action='store_true');a=p.parse_args()
 if a.five:OUT=OUT.parent/'tournament5_v1'
 bundles=json.loads((OUT/'BUNDLES.json').read_text());hashes={k:v['sha256'] for k,v in bundles.items()}
 dest=OUT/('pilot' if a.pilot else 'matches');dest.mkdir(parents=True,exist_ok=True)
 pairs=([('E22S','E23M')] if a.five else [('E22G','E23G'),('E22S','E23S')]) if a.pilot else list(itertools.combinations(bundles,2))
 seeds=[180911301] if a.pilot else list(range(180911301,180911308))
 schedule=[dict(id=f'{x}_{y}_{s}_{rev}',seed=s,players=[y,x] if rev else [x,y]) for s in seeds for x,y in pairs for rev in (0,1)] if a.five else [dict(id=f'{x}_{y}_{s}_{rev}',seed=s,players=[y,x] if rev else [x,y]) for x,y in pairs for s in seeds for rev in (0,1)]
 protocol=dict(hashes=hashes,schedule=schedule,method='Serial actual file loader; shared endogenous market; all pairings, seven exposed seeds, reversed seats. Win=1, tie=0.5. Reserved seeds unused.',scope='Evolved portfolios plus service/sale adaptation and shared E22S repairs; not a pure species-only causal effect; not a Kaggle rating prediction.')
 pp=dest/'PROTOCOL.json'
 if pp.exists():assert json.loads(pp.read_text())==protocol
 else:pp.write_text(json.dumps(protocol,indent=2))
 if a.five and not a.pilot:
  previous=OUT.parent/'tournament4_v1/matches'
  for source in sorted(previous.glob('E*.json')):
   row=json.loads(source.read_text());path=dest/source.name
   assert all(hashes[k]==v for k,v in row['hashes'].items())
   assert row['id'] in {m['id'] for m in schedule}
   if path.exists():continue
   row['reused_from']=dict(path=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest())
   row['hashes']=hashes
   replay=source.with_suffix('.replay.json.gz')
   assert replay.exists()
   shutil.copyfile(replay,dest/replay.name)
   path.write_text(json.dumps(row,separators=(',',':')),encoding='utf-8')
   print('REUSED',row['id'],flush=True)
 with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
  from kaggle_environments import make
  from kaggle_environments.agent import get_last_callable
  from docs.model_specs.codex.e22.tools.analyze_external_20260914 import enrich
 for k,b in bundles.items():
  assert hashlib.sha256(Path(b['path']).read_bytes()).hexdigest()==hashes[k]
  assert get_last_callable(Path(b['path']).read_text(encoding='utf-8')).__name__=='agent'
 for n,m in enumerate(schedule[:a.limit] if a.limit else schedule,1):
  path=dest/(m['id']+'.json')
  if path.exists():
   assert json.loads(path.read_text())['hashes']==hashes
   continue
  start=time.time()
  for k,b in bundles.items():assert hashlib.sha256(Path(b['path']).read_bytes()).hexdigest()==hashes[k]
  env=make('kaggriculture',configuration=dict(seed=m['seed'],episodeSteps=720,turnsPerDay=24),debug=False)
  with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):env.run([bundles[k]['path'] for k in m['players']])
  game=env.toJSON()
  assert len(game['steps'])==720 and all(x['status']=='DONE' for x in game['steps'][-1]),(m,game['rewards'])
  for i,s in enumerate(game['steps']):s[0]['observation']['step']=i
  replay_path=dest/(m['id']+'.replay.json.gz')
  replay_tmp=replay_path.with_suffix('.tmp')
  replay_tmp.write_bytes(gzip.compress(json.dumps(game,separators=(',',':')).encode('utf-8'),compresslevel=1,mtime=0))
  replay_tmp.replace(replay_path)
  profiles=[enrich(game,s) for s in (0,1)]
  checks=[]
  for s,profile in enumerate(profiles):
   assert profile['ledger']['cash_parity_errors']==0
   f=game['steps'][-1][s]['observation']['farms'][s]
   mix=dict(Counter(t['animal'] for row in f['tiles'] for t in row if isinstance(t,dict) and t.get('animal')))
   checks.append(dict(mix=mix,hands=len(f['hands']),escapes=len(profile['ledger']['animal_escapes']),unfed=len(profile['unfed']),terminal=profile['terminal']))
  row=dict(**m,hashes=hashes,rewards=game['rewards'],profiles=profiles,checks=checks,seconds=round(time.time()-start,2))
  temporary=path.with_suffix('.tmp');temporary.write_text(json.dumps(row,separators=(',',':')),encoding='utf-8');temporary.replace(path)
  print(json.dumps(dict(n=n,total=len(schedule),id=m['id'],rewards=row['rewards'],checks=[{k:v for k,v in c.items() if k!='terminal'} for c in checks],seconds=row['seconds'])),flush=True)
 print('COMPLETE',dest,flush=True)

if __name__=='__main__':main()
