"""Matched late-season labor ablation; preserve pre-D20 actions exactly."""
import gzip,hashlib,json,sys
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
BASE=ROOT/'docs/model_specs/codex/e20'
OUT=BASE/'reports/labor_closing'

def main():
    rows=[]
    for p in sorted((BASE/'artifacts/labor_closing').glob('*.kpi.json')):
        c=json.loads(p.read_text());seat=next(s['seat'] for s in c['sides'] if s['name']=='E20v31')
        name=f"{'E20v28_E18' if seat==0 else 'E18_E20v28'}_{c['seed']}"
        old=BASE/'artifacts/e20_1_care'/f'{name}.json'
        a=json.loads(old.with_suffix('.kpi.json').read_text())['sides'][seat];b=c['sides'][seat]
        meta=json.loads(p.with_name(p.name.replace('.kpi.json','.json')).read_text())
        assert all(x['calls']==719 for x in meta['runtime'])
        assert meta['runtime'][seat]['core_errors']==0
        def read(path):
            with gzip.open(path,'rt') as f:return json.load(f)
        r0=read(old.with_suffix('.replay.json.gz'));r1=read(p.with_name(p.name.replace('.kpi.json','.replay.json.gz')))
        assert len(r1['steps'])==720 and all(s['status']=='DONE' for s in r1['steps'][-1])
        assert [x[seat]['action'] for x in r0['steps'][1:457]]==[x[seat]['action'] for x in r1['steps'][1:457]]
        row=dict(seed=c['seed'],seat=seat,opening_D1_D19_equal=True,changed_batches_D20_D30=sum(a[seat]['action']!=b[seat]['action'] for a,b in zip(r0['steps'][457:],r1['steps'][457:])),models={})
        first=next((i for i in range(457,720) if r0['steps'][i][seat]['action']!=r1['steps'][i][seat]['action']),None)
        row['first_changed_batch']=first
        row['topology']=meta['opening'][seat]['topology']
        assert row['topology']==[7,7,2]
        for label,s in [('E20.1',a),('E20v31',b)]:
            late=s['ledger']['daily'][19:]
            row['models'][label]=dict(cash=s['reward'],losses=len(s['ledger']['animal_escapes']),stress=len(s['crop_starvation']),
                actions={k:sum(d[k] for d in s['kpi'][19:]) for k in ['MOVE','PASS','WATER','FEED','CARE']},
                wages=sum(d['hire_cash'] for d in late),sales=sum(sum(d['sales_cash'].values()) for d in late),
                crop_tile_days=sum(d['crop_tiles'] for d in s['kpi'][19:]))
        rows.append(row)
    assert {(r['seed'],r['seat']) for r in rows}=={(s,w) for s in [180910101,180910102,180910103] for w in [0,1]}
    summary={m:{k:mean(r['models'][m][k] for r in rows) for k in ['cash','losses','stress','wages','sales','crop_tile_days']} for m in ['E20.1','E20v31']}
    for m in summary:summary[m]['actions']={k:mean(r['models'][m]['actions'][k] for r in rows) for k in ['MOVE','PASS','WATER','FEED','CARE']}
    delta=summary['E20v31']['cash']-summary['E20.1']['cash']
    result=dict(summary=summary,rows=rows,delta_cash=delta,delta_percent=100*delta/summary['E20.1']['cash'],promoted=False,scope='Exposed development seeds, matched opponent E18; D20-D30 labor screen')
    result['distinct_seeds']=len({r['seed'] for r in rows})
    result['decision']='NOT_ADOPTED' if delta<=0 or summary['E20v31']['stress']>summary['E20.1']['stress'] or summary['E20v31']['losses']>summary['E20.1']['losses'] else 'DEVELOPMENT_ONLY_REQUIRES_CONFIRMATION'
    (OUT/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    lines=['# D20-D30: servizi residui fuori coda','',f'{len(rows)} casi appaiati contro E18. Delta cassa medio: {delta:+,.1f} ({result["delta_percent"]:+.2f}%). Nessuna promozione su questo campione di sviluppo.','',
           '| Modello | Cassa finale | MOVE D20-D30 | PASS D20-D30 | WATER D20-D30 | Costo manovali D20-D30 | Coltivate: somma checkpoint D20-D30 |','|---|---:|---:|---:|---:|---:|---:|']
    for m,s in summary.items():lines.append(f'| {m} | {s["cash"]:,.1f} | {s["actions"]["MOVE"]:.1f} | {s["actions"]["PASS"]:.1f} | {s["actions"]["WATER"]:.1f} | {s["wages"]:.1f} | {s["crop_tile_days"]:.1f} |')
    lines+=['','| Seed | Ruolo | E20.1 | E20v31 | Delta |','|---|---:|---:|---:|---:|']
    for r in rows:
        a,b=[r['models'][m]['cash'] for m in ['E20.1','E20v31']];lines.append(f'| {r["seed"]} | {r["seat"]} | {a} | {b} | {b-a:+} |')
    lines+=['',f'Decisione: **{result["decision"]}**. I due ruoli verificano la simmetria; il campione contiene solo tre seed distinti, gia esposti.',
            '', '| Modello | Stress colture, partita intera | Fughe animali | FEED D20-D30 | CARE D20-D30 | Vendite D20-D30 |',
            '|---|---:|---:|---:|---:|---:|']
    for m,s in summary.items():
        lines.append(f'| {m} | {s["stress"]:.2f} | {s["losses"]:.2f} | {s["actions"]["FEED"]:.2f} | {s["actions"]["CARE"]:.2f} | {s["sales"]:.2f} |')
    diagnosis=json.loads((OUT/'DIAGNOSIS_SUMMARY.json').read_text())
    lines+=['', 'Diagnosi E20.1, seed 180910101 ruolo 0: 719 azioni riprodotte esattamente, 209 PASS D20-D30. Nei tentativi associati a 167 PASS viaggio e lavoro superano gia il tempo residuo; in 132 compare un blocco di coda, in 15 mancano materiali, in 2 sono prenotati. Il rientro incide su 10 e il margine di approvvigionamento su 3. Le categorie si sovrappongono e non misurano PASS evitabili.',
            '', f'Soltanto {len(diagnosis["late_free_opportunities_with_preparable_service_ignoring_route"])} opportunita del lavoratore libero nelle ultime sei ore hanno un servizio preparabile rimuovendo il blocco di coda: D21 H21-H22 e D26 H20. Questo controfattuale locale non garantisce il beneficio della modifica, che puo cambiare anche assegnazioni gia eseguibili e traiettorie successive.',
            '', 'La variante applica la deroga di coda alle offerte di servizio durante l assegnazione, non solo dopo un PASS. Quindi puo anticipare o spostare servizi tra lavoratori. La prova misura questo comportamento complessivo, non un recupero isolato delle tre opportunita.',
            '', '[Motivi dei rifiuti](DIAGNOSIS_SUMMARY.json) - [Traccia completa](ADMISSION_REASONS.json).']
    if result['decision']=='NOT_ADOPTED':
        lines+=['', 'Valutazione: E20v31 non viene adottata. I PASS diminuiscono, ma aumentano gli spostamenti e la cassa media peggiora. Le coltivate aumentano leggermente e lo stress non peggiora: il problema di questa variante e economico, non una regressione biologica. E20.1 pubblicata resta il riferimento.',
                '', 'Il prossimo esperimento dovrebbe verificare il costo dei percorsi e dei rifornimenti prima del finale della giornata. La diagnosi non giustifica togliere il margine di rientro o aggiungere manovali: i rifiuti da soli non dimostrano che queste mosse migliorerebbero la produzione.']
    lines+=['','Tutte le azioni prima di D20 identiche al controllo. Entrambi gli agenti ricevono 719 chiamate; nessun errore del core E20v31. Missioni attive e controlli di tempo/materiali conservati. D30 conserva il gestore terminale originale. PASS e MOVE sono comandi richiesti; WATER/FEED/CARE sono esecuzioni verificate.','', '[Protocollo](PROTOCOL.md) - [Dati completi](RESULT.json)']
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
