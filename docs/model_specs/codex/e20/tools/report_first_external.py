"""External daily KPI trajectories, audited economics and frozen provenance."""
import csv,hashlib,html,json,sys
from pathlib import Path
from statistics import mean,median
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools.acquire_first_external import OUT
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS

def build():
    cohort=json.loads((OUT/'cohort.json').read_text(encoding='utf-8'))
    profiles=[json.loads((OUT/f"profile_{g['episode']}.json").read_text(encoding='utf-8')) for g in cohort['games']]
    games=[p for p in profiles if not p['selfplay']]
    groups={'candidate':[p['sides'][p['seat']] for p in games], 'top770':[p['sides'][1-p['seat']] for p in games]}
    labels={'candidate':'E20.1 esterna','top770':'Avversari stessi incontri'}
    summary={}
    for k,ps in groups.items():
        summary[k]=dict(n=len(ps),cash_mean=mean(p['reward'] for p in ps),cash_median=median(p['reward'] for p in ps),
          cash_min=min(p['reward'] for p in ps),cash_max=max(p['reward'] for p in ps),
          animal_losses=sum(len(p['ledger']['animal_escapes']) for p in ps),
          stress=sum(len(p['crop_starvation']) for p in ps),
          sales=mean(sum(sum(d['sales_cash'].values()) for d in p['ledger']['daily']) for p in ps),
          purchases=mean(sum(sum(d['purchase_cash'].values()) for d in p['ledger']['daily']) for p in ps),
          wages=mean(sum(d['hire_cash'] for d in p['ledger']['daily']) for p in ps))
    wins=sum(p['rewards'][p['seat']]>p['rewards'][1-p['seat']] for p in games)
    series={k:{field:[[median(v),min(v),max(v)] for d in range(30) for v in [[p['kpi'][d][field] for p in ps]]] for field in [f[0] for f in FIELDS]+['unlocked_tiles']} for k,ps in groups.items()}
    data=dict(topLabel=labels['top770'],metrics=[dict(key=k,label=l,unit=u) for k,l,u in FIELDS],series=series,summary=summary,wins=wins,games=len(games),submission_id=56142698)
    (OUT/'data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (OUT/'daily_kpi.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['episode','seat','role','day']+[v[0] for v in FIELDS]+['unlocked_tiles']);w.writeheader()
        for p in games:
            for side in p['sides']:
                for d,row in enumerate(side['kpi'],1):w.writerow(dict(episode=p['episode'],seat=side['seat'],role='E20.1' if side['seat']==p['seat'] else 'opponent',day=d,**{k:row[k] for k in [v[0] for v in FIELDS]+['unlocked_tiles']}))
    def fmt(x):return f'{x:,.1f}'.replace(',','X').replace('.',',').replace('X','.')
    table='<div class="tablewrap"><table><tr><th>Indicatore</th><th>E20.1</th><th>Avversari</th></tr>'
    for key,label in [('cash_mean','Cassa media'),('cash_median','Cassa mediana'),('cash_min','Cassa minima'),('cash_max','Cassa massima'),('animal_losses','Perdite animali totali'),('stress','Transizioni crop→weed dopo stress'),('sales','Vendite medie'),('purchases','Acquisti medi'),('wages','Manovali, costo medio')]:
        table+=f'<tr><td>{label}</td>'+''.join(f'<td>{fmt(summary[k][key])}</td>' for k in groups)+'</tr>'
    table+='</table></div>'
    rows='<div class="tablewrap"><table><tr><th>Episodio</th><th>Ruolo</th><th>Avversario</th><th>Cassa E20.1</th><th>Cassa avversario</th><th>Esito</th></tr>'
    for p in sorted(games,key=lambda x:x['episode']):
        s=p['seat'];a,b=p['rewards'][s],p['rewards'][1-s]
        rows+=f'<tr><td><a href="https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56142698&episodeId={p["episode"]}">{p["episode"]}</a></td><td>{s}</td><td>{html.escape(p["teams"][1-s])}</td><td>{fmt(a)}</td><td>{fmt(b)}</td><td>{"V" if a>b else "S" if a<b else "P"}</td></tr>'
    rows+='</table></div>'
    template=(ROOT/'docs/model_specs/codex/e19/tools/complete_kpi_template.html').read_text(encoding='utf-8')
    style=template.split('<style>')[1].split('</style>')[0]
    script=template.split('<script>')[1].split('</script>')[0].replace("candidate:'770 assistita'","candidate:'E20.1 esterna'")
    body=f'''<h1>E20.1 · primi replay esterni · 22 KPI</h1>
<p>Submission <a href="https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56142698">56142698</a> · Complete · rating osservato 944 · 10 settembre 2026.</p>
<p><strong>{wins}/{len(games)} vittorie</strong>. Coorte congelata al primo accesso: 21 partite competitive complete, un self-play conservato separatamente (107446770), un incontro ancora in corso escluso. Nessun filtro per risultato. Tutte le finali E20.1 sono 7–7–2.</p>
<p>Mediana puntuale e banda min–max, non intervallo di confidenza né una singola partita. Stessi incontri per le due serie, avversari eterogenei: questa è la diagnosi della coorte esterna, non il benchmark Top772 ancora da identificare.</p>
{table}<div class="toolbar"><button data-series="candidate" aria-pressed="true"><span class="swatch"></span>E20.1 esterna</button><button data-series="top770" aria-pressed="true"><span class="swatch reference"></span>Avversari stessi incontri</button><span class="meta">Passaggio o clic sul grafico per i valori; frecce sinistra/destra da tastiera.</span></div><div class="grid" id="charts"></div>
<h2>Risultati per incontro</h2>{rows}
<details><summary>Tutti i valori giornalieri: mediana E20.1 / avversari</summary><div class="tablewrap" id="daily-table"></div></details>
<h2>Metodo e provenienza</h2><p>Checkpoint 24×D−1: H24 prima dell’ultimo batch D1–D29, terminale D30. Flussi su tutti i batch del giorno. Persone = manovali + contadino; tratteggiate nel pannello coltivate = terreno sbloccato. Animali collocati esclusi deposito e inventari. MOVE e PASS richiesti, WATER/FEED/CARE verificati dal ledger. Non irrigate a H24 non implica morte; le perdite animali sono verificate al refresh. Tutti i replay hanno 720 stati DONE/DONE e ledger di cassa riconciliato. I test interni non sono stati rilanciati né la policy modificata.</p>
<p><a href="cohort.json">Catalogo e hash replay</a> · <a href="data.json">Dati aggregati</a> · <a href="daily_kpi.csv">CSV giornaliero</a> · <a href="manifest.json">Provenienza</a></p>'''
    page='<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>E20.1 esterna — 22 KPI</title><style>'+style+'</style><main id="complete-kpi">'+body+'</main><script id="kpi-data" type="application/json">'+json.dumps(data,ensure_ascii=False).replace('</','<\\/')+'</script><script>'+script+'</script></html>'
    (OUT/'REPORT.html').write_text(page,encoding='utf-8')
    (OUT/'REPORT.md').write_text(f'# E20.1: prima coorte esterna\n\nSubmission 56142698 Complete. {wins}/21 vittorie; 21/21 finali 772. Un self-play escluso dalle medie.\n\nCassa media E20.1 {fmt(summary["candidate"]["cash_mean"])}, avversari {fmt(summary["top770"]["cash_mean"])}. Perdite animali E20.1: {summary["candidate"]["animal_losses"]}.\n\n[22 KPI](REPORT.html) · [Catalogo](cohort.json) · [CSV](daily_kpi.csv).\n\nTop772: identità in attesa di chiarimento; nessuna sostituzione con un corpus storico già consumato.\n',encoding='utf-8')
    sources=[Path(__file__),Path(__file__).with_name('analyze_first_external.py'),Path(__file__).with_name('acquire_first_external.py'),ROOT/'docs/model_specs/codex/e19/tools/complete_kpi_template.html',ROOT/'submission/submission_codex_e20_772_e20v28_loaderfix.py']
    manifest=dict(submission_id=56142698,benchmark_top772='IDENTITY_PENDING',panels=22,raw_games=len(profiles),competitive_games=len(games),cash_parity_errors=0,sources={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},outputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file() and p.name!='manifest.json'})
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':build()
