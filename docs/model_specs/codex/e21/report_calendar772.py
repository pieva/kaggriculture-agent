"""Report all attempted calendar diagnostics, including technical failures."""
from pathlib import Path
import json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from markdown_it import MarkdownIt
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[3]
import sys
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    out=BASE/'reports/calendar772_c1';results=read(out/'RESULTS.json');pairs=[];summary=[]
    for r in results:
        left,right=('Calendar772','E18') if r['seat']==0 else ('E18','Calendar772')
        bleft,bright=('Base772','E18') if r['seat']==0 else ('E18','Base772')
        cp=BASE/f"artifacts/calendar772_c1/{left}_{right}_{r['seed']}.kpi.json"
        bp=BASE/f"artifacts/calendar772_c1/{bleft}_{bright}_{r['seed']}.kpi.json"
        c=read(cp)['sides'][r['seat']];b=read(bp)['sides'][r['seat']];pairs.append((c,b))
        summary.append(dict(result=r,calendar_checkpoints={str(d):{k:c['kpi'][d-1][k] for k in ['MELON','WHEAT','STRAWBERRY','CARROT','COW','SHEEP','GOOSE','people']} for d in [12,15,20,25,30]},candidate_crop_audit=c['crop_starvation'],baseline_crop_audit=b['crop_starvation']))
    (out/'DIAGNOSIS.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    complete=len(results)==4 and all(r['technical_pass'] for r in results)
    deltas={s:float(np.mean([r['cash_delta'] for r in results if r['seed']==s])) for s in sorted({r['seed'] for r in results})}
    biological=all(len(c['crop_starvation'])<=len(b['crop_starvation']) and sum(d['verified_animal_losses'] for d in c['kpi'])<=sum(d['verified_animal_losses'] for d in b['kpi']) for c,b in pairs)
    economic=complete and all(d>0 for d in deltas.values())
    gate=dict(technical_complete=complete,positive_cash_each_seed=economic,biological_not_worse_each_case=biological,seed_cash_deltas=deltas,development_pass=complete and economic and biological)
    (out/'GATE.json').write_text(json.dumps(gate,indent=2),encoding='utf-8')
    t=f'''# 772 E20.1: prova del calendario comune

**Stato: {'quattro casi tecnicamente completati; verificare il gate economico e biologico sotto' if complete else 'screening fermato: invarianti tecniche non soddisfatte'}.** La 772 E20.1 pubblicata non ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨ stata modificata nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© ripubblicata.

La candidata conserva apertura, dispatcher, geometria 772 e mix 10 mucche/6 pecore della E20.1 pubblicata (loaderfix, submission 56142698). Cambia le intenzioni del calendario biologico: 33 fragole/23 grani, esclusione dei due pascoli Q2 dalle intenzioni agricole, successione delle fragole esaurite verso grano da D21, preferenza carote dal D25 quando maturazione e consegna entrano nel termine. Restano le prioritÃƒÆ’Ã‚Â  remote-first e CARE utile della 772 e il massimo di 12 aiutanti. Le quote non garantiscono la replica del calendario esterno, che arriva a 33 fragole giÃƒÆ’Ã‚Â  a D12.

Questa prova conserva il dispatcher della base 772; la precedente prova 774 trasferiva anche il dispatcher V48. Il confronto tra le due prove non isola quindi il solo effetto della topologia.

## Tutti i casi eseguiti C1

| Seed | Ruolo | Chiamate | Prefisso uguale | Topologia finale | Animali C/S/G | Cassa candidata | Cassa 772 E20.1 | Delta | Tecnica |
|---|---:|---:|---|---|---|---:|---:|---:|---|
'''
    for r in results:
        t+=f"| {r['seed']} | {r['seat']} | {r['runtime']['calls']} | {r['prefix_equal']} | {r['topology']} | {list(r['mix'].values())} | {r['cash']:.0f} | {r['baseline_cash']:.0f} | {r['cash_delta']:+.0f} | {r['technical_pass']} |\n"
    t+='\nIl confronto locale usa lo stesso seed, ruolo e avversario775 delle prove 772 E20.1 giÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  salvate. Le reazioni del mercato e dellÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢avversario possono divergere dopo il cambio di azioni. Seed giÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  esposti, nessuna conferma indipendente e nessuna prova di mantenere il vantaggio iniziale di rating. I seed riservati180912401ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ407 restano inutilizzati.\n'
    t+=f'\n**Gate di sviluppo: {"PASS" if gate["development_pass"] else "NON SUPERATO"}.** Cassa positiva in ciascun seed: {economic}; perdite biologiche non peggiori in ciascun caso: {biological}. Delta mediando i ruoli per seed: {deltas}.\n'
    t+='\n## Calendario effettivamente realizzato\n\nLe quote sono intenzioni soggette a capacitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â , non semine forzate. Il raggiungimento tardivo delle 33 fragole non equivale al calendario esterno D12.\n\n| Giorno | Modello | Fragole | Grano | Meloni | Carote | MOVE | PASS |\n|---|---|---:|---:|---:|---:|---:|---:|\n'
    for d in [12,15,20,25,30]:
        for i,label in [(0,'C1'),(1,'772 E20.1')]:
            vals=[np.mean([p[i]['kpi'][d-1][k] for p in pairs]) for k in ['STRAWBERRY','WHEAT','MELON','CARROT','MOVE','PASS']]
            t+=f'| {d} | {label} | '+' | '.join(f'{v:.1f}' for v in vals)+' |\n'
    t+='\n## ContabilitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  e sicurezza\n\nMedie per partita, intera stagione.\n\n| Misura | C1 | 772 E20.1 |\n|---|---:|---:|\n'
    for label,fun in [('Vendite',lambda p:sum(sum(d['sales_cash'].values()) for d in p['ledger']['daily'])),('Acquisti',lambda p:sum(sum(d['purchase_cash'].values()) for d in p['ledger']['daily'])),('Assunzioni',lambda p:sum(d['hire_cash'] for d in p['ledger']['daily'])),('Perdite crop per sete',lambda p:len(p['crop_starvation'])),('Fughe animali',lambda p:sum(d['verified_animal_losses'] for d in p['kpi']))]:
        vals=[np.mean([fun(p[i]) for p in pairs]) for i in [0,1]];t+=f'| {label} | {vals[0]:.2f} | {vals[1]:.2f} |\n'
    t+='\n## Vendite per prodotto\n\nMedie per partita; prezzo medio realizzato = ricavi / unità vendute. Le variazioni di prezzo comprendono la reazione del mercato e non sono un effetto a mercato fissato.\n\n| Prodotto | Unità variante | Unità base | Ricavi variante | Ricavi base | Prezzo variante | Prezzo base |\n|---|---:|---:|---:|---:|---:|---:|\n'
    for product in ['MELON','STRAWBERRY','WHEAT','CARROT','MILK','WOOL','FERTILIZER']:
        units=[sum(sum(d['sold_units'].get(product,0) for d in p[i]['ledger']['daily']) for p in pairs)/len(pairs) for i in [0,1]]
        sales=[sum(sum(d['sales_cash'].get(product,0) for d in p[i]['ledger']['daily']) for p in pairs)/len(pairs) for i in [0,1]]
        prices=[sales[i]/units[i] if units[i] else 0 for i in [0,1]]
        t+='| '+product+' | '+' | '.join(f'{v:.2f}' for v in units+sales+prices)+' |\n'
    t+='\nNota di audit: il primo controllo tecnico si è fermato perché il wrapper775 espone core_errors=null (dato non disponibile). Il runner è stato corretto per verificare le chiamate di entrambi e gli errori core delle772. Nessuna modifica alla policy o al criterio economico; evidenza conservata in GATE_CORRECTION.json e RESULTS_INITIAL_GATE.json.\n'
    t+='\n## Tempi e residui per caso\n\n| Seed | Ruolo | Primo giorno Ã¢â€°Â¥33 fragole variante/base | Perdite crop variante/base | Animali residui variante/base | Delta cassa D15 | Delta cassa D20 | Delta cassa D30 |\n|---|---:|---|---|---|---:|---:|---:|\n'
    for row,(c,b) in zip(results,pairs):
        first=[next((d+1 for d,k in enumerate(x['kpi']) if k['STRAWBERRY']>=33),None) for x in (c,b)]
        residual=[sum(x['terminal'][where].get(species,0) for where in ('shed','carried') for species in ('COW','SHEEP','GOOSE')) for x in (c,b)]
        delta=[c['kpi'][d-1]['money']-b['kpi'][d-1]['money'] for d in (15,20,30)]
        t+=f"| {row['seed']} | {row['seat']} | {first} | {len(c['crop_starvation'])}/{len(b['crop_starvation'])} | {residual} | "+' | '.join(f'{v:+.0f}' for v in delta)+' |\n'
    if not complete:t+='\n**Il risultato non consente di giudicare il calendario sulla struttura richiesta:** il trasferimento deve prima soddisfare gli invarianti. Nessuna promozione o ulteriore estensione automatica ai casi riservati.\n'
    fig,axes=plt.subplots(6,4,figsize=(17,22),layout='constrained');fig.suptitle('772: calendario C1 e base E20.1 ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â· soli casi eseguiti\nControllare validitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  tecnica prima di interpretare le curve',fontsize=16)
    for ax,(key,label,unit) in zip(axes.flat,FIELDS):
        for side,color,title in [(0,'#c46222','Calendario C1'),(1,'#216ec0','772 E20.1 congelata')]:
            arr=np.array([[d[key] for d in pair[side]['kpi']] for pair in pairs]);ax.plot(range(1,31),np.mean(arr,axis=0),label=title,color=color)
        ax.set_title(label,fontsize=10);ax.set_xlabel('Giorno');ax.set_ylabel(unit);ax.grid(alpha=.2)
    for ax in list(axes.flat)[22:]:ax.axis('off')
    axes.flat[22].legend(*axes.flat[0].get_legend_handles_labels(),loc='center');fig.savefig(out/'KPI22.png',dpi=100);plt.close(fig)
    t+='\n![22 KPI diagnostici](KPI22.png)\n\nDati completi in DIAGNOSIS.json, RESULTS.json e negli artefatti .kpi.json/.replay.json.gz. Le perdite e i servizi non vengono esclusi quando sfavorevoli. Protocollo e hash fissati prima dei risultati in PROTOCOL.json.\n'
    (out/'REPORT.md').write_text(t,encoding='utf-8');(out/'REPORT.html').write_text('<meta charset="utf-8"><title>772 calendario C1</title><style>body{font:17px/1.5 system-ui;max-width:1200px;margin:32px auto;padding:20px}img{max-width:100%}td,th{padding:7px;border-bottom:1px solid #ddd}</style>'+MarkdownIt().enable('table').render(t),encoding='utf-8')
    (out/'MANIFEST.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file() and p.name!='MANIFEST.json'},indent=2),encoding='utf-8')
    print('REPORT',len(results),complete)
if __name__=='__main__':main()
