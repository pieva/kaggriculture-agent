"""Require complete paired development and standalone parity before holdout runs."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'docs/model_specs/codex/e20'

def main():
    evaluation=BASE/'reports/e20_1/development/evaluation.json'
    verification=BASE/'reports/e20_1/verification_e20_1_care_E20v28.json'
    e=json.loads(evaluation.read_text());v=json.loads(verification.read_text())
    protocol=json.loads((BASE/'E20_1_PROTOCOL.json').read_text())
    frozen=protocol['frozen_for_role_swap'];bundle=ROOT/frozen['file']
    assert hashlib.sha256(bundle.read_bytes()).hexdigest()==frozen['sha256']==v['bundle_sha256']
    assert e['complete_both_seats'] and e['summary']['E20v28']['gate_passed']
    assert set(e['expected_seeds'])==set(protocol['development_seeds'])
    assert len(v['cases'])==20 and v['passed']
    assert sum(c['bundle_action_parity']==719 for c in v['cases'])>=4
    result=dict(passed=True,variant='E20v28',bundle_sha256=frozen['sha256'],
        metrics=e['summary']['E20v28'],control=e['summary']['E19'],
        evidence={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [evaluation,verification]},
        holdout_seeds=protocol['confirmation_seeds_reserved_before_results'])
    (BASE/'artifacts/E20_1_DEVELOPMENT_GATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
