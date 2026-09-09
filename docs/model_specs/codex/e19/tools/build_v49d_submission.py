"""Build candidate in an isolated namespace; never write frozen V48 artifacts."""
import ast
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
TOOLS=Path(__file__).resolve().parent
PREFIX='docs.model_specs.codex.e19.tools.'
OUT=ROOT/'submission/submission_codex_e19_770_v49d_candidate.py'


def build():
    seen={};order=[]
    def visit(name):
        if name in seen:return
        source=(TOOLS/(name+'.py')).read_text(encoding='utf-8');seen[name]=source
        for node in ast.walk(ast.parse(source)):
            if isinstance(node,ast.ImportFrom) and node.module and node.module.startswith(PREFIX):
                visit(node.module[len(PREFIX):])
        order.append(name)
    visit('policy_770_v49d')
    core_path=ROOT/'submission/submission_codex_e19_control_770_v2.py'
    base_path=ROOT/'submission/submission_codex_e18_770_assisted_start_v1_candidate.py'
    core=core_path.read_text(encoding='utf-8');base=base_path.read_text(encoding='utf-8')
    lines=['# V49 candidate. Not published. Standard library only.',
        'import sys as _sys, types as _types',
        '_pkg=_types.ModuleType("_v49dpkg"); _pkg.__path__=[]; _sys.modules["_v49dpkg"]=_pkg',
        '_CORE_SOURCE='+repr(core)]
    for name in order:
        source=seen[name].replace(PREFIX,'_v49dpkg.')
        source=source.replace("source=Path(__file__).resolve().parents[5]/'submission/submission_codex_e19_control_770_v2.py'",'source=None')
        source=source.replace("source.read_text(encoding='utf-8')",'_CORE_SOURCE')
        assert '.read_text(' not in source and '.read_bytes(' not in source,name
        lines.extend(['_m=_types.ModuleType('+repr('_v49dpkg.'+name)+')',
            '_m.__file__='+repr('/bundle/docs/model_specs/codex/e19/tools/'+name+'.py'),
            '_m._CORE_SOURCE=_CORE_SOURCE','_sys.modules[_m.__name__]=_m',
            'setattr(_pkg,'+repr(name)+',_m)',
            'exec(compile('+repr(source)+',_m.__file__,"exec"),_m.__dict__)'])
    lines+=['_base=_types.ModuleType("_v49d_assisted"); _base.__file__="/bundle/assisted.py"',
        'exec(compile('+repr(base)+',_base.__file__,"exec"),_base.__dict__)', '''
MODEL_VERSION='CODEX-E19-770-V49D-CANDIDATE'
def create_agent(run_context=None):
    policy=_base.create_agent(run_context)
    _sys.modules['_v49dpkg.policy_770_v49d'].install(policy.core)
    return policy
_ACTIVE={}
def agent(observation,configuration=None):
    configuration=configuration or {}
    seat=int(observation.get('player',0))
    step=observation['day']*configuration.get('turnsPerDay',24)+observation['hour']
    previous=_ACTIVE.get(seat)
    policy=create_agent({'player_position':seat}) if previous is None or step<=previous[0] else previous[1]
    _ACTIVE[seat]=(step,policy)
    return policy(observation,configuration)
''']
    OUT.write_text('\n'.join(lines),encoding='utf-8')
    sources=[TOOLS/(name+'.py') for name in order]+[core_path,base_path,Path(__file__)]
    manifest=dict(output=OUT.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),
        sources={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
        status='candidate_not_published')
    dest=ROOT/'docs/model_specs/codex/e19/reports/pass_reduction_v49_20260909'
    dest.mkdir(parents=True,exist_ok=True)
    (dest/'candidate_d_manifest.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps(dict(path=str(OUT),sha256=manifest['sha256'],source_count=len(sources))))


if __name__=='__main__':build()
