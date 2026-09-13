import json,html
from pathlib import Path
import e209_s56165462_charts as charts
ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/model_specs/codex/e22/reports/kiki_rotation_20260913'

def main():
    data=json.loads((OUT/'ANALYSIS.json').read_text(encoding='utf-8'));rows=data['rows']
    assert all(not r['replacements'] and not r['removals'] for r in rows)
    footprints={tuple((x,y) for x,y,k in r['daily'][19]['structures']) for r in rows}
    assert len(footprints)==1
    summary=[]
    for r in rows:
        order=next(p for p in r['purchases'] if p['features']['day']==8 and p['features']['hour']==2)
        animals={k:v for k,v in r['daily'][19]['own'].items() if k in ['COW','SHEEP','GOOSE']}
        products={k:dict(sold=sum(d['sold_units'].get(k,0) for d in r['ledger']['daily']),revenue=sum(d['sales_cash'].get(k,0) for d in r['ledger']['daily'])) for k in ['MILK','WOOL','EGG']}
        for p in products.values():p['realized_price']=p['revenue']/p['sold'] if p['sold'] else None
        summary.append(dict(episode=r['episode'],yarn=order['features']['shops'].get('YARN_STORE',0),choice=order['order'][1],animals=animals,products=products,last_placement_day=max(e['day'] for e in r['placements'])))
    (OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    text='''# Kiki yi2 — scelta del mix e rischio di saturazione

Submission **56137379**, otto replay già acquisiti: cinque del pilota e tre della precedente verifica. Questo approfondimento non aggiunge un campione indipendente. Hash dei replay verificati, registri economici di entrambi i giocatori riconciliati.

## Risultato

**Zero sostituzioni e zero rimozioni di animali negli otto replay.** La variabilità è nella costruzione del portafoglio durante la crescita, non in una rotazione di animali già collocati dopo la caduta dei prezzi. Nel motore locale `DIG` non rimuove animali e `PLACE` richiede una struttura libera; le colture hanno quindi una flessibilità diversa.

Le 17 coordinate dedicate all'allevamento a D20 coincidono in tutti gli otto replay. I tipi di struttura cambiano: 14 pascoli + 3 pollai nel ramo misto, 17 pascoli nel ramo lana. È un'impronta stabile con una scelta di struttura su tre caselle, non una topologia integralmente identica.

## Decisione osservata a D8 H2

- Nei cinque casi senza negozio di lana, l'ordine compra una mucca. A D20: 8 mucche, 6 pecore, 3 oche.
- Nei tre casi con uno o due negozi di lana, l'ordine compra una pecora. A D20: 6 mucche, 10 pecore, nessuna oca; un pascolo è privo di animale.
- La corrispondenza negozio/scelta è 8/8 in questo campione già studiato. È un'associazione osservata, non l'identificazione del codice o una prova di rendimento causale.

Un contrasto utile: episodio 108483384, latte 210 e lana 200, con negozio lana, sceglie pecora; episodio 108487585, latte 194 e lana 195, senza negozio lana, sceglie mucca. Il solo prezzo istantaneo più alto non spiega entrambi.

## Quanto protegge dalla saturazione?

Nei tre casi del ramo lana vengono vendute 244 unità di lana, con prezzo medio realizzato circa 238–245. Nei cinque casi del ramo misto vengono vendute 161 unità, ma il prezzo realizzato è circa 42–58. È coerente con la presenza di domanda persistente nel primo ramo. Non misura il guadagno della scelta: mercati e avversari sono diversi e non abbiamo simulato la scelta alternativa nello stesso scenario.

Kiki continua a produrre e vendere anche nel ramo con lana poco remunerativa. Non emerge dagli animali una correzione tardiva del mix in risposta a saturazione già avvenuta. I grafici confrontano vendite proprie e avversarie; non attribuiscono automaticamente tutta la discesa del prezzo alle nostre vendite. Prezzo a fine giornata e prezzo medio effettivamente incassato sono distinti.

## Collegamento con i pomodori

Base di riferimento: **E20.9fix**, file `submission/submission_codex_e20_9_placefix_internal.py`, derivata da E20v44 late tomato con la successiva correzione dei depositi PLACE. Le due conversioni fragola→pomodoro a D20–D21 sono programmate, con controllo della cassa; non sono già un trigger di saturazione. Rimangono limiti di liquidazione finale.

L'evoluzione comune da sperimentare è scegliere l'investimento sulla domanda attesa alla produzione: per animali nelle caselle ancora libere, per colture alla successione utile. Il costo comprende acquisto/semi, lavoro, fertilizzante, grano e valore della vendita rinunciata per autoconsumo. Una coltura alternativa deve maturare, essere raccolta, consegnata e venduta entro D30.

## Primo esperimento proposto, non implementato

Conservare le coordinate e il calendario di riferimento. Prima isolare la scelta COW/SHEEP su pascoli ancora liberi a D8, usando la presenza del negozio di lana come regola osservabile da verificare. Questo è un trasferimento parziale del comportamento kiki: non replica il ramo che cambia tre pollai in pascoli. Tenere invariati gli altri animali e le colture per misurarne l'effetto.

Poi valutare separatamente la conversione a pomodoro, con produzione propria e avversaria attesa e domanda dei negozi, anziché reagire soltanto al prezzo odierno. Infine combinare le due modifiche. Servono confronti accoppiati della policy di base, della modifica animale, della modifica colturale e della combinazione: cassa, margine, quantità vendute, prezzi realizzati, costo del lavoro, mangime e residui. L'obiettivo è migliorare il margine finale evitando eccessi di offerta; smettere di vendere a prezzo basso può da solo peggiorare il risultato.

Nessuna policy modificata o pubblicata in questo approfondimento. [Grafici D1–D30](REPORT.html), [dati sintetici](SUMMARY.json), [transizioni e registri economici](ANALYSIS.json).
'''
    (OUT/'REPORT.md').write_text(text,encoding='utf-8')
    body='<h1>Kiki yi2 · mix animale e saturazione</h1><p>8 replay della submission 56137379 · <b>nessuna sostituzione di animali già presenti</b>. Scelta del mix durante la crescita, con 17 coordinate comuni e due configurazioni di strutture.</p><p>Con negozio lana: 6 mucche e 10 pecore (3 casi). Senza: 8 mucche, 6 pecore, 3 oche (5 casi). Associazione osservata, non efficacia causale dimostrata.</p><p><a href="REPORT.md">Analisi, limiti e prossimo esperimento</a> · <a href="SUMMARY.json">Dati sintetici</a></p><label>Replay <select id="match">'+''.join(f'<option value="{i}">{r["episode"]} · negozi lana D8: {summary[i]["yarn"]}</option>' for i,r in enumerate(rows))+'</select></label>'
    if (OUT.parent/'kiki_variability_extended_20260913/REPORT.html').exists():
        body='<aside><b>Aggiornamento:</b> il campione esteso a 39 replay mostra quattro mix e un controesempio alla regola del negozio lana. <a href="../kiki_variability_extended_20260913/REPORT.html">Apri analisi estesa</a>.</aside>'+body
    for i,r in enumerate(rows):
        body+=f'<section data-i="{i}"'+(' hidden' if i else '')+f'><h2>Episodio {r["episode"]}</h2><a href="https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56137379&amp;episodeId={r["episode"]}">Apri partita Kaggle</a><p>Blu: kiki yi2. Arancio: avversario, salvo diversa legenda nel titolo. Snapshot a fine giornata; assenza di vendite rappresentata con un vuoto.</p><div class="plots">'
        def plot(title,series,unit,names=('kiki yi2','Avversario')):
            charts.NAMES=list(names);return charts.chart(title,series,unit)
        for animal in ['COW','SHEEP','GOOSE']:
            body+=plot(animal+' · animali',[[d[key].get(animal,0) for d in r['daily']] for key in ['own','opponent']],'animali')
        body+=plot('Cassa kiki',[[d['cash'] for d in r['daily']]],'monete')
        body+=plot('Costo lavoro',[[d['hire_cash'] for d in r[key]['daily']] for key in ['ledger','opponent_ledger']],'monete/giorno')
        for item in ['MILK','WOOL','EGG','STRAWBERRY','TOMATO','WHEAT']:
            if item in ['STRAWBERRY','TOMATO','WHEAT']:
                body+=plot(item+' · caselle',[[d[key].get(item,0) for d in r['daily']] for key in ['own','opponent']],'caselle')
            body+=plot(item+' · quantità vendute',[[d['sold_units'].get(item,0) for d in r[key]['daily']] for key in ['ledger','opponent_ledger']],'unità/giorno')
            body+=plot(item+' · blu prezzo fine giornata / arancio realizzato kiki',[[d['prices'][item] for d in r['daily']],[d['sales_cash'].get(item,0)/d['sold_units'][item] if d['sold_units'].get(item,0) else None for d in r['ledger']['daily']]],'monete/unità',('Prezzo fine giornata','Realizzato kiki'))
            body+=plot(item+' · ricavi',[[d['sales_cash'].get(item,0) for d in r[key]['daily']] for key in ['ledger','opponent_ledger']],'monete/giorno')
        body+='</div></section>'
    body+='<script>document.getElementById("match").onchange=e=>document.querySelectorAll("section[data-i]").forEach(s=>s.hidden=s.dataset.i!==e.target.value);</script>'
    (OUT/'REPORT.html').write_text('<!doctype html><html lang="it"><meta charset="utf-8"><title>Kiki yi2 · mix e saturazione</title><style>body{font:16px system-ui;background:#f4f6f2;color:#22362e;max-width:1400px;margin:30px auto;padding:0 24px}p{line-height:1.6}section{background:white;padding:24px;margin-top:20px;border-radius:12px}.plots{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.plot{border:1px solid #ddd;border-radius:8px;padding:14px}svg{width:100%}select{font:inherit;padding:10px}@media(max-width:800px){.plots{grid-template-columns:1fr}}</style>'+body+'</html>',encoding='utf-8')
    print('8 replay, 208 daily SVG charts. No policy edits. Last placement days:',[s['last_placement_day'] for s in summary])
if __name__=='__main__':main()
