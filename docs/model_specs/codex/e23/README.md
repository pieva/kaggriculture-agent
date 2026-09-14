# E23 — nuova architettura dal confronto con i top 2750–3000

Stato: fase preparata il 14 settembre 2026; nessuna policy E23 implementata o pubblicata. La prossima sessione parte dal confronto economico e operativo con i top, usando E22 come controllo congelato.

## Evidenze di partenza

- [Atlante dei top](../e22/reports/top_2750_3000_20260914/REPORT.html): 5 submission, 5 replay competitivi ciascuna, selezione per score 2750–3000 al momento dell'acquisizione. Catalogo, hash, collocamenti e traiettorie sono nello stesso report.
- [Khalid vs E22.1](../e22/reports/top_2750_3000_20260914/KHALID_VS_E22_1.md): 56220723 è la famiglia più regolare, 14 pascoli e 4 pollai in 5/5 replay, uno vuoto. Mix 8C6S3G in 2/5 e 9C5S3G in 3/5. Q3 aperto a D19 H2 solo in 2/5: non attribuire a Q3 da solo il vantaggio di rating.
- [E22.1 vs E22.2 esterne](../e22/reports/external_e22_2_20260914/REPORT.html): 22 KPI, volumi, prezzi, errori operativi e confronti con avversari diversi.
- [Scelta grano/carote in Q2](../e22/reports/e22_1_q2_coop_20260914/REPORT.html): esempio di successione valutata sulla cassa finale e sui percorsi, preservando le ultime fragole.

## Controlli congelati

| Versione | Ruolo per E23 | Ultimo stato registrato |
|---|---|---|
| E22.1, 56206528 | Baseline 8C6S3G, tre pollai Q0 | Pubblicata |
| E22.1 Q2 Grano v1 | Miglioria locale del calendario finale | Complete, submission 56228842; acquisire risultati senza reinviare |
| E22.2, 56212495 | Controllo 8C9S, tre pascoli Q0 | Pubblicata |
| E22.2 fix v1, 56228129 | Controllo delle correzioni meccaniche | Complete; risultati esterni da acquisire |

Il [registro versioni](../e22/VERSIONS.json) contiene bundle e SHA256. Q2 Grano: 20 scenari +68,15 medio, 14/14 confronti diretti vinti, +73,43 medio; questi sono risultati locali. Fix E22.2: meccanica corretta, ma 4/14 vittorie e margine medio −180,29 contro E22.1; non assumerne la superiorità economica.

## Lavoro della prossima sessione

1. Recuperare esito e primi replay delle due nuove submission E22, distinguendo rating iniziale da risultati comparabili. Conservare bundle e campioni originali.
2. Costruire il confronto per fase D1–11, D12–19, D20–30: topologia realmente occupata, calendario di collocamento/raccolta, costo dei lavoratori, trasporto, vendite e prezzi. Separare scelte ricorrenti da fughe, acquisti negati e comandi senza effetto.
3. Quantificare le ipotesi: scelta mucca/pecora in (6,2), oche/pecore Q0, convenienza e tempi di Q3, successioni colturali e consegne condivise. Valutare ricavi marginali meno acquisti, mangime, manodopera e raccolte sacrificate.
4. Disegnare E23 con componenti verificabili: stato osservato e disponibilità, allocazione di capitale/terreno/specie, calendario delle attività, assegnazione dei lavoratori e rotte, gestione scorte/vendite. Sono aree da progettare, non decisioni architetturali già validate.
5. Implementare una prima variante congelata e confronti per singolo intervento. Testare loader reale, contabilità, completamento azioni, alimentazione, irrigazione, overflow e liquidazione D30; produrre il report standard 22 KPI + prezzi.

I semi 180911301–307 sono già esposti. I semi 180912401–407 sono ancora riservati: non usarli per selezionare le ipotesi. Gli avversari riprodotti con azioni registrate servono alla diagnostica; non sostituiscono confronti indipendenti o risultati esterni.

Non copiare una topologia perché compare in un replay con score elevato. Il campione è esplorativo e non fornisce il codice o la logica decisionale dei competitor.

## Riproducibilità e ambiente

Workspace corrente: worktree `756c/kaggriculture-agent`, ramo `codex/e22-2-pascoli-release`. Runtime Python già disponibile in `C:/Users/pietr/Projects/kaggriculture-agent/.venv/Scripts/python.exe`; evitare modifiche all'altro checkout.

I report HTML/CSV, cataloghi e strumenti sono versionati. Replay grezzi, profili riproducibili, log e tentativi scartati restano locali e ignorati da Git. [Catalogo di chiusura E22](../e22/reports/closeout_20260914/README.md). La richiesta di preparare E23 non avvia automaticamente una nuova task o una nuova submission.
