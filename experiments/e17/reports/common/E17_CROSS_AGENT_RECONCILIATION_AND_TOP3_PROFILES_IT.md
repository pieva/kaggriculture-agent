# E17 — Riconciliazione cross-agent, profili Top 3 e gap della Codex V9

- **Data:** 2026-09-02
- **Ambito:** 9 replay Kaggle E17, 18 player-seat, 720 step per episodio
- **Top player osservati:** `tetsuya`, `OceanMix`, `Crop Dusta`
- **Analisi confrontate:** Antigravity, Copilot, Codex
- **Baseline interna:** `CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY`
- **Stato:** review cross-agent completata — Copilot `ACCEPT_WITH_CHANGES`, Antigravity `ACCEPT`; nessuna modifica alla policy

## 1. Esito esecutivo

I tre top player non usano una singola routine dominante, ma tre archetipi 3Q distinti:

1. **`tetsuya`: 3Q distribuito, reinvestimento anticipato e chiusura pulita.** Apre Q1 relativamente tardi (D7), ma Q2 a D10; distribuisce il bestiame anche in Q2, usa quattro crop e tre specie animali, non perde animali e liquida completamente l'inventario nel campione.
2. **`OceanMix`: spina zootecnica compatta Q0/Q1 e satellite colturale Q2.** Apre Q1 a D6 e Q2 a D11, concentra tutto il bestiame nei primi due quadranti e usa Q2 come modulo esclusivamente colturale. È l'archetipo logisticamente più efficiente.
3. **`Crop Dusta`: espansione molto anticipata, massima diversificazione e massimo rischio.** Apre Q1 tra D5 e D6 e Q2 tra D8 e D9; mescola crop e bestiame nei tre quadranti, ma paga il layout disperso con il maggiore movimento, 31 eventi di fuga derivati e più inventario invenduto.

Il corpus supporta il mantenimento del 3Q della Codex V9 come baseline E17, ma non dimostra che 3Q o 12 hands siano ottimi universali. Il gap principale osservabile rispetto alla leaderboard **non sembra essere l'assenza di Q2** né una workforce massima inferiore, perché la V9 è già allineata alle configurazioni comuni del campione. Il divario più plausibile è nella capacità di adattare una routine densa a contesa di mercato, seed, avversario e stato effettivamente eseguito. La V9 produce molto nei test locali, ma resta open-loop: il suo replay specchio scende a 46.251 e il rating Kaggle osservato è 1.159,9 contro 2.869–2.947 dei Top 3.

La conseguenza operativa per E17 è netta: **preservare il nucleo produttivo V9, introdurre prima un ledger requested/executed completo e poi testare causalmente, una variabile alla volta, contesa di mercato, topologia zootecnica e anticipo Q2 a D10.** Copiare integralmente uno dei tre profili non è giustificato dai nove replay.

## 2. Riconciliazione delle tre analisi

| Campo | Antigravity | Copilot | Codex | Valore canonico adottato |
|---|---|---|---|---|
| Integrità corpus | 9/9 validi | 9/9 validi | 9/9 validi | Consenso: 9 episodi, modulo `1.32.7`, 720 step |
| Score e record | Concordanti sui valori medi | Concordanti | Ricalcolo diretto | Ricalcolo Codex dai reward terminali |
| Sblocco Q1/Q2 | Quasi concordante; alcune discrepanze nel testo narrativo | Concordante con il raw | Ricalcolo diretto per prima transizione locked→owned | Valori Codex/Copilot; per Crop Dusta Q1 medio s135,2 e Q2 medio s206,6 |
| MOVE | Concordante | Concordante | Concordante | Comandi MOVE emessi, non prova di esecuzione |
| Hands | Picco 12 | Picco 12; distingue anche terminali | Picco e snapshot giornalieri | **Picco 12 per tutti**; i valori terminali non descrivono la capacità massima |
| Topologia finale | Occupancy per specie, con alcune incoerenze nel testo manuale | Conta strutture PASTURE/COOP | Occupancy animale e crop per tile | CSV Codex e JSON Antigravity, verificati sul raw |
| Fughe animali | 31, tutte Crop Dusta | `UNKNOWN` | 31 transizioni EOD ricostruite | **DERIVED**, non campo nativo: 1 dopo D23, 5 dopo D27, 25 dopo D28; 0 eventi derivati per tetsuya/OceanMix |
| Mix crop/animali | Ricostruito dai comandi richiesti | Parziale | Occupancy e timeline | Mix Antigravity etichettato **requested**; occupancy Codex etichettata **observed** |
| Inferenza strategica | Priorità a Q2 D10 | Priorità a ledger/milestone telemetry | Priorità a floor, contesa e causalità | Telemetria come prerequisito; interventi separati e preregistrati |

Correzioni rilevanti:

- le mediane corrette sono 95.127 per `tetsuya`, 82.271 per `OceanMix` e 87.152 per `Crop Dusta`;
- per `Crop Dusta`, gli sblocchi Q2 osservati sono s218, s199, s201, s212 e s203: media s206,6, mediana s203;
- le fughe non sono un campo evento esplicito: i 31 eventi sono `DERIVED` dalle transizioni EOD. L'audit ora registra animale presente a H23, `consecutive_unfed=1`, `fed_today=false`, assenza di FEED/PICKUP eseguiti prima dello snapshot, zero richieste FEED/PICKUP all'EOD e stessa struttura vuota nel primo stato del giorno successivo;
- i numeri di `PLANT`, `BUY_ANIMAL`, `SELL` e simili descrivono richieste della policy finché non esiste un ledger di esecuzione completo.

## 3. Quadro quantitativo comparabile

| Metrica | `tetsuya` | `OceanMix` | `Crop Dusta` | Codex V9 |
|---|---:|---:|---:|---:|
| Rating Kaggle nello snapshot di raccolta 2026-09-01 | **2.947,0** | 2.875,8 | 2.869,0 | **1.159,9** |
| Episodi nel corpus | 4 | 4 | 5 | 12 holdout locali |
| Record nel corpus | **3–1** | 2–2 | 2–3 | n/a |
| Denaro finale medio | **96.568** | 82.535,25 | 91.361,20 | 137.954,33 passivo; 106.836,43 vecchio torneo |
| Denaro finale min–max | 76.264–119.754 | 51.238–114.361 | 64.811–114.881 | 77.542–181.339 holdout |
| Sblocco Q1 | D7:H01, s169 | D6:H07, s151 | media D5,4, s135,2 | D6 |
| Sblocco Q2 | D10:H01, s241 | D11:H02, s266 | media D8,2, s206,6 | D11 |
| Q3 | mai | mai | mai | mai |
| Peak hands | 12 | 12 | 12 | 12 |
| Peak crop medio | 58,0 | **61,0** | 60,6 | 55 |
| Peak animali medio | 15,0 | 14,25 | 16,8 | **19** |
| Azioni produttive medie | 2.690,5 | **2.938,0** | 2.857,2 | 2.842 |
| MOVE medi | 3.377,25 | **3.075,75** | 4.070,0 | 3.546 |
| MOVE / produttive | 1,2553 | **1,0468** | 1,4267 | 1,2477 |
| PASS medi | 1.317,5 | 831,25 | **287,2** | 676 |
| Eventi fuga derivati (criterio EOD) | **0** | **0** | **31** | **0** |
| Specie crop richieste | 4 | 4 | **5** | 3 |
| Specie animali richieste | **3** | 2 | **3** | 2 |
| Inventario finale invenduto medio | **0** | 35,5 | 373 | non misurato executed |

I valori monetari non sono direttamente confrontabili tra corpus Kaggle, runner passivo e torneo locale. Il rating Kaggle resta il segnale competitivo sintetico: la V9 vale circa il 39–40% del rating dei tre top nello snapshot. Anche il precedente sweep locale 28–0 non colma questa evidenza, perché misurava versioni più deboli e in seguito strategicamente non indipendenti.

## 4. Evoluzione temporale delle topologie

Legenda: `C` = crop attive, `A` = animali presenti, `I` = tile inattive. I valori sono medie per agente; ogni quadrante contiene 25 tile. D29 rappresenta la fase di liquidazione e non la densità stagionale.

| Agente | D10 | D15 | D29 |
|---|---|---|---|
| `tetsuya` | Q0 C18/A7/I0; Q1 C22,75/A2,25/I0; Q2 C15/A1,75/I8,25 | Q0 C18/A7/I0; Q1 C22,75/A2,25/I0; Q2 C17,25/A5,75/I2 | Q0 C1/A7/I17; Q1 C3,5/A2,25/I19,25; Q2 C0,25/A5,75/I19 |
| `OceanMix` | Q0 C14,75/A6,75/I3,5; Q1 C18/A7/I0; Q2 locked | Q0 C17,75/A7,25/I0; Q1 C17,75/A7/I0,25; Q2 C25/A0/I0 | Q0 C0/A7,25/I17,75; Q1 C0/A7/I18; Q2 C0/A0/I25 |
| `Crop Dusta` | Q0 C17,4/A6,4/I1,2; Q1 C20,4/A4/I0,6; Q2 C20,4/A1,4/I3,2 | Q0 C17,8/A7,2/I0; Q1 C18,8/A5,6/I0,6; Q2 C20,8/A2,8/I1,4 | Q0 C1,4/A3,6/I20; Q1 C1,2/A4/I19,8; Q2 C1,4/A3/I20,6 |

Lettura temporale:

- `tetsuya` completa la propria architettura tra D10 e D15: Q1 resta principalmente colturale, Q2 cresce da modulo colturale incompleto a modulo misto con circa sei animali;
- `OceanMix` non “lascia inutilizzato” Q2: a D15 lo occupa con 25 crop e lo mantiene quasi pienamente colturale fino alla liquidazione; semplicemente non vi costruisce il nucleo zootecnico;
- `Crop Dusta` ha già tre quadranti produttivi a D10 e li mantiene tutti misti; il vantaggio di anticipo viene accompagnato dal più alto costo di movimento e da una fragilità terminale evidente.

## 5. Profilo 1 — `tetsuya`

### Tempistiche e capitale

- Q1 invariabilmente a s169 (D7:H01), Q2 a s241 (D10:H01).
- Cassa media a D10: 871,75, intervallo 452–1.174. È un profilo di reinvestimento precoce, non di riserva liquida.
- La cassa sale rapidamente dopo la costruzione: media 13.898 a D15, 52.483 a D20 e 96.568 a D29.

### Diversificazione

- `PLANT` richiesti per episodio: WHEAT 166,25; STRAWBERRY 37,5; MELON 13,75; CARROT 2.
- Acquisti animali richiesti: COW 5; SHEEP 8; GOOSE 2.
- Quattro crop e tre specie animali; la diversificazione animale serve anche a distribuire flussi di MILK, WOOL ed EGG.

### Topologia

- Q0: nucleo bilanciato, circa 18 crop + 7 animali nella fase matura.
- Q1: modulo ad alta densità colturale, con solo 2–3 animali.
- Q2: modulo misto, con circa 17 crop + 6 animali da D15.
- Finale: circa 7 animali in Q0, 2,25 in Q1 e 5,75 in Q2; il bestiame rimane distribuito fino alla chiusura.

### Strategia generale

`tetsuya` scambia liquidità iniziale per un giorno di produzione Q2 in più rispetto a V9/OceanMix. Non massimizza né la precocità assoluta né l'efficienza di routing; combina invece densità, diversificazione, servicing senza fughe e liquidazione completa. Nel campione è l'unico profilo con 3–1, miglior denaro medio e inventario terminale nullo.

### Confronto con Codex V9

La V9 è già vicina a questo archetipo per distribuzione zootecnica su Q2 e rapporto MOVE/produttive (1,2477 contro 1,2553), ma è più animal-dense (19 contro 15 di picco), apre Q2 un giorno dopo e non usa CARROT o GOOSE. Il gap più credibile non è “più densità”: è verificare se **D10 + minore carico animale + liquidazione/fill reattivi** aumentino il floor competitivo.

## 6. Profilo 2 — `OceanMix`

### Tempistiche e capitale

- Q1 invariabilmente a s151 (D6:H07), Q2 a s266 (D11:H02): stesso calendario macro della V9.
- Cassa media a D10: 15.820,75, intervallo 15.400–16.170, molto superiore a `tetsuya` e `Crop Dusta`.
- Il profilo conserva una riserva prima di Q2 e cresce più gradualmente: 26.126 a D15, 49.138 a D20, 82.535 a D29.

### Diversificazione

- `PLANT` richiesti per episodio: WHEAT 182,5; STRAWBERRY 36,75; CARROT 19,25; MELON 12.
- Acquisti animali richiesti: COW 8,25; SHEEP 6,25; nessuna GOOSE.
- Quattro crop, due specie animali; è il profilo più cow-heavy dei tre.

### Topologia

- Q0 e Q1 contengono tutto il bestiame: circa 7 animali per quadrante.
- Q2 è un satellite colturale: 25 crop a D15–D20 e nessun animale.
- La liquidazione finale svuota completamente le crop di tutti i quadranti; restano circa 14,25 animali nei soli Q0/Q1.

### Strategia generale

`OceanMix` separa produzione animale e coltivazione su scala di quadrante. Questo riduce i percorsi di feed/care/collect e consente il miglior rapporto MOVE/produttive del campione (1,0468), il maggior numero di azioni produttive (2.938) e zero fughe. Il costo è un'apertura Q2 più tarda e una maggiore esposizione alle prestazioni economiche del grande satellite colturale.

### Confronto con Codex V9

Calendario e workforce coincidono, ma la topologia è opposta: V9 colloca cinque SHEEP in Q2 e arriva a 19 animali. `OceanMix` dimostra che Q2 può produrre intensamente senza bestiame e con travel molto inferiore. Il principale contrasto topologico E17 deve quindi essere **V9 distribuita contro una variante compact-spine Q0/Q1 + crop-only Q2**, mantenendo invariati timing, workforce e budget iniziale.

## 7. Profilo 3 — `Crop Dusta`

### Tempistiche e capitale

- Q1: s122 o s155; media s135,2 (D5,4), mediana s122.
- Q2: s199–s218; media s206,6 (D8,2), mediana s203.
- Cassa media: 131 a D5, 7.073 a D10, 19.369 a D15 e 91.361 a D29.
- L'espansione è più precoce ma non identica tra episodi, indice di una cadenza o condizione diversa dagli altri due profili invarianti.

### Diversificazione

- `PLANT` richiesti per episodio: WHEAT 121,6; STRAWBERRY 31; CARROT 28,2; MELON 12,4; TOMATO 5,2.
- Acquisti animali richiesti: COW 7,4; SHEEP 6,2; GOOSE 3,4.
- È l'unico Top 3 a usare tutte le cinque crop, incluso TOMATO, e usa tutte le tre specie animali.

### Topologia

- Già a D10 i tre quadranti sono misti e quasi saturi.
- A D15 mantiene 17,8–20,8 crop e 2,8–7,2 animali in ogni quadrante.
- Le perdite terminali riducono gli animali vivi medi a 3,6/4/3 per Q0/Q1/Q2, lasciando numerose strutture vuote.

### Strategia generale

`Crop Dusta` massimizza il tempo utile di Q1/Q2, la varietà di ricavi e l'uso degli slot: solo 287 PASS medi. Il prezzo è 4.070 MOVE, rapporto 1,4267, inventario invenduto medio 373 e 31 fughe, concentrate soprattutto dopo D28. Il campione non permette di stabilire se una parte delle fughe terminali sia un abbandono economicamente deliberato; permette però di dire che la strategia è meno serviceable e più variabile.

### Confronto con Codex V9

La V9 risolve già il rischio più evidente di questo archetipo: zero fughe. `Crop Dusta` dimostra che D8 è tecnicamente raggiungibile, ma non che sia causalmente migliore. L'anticipo estremo non deve essere la prima mutazione della V9: andrà testato solo dopo aver misurato fill, stock, servizio per quadrante e costo marginale del travel.

## 8. Profilo della nostra Codex V9

### Architettura attuale

- Routine open-loop di 719 step con correzione causale del feed D8.
- Q1 a D6, Q2 a D11, Q3 mai.
- 12 hands, picco 55 crop e 19 animali.
- Mix target: MELON 17, STRAWBERRY 27, WHEAT 12; COW 6, SHEEP 11.
- Distribuzione animale registrata: Q0 8, Q1 6, Q2 5; Q2 produce il primo output a D15.
- 2.842 azioni produttive, 3.546 MOVE, 676 PASS, MOVE/produttive 1,2477, zero fughe.

### Punti di forza supportati dal campione e dai test locali

- Il 3Q NW→NE→SW è compatibile con tutti i top osservati e nessuno apre Q3; questo supporta la baseline, senza dimostrarne l'ottimalità universale.
- La workforce massima è allineata al picco comune di 12 hands; aumentarla non è una priorità motivata da questo corpus, ma 12 non è un optimum dimostrato.
- Densità produttiva e servicing animale sono forti; il rapporto di routing è vicino a `tetsuya` e molto migliore di `Crop Dusta`.
- La correzione D8 elimina le fughe senza rinunciare alla zootecnia distribuita.

### Fragilità che il benchmark rende più importanti

- La routine temporale non verifica l'esito reale degli ordini; richieste elevate possono fallire o spostare i prezzi in mirror/contesa.
- La topologia V9 è più animal-dense di tutti i tre profili osservati e non è stata confrontata causalmente con una spina compatta.
- Il mix è meno diversificato: tre crop e due specie animali contro 4/3 di `tetsuya`, 4/2 di `OceanMix`, 5/3 di `Crop Dusta`.
- Non esiste un ledger executed completo per inventario, fill, sell e fertilizer; non sappiamo distinguere saturazione produttiva da saturazione nominale.
- La chiusura è statica: il benchmark dei top mostra che liquidazione e rischio terminale separano nettamente `tetsuya` da `Crop Dusta`.
- La distanza tra denaro locale elevato e rating Kaggle basso suggerisce un problema di robustezza competitiva, non una carenza di produzione nominale.

## 9. Gap E17, priorità e test causali

| Priorità | Gap Codex | Evidenza | Esperimento isolato | Promozione minima |
|---:|---|---|---|---|
| P0 | Ledger requested/executed assente | Tutte le analisi devono distinguere comandi ed esiti; V9 mirror 46.251 | Aggiungere sola telemetria di fill, stock, inventory value, servizio e milestone, con parità azione-per-azione | 100% copertura; hash delle azioni invariato; nessun delta di score |
| P1 | Bassa adattività alla contesa | Rating 1.159,9; mirror molto sotto holdout; routine open-loop | Una sola guardia fill-aware sui flussi WHEAT, senza cambiare layout o calendario | Mirror ≥90K; holdout min ≥100K; zero fughe |
| P2 | Topologia zootecnica non ottimizzata | OceanMix 1,0468 MOVE/produttive con animali solo Q0/Q1; V9 1,2477 con 5 SHEEP Q2 | A/B: V9 distribuita contro compact-spine Q0/Q1 + crop-only Q2, stessi asset/budget/timing | MOVE/produttive ≤1,10 e denaro non inferiore oltre il 2% |
| P3 | Timing Q2 forse tardivo | tetsuya D10, zero fughe e miglior media; V9/Ocean D11; Crop D8 fragile | Spostare solo BUY_LAND/attivazione Q2 da D11 a D10, mantenendo il modulo invariato | Δ media ≥+3K, floor non peggiore, zero fughe |
| P4 | Chiusura non reattiva | Inventario finale: 0 tetsuya, 35,5 Ocean, 373 Crop; V9 executed unknown | Guardia terminale di liquidazione basata su inventory e fill, senza cambiare produzione D0–D25 | Inventario invenduto = 0; nessuna regressione media |
| P5 | Mix meno diversificato | Tutti i Top 3 usano CARROT; due usano GOOSE; Crop usa TOMATO ma è fragile | Sostituzione limitata di una sola famiglia crop con CARROT; GOOSE in test separato | Miglioramento su prezzi/seed preregistrati senza peggiorare routing |
| P6 | Weed e recovery poco reattivi | V9 dichiara bassa reattività; top efficienti mantengono pochi weed | Una sola guardia condizionale DIG/recovery | Miglioramento floor; nessun cambio di macro-cadenza |
| Non prioritario | Numero quadranti e peak hands | Tutti i target osservati usano 3Q e raggiungono 12 hands | Non aprire Q3 e non aumentare workforce nella prima sequenza E17 | Mantenere come controllo, non dichiarare optimum |

### Sequenza raccomandata

1. **E17.0 — Measurement freeze.** Integrare il ledger senza modificare una sola azione; rieseguire canonical, holdout, mirror e seed/seat bilanciati.
2. **E17.1 — Market robustness.** Inserire una guardia fill-aware circoscritta a WHEAT. È il test più direttamente collegato al divario tra score locale e rating Kaggle.
3. **E17.2 — Topology contrast.** Confrontare la V9 distribuita con il profilo compact-spine di `OceanMix`, senza anticipare Q2 e senza cambiare il numero totale di asset.
4. **E17.3 — Q2 D10.** Testare l'unica differenza temporale piccola e interpretabile suggerita da `tetsuya`.
5. **E17.4 — Endgame closed loop.** Liquidazione condizionata all'inventario eseguito.
6. **E17.5 — Diversificazione.** Solo se il ledger mostra un collo di bottiglia economico, introdurre CARROT; testare GOOSE e TOMATO separatamente.
7. **E17.6 — Frontier aggressiva.** Valutare D8 soltanto con un vincolo esplicito di serviceability per quadrante e rollback alla prima fuga.

Ogni esperimento deve usare seed preregistrati, entrambi i seat, controllo invariato, una sola mutazione strategica e gli stessi gate V9.1:

```text
HOLDOUT_MEAN >= 145000
HOLDOUT_MIN >= 100000
COMPETITIVE_MIRROR >= 90000
ANIMAL_ESCAPES == 0
MOVE_PER_PRODUCTIVE <= 1.20
EXECUTED_MARKET_LEDGER_COVERAGE == 100%
```

Per il contrasto topologico si aggiunge un target informativo, non ancora un gate globale: `MOVE_PER_PRODUCTIVE <= 1.10`.

## 10. Cosa non concludere dai nove replay

- Non esiste uno scontro `tetsuya`–`OceanMix`: il loro ordinamento causale non è identificato.
- Rating Kaggle, denaro finale e win rate del piccolo corpus misurano fenomeni diversi.
- I replay sono osservazionali e soggetti a opponent/market interference; non provano che D10, CARROT o GOOSE causino da soli un miglioramento.
- La composizione D29 è successiva alla liquidazione e non descrive l'uso stagionale di Q2.
- I 31 eventi di fuga di `Crop Dusta` sono derivati con criterio EOD auditabile, non osservati come campo nativo; il loro costo-opportunità netto non è identificato senza un controfattuale.
- Le stime puntuali di miglioramento proposte nelle analisi indipendenti sono ipotesi da preregistrare, non risultati già dimostrati.

## 11. Tracciabilità

- `docs/model_specs/antigravity/e17/reports/E17_TOP3_REPLAY_ANALYSIS.md`
- `docs/model_specs/antigravity/e17/artifacts/discovery/E17_TOP3_REPLAY_METRICS.json`
- `docs/model_specs/copilot/e17/reports/E17_TOP3_REPLAY_ANALYSIS.md`
- `docs/model_specs/copilot/e17/artifacts/discovery/E17_TOP3_REPLAY_METRICS.json`
- `docs/model_specs/codex/e17/reports/E17_TOP3_REPLAY_ANALYSIS.md`
- `docs/model_specs/codex/e17/artifacts/discovery/E17_TOP3_REPLAY_METRICS.json`
- `docs/model_specs/codex/e17/artifacts/discovery/E17_QUADRANT_DAILY_TIMELINE.csv`
- `docs/model_specs/codex/e17/artifacts/discovery/E17_ANIMAL_ESCAPE_EVENTS.csv`
- `docs/model_specs/copilot/e17/reviews/E17_CROSS_AGENT_FEEDBACK_AND_COPILOT_CRITICAL_ANALYSIS_IT.md`
- `docs/model_specs/antigravity/e17/reviews/E17_CROSS_AGENT_FEEDBACK_AND_ANTIGRAVITY_CRITICAL_ANALYSIS_IT.md`
- `docs/model_specs/codex/MODEL_SPEC_CODEX_C2_3Q_POST_FOUNDATION_REVIEW.md`
- `docs/governance/history/model_spec_c2/codex/CODEX_V9_0_FINAL_REPORT_IT.md`
- `docs/governance/history/model_spec_c2/codex/CODEX_V9_0_HOLDOUT_RESULTS.json`

## 12. Riconciliazione dei feedback disponibili

### Copilot — `ACCEPT_WITH_CHANGES`

Il feedback è accolto integralmente nei punti metodologici:

- 3Q e picco 12 sono ora descritti come configurazioni comuni osservate, non come ottimi dimostrati;
- la colonna fughe è esplicitamente `DERIVED`;
- `E17_ANIMAL_ESCAPE_EVENTS.csv` è stato esteso con EpisodeId, player, step pre/post-EOD, coordinata, struttura, `consecutive_unfed`, `fed_today`, evidenza di FEED/PICKUP non eseguiti prima dello snapshot e conteggio delle richieste FEED/PICKUP all'EOD;
- resta il divieto di confrontare direttamente rating Kaggle, cassa del corpus e score dei runner locali;
- la roadmap Codex non viene trasferita a Copilot: una futura policy Copilot deve partire da una baseline indipendente.

### Antigravity — `ACCEPT`

Il feedback formale post-riconciliazione (`docs/model_specs/antigravity/e17/reviews/E17_CROSS_AGENT_FEEDBACK_AND_ANTIGRAVITY_CRITICAL_ANALYSIS_IT.md`) accoglie integralmente l'impianto metodologico e la roadmap unificata:

- **Separazione epistemologica:** pieno accordo su distinzione `OBSERVED`, `DERIVED`, `INFERRED` e separazione fra comandi *requested* ed esiti *executed*;
- **Audit fughe e composizioni D29:** recepiti l'audit 31/31 su EOD e la natura post-liquidazione di D29;
- **Q2 D10 e contrasto topologico:** accettati come ipotesi da sottoporre a test causale isolato (`E17.2` topologico e `E17.3` anticipo temporale) con soglie preregistrate e vincolo assoluto di zero fughe;
- **Indipendenza strategica (GAP-05):** riconosciuta la necessità primaria di una baseline nativa indipendente senza dipendenze dalla routine Codex prima di procedere con i test C2.1;
- **Convergenza sulla roadmap:** piena sottoscrizione della sequenza E17.0 -> E17.6.

L'`ACCEPT` non modifica le cautele già adottate: 3Q/12 hands restano standard osservati, non ottimi dimostrati; l'associazione fra precocità, travel e fughe non è causale; il rating 1.159,9 è riferito alla submission Codex, non alla V4 Antigravity derivativa.

La riconciliazione esterna è pertanto **completata e chiusa in via definitiva** sia per Copilot sia per Antigravity.

## 13. Decisione finale per E17

La baseline da preservare è Codex V9, non una replica dei top. E17 non
preseleziona un archetipo vincente: i nove replay mostrano combinazioni
differenti e competitive di timing, topologia, densità, diversificazione,
capitale e chiusura. Queste dimensioni devono essere separate prima di
costruire una candidata composita. I replay indicano tre direzioni iniziali da
sottoporre a causalità:

1. **reattività alla contesa e agli esiti reali**;
2. **compattazione zootecnica e riduzione del travel**;
3. **anticipo controllato di Q2 da D11 a D10**.

Il primo sviluppo deve essere il ledger executed con parità comportamentale; la prima mutazione di policy deve poi attaccare la contesa di mercato. Solo dopo sarà possibile attribuire correttamente l'eventuale miglioramento a timing, topologia o diversificazione.

## 14. Addendum leaderboard — 2026-09-02

Lo snapshot successivo fornito dall'utente mostra:

```text
1. Crop Dusta  2917.8
2. tetsuya     2890.3
3. 3정훈       2878.5
```

`OceanMix` non compare nei primi sette visibili. Questo aggiornamento non
modifica le metriche dei nove replay, ma cambia la loro etichetta: sono un
benchmark di tre archetipi selezionati da un precedente Top 3, non la
fotografia del Top 3 corrente.

La leadership di Crop Dusta impedisce di trattare il suo approccio soltanto
come variante marginale o fallimentare. RQ6 — frontiera Q2 D8 — diventa un
checkpoint obbligatorio prima della chiusura di E17. Non viene però anticipato
prima di ledger, contesa e serviceability: il nuovo rating non identifica
causalmente D8, diversificazione o fughe terminali come fonti del vantaggio.
