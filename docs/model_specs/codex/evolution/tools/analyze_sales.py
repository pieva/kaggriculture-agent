"""Exact symmetric revenue decomposition by item; descriptive, not causal."""
import json,sys
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
BASE=ROOT/'docs/model_specs/codex/evolution';OUT=BASE/'reports/sales_20260910';SOURCE=ROOT/'docs/model_specs/codex/e20/artifacts/e20_1_confirmation'
WINDOWS=[('D15-D19',14,19),('D20-D24',19,24),('D25-D30',24,30)]
def main():
    sides={}
    for p in SOURCE.glob('*.kpi.json'):
        r=json.loads(p.read_text())
        for s in r['sides']:sides[(r['seed'],s['name'],r['sides'][1-s['seat']]['name'],s['seat'])]=s
    rows=[]
    for a,b,opponent in [('E19','E20.1','E18'),('E18','E19','E20.1'),('E18','E20.1','E19')]:
        for seed in range(180910201,180910208):
            for seat in [0,1]:
                for window,start,end in WINDOWS:
                    ds=[sides[(seed,m,opponent,seat)]['ledger']['daily'][start:end] for m in [a,b]]
                    products=sorted({k for dd in ds for d in dd for k in d['sales_cash']})
                    for item in products:
                        q=[sum(d['sold_units'].get(item,0) for d in dd) for dd in ds];v=[sum(d['sales_cash'].get(item,0) for d in dd) for dd in ds]
                        p0=v[0]/q[0] if q[0] else (v[1]/q[1] if q[1] else 0);p1=v[1]/q[1] if q[1] else p0
                        volume=(q[1]-q[0])*(p0+p1)/2;price=(p1-p0)*(q[0]+q[1])/2
                        assert abs(volume+price-(v[1]-v[0]))<1e-7
                        rows.append(dict(a=a,b=b,opponent=opponent,seed=seed,seat=seat,window=window,item=item,units_a=q[0],units_b=q[1],sales_a=v[0],sales_b=v[1],delta=v[1]-v[0],volume_component=volume,price_component=price))
    summary=[]
    for a,b,opp in [('E19','E20.1','E18'),('E18','E19','E20.1'),('E18','E20.1','E19')]:
        for window,_,_ in WINDOWS:
            rr=[x for x in rows if (x['a'],x['b'],x['window'])==(a,b,window)]
            summary.append(dict(a=a,b=b,opponent=opp,window=window,**{k:sum(x[k] for x in rr)/14 for k in ['delta','volume_component','price_component']},products=[dict(item=item,**{k:sum(x[k] for x in rr if x['item']==item)/14 for k in ['delta','volume_component','price_component','units_a','units_b']}) for item in sorted({x['item'] for x in rr})]))
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'data.json').write_text(json.dumps(dict(summary=summary,rows=rows),indent=2)+'\n')
    lines=['# Vendite: volumi e prezzi realizzati','', '42 partite diagnostiche gia esposte. Confronti sullo stesso avversario/seed/ruolo, poi media su sette seed e due ruoli. Delta secondo modello meno primo. Per prodotto, delta vendite = delta quantita * prezzo medio dei due modelli + delta prezzo * quantita media. Se un modello non vende, il prezzo non osservato viene posto uguale a quello dell altro e il delta assegnato al volume. La scomposizione e contabile, non causale: prezzi diversi possono riflettere tempi di vendita, offerta propria e reazioni dell avversario. Quantita venduta non equivale a produzione.', '', '| Primo | Secondo | Finestra | Delta vendite | Componente volumi | Componente prezzi |','|---|---|---|---:|---:|---:|']
    for r in summary:lines.append(f'| {r["a"]} | {r["b"]} | {r["window"]} | {r["delta"]:+.1f} | {r["volume_component"]:+.1f} | {r["price_component"]:+.1f} |')
    lines+=['', '## E20.1 meno E19: D20-D24 per seed', '', 'Ruoli mediati dentro ogni seed. La componente prezzi non ha lo stesso segno in tutte le situazioni.', '', '| Seed | Componente volumi | Componente prezzi |','|---|---:|---:|']
    for seed in range(180910201,180910208):
        rr=[x for x in rows if x['a']=='E19' and x['seed']==seed and x['window']=='D20-D24']
        lines.append(f'| {seed} | {sum(x["volume_component"] for x in rr)/2:+.1f} | {sum(x["price_component"] for x in rr)/2:+.1f} |')
    lines+=['','## E20.1 meno E19, contro E18','','| Finestra | Prodotto | Delta vendite | Volumi | Prezzi | Unita E19 | Unita E20.1 |','|---|---|---:|---:|---:|---:|---:|']
    for r in summary[:3]:
        for p in sorted(r['products'],key=lambda p:abs(p['delta']),reverse=True):
            lines.append('| '+r['window']+' | '+p['item']+' | '+' | '.join(f'{p[k]:+.1f}' for k in ['delta','volume_component','price_component','units_a','units_b'])+' |')
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8');print(json.dumps(summary[:3],indent=2))
if __name__=='__main__':main()
