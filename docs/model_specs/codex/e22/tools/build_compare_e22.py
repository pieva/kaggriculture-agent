"""Observed constant plan replica and serial paired diagnostic comparison."""
import base64,copy,gzip,hashlib,json,sys,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
OUT=ROOT/'docs/model_specs/codex/e22/reports/e22_replica_internal';OUT.mkdir(exist_ok=True)
ART=ROOT/'docs/model_specs/codex/e22/artifacts/e22_replica_internal';ART.mkdir(parents=True,exist_ok=True)
BUNDLE=ROOT/'submission/submission_codex_e22_s56165462_observed_v1.py'
FROZEN=ROOT/'submission/submission_codex_e20_9_e20v44_late_tomato.py'
def main():
 source=ROOT/'data/replays/json/e22_s56165462_56165462/108518933.json';r=json.loads(source.read_text(encoding='utf-8'))
 records=json.loads((OUT.parent/'e209_s56165462_kpi_20260913/CONSISTENCY_56165462.json').read_text())['records'];seat=next(x['seat'] for x in records if x['episode']==108518933)
 frames=[s[seat]['action'] for s in r['steps'][1:]]
 payload=base64.b64encode(zlib.compress(json.dumps(frames,separators=(',',':')).encode())).decode()
 code='''"""E22 internal baseline: observed constant plan, s56165462 56165462.
Reconstructed from public actions, not the competitor source code.
Uses only current day/hour. No future observations or replay outcomes.
"""
import base64,zlib,json,copy
_PLAN=json.loads(zlib.decompress(base64.b64decode(PAYLOAD)))
class Agent:
 def __init__(self,context=None):pass
 def __call__(self,obs,cfg=None):
  i=int(obs['day'])*24+int(obs['hour'])
  return copy.deepcopy(_PLAN[i]) if 0<=i<len(_PLAN) else {'farmer':['PASS'],'hands':[],'market':[]}
def create_agent(context=None):return Agent(context)
_AGENT=Agent()
def agent(observation,configuration=None):
 return _AGENT(observation,configuration)
'''.replace('PAYLOAD',repr(payload))
 BUNDLE.write_text(code,encoding='utf-8');ns={};exec(code,ns)
 for rec in records:
  raw=json.loads((ROOT/f"data/replays/json/e22_s56165462_56165462/{rec['episode']}.json").read_text(encoding='utf-8'));a=ns['create_agent']()
  assert all(a(raw['steps'][i][rec['seat']]['observation'])==raw['steps'][i+1][rec['seat']]['action'] for i in range(719))
 from docs.model_specs.codex.e20.tools.operational_calendar_v44 import Agent as Fixed
 # Regression: product PLACE must survive an occupied shed-access tile.
 test=Fixed({'player_position':1});test.start_day(11);test.queues[1]=[dict(position=[4,4],command=['PLACE','MELON',6],source_day=11,source_hour=1)];test.indices[1]=0
 old=json.loads((ROOT/'data/replays/json/e22_opponents_20260913/108480607.json').read_text(encoding='utf-8'));obs=copy.deepcopy(old['steps'][251][1]['observation']);assert obs['farms'][1]['hands'][0]==[4,4];assert obs['private']['inventories'][1]['MELON']==6
 assert test.act_worker(1,obs,copy.deepcopy({k:obs['private'][k] for k in ['shed','seeds']}))==['PLACE','MELON',6]
 protocol=dict(models=['E22Replica','E209Fix'],opponent='E209 frozen',seeds=[180911301,180911303],seats=[0,1],replica_submission=56165462,replica_episode=108518933,parity_replays=20,parity_actions=14380,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),bundle_sha256=hashlib.sha256(BUNDLE.read_bytes()).hexdigest(),frozen_sha256=hashlib.sha256(FROZEN.read_bytes()).hexdigest(),fix='PLACE skip only for animal items, not product deposits',limits='Exposed seeds; internal diagnostics, no rating inference or publication. One simulation at a time.')
 assert protocol['frozen_sha256']=='56956735924f78d3d5502754425b207c67849ff217980e3c383add726b47debe'
 (OUT/'PROTOCOL.json').write_text(json.dumps(protocol,indent=2),encoding='utf-8')
 print('PARITY 14380 actions; regression passed',flush=True)
 from kaggle_environments import make
 from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit,end_state
 rows=[]
 for model in protocol['models']:
  for seed in protocol['seeds']:
   for seat in protocol['seats']:
    path=ART/f'{model}_{seed}_{seat}.json'
    if path.exists():rows.append(json.loads(path.read_text()));continue
    frozen={};exec(FROZEN.read_text(encoding='utf-8'),frozen)
    candidate=ns['create_agent']() if model=='E22Replica' else Fixed({'player_position':seat})
    agents=[None,None];agents[seat]=candidate;agents[1-seat]=frozen['create_agent']({'player_position':1-seat})
    env=make('kaggriculture',configuration=dict(seed=seed,episodeSteps=720,turnsPerDay=24),debug=False);env.run(agents);game=env.toJSON()
    assert len(game['steps'])==720 and all(s['status']=='DONE' for s in game['steps'][-1])
    ledgers=[audit(game,i) for i in [0,1]]
    row=dict(model=model,seed=seed,seat=seat,rewards=game['rewards'],margin=game['rewards'][seat]-game['rewards'][1-seat],ledgers=ledgers,terminal=[end_state(game,i) for i in [0,1]])
    with gzip.open(path.with_suffix('.replay.json.gz'),'wt',encoding='utf-8') as f:json.dump(game,f,separators=(',',':'))
    path.write_text(json.dumps(row,separators=(',',':')),encoding='utf-8');rows.append(row)
    print('RESULT',model,seed,seat,row['rewards'],row['margin'],flush=True)
 (OUT/'RESULTS.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
if __name__=='__main__':main()
