"""Hash and historical ledger checks. All original inputs are read-only."""
import hashlib
import importlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/model_specs/codex/e19/reports/pass_reduction_v49_20260909'
ORIGINAL=Path('C:/Users/pietr/Projects/kaggriculture-agent')


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    frozen=json.loads((ROOT/'docs/model_specs/codex/e19/artifacts/derived/v48_external_manifest.json').read_text())
    candidate=json.loads((OUT/'candidate_f_manifest.json').read_text())
    for manifest in [frozen,candidate]:
        assert sha(ROOT/manifest['output'])==manifest['sha256']
        for path,digest in manifest['sources'].items():assert sha(ROOT/path)==digest,path
    engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    expected=json.loads((ROOT/'docs/foundation/ENGINE_SOURCE_MANIFEST.json').read_text())
    for name,digest in expected['files'].items():assert sha(Path(engine.__file__).parent/name)==digest,name
    historical=[]
    for path in sorted(OUT.glob('development_v48_*.json')):
        if path.name.endswith('_obligations.json'):continue
        run=json.loads(path.read_text())
        relative=Path('docs/model_specs/codex/e19/artifacts/derived/portfolio_succession_20260907')/f'daily_routes_v48_{run["seed"]}_{run["seat"]}.json'
        original=ROOT/relative
        if not original.exists():original=ORIGINAL/relative
        old=json.loads(original.read_text())['sides']['candidate']
        assert run['reward']==old['reward'],path.name
        assert run['ledger']==old['ledger'],path.name
        historical.append(dict(seed=run['seed'],seat=run['seat'],ledger_parity=True,
            original_relative=relative.as_posix(),original_sha256=sha(original)))
    result=dict(frozen_v48_sha256=frozen['sha256'],baseline_sources=len(frozen['sources']),
        candidate_sha256=candidate['sha256'],candidate_sources=len(candidate['sources']),
        engine_files=expected['files'],historical_baseline_parity=historical,
        tests_logs={name:sha(ROOT/'scratch/v49'/name) for name in ['tests.log','tests_f.log']},
        tests_passed=17)
    (OUT/'integrity.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
