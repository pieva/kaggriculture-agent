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

def summarize(result):
    counts=Counter(); opportunities=Counter(); feasible=[]
    for event in result['events']:
        reasons=set(); ready=set()
        for preparation in event['preparations']:
            for rejection in preparation['rejections']:
                reason=rejection['reason']
                if reason=='time':
                    reason=('travel_and_work' if rejection['steps']>rejection['remaining'] else
                            'return_reserve' if rejection['return_cost'] else 'procurement_margin')
                counts[reason]+=1; reasons.add(reason)
                if (rejection['reason']=='route_reservation' and rejection['unreserved_steps'] is not None
                    and not event['active_job'] and 20<=event['day']<=29 and event['hour']>=19
                    and all(c[0] in {'FEED','WATER','CARE','HARVEST','COLLECT_FERTILIZER','FERTILIZE'}
                            for c in preparation['commands'])):
                    ready.add(json.dumps([preparation['target'],preparation['commands']]))
        opportunities.update(reasons)
        if ready:
            feasible.append(dict(day=event['day'],hour=event['hour'],worker=event['worker'],
                                 unique_services=[json.loads(s) for s in sorted(ready)]))
    return dict(action_parity=719,pass_total=len(result['events']),rejected_attempt_counts=dict(counts),
                pass_opportunities_with_reason=dict(opportunities),
                late_free_opportunities_with_preparable_service_ignoring_route=feasible,
                note='Reasons overlap within a PASS. Dispatcher attempts repeat. Neither count is a count of avoidable PASS; shadow preparation is not full admission.')

def main():
    path=BASE/'artifacts/e20_1_care/E20v28_E18_180910101.replay.json.gz'
    with gzip.open(path,'rt') as f:r=json.load(f)
    p=create_agent({'player_position':0},'E20v28');c=p.core
    prepare,certificate=c._prepare_steps,c._day_route_certificate
    preparations=[];certificates=[];hours=[]
    def prep(w,t,commands,**kwargs):
        reasons=[]
        def trace(frame,event,value):
            if event!='return' or value is not None:return
            loc=frame.f_locals
            if frame.f_code.co_name=='_prepare_steps':
                if 'return_cost' in loc:
                    reasons.append(dict(reason='time',steps=len(loc['steps']),return_cost=loc['return_cost'],remaining=c.remaining,buy=bool(loc.get('buy'))))
                elif 'free' in loc:
                    item=loc['item']; stock=c.private['shed'].get(item,0)
                    reasons.append(dict(reason='reserved_material' if stock>=loc['n'] else 'missing_material',item=item,stock=stock,free=loc['free'],need=loc['n']))
            elif frame.f_code.co_name=='route_prepare' and not reasons:
                shadow=loc['prepare'](loc['worker'],loc['target'],loc['commands'],**loc['kwargs'])
                reasons.append(dict(reason='route_reservation',unreserved_steps=None if shadow is None else len(shadow)))
        if c.day>=19:sys.setprofile(trace)
        try:value=prepare(w,t,commands,**kwargs)
        finally:sys.setprofile(None)
        if c.day>=19:preparations.append(dict(worker=w,target=t,steps=None if value is None else len(value),commands=commands,rejections=reasons,position=c.positions[w],remaining=c.remaining))
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
    out=BASE/'reports/labor_closing/ADMISSION_REASONS.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(dict(variant='E20v28',seed=180910101,seat=0,action_parity=719,counts=dict(counts),events=hours,note='Only opportunities actually considered by the policy. Rejected preparation does not alone prove a feasible alternative or an avoidable PASS.'),indent=2)+'\n')
    out.with_name('DIAGNOSIS_SUMMARY.json').write_text(json.dumps(summarize(dict(events=hours)),indent=2)+'\n')
    print(json.dumps(dict(counts)))

if __name__=='__main__':main()
