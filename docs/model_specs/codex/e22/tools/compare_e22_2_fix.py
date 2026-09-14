"""Expose the same 14 seed/seat cases used to select E22.2; no reserved seeds."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from docs.model_specs.codex.e22.tools import compare_q0_pastures as suite

suite.CAND = ROOT / 'submission/submission_codex_e22_2_fix_v1.py'
suite.OUT = ROOT / 'docs/model_specs/codex/e22/reports/e22_2_fix_v1/direct'
suite.ART = ROOT / 'docs/model_specs/codex/e22/artifacts/e22_2_fix_v1/direct'
suite.INTERVENTION = 'E22.2 bug fixes: finance missing hires, recover D2 feed, remove weeds and retry planting, use idle service slots, avoid shed overflow, deliver and sell final fertilizer.'

if __name__ == '__main__':
    # The original seven confirmation seeds remain unconsumed.
    if '--phase' in sys.argv or '--confirmation' in sys.argv:
        raise SystemExit('This regression suite uses exposed seeds only.')
    suite.main()
