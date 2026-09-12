"""Clean UTF-8 reports for the three preserved 772 calendar diagnostics."""
from pathlib import Path
import json, hashlib, shutil, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from markdown_it import MarkdownIt
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[3]
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS

def read(p):return json.loads(p.read_text(encoding='utf-8'))

def report(stage):
    out=BASE/'reports'/stage
    rows=read(out/'RESULTS.json')
    pairs=[]
    for r in rows:
        left,right=('Calendar772','E18') if r['seat']==0 else ('E18','Calendar772')
        bl,br=('Base772','E18') if r['seat']==0 else ('E18','Base772')
        pairs.append((read(BASE/f"artifacts/{stage}/{left}_{right}_{r['seed']}.kpi.json")['sides'][r['seat']],read(BASE/f"artifacts/calendar772_c1/{bl}_{br}_{r['seed']}.kpi.json")['sides'][r['seat']]))
    title={'calendar772_c1':'772: calendario dal D12, prova interrotta', 'calendar772_d1':'772: piano da D1, primo prototipo', 'calendar772_d1_c2':'772: piano da D1, correzione raccolte premature'}[stage]
    t='# '+title+'\n\n'
    if stage=='calendar772_c1':
        t+='Un confronto completo conservato; prosecuzione interrotta su indicazione dell’utente per progettare il piano da D1. Apertura e dispatcher della772 pubblicata invariati; quote e successione colturale modificate. Nessuna conclusione su una suite completa.\n\n'
    else:
        t+='**Screening non superato: il calendario comune non è stato realizzato nei tempi richiesti.** Piano attivo da D1, senza apertura congelata. Date e posizioni colturali, organico e apertura dei quadranti provengono dal calendario storico del rappresentante107083439. La policy legge solo osservazioni correnti e questo piano statico, senza prezzi o stati futuri. Conserva come obiettivo la geometria772 e10mucche/6pecore; due colture Q2 sono trasposte nei precedenti siti delle oche. Cambiano apertura, calendario e organico.\n\n'
        t+='Gate temporale: D1 con12meloni e7grani,4fragole aD6,20 aD9 e33 aD12. Un fallimento interrompe gli altri casi: la cassa non valuta il rendimento del calendario comune effettivamente realizzato.\n\n'
    if stage=='calendar772_d1_c2':
        t+='C2 corregge solo HARVEST prematuri: yield_units positivo non basta, deve essere raggiunta anche l’età minima della coltura. Il calendario del primo prototipo è invariato. C1 rimane conservata con11animali finali e779 HARVEST non confermati; C2 completa16animali e azzera gli HARVEST non confermati, ma manca i checkpoint iniziali.\n\n'
    t+='Controllo:772 E20.1 loaderfix pubblicata, submission56142698. Stesso seed, ruolo e avversario775. Mercato e avversario reagiscono alle azioni: non è una prova a prezzi fissati. Seed esposti, nessuna validazione indipendente; seed180912401–407 inutilizzati. Nessuna pubblicazione.\n\n| Seed | Ruolo | Cassa variante | Cassa base | Delta | Topologia | C/S/G | Chiamate | Errori core | Gate tecnico |\n|---|---:|---:|---:|---:|---|---|---:|---:|---|\n'
    for r in rows:
        t+=f"| {r['seed']} | {r['seat']} | {r['cash']:.0f} | {r['baseline_cash']:.0f} | {r['cash_delta']:+.0f} | {r['topology']} | {list(r['mix'].values())} | {r['runtime']['calls']} | {r['runtime']['core_errors']} | {r['technical_pass']} |\n"
    t+='\n## Calendario realizzato\n\n| Giorno | Modello | Meloni | Grano | Fragole | Carote | Mucche | Pecore | Persone |\n|---|---|---:|---:|---:|---:|---:|---:|---:|\n'
    common=read(ROOT/'docs/model_specs/codex/e19/reports/restart770_20260912/external_107083439.json')
    for d in [1,6,9,11,12,15,20,25,30]:
        for name,profiles in [('Variante',[p[0] for p in pairs]),('Base772',[p[1] for p in pairs]),('Comune storico',[common])]:
            vals=[np.mean([p['kpi'][d-1][k] for p in profiles]) for k in ['MELON','WHEAT','STRAWBERRY','CARROT','COW','SHEEP','people']]
            t+=f'| D{d} | {name} | '+' | '.join(f'{v:.1f}' for v in vals)+' |\n'
    t+='\n## Contabilità e perdite\n\n| Misura media per partita | Variante | Base772 |\n|---|---:|---:|\n'
    for label,fn in [('Vendite',lambda p:sum(sum(d['sales_cash'].values()) for d in p['ledger']['daily'])),('Acquisti',lambda p:sum(sum(d['purchase_cash'].values()) for d in p['ledger']['daily'])),('Assunzioni',lambda p:sum(d['hire_cash'] for d in p['ledger']['daily'])),('Perdite colture per sete',lambda p:len(p['crop_starvation'])),('Fughe animali',lambda p:sum(k['verified_animal_losses'] for k in p['kpi']))]:
        vals=[np.mean([fn(p[i]) for p in pairs]) for i in [0,1]]
        t+=f'| {label} | {vals[0]:.1f} | {vals[1]:.1f} |\n'
    t+='\n## Traiettorie dei22KPI\n\nCurve medie dei soli casi eseguiti. Il riferimento comune è descrittivo, da altra partita e altro mix animale.\n\n![22KPI](KPI22.png)\n\nProtocollo e hash in PROTOCOL.json; risultati integrali in RESULTS.json e negli artefatti replay/KPI. Il controllo iniziale della prova calendar772_c1 è stato corretto per distinguere core_errors=null della775 da un errore; policy invariata e audit conservato.\n'
    fig,axes=plt.subplots(6,4,figsize=(17,22),layout='constrained')
    fig.suptitle(title,fontsize=16)
    for ax,(key,label,unit) in zip(axes.flat,FIELDS):
        for idx,color,name in [(0,'#c46222','Variante'),(1,'#216ec0','Base772')]:
            ax.plot(range(1,31),np.mean([[k[key] for k in p[idx]['kpi']] for p in pairs],axis=0),color=color,label=name)
        ax.plot(range(1,31),[k[key] for k in common['kpi']],color='#44885c',linestyle=':',label='Comune storico')
        ax.set_title(label,fontsize=10);ax.set_xlabel('Giorno');ax.set_ylabel(unit);ax.grid(alpha=.2)
    for ax in list(axes.flat)[22:]:ax.axis('off')
    axes.flat[22].legend(*axes.flat[0].get_legend_handles_labels(),loc='center')
    fig.savefig(out/'KPI22.png',dpi=100);plt.close(fig)
    (out/'REPORT.md').write_text(t,encoding='utf-8')
    (out/'REPORT.html').write_text('<meta charset="utf-8"><title>'+title+'</title><style>body{font:17px/1.5 system-ui;max-width:1200px;margin:32px auto;padding:20px}img{max-width:100%}td,th{padding:7px;border-bottom:1px solid #ddd}</style>'+MarkdownIt().enable('table').render(t),encoding='utf-8')
    gate=dict(status='STOPPED_BY_USER' if stage=='calendar772_c1' else 'TIMETABLE_NOT_REALIZED',completed_pairs=len(rows),promotion=False,results=rows)
    (out/'GATE.json').write_text(json.dumps(gate,indent=2),encoding='utf-8')
    (out/'MANIFEST.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file() and p.name!='MANIFEST.json'},indent=2),encoding='utf-8')
    print(stage,'report complete')

if __name__=='__main__':
    for stage in ['calendar772_c1','calendar772_d1','calendar772_d1_c2']:report(stage)
