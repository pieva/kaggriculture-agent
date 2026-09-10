"""Final decision report, derived only from completed audited cohorts."""
import hashlib
import json
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'docs/model_specs/codex/e20'
OUT=BASE/'reports/e20_1'

def read(p):return json.loads(p.read_text())
def fmt(n):return f'{n:,.2f}'.replace(',','X').replace('.',',').replace('X','.')

def main():
    paths=[OUT/'development/evaluation.json',OUT/'confirmation/evaluation.json',
        BASE/'reports/e20_1_confirmation/data.json',OUT/'topology_control/evaluation.json',
        BASE/'artifacts/E20_1_CONFIRMATION_VERIFICATION.json',BASE/'artifacts/E20_1_DEVELOPMENT_GATE.json']
    dev,fresh,tournament,control,verification,gate=map(read,paths)
    assert verification['technical_verification_passed'] and gate['passed']
    assert dev['complete_both_seats'] and fresh['complete_both_seats']
    assert len(control['matched'])==10
    control_proof=OUT/'verification_e20_1_control_C770.json'
    cp=read(control_proof)
    assert cp['passed'] and len(cp['cases'])==10
    paths.append(control_proof)
    c=fresh['summary']['E20.1'];ref=fresh['summary']['E19'];d=dev['summary']['E20v28']
    promoted=c['gate_passed']
    status='Confermata nel test locale indipendente' if promoted else 'Non promossa: il gate indipendente non è superato'
    old=dev['summary']['E20v18'];ctrl=control['summary']['C770'];c772=control['summary']['E20v28']
    topology_deltas=[r['E20v28']-r['C770'] for r in control['matched']]
    economics={}
    for model in ['E19','E20.1']:
        sides=[]
        for row in fresh['matched']:
            seat,seed=row['seat'],row['seed']
            stem=f'{model}_E18_{seed}' if seat==0 else f'E18_{model}_{seed}'
            p=BASE/'artifacts/e20_1_confirmation'/f'{stem}.kpi.json'
            sides.append(read(p)['sides'][seat])
        economics[model]=dict(
            sales=mean(sum(sum(day['sales_cash'].values()) for day in s['ledger']['daily']) for s in sides),
            purchases=mean(sum(sum(day['purchase_cash'].values()) for day in s['ledger']['daily']) for s in sides),
            hires=mean(sum(day['hire_cash'] for day in s['ledger']['daily']) for s in sides),
            land=mean(sum(day['land_cash'] for day in s['ledger']['daily']) for s in sides),
            unit_cash=mean(sum(day['unit_cash_delta'] for day in s['ledger']['daily']) for s in sides),
            products={product:dict(
                harvested=mean(sum(day['harvested'].get(product,0) for day in s['ledger']['daily']) for s in sides),
                sales=mean(sum(day['sales_cash'].get(product,0) for day in s['ledger']['daily']) for s in sides))
                for product in ['WHEAT','MELON','STRAWBERRY','MILK','WOOL']})
    changes={k:economics['E20.1'][k]-economics['E19'][k] for k in ['sales','purchases','hires','land','unit_cash']}
    residual=c['delta_vs_E19']-(changes['sales']-changes['purchases']-changes['hires']-changes['land']+changes['unit_cash'])
    assert abs(residual)<1e-6,('Unreconciled economic difference',residual)
    (OUT/'ECONOMIC_DECOMPOSITION.json').write_text(json.dumps(dict(models=economics,changes=changes,residual=residual),indent=2)+'\n')
    runtime=[]
    for stage in ['e20_1_confirmation','e20_1_control']:
        for p in (BASE/'artifacts'/stage/'invalid_under_load').glob('*.json'):
            if '.kpi.' in p.name:continue
            r=read(p)
            runtime.append(dict(stage=stage,case=p.name,agents=r['agents'],
                calls=[v['calls'] for v in r['runtime']],overage=[v['overage_seconds'] for v in r['runtime']]))
    lines=['# E20.1 — sviluppo, conferma e traiettorie dei 22 KPI','',f'**{status}.**','',
        f"La candidata E20v28 conserva la topologia 7–7–2 e l'apertura di E19 fino a D11. Su 20 partite di sviluppo raggiunge {fmt(d['cash'])} contro {fmt(dev['summary']['E19']['cash'])} di E19 (+{fmt(d['delta_percent_vs_E19'])}%). Su 14 confronti appaiati indipendenti contro E18, il delta diventa {fmt(c['delta_percent_vs_E19'])}%; seed con delta positivo: {c['positive_seeds_vs_E19']}/{c['seed_count']}.",
        '', '[Apri il torneo interattivo con i 22 KPI](../e20_1_confirmation/REPORT.html) · [Confronto indipendente appaiato](confirmation/REPORT.html)',
        '', '## Cosa cambia', '',
        '1. A parità di urgenza, il pianificatore inserisce prima i tile più lontani dal lavoratore disponibile più vicino. Conserva le priorità e i vincoli di costo e capacità; modifica lo stesso ordinamento nei percorsi e nei certificati.',
        '2. Il piano omette CARE quando non può aggiungere produzione: bonus già saturo oppure nessuna produzione residua utile. Tiene conto del consumo notturno del vecchio bonus prima di immagazzinare quello odierno.',
        '', 'Q2 resta una mucca in (4,5) e una pecora in (4,6). Target 10 mucche e 6 pecore, massimo 12 braccianti. Le intenzioni colturali di Q0/Q1 e l’apertura assistita sono conservate; i servizi effettivi dopo D11 cambiano con il pianificatore.',
        '', '## Sviluppo e prove scartate','',
        'Cinque nuove varianti sono state provate su tutti i dieci seed già conosciuti, prima di scegliere la combinazione. L’estensione della protezione idrica e il solo accesso fuori coda azzerano lo stress ma peggiorano la cassa del 16,69% e del 20,36% rispetto a E19 nel primo screen. I percorsi distanti e il filtro CARE vengono invece verificati separatamente e poi combinati.',
        '', '| Modello, sviluppo appaiato | Cassa media | Stress / partita | Perdite animali |',
        '|---|---:|---:|---:|']
    for m,label in [('E19','E19'),('E20v18','E20 precedente'),('E20v28','E20.1')]:
        v=dev['summary'][m];lines.append(f"| {label} | {fmt(v['cash'])} | {fmt(v['stress'])} | {v['animal_losses']} |")
    lines+=['',f"Rispetto alla E20 precedente, lo stress di sviluppo scende da {fmt(old['stress'])} a {fmt(d['stress'])}; WATER varia di {fmt(d['actions']['WATER']-old['actions']['WATER'])} azioni per stagione, CARE di {fmt(d['actions']['CARE']-old['actions']['CARE'])}, MOVE di {fmt(d['actions']['MOVE']-old['actions']['MOVE'])}. Il risultato non dipende dal semplice aumento dei WATER o dalla riduzione dei PASS.",
        '', '[Screen completo](screen/REPORT.html) · [Sviluppo in entrambi i ruoli](development/REPORT.html) · [Ablation appaiata dei percorsi](paired_ablation/REPORT.html)',
        '', '## Conferma su sette seed nuovi','',
        '| Modello contro E18 | Cassa media | Mediana | Minimo | Stress / partita | Perdite animali |',
        '|---|---:|---:|---:|---:|---:|']
    for m in ['E19','E20.1']:
        v=fresh['summary'][m];lines.append(f"| {m} | {fmt(v['cash'])} | {fmt(v['median_cash'])} | {fmt(v['min_cash'])} | {fmt(v['stress'])} | {v['animal_losses']} |")
    lines+=['',f"Differenza media E20.1−E19: {fmt(c['delta_vs_E19'])}; mediana delle differenze per seed: {fmt(c['median_seed_delta_vs_E19'])}; peggiore differenza per seed: {fmt(c['worst_seed_delta_vs_E19'])}. Gli scambi di ruolo non sono nuove repliche indipendenti.",
        '', 'La candidata è stata congelata prima di questa coorte. Nessuna variazione di strategia, parametri o seed durante la conferma. Il gate richiede economia almeno E19, mediana positiva delle differenze, miglioramento nella maggioranza dei seed, stress non superiore a E19 e zero perdite animali.',
        '', '## Dove cambia la cassa, a parità di avversario','',
        f"Rispetto a E19, E20.1 cambia le vendite di {fmt(changes['sales'])}, gli acquisti di {fmt(changes['purchases'])}, le assunzioni di {fmt(changes['hires'])} e gli acquisti di terreno di {fmt(changes['land'])}; il saldo delle azioni sul campo cambia di {fmt(changes['unit_cash'])}. Queste componenti riconciliano la differenza finale di cassa.",
        '', '| Prodotto | Quantità raccolta E19 | Quantità raccolta E20.1 | Delta incassi E20.1−E19 |',
        '|---|---:|---:|---:|']
    for product in economics['E19']['products']:
        x=economics['E19']['products'][product];y=economics['E20.1']['products'][product]
        lines.append(f"| {product} | {fmt(x['harvested'])} | {fmt(y['harvested'])} | {fmt(y['sales']-x['sales'])} |")
    lines+=['','Quantità raccolta e incassi sono grandezze distinte: dividere queste colonne non restituisce necessariamente il prezzo delle vendite. La scomposizione è contabile; non attribuisce causalmente tutto il delta a un singolo intervento, perché il mercato e l’avversario reagiscono. [Dati della scomposizione](ECONOMIC_DECOMPOSITION.json).',
        '', 'Il problema residuo da verificare è il margine economico di Q2 e la monetizzazione della produzione. In questa coorte E20.1 raccoglie più latte ma ne ricava meno, mentre la lana aumenta sia in quantità sia in incassi; diminuiscono anche gli incassi delle fragole. Una successiva revisione può confrontare il mix dei due pascoli e le decisioni di vendita con questo pianificatore, usando prezzi osservati e nuovi seed di conferma. È un’ipotesi di lavoro, non un miglioramento già dimostrato.',
        '', '## Torneo E18 / E19 / E20.1','',
        '| Modello | Vittorie / partite | Cassa media complessiva |',
        '|---|---:|---:|']
    for m,v in tournament['summary'].items():lines.append(f"| {m} | {v['wins']} / {v['matches']} | {fmt(v['mean_cash'])} |")
    lines+=['','42 partite, 7 seed e tutte le coppie in entrambi i ruoli. La classifica include due avversari diversi per modello; il confronto economico appaiato sopra mantiene invece fisso E18. Il report interattivo presenta tutti i 22 KPI, mediana e intervallo min–max, e tabelle per le tre fasi D1–D10, D11–D20 e D21–D30.',
        '', '## Il controllo con lo stesso pianificatore e topologia 770','',
        f"Sui dieci seed già esposti, in posizione 0 contro E18, C770 chiude a {fmt(ctrl['cash'])} e la 772 E20.1 a {fmt(c772['cash'])}: differenza {fmt(mean(topology_deltas))}, positiva in {sum(x>0 for x in topology_deltas)}/10 casi. Stress {fmt(ctrl['stress'])} contro {fmt(c772['stress'])}; perdite animali {ctrl['animal_losses']} contro {c772['animal_losses']}.",
        '', 'C770 usa lo stesso bundle e gli stessi due interventi, ma senza animali o riserve Q2, target 14 e mix 9 mucche / 5 pecore. È un controllo di ricerca, non una nuova versione ufficiale di E19. Il confronto non misura il mero margine contabile di due animali: cambiano anche colture, percorsi, mercato e risposta dell’avversario. È uno screen su seed conosciuti, non una seconda conferma indipendente.',
        '', '[Controllo topologico e 22 KPI](topology_control/REPORT.html)',
        '', '## Verifiche e completezza','',
        '- Apertura identica e limiti intragiornalieri 7–7–2 verificati su tutta la coorte di sviluppo; nella conferma l’apertura viene confrontata nelle 14 condizioni con avversario comune E18.',
        '- Parità completa delle 719 azioni fra sorgente e standalone su due seed e due ruoli. Nove test di contratto superati, compreso il divieto di accesso a file esterni durante la creazione del bundle.',
        '- I ledger riconciliano i saldi con l’engine. WATER, FEED e CARE derivano dalle esecuzioni riuscite, non dalle proposte.',
        f"- {len(runtime)} tentativi sotto carico sono archiviati perché uno degli agenti non ha ricevuto tutte le 719 chiamate. Gli stessi casi sono stati ripetuti con un solo processo e con identici bundle, seed e limiti di gioco. I tentativi incompleti non entrano nelle medie. Non è stato escluso alcun seed dal protocollo.",
        '', 'Il campo condiviso `step`, salvato dal replay soltanto nel ruolo 0, viene ricostruito anche per il ruolo 1 senza copiare dati privati. Questo corregge il lettore di validazione; il bundle non è stato modificato.',
        '', '## Decisione e artefatti','',
        ('E20.1 supera il gate indipendente definito prima dei risultati. È una candidata locale verificata; la superiorità esterna richiede partite esterne.' if promoted else 'E20.1 resta sperimentale. Il miglioramento nello sviluppo non soddisfa il gate indipendente e non giustifica la sostituzione automatica dei riferimenti. I risultati operativi e i casi negativi sono conservati nel report, senza reinterpretare a posteriori la soglia di promozione.'),
        '', '[Bundle E20.1](../../../../../../submission/submission_codex_e20_772_e20v28_candidate.py) · [Specifica](../../E20_1_SPEC.md) · [Protocollo](../../E20_1_PROTOCOL.json) · [Verifica indipendente](../../artifacts/E20_1_CONFIRMATION_VERIFICATION.json)',
        '', f"SHA256 della candidata: `{verification['frozen_candidate_sha256']}`. Nessuna nuova submission Kaggle."]
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    from markdown_it import MarkdownIt
    body=MarkdownIt('commonmark').enable('table').render('\n'.join(lines))
    page='''<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>E20.1 — report finale</title><style>body{font:16px/1.65 system-ui;background:#f4f6f8;color:#203047;margin:0}main{max-width:1050px;margin:auto;padding:32px}h1{font-size:32px}h2{margin-top:38px}a{color:#146fac}table{border-collapse:collapse;display:block;overflow:auto;background:white;max-width:100%}th,td{padding:9px 13px;border-bottom:1px solid #dce2eb;text-align:right;white-space:nowrap}td:first-child,th:first-child{text-align:left}code{overflow-wrap:anywhere;font-size:12px}@media(max-width:600px){main{padding:18px}h1{font-size:27px}table{font-size:13px}}</style><main>'''+body+'</main></html>'
    (OUT/'REPORT.html').write_text(page,encoding='utf-8')
    decision=dict(status=status,promoted=promoted,development=d,confirmation=c,control770=ctrl,
        runtime_archives=runtime,bundle_sha256=verification['frozen_candidate_sha256'],
        sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths+[Path(__file__)]})
    (OUT/'DECISION.json').write_text(json.dumps(decision,indent=2)+'\n')
    print(json.dumps(dict(status=status,development_delta=d['delta_percent_vs_E19'],confirmation_delta=c['delta_percent_vs_E19'],promoted=promoted)))

if __name__=='__main__':main()
