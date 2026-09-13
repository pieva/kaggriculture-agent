"""Verify packaged actions against all four actual candidate replays and file loader."""
import sys,json,gzip,copy,hashlib
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools.operational_calendar_v44 import Agent
BASE=ROOT/'docs/model_specs/codex/e20';OUT=BASE/'reports/e20_9_release'
bundle=ROOT/'submission/submission_codex_e20_9_e20v44_late_tomato.py'
source=bundle.read_text(encoding='utf-8');checks=[]
for seed in [180911301,180911303]:
 for seat in [0,1]:
  names=['Tomato','E18'] if seat==0 else ['E18','Tomato']
  p=BASE/'artifacts/e20_9_development_d'/f'{names[0]}_{names[1]}_{seed}.replay.json.gz'
  r=json.load(gzip.open(p,'rt',encoding='utf-8'));scope={};local=Agent({'player_position':seat})
  with patch('builtins.open',side_effect=AssertionError('filesystem')),patch('io.open',side_effect=AssertionError('filesystem')):
   exec(compile(source,'<kaggle-exec>','exec'),scope)
  for i in range(719):
   obs=copy.deepcopy(r['steps'][i][seat]['observation']);expected=local(copy.deepcopy(obs),r['configuration'])
   with patch('builtins.open',side_effect=AssertionError('filesystem')),patch('io.open',side_effect=AssertionError('filesystem')):
    actual=scope['agent'](obs,r['configuration'])
   assert actual==expected==r['steps'][i+1][seat]['action'],(seed,seat,i)
   assert 'TOMATO_MISSION' not in json.dumps(actual)
  first=copy.deepcopy(r['steps'][0][seat]['observation'])
  assert scope['agent'](first,r['configuration'])==r['steps'][1][seat]['action']
  checks.append(dict(seed=seed,seat=seat,actions_equal=719,reset=True))
(OUT/'PARITY.json').write_text(json.dumps(checks,indent=2),encoding='utf-8');print('PARITY',checks,flush=True)
from kaggle_environments import make
env=make('kaggriculture',configuration={'seed':180911301,'episodeSteps':720,'turnsPerDay':24},debug=False)
env.run([str(ROOT/'submission/submission_codex_e18_2_capacity_governed_v4d.py'),str(bundle)])
r=env.toJSON();assert len(r['steps'])==720 and all(s['status']=='DONE' for s in r['steps'][-1]);assert r['rewards']==[87919.0,86034.0],r['rewards']
(OUT/'LOADER.json').write_text(json.dumps(dict(steps=720,rewards=r['rewards'],statuses=r['statuses'],sha256=hashlib.sha256(bundle.read_bytes()).hexdigest()),indent=2),encoding='utf-8');print('LOADER',r['rewards'])
