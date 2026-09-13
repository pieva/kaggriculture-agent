"""Wheat mass balance and feed economics; no assumed stock provenance."""
import importlib,json,sys
from pathlib import Path
from statistics import mean

ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
OUT=ROOT/'docs/model_specs/codex/e22/reports/top_trigger_pilot_20260913'


def stock(private):return private['shed'].get('WHEAT',0)+sum(i.get('WHEAT',0) for i in private['inventories'])


def main():
    from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit
    engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    cohort=json.loads((OUT/'COHORT.json').read_text(encoding='utf-8'));dest=OUT/'feed_profiles';dest.mkdir(exist_ok=True)
    rows=[];errors=[]
    for g in cohort['games']:
        p=dest/f"{g['submission']}_{g['episode']}.json"
        if p.exists():row=json.loads(p.read_text(encoding='utf-8'));rows.append(row);continue
        r=json.loads((ROOT/g['path']).read_text(encoding='utf-8'));seat=g['seat'];losses=[];i=0
        original=engine._process_market
        def market(states,env):
            nonlocal i
            original(states,env);i+=1
            diff=stock(states[seat].observation.private)-stock(r['steps'][i][seat]['observation']['private'])
            if diff:
                assert diff>0 and i%24==0,(g['episode'],i,diff)
                losses.append(dict(step=i,units=diff))
        engine._process_market=market
        try:ledger=audit(r,seat)
        except AssertionError as exc:
            errors.append(dict(name=g['name'],episode=g['episode'],error=str(exc)))
            print('FEED EXCLUDED',g['name'],g['episode'],str(exc),flush=True)
            continue
        finally:engine._process_market=original
        assert i==719 and ledger['cash_parity_errors']==0
        ds=ledger['daily']
        totals={k:sum(d[field].get(item,0) for d in ds) for k,field,item in [('harvested','harvested','WHEAT'),('bought','bought_units','BUY_PRODUCT:WHEAT'),('sold','sold_units','WHEAT'),('fed','executed_actions','FEED'),('purchase_cash','purchase_cash','BUY_PRODUCT:WHEAT'),('sales_cash','sales_cash','WHEAT'),('seed_cash','purchase_cash','BUY_SEED:WHEAT')]}
        totals.update(initial=stock(r['steps'][0][seat]['observation']['private']),final=stock(r['steps'][-1][seat]['observation']['private']),discarded=sum(x['units'] for x in losses))
        residual=totals['initial']+totals['harvested']+totals['bought']-totals['sold']-totals['fed']-totals['final']-totals['discarded']
        if residual:
            errors.append(dict(name=g['name'],episode=g['episode'],error=f'mass balance residual {residual}',totals=totals))
            print('FEED EXCLUDED',g['name'],g['episode'],'mass balance',residual,flush=True)
            continue
        row=dict(name=g['name'],submission=g['submission'],episode=g['episode'],band=g['band'],rating=g['display_score'],totals=totals,discard_events=losses,daily=ds,cash_parity_errors=ledger['cash_parity_errors'])
        p.write_text(json.dumps(row,separators=(',',':'))+'\n',encoding='utf-8');rows.append(row);print('FEED AUDITED',g['name'],g['episode'],flush=True)
    summary=[]
    for sid in dict.fromkeys(x['submission'] for x in rows):
        gs=[x for x in rows if x['submission']==sid]
        summary.append(dict(name=gs[0]['name'],submission=sid,n=len(gs),mean={k:mean(x['totals'][k] for x in gs) for k in gs[0]['totals']}))
    (OUT/'FEED_SUMMARY.json').write_text(json.dumps(dict(models=summary,n=len(rows),excluded=errors,note='Grain is fungible. Harvested and bought grain cannot be uniquely assigned to FEED without an attribution convention. Avoided purchases and net savings require a counterfactual including forgone sales, work and land costs. Excluded replays have unresolved reconstruction discrepancies; do not use their feed totals.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=True))


if __name__=='__main__':main()
