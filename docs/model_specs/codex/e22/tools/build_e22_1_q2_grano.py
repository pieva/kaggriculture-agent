"""Freeze the tested terminal wheat succession in a standalone E22.1 bundle."""
import base64
import copy
import hashlib
import json
import zlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'submission/submission_codex_e22_1_pollai.py'
DEST=ROOT/'submission/submission_codex_e22_1_q2_grano_v1.py'
OUT=ROOT/'docs/model_specs/codex/e22/reports/e22_1_q2_grano_v1'


def main():
    source=BASE.read_bytes()
    assert hashlib.sha256(source).hexdigest()=='f32ac78b8c220a21da8a9e71fb5c2e7a652298adfae53107beda5517d59a191d'
    ns={};exec(source,ns);old=ns['_PLAN'];plan=copy.deepcopy(old)
    plan[654]['market'].append(['BUY_SEED','WHEAT',1])
    sequence=[['PLANT','WHEAT'],['WATER']]+[old[648+h-1]['hands'][9] for h in range(8,25) if h not in (10,15)]
    for h,cmd in enumerate(sequence,8):plan[648+h-1]['hands'][9]=copy.deepcopy(cmd)
    plan[676]['hands'][5]=['WATER']
    sequence=[]
    for h in range(3,24):
        if h in (5,11,22,23):continue
        sequence.append(old[696+h-1]['hands'][9])
        if h==8:sequence.extend([['WEST'],['WATER'],['HARVEST'],['EAST']])
    for h,cmd in enumerate(sequence,3):plan[696+h-1]['hands'][9]=copy.deepcopy(cmd)
    encoded=base64.b64encode(zlib.compress(json.dumps(plan,separators=(',',':')).encode(),9)).decode()
    text='''"""E22.1 Q2 Grano v1: three Q0 geese, 8 cows and 6 sheep.
Replace the empty late Q2 coop with D28 wheat, harvested and sold D30.
Frozen schedule uses current day/hour only. No replay files or future data.
"""
import base64,zlib,json,copy
_PLAN=json.loads(zlib.decompress(base64.b64decode('''+repr(encoded)+''')))
class Agent:
 def __init__(self,context=None):pass
 def __call__(self,obs,cfg=None):
  i=int(obs['day'])*24+int(obs['hour'])
  return copy.deepcopy(_PLAN[i]) if 0<=i<len(_PLAN) else {'farmer':['PASS'],'hands':[],'market':[]}
def create_agent(context=None):return Agent(context)
_AGENT=Agent()
def agent(observation,configuration=None):
 return _AGENT(observation,configuration)
'''
    DEST.write_text(text,encoding='utf-8')
    OUT.mkdir(parents=True,exist_ok=True)
    tested=json.loads((OUT.parent/'e22_1_q2_coop_20260914/CROP_COUNTERFACTUALS.json').read_text())
    cohort=json.loads((OUT.parent/'external_e22_2_20260914/COHORT.json').read_text())
    changed=[i for i in range(719) if old[i]!=plan[i]]
    calls=0
    for r in tested:
        g=next(g for g in cohort if g['episode']==r['episode']);game=json.loads((ROOT/g['path']).read_text())
        overrides={(a['day']-1)*24+a['hour']-1:a['action'] for a in r['arms'][1]['changes']}
        for i in range(719):
            assert plan[i]==overrides.get(i,game['steps'][i+1][r['seat']]['action'])
            calls+=1
    fresh={};exec(DEST.read_text(),fresh)
    assert fresh['agent']({'day':27,'hour':7})==plan[655]
    response=fresh['agent']({'day':27,'hour':7});response['hands'][9]=['PASS']
    assert fresh['agent']({'day':27,'hour':7})==plan[655]
    assert old[:648]==plan[:648]
    result=dict(version='E22.1 Q2 Grano v1',base_sha256=hashlib.sha256(source).hexdigest(),sha256=hashlib.sha256(DEST.read_bytes()).hexdigest(),bytes=DEST.stat().st_size,plan_steps=len(plan),changed_steps=changed,diagnostic_action_parity=calls,independent_return_copy=True,no_file_dependency=True,entrypoint='agent')
    (OUT/'BUILD.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
