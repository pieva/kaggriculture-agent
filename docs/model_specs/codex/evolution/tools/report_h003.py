"""H002 paired full-trajectory audit, prices, sale timing and biological gates."""
import csv,gzip,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools.audit_results import run as audit
from docs.model_specs.codex.evolution.tools.sale_events import audit_with_sales
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS
BASE=ROOT/'docs/model_specs/codex/evolution';ART=BASE/'artifacts';OUT=BASE/'reports/H003'
def read(p):return json.loads(p.read_text())
def main():
    rows=[];sources={};daily_rows=[]
    for model in ['E18','E19','E20.1']:
        for seed in [180910201,180910202]:
            cp=ART/'H001'/f'{model}_control.json' if seed==180910201 else ART/'H002'/f'{model}_{seed}_control.json'
            tp=cp if model=='E18' else ART/'H003'/f'{model}_{seed}_strawberry_first.json';cm,tm=read(cp),read(tp)
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
                ledger=audit_with_sales(r,0);s=k['sides'][0];replays[label]=r;audits[label]=k
                daily_rows.extend(dict(model=model,seed=seed,condition=label,day=day,**{key:v[key] for key,_,_ in FIELDS}) for day,v in enumerate(s['kpi'],1))
                sale_path=OUT/f'{model}_{seed}_{label}_sales.json';sale_path.write_text(json.dumps(ledger['sale_events'],indent=2)+'\n')
                windows={}
                for name,end in [('D20',20),('D20-D22',22),('D20-D30',30)]:
                    ds=ledger['daily'][19:end];idx=min(end*24,719);obs=r['steps'][idx][0]['observation'];stock=obs['private']['shed'].get('STRAWBERRY',0)+sum(inv.get('STRAWBERRY',0) for inv in obs['private']['inventories'])
                    units=sum(d['sold_units'].get('STRAWBERRY',0) for d in ds);sales=sum(d['sales_cash'].get('STRAWBERRY',0) for d in ds)
                    cash=obs['farms'][0]['money'];opp=obs['farms'][1]['money']
                    windows[name]=dict(cash=cash,opponent_cash=opp,margin=cash-opp,strawberry_units=units,strawberry_sales=sales,strawberry_price=sales/units if units else None,strawberry_stock=stock,sales=sum(sum(d['sales_cash'].values()) for d in ds),purchases=sum(sum(d['purchase_cash'].values()) for d in ds),wages=sum(d['hire_cash'] for d in ds))
                trigger=tm['intervention'];events=[e for e in ledger['sale_events'] if e['item']=='STRAWBERRY' and trigger and e['step']>=trigger['step']+1]
                conditions[label]=dict(windows=windows,losses=len(s['ledger']['animal_escapes']),stress=len(s['crop_starvation']),first_strawberry_sale_at_or_after_trigger=events[0] if events else None)
            a,b=conditions['control'],conditions['reorder'];bio=b['losses']>a['losses'] or b['stress']>a['stress']
            physical_equal=all({key:value for key,value in replays['control']['steps'][i][0]['observation']['farms'][seat].items() if key!='money'}=={key:value for key,value in replays['reorder']['steps'][i][0]['observation']['farms'][seat].items() if key!='money'} for i in range(457,720) for seat in [0,1])
            services_equal=all(audits['control']['sides'][seat]['ledger']['daily'][d]['executed_actions']==audits['reorder']['sides'][seat]['ledger']['daily'][d]['executed_actions'] for seat in [0,1] for d in range(19,30))
            rows.append(dict(model=model,seed=seed,physical_farms_equal=physical_equal,executed_services_equal=services_equal,intervention=tm['intervention'],conditions=conditions,delta_cash=b['windows']['D20-D30']['cash']-a['windows']['D20-D30']['cash'],delta_margin=b['windows']['D20-D30']['margin']-a['windows']['D20-D30']['margin'],biological_regression=bio,decision='NOT_APPLICABLE' if tm['intervention'] is None else 'REJECT_BIOLOGICAL_REGRESSION' if bio else 'DIAGNOSTIC_ONLY',adopted=False))
    (OUT/'RESULT.json').write_text(json.dumps(dict(experiment='H003',distinct_seeds=2,paired_situations=6,rows=rows,metadata_sources_sha256=sources),indent=2)+'\n')
    with (OUT/'daily_22_kpi.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(daily_rows[0]));writer.writeheader();writer.writerows(daily_rows)
    scan=read(OUT/'ONE_STEP.json')['rows']
    lines=['# H003: priorita delle fragole fra le vendite correnti','', 'Condizione osservabile: esiste una vendita di fragole preceduta soltanto da altre vendite. Si porta al primo posto una sola volta in D20, senza cambiare quantita, ora o comandi dei lavoratori. La regola non usa gli ordini contemporanei o futuri dell avversario.', '', '## Effetto immediato sul campione diagnostico', '', '42 transizioni originali riprodotte esattamente, 84 decisioni dei due giocatori. Azione avversaria originale fissata solo nella transizione simultanea; nessun uso dell azione avversaria per scegliere la modifica. Media sui soli casi applicabili. Tutti i sette seed sono gia esposti.', '', '| Modello | Applicabili | Delta cassa medio | Positivi / nulli / negativi |','|---|---:|---:|---|']
    for model in ['E18','E19','E20.1']:
        rr=[r for r in scan if r['model']==model and r['reason']=='reordered']
        average=sum(r['delta_cash'] for r in rr)/len(rr) if rr else 0
        lines.append(f'| {model} | {len(rr)}/28 | {average:+.1f} | {sum(r["delta_cash"]>0 for r in rr)} / {sum(r["delta_cash"]==0 for r in rr)} / {sum(r["delta_cash"]<0 for r in rr)} |')
    lines+=['', '## Effetto immediato per avversario', '', '| Modello | Avversario | Casi | Delta cassa medio | Positivi | Negativi |','|---|---|---:|---:|---:|---:|']
    for model in ['E19','E20.1']:
        for opponent in ['E18','E19','E20.1']:
            rr=[r for r in scan if r['model']==model and r['opponent']==opponent and r['reason']=='reordered']
            if rr:lines.append(f'| {model} | {opponent} | {len(rr)} | {sum(r["delta_cash"] for r in rr)/len(rr):+.1f} | {sum(r["delta_cash"]>0 for r in rr)} | {sum(r["delta_cash"]<0 for r in rr)} |')
    lines+=['', 'Contro E18 tutti i casi applicabili migliorano la transazione corrente; i negativi emergono negli scontri E19/E20.1. E una segmentazione diagnostica successiva agli esiti, non una condizione da inserire nella policy. Identita del modello avversario e sua azione contemporanea non sono input della regola. Prima di una regola adattiva occorre verificare se il suo comportamento di vendita sia inferibile dalla storia osservabile del mercato.', '', '## Prosecuzioni complete: due seed, ruolo0', '', 'E18 e gia al primo posto nei due casi: il controllo viene riusato come esito non applicabile, non contato come nuova simulazione. Quattro trattamenti nuovi, sei controlli verificati e riusati con confronto degli hash. Gli avversari reagiscono in tutte le prosecuzioni complete.', '', '| Modello | Seed | Delta cassa | Delta margine | Stress controllo/intervento | Fughe controllo/intervento | Stati fisici / servizi identici | Decisione |','|---|---:|---:|---:|---:|---:|---|---|']
    for r in rows:
        a,b=r['conditions']['control'],r['conditions']['reorder']
        lines.append(f'| {r["model"]} | {r["seed"]} | {r["delta_cash"]:+.0f} | {r["delta_margin"]:+.0f} | {a["stress"]}/{b["stress"]} | {a["losses"]}/{b["losses"]} | {r["physical_farms_equal"]} / {r["executed_services_equal"]} | {r["decision"]} |')
    lines+=['', '## Fragole e altre componenti, D20-D30', '', '| Modello | Seed | Delta vendite fragole | Delta altre vendite | Delta acquisti | Delta salari | Delta unita fragole |','|---|---:|---:|---:|---:|---:|---:|']
    for r in rows:
        a,b=[r['conditions'][c]['windows']['D20-D30'] for c in ['control','reorder']]
        ds=b['strawberry_sales']-a['strawberry_sales'];other=b['sales']-a['sales']-ds
        lines.append(f'| {r["model"]} | {r["seed"]} | {ds:+.0f} | {other:+.0f} | {b["purchases"]-a["purchases"]:+.0f} | {b["wages"]-a["wages"]:+.0f} | {b["strawberry_units"]-a["strawberry_units"]:+.0f} |')
    lines+=['', 'Nessuna promozione: lo scan misura una sola transizione; le quattro traiettorie nuove coprono soltanto due seed. Tutti i rami nuovi hanno719chiamate per agente e DONE/DONE, nessun errore nei core strumentati; parita fino al trigger e controlli fino al terminale. Il beneficio sulla singola richiesta non dimostra una buona regola per tutti i giorni/prodotti. [Protocollo](../../H003_PROTOCOL.md) - [Dati](RESULT.json) - [Scan completo](ONE_STEP.json) - [22KPI](daily_22_kpi.csv).']
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print([(r['model'],r['seed'],r['delta_cash'],r['delta_margin']) for r in rows])
def diagnose_orders():
    scan=read(OUT/'ONE_STEP.json')['rows'];rows=[]
    for x in scan:
        if x['reason']!='reordered':continue
        enemy=next(y for y in scan if y['seed']==x['seed'] and y['model']==x['opponent'] and y['opponent']==x['model'] and y['seat']==1-x['seat'])
        pos=next((i for i,o in enumerate(enemy['action_before'].get('market',[])) if len(o)>1 and o[:2]==['SELL','STRAWBERRY']),None)
        rows.append(dict(model=x['model'],seed=x['seed'],seat=x['seat'],opponent=x['opponent'],opponent_strawberry_order_position=pos,delta_cash=x['delta_cash'],note='Retrospective diagnosis only; contemporaneous opponent orders are unavailable to the rule'))
    (OUT/'OPPONENT_ORDER_DIAGNOSIS.json').write_text(json.dumps(rows,indent=2)+'\n')
    lines=['','## Diagnosi retrospettiva della posizione concorrente','', '| Posizione delle fragole nella lista avversaria, base0 | Positivi | Negativi |','|---|---:|---:|']
    for pos in sorted({r['opponent_strawberry_order_position'] for r in rows}):
        rr=[r for r in rows if r['opponent_strawberry_order_position']==pos]
        lines.append(f'| {pos} | {sum(r["delta_cash"]>0 for r in rr)} | {sum(r["delta_cash"]<0 for r in rr)} |')
    lines+=['', 'Questa informazione spiega dove cercare il meccanismo, ma e ricostruita dopo la partita: non si puo passare l ordine concorrente contemporaneo alla policy. Il prossimo esperimento deve prima verificare un inferenza dalla sola storia osservata. Nessuna regola basata sul nome del modello o sui dati futuri viene adottata.']
    p=OUT/'REPORT.md';p.write_text(p.read_text(encoding='utf-8').split('\n## Diagnosi retrospettiva')[0]+'\n'.join(lines)+'\n',encoding='utf-8')
if __name__=='__main__':
    main()
    diagnose_orders()
