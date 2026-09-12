"""Package the relocated operational calendar with no runtime filesystem use."""
from pathlib import Path
import json,hashlib,zlib,base64
ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'docs/model_specs/codex/e20'
sources=[BASE/'tools/operational_calendar_base.py',BASE/'tools/operational_calendar_goose2.py']
data={n:json.loads((BASE/f'configs/e20v40/{n}.json').read_text(encoding='utf-8')) for n in ['PLAN_772','PLAN_NATIVE','PROGRAM']}
source=sources[0].read_text(encoding='utf-8').replace('from pathlib import Path\n','').replace('BASE=Path(__file__).resolve().parents[1]','')
source=source.replace("json.loads((BASE/'configs/e20v40'/('PLAN_772.json' if adapt else 'PLAN_NATIVE.json')).read_text(encoding='utf-8'))","deepcopy(_DATA['PLAN_772' if adapt else 'PLAN_NATIVE'])")
source=source.replace("json.loads((BASE/'configs/e20v40/PROGRAM.json').read_text(encoding='utf-8'))","_DATA['PROGRAM']")
source=source.replace("json.loads((BASE/'configs/e20v40/PLAN_NATIVE.json').read_text(encoding='utf-8'))","_DATA['PLAN_NATIVE']")
assert 'read_text' not in source and '__file__' not in source
sub=sources[1].read_text(encoding='utf-8').replace('from docs.model_specs.codex.e20.tools.operational_calendar_base import Agent as BaseAgent','BaseAgent=Agent')
packed=base64.b85encode(zlib.compress(json.dumps(data,separators=(',',':')).encode(),9)).decode()
source='import base64,zlib,json\n_DATA=json.loads(zlib.decompress(base64.b85decode('+repr(packed)+')))\n'+source+'\n'+sub+'''
MODEL_VERSION='CODEX-E20.8-E20V40-COMMON-CALENDAR-2G'
_ACTIVE={}
def agent(observation,configuration=None):
    seat=int(observation.get('player',0))
    step=observation['day']*24+observation['hour']
    previous=_ACTIVE.get(seat)
    policy=create_agent({'player_position':seat}) if previous is None or step<=previous[0] else previous[1]
    _ACTIVE[seat]=(step,policy)
    return policy(observation,configuration)
'''
compile(source,'<kaggle-exec>','exec')
out=ROOT/'submission/submission_codex_e20_8_e20v40_calendar_2g.py'
if out.exists():assert out.read_text(encoding='utf-8')==source
else:out.write_text(source,encoding='utf-8')
sources += list((BASE/'configs/e20v40').glob('*.json'))+[Path(__file__)]
manifest={'version':'E20.8 / E20v40','origin':'E21 operational772_goose2_v2; relocated without strategy changes','mix':{'COW':8,'SHEEP':6,'GOOSE':2},'pasture_topology':[7,6,1],'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
out.with_suffix('.manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(out,manifest['sha256'])
