"""Freeze E20.9 tomato candidate; preserve E20.8 bundle."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[5];BASE=ROOT/'docs/model_specs/codex/e20'
parent=ROOT/'submission/submission_codex_e20_8_e20v40_calendar_2g.py'
policy=BASE/'tools/operational_calendar_v44.py'
s=parent.read_text(encoding='utf-8').split("MODEL_VERSION=")[0]
s+='\n'+policy.read_text(encoding='utf-8').replace('from docs.model_specs.codex.e20.tools.operational_calendar_goose2 import Agent as Parent','Parent=Agent')
s+="""
MODEL_VERSION='CODEX-E20.9-E20V44-LATE-TOMATO'
_ACTIVE={}
def agent(observation,configuration=None):
    seat=int(observation.get('player',0))
    step=observation['day']*24+observation['hour']
    previous=_ACTIVE.get(seat)
    policy=create_agent({'player_position':seat}) if previous is None or step<=previous[0] else previous[1]
    _ACTIVE[seat]=(step,policy)
    return policy(observation,configuration)
"""
compile(s,'<candidate>','exec');assert '__file__' not in s and 'read_text' not in s
out=ROOT/'submission/submission_codex_e20_9_e20v44_late_tomato.py'
if out.exists():assert out.read_text(encoding='utf-8')==s
else:out.write_text(s,encoding='utf-8')
m={'version':'E20.9 / E20v44','status':'experimental; not submitted','topology':[7,6,1],'animals':{'COW':8,'SHEEP':6,'GOOSE':2},'tomato_sites':[[3,7],[4,8]],'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [parent,policy,Path(__file__)]}}
out.with_suffix('.manifest.json').write_text(json.dumps(m,indent=2),encoding='utf-8');print(out,m['sha256'])
