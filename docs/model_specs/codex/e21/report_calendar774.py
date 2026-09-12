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
    out=BASE/'reports/calendar774_c2';results=read(out/'RESULTS.json');pairs=[];summary=[]
    for r in results:
        left,right=('Calendar774','E18') if r['seat']==0 else ('E18','Calendar774')
        bleft,bright=('Repair774','E18') if r['seat']==0 else ('E18','Repair774')
        cp=BASE/f"artifacts/calendar774_c2/{left}_{right}_{r['seed']}.kpi.json"
        bp=BASE/f"artifacts/repair774_v2/{bleft}_{bright}_{r['seed']}.kpi.json"
        c=read(cp)['sides'][r['seat']];b=read(bp)['sides'][r['seat']];pairs.append((c,b))
        summary.append(dict(result=r,calendar_checkpoints={str(d):{k:c['kpi'][d-1][k] for k in ['MELON','WHEAT','STRAWBERRY','CARROT','COW','SHEEP','GOOSE','people']} for d in [12,15,20,25,30]},candidate_crop_audit=c['crop_starvation'],baseline_crop_audit=b['crop_starvation']))
    (out/'DIAGNOSIS.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    complete=len(results)==4 and all(r['technical_pass'] for r in results)
    deltas={s:float(np.mean([r['cash_delta'] for r in results if r['seed']==s])) for s in sorted({r['seed'] for r in results})}
    biological=all(len(c['crop_starvation'])<=len(b['crop_starvation']) and sum(d['verified_animal_losses'] for d in c['kpi'])<=sum(d['verified_animal_losses'] for d in b['kpi']) for c,b in pairs)
    economic=complete and all(d>0 for d in deltas.values())
    gate=dict(technical_complete=complete,positive_cash_each_seed=economic,biological_not_worse_each_case=biological,seed_cash_deltas=deltas,development_pass=complete and economic and biological)
    (out/'GATE.json').write_text(json.dumps(gate,indent=2),encoding='utf-8')
    t=f'''# E21 774: prova del calendario comune

**Stato: {'quattro casi tecnicamente completati; verificare il gate economico e biologico sotto' if complete else 'screening fermato: invarianti tecniche non soddisfatte'}.** La Repair2 pubblicata non è stata modificata né ripubblicata.

La candidata C2 conserva il prefisso E21 D1–D11 e mira alla stessa geometria 774 e allo stesso mix8C/9S/1G. Da D12 usa il pianificatore osservativo e il dispatcher già esistenti della V48, adattati a caselle riservate, 33 fragole/23 grani, successione delle fragole verso grano e carote nel finale. Questo cambia calendario e dispatcher, non identifica causalmente il solo calendario. L'organico rimane limitato a12 aiutanti; nessun cap artificiale sui MOVE.

## Difetto corretto durante lo screening

C1 si interrompe dopo265 chiamate: il controller770 non classificava GOOSE fra gli animali e tentava di quotarla come prodotto di mercato (KeyError). C2 aggiunge la regola motore dell'oca ai dizionari isolati del controller, senza cambiare il codice congelato degli altri agenti. C1 e relativi sorgenti sono conservati nella cartella calendar774_c1; la sua cassa non è un risultato competitivo valido.

## Tutti i casi eseguiti C2

| Seed | Ruolo | Chiamate | Prefisso uguale | Topologia finale | Animali C/S/G | Cassa candidata | Cassa Repair2 | Delta | Tecnica |
|---|---:|---:|---|---|---|---:|---:|---:|---|
'''
    for r in results:
        t+=f"| {r['seed']} | {r['seat']} | {r['runtime']['calls']} | {r['prefix_equal']} | {r['topology']} | {list(r['mix'].values())} | {r['cash']:.0f} | {r['baseline_cash']:.0f} | {r['cash_delta']:+.0f} | {r['technical_pass']} |\n"
    t+='\nIl confronto locale usa lo stesso seed, ruolo e avversario775 delle prove Repair2 già salvate. Le reazioni del mercato e dell’avversario possono divergere dopo il cambio di azioni. Seed già esposti, nessuna conferma indipendente e nessuna prova di mantenere il vantaggio iniziale di rating. I seed riservati180912401–407 restano inutilizzati.\n'
    t+=f'\n**Gate di sviluppo: {"PASS" if gate["development_pass"] else "NON SUPERATO"}.** Cassa positiva in ciascun seed: {economic}; perdite biologiche non peggiori in ciascun caso: {biological}. Delta mediando i ruoli per seed: {deltas}.\n'
    t+='\n## Calendario effettivamente realizzato\n\nLe quote sono intenzioni soggette a capacità, non semine forzate. Il raggiungimento tardivo delle 33 fragole non equivale al calendario esterno D12.\n\n| Giorno | Modello | Fragole | Grano | Meloni | Carote | MOVE | PASS |\n|---|---|---:|---:|---:|---:|---:|---:|\n'
    for d in [12,15,20,25,30]:
        for i,label in [(0,'C2'),(1,'Repair2')]:
            vals=[np.mean([p[i]['kpi'][d-1][k] for p in pairs]) for k in ['STRAWBERRY','WHEAT','MELON','CARROT','MOVE','PASS']]
            t+=f'| {d} | {label} | '+' | '.join(f'{v:.1f}' for v in vals)+' |\n'
    t+='\n## Contabilità e sicurezza\n\nMedie per partita, intera stagione.\n\n| Misura | C2 | Repair2 |\n|---|---:|---:|\n'
    for label,fun in [('Vendite',lambda p:sum(sum(d['sales_cash'].values()) for d in p['ledger']['daily'])),('Acquisti',lambda p:sum(sum(d['purchase_cash'].values()) for d in p['ledger']['daily'])),('Assunzioni',lambda p:sum(d['hire_cash'] for d in p['ledger']['daily'])),('Perdite crop per sete',lambda p:len(p['crop_starvation'])),('Fughe animali',lambda p:sum(d['verified_animal_losses'] for d in p['kpi']))]:
        vals=[np.mean([fun(p[i]) for p in pairs]) for i in [0,1]];t+=f'| {label} | {vals[0]:.2f} | {vals[1]:.2f} |\n'
    if not complete:t+='\n**Il risultato non consente di giudicare il calendario sulla struttura richiesta:** il trasferimento deve prima soddisfare gli invarianti. Nessuna promozione o ulteriore estensione automatica ai casi riservati.\n'
    fig,axes=plt.subplots(6,4,figsize=(17,22),layout='constrained');fig.suptitle('E21: calendario C2 e Repair2 · soli casi eseguiti\nControllare validità tecnica prima di interpretare le curve',fontsize=16)
    for ax,(key,label,unit) in zip(axes.flat,FIELDS):
        for side,color,title in [(0,'#c46222','Calendario C2'),(1,'#216ec0','Repair2 congelata')]:
            arr=np.array([[d[key] for d in pair[side]['kpi']] for pair in pairs]);ax.plot(range(1,31),np.mean(arr,axis=0),label=title,color=color)
        ax.set_title(label,fontsize=10);ax.set_xlabel('Giorno');ax.set_ylabel(unit);ax.grid(alpha=.2)
    for ax in list(axes.flat)[22:]:ax.axis('off')
    axes.flat[22].legend(*axes.flat[0].get_legend_handles_labels(),loc='center');fig.savefig(out/'KPI22.png',dpi=100);plt.close(fig)
    t+='\n![22 KPI diagnostici](KPI22.png)\n\nDati completi in DIAGNOSIS.json, RESULTS.json e negli artefatti .kpi.json/.replay.json.gz. Le perdite e i servizi non vengono esclusi quando sfavorevoli. Protocollo e hash fissati prima dei risultati in PROTOCOL.json.\n'
    (out/'REPORT.md').write_text(t,encoding='utf-8');(out/'REPORT.html').write_text('<meta charset="utf-8"><title>E21 calendario774 C2</title><style>body{font:17px/1.5 system-ui;max-width:1200px;margin:32px auto;padding:20px}img{max-width:100%}td,th{padding:7px;border-bottom:1px solid #ddd}</style>'+MarkdownIt().enable('table').render(t),encoding='utf-8')
    (out/'MANIFEST.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file() and p.name!='MANIFEST.json'},indent=2),encoding='utf-8')
    print('REPORT',len(results),complete)
if __name__=='__main__':main()
