"""Package the common operational 774 plan without filesystem access."""
from pathlib import Path
import json,zlib,base64,hashlib
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[3]
out=BASE/'reports/operational774_v1'
data={n:json.loads((out/(n+'.json')).read_text(encoding='utf-8')) for n in ['PLAN_774','PLAN_NATIVE','PROGRAM']}
s=(BASE/'operational774_v1_policy.py').read_text(encoding='utf-8').replace('from pathlib import Path\n','').replace('BASE=Path(__file__).resolve().parent','')
s=s.replace("json.loads((BASE/'reports/operational774_v1'/('PLAN_774.json' if adapt else 'PLAN_NATIVE.json')).read_text(encoding='utf-8'))","deepcopy(_DATA['PLAN_774' if adapt else 'PLAN_NATIVE'])")
for name in ['PROGRAM','PLAN_NATIVE']:
 s=s.replace("json.loads((BASE/'reports/operational774_v1/"+name+".json').read_text(encoding='utf-8'))","_DATA['"+name+"']")
assert '__file__' not in s and 'read_text' not in s
packed=base64.b85encode(zlib.compress(json.dumps(data,separators=(',',':')).encode(),9)).decode()
s='import base64,zlib,json\n_DATA=json.loads(zlib.decompress(base64.b85decode('+repr(packed)+')))\n'+s
s+="""
MODEL_VERSION='CODEX-E21-COMMON774-V1'
_ACTIVE={}
def agent(observation,configuration=None):
 seat=int(observation.get('player',0));step=observation['day']*24+observation['hour'];previous=_ACTIVE.get(seat)
 policy=create_agent({'player_position':seat}) if previous is None or step<=previous[0] else previous[1]
 _ACTIVE[seat]=(step,policy)
 return policy(observation,configuration)
"""
compile(s,'<standalone>','exec')
p=ROOT/'submission/submission_codex_e21_common774_v1.py'
if p.exists():assert p.read_text(encoding='utf-8')==s
else:p.write_text(s,encoding='utf-8')
p.with_suffix('.manifest.json').write_text(json.dumps({'version':'E21-COMMON774-V1','status':'local candidate, not submitted','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sources':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in [BASE/'operational774_v1_policy.py',BASE/'adapt_operational774_v1.py']+list(out.glob('PLAN*.json'))+[out/'PROGRAM.json']}},indent=2),encoding='utf-8');print(p)
