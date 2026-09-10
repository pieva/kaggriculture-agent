"""H002 paired full-trajectory audit, prices, sale timing and biological gates."""
import csv,gzip,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools.audit_results import run as audit
from docs.model_specs.codex.evolution.tools.sale_events import audit_with_sales
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS
BASE=ROOT/'docs/model_specs/codex/evolution';ART=BASE/'artifacts';OUT=BASE/'reports/H006_FULL'
def read(p):return json.loads(p.read_text())
def main():
    rows=[];sources={};daily_rows=[]
    for target in [0,1]:
        for seed in [180910204,180910206]:
            model='E19'
            cp=ART/'H006_FULL'/f'{model}_{seed}_seat{target}_control.json'
            tp=ART/'H006_FULL'/f'{model}_{seed}_seat{target}_strawberry_first.json';cm,tm=read(cp),read(tp)
            assert cm['source_replay_sha256']==tm['source_replay_sha256'] and cm['engine']==tm['engine']
            for key,value in cm['sources'].items():
                if key.startswith('submission'):assert tm['sources'][key]==value
            assert cm['verification']['suffix_states']==263 and cm['verification']['suffix_action_batches']==263
            assert tm['verification']['suffix_states']==(tm['intervention']['step']-456 if tm['intervention'] else 263)
            conditions={};replays={};audits={}
            for label,p,meta in [('control',cp,cm),('reorder',tp,tm)]:
                sources[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
                assert all(x['calls']==719 and x['core_errors'] in [0,None] for x in meta['runtime'])
                assert all(x['core_errors']==0 for name,x in zip(meta['agents'],meta['runtime']) if name!='E18')
                audit(str(p));k=read(p.with_suffix('.kpi.json'));assert k['replay_sha256']==meta['replay_sha256']
                with gzip.open(p.with_suffix('.replay.json.gz'),'rb') as f:raw=f.read()
                assert hashlib.sha256(raw).hexdigest()==meta['replay_sha256'];r=json.loads(raw)
                assert len(r['steps'])==720 and all(s['status']=='DONE' for s in r['steps'][-1])
                ledger=audit_with_sales(r,target);s=k['sides'][target];replays[label]=r;audits[label]=k
                daily_rows.extend(dict(model=meta['agents'][side],target_seat=target,seat=side,seed=seed,condition=label,day=day,**{key:v[key] for key,_,_ in FIELDS}) for side in [0,1] for day,v in enumerate(k['sides'][side]['kpi'],1))
                sale_path=OUT/f'{model}_{seed}_seat{target}_{label}_sales.json';sale_path.write_text(json.dumps(ledger['sale_events'],indent=2)+'\n')
                windows={}
                for name,end in [('D20',20),('D20-D22',22),('D20-D30',30)]:
                    ds=ledger['daily'][19:end];idx=min(end*24,719);obs=r['steps'][idx][target]['observation'];stock=obs['private']['shed'].get('STRAWBERRY',0)+sum(inv.get('STRAWBERRY',0) for inv in obs['private']['inventories'])
                    units=sum(d['sold_units'].get('STRAWBERRY',0) for d in ds);sales=sum(d['sales_cash'].get('STRAWBERRY',0) for d in ds)
                    cash=obs['farms'][target]['money'];opp=obs['farms'][1-target]['money']
                    windows[name]=dict(cash=cash,opponent_cash=opp,margin=cash-opp,strawberry_units=units,strawberry_sales=sales,strawberry_price=sales/units if units else None,strawberry_stock=stock,sales=sum(sum(d['sales_cash'].values()) for d in ds),purchases=sum(sum(d['purchase_cash'].values()) for d in ds),wages=sum(d['hire_cash'] for d in ds))
                trigger=tm['intervention'];events=[e for e in ledger['sale_events'] if e['item']=='STRAWBERRY' and trigger and e['step']>=trigger['step']+1]
                conditions[label]=dict(windows=windows,losses=len(s['ledger']['animal_escapes']),stress=len(s['crop_starvation']),first_strawberry_sale_at_or_after_trigger=events[0] if events else None)
            a,b=conditions['control'],conditions['reorder'];bio=b['losses']>a['losses'] or b['stress']>a['stress']
            assert tm['intervention']['step']==456 and tm['intervention']['reason']=='reordered'
            selected=next(r for r in read(BASE/'reports/H006/RESULT.json')['evaluation'] if r['model']==model and r['seed']==seed and r['seat']==target and r['opponent']=='E18')
            assert selected['apply']
            immediate=[r['steps'][457][0]['observation']['farms'] for r in [replays['control'],replays['reorder']]]
            assert immediate[1][target]['money']-immediate[0][target]['money']==selected['delta_cash']
            changed_worker_batches=[sum(any(replays['control']['steps'][i][seat]['action'].get(key)!=replays['reorder']['steps'][i][seat]['action'].get(key) for key in ['farmer','hands']) for i in range(457,720)) for seat in [0,1]]
            physical_equal=all({key:value for key,value in replays['control']['steps'][i][0]['observation']['farms'][seat].items() if key!='money'}=={key:value for key,value in replays['reorder']['steps'][i][0]['observation']['farms'][seat].items() if key!='money'} for i in range(457,720) for seat in [0,1])
            services_equal=all(audits['control']['sides'][seat]['ledger']['daily'][d]['executed_actions']==audits['reorder']['sides'][seat]['ledger']['daily'][d]['executed_actions'] for seat in [0,1] for d in range(19,30))
            rows.append(dict(model=model,seed=seed,seat=target,physical_farms_equal=physical_equal,executed_services_equal=services_equal,intervention=tm['intervention'],conditions=conditions,delta_cash=b['windows']['D20-D30']['cash']-a['windows']['D20-D30']['cash'],delta_margin=b['windows']['D20-D30']['margin']-a['windows']['D20-D30']['margin'],biological_regression=bio,decision='NOT_APPLICABLE' if tm['intervention'] is None else 'REJECT_BIOLOGICAL_REGRESSION' if bio else 'DIAGNOSTIC_ONLY',adopted=False))
            rows[-1].update(changed_worker_batches_by_seat=changed_worker_batches,initial_delta_cash=selected['delta_cash'],initial_delta_margin=selected['delta_margin'])
    (OUT/'RESULT.json').write_text(json.dumps(dict(experiment='H006_FULL',distinct_seeds=2,paired_situations=4,rows=rows,metadata_sources_sha256=sources),indent=2)+'\n')
    with (OUT/'daily_22_kpi.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(daily_rows[0]));writer.writeheader();writer.writerows(daily_rows)
    lines=['# H006: verifica fino a D30', '', 'Quattro interventi E19 contro E18, due seed diagnostici gia esposti e due ruoli accoppiati. Quattro controlli nuovi riproducono esattamente 263 transizioni dopo il checkpoint. Forecast ricostruito dalla storia propria e confrontato con le predizioni congelate; avversari liberi di reagire. Nessuna promozione.', '', '| Seed | Ruolo E19 | Delta cassa D30 | Delta margine D30 | Stress controllo/intervento | Fughe controllo/intervento | Fattorie fisiche / servizi identici |','|---|---:|---:|---:|---:|---:|---|']
    for row in rows:
        a,b=[row['conditions'][c] for c in ['control','reorder']]
        lines.append(f"| {row['seed']} | {row['seat']} | {row['delta_cash']:+.0f} | {row['delta_margin']:+.0f} | {a['stress']}/{b['stress']} | {a['losses']}/{b['losses']} | {row['physical_farms_equal']} / {row['executed_services_equal']} |")
    lines+=['', '## Traiettoria economica', '', '| Seed | Ruolo | Finestra | Delta cassa | Delta margine | Delta incassi fragole | Delta altre vendite | Delta acquisti | Delta salari | Delta unita fragole | Delta stock fragole |','|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for row in rows:
        for window in ['D20','D20-D22','D20-D30']:
            a,b=[row['conditions'][c]['windows'][window] for c in ['control','reorder']]
            ds=b['strawberry_sales']-a['strawberry_sales']
            vals=[b[k]-a[k] for k in ['cash','margin']]+[ds,b['sales']-a['sales']-ds]+[b[k]-a[k] for k in ['purchases','wages','strawberry_units','strawberry_stock']]
            lines.append('| '+str(row['seed'])+' | '+str(row['seat'])+' | '+window+' | '+' | '.join(f'{v:+.0f}' for v in vals)+' |')
    index={(r['seed'],r['target_seat'],r['seat'],r['condition'],r['day']):r for r in daily_rows}
    trajectory=[]
    for row in rows:
        for side in [0,1]:
            for day in range(1,31):
                a,b=[index[(row['seed'],row['seat'],side,c,day)] for c in ['control','reorder']]
                trajectory.append(dict(seed=row['seed'],target_seat=row['seat'],seat=side,model=a['model'],day=day,**{key:b[key]-a[key] for key,_,_ in FIELDS}))
    with (OUT/'delta_22_kpi.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(trajectory[0]));w.writeheader();w.writerows(trajectory)
    lines+=['', '## I 22 KPI: massima differenza assoluta giornaliera D20-D30', '', 'La tabella copre tutte e quattro le coppie; le serie complete, incluse entrambe le condizioni, sono nei CSV. Un massimo nullo significa traiettoria giornaliera identica nel campione.', '', '| KPI | E19 | E18 |','|---|---:|---:|']
    for key,label,_ in FIELDS:
        values=[max(abs(r[key]) for r in trajectory if r['model']==m and r['day']>=20) for m in ['E19','E18']]
        lines.append(f'| {label} ({key}) | {values[0]:.4g} | {values[1]:.4g} |')
    lines+=['', 'Tutti gli otto rami: 719 chiamate per agente, DONE/DONE e zero errori nei core strumentati. I ruoli non sono repliche indipendenti; questi seed sono gia esposti. Nessuna conclusione sulla generalizzazione e nessuna modifica di E18, E19 o E20.1.', '', '[Protocollo](../../H006_CONTINUATION_PROTOCOL.md) · [Risultati](RESULT.json) · [22 KPI completi](daily_22_kpi.csv) · [Differenze giornaliere](delta_22_kpi.csv).']
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print([(r['seed'],r['seat'],r['delta_cash'],r['delta_margin']) for r in rows])

if __name__=='__main__':main()
