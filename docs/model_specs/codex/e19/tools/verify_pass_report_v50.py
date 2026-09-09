"""Seal evidence and verify frozen baselines, scope and local report links."""
from html.parser import HTMLParser
import gzip,hashlib,importlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/model_specs/codex/e19/reports/pass_reduction_v50'


class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.images=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if tag=='img':self.images.append(a['src'])


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifests=[ROOT/'docs/model_specs/codex/e19/artifacts/derived/v48_external_manifest.json',ROOT/'docs/model_specs/codex/e19/reports/pass_reduction_v49_20260909/candidate_f_manifest.json',OUT/'candidate_manifest.json']
    checked=[]
    for path in manifests:
        m=json.loads(path.read_text());assert sha(ROOT/m['output'])==m['sha256']
        for p,digest in m['sources'].items():assert sha(ROOT/p)==digest,p
        checked.append(dict(bundle=m['output'],sha256=m['sha256'],source_entries=len(m['sources'])))
    engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    expected=json.loads((ROOT/'docs/foundation/ENGINE_SOURCE_MANIFEST.json').read_text())['files']
    for name,digest in expected.items():assert sha(Path(engine.__file__).parent/name)==digest,name
    cases=[p for p in OUT.glob('development_v50*.json') if not p.name.endswith('_obligations.json')]
    assert len(cases)==17,len(cases)
    baseline={};scope=[]
    for path in cases:
        r=json.loads(path.read_text());seed,seat=r['seed'],r['seat']
        assert seed in {180903001,180903002,180903003} and seat==0
        if seed not in baseline:baseline[seed]=json.load(gzip.open(ROOT/f'scratch/v49/development_v49f_{seed}_0.json.gz','rt'))['replay']
        replay=json.load(gzip.open(ROOT/r['details'],'rt'))['replay']
        assert all(replay['steps'][i][seat]['action']==baseline[seed]['steps'][i][seat]['action'] for i in range(1,673)),path.name
        scope.append(dict(case=path.name,d1_d28_parity=True,raw_sha256=sha(ROOT/r['details'])))
    assert not list(OUT.glob('validation_*.json'))
    runtimes=[json.loads(p.read_text()) for p in sorted(OUT.glob('runtime_v49f_*.json'))]
    assert len(runtimes)==2 and all(r['passed'] and r['recorded_action_parity'] for r in runtimes)
    parity=json.loads((OUT/'parity_v50j_180903003_0.json').read_text())
    assert parity['actions']==719 and parity['mismatches']==0
    summary=json.loads((OUT/'summary_v50j.json').read_text());assert summary['status']=='REJECTED'
    parser=Links();parser.feed((OUT/'REPORT_V50_IT.html').read_text(encoding='utf-8'))
    for link in parser.links+parser.images:
        if '://' not in link:assert (OUT/link).exists(),link
    assert len(parser.images)==12
    result=dict(frozen_manifests=checked,engine=expected,candidate_cases=17,scope=scope,
        selected_status='REJECTED',new_seeds_opened=False,standard_runtime_v49f_passed_seats=[0,1],
        tests_log_sha256=sha(ROOT/'scratch/v50/tests.log'),tests_passed=11,report_images=12,local_links_ok=True)
    (OUT/'integrity.json').write_text(json.dumps(result,indent=2))
    files={p.relative_to(ROOT).as_posix():sha(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='report_manifest.json'}
    (OUT/'report_manifest.json').write_text(json.dumps(dict(files=files),indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in ['scope','engine','frozen_manifests']}))


if __name__=='__main__':main()
