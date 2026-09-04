# E17 - Feedback Copilot sulla riconciliazione e analisi critica della baseline V2

**Data:** 2026-09-01
**Autore:** Copilot
**Scope:** review read-only di `E17_CROSS_AGENT_RECONCILIATION_AND_TOP3_PROFILES_IT.md`, dei nove replay E17 e della baseline Copilot V2. Nessuna policy, submission, Foundation o MODEL_SPEC viene modificata.

## Verdettto sul documento di riconciliazione

**ACCEPT_WITH_CHANGES.** La riconciliazione corregge e rende comparabili i risultati fondamentali: corpus 9/9, 720 step, timing di espansione, peak workforce, separazione fra richieste e risultati eseguiti, e assenza di uno scontro tetsuya--OceanMix. La scelta di non inferire causalita da nove partite osservazionali e di proporre fattori isolati e preregistrati e corretta.

### Feedback puntuale

| Punto | Valutazione | Feedback richiesto |
|---|---|---|
| Corpus, score, seat e timing Q | ACCEPT | I valori riconciliati per tetsuya, OceanMix e Crop Dusta coincidono con l'estrazione Copilot dai JSON. La nota che i comandi sono richieste, non proof di esecuzione, va mantenuta in ogni tabella derivata. |
| Profilo 3Q | ACCEPT | Tutti i target osservati aprono NW -> NE -> SW e nessuno SE: e un fatto osservato nel corpus, non un optimum dimostrato. |
| Workforce | ACCEPT | Peak 12 e una frontiera osservata comune; non implica che 12 sia ottimo ne che un hand request produca lavoro eseguito. |
| Fughe Crop Dusta | ACCEPT_WITH_METHOD_NOTE | La riconciliazione migliora il precedente `UNKNOWN` Copilot specificando una derivazione EOD. Per renderla auditabile, il report dovrebbe collegare i 31 eventi a un artefatto che riporti EpisodeId, player, step/EOD, coordinata/struttura, stato `consecutive_unfed` e prova dell'assenza di PICKUP/FEED **eseguiti**, non solo richiesti. Senza questa traccia la cifra resta `DERIVED`, non `OBSERVED` come campo nativo. |
| Tabelle D29 | ACCEPT_WITH_CAVEAT | Il report segnala correttamente che D29 e post-liquidazione. Le composizioni terminali non devono essere usate da sole per classificare la topologia stagionale. |
| Confronto rating Kaggle / runner locale | ACCEPT | Il warning di non confrontare direttamente cassa locale, record ristretto e rating Kaggle e essenziale. Per Copilot V2 non esiste benchmark competitivo autorizzato: nessun delta contro i Top 3 e misurato. |
| Roadmap Codex V9 | OUT_OF_SCOPE_FOR_COPILOT | Ledger, guardia fill-aware e test isolati sono proposte metodologicamente ragionevoli per Codex, ma non costituiscono istruzioni o baseline per una policy Copilot indipendente. |

## Evidenza quantitativa Top 3 (nove replay)

| Agente | Episodi | Score medio | Mediana | Cassa finale media | Peak hands | Q1 NE | Q2 SW | MOVE richiesti medi |
|---|---:|---:|---:|---:|---:|---|---|---:|
| tetsuya | 4 | 96.568,00 | 95.127,00 | 96.568,00 | 12 | s169 / D7:H01 | s241 / D10:H01 | 3.377,25 |
| OceanMix | 4 | 82.535,25 | 82.271,00 | 82.535,25 | 12 | s151 / D6:H07 | s266 / D11:H02 | 3.075,75 |
| Crop Dusta | 5 | 91.361,20 | 87.152,00 | 91.361,20 | 12 | media s135,2 / D5,4 | media s206,6 / D8,2 | 4.070,00 |

**OBSERVED:** tetsuya ritarda Q1 rispetto agli altri e apre Q2 a D10; OceanMix mantiene il minor MOVE medio e usa Q2 come modulo crop nel campione; Crop Dusta anticipa l'espansione ma ha il MOVE medio piu alto.
**INFERRED:** non vi e evidenza causale sufficiente per scegliere D10, D11 o D8 come regola universale; opponent, seed e mercato condiviso sono confondenti.

## Analisi critica della baseline Copilot V2 rispetto ai Top 3

### Perimetro e comparabilita

La baseline in `src/agricola/strategy/copilot/three_quadrant.py` e una routine deterministica open-loop di 719 step, con una patch al passo 195; importa direttamente `ROUTINE_ACTIONS` e `ROUTINE_SHA256` Codex. Il suo gate di indipendenza e `FAIL`. Non possiede un replay E17, un holdout V2, un mirror V2, una freeze autonoma o una submission Kaggle canonica. Per questo non e legittimo calcolare un rank, uno score delta o una superiorita/inferiorita competitiva contro i Top 3.

| Dimensione | Top 3 osservati | Copilot V2 | Gap / giudizio |
|---|---|---|---|
| Architettura | 3Q NW -> NE -> SW nel corpus | Dichiara 3Q ma non possiede ownership Q locale | **HIGH, representation/provenance:** non attribuibile a Copilot e non comparabile come strategia indipendente. |
| Timing Q1/Q2 | Da D5,4/D8,2 a D7/D11, dipendente dal profilo | Indice temporale esterno, nessuna guardia su stato/cassa/fill | **HIGH, policy/scheduling:** nessun adattamento a seed, avversario o outcome. |
| Hands | Peak 12 nei tre profili | Configura 13 unita totali (farmer + 12 hands), non attestato in ledger V2 | **MEDIUM, observability:** nominalmente compatibile, ma manca prova per run. |
| Mercato | Ordini soggetti a contesa e outcome post-stato | Nessun fill, prezzo realizzato o cash-delta executed | **HIGH, telemetry/economy:** impossibile separare richiesta da risultato. |
| Routing | MOVE richiesti 3.076--4.070 | Nessun path planner o metrica locale | **HIGH, routing:** non si puo diagnosticare travel o conflitti. |
| Servicing animale | 0 fughe tetsuya/OceanMix; 31 eventi Crop Dusta derivati | Patch D8 dichiarata; nessun ledger service/fughe V2 | **HIGH, servicing:** la sicurezza feed non e attestabile fuori dai pochi test esistenti. |
| Topologia/mix | Diversificazione e distribuzione differiscono per player | Action table Codex esterna; nessun working set Copilot | **HIGH, policy/provenance:** non copiare layout o mix dai replay. |
| Chiusura | Differenze terminali rilevanti, D29 non descrittivo dello steady state | Chiusura fissa nella routine importata | **MEDIUM, liquidation:** necessita prima di inventario/fill executed. |

### Cosa preservare e cosa non inferire

- **OBSERVED:** il 3Q e compatibile con tutti i replay Top 3; peak 12 hands e comune; Q3/SE non e necessario nel corpus.
- **INFERRED:** una futura candidata Copilot indipendente dovrebbe rendere reattivi i soli punti in cui il contratto C2.1 espone informazione online, senza usare esiti futuri come feature.
- **UNKNOWN:** azioni V2 realmente eseguite, fill, stock, invenduto, fughe, densita temporale e routing V2 nei nove replay; questi JSON non contengono V2.
- **NON AZIONE:** non adottare meccanicamente timing, mix, struttura o routine dei Top 3; non riusare la routine Codex come base di merito Copilot.

## Raccomandazione critica per il prossimo lavoro Copilot

Prima di una mutazione strategica, creare una baseline **nuova e indipendente** e uno strumento offline di telemetria requested/executed che non alteri le azioni. Il primo confronto causale deve isolare una sola guardia basata su osservazioni online (per esempio ordine di mercato condizionato a cassa/stato osservati), contro una baseline Copilot congelata e indipendente, con almeno sei seed preregistrati e seat bilanciati. Metriche: score, cassa, sblocco Q1/Q2, peak hands, fill executed, inventario terminale, fughe derivate auditabili e MOVE/produttive. Promozione: parita dell'instrumentation, 100% copertura del ledger, zero fughe e nessuna regressione del floor. Questo e un disegno sperimentale proposto, non un risultato misurato.

## Limiti

I nove replay sono un corpus osservazionale: non identificano causalita su timing Q2, mix, routing o liquidazione. Le metriche per azione nel replay sono richieste salvo una ricostruzione esplicitamente auditabile dell'esecuzione. Questo feedback ha consultato la riconciliazione cross-agent su richiesta dell'utente; non importa, copia o adatta routine di altri agenti.
