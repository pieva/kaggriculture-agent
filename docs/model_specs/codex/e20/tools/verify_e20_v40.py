from pathlib import Path
import sys,json,gzip,copy
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools.operational_calendar_goose2 import Agent
BASE=ROOT/'docs/model_specs/codex/e20'
bundle=ROOT/'submission/submission_codex_e20_8_e20v40_calendar_2g.py'
source=bundle.read_text(encoding='utf-8');rows=[]
for seed in [180911301,180911303]:
 replay=json.load(gzip.open(ROOT/f'docs/model_specs/codex/e21/artifacts/operational772_goose2_v2/Goose2_E18_{seed}.replay.json.gz','rt',encoding='utf-8'))
 for seat in [0,1]:
  scope={};local=Agent({'player_position':seat})
  with patch('builtins.open',side_effect=AssertionError('filesystem')),patch('io.open',side_effect=AssertionError('filesystem')):
   exec(compile(source,'<kaggle-exec>','exec'),scope)
  matches=0
  for i in range(719):
   obs=copy.deepcopy(replay['steps'][i][0]['observation'])
   if seat==1:obs['farms'].reverse();obs['player']=1
   expected=local(copy.deepcopy(obs),replay['configuration'])
   with patch('builtins.open',side_effect=AssertionError('filesystem')),patch('io.open',side_effect=AssertionError('filesystem')):actual=scope['agent'](obs,replay['configuration'])
   assert actual==expected,(seed,seat,i)
   if seat==0:assert actual==replay['steps'][i+1][0]['action'],(seed,i,'historical parity')
   matches+=1
  rows.append({'seed':seed,'seat':seat,'actions_equal':matches,'seat1_input':'mirrored observations' if seat else 'actual replay'})
out=BASE/'reports/e20_8_release';out.mkdir(exist_ok=True)
(out/'PARITY.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(rows)
if __name__=='__main__':
 from kaggle_environments import make
 # Exercise real file loader and actual opposite seat, not only mirrored inputs.
 opponent=str(ROOT/'submission/submission_codex_e18_2_capacity_governed_v4d.py')
 env=make('kaggriculture',configuration={'seed':180911301,'episodeSteps':720,'turnsPerDay':24},debug=False)
 env.run([opponent,str(bundle)])
 result=env.toJSON();assert len(result['steps'])==720 and all(s['status']=='DONE' for s in result['steps'][-1])
 assert result['rewards']==[87172.0,85740.0],result['rewards']
 with gzip.open(out/'LOADER_SEAT1.replay.json.gz','wt',encoding='utf-8') as f:json.dump(result,f)
 (out/'LOADER.json').write_text(json.dumps({'status':result['statuses'],'rewards':result['rewards'],'steps':len(result['steps']),'seed':180911301,'seat':1},indent=2),encoding='utf-8')
 print('LOADER',result['rewards'])
