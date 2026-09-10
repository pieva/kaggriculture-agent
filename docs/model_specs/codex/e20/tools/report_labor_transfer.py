"""Matched late-season labor ablation; preserve pre-D20 actions exactly."""
import gzip,hashlib,json,sys
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
BASE=ROOT/'docs/model_specs/codex/e20'
OUT=BASE/'reports/labor_transfer'

def main():
    rows=[]
    for p in sorted((BASE/'artifacts/labor_transfer').glob('*.kpi.json')):
        c=json.loads(p.read_text());seat=next(s['seat'] for s in c['sides'] if s['name']=='E20v30')
        name=f"{'E20v28_E18' if seat==0 else 'E18_E20v28'}_{c['seed']}"
        old=BASE/'artifacts/e20_1_care'/f'{name}.json'
        a=json.loads(old.with_suffix('.kpi.json').read_text())['sides'][seat];b=c['sides'][seat]
        meta=json.loads(p.with_name(p.name.replace('.kpi.json','.json')).read_text())
        assert all(x['calls']==719 for x in meta['runtime'])
        assert meta['runtime'][seat]['core_errors']==0
        def read(path):
            with gzip.open(path,'rt') as f:return json.load(f)
        r0=read(old.with_suffix('.replay.json.gz'));r1=read(p.with_name(p.name.replace('.kpi.json','.replay.json.gz')))
        assert [x[seat]['action'] for x in r0['steps'][1:457]]==[x[seat]['action'] for x in r1['steps'][1:457]]
        diagnostics=read(p.with_name(p.name.replace('.kpi.json',f'.seat{seat}.diagnostics.json.gz')))
        transfers=[x for x in diagnostics['routes'] if x.get('event')=='late_transfer']
        assert all(20<=x['day']<=29 and x['estimated_saved_steps']>0 for x in transfers)
        row=dict(seed=c['seed'],seat=seat,opening_D1_D19_equal=True,changed_batches_D20_D30=sum(a[seat]['action']!=b[seat]['action'] for a,b in zip(r0['steps'][457:],r1['steps'][457:])),transfers=len(transfers),estimated_saved_steps=sum(x['estimated_saved_steps'] for x in transfers),models={})
        for label,s in [('E20.1',a),('E20v30',b)]:
            late=s['ledger']['daily'][19:]
            row['models'][label]=dict(cash=s['reward'],losses=len(s['ledger']['animal_escapes']),stress=len(s['crop_starvation']),
                actions={k:sum(d[k] for d in s['kpi'][19:]) for k in ['MOVE','PASS','WATER','FEED','CARE']},
                wages=sum(d['hire_cash'] for d in late),sales=sum(sum(d['sales_cash'].values()) for d in late),
                crop_tile_days=sum(d['crop_tiles'] for d in s['kpi'][19:]))
        rows.append(row)
    assert rows
    summary={m:{k:mean(r['models'][m][k] for r in rows) for k in ['cash','losses','stress','wages','sales','crop_tile_days']} for m in ['E20.1','E20v30']}
    for m in summary:summary[m]['actions']={k:mean(r['models'][m]['actions'][k] for r in rows) for k in ['MOVE','PASS','WATER','FEED','CARE']}
    delta=summary['E20v30']['cash']-summary['E20.1']['cash']
    result=dict(summary=summary,rows=rows,delta_cash=delta,delta_percent=100*delta/summary['E20.1']['cash'],promoted=False,scope='Exposed development seeds, matched opponent E18; D20-D30 labor screen')
    result['transfers_total']=sum(r['transfers'] for r in rows)
    result['distinct_seeds']=len({r['seed'] for r in rows})
    (OUT/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    lines=['# D20-D30: trasferimento mirato del lavoro residuo','',f'{len(rows)} casi appaiati contro E18. Delta cassa medio: {delta:+,.1f} ({result["delta_percent"]:+.2f}%). Nessuna promozione su questo campione di sviluppo.','',
           '| Modello | Cassa finale | MOVE D20-D30 | PASS D20-D30 | WATER D20-D30 | Costo manovali D20-D30 | Coltivate: somma checkpoint D20-D30 |','|---|---:|---:|---:|---:|---:|---:|']
    for m,s in summary.items():lines.append(f'| {m} | {s["cash"]:,.1f} | {s["actions"]["MOVE"]:.1f} | {s["actions"]["PASS"]:.1f} | {s["actions"]["WATER"]:.1f} | {s["wages"]:.1f} | {s["crop_tile_days"]:.1f} |')
    lines+=['','| Seed | Ruolo | E20.1 | E20v30 | Delta |','|---|---:|---:|---:|---:|']
    for r in rows:
        a,b=[r['models'][m]['cash'] for m in ['E20.1','E20v30']];lines.append(f'| {r["seed"]} | {r["seat"]} | {a} | {b} | {b-a:+} |')
    lines+=['','Tutte le azioni prima di D20 identiche al controllo. Entrambi gli agenti ricevono 719 chiamate; nessun errore del core E20v30. Missioni attive conservate, costi residui sottratti ai budget. D30 conserva il gestore terminale originale. PASS e MOVE sono comandi richiesti; WATER/FEED/CARE sono esecuzioni verificate.','', '[Protocollo](PROTOCOL.md) Ãƒâ€šÃ‚Â· [Dati completi](RESULT.json)']
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
