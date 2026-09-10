# E20 — target 7–7–2

## Strategia

Obiettivo richiesto il 2026-09-10: conservare pianificazione E19 in Q0/Q1,
riusare l'avvio dei pascoli E18 in Q2 fino a due tile, e raggiungere almeno
l'economia E19 prima del torneo a tre e dell'analisi dei 22 KPI.

Riferimenti immutabili: E18 = `submission_codex_e18_2_capacity_governed_v4d.py`
(7–7–5); E19 = `submission_codex_e18_770_v48_external.py` (7–7–0).
Le indicazioni storiche che rinviavano le topologie alternative sono superate
dalla richiesta corrente. Non viene modificato l'engine.

L'avvio assistito fino a D11 rimane quello di E19. Da D12 il piano biologico,
le rotazioni, i servizi, la certificazione della capacità e le rotte restano
V48, con due posizioni Q2 riservate agli animali: mucca in (4,5) e pecora in
(4,6), coordinate zero-based. Sono due dei cinque pascoli di E18, costruiti
dal riferimento a D12 H4/H8. Il primo troncamento sperimentale usava (3,5)
e (4,5), le prime due posizioni dell'avvio E18; la disposizione selezionata
deriva dall'ottimizzazione della logistica Q2. Il limite globale passa a 16,
distribuito 7/7/2 secondo l'ordine di attivazione dei quadranti.

I due pascoli sono proposte di missione soggette alle verifiche V48 di cassa,
inventario, tempo e servizi. Non sono azioni imposte né acquisti senza fondi.
Le colture evitano le due posizioni riservate. L'assegnazione delle intenzioni
conserva le quote V48 (23 grano / 38 fragole) e l'ordine del piano; soltanto
l'esecuzione sulle due posizioni Q2 viene esclusa, per non riassegnare Q0/Q1.
Non sono 61 colture effettive: i due pascoli ne sottraggono lo spazio.
L'effettiva costruzione e
collocazione deve essere verificata nei replay; il target non prova il risultato.

Il mix selezionato è una mucca e una pecora (E20v18). Q0/Q1 conservano 9 mucche
e 5 pecore. D30 conserva la chiusura V48; non si modifica il mercato in base
a seed o informazioni future.

## Implementazione

- [Policy e varianti](tools/policy.py): estensione isolata del piano V48,
  con controlli sulle sostituzioni del sorgente e riuso del bundle congelato.
- [Runner](tools/run_experiment.py): stagioni complete, doppia posizione,
  replay compressi e hash, topologia e calendario osservati.
- [Builder standalone](tools/build_submission.py) e
  [bundle congelato](../../../../submission/submission_codex_e20_772_e20v18_candidate.py):
  nessun caricamento di file, rete, seed o replay durante il gioco.
- [Audit](tools/audit_results.py): riconciliazione engine di entrambi i lati.
- [Report](tools/build_report.py): 22 pannelli per accoppiamento, CSV e dati.
- [Test](tests/test_e20_contract.py): avvio identico, limiti topologici e
  isolamento dei riferimenti congelati.
- Gli artifact development e baseline sono sotto `artifacts/`; la valutazione
  finale deve usare seed separati, congelati prima di esaminarne i risultati.

## Protocollo economico

Development: confronto matched E20 vs E18 ed E19 vs E18, stesso seed e ruolo.
Soglia primaria: cassa finale media E20 almeno pari a E19; non basta battere E18.
Verificare separatamente completamento, 7–7–2 effettiva, perdite e servizi.
Il torneo finale è un round-robin fra E18, E19 e la variante E20 congelata,
con tutti gli accoppiamenti e i ruoli su seed non usati nel tuning.
Il torneo è simulazione interna; non è evidenza di ranking Kaggle esterno.

Il report mantiene i 22 indicatori V4.1, con viste per accoppiamento e
aggregati bilanciati, checkpoint D1–D30 e ledger economico riconciliato.
Curve aggregate e bande min–max non sono singole traiettorie né intervalli
di confidenza. Risultati e limiti appartengono al report, non a questa specifica.
