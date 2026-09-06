"""Supplementary common-random-number diagnostic; NOT an official engine gate.

The stock engine consumes weed RNG draws only for empty tiles, then chooses a
town shop from the same stream. Investment changes the future demand sample even
at the same seed. Here one weed draw is consumed per board coordinate, including
occupied/locked tiles. Eligibility and probability of weed growth are unchanged;
the random schedule and shops are shared across treatments. This is a test-only
in-memory replacement. Never bundle it into an agent or substitute these results
for unmodified-engine/holdout/submission validation.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from unittest.mock import patch

from docs.model_specs.codex.e18.tools.run_e18_31_assignment_gate import gate, run_case


def coordinate_clock_weeds(farm, board_size, weed_chance, rng):
    for y in range(board_size):
        for x in range(board_size):
            draw = rng.random()
            if farm['tiles'][y][x] is None and draw < weed_chance:
                farm['tiles'][y][x] = {'kind':'WEED'}


def run(variant, opponent, seed, seat):
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    with patch.object(engine, '_spawn_weeds', coordinate_clock_weeds):
        result = run_case(variant, opponent, seed, seat)
    result['engine_regime'] = 'SUPPLEMENTARY_COMMON_RANDOM_NUMBERS_NOT_OFFICIAL'
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seeds', nargs='+', type=int, default=[180903001,180903002,180903003,180903004,180903005,180903006,180903007])
    parser.add_argument('--variants', nargs='+', default=['BASELINE','COMBINED'])
    parser.add_argument('--opponents', nargs='+', default=['E18.16'])
    parser.add_argument('--label', required=True)
    args=parser.parse_args()
    assert set(args.seeds) <= set(range(180903001,180903008))
    assert args.label.replace('_','').isalnum()
    output=gate.DERIVED/f'E18_31_CRN_DIAGNOSTIC_{args.label}.json'
    assert not output.exists()
    files=[Path(__file__),Path(__file__).with_name('e18_31_assignment_controller.py')]
    if 'OBLIGATION' in args.variants:
        files.append(Path(__file__).with_name('e18_31_obligation_controller.py'))
    if 'UNIFIED' in args.variants:
        files.extend([Path(__file__).with_name('e18_31_obligation_controller.py'),
                      Path(__file__).with_name('e18_31_unified_investment_controller.py')])
    payload=dict(complete=False,holdout_consumed=False,
        engine_regime='SUPPLEMENTARY_COMMON_RANDOM_NUMBERS_NOT_OFFICIAL',
        description=__doc__,source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        matches=[],failures=[])
    cases=[(v,o,s,0) for v in args.variants for o in args.opponents for s in args.seeds]
    with ProcessPoolExecutor(max_workers=2) as pool:
        pending={pool.submit(run,*c):c for c in cases}
        for future in as_completed(pending):
            try:
                payload['matches'].append(future.result())
            except Exception as exc:
                payload['failures'].append(dict(case=pending[future],error=repr(exc)))
            output.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    payload['complete']=not payload['failures'] and len(payload['matches'])==len(cases)
    output.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    if not payload['complete']:
        raise SystemExit(1)


if __name__=='__main__':
    main()
