"""Exact accounting gap E18 minus E20.2; attribution is descriptive, not causal."""
import json
from collections import Counter
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[5];BASE=ROOT/'docs/model_specs/codex/e20'
ART=BASE/'artifacts/e20_2_confirmation';OUT=BASE/'reports/e20_2_confirmation'
def totals(side,start=0,end=30):
    days=side['ledger']['daily'][start:end]
    values={k:dict(sum((Counter(d[k]) for d in days),Counter())) for k in ['sales_cash','sold_units','harvested','purchase_cash','bought_units','planted','executed_actions','requested_actions']}
    values.update({k:sum(d[k] for d in days) for k in ['hire_cash','land_cash','unit_cash_delta']})
    values['net']=sum(values['sales_cash'].values())-sum(values['purchase_cash'].values())-values['hire_cash']-values['land_cash']+values['unit_cash_delta']
    return values
def main():
    matches=[]
    for p in sorted(ART.glob('*.kpi.json')):
        c=json.loads(p.read_text(encoding='utf-8'))
        if {s['name'] for s in c['sides']}!={'E18','E20.2'}:continue
        sides={s['name']:s for s in c['sides']};a,b=[totals(sides[n]) for n in ['E18','E20.2']]
        pieces=dict(initial=sides['E18']['ledger']['initial_cash']-sides['E20.2']['ledger']['initial_cash'],sales=sum(a['sales_cash'].values())-sum(b['sales_cash'].values()),purchase_saving=sum(b['purchase_cash'].values())-sum(a['purchase_cash'].values()),hire_saving=b['hire_cash']-a['hire_cash'],land_saving=b['land_cash']-a['land_cash'],unit_actions=a['unit_cash_delta']-b['unit_cash_delta'])
        gap=sides['E18']['reward']-sides['E20.2']['reward'];assert abs(sum(pieces.values())-gap)<1e-6
        products={}
        for item in sorted(set(a['sales_cash'])|set(b['sales_cash'])):
            qa,qb=[t['sold_units'].get(item,0) for t in [a,b]];ra,rb=[t['sales_cash'].get(item,0) for t in [a,b]]
            pa=ra/qa if qa else None;pb=rb/qb if qb else None
            volume=(qa-qb)*(pa+pb)/2 if qa and qb else ra-rb
            price=(pa-pb)*(qa+qb)/2 if qa and qb else 0
            assert abs(volume+price-(ra-rb))<1e-6
            products[item]=dict(revenue_gap=ra-rb,sold_E18=qa,sold_E20=qb,price_E18=pa,price_E20=pb,harvest_E18=a['harvested'].get(item,0),harvest_E20=b['harvested'].get(item,0),volume_component=volume,price_component=price)
        phases={}
        for label,start,end in [('D1-11',0,11),('D12-19',11,19),('D20-30',19,30)]:
            ta,tb=[totals(sides[n],start,end) for n in ['E18','E20.2']]
            phases[label]=dict(gap=ta['net']-tb['net'],E18=ta,E20=tb)
        matches.append(dict(seed=c['seed'],E20_seat=sides['E20.2']['seat'],cash_gap_E18_minus_E20=gap,pieces=pieces,products=products,phases=phases,totals=dict(E18=a,E20=b),terminal={n:s['terminal'] for n,s in sides.items()}))
    assert len(matches)==14
    pieces={k:mean(m['pieces'][k] for m in matches) for k in matches[0]['pieces']}
    products={p:mean(m['products'].get(p,{}).get('revenue_gap',0) for m in matches) for p in sorted({p for m in matches for p in m['products']})}
    result=dict(matches=matches,mean_cash_gap=mean(m['cash_gap_E18_minus_E20'] for m in matches),mean_pieces=pieces,mean_revenue_gap_by_product=products,note='E18 minus E20.2. Exact cash identity, descriptive price/volume decomposition; not marginal causal values. Roles paired within seven seeds.')
    (OUT/'CASH_GAP.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    lines=['# Perché E18 ha più o meno cassa di E20.2','',f"Divario medio E18 meno E20.2: {result['mean_cash_gap']:+.1f}. Identità contabile verificata in tutti i 14 scontri.",'','| Componente | Contributo al vantaggio E18 |','|---|---:|']
    for k,v in pieces.items():lines.append(f'| {k} | {v:+.1f} |')
    lines+=['','| Prodotto | Maggiori ricavi E18 |','|---|---:|']
    for k,v in sorted(products.items(),key=lambda kv:-kv[1]):lines.append(f'| {k} | {v:+.1f} |')
    lines+=['','| Fase | Flusso netto E18 meno E20.2 |','|---|---:|']
    for phase in ['D1-11','D12-19','D20-30']:lines.append(f"| {phase} | {mean(m['phases'][phase]['gap'] for m in matches):+.1f} |")
    lines+=['','La scomposizione quantità/prezzo nel JSON è una identità simmetrica, non una stima controfattuale: cambiare produzione o calendario delle vendite cambia anche il mercato e le azioni avversarie. Se un modello non vende un prodotto, tutto il divario viene attribuito alla componente volume e il prezzo mancante resta nullo.', '', 'Scorte terminali, raccolto e venduto sono riportati separatamente; un prodotto rimasto in deposito o sul terreno non contribuisce alla cassa. PASS e servizi sono descrittori operativi e non vengono assunti come causa.', '', '[Dati per seed, ruolo, prodotto e fase](CASH_GAP.json) · [22 KPI](REPORT.html)']
    (OUT/'CASH_GAP.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('\n'.join(lines))
if __name__=='__main__':main()
