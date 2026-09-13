import json
from pathlib import Path
from collections import Counter,defaultdict
import e209_s56165462_charts as charts
ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/model_specs/codex/e22/reports/kiki_variability_extended_20260913'

def main():
    data=json.loads((OUT/'ANALYSIS.json').read_text(encoding='utf-8'));rows=data['rows'];p=data['protocol']
    groups=defaultdict(list);footprints=defaultdict(list);layouts=defaultdict(list);crops=defaultdict(list);rules=[]
    for r in rows:
        key=', '.join(f'{k}:{v}' for k,v in sorted(r['d20_animals'].items()));groups[key].append(r['episode'])
        footprints[str([(x,y) for x,y,k in r['daily'][19]['structures']])].append(r['episode'])
        layouts[str(r['daily'][19]['structures'])].append(r['episode'])
        crops[', '.join(f'{k}:{v}' for k,v in sorted(r['daily'][19]['counts'].items()) if k not in ['COW','SHEEP','GOOSE'])].append(r['episode'])
        orders=[o for o in r['purchases'] if o['day']==8 and o['hour']==2]
        if orders:
            o=orders[0];yarn=o['shops'].get('YARN_STORE',0)>0;sheep=any(a['order'][1]=='SHEEP' and a['order'][2]>0 for a in orders)
            rules.append(dict(episode=r['episode'],yarn=yarn,sheep=sheep,match=yarn==sheep,prices=o['prices'],orders=orders))
    summary=dict(n=len(rows),eligible=p['eligible_public'],groups=dict(groups),d20_footprints=len(footprints),d20_layouts=len(layouts),d20_crop_groups=dict(crops),replacements=sum(len(r['replacements']) for r in rows),removals=sum(len(r['removals']) for r in rows),trigger_covered=len(rules),trigger_matches=sum(t['match'] for t in rules),trigger_counterexamples=[t for t in rules if not t['match']],tomato_replays=[r['episode'] for r in rows if any(e['crop']=='TOMATO' for e in r['crop_events'])],max_last_placement_day=max(e['day'] for r in rows for e in r['placements']))
    (OUT/'SUMMARY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    branches=Counter((next(o['order'][1] for o in r['purchases'] if o['day']==8),next(o['order'][1] for o in r['purchases'] if o['day']==11)) for r in rows)
    sequences=Counter(tuple(sorted(set((e['day'],e['crop']) for e in r['crop_events'] if e['day']>=20))) for r in rows)
    summary['purchase_branches']=[dict(d8=a,d11=b,n=n) for (a,b),n in branches.items()]
    summary['late_crop_day_species_patterns']=len(sequences)
    (OUT/'SUMMARY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    interpretation='''Le quattro configurazioni corrispondono a due finestre di acquisto: D8 COW oppure SHEEP, D11–D12 GOOSE oppure SHEEP. Le combinazioni osservate sono COW/GOOSE in 26 casi, SHEEP/SHEEP in 9, COW/SHEEP in 3 e SHEEP/GOOSE in 1. Non sono quattro riscritture del piano intero: sono compatibili con due decisioni locali, senza provare che il codice le calcoli indipendentemente.

Il controesempio 107961405 sceglie SHEEP a D8 H2 senza negozio lana, con latte 210 e lana 189; poi sceglie GOOSE. Quindi YARN_STORE non è una spiegazione completa. Anche il secondo ramo richiede analisi: 107358349 acquista pecore dopo l'arrivo di YARN_STORE, ma 107663612 e 107775518 fanno lo stesso senza quel negozio. Non introdurre una regola assoluta ricavata dagli otto replay iniziali.

Le successioni tardive mostrano lo stesso insieme di coppie giorno/specie in tutti i 39 replay: semine di grano a D20–D25 e in alcuni passaggi D27–D28, carote a D25–D28; nessun pomodoro. Questa misura non implica identità dei comandi, delle coordinate o delle quantità. Il nucleo colturale resta molto stabile.

Una rimozione nell'episodio 108444786 è verificata come fuga: pecora (7,4), passaggio D16→D17, non alimentata e consecutive_unfed=1 prima del refresh. Non viene ricomprata; non è una rotazione. Tutti gli ultimi collocamenti animali del campione avvengono entro D12.

Per la nostra evoluzione conviene quindi studiare separatamente la scelta COW/SHEEP su pascoli liberi e la scelta delle tre strutture finali, conservando il calendario, prima di affiancare la conversione colturale a pomodoro. Nessuna prova qui dimostra ancora quanto ciascuna scelta riduca la saturazione rispetto alla sua alternativa nello stesso mercato.'''
    intro=f"Submission 56137379: {len(rows)} replay su {p['eligible_public']} pubblici disponibili. Selezione cronologica distribuita: 32 indici equidistanti, uniti agli 8 replay precedenti; una sovrapposizione. Nessun filtro su risultato o configurazione. Periodo campionato: {rows[0]['created']} — {rows[-1]['created']}. Non è un censimento né un campione casuale."
    findings=f"A D20: {len(groups)} mix animali, {len(footprints)} impronte spaziali e {len(layouts)} disposizioni dei tipi di struttura. Sostituzioni di specie su caselle precedentemente occupate: {summary['replacements']}; rimozioni animali: {summary['removals']}. Queste ultime possono essere fughe e non scelte strategiche."
    trigger=f"Regola precedente, senza riadattare soglie: a D8 H2 ordine SHEEP se YARN_STORE è presente. Copertura {len(rules)}/{len(rows)}, corrispondenze {summary['trigger_matches']}/{len(rules)}. Associazione osservata: non identifica il programma né dimostra il beneficio economico."
    md='# Kiki yi2 — variabilità estesa\n\n'+intro+'\n\n'+findings+'\n\n## Mix animali a D20\n\n'+'\n'.join(f'- **{k}**: {len(es)} replay.' for k,es in groups.items())+'\n\n'+trigger+'\n\n## Colture\n\n'+'\n'.join(f'- {k}: {len(es)} replay a D20.' for k,es in crops.items())+f"\n\nReplay con almeno una semina di pomodoro: {len(summary['tomato_replays'])}/{len(rows)}. I grafici giornalieri permettono di distinguere mix a D20 e successioni finali.\n\n## Limiti\n\nLe assenze di animali o colture non sono automaticamente decisioni di portafoglio: possono essere investimenti incompleti o perdite. Prezzi riportati a fine giornata, non prezzi realizzati delle vendite. In questa estensione si verificano hash, episodi completi e transizioni; non si ripete l'audit economico dei due giocatori eseguito sugli otto replay precedenti. Le frequenze descrivono solo il campione; nessuna modifica di policy.\n\n[Grafici D1–D30](REPORT.html) · [Dati sintetici ed episodi per gruppo](SUMMARY.json) · [Dati completi](ANALYSIS.json).\n"
    md+='\n\n## Cosa cambia rispetto al primo campione\n\n'+interpretation+'\n'
    (OUT/'REPORT.md').write_text(md,encoding='utf-8')
    body='<h1>Kiki yi2 · variabilità estesa</h1><p>'+intro+'</p><p>'+findings+'</p><ul>'+''.join(f'<li><b>{k}</b>: {len(es)} replay</li>' for k,es in groups.items())+'</ul><p>'+trigger+'</p><p><a href="REPORT.md">Metodo e limiti</a> · <a href="SUMMARY.json">Gruppi e controesempi</a></p><label>Replay <select id="match">'+''.join(f'<option value="{i}">{r["episode"]} · {r["created"][:10]} · {r["d20_animals"]}</option>' for i,r in enumerate(rows))+'</select></label>'
    body+='<details><summary>Finestre decisionali, controesempi e significato</summary>'+''.join('<p>'+p+'</p>' for p in interpretation.split('\n\n'))+'</details>'
    for i,r in enumerate(rows):
        body+=f'<section data-i="{i}"'+(' hidden' if i else '')+f'><h2>Episodio {r["episode"]}</h2><p><a href="https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56137379&amp;episodeId={r["episode"]}">Partita su Kaggle</a> · Dati di fine giornata; prezzi di mercato, non incassati.</p><div class="plots">'
        def plot(title,seqs,names,unit):charts.NAMES=names;return charts.chart(title,seqs,unit)
        ds=r['daily']
        for names in [['COW','SHEEP'],['GOOSE'],['STRAWBERRY','TOMATO'],['WHEAT','CARROT'],['MELON']]:
            body+=plot(' / '.join(names)+' · blu / arancio',[[d['counts'].get(k,0) for d in ds] for k in names],names,'caselle occupate')
        for names in [['MILK','WOOL'],['STRAWBERRY','TOMATO']]:body+=plot('Prezzi '+ ' / '.join(names)+' · blu / arancio',[[d['prices'][k] for d in ds] for k in names],names,'monete/unità')
        body+=plot('Strutture · blu pascoli / arancio pollai',[[sum(t[2]==k for t in d['structures']) for d in ds] for k in ['PASTURE','COOP']],['Pascoli','Pollai'],'caselle')
        body+=plot('Cassa',[[d['cash'] for d in ds]],['Kiki'],'monete')+'</div></section>'
    body+='<script>document.getElementById("match").onchange=e=>document.querySelectorAll("section[data-i]").forEach(s=>s.hidden=s.dataset.i!==e.target.value);</script>'
    (OUT/'REPORT.html').write_text('<!doctype html><html lang="it"><meta charset="utf-8"><title>Kiki yi2 · variabilità estesa</title><style>body{font:16px system-ui;background:#f4f6f2;color:#22362e;max-width:1400px;margin:30px auto;padding:0 24px}p{line-height:1.6}section{background:white;padding:24px;margin-top:20px;border-radius:12px}.plots{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.plot{border:1px solid #ddd;border-radius:8px;padding:14px}svg{width:100%}select{font:inherit;padding:10px;max-width:100%}@media(max-width:800px){.plots{grid-template-columns:1fr}}</style>'+body+'</html>',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=True))
if __name__=='__main__':main()
