"""Check replay fidelity, observation purity and actual end-state invariants."""
import argparse,copy,gzip,hashlib,json,runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/model_specs/codex/e23/reports/tournament4_v1'

def main():
 global OUT
 parser=argparse.ArgumentParser();parser.add_argument('--five',action='store_true');args=parser.parse_args()
 if args.five:OUT=OUT.parent/'tournament5_v1'
 bundles=json.loads((OUT/'BUNDLES.json').read_text());verified=0;games=0
 for path in sorted((OUT/'pilot').glob('E*.json')):
  row=json.loads(path.read_text());games+=1
  with gzip.open(path.with_suffix('.replay.json.gz'),'rt',encoding='utf-8') as f:r=json.load(f)
  for seat,key in enumerate(row['players']):
   if not key.startswith('E23'):continue
   b=bundles[key];assert hashlib.sha256(Path(b['path']).read_bytes()).hexdigest()==b['sha256']
   ns=runpy.run_path(b['path']);policy=ns['agent'];frozen=copy.deepcopy(ns['_PLAN'])
   for i in range(719):
    obs=r['steps'][i][seat]['observation'];before=copy.deepcopy(obs)
    actual=r['steps'][i+1][seat]['action'];out=policy(obs,r['configuration'])
    assert out==actual,(key,i,'replay mismatch')
    assert obs==before,(key,i,'observation mutated')
    assert policy(obs,r['configuration'])==out,(key,i,'nondeterminism')
    assert len(out['market'])<=r['configuration']['maxMarketOrdersPerTurn']
    verified+=1
   assert ns['_PLAN']==frozen,'embedded calendar mutated'
   assert row['checks'][seat]['mix']==b['mix']
   assert row['checks'][seat]['escapes']==0
   assert row['checks'][seat]['hands']==11
   assert row['profiles'][seat]['ledger']['cash_parity_errors']==0
   assert all(row['profiles'][seat]['terminal'][kind].get(p,0)==0 for kind in ['shed','carried'] for p in ['MILK','WOOL','EGG'])
 result=dict(pilot_games=games,e23_actions_verified=verified,deterministic=True,observation_and_plan_unchanged=True,expected_mixes=True,escapes=0,terminal_carried_or_shed_animal_products=0,remaining_tile_yield='Reported separately; zero carry does not imply full harvest.',hashes={k:v['sha256'] for k,v in bundles.items()})
 assert games==(2 if args.five else 4) and verified==(1438 if args.five else 2876)
 (OUT/'PILOT_VERIFICATION.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=='__main__':main()
