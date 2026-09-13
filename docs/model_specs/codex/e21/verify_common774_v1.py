"""Verify packaged actions against all four actual candidate replays and file loader."""
import sys,json,gzip,copy,hashlib
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e21.operational774_v1_policy import Agent
BASE=ROOT/'docs/model_specs/codex/e21';OUT=BASE/'reports/operational774_v1'
bundle=ROOT/'submission/submission_codex_e21_common774_v1.py'
source=bundle.read_text(encoding='utf-8');checks=[]
for seed in [180911301,180911303]:
 for seat in [0,1]:
  names=['Common774','E18'] if seat==0 else ['E18','Common774']
  p=BASE/'artifacts/operational774_v1'/f'{names[0]}_{names[1]}_{seed}.replay.json.gz'
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
  k=json.loads(p.with_name(p.name.replace('.replay.json.gz','.kpi.json')).read_text());side=k['sides'][seat]
  assert side['kpi'][-1]['animals']=={'COW':8,'SHEEP':9,'GOOSE':1}
  assert side['kpi'][-1]['pasture_topology']=={'Q0':7,'Q1':7,'Q2':4,'Q3':0}
  assert not side['ledger']['animal_escapes'] and side['ledger']['cash_parity_errors']==0
  assert side['kpi'][11]['STRAWBERRY']==33
  native=json.loads((BASE/f'artifacts/operational772_recorded_control/OpRecorded_E18_{seed}.kpi.json').read_text())['sides'][0]
  daily=[{'day':x['day'],'actual':{c:x[c] for c in ['MELON','WHEAT','STRAWBERRY','CARROT']},'native':{c:y[c] for c in ['MELON','WHEAT','STRAWBERRY','CARROT']}} for x,y in zip(side['kpi'],native['kpi'])]
  checks.append(dict(seed=seed,seat=seat,actions_equal=719,reset=True,cash=side['reward'],opponent=k['sides'][1-seat]['reward'],metrics=dict(local.metrics),crop_losses=side['crop_starvation'],terminal=side['terminal'],daily_alignment=daily,unfinished_jobs=local.log))
(OUT/'PARITY.json').write_text(json.dumps(checks,indent=2),encoding='utf-8');print('PARITY',checks,flush=True)
from kaggle_environments import make
env=make('kaggriculture',configuration={'seed':180911301,'episodeSteps':720,'turnsPerDay':24},debug=False)
env.run([str(ROOT/'submission/submission_codex_e18_2_capacity_governed_v4d.py'),str(bundle)])
r=env.toJSON();assert len(r['steps'])==720 and all(s['status']=='DONE' for s in r['steps'][-1]);assert r['rewards']==[79012.0,83239.0],r['rewards']
(OUT/'LOADER.json').write_text(json.dumps(dict(steps=720,rewards=r['rewards'],statuses=r['statuses'],sha256=hashlib.sha256(bundle.read_bytes()).hexdigest()),indent=2),encoding='utf-8');print('LOADER',r['rewards'])
