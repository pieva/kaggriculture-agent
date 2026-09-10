"""H002 paired full-trajectory audit, prices, sale timing and biological gates."""
import csv,gzip,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools.audit_results import run as audit
from docs.model_specs.codex.evolution.tools.sale_events import audit_with_sales
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS
BASE=ROOT/'docs/model_specs/codex/evolution';ART=BASE/'artifacts';OUT=BASE/'reports/H002'
def read(p):return json.loads(p.read_text())
def main():
    rows=[];sources={};daily_rows=[]
    for model in ['E18','E19','E20.1']:
        for seed in [180910201,180910202]:
            cp=ART/'H001'/f'{model}_control.json' if seed==180910201 else ART/'H002'/f'{model}_{seed}_control.json'
            tp=ART/'H002'/f'{model}_{seed}_defer_strawberry.json';cm,tm=read(cp),read(tp)
            assert cm['source_replay_sha256']==tm['source_replay_sha256'] and cm['engine']==tm['engine']
            for key,value in cm['sources'].items():
                if key.startswith('submission'):assert tm['sources'][key]==value
            assert cm['verification']['suffix_states']==263 and cm['verification']['suffix_action_batches']==263
            assert tm['verification']['suffix_states']==(tm['intervention']['step']-456 if tm['intervention'] else 263)
            conditions={}
            for label,p,meta in [('control',cp,cm),('defer',tp,tm)]:
                sources[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
                assert all(x['calls']==719 and x['core_errors'] in [0,None] for x in meta['runtime'])
                assert all(x['core_errors']==0 for name,x in zip(meta['agents'],meta['runtime']) if name!='E18')
                audit(str(p));k=read(p.with_suffix('.kpi.json'));assert k['replay_sha256']==meta['replay_sha256']
                with gzip.open(p.with_suffix('.replay.json.gz'),'rb') as f:raw=f.read()
                assert hashlib.sha256(raw).hexdigest()==meta['replay_sha256'];r=json.loads(raw)
                assert len(r['steps'])==720 and all(s['status']=='DONE' for s in r['steps'][-1])
                ledger=audit_with_sales(r,0);s=k['sides'][0]
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
            a,b=conditions['control'],conditions['defer'];bio=b['losses']>a['losses'] or b['stress']>a['stress']
            rows.append(dict(model=model,seed=seed,intervention=tm['intervention'],conditions=conditions,delta_cash=b['windows']['D20-D30']['cash']-a['windows']['D20-D30']['cash'],delta_margin=b['windows']['D20-D30']['margin']-a['windows']['D20-D30']['margin'],biological_regression=bio,decision='NOT_APPLICABLE' if tm['intervention'] is None else 'REJECT_BIOLOGICAL_REGRESSION' if bio else 'DIAGNOSTIC_ONLY',adopted=False))
    (OUT/'RESULT.json').write_text(json.dumps(dict(experiment='H002',distinct_seeds=2,paired_situations=6,rows=rows,metadata_sources_sha256=sources),indent=2)+'\n')
    with (OUT/'daily_22_kpi.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(daily_rows[0]));writer.writeheader();writer.writerows(daily_rows)
    lines=['# H002: rinvio di una richiesta di vendita delle fragole','', 'Sei situazioni: tre modelli, due seed diagnostici, ruolo0. Stesso stato iniziale in ogni confronto con se stesso, avversario reattivo. Nessuna promozione. Il trattamento elimina una richiesta corrente e lascia al controller le decisioni successive, non impone un ritardo di durata fissa.', '', '| Modello | Seed | Delta cassa finale | Delta margine | Stress controllo/intervento | Fughe controllo/intervento | Decisione |','|---|---:|---:|---:|---:|---:|---|']
    for r in rows:
        a,b=r['conditions']['control'],r['conditions']['defer'];lines.append(f'| {r["model"]} | {r["seed"]} | {r["delta_cash"]:+.0f} | {r["delta_margin"]:+.0f} | {a["stress"]}/{b["stress"]} | {a["losses"]}/{b["losses"]} | {r["decision"]} |')
    for name in ['D20','D20-D22','D20-D30']:
        lines+=['',f'## {name}: intervento meno controllo','','| Modello | Seed | Delta cassa | Delta vendite fragole | Delta unita fragole | Prezzo medio controllo/intervento | Delta stock fragole |','|---|---:|---:|---:|---:|---:|---:|']
        for r in rows:
            a,b=[r['conditions'][c]['windows'][name] for c in ['control','defer']]
            price=lambda x:'n/a' if x is None else f'{x:.2f}'
            lines.append(f'| {r["model"]} | {r["seed"]} | {b["cash"]-a["cash"]:+.0f} | {b["strawberry_sales"]-a["strawberry_sales"]:+.0f} | {b["strawberry_units"]-a["strawberry_units"]:+.0f} | {price(a["strawberry_price"])}/{price(b["strawberry_price"])} | {b["strawberry_stock"]-a["strawberry_stock"]:+.0f} |')
    lines+=['','## Tempi effettivi','','Primo SELL fragole riuscito al trigger o dopo, verificato eseguendo il mercato sui due giocatori e riconciliando la cassa.','','| Modello | Seed | Trigger | Vendita controllo | Vendita intervento |','|---|---:|---|---|---|']
    for r in rows:
        fmt=lambda e:'nessuna' if not e else f'D{e["day"]} H{e["hour"]}'
        lines.append(f'| {r["model"]} | {r["seed"]} | {fmt(r["intervention"])} | {fmt(r["conditions"]["control"]["first_strawberry_sale_at_or_after_trigger"])} | {fmt(r["conditions"]["defer"]["first_strawberry_sale_at_or_after_trigger"])} |')
    lines+=['', 'I sei controlli sono verificati fino al terminale; tre del seed201 vengono riusati da H001 dopo confronto degli hash di sorgente, bundle ed engine. Tutti i rami hanno719chiamate per agente, zero errori nei core che espongono il contatore e DONE/DONE. Audit dei flussi e transazioni riuscite; prezzi medi ponderati per unita vendute. Lo stock conta deposito e inventari, non frutti ancora sulle caselle.', '', 'Un prezzo medio diverso puo includere quantita e tempi differenti, oltre a reazioni dell avversario. Il trattamento identifica un effetto locale della richiesta omessa, non la causa universale del divario tra i modelli. Due seed non autorizzano una regola generale. [Protocollo](../../H002_PROTOCOL.md) - [Dati](RESULT.json) - [Scomposizione vendite](../sales_20260910/REPORT.md).']
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8');print([(r['model'],r['seed'],r['delta_cash'],r['delta_margin'],r['decision']) for r in rows])
if __name__=='__main__':
    main()
    from docs.model_specs.codex.evolution.tools.isolate_h002 import summarize
    summarize()
