"""Audit frozen external replays and record both players' unit market settlements."""
import csv, hashlib, importlib, json, sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
OUT=ROOT/'docs/model_specs/codex/e20/reports/external_e20_8_20260913'
from docs.model_specs.codex.e20.tools.analyze_first_external import profile

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')

def trace_profile(r,seat):
    engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    old_commit,old_market=engine._commit_unit,engine._process_market
    events=[];batches=[];context={};idx=0
    def commit(op,item,price,farm,private,market,capacity=100):
        ok=old_commit(op,item,price,farm,private,market,capacity)
        if ok:
            player=next(i for i,f in enumerate(context['farms']) if f is farm)
            events.append(dict(step=context['step'],day=context['day'],hour=context['hour'],seat=player,op=op,product=item,price=price))
        return ok
    def market(states,env):
        nonlocal idx
        idx+=1;previous=r['steps'][idx-1][0]['observation'];recorded=r['steps'][idx][0]['observation']
        context.update(step=idx,day=previous['day']+1,hour=previous['hour']+1,farms=states[0].observation.farms)
        start=len(events);m=states[0].observation.market
        pre=deepcopy(m);old_market(states,env);post=deepcopy(m)
        states[0].observation.town=deepcopy(previous['town'])
        engine._town_consume(env,states,previous['day']*24+previous['hour'])
        assert m['prices']==recorded['market']['prices'],('price parity',idx)
        assert m['inventory']==recorded['market']['inventory'],('inventory parity',idx)
        for product in pre['prices']:
            ev=[e for e in events[start:] if e['product']==product]
            row=dict(step=idx,day=previous['day']+1,hour=previous['hour']+1,product=product,
                price_before=pre['prices'][product],price_after_trades=post['prices'][product],price_after_town=m['prices'][product],
                inventory_before=pre['inventory'][product],inventory_after_trades=post['inventory'][product],inventory_after_town=m['inventory'][product],
                town_consumption=post['inventory'][product]-m['inventory'][product])
            for label,player in [('own',seat),('opponent',1-seat)]:
                sales=[e for e in ev if e['seat']==player and e['op']=='SELL']
                buys=[e for e in ev if e['seat']==player and e['op']=='BUY_PRODUCT']
                row.update({label+'_sold':len(sales),label+'_revenue':sum(e['price'] for e in sales),label+'_bought':len(buys),label+'_floor_sales':sum(e['price']==1 for e in sales)})
            delta=sum(row[k+'_sold']-row[k+'_floor_sales']-row[k+'_bought'] for k in ['own','opponent'])
            assert row['inventory_before']+delta==row['inventory_after_trades']
            batches.append(row)
    engine._commit_unit,engine._process_market=commit,market
    try:s=profile(r,seat)
    finally:engine._commit_unit,engine._process_market=old_commit,old_market
    assert idx==719
    for day in s['ledger']['daily']:
        for product,n in day['sold_units'].items():
            sales=[e for e in events if e['day']==day['day'] and e['seat']==seat and e['op']=='SELL' and e['product']==product]
            assert len(sales)==n and sum(e['price'] for e in sales)==day['sales_cash'][product]
    return s,events,batches

def main():
    inv=read(OUT/'INVENTORY.json');dest=OUT/'profiles';dest.mkdir(exist_ok=True)
    errors=[]
    for g in inv['models']['E20.8']['games']:
        p=dest/f"{g['episode']}.json"
        if p.exists():
            assert read(p)['sha256']==g['sha256'];continue
        try:
            assert g['complete'] and not g['missing_observation_fields']
            raw=(ROOT/g['raw_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==g['sha256'];r=json.loads(raw)
            own,events,batches=trace_profile(r,g['seat']);opp=profile(r,1-g['seat'])
            for side in [own,opp]:assert side['ledger']['cash_parity_errors']==0
            save(p,dict(**g,own=own,opponent=opp,market=batches))
            with (dest/f"{g['episode']}_transactions.csv").open('w',newline='',encoding='utf-8') as f:
                w=csv.DictWriter(f,fieldnames=list(events[0]));w.writeheader();w.writerows(events)
            print('VERIFIED',g['episode'],own['reward'],opp['reward'],len(events),flush=True)
        except Exception as exc:
            import traceback
            errors.append(dict(episode=g['episode'],error=str(exc),trace=traceback.format_exc()));print('ERROR',errors[-1],flush=True)
            break
    save(OUT/'AUDIT_ERRORS.json',errors)
    if errors:raise RuntimeError('Audit stopped; inspect AUDIT_ERRORS.json')

if __name__=='__main__':main()
