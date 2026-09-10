"""Verify completeness, frozen provenance and observed topology on all 42 games."""
import gzip
import hashlib
import itertools
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'docs/model_specs/codex/e20'

def main():
    protocol=json.loads((BASE/'VALIDATION_PROTOCOL.json').read_text())
    expected={(a,b,s) for a,b in itertools.permutations(['E18','E19','E20'],2) for s in protocol['tournament_seeds_reserved_before_results']}
    paths=[p for p in (BASE/'artifacts/tournament').glob('*.json') if not p.name.endswith('.kpi.json')]
    observed=set();prefixes={};max_cap=[0,0,0];errors=[];crop_stress={};animal_losses={};source_hashes={}
    for path in paths:
        meta=json.loads(path.read_text())
        key=(*meta['agents'],meta['seed']);assert key not in observed;observed.add(key)
        assert path.with_suffix('.kpi.json').exists()
        detail=json.loads(path.with_suffix('.kpi.json').read_text())
        with gzip.open(path.with_suffix('.replay.json.gz'),'rb') as f:raw=f.read()
        assert hashlib.sha256(raw).hexdigest()==meta['replay_sha256']
        replay=json.loads(raw)
        assert len(replay['steps'])==720
        assert all(s['status']=='DONE' for s in replay['steps'][-1])
        for p,h in meta['sources'].items():
            if p.startswith('submission'):
                assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
                source_hashes[p]=h
        for seat,name in enumerate(meta['agents']):
            assert meta['runtime'][seat]['calls']==719
            if name in {'E19','E20'}:
                assert meta['runtime'][seat]['core_errors']==0
            side=detail['sides'][seat]
            assert side['reward']==meta['rewards'][seat]
            crop_stress[name]=crop_stress.get(name,0)+len(side['crop_starvation'])
            animal_losses[name]=animal_losses.get(name,0)+len(side['ledger']['animal_escapes'])
            if name not in {'E19','E20'}:continue
            if meta['agents'][1-seat]=='E18':
                prefixes[(meta['seed'],seat,name)]=[s[seat]['action'] for s in replay['steps'][1:265]]
            if name!='E20':continue
            for step in replay['steps']:
                farm=step[seat]['observation']['farms'][seat]
                counts=[0,0,0]
                for y,row in enumerate(farm['tiles']):
                    for x,t in enumerate(row):
                        if isinstance(t,dict) and t.get('kind')=='PASTURE':counts[(0 if x<5 else 1) if y<5 else 2]+=1
                assert all(n<=cap for n,cap in zip(counts,[7,7,2]))
                max_cap=[max(a,b) for a,b in zip(max_cap,counts)]
    assert observed==expected,(expected-observed,observed-expected)
    for seed in protocol['tournament_seeds_reserved_before_results']:
        for seat in (0,1):assert prefixes[(seed,seat,'E19')]==prefixes[(seed,seat,'E20')]
    result=dict(complete=True,games=42,independent_seeds=7,expected_pairings_verified=True,
                opening_E19_E20_parity_cases=14,E20_max_observed_pastures=max_cap,
                frozen_bundles=source_hashes,animal_losses=animal_losses,crop_stress_transitions=crop_stress,
                source=str(Path(__file__).relative_to(ROOT)))
    (BASE/'artifacts/TOURNAMENT_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
