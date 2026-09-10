"""Record verified terminal outcomes and preserve the earlier shadow experiment."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'docs/model_specs/codex/evolution'
OUT=BASE/'reports/H006_FULL'
data=json.loads((OUT/'RESULT.json').read_text())
rows=data['rows']
assert len(rows)==4 and {(r['seed'],r['seat']) for r in rows}=={(s,t) for s in [180910204,180910206] for t in [0,1]}
same_work=all(r['physical_farms_equal'] and r['executed_services_equal'] and r['changed_worker_batches_by_seat']==[0,0] for r in rows)
cash=[r['delta_cash'] for r in rows];margin=[r['delta_margin'] for r in rows]
same_initial=all(r['delta_cash']==r['initial_delta_cash'] and r['delta_margin']==r['initial_delta_margin'] for r in rows)
isolated=True
for r in rows:
    a,b=[r['conditions'][c]['windows']['D20-D30'] for c in ['control','reorder']]
    ds=b['strawberry_sales']-a['strawberry_sales']
    isolated &= ds==r['delta_cash'] and b['sales']-a['sales']==ds and all(a[k]==b[k] for k in ['purchases','wages','strawberry_units','strawberry_stock'])
summary=f'''Completate quattro prosecuzioni modificate e quattro controlli esatti fino a D30, E19 contro E18, seed 180910204 e 180910206, entrambi i ruoli. Tutti gli otto rami hanno 719 chiamate per agente, DONE/DONE e zero errori nei core strumentati; ogni controllo riproduce 263 transizioni complete dopo 456 azioni ricostruite per agente. Il forecast H006 e ricostruito dalla storia propria e coincide con le predizioni congelate.

Delta cassa terminale medio {sum(cash)/4:+.1f}, intervallo [{min(cash):+.0f}, {max(cash):+.0f}]; delta margine medio {sum(margin)/4:+.1f}, intervallo [{min(margin):+.0f}, {max(margin):+.0f}]. Due seed, non quattro repliche indipendenti. Beneficio iniziale esattamente conservato fino a D30: {same_initial}. Lavoro, servizi e fattorie fisiche invariati in entrambi gli agenti: {same_work}. Differenza di cassa isolata negli incassi delle fragole, con uguali volumi/stock finali, altre vendite, acquisti e salari: {bool(isolated)}.

Sono disponibili le traiettorie dei 22 KPI di entrambi gli agenti, le differenze giornaliere e due grafici completi. Nessuna modifica o promozione dei modelli. Il campione e diagnostico gia esposto; i seed riservati restano inutilizzati. Questa verifica misura la persistenza di un singolo riordino D20 H1: non dimostra una regola utile ogni giorno, un miglioramento della manodopera o un vantaggio su altri avversari.
'''
report=OUT/'REPORT.md'
text=report.read_text(encoding='utf-8').split('\n## Valutazione conclusiva')[0]
report.write_text(text.rstrip()+'\n\n## Valutazione conclusiva\n\n'+summary,encoding='utf-8')
heading='## 2026-09-10 — H006: quattro prosecuzioni complete verificate'
checkpoint=heading+'\n\n'+summary+'\n[Report e 22 KPI](model_specs/codex/evolution/reports/H006_FULL/REPORT.md).\n'
for name in ['PROJECT_STATE.md','NEW_SESSION.md','EXPERIMENT_LOG.md']:
    path=ROOT/'docs'/name;text=path.read_text(encoding='utf-8')
    if heading not in text:
        path.write_text(text.rstrip()+'\n\n'+checkpoint if name=='EXPERIMENT_LOG.md' else checkpoint+'\n---\n\n'+text,encoding='utf-8')
rp=BASE/'REGISTRY.json';reg=json.loads(rp.read_text())
for e in reg['experiments']:
    if e['id']=='H006':
        e['full_continuations']=dict(status='complete',controls=4,interventions=4,distinct_seeds=2,adopted=False,result_path='docs/model_specs/codex/evolution/reports/H006_FULL/RESULT.json',mean_delta_cash=sum(cash)/4,mean_delta_margin=sum(margin)/4)
rp.write_text(json.dumps(reg,indent=2)+'\n')
p=BASE/'README.md';s=p.read_text(encoding='utf-8')
if '## H006: prosecuzioni complete' not in s:
    p.write_text(s.rstrip()+'\n\n## H006: prosecuzioni complete\n\n[Protocollo](H006_CONTINUATION_PROTOCOL.md) · [Report e grafici dei 22 KPI](reports/H006_FULL/REPORT.md). Script nella directory tools, da eseguire con il Python del progetto in sequenza: `branch_h006_full.py`, `report_h006_full.py`, `plot_h006_full.py`, `close_h006_full.py`. Otto simulazioni seriali; campione diagnostico, nessuna adozione.\n',encoding='utf-8')
paths=[p for p in OUT.iterdir() if p.suffix in ['.json','.md','.csv','.png'] and p.name!='MANIFEST.json']
paths += list((BASE/'artifacts/H006_FULL').glob('*.json'))
paths += [BASE/'tools'/n for n in ['branch_h006_full.py','report_h006_full.py','plot_h006_full.py','close_h006_full.py']]
paths += [BASE/'H006_CONTINUATION_PROTOCOL.md',BASE/'H006_PROTOCOL.md',BASE/'reports/H006/PREDICTIONS.json',rp]
(OUT/'MANIFEST.json').write_text(json.dumps(dict(status='complete',sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}),indent=2)+'\n')
print(summary)
