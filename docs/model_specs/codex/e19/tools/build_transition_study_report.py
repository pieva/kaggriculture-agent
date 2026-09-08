"""Trace-backed transition analysis and two isolated diagnostic experiments."""
import base64
import hashlib
import json
import os
from pathlib import Path
from statistics import mean

ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'docs/model_specs/codex/e19'
DATA=BASE/'artifacts/derived/transition_study_20260907'
OUT=BASE/'reports/transition_study_20260907'
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'scratch/matplotlib_kpi'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from markdown_it import MarkdownIt


def fmt(x):return f'{x:,.1f}'.replace(',','X').replace('.',',').replace('X','.')


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    cases=[(s,t) for s in range(180903001,180903004) for t in (0,1)]
    oldpaths=[DATA.parent/'assisted_770_d30_20260907'/f'{s}_{t}.json' for s,t in cases]
    old=[json.loads(p.read_text()) for p in oldpaths]
    groups={'Base':[dict(p,sides={'candidate':p['sides']['assisted'],'v4d':p['sides']['v4d']}) for p in old]}
    for label,key in [('Valore CARE','care_value'),('Ponte WATER','water_bridge')]:
        groups[label]=[json.loads((DATA/f'{key}_{s}_{t}.json').read_text()) for s,t in cases]
    trace=json.loads((DATA/'baseline_180903001_0.json').read_text())
    summary={}
    for label,group in groups.items():
        cash=mean(p['sides']['candidate']['reward'] for p in group)
        reference=mean(p['sides']['v4d']['reward'] for p in group)
        summary[label]=dict(cash=cash,reference=reference,relative_pct=100*(cash/reference-1),
            wins=sum(p['sides']['candidate']['reward']>p['sides']['v4d']['reward'] for p in group),
            d12_care=mean(p['sides']['candidate']['ledger']['daily'][11]['executed_actions'].get('CARE',0) for p in group),
            d12_plants=mean(sum(p['sides']['candidate']['ledger']['daily'][11]['planted'].values()) for p in group),
            d15_strawberry=mean(p['sides']['candidate']['daily'][14]['crops']['STRAWBERRY'] for p in group),
            deaths=sum(len(p['sides']['candidate']['crop_starvation']) for p in group),
            escapes=sum(len(p['sides']['candidate']['ledger']['animal_escapes']) for p in group),
            incomplete=sum(p.get('incomplete',p.get('incomplete_missions',0))>0 for p in group))
    bridge_events=sum(len(p['bridge_events']) for p in groups['Ponte WATER'])
    bridge_equal=sum(p['prefix_parity'] for p in groups['Ponte WATER'])
    first=trace['trace'][0]
    urgent=sum(s['priority']==3 and ['WATER'] in s['commands'] for s in first['unclaimed_services'])
    urgent+=sum(any(c==['WATER'] for c,pos in j['steps']) for j in first['active'].values())
    day12=trace['sides']['candidate']['ledger']['daily'][11]
    move_share=100*day12['requested_actions'].get('MOVE',0)/sum(day12['requested_actions'].values())
    fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained')
    for label,color in zip(groups,['#176b9b','#b75a2c','#6d55a4']):
        group=groups[label]
        for ax,key,title in [(axes[0,0],'CARE','CARE eseguiti'),(axes[0,1],'WATER','WATER eseguiti')]:
            ax.plot(range(11,21),[mean(p['sides']['candidate']['ledger']['daily'][d-1]['executed_actions'].get(key,0) for p in group) for d in range(11,21)],label=label,color=color,lw=2)
            ax.set_title(title)
        axes[1,0].plot(range(11,21),[mean(p['sides']['candidate']['daily'][d-1]['crops']['STRAWBERRY'] for p in group) for d in range(11,21)],label=label,color=color,lw=2)
        axes[1,1].plot(range(11,21),[mean(sum(p['sides']['candidate']['ledger']['daily'][d-1]['planted'].values()) for p in group) for d in range(11,21)],label=label,color=color,lw=2)
    axes[1,0].set_title('Piante di fragole');axes[1,1].set_title('Nuove piantagioni eseguite')
    for ax in axes.flat:ax.grid(alpha=.2);ax.axvline(11.5,color='#444',ls=':');ax.set_xticks(range(11,21));ax.legend(fontsize=8);ax.set_xlabel('Giorno')
    fig.savefig(OUT/'esperimenti.png',dpi=140);fig.savefig(OUT/'esperimenti.svg');plt.close(fig)
    lines=['# Studio della transizione D11–D15 · 770 assistita','',
           '## Conclusione','',
           '**Il collo di bottiglia immediato è il servizio ereditato, non la mancanza di cassa.** Nel caso tracciato D12 comincia con 25 irrigazioni urgenti: il core assegna i primi lavoratori a WATER, rinvia la crescita e completa solo 6 CARE. La diversa valutazione dei CARE esiste nel codice, ma correggerla da sola non sblocca D12.', '',
           'Questo studio comprende una riproduzione integrale strumentata della base e due esperimenti su tre semi di sviluppo, entrambe le posizioni. È una diagnosi locale: non modifica né promuove le submission congelate.', '',
           '## Ricostruzione del passaggio nel caso 180903001 / posizione 0','',
           f'- Cassa iniziale D12: **{fmt(first["cash"])}**; riserva di manutenzione stimata dal core: **{fmt(first["maintenance_floor"])}**. La liquidità non è il vincolo attivo di questa apertura.',
           f'- Irrigazioni urgenti: **{urgent}** (24 offerte ancora non assegnate più la missione WATER già assegnata al contadino). Nel core priorità 3 significa rischio biologico e prevale sul valore economico delle alternative.',
           '- A H1 non ci sono manovali: il reset giornaliero richiede nuove assunzioni. Il core osserva 6 manovali a H2, 7 a H3 e 12 a H4; i lavoratori disponibili vengono assegnati a visite WATER separate.',
           f'- D12 registra **{day12["requested_actions"].get("MOVE",0)} movimenti**, pari al **{fmt(move_share)}%** dei comandi richiesti, **{day12["requested_actions"].get("PASS",0)} PASS**, **{day12["executed_actions"].get("CARE",0)} CARE** e **{sum(day12["planted"].values())} piantagioni**.',
           '- Il terreno aggiuntivo viene acquistato a H2, ma la capacità agricola non viene immediatamente occupata. Si espande la superficie prima di riuscire ad aumentare il lavoro produttivo svolto.', '',
           '| Giorno | Cassa a inizio giorno | CARE | Nuove piantagioni | MOVE | PASS | Rifiuti di crescita per percorsi |','|---|---:|---:|---:|---:|---:|---:|']
    for day in range(12,16):
        ts=[t for t in trace['trace'] if t['day']==day];f=trace['sides']['candidate']['ledger']['daily'][day-1]
        lines.append(f'| D{day} | {fmt(ts[0]["cash"])} | {f["executed_actions"].get("CARE",0)} | {dict(f["planted"])} | {f["requested_actions"].get("MOVE",0)} | {f["requested_actions"].get("PASS",0)} | {sum(t["metric_delta"].get("growth_rejected_day_route",0) for t in ts)} |')
    lines+=['', 'I rifiuti sono valutazioni ripetute, non altrettanti investimenti indipendenti persi. I PASS non sono necessariamente tutti riutilizzabili: contano posizione, inventario e tempo residuo. La traccia dopo l’assegnazione conserva posizioni, inventari, missioni, riserve e servizi non assegnati per ogni ora D12–D15.', '',
            '### Controllo operativo: V4D nella stessa partita a D12', '',
            'Le 25 irrigazioni sono un carico ereditato reale, ma non dimostrano un’impossibilità fisica di crescere. La V4D avversaria parte dalla stessa apertura e utilizza una diversa organizzazione del lavoro:', '',
            '| D12, seed 180903001 | Core nuovo | V4D avversaria |','|---|---:|---:|',
            '| MOVE richiesti | 192 | 130 |',
            '| WATER eseguiti | 25 | 46 |',
            '| CARE eseguiti | 6 | 19 |',
            '| Nuove piantagioni | 0 | 21 |',
            '| PASS richiesti | 34 | 17 |',
            '| Manovali al checkpoint | 12 | 12 |', '',
            'Le 21 piantagioni V4D sono 8 meloni, 12 grani e 1 fragola. La V4D espande anche il bestiame oltre il perimetro 770: non è un confronto a portafoglio finale identico. Tuttavia, il minor numero di movimenti insieme al maggior servizio eseguito rafforza l’ipotesi che il coordinamento dei percorsi sia una leva concreta; la sola liquidità o il solo numero massimo di manovali non spiegano il divario.', '',
            '## Tre meccanismi distinti','',
            '1. **Precedenza biologica:** il punteggio distingue in modo assoluto le urgenze di priorità 3. Un bonus economico ai CARE di priorità inferiore non può cambiare le prime assegnazioni quando l’irrigazione è urgente.',
            '2. **Valore dei CARE incompleto:** `_services` valuta il latte/lana già raccoglibile e il fertilizzante disponibile, ma non accredita il prodotto futuro aggiuntivo del CARE. Il motore accumula il bonus solo con animale nutrito e curato, dopo l’eventuale produzione del refresh.',
            '3. **Percorsi e ammissione della crescita:** le nuove piantagioni devono lasciare spazio al piano dei servizi osservati. Il certificato include anche attività facoltative, mentre i percorsi operativi sono organizzati per missione su una singola casella. È plausibile che il loro coordinamento limiti la crescita; questa prova non dimostra che sia sicuro eliminare il certificato.', '',
            '## Esperimenti isolati','',
            '**Valore CARE:** aggiunge al servizio una stima marginale di un’unità di latte/lana, usando il prezzo osservato diviso per il ritardo alla successiva produzione utile. Non accredita bonus già saturi. È una stima diagnostica conservativa, non un modello esatto di tutte le produzioni future né ricavo garantito: restano necessari alimentazione, spazio e raccolta. Il risultato riguarda questa specifica stima, non ogni possibile valorizzazione dei CARE. Apertura D1–D11 identica alla base, stessi vincoli e stesso certificato.', '',
            '**Ponte WATER:** nella sola D11 sostituisce un PASS con WATER se il lavoratore si trova già su una coltura non irrigata, senza muoverlo né cambiare acquisti e raccolte programmati. Verifica se esistono opportunità gratuite per ridurre il servizio urgente ereditato. Il controllo richiede la stessa cassa di chiusura D11 e 72 meloni raccolti.', '',
            '| KPI, stessi 6 casi | Base | Valore CARE | Ponte WATER |','|---|---:|---:|---:|']
    for key,title in [('cash','Cassa finale candidata'),('reference','Cassa finale V4D avversaria'),('relative_pct','Scarto relativo rispetto a V4D (%)'),('wins','Vittorie su 6'),('d12_care','CARE D12'),('d12_plants','Piantagioni D12'),('d15_strawberry','Fragole D15'),('deaths','Morti colture'),('escapes','Fughe animali'),('incomplete','Casi con missioni residue')]:
        lines.append('| '+title+' | '+' | '.join(fmt(summary[k][key]) for k in groups)+' |')
    lines+=['',f'Il valore CARE cambia la cassa media di **{fmt(summary["Valore CARE"]["cash"]-summary["Base"]["cash"])}** rispetto alla base. Il confronto relativo con V4D passa da **{fmt(summary["Base"]["relative_pct"])}%** a **{fmt(summary["Valore CARE"]["relative_pct"])}%**. La maggiore cassa osservata nel primo caso non si conferma come miglioramento medio.', '',
            f'Il ponte WATER ha effettuato **{bridge_events} sostituzioni** complessive; **{bridge_equal}/6** prefissi sono rimasti identici anche come azioni. '+('Non c’erano PASS utilizzabili sulle colture non irrigate: è un controllo nullo, non una smentita dell’utilità di preparare l’irrigazione prima del passaggio.' if bridge_events==0 else 'Le sostituzioni e i loro effetti sono conservati nei dati. La parità di cassa D11 e raccolto dei meloni è verificata in ciascun caso.'), '',
            '![Risultati operativi degli esperimenti](esperimenti.png)', '',
            '## Decisione e prossimo intervento proposto','',
            '**Nessuna promozione del solo bonus CARE.** Non risolve il blocco D12 e non migliora il risultato medio del campione. Il ponte WATER è una prova della disponibilità di azioni libere, non un nuovo pianificatore di irrigazione.', '',
            'La prossima modifica da isolare è una **preparazione operativa del passaggio**, con gruppi di visite vicine per irrigare e servire gli animali, seguita dall’ammissione delle nuove colture. Il criterio di rilascio della guida deve considerare le obbligazioni effettivamente eseguibili dalla squadra e il lavoro residuo, oltre alla data e alla cassa. Non basta prolungare il calendario storico o forzare più fragole.', '',
            'Criteri di verifica: conservare raccolto e cassa D11; zero perdite biologiche; ridurre percorrenze e servizio residuo D12; misurare CARE realmente produttivi, nuove piantagioni D12–D15 e raccolti successivi; accettare solo un miglioramento confermato del confronto con V4D fino a D30. Non abbassare i vincoli di sopravvivenza per ottenere più crescita apparente.', '',
            '## Evidenza e limiti','',
            '- Base strumentata seed 180903001, posizione 0: tutti i KPI, flussi, scorte terminali e risultati D1–D30 di entrambi i lati coincidono con il run già consolidato. La strumentazione non cambia la policy.',
            '- Esperimenti su seed 180903001–180903003, posizioni 0 e 1; sei casi per variante, confrontati con gli stessi sei casi della base. Sono semi di sviluppo, non validazione esterna.',
            '- Mercato endogeno: ogni variante può cambiare anche il comportamento e gli incassi di V4D. Si riportano sempre entrambi i lati e il rapporto fra le medie.',
            '- Il meccanismo dettagliato dei 25 WATER è documentato nel caso tracciato; non va automaticamente generalizzato a qualsiasi stato futuro o topologia.',
            '- Nessuna modifica alla 770 congelata, alla 662 o alla V4D pubblicata; nessuna nuova submission. Le prove sono adattatori locali riproducibili.', '',
            '[Sintesi numerica](summary.json) · [Manifest delle fonti](manifest.json).','']
    md=OUT/'REPORT_TRANSIZIONE_D11_D15_IT.md';md.write_text('\n'.join(lines),encoding='utf-8')
    html=MarkdownIt().enable('table').render(md.read_text(encoding='utf-8'))
    html=html.replace('src="esperimenti.png"','src="data:image/png;base64,'+base64.b64encode((OUT/'esperimenti.png').read_bytes()).decode()+'"')
    css='body{max-width:1100px;margin:40px auto;padding:0 24px;font:17px/1.6 system-ui;color:#243445}img{max-width:100%}h2{margin-top:2em}table{display:block;overflow:auto;border-collapse:collapse;font-size:14px}td,th{padding:8px;border-bottom:1px solid #ddd;text-align:right}td:first-child,th:first-child{text-align:left}th{background:#edf2f7}'
    md.with_suffix('.html').write_text('<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Studio transizione D11–D15</title><style>'+css+'</style><body>'+html+'</body></html>',encoding='utf-8')
    (OUT/'summary.json').write_text(json.dumps(dict(groups=summary,bridge_events=bridge_events,bridge_identical_prefixes=bridge_equal,diagnostic_case_urgent_water=urgent),indent=2)+'\n')
    files=oldpaths+list(DATA.glob('*.json'))+[Path(__file__),BASE/'tools/study_transition.py',BASE/'tools/study_transition_water.py',ROOT/'submission/submission_codex_e18_770_assisted_start_v1_candidate.py']
    (OUT/'manifest.json').write_text(json.dumps(dict(source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},output_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.name!='manifest.json'}),indent=2)+'\n')
    print(json.dumps(dict(groups=summary,bridge_events=bridge_events),indent=2))


if __name__=='__main__':main()
