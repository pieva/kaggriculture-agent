"""Freeze an explicitly selected E20 variant as a standard-library bundle."""
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[5]

def build(variant):
    from docs.model_specs.codex.e20.tools.policy import VARIANTS
    assert variant in VARIANTS
    policy=Path(__file__).with_name('policy.py')
    parent=ROOT/'submission/submission_codex_e18_770_v48_external.py'
    biological=ROOT/'docs/model_specs/codex/e19/tools/biological_plan_770_v48.py'
    routes=ROOT/'docs/model_specs/codex/e19/tools/daily_routes_770_v48.py'
    source=policy.read_text()
    replacements={
        "ROOT=Path(__file__).resolve().parents[5]":"ROOT=None",
        "str(Path(__file__))": "'<e20-embedded>'",
        "runpy.run_path(str(ROOT/'submission/submission_codex_e18_770_v48_external.py'))":"_load_parent()",
        "(ROOT/'submission/submission_codex_e18_770_v48_external.py').read_text()":"_PARENT_SOURCE",
        "(ROOT/'docs/model_specs/codex/e19/tools/biological_plan_770_v48.py').read_text()":"_BIO_SOURCE",
        "(ROOT/'docs/model_specs/codex/e19/tools/daily_routes_770_v48.py').read_text()":"_ROUTE_SOURCE",
    }
    for old,new in replacements.items():
        assert source.count(old)==(2 if old=='str(Path(__file__))' else 1),old
        source=source.replace(old,new)
    assert '.read_text(' not in source
    source='import types\n_PARENT_SOURCE='+repr(parent.read_text())+'\n_BIO_SOURCE='+repr(biological.read_text())+'\n_ROUTE_SOURCE='+repr(routes.read_text())+'''
def _load_parent():
    module=types.ModuleType('_e20_parent')
    module.__file__='/bundle/docs/model_specs/codex/e20/parent.py'
    sys.modules[module.__name__]=module
    exec(compile(_PARENT_SOURCE,module.__file__,'exec'),module.__dict__)
    return module.__dict__
'''+source
    source+='\n_CREATE_VARIANT=create_agent\nSELECTED_VARIANT='+repr(variant)+'''
MODEL_VERSION='CODEX-E20-772-'+SELECTED_VARIANT.upper()
def create_agent(run_context=None):
    return _CREATE_VARIANT(run_context,SELECTED_VARIANT)
_ACTIVE={}
def agent(observation,configuration=None):
    configuration=configuration or {}
    seat=int(observation.get('player',0))
    step=observation['day']*configuration.get('turnsPerDay',24)+observation['hour']
    previous=_ACTIVE.get(seat)
    policy=create_agent({'player_position':seat}) if previous is None or step<=previous[0] else previous[1]
    _ACTIVE[seat]=(step,policy)
    return policy(observation,configuration)
'''
    output=ROOT/f'submission/submission_codex_e20_772_{variant.lower()}_candidate.py'
    assert not output.exists(),'Frozen bundle cannot be overwritten'
    compile(source,str(output),'exec')
    output.write_text(source,encoding='utf-8')
    manifest=dict(variant=variant,parameters=VARIANTS[variant],uploaded=False,status='LOCAL_FROZEN_CANDIDATE',
        sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
        sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [policy,parent,biological,routes,Path(__file__)]})
    output.with_suffix('.manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(output)

if __name__=='__main__':
    sys.path.insert(0,str(ROOT));build(sys.argv[1])
