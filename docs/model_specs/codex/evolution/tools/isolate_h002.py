"""Verify whether the sale pulse changed physical work or only settlement."""
import gzip,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];BASE=ROOT/'docs/model_specs/codex/evolution';OUT=BASE/'reports/H002'
def summarize():
    data=json.loads((OUT/'RESULT.json').read_text());rows=[]
    for row in data['rows']:
        m,s=row['model'],row['seed']
        cp=BASE/'artifacts/H001'/f'{m}_control.replay.json.gz' if s==180910201 else BASE/'artifacts/H002'/f'{m}_{s}_control.replay.json.gz'
        tp=BASE/'artifacts/H002'/f'{m}_{s}_defer_strawberry.replay.json.gz'
        with gzip.open(cp,'rt') as f:a=json.load(f)
        with gzip.open(tp,'rt') as f:b=json.load(f)
        ak=json.loads(cp.with_name(cp.name.replace('.replay.json.gz','.kpi.json')).read_text())
        bk=json.loads(tp.with_name(tp.name.replace('.replay.json.gz','.kpi.json')).read_text())
        executed_equal=all(ak['sides'][seat]['ledger']['daily'][d]['executed_actions']==bk['sides'][seat]['ledger']['daily'][d]['executed_actions'] for seat in [0,1] for d in range(19,30))
        physical_equal=all({key:value for key,value in a['steps'][i][0]['observation']['farms'][seat].items() if key!='money'}=={key:value for key,value in b['steps'][i][0]['observation']['farms'][seat].items() if key!='money'} for seat in [0,1] for i in range(457,720))
        differences=[]
        for seat in [0,1]:
            differences.append(sum(any((a['steps'][i][seat]['action'] or {}).get(key)!=(b['steps'][i][seat]['action'] or {}).get(key) for key in ['farmer','hands']) for i in range(457,720)))
        x,y=[row['conditions'][c]['windows']['D20-D30'] for c in ['control','defer']]
        delta_sales=y['sales']-x['sales'];delta_strawberry=y['strawberry_sales']-x['strawberry_sales']
        result=dict(model=m,seed=s,changed_worker_batches= differences,delta_other_sales=delta_sales-delta_strawberry,delta_purchases=y['purchases']-x['purchases'],delta_wages=y['wages']-x['wages'],delta_strawberry_units=y['strawberry_units']-x['strawberry_units'],delta_strawberry_stock=y['strawberry_stock']-x['strawberry_stock'],delta_cash=row['delta_cash'],delta_strawberry_sales=delta_strawberry)
        result.update(physical_farms_equal_excluding_cash=physical_equal,executed_services_equal=executed_equal)
        rows.append(result)
    (OUT/'ISOLATION.json').write_text(json.dumps(rows,indent=2)+'\n')
    lines=['', '## Verifica del meccanismo', '', '| Modello | Seed | Batch di lavoro diversi, agente/avversario | Delta altre vendite | Delta acquisti | Delta salari |','|---|---:|---:|---:|---:|---:|']
    for r in rows:lines.append(f'| {r["model"]} | {r["seed"]} | {r["changed_worker_batches"][0]}/{r["changed_worker_batches"][1]} | {r["delta_other_sales"]:+.0f} | {r["delta_purchases"]:+.0f} | {r["delta_wages"]:+.0f} |')
    if all(r['changed_worker_batches']==[0,0] and r['physical_farms_equal_excluding_cash'] and r['executed_services_equal'] and all(r[k]==0 for k in ['delta_other_sales','delta_purchases','delta_wages','delta_strawberry_units','delta_strawberry_stock']) and r['delta_cash']==r['delta_strawberry_sales'] for r in rows):
        lines+=['', 'In tutti e sei i casi il lavoro di entrambi gli agenti resta identico per l intero seguito, le quantita totali di fragole vendute e lo stock finale coincidono, e il delta di cassa e interamente riconciliato con gli incassi delle fragole. Questa prova circoscrive l effetto locale al calendario di vendita e al prezzo realizzato, senza un cambiamento del lavoro fisico. E18 peggiora in entrambi i seed; E19 ed E20.1 migliorano modestamente. Non emerge una regola universale di rinvio.', '', 'Prossimo punto da verificare: prezzo ottenibile e concorrenza nelle finestre di vendita, non un ritardo fisso applicato a tutte le topologie. Il deficit medio E20.1 rispetto a E19 non e spiegato integralmente da questa singola richiesta.']
    (OUT/'REPORT.md').write_text((OUT/'REPORT.md').read_text(encoding='utf-8').split('\n## Verifica del meccanismo')[0]+'\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(rows,indent=2))
if __name__=='__main__':summarize()
