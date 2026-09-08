import ast,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];B=ROOT/'docs/model_specs/codex/e19/tools';OUT=ROOT/'submission/submission_codex_e18_770_v29_external.py'
prefix='docs.model_specs.codex.e19.tools.';seen={};order=[]
def visit(name):
 if name in seen:return
 s=(B/(name+'.py')).read_text(encoding='utf-8');seen[name]=s
 for n in ast.walk(ast.parse(s)):
  if isinstance(n,ast.ImportFrom) and n.module and n.module.startswith(prefix):visit(n.module[len(prefix):])
 order.append(name)
visit('daily_route_scheduler_770_v29')
core=(ROOT/'submission/submission_codex_e19_control_770_v2.py').read_text(encoding='utf-8')
base=(ROOT/'submission/submission_codex_e18_770_assisted_start_v1_candidate.py').read_text(encoding='utf-8')
lines=['# V29 external benchmark. Frozen policy; standard library bundle.','import sys as _sys, types as _types', '_pkg=_types.ModuleType("_v29pkg"); _pkg.__path__=[]; _sys.modules["_v29pkg"]=_pkg', '_CORE_SOURCE='+repr(core)]
for name in order:
 s=seen[name].replace(prefix,'_v29pkg.')
 s=s.replace("source=Path(__file__).resolve().parents[5]/'submission/submission_codex_e19_control_770_v2.py'",'source=None')
 s=s.replace("source.read_text(encoding='utf-8')",'_CORE_SOURCE')
 assert '.read_text(' not in s and '.read_bytes(' not in s,name
 lines.extend(['_m=_types.ModuleType('+repr('_v29pkg.'+name)+')', '_m.__file__='+repr('/bundle/docs/model_specs/codex/e19/tools/'+name+'.py'), '_m._CORE_SOURCE=_CORE_SOURCE','_sys.modules[_m.__name__]=_m','setattr(_pkg,'+repr(name)+',_m)','exec(compile('+repr(s)+',_m.__file__,"exec"),_m.__dict__)'])
lines+=['_base=_types.ModuleType("_v29_assisted"); _base.__file__="/bundle/assisted.py"','exec(compile('+repr(base)+',_base.__file__,"exec"),_base.__dict__)', '''
MODEL_VERSION='CODEX-E18-770-V29-EXTERNAL'
def create_agent(run_context=None):
    policy=_base.create_agent(run_context)
    _sys.modules['_v29pkg.daily_route_scheduler_770_v29'].install(policy.core)
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
manifest=dict(output=str(OUT.relative_to(ROOT)),sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),sources={str((B/(n+'.py')).relative_to(ROOT)):hashlib.sha256((B/(n+'.py')).read_bytes()).hexdigest() for n in order})
(ROOT/'docs/model_specs/codex/e19/artifacts/derived/v29_external_manifest.json').write_text(json.dumps(manifest,indent=2))
print(OUT,len(OUT.read_bytes()),len(order))
