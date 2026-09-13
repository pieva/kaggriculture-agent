"""Serial E19.2 screening, original E19 frozen and explicit source hashes."""
import gzip,hashlib,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
HERE=Path(__file__).resolve().parent
def main():
 candidate=sys.argv[1] if len(sys.argv)>1 else 'v52a'
 out=HERE/'reports'/candidate;art=HERE/'artifacts'/candidate;out.mkdir(parents=True,exist_ok=True);art.mkdir(parents=True,exist_ok=True)
 paths=[ROOT/f'submission/archive/e19_rejected/submission_codex_e19_2_770_{candidate}.py',ROOT/'submission/submission_codex_e19_770_v51_candidate.py']
 protocol={'candidate':candidate,'control':'E19 V51C','seeds':[180911301,180911303],'seats':[0,1] if '--both' in sys.argv else [0],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'method':'Serial direct paired games, exposed seeds; no publication.'}
 (out/'PROTOCOL.json').write_text(json.dumps(protocol,indent=2),encoding='utf-8')
 from kaggle_environments import make
 from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit,end_state
 rows=[]
 for seed in protocol['seeds']:
  for seat in protocol['seats']:
   dest=art/f'{seed}_{seat}.json'
   if dest.exists():rows.append(json.loads(dest.read_text()));continue
   agents=[None,None];times=[[],[]]
   for p,s in zip(paths,[seat,1-seat]):
    ns={};exec(p.read_text(encoding='utf-8').replace('_v51pkg',f'_e192seat{s}'),ns);agents[s]=ns['create_agent']({'player_position':s})
   def capture(i):
    def fn(o,c):
     start=time.perf_counter();a=agents[i](o,c);times[i].append(time.perf_counter()-start);return a
    return fn
   env=make('kaggriculture',configuration={'seed':seed,'episodeSteps':720,'turnsPerDay':24},debug=False);env.run([capture(0),capture(1)]);r=env.toJSON()
   assert len(r['steps'])==720 and all(s['status']=='DONE' for s in r['steps'][-1])
   ls=[audit(r,i) for i in [0,1]]
   row={'candidate':candidate,'seed':seed,'seat':seat,'rewards':r['rewards'],'margin':r['rewards'][seat]-r['rewards'][1-seat],'ledger':ls,'terminal':[end_state(r,i) for i in [0,1]],'runtime':[{'calls':len(t),'max_seconds':max(t),'seconds':sum(t)} for t in times],'core_errors':[getattr(a.core,'error_count',None) for a in agents]}
   with gzip.open(dest.with_suffix('.replay.json.gz'),'wt',encoding='utf-8') as f:json.dump(r,f,separators=(',',':'))
   dest.write_text(json.dumps(row,separators=(',',':')),encoding='utf-8');rows.append(row)
   print('RESULT',candidate,seed,seat,r['rewards'],'margin',row['margin'],'labor',[sum(d['hire_cash'] for d in l['daily']) for l in ls],'escapes',[len(l['animal_escapes']) for l in ls],flush=True)
 (out/'RESULTS.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
if __name__=='__main__':main()
