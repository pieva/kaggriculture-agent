"""Verify cohort completeness and immutable policy/replay/ledger provenance."""
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools.run_experiment import BUNDLES
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS
BASE=ROOT/'docs/model_specs/codex/e20'

def main():
    gate=json.loads((BASE/'artifacts/E20_1_DEVELOPMENT_GATE.json').read_text())
    models=['E18','E19','E20.1'];seeds=gate['holdout_seeds']
    paths=[p for p in (BASE/'artifacts/e20_1_confirmation').glob('*.json') if '.kpi.' not in p.name]
    expected={(a,b,s) for a in models for b in models if a!=b for s in seeds}
    observed=set();proof=[]
    for p in sorted(paths):
        r=json.loads(p.read_text());a,b=r['agents'];key=(a,b,r['seed'])
        assert key not in observed;observed.add(key)
        audit=json.loads(p.with_suffix('.kpi.json').read_text())
        assert audit['replay_sha256']==r['replay_sha256']
        assert [s['name'] for s in audit['sides']]==r['agents']
        assert all(x['calls']==719 for x in r['runtime'])
        for i,m in enumerate(r['agents']):
            filename=BUNDLES[m];bundle=ROOT/'submission'/filename
            actual=hashlib.sha256(bundle.read_bytes()).hexdigest()
            recorded=next(v for k,v in r['sources'].items() if k.endswith(filename))
            assert actual==recorded
            if m=='E20.1':assert actual==gate['bundle_sha256'] and r['runtime'][i]['core_errors']==0
            side=audit['sides'][i]
            assert len(side['kpi'])==30 and side['reward']==r['rewards'][i]
            assert all(all(k in d for k,_,_ in FIELDS) for d in side['kpi'])
        proof.append(dict(match=key,replay_sha256=r['replay_sha256'],
            ledger_sha256=hashlib.sha256(p.with_suffix('.kpi.json').read_bytes()).hexdigest()))
    assert observed==expected,(len(observed),len(expected),expected-observed)
    revision=json.loads((BASE/'reports/e20_1/verification_e20_1_confirmation_E20.1.json').read_text())
    assert revision['passed'] and len(revision['cases'])==28
    assert sum(c['opening_parity']==264 for c in revision['cases'])==14
    evaluation=json.loads((BASE/'reports/e20_1/confirmation/evaluation.json').read_text())
    result=dict(technical_verification_passed=True,matches=len(proof),seeds=seeds,
        independent_economic_gate_passed=evaluation['summary']['E20.1']['gate_passed'],
        frozen_candidate_sha256=gate['bundle_sha256'],proof=proof)
    (BASE/'artifacts/E20_1_CONFIRMATION_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='proof'},indent=2))

if __name__=='__main__':main()
