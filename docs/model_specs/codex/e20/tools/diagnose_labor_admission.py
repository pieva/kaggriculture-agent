"""Observe actual preparation/certificate decisions without changing actions."""
import gzip,json,sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools.policy import create_agent
from docs.model_specs.codex.e20.tools.verify_revision import observation_at
BASE=ROOT/'docs/model_specs/codex/e20'

def main():
    path=BASE/'artifacts/e20_1_care/E20v28_E18_180910101.replay.json.gz'
    with gzip.open(path,'rt') as f:r=json.load(f)
    p=create_agent({'player_position':0},'E20v28');c=p.core
    prepare,certificate=c._prepare_steps,c._day_route_certificate
    preparations=[];certificates=[];hours=[]
    def prep(w,t,commands,**kwargs):
        value=prepare(w,t,commands,**kwargs)
        if c.day>=19:preparations.append(dict(worker=w,target=t,steps=None if value is None else len(value),commands=commands))
        return value
    def cert(w,job,services=None):
        value=certificate(w,job,services)
        if c.day>=19:certificates.append(dict(worker=w,target=job['target'],accepted=bool(value)))
        return value
    c._prepare_steps=prep;c._day_route_certificate=cert
    counts=Counter()
    for i in range(1,720):
        preparations.clear();certificates.clear()
        obs=observation_at(r,i-1,0);a=p(obs,r['configuration'])
        assert a==r['steps'][i][0]['action'],i
        if obs['day']<19:continue
        commands=[a.get('farmer',['PASS']),*a.get('hands',[])]
        for w,cmd in enumerate(commands):
            if not cmd or cmd[0]!='PASS':continue
            preps=[x for x in preparations if x['worker']==w]
            certs=[x for x in certificates if x['worker']==w]
            job=c.active.get(w)
            category=('active_job_waiting' if job else 'no_prepare_attempt' if not preps else 'all_prepare_rejected' if all(x['steps'] is None for x in preps) else 'prepared_but_no_assignment')
            counts[category]+=1
            hours.append(dict(day=obs['day']+1,hour=obs['hour']+1,worker=w,category=category,active_job=deepcopy(job),inventory=dict(c.private['inventories'][w]),shed=dict(c.private['shed']),preparations=preps,certificates=certs,queue=c.daily_route_state.get('remaining',{}).get(str(w),[])))
    out=BASE/'reports/labor_transfer/ADMISSION_DIAGNOSTIC.json'
    out.write_text(json.dumps(dict(variant='E20v28',seed=180910101,seat=0,action_parity=719,counts=dict(counts),events=hours,note='Only opportunities actually considered by the policy. Rejected preparation does not alone prove a feasible alternative or an avoidable PASS.'),indent=2)+'\n')
    print(json.dumps(dict(counts)))

if __name__=='__main__':main()
