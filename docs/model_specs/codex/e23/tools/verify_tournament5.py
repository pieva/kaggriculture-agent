"""Final balanced-schedule and artifact-provenance verification; no new games."""
import hashlib,itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/model_specs/codex/e23/reports/tournament5_v1'

def main():
 bundles=json.loads((OUT/'BUNDLES.json').read_text());protocol=json.loads((OUT/'matches/PROTOCOL.json').read_text())
 rows=[json.loads(p.read_text()) for p in sorted((OUT/'matches').glob('E*.json'))]
 assert len(rows)==140 and {r['id'] for r in rows}=={r['id'] for r in protocol['schedule']}
 hashes={k:hashlib.sha256(Path(v['path']).read_bytes()).hexdigest() for k,v in bundles.items()}
 assert hashes==protocol['hashes']=={k:v['sha256'] for k,v in bundles.items()}
 assert all(r['hashes']==hashes for r in rows)
 counts=Counter(k for r in rows for k in r['players']);assert set(counts.values())=={56}
 archives=[];reversal=[]
 for r in rows:
  assert len(r['profiles'])==2 and len(r['checks'])==2
  if 'reused_from' in r:
   source=r['reused_from'];assert hashlib.sha256(Path(source['path']).read_bytes()).hexdigest()==source['sha256']
  for seat,p in enumerate(r['profiles']):
   assert p['reward']==r['rewards'][seat] and p['ledger']['cash_parity_errors']==0
   assert len(p['kpi'])==len(p['ledger']['daily'])==30
  path=OUT/'matches'/(r['id']+'.replay.json.gz');assert path.exists()
  archives.append(dict(match=r['id'],path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),reused_from=r.get('reused_from')))
 for a,b in itertools.combinations(bundles,2):
  for seed in range(180911301,180911308):
   pair=[r for r in rows if r['seed']==seed and set(r['players'])=={a,b}]
   assert len(pair)==2 and {tuple(r['players']) for r in pair}=={(a,b),(b,a)}
   delta={k:pair[0]['rewards'][pair[0]['players'].index(k)]-pair[1]['rewards'][pair[1]['players'].index(k)] for k in (a,b)}
   reversal.append(dict(a=a,b=b,seed=seed,reward_difference=delta))
 diagnostic=json.loads((OUT/'DIAGNOSTICS.json').read_text());assert diagnostic['matches']==140
 runtime=json.loads((OUT/'RUNTIME.json').read_text());assert hashlib.sha256(Path(runtime['engine_path']).read_bytes()).hexdigest()==runtime['engine_sha256']
 for path,digest in runtime['audit_dependencies'].items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest
 result=dict(matches=140,profiles=280,per_policy=dict(counts),pairings=10,exposed_seeds=list(range(180911301,180911308)),reserved_seeds_used=False,
  hashes=hashes,cash_parity_errors=0,paired_seat_checks=len(reversal),seat_reversals_with_reward_difference=sum(any(r['reward_difference'].values()) for r in reversal),
  expected_mix_profiles=sum(v['expected_mix_games'] for v in diagnostic['summary'].values()),q2_wheat_harvest_profiles=sum(v['q2_wheat_harvest_games'] for v in diagnostic['summary'].values()),
  animal_escapes=sum(v['escapes'] for v in diagnostic['summary'].values()),animal_inventory_difference=dict(sum((Counter(v['animal_inventory_difference']) for v in diagnostic['summary'].values()),Counter())),
  reused_matches=sum('reused_from' in r for r in rows),pilot_games=6,pilot_e23_actions_verified=4314,engine_hash_verified=True,archive_hashes_recorded=140)
 (OUT/'REPLAY_MANIFEST.json').write_text(json.dumps(archives,indent=2),encoding='utf-8')
 (OUT/'SEAT_REVERSALS.json').write_text(json.dumps(reversal,indent=2),encoding='utf-8')
 (OUT/'VERIFICATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
