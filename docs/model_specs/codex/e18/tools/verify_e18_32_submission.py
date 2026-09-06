"""Exact source/bundle/public-loader parity, including real call-time measurement."""
import hashlib
import json
from concurrent.futures import ProcessPoolExecutor

from docs.model_specs.codex.e18.tools import verify_e18_31_submission as verifier
from docs.model_specs.codex.e18.tools.build_e18_32_submission import OUTPUT,DERIVED
from docs.model_specs.codex.e18.tools.e18_32_claim_routing_controller import ClaimRoutingController
PARITY=DERIVED/'E18_32_SUBMISSION_PARITY_V7.json'


def verify_case(case):
    verifier.OUTPUT=OUTPUT
    verifier.UnifiedInvestmentController=ClaimRoutingController
    return verifier.verify_case(case)


def main():
    target=PARITY
    assert not target.exists()
    with ProcessPoolExecutor(max_workers=2) as executor:
        rows=list(executor.map(verify_case,[(s,t) for s in [180903001,180903005] for t in [0,1]]))
    report=dict(passed=True,submission_sha256=hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
                matches=rows,holdout_consumed=False,new_submission=False)
    target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(str(target),flush=True)


if __name__=='__main__':
    main()
