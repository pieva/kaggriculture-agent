# POST-E15 — MODEL CAPABILITY CHECK (Copilot / Model Analyst)

**Ruolo assunto:** MODEL ANALYST. Nessun file è stato modificato durante l'analisi. Nessun codice o submission è stato generato. Nessuna policy è stata corretta o ottimizzata. Non ho avuto accesso a risposte di altri modeler su questo stesso task al momento dell'analisi.

---

## 0. Legenda di provenienza

| Tag | Significato | Fonti usate |
|---|---|---|
| **[FRAME]** | METHODOLOGICAL FRAME — definizioni e metodo | [README.md](../../../README.md), [ONTOLOGY_E15_FROZEN.md](../../e15/freeze/ONTOLOGY_E15_FROZEN.md) |
| **[E15-PRIMARY]** | PRIMARY E15 EVIDENCE — osservazioni/misure frozen | `summary.json` ×3, `telemetry.json` ×3, `E15_M*_NEUTRAL_FORENSIC_ANALYSIS.md` ×3 (redatte pre-challenge), MODEL_SPEC frozen ×3 (per le hypotheses *ex ante*) |
| **[POST-E15-INTERPRETATION]** | Interpretazioni/sintesi già formulate nel repo | `E15_M*_CONSENSUS.md` ×3, `E15_FINAL_TOURNAMENT_SYNTHESIS.md`, `PROJECT_STATE.md`, `M2_COPILOT_INDEPENDENT_AUDIT.md`, `P0_P1_ENVIRONMENT_AUDIT.md` |
| **[MY-INFERENCE]** | Inferenza prodotta autonomamente in questo capability check | Ragionamento originale in questo documento |

Non ho trattato alcuna proposizione come dimostrata solo perché presente nel README o in un documento di sintesi: dove la sintesi interpreta, l'ho segnalato come **[POST-E15-INTERPRETATION]** e ho verificato, quando possibile, il dato sottostante nei documenti **[E15-PRIMARY]**.

**Risultato competitivo (fatto verificato, [E15-PRIMARY]):**

| Match | P0 | P1 | Seed | Score | Winner |
|---|---|---|---:|---|---|
| M1 | Antigravity | Codex | 1113294977 | $8,672 vs $20,461 | Codex |
| M2 | Codex | Copilot | 3033283457 | $27,510 vs $37,752 | Copilot |
| M3 | Copilot | Antigravity | 3122977751 | $26,629 vs $9,371 | Copilot |

Standing: Copilot 2–0, Codex 1–1, Antigravity 0–2. `total_steps = 720` in tutti e tre i match.

---

## A. Evidence reconstruction

### A.1 Struttura dell'esperimento **[FRAME]**
E15 è un torneo pairwise a tre agenti indipendenti (Antigravity, Codex, Copilot), ciascuno con: ontologia comune frozen (64 `concept_id`), `MODEL_SPEC` frozen separato, submission frozen separata (SHA256 verificati in `FREEZE_MANIFEST.md`). Ogni agente gioca esattamente una volta come P0 e una volta come P1 (bilanciamento posizionale strutturale). Per ciascun match: neutral forensic analysis → challenge indipendenti dei due model owner → consensus synthesis → doppio ACK, prima di autorizzare il match successivo.

### A.2 Risultati osservati **[E15-PRIMARY]**
- **M1** — capacità nominale alta (Antigravity: 3Q, 12 hands, 18 pasture, 18 animali) perde contro capacità nominale più bassa ma molto più attivata (Codex: 2Q, max 28 crop attive, 439 WATER vs 34).
- **M2** — le due policy condividono quasi tutto (stesso Q1 al Day 11 Hour 1, max 10 hands, WATER 475 vs 446, azioni totali quasi identiche 5.320 vs 5.297); vince il working set **più piccolo** (Copilot: 28 crop/5 pasture/4 animali) su quello più grande (Codex: 37 crop/9 pasture/7 animali).
- **M3** — replica quasi esatta della firma Antigravity di M1 (WATER 30 vs 34, HARVEST 374 vs 414, MOVE 5.047 vs 5.019, 18 pasture/18 animali/3Q in entrambi) contro un Copilot strutturalmente simile a M2 (WATER 439, 5 pasture, 4 animali, 25 crop, 302 SELL).

### A.3 Evidenze strategiche rilevanti **[E15-PRIMARY]**
Due "policy fingerprint" altamente riproducibili:
- **Antigravity (M1≈M3):** WATER 34/30, HARVEST 414/374, MOVE 5.019/5.047, 18 pasture/18 animali/3Q/12 hands, herd finale 17 (13 Cow + 4 Sheep) in entrambe.
- **Copilot (M2≈M3):** WATER 446/439, 5 pasture/4 animali/9 hands, SELL orders 298/302.

Il rapporto HARVEST/PLANT (una proxy di dispatch inefficiente, non una misura diretta di fallimento) è ~4.45 (M1) e ~3.74 (M3) per Antigravity contro ~0.95–0.98 per Codex/Copilot.

### A.4 Requested orders vs executed transactions — esplicitato **[E15-PRIMARY]**
Ho verificato direttamente `telemetry.json` (M2): il blocco `market_orders` riporta **conteggi di ordini per tipo** (`HIRE`, `BUY_LAND`, `BUY_SEED`, `BUY_ANIMAL`, `BUY_PRODUCT`, `SELL`), non quantità eseguite né valore monetario realizzato. Tutti e tre i `NEUTRAL_FORENSIC_ANALYSIS` e il `M2_COPILOT_INDEPENDENT_AUDIT.md` lo dichiarano esplicitamente ("le quantità sono richieste di market order; non vanno automaticamente trattate come quantità tutte eseguite"). Non esiste, in nessuno dei tre match, un ledger di transazioni eseguite con prezzo realizzato. Questo è un **limite strutturale dell'osservabilità**, non un'omissione di analisi: l'ontologia stessa (§8) richiede `INCONCLUSIVE` quando questa telemetria manca, ed è quanto i verdetti fanno sistematicamente per `market_transaction_value`, `feed_market_expenditure`, `market_churn_cost`.

### A.5 Limiti dell'evidenza disponibile **[MY-INFERENCE]**
1. **N=3 match, ciascuno single-seed, single-opponent-pairing.** Ogni confronto è un singolo campionamento congiunto di seed × avversario; non esiste ripetizione dello stesso match con seed diverso.
2. **Nessun ledger di esecuzione** (§A.4): impossibile calcolare margini netti, costo del churn, prezzo realizzato.
3. **Nessun action-effectiveness audit**: HARVEST/PLANT alto è una firma, non una prova diretta di quante HARVEST siano fallite.
4. **Variazione simultanea di più fattori** nella policy Antigravity (land + workforce + livestock scalano insieme): impossibile isolare l'effetto marginale di una singola variabile.
5. **Nessun confronto locale↔Kaggle** in E15 (`local_kaggle_fidelity_gap` = `NOT_DISCRIMINATED` in tutti e tre i match).
6. **Sequenza documentale**: `E15_M3_NEUTRAL_FORENSIC_ANALYSIS.md` si chiude dichiarando "E15 non è ancora epistemicamente CLOSED" — è un artefatto pre-consensus. La chiusura epistemica risulta solo nei documenti successivi (consensus M3, synthesis, `PROJECT_STATE.md`), tutti datati 2026-08-29. Non è una contraddizione, ma va tenuto distinto: la dichiarazione di chiusura è **[POST-E15-INTERPRETATION]**, successiva all'evidenza grezza.

---

## B. Layer diagnosis

Le tre dimensioni sono valutate separatamente per costruzione; non ho inferito un livello dall'altro.

### Antigravity

- **MODEL_VALIDITY:** `PARTIALLY_SUPPORTED` **[MY-INFERENCE, convergente con POST-E15-INTERPRETATION]**. Diversi principi dichiarati nel MODEL_SPEC frozen restano coerenti con l'evidenza: `irrigation_dispatch_priority` era già Rank 1/Critical/High *ex ante* (`MODEL_SPEC_ANTIGRAVITY_E15_FROZEN.md`) e M1/M3 non lo falsificano — anzi, il vincitore in entrambi i casi è chi irriga di più. Anche il falsification log *pre-registrato* (prima di E15) già rifiutava "più Q2/Hands/livestock vince da solo": E15 non fa che replicare quella stessa diagnosi su un torneo indipendente.
- **POLICY_REALIZATION:** `STRONGLY_WEAKENED` **[POST-E15-INTERPRETATION, verificato]**. Il MODEL_SPEC dichiara watering Rank 1 Critical; la submission realizza 34/30 WATER su 720 step. Dichiara `feed_autarky_pipeline` Rank 2 Critical; la submission richiede comunque ampi BUY_PRODUCT Wheat (904–1.007 richieste). Il MODEL_SPEC non è tradotto fedelmente in comportamento osservato.
- **IMPLEMENTATION_FIDELITY:** `STRONGLY_WEAKENED`, ma **UNRESOLVED nella causa precisa** **[MY-INFERENCE]**. La firma HARVEST≫PLANT e il MOVE elevato sono coerenti con un problema di dispatch/routing nel codice, ma nessun artefatto E15 include un'ispezione del codice o un action-effectiveness audit: l'attribuzione a un bug specifico resta un'inferenza, non un'osservazione diretta.

### Codex

- **MODEL_VALIDITY:** `PARTIALLY_TO_SUBSTANTIALLY_SUPPORTED` **[POST-E15-INTERPRETATION, verificato]**. Il Rank 1 *ex ante* Codex (`monetized_throughput_per_worker_action`, Very High/High) è supportato in M1 (vince nettamente) ma indebolito in M2, dove Codex ha più WATER, più crop, più productive-action-share e **perde comunque**. Questo non falsifica il concetto, ma **falsifica la sua lettura come driver monotono aggregato**, esattamente come registrato nel M2 consensus.
- **POLICY_REALIZATION:** `PARTIALLY_SUPPORTED` **[MY-INFERENCE]**. A differenza di Antigravity, non emerge un gap grossolano modello↔comportamento; il gap è più sottile: Codex realizza una capacità fisica maggiore di quanto il proprio stesso principio (Rank 1: monetizzazione, non volume) prescriverebbe come ottimale, il che è un segnale di **coerenza parziale interna** più che di un fallimento di traduzione.
- **IMPLEMENTATION_FIDELITY:** `UNRESOLVED` **[MY-INFERENCE]**. Nessuna firma di malfunzionamento comparabile ad Antigravity è stata osservata (HARVEST/PLANT ≈ 0.95–0.98, in linea con Copilot); non ci sono elementi per dubitare che il codice realizzi la policy dichiarata.

### Copilot

- **MODEL_VALIDITY:** `SUBSTANTIALLY_SUPPORTED` **[POST-E15-INTERPRETATION, verificato]**. I tre principi Rank 1–3 *ex ante* (`throughput_to_cash_conversion`, `working_set_capacity_gate`, `crop_activation_and_monetization`) sono coerenti con M2 e M3. Nota critica indipendente **[MY-INFERENCE]**: il proprio `M2_COPILOT_INDEPENDENT_AUDIT.md` classifica il Rank 1 stesso come `NOT_DISCRIMINATED` ("entrambi convergono; Copilot 37% più efficiente ma il meccanismo non è chiaro") — quindi il supporto a MODEL_VALIDITY è più debole di quanto il record 2–0 suggerisca superficialmente, e questa è una distinzione che l'agente vincitore ha correttamente segnalato su di sé.
- **POLICY_REALIZATION:** `SUPPORTED` **[POST-E15-INTERPRETATION, verificato]**. Il footprint M2→M3 è quasi identico (WATER 446/439, 5 pasture, 4 animali, 9 hands, SELL 298/302): la submission realizza una policy stabile e riproducibile.
- **IMPLEMENTATION_FIDELITY:** `UNRESOLVED` (non `SUPPORTED`, per costruzione: stabilità comportamentale ≠ prova che il codice esegua correttamente ogni istruzione della policy) **[MY-INFERENCE]**. Nessun audit del codice sorgente Copilot è stato effettuato in questo capability check.

**Osservazione trasversale [MY-INFERENCE]:** in nessuno dei tre casi la vittoria/sconfitta determina automaticamente MODEL_VALIDITY. Il caso più chiaro è Antigravity: perde 0–2 ma diversi suoi principi dichiarati non sono falsificati, solo non realizzati dalla propria submission.

---

## C. Feature analysis

Concetti selezionati tra i 64 canonici perché hanno prodotto evidenza materiale in ≥1 match. I concetti non elencati qui restano, per costruzione, `NOT_DISCRIMINATED`/`INCONCLUSIVE` in tutti i match consultati (es. `hire_order_scheduling`, `fertilizer_byproduct_flow`, `endgame_shutdown_timing`, `endgame_inventory_liquidation`, `local_kaggle_fidelity_gap`, `market_sellthrough_lag`, `unsold_inventory_value`) e li classifico globalmente `UNRESOLVED` senza schema dedicato, per proporzionalità.

### A — Terreno e superficie produttiva

```text
concept_id: land_surface_total
feature_status: NOT_FEATURE
relationship: non_monotonic
e15_evidence: M1: Antigravity 3Q perde vs Codex 2Q. M3: Antigravity 3Q perde vs Copilot 2Q. M2: entrambi 2Q, non discrimina.
failure_region: land_surface_total alto (3Q) senza attivazione proporzionale (Antigravity M1/M3)
success_region: land_surface_total basso/medio (2Q) con alta attivazione (Codex M1, Copilot M2/M3)
candidate_threshold_or_interval: nessuno — la superficie totale non è mai stata isolata come variabile indipendente; è sempre confusa con workforce/livestock scaling simultaneo
confidence: Medium (3/3 match coerenti nel rifiutare "più land=meglio", ma 0/3 isolano land come variabile singola)
confounders: Q2 Antigravity è acquistato insieme a ramp di hands/livestock; impossibile separare l'effetto del possesso di land da quello delle altre espansioni simultanee
next_test_values: usare le submission frozen esistenti (invariate) su nuovi seed per vedere se il pattern "3Q perde" si ripete anche quando gli altri fattori restano fissi per costruzione (sono già fissi nelle submission frozen)
falsification_condition: una submission con 3Q attivato (crop_surface_maintained comparabile a quella dei vincitori 2Q) che comunque perde contro un 2Q meglio attivato falsificherebbe l'idea che sia l'attivazione, e non la superficie, a discriminare
```

```text
concept_id: maintained_productive_surface
feature_status: FEATURE
relationship: positive, ma con evidenza di saturazione (M2)
e15_evidence: M1: 28 vs 8 crop attive (winner vs loser). M3: 25 vs 9 (winner vs loser). M2: 28 (winner) vs 37 (loser) — qui MENO superficie mantenuta vince.
failure_region: <10 crop attive massime su un episodio di 720 step (Antigravity, entrambe le occorrenze)
success_region: 25–28 crop attive massime nei due match vinti da Copilot; ma 37 (Codex, M2) non produce risultato migliore di 28
candidate_threshold_or_interval: la relazione è positiva solo fino a un certo punto tra ~9 e ~25; oltre ~28–37 l'evidenza (M2) indica rendimenti non crescenti o negativi. Nessun valore preciso di saturazione è osservato, solo il bracket 28<37 con esito invertito.
confidence: Medium-High per la parte "collasso sotto soglia" (2 repliche indipendenti); Low per la parte "saturazione oltre 28" (1 sola osservazione, confounded con altre differenze M2)
confounders: la superficie mantenuta è un aggregato derivato da watering+dispatch+crop mix; non scompone quale sotto-componente guida il risultato in M2
next_test_values: replicare M2-like matchup (working set comparabile in altri aspetti, superficie diversa) su seed multipli per vedere se 28<37 si conferma o è rumore di singolo seed
falsification_condition: una nuova osservazione dove 37 crop attive mantenute battono 28 a parità di WATER/SELL/monetizzazione qualitativa indebolirebbe l'ipotesi di saturazione
```

```text
concept_id: land_activation_payback
feature_status: FEATURE
relationship: conditional (payback dipende da timing e capacità di attivazione, non dal possesso)
e15_evidence: M1/M3: Q2 Antigravity acquisito ma non seguito da crescita proporzionale di crop/cash; il lead avversario diventa permanente prima (M3) o poco dopo (M1) l'acquisto di Q2.
failure_region: acquisto di nuova superficie mentre operating_cash_buffer è già sotto stress (Antigravity Day 18/19 in entrambi i match, cash residuo $73–$81)
success_region: nessuna espansione territoriale osservata nei match vinti da Copilot (resta a 2Q in entrambi); non testato positivamente, solo per assenza
candidate_threshold_or_interval: non determinabile — non esiste nel dataset un caso di espansione territoriale SEGUITA da payback positivo con cui confrontare i casi di fallimento
confidence: Medium (2 repliche del fallimento, 0 osservazioni dirette di successo)
confounders: il timing dell'acquisto coincide con ramp di workforce/livestock; il fallimento economico osservato dopo Q2 potrebbe essere causato da uno qualunque dei tre fattori simultanei
next_test_values: nessuna submission frozen testa oggi un'espansione territoriale con payback positivo; servirebbe una variante di policy (non autorizzata in questa fase) che espanda land SOLO quando maintained_productive_surface e cash superano soglie dichiarate
falsification_condition: osservare un'espansione territoriale seguita da crescita proporzionale di crop_surface_maintained e cash entro pochi giorni falsificherebbe la generalità del fallimento osservato
```

```text
concept_id: pasture_arable_surface_tradeoff
feature_status: FEATURE
relationship: negative (più pasture, a parità di altri fattori, coincide con meno crop e risultato peggiore)
e15_evidence: M1: 18 pasture/8 crop (loser) vs 9 pasture/28 crop (winner, ratio invertito). M2: 9 pasture/37 crop (loser) vs 5 pasture/28 crop (winner). M3: 18 pasture/9 crop (loser) vs 5 pasture/25 crop (winner).
failure_region: pasture ≥ 9 con crop attive proporzionalmente basse (Antigravity 18/8-9; Codex M2 9/37 — qui il rapporto è meno estremo e infatti Codex non collassa come Antigravity, perde solo relativamente)
success_region: pasture ≤ 5 con crop attive 25–28 (Copilot, tutte e 3 le occorrenze osservabili in M2/M3)
candidate_threshold_or_interval: failure osservato a 9 e 18 pasture; success osservato a 5. L'intervallo 6–8 non è mai stato testato.
confidence: High per la direzione (3/3 match coerenti); Low per un valore soglia preciso
confounders: pasture size è scelta insieme a livestock_headcount (sono quasi collineari nei dati: 18 pasture ↔ 18 animali, 9↔7, 5↔4) — impossibile separare l'effetto della superficie pasture da quello del numero di animali
next_test_values: 5 / 7 / 9 pasture a parità di crop-surface target, così da rompere la collinearità con livestock_headcount
falsification_condition: un working set con 9 pasture ma crop_surface_maintained comparabile a 25–28 (cioè pasture alte senza sacrificio di superficie arabile) che comunque perde, falsificherebbe il tradeoff come meccanismo causale
```

### B — Workforce, dispatch, logistica

```text
concept_id: workforce_headcount
feature_status: NOT_FEATURE
relationship: non_monotonic
e15_evidence: M1: 12 hands (loser) vs 10 (winner). M3: 12 (loser) vs 9 (winner). M2: 10 vs 10, non discrimina.
failure_region: 12 hands accompagnato da bassa crop_surface_maintained (Antigravity)
success_region: 9-10 hands con alta monetizzazione (Codex M1, Copilot M2/M3)
candidate_threshold_or_interval: nessuno stimabile — il conteggio hands da solo non separa mai i due esiti in modo pulito; conta come viene usato, non quanto è grande
confidence: Medium (rifiuto coerente di "più hands=meglio" in 2/3 match utili, ma mai isolato da dispatch quality)
confounders: più hands richiede più MOVE per coordinamento spaziale; il numero di hands è confuso con l'efficienza del routing dello stesso agente
next_test_values: nessun valore aggiuntivo prioritario — questo concetto è già ragionevolmente indebolito; risorse andrebbero investite altrove (vedi action_dispatch_failure)
falsification_condition: una policy con 12 hands e watering/dispatch comparabili ai vincitori attuali che comunque perde manterrebbe NOT_FEATURE; se invece vincesse, andrebbe riconsiderato come feature condizionata alla qualità del dispatch
```

```text
concept_id: productive_action_share
feature_status: NOT_FEATURE
relationship: unresolved / not_discriminating
e15_evidence: M1: quota quasi identica tra i due player. M2: Codex ha quota grezza SUPERIORE (18.35% vs 17.24%) e PERDE. M3: quota grezza non discrimina l'esito.
failure_region: n/d — non è mai stato il fattore che separa vincitore/perdente
success_region: n/d
candidate_threshold_or_interval: non applicabile — l'evidenza indica che questa metrica aggregata è insufficiente indipendentemente dal suo valore
confidence: High per la conclusione negativa ("share grezza non basta"), coerente in tutti i 3 consensus
confounders: la composizione delle azioni (quali azioni, non quante) è confusa con il denominatore aggregato; due policy con la stessa share possono avere composizioni radicalmente diverse (HARVEST/PLANT 4.45 vs 0.95)
next_test_values: sostituire la metrica con una scomposizione per tipo di azione (WATER share, HARVEST/PLANT ratio) già usata qualitativamente nei forensic report, resa quantitativa e comparabile
falsification_condition: se in un futuro match la share grezza correlasse sistematicamente con l'esito su più seed, andrebbe riconsiderata; al momento nessuna delle 3 osservazioni lo supporta
```

```text
concept_id: action_dispatch_failure
feature_status: FEATURE
relationship: negative (firma HARVEST≫PLANT associata a esito peggiore)
e15_evidence: M1: HARVEST/PLANT 4.45 (Antigravity, loser) vs 0.95 (Codex, winner). M3: 3.74 (Antigravity, loser) vs 0.98 (Copilot, winner). M2: nessuna firma estrema in nessuno dei due player.
failure_region: HARVEST/PLANT > 3.7 combinato con crop_surface_maintained bassa
success_region: HARVEST/PLANT ≈ 0.95–0.98
candidate_threshold_or_interval: failure osservato ≥3.74; success osservato ≤0.98. Intervallo 1.0–3.7 mai osservato.
confidence: Medium — la firma è replicata 2/2 volte in cui appare, ma resta una proxy: nessun action-effectiveness audit conferma che le HARVEST "in eccesso" siano effettivamente fallite piuttosto che, ad esempio, ripetute su tile parzialmente maturate per design
confounders: il rapporto è meccanicamente legato anche al numero di PLANT (basso in Antigravity, 91-100) quanto al numero di HARVEST (alto, 374-414); non è chiaro se il problema sia "troppe HARVEST inutili" o "troppo poche PLANT"
next_test_values: richiede telemetria aggiuntiva non ancora raccolta — success/failure flag per singola azione dispatchata (già elencata come osservabilità mancante in E15_FINAL_TOURNAMENT_SYNTHESIS §13)
falsification_condition: se un'ispezione diretta del codice/log azione-per-azione mostrasse che le HARVEST "in eccesso" sono in realtà valide (es. raccolta multi-tile legittima), la firma resterebbe una correlazione statistica ma perderebbe l'interpretazione causale di "dispatch failure"
```

```text
concept_id: worker_action_monetization_rate
feature_status: FEATURE
relationship: positive (come proxy macro)
e15_evidence: M1: proxy non calcolato esplicitamente ma final_money/azioni favorisce nettamente Codex. M2: $7.13/azione (Copilot) vs $5.17/azione (Codex). M3: proxy favorisce Copilot (final money 2.84× con azioni totali comparabili).
failure_region: non definito in termini assoluti, solo relativo al confronto diretto nella stessa coppia
success_region: idem
candidate_threshold_or_interval: nessun valore assoluto proponibile — il proxy dipende dalla durata dell'episodio (720 step fissi in E15) e non è stato validato contro un ledger reale
confidence: Medium — coerente in tutti i match disponibili, ma esplicitamente qualificato come "proxy macro, non ricavo marginale" in ogni consensus; il Copilot audit stesso lo declassa a NOT_DISCRIMINATED come meccanismo causale pur confermandolo come correlazione
confounders: il denominatore include MOVE (~70% delle azioni in tutti i match): due policy con MOVE-share identico ma monetizzazione diversa mostrano che il proxy macro nasconde grande eterogeneità nella qualità delle azioni non-movement
next_test_values: calcolare la forma "netta" già richiesta dall'ontologia (§B, worker_action_monetization_rate: forma macro E forma netta escludendo puro movimento) — mai riportata nei tre match
falsification_condition: se la forma netta (esclusa MOVE) invertisse il ranking rispetto alla forma macro in un futuro match, il concetto andrebbe riformulato come artefatto del denominatore
```

```text
concept_id: movement_overhead
feature_status: UNRESOLVED
relationship: conditional (discrimina in M3, non in M1/M2)
e15_evidence: M1: MOVE assoluto 5.019 vs 3.761, ma quota sul totale azioni ~71% per entrambi (NOT_DISCRIMINATED come quota). M2: 3.763 vs 3.768, quasi identico. M3: 5.047 vs 3.765, e qui il consensus lo classifica SUPPORTED.
failure_region: MOVE assoluto >5.000 in un episodio dove la quota relativa non è comunque distinguibile dal vincitore (M1)
success_region: MOVE assoluto ~3.760 in tutti i match vinti da Codex/Copilot
candidate_threshold_or_interval: nessuno — la stessa quota relativa (~70%) appare sia nei vincitori sia negli sconfitti; il concetto oscilla tra SUPPORTED e NOT_DISCRIMINATED a seconda del match, il che è di per sé informativo (dipende da cosa lo si confronta)
confidence: Low — verdetti discordanti tra match sullo stesso concetto senza una spiegazione strutturale registrata
confounders: `necessary_transit_fraction` (quota di movimento funzionale) non è mai stata calcolata in nessun match: senza di essa, MOVE assoluto o percentuale non distingue movimento "sprecato" da movimento necessario alla logistica di un working set più grande
next_test_values: richiede la metrica `necessary_transit_fraction` (già nell'ontologia, mai popolata) prima di ulteriori test quantitativi
falsification_condition: se, una volta introdotta `necessary_transit_fraction`, il movimento "in eccesso" di Antigravity risultasse comparabile in proporzione a quello di Copilot/Codex, l'ipotesi di un dispatch inefficiente specifico di Antigravity risulterebbe indebolita
```

### C — Crop care

```text
concept_id: watering_execution_rate
feature_status: FEATURE
relationship: thresholded
e15_evidence: M1: 34 (loser) vs 439 (winner). M3: 30 (loser) vs 439 (winner). M2: 475 (loser) vs 446 (winner) — qui il valore più ALTO perde.
failure_region: ~30–34 azioni WATER su 720 step (~1/giorno), osservato 2/2 volte con collasso della crop_surface_maintained
success_region: ~439–475 azioni WATER, osservato in tutti e tre i vincitori/quasi-vincitori
candidate_threshold_or_interval: fallimento osservato ≤34; adeguatezza osservata ≥439. L'intervallo 35–438 NON è mai stato campionato — non è un optimum, è un buco di osservazione enorme (quasi tutto il range utile dell'episodio).
confidence: High per "watering estremamente basso è catastrofico" (2 repliche indipendenti, seed e avversari diversi); Low/nullo per qualunque soglia puntuale, e M2 dimostra che tra 439 e 475 la relazione smette di essere monotona
confounders: watering è realizzato dalla stessa policy che decide workforce, quadranti e dispatch; non è mai stato variato isolatamente
next_test_values: 100 / 200 / 300 azioni WATER equivalenti (richiede varianti di policy, non testabili con le sole submission frozen attuali) per mappare il buco 35–438
falsification_condition: una policy con ~100-150 WATER che mantenga comunque una crop_surface_maintained comparabile ai vincitori attuali falsificherebbe la posizione della soglia vicino a 400+
```

*(`watering_continuity` mostra lo stesso pattern qualitativo di `watering_execution_rate` in tutti e tre i match — SUPPORTED in M1/M3, NOT_DISCRIMINATED in M2 — e non viene trattato come concetto separato in questo report per evitare duplicazione: l'evidenza e i confounder coincidono.)*

### D — Feed e livestock

```text
concept_id: livestock_headcount
feature_status: NOT_FEATURE
relationship: non_monotonic
e15_evidence: M1: 18 max/17 finale (loser) vs 7 (winner). M2: 7 (loser) vs 4 (winner). M3: 18 max/17 finale (loser) vs 4 (winner).
failure_region: herd ≥17-18 combinato con pasture ≥18 e crop_surface_maintained bassa
success_region: herd 4-7 in tutti i match vinti
candidate_threshold_or_interval: il README stesso [FRAME] avverte esplicitamente: "17-18 animali perdenti contro 4-7 non implica max_herd=4"; l'evidenza delimita un intervallo iniziale 4–17 da restringere, non un target
confidence: High per il rifiuto di "herd grande=meglio" (3/3 match); Low per qualunque valore specifico entro 4-7
confounders: herd size è quasi perfettamente collineare con pasture size nei dati osservati (18↔18, 7↔9, 4↔5); l'effetto attribuito al numero di animali potrebbe in parte appartenere alla superficie pasture o al feed drain associato
next_test_values: 4 / 7 / 10 / 13 / 17 a parità di pasture-alignment e cash buffer (valori esplicitamente indicati come piano di restringimento futuro in README §Evoluzione sperimentale, non ancora eseguiti)
falsification_condition: un herd di 10-13, correttamente allineato a pasture e feed, che produca final_money comparabile o superiore a 4-7 falsificherebbe l'ipotesi di un vantaggio specifico degli herd piccoli in sé (a favore di "allineamento conta più della taglia")
```

```text
concept_id: feed_market_dependency
feature_status: UNRESOLVED
relationship: unresolved / confounded
e15_evidence: M1: Antigravity dichiara autarky come Rank 2 Critical ma richiede 904-1.007 BUY_PRODUCT Wheat; Codex ne richiede ancora di più (1.334-1.483) e vince. M2/M3: Copilot richiede più Wheat di mercato di Antigravity/Codex e vince comunque.
failure_region: non isolabile — alta dipendenza da mercato Wheat è presente sia nei vincitori sia negli sconfitti in tutti e tre i match
success_region: non isolabile, per lo stesso motivo
candidate_threshold_or_interval: nessuno — questo è uno dei concetti dove l'evidenza rifiuta la semplice equivalenza "dipendenza dal mercato = negativo", coerentemente con la separazione canonica esplicita nell'ontologia (§5.4 "feed security = feed autarky" è un'equivalenza rifiutata)
confidence: Low (CONFOUNDED in 3/3 match, nessuna direzione stabilita)
confounders: la quantità RICHIESTA di Wheat non distingue tra acquisto di emergenza (a prezzo penalizzato) e flusso operativo deliberato a scopo di liquidità; manca sia il ledger eseguito sia il prezzo pagato per unità
next_test_values: impossibile progredire senza executed transaction ledger con prezzo per ordine — priorità di osservabilità, non di test aggiuntivo
falsification_condition: se il ledger eseguito mostrasse che i vincitori pagano sistematicamente prezzi peggiori per il Wheat comprato, l'ipotesi "dipendenza dal mercato è ininfluente" andrebbe rivista in "dipendenza dal mercato ha un costo ma è compensata altrove"
```

```text
concept_id: species_margin_differential
feature_status: UNRESOLVED
relationship: unresolved
e15_evidence: M1: Codex vince con 0 Sheep/7 Cow. M2: Copilot vince con 0 Sheep/4 Cow (nessuna Sheep in nessuno dei due player). M3: Copilot vince con 0 Sheep/4 Cow contro Antigravity 13 Cow/4 Sheep.
failure_region: non osservabile — nessun match confronta direttamente il margine Wool vs Milk a parità di altre condizioni
success_region: non osservabile
candidate_threshold_or_interval: nessuno — 2/3 match non contengono Sheep in nessuno dei due giocatori
confidence: Low (NOT_DISCRIMINATED in tutti e 3 i consensus)
confounders: Antigravity è l'unico agente che alleva Sheep, ma lo fa insieme a una scala complessiva 4× più grande di tutto il resto; l'eventuale svantaggio economico delle Sheep è indistinguibile dall'effetto scala generale
next_test_values: confronto diretto Cow-only vs Sheep-only a parità di headcount e pasture (nessuna submission frozen attuale lo permette)
falsification_condition: qualunque risultato futuro con dati sufficienti a isolare il margine per specie; al momento non esiste falsificazione possibile perché non esiste discriminazione
```

### E — Capitale, mercato, conversione

```text
concept_id: operating_cash_buffer
feature_status: UNRESOLVED
relationship: non_monotonic / thresholded verso il basso
e15_evidence: M1: Codex apre con $928 vs $176 Antigravity e vince; ma Antigravity supera Codex in cash ai Day 8-9 e 18. M2: Copilot accetta cash molto più basso di Codex nei Day 4-9 (es. Day 9: $225 vs $837) e vince comunque. M3: Antigravity scende a $73 (Day 18) sotto stress da espansione e perde.
failure_region: cash quasi a zero ($73-$81) IN COINCIDENZA con una fase di espansione attiva (acquisto Q2/herd ramp) — osservato 2/2 volte per Antigravity
success_region: cash basso temporaneo SENZA espansione simultanea (Copilot M2, Day 4-9) non impedisce la vittoria
candidate_threshold_or_interval: nessuno assoluto — ciò che sembra discriminare non è il livello di cash ma la sua co-occorrenza con impegni di spesa aggiuntivi; il consensus M2 arbitra esplicitamente CONFOUNDED, non SUPPORTED
confidence: Low-Medium — il pattern "cash quasi a zero + espansione = fragilità" è visivamente coerente ma non è mai stato isolato da un esperimento controllato
confounders: il livello di cash è un effetto a valle di tutte le altre decisioni di spesa simultanee (hiring, land, animali, seed); trattarlo come causa indipendente rischia di invertire la direzione causale reale
next_test_values: nessun valore numerico proponibile in modo responsabile finché non si separa "cash basso per scelta" da "cash basso per fallimento di conversione"
falsification_condition: un match dove un buffer di cash elevato e stabile per tutta la partita produce comunque un risultato peggiore di un buffer variabile/basso confermerebbe che il livello assoluto non è la variabile rilevante (parzialmente già osservato in M2)
```

```text
concept_id: deployable_capital_window
feature_status: FEATURE
relationship: positive (timing dell'investimento, non l'ammontare)
e15_evidence: M1: Codex investe mantenendo liquidità disponibile in momenti chiave, mentre Antigravity la esaurisce durante Q2. M2: Copilot investe presto (cash basso Day 4-9) poi converte rapidamente in crescita di cash da Day 10. M3: Copilot entra in generazione di cash sostenuta prima di Antigravity.
failure_region: capitale immobilizzato in asset (land/herd) senza una finestra successiva di generazione di cash osservabile (Antigravity, entrambe le occorrenze)
success_region: capitale investito seguito, entro pochi giorni, da una traiettoria di cash crescente e sostenuta (Copilot/Codex M1)
candidate_threshold_or_interval: non quantificato in giorni in modo comparabile tra i match (M1: lock-in permanente Day 19; M2: ~Day 12; M3: Day 10 Hour 12) — la LATENZA tra investimento e ritorno varia troppo tra match per proporre un intervallo unico
confidence: Medium — direzione coerente in 3/3 match, ma la variabile temporale non è normalizzata tra match diversi
confounders: la finestra "deployable" dipende dal mix esatto di spese pregresse; due episodi con la stessa cash disponibile ma storie di spesa diverse potrebbero avere finestre diverse per ragioni non catturate
next_test_values: normalizzare la metrica come "giorni dal picco di investimento al recupero del cash pre-investimento" e confrontarla su più seed
falsification_condition: un investimento seguito da un ritorno di cash comparabile in tempi simili a quello dei vincitori ma senza vantaggio economico finale falsificherebbe il legame fra finestra di capitale e risultato
```

```text
concept_id: inventory_to_cash_conversion
feature_status: FEATURE
relationship: positive (come proxy da conteggio ordini, non da valore realizzato)
e15_evidence: M1: Codex registra un mix di vendita più ampio (incl. Strawberry/Melon) mentre Antigravity non registra vendite di cash crop. M2: Copilot 298 SELL vs Codex 212. M3: Copilot 302 SELL vs Antigravity 198.
failure_region: assenza quasi totale di SELL su prodotti cash-crop ad alto valore (Antigravity, M1)
success_region: SELL orders numerosi e diversificati per prodotto (Copilot in M2/M3, Codex in M1)
candidate_threshold_or_interval: nessuno in termini di valore monetario reale — tutti i numeri sono conteggi di ordini richiesti, non quantità/valore eseguiti (vedi §A.4)
confidence: Medium — direzione coerente in 3/3 match, ma esplicitamente qualificata come "cautela requests≠executions" in ogni consensus
confounders: più ordini SELL richiesti potrebbero riflettere più tentativi (incl. falliti/ripetuti) piuttosto che più valore effettivamente incassato
next_test_values: richiede ledger eseguito; senza di esso qualunque soglia numerica sarebbe inventata
falsification_condition: se il ledger eseguito mostrasse che gran parte dei 298-302 SELL Copilot falliscono o si annullano a vicenda (es. wash trading Wheat), la relazione "più SELL orders = più cash" risulterebbe artefattuale
```

```text
concept_id: market_transaction_value
feature_status: UNRESOLVED
relationship: unresolved (osservabilità insufficiente)
e15_evidence: In tutti e tre i match il verdetto è esplicitamente INCONCLUSIVE — nessun dossier disponibile ricostruisce prezzo realizzato o valore netto per transazione.
failure_region: non osservabile
success_region: non osservabile
candidate_threshold_or_interval: non proponibile
confidence: n/a — questo è un caso in cui l'assenza di dati è essa stessa il risultato principale, non una conclusione debole su un fenomeno osservato
confounders: qualunque interpretazione di "chi guadagna di più per unità venduta" costruita sui soli conteggi di ordini sarebbe una sovrainterpretazione non supportata
next_test_values: aggiungere, alla harness esistente, la cattura di prezzo × quantità eseguita per ordine (già richiesto in ONTOLOGY_E15_FROZEN §8.6 e in E15_FINAL_TOURNAMENT_SYNTHESIS §13, mai implementato)
falsification_condition: non applicabile finché l'osservabilità non esiste
```

### G — Condizione del campo

```text
concept_id: field_cleanliness_state
feature_status: NOT_FEATURE
relationship: unresolved / negative-if-anything
e15_evidence: M1: Codex termina con 22 weeds e vince; Antigravity con 5 weeds e perde. M2/M3: non emerge come driver economico.
failure_region: n/d
success_region: n/d
candidate_threshold_or_interval: non applicabile
confidence: Medium per la conclusione negativa (coerente con la separazione canonica esplicita "clean field = profitable field" esclusa dall'ontologia §5.8)
confounders: pochi weeds in Antigravity riflettono probabilmente un campo scarsamente coltivato (meno tile attive da infestare), non una gestione superiore — un caso di causalità inversa
next_test_values: nessuno prioritario — l'evidenza è già coerente nel rifiutare questo concetto come feature diretta
falsification_condition: un caso dove un campo pulito E ampiamente coltivato producesse un vantaggio economico chiaro rispetto a un campo sporco ma altrettanto coltivato risolleverebbe il concetto
```

### H — Diagnostica

```text
concept_id: state_capacity_alignment
feature_status: FEATURE
relationship: conditional / interaction (non riducibile a una singola variabile)
e15_evidence: concetto più consistentemente SUPPORTED in tutti e tre i consensus. M1/M3: capacità nominale alta + capacità attivata bassa (Antigravity) perde. M2: capacità nominale comparabile, ma capacità monetizzata diversa (Copilot) vince.
failure_region: nominal capacity ≫ maintained/monetized capacity
success_region: maintained/monetized capacity ≈ working-set size scelto deliberatamente
candidate_threshold_or_interval: nessun valore numerico — l'ontologia stessa lo qualifica PROVISIONAL e richiede una formula esplicita mai fornita in nessun match
confidence: Medium — è il concetto con la direzione più stabile (3/3), ma è anche il meno operazionalizzato quantitativamente di tutti quelli qui trattati
confounders: senza una formula pre-registrata, "alignment" rischia di essere un'etichetta post-hoc applicata a qualunque pattern coerente con l'esito già noto (rischio di conferma circolare)
next_test_values: pre-registrare una formula (es. crop_surface_maintained / activated_land_surface, o monetized_productive_output / worker_capacity_available) PRIMA di osservare il risultato di un nuovo match
falsification_condition: se, una volta fissata una formula pre-registrata, un match mostrasse alignment più basso nel vincitore, il concetto andrebbe riformulato o scomposto
```

```text
concept_id: economic_lock_in_onset
feature_status: FEATURE (come fenomeno), ma NOT_FEATURE come costante temporale
relationship: timing, non fisso
e15_evidence: M1: lock-in permanente Day 19. M2: ~Day 12 (step 301, Day 12 Hour 13). M3: step 252, Day 10 Hour 12 — prima ancora del Q1 Copilot.
failure_region: n/d (è un fenomeno di timing, non di successo/fallimento)
success_region: n/d
candidate_threshold_or_interval: nessuna soglia unica — i tre valori osservati (Day 19, Day 12, Day 10H12) differiscono per quasi un terzo dell'episodio; l'ontologia stessa vieta di trattarlo come sinonimo di `operational_divergence_onset` o come costante universale (§5.9)
confidence: High per l'esistenza del fenomeno come distinto dalla divergenza operativa iniziale; Low per qualunque valore di riferimento comune tra match
confounders: **attenzione specifica**: nel corpus pre-E15 (E13, background) un gap economico "si blocca" anch'esso attorno al Day 12 (episodio Harith/Pietro). La coincidenza numerica con M2 è **[MY-INFERENCE]** probabilmente casuale o un artefatto della struttura del gioco (es. sblocco Q1 verso metà partita), non evidenza di una legge universale "Day 12": trattarla come tale sarebbe un errore di pattern-matching tra esperimenti diversi (E13 non è evidenza E15)
next_test_values: registrare systematicamente step/day di lock-in su nuovi seed per costruire una distribuzione, non un singolo valore
falsification_condition: se la distribuzione dei lock-in su più seed si concentrasse strettamente attorno a un giorno specifico, la posizione "nessuna costante universale" andrebbe rivista
```

---

## D. Confounder analysis

| # | Confounder | Feature collegate | Interpretazione falsa possibile | Osservabilità mancante | Esperimento separatore |
|---|---|---|---|---|---|
| 1 | **Requested orders vs executed transactions** | `worker_action_monetization_rate`, `inventory_to_cash_conversion`, `feed_market_expenditure`, `market_churn_cost`, `market_transaction_value` | "Più SELL/BUY orders → più profitto/perdita reale" | Ledger di esecuzione con prezzo e quantità effettivamente riempita per ordine | Instrumentare l'harness (nessuna modifica alla policy) per loggare fill-quantity e prezzo per ogni ordine |
| 2 | **Espansione simultanea multi-variabile** (Antigravity) | `land_surface_total`, `workforce_headcount`, `livestock_headcount`, `land_activation_payback` | "3Q causa la sconfitta" (in realtà 3Q, 12 hands e 18 livestock crescono insieme) | Nessuna ablation con una sola variabile alla volta | Richiede varianti di policy con una singola dimensione variata per volta (non autorizzato in questa fase) |
| 3 | **N=1 seed per pairing** | Tutti i verdetti `SUPPORTED` | "Il pattern osservato è strutturale/generale" | Distribuzione di risultati su seed multipli | Rieseguire le stesse 3 submission frozen su seed nuovi (proposta §E) |
| 4 | **Proxy di dispatch (HARVEST/PLANT) invece di effectiveness reale** | `action_dispatch_failure`, `routing_completion_efficiency`, `movement_overhead` | "Ogni HARVEST in eccesso è un fallimento" | Flag di successo/fallimento per singola azione dispatchata | Aggiungere action-level success telemetry (già richiesto in ONTOLOGY §8.3) |
| 5 | **Adozione asimmetrica dell'ontologia tra i tre MODEL_SPEC** (da PROJECT_STATE/EXPERIMENT_LOG: Antigravity 59 USED, Codex 37 USED, Copilot 50 USED su 64) | Qualunque confronto diretto tra concetti "assenti" in un modello vs "presenti" in un altro | "Il concetto X non conta perché il modello Y non lo usa" | Non è possibile distinguere "concetto irrilevante" da "concetto non modellato per scelta implementativa" | Verificare se, introducendo esplicitamente un concetto oggi `NOT_USED`, il comportamento migliora — richiede revisione MODEL_SPEC, non ancora autorizzata |
| 6 | **P0/P1 come argomento strutturale, non statistico** | Validità di ogni confronto pairwise | "Il vantaggio P1 in M3 (+$17.258) potrebbe riflettere bias posizionale" | Test statistico multi-seed dell'effetto posizione (l'audit attuale è un'analisi del codice, non un campione di risultati) | Ripetere gli stessi match con P0/P1 invertiti sugli stessi seed, oltre al già presente bilanciamento round-robin |
| 7 | **Coincidenza numerica cross-esperimento** (es. "Day 12" in E13 e in M2) | `economic_lock_in_onset` | "Esiste una soglia temporale universale del gioco" | Distribuzione di lock-in onset su molti episodi/seed indipendenti | Registrare onset su nuovi seed prima di formulare qualunque soglia temporale |
| 8 | **`final_money` come aggregato unico** | `product_mix_revenue`, `crop_revenue_mix`, `livestock_product_flow` | "La feature X spiega il gap economico" quando in realtà il gap è la somma di più flussi (crop + livestock + costi feed + costi land) che si muovono insieme | Scomposizione per categoria di ricavo/costo con provenienza prezzo | Richiedere breakdown `product_mix_revenue` con valore per categoria, non solo conteggio ordini |

---

## E. Candidate design for the next common training round

Principio guida **[MY-INFERENCE]**: le due incertezze che bloccano il maggior numero di verdetti `CONFOUNDED`/`INCONCLUSIVE`/`NOT_ESTABLISHED` sono, trasversalmente, (a) l'assenza di un ledger di esecuzione e (b) l'assenza di replica multi-seed. Il disegno minimo che le attacca entrambe **non richiede modificare né generare alcuna policy**: riusa le tre submission frozen esistenti, invariate, su nuovi seed, con telemetria arricchita. Questo rispetta il vincolo "E15 è già TRAINING EVIDENCE" perché non introduce nuove ipotesi di modello, si limita a testare la robustezza delle ipotesi già emerse.

```text
training_or_validation: TRAINING
hypothesis: Le policy fingerprint osservate in E15 (collasso Antigravity a basso watering/alta scala nominale; vittoria Copilot con working set compatto e alta monetizzazione; posizione intermedia Codex) sono proprietà strutturali delle tre submission frozen, non artefatti dei tre seed/pairing specifici testati in E15.
feature_under_test: watering_execution_rate (esistenza soglia ~34 vs ~440), state_capacity_alignment (direzione), pasture_arable_surface_tradeoff, deployable_capital_window, worker_action_monetization_rate (forma netta vs macro)
controlled_variables: environment version (0.1.0, invariato), le tre submission frozen (SHA256 invariati, nessuna modifica), ontologia frozen, protocollo di posizione (round-robin P0/P1 bilanciato come in E15)
test_values: 5 nuovi seed non utilizzati in E15, ciascuno con tutte e 3 le coppie possibili (Antigravity-Codex, Codex-Copilot, Copilot-Antigravity) in entrambe le posizioni P0/P1 → 30 match totali (5 seed × 3 coppie × 2 posizioni), oppure un sottoinsieme ridotto (es. 3 seed) se il budget computazionale è vincolante — il minimo utile è ≥3 seed nuovi per iniziare a stimare varianza inter-seed
expected_discrimination: se il pattern Copilot 2-0/Antigravity 0-2 si replica in ≥4/5 seed, GENERALIZATION passa da NOT_ESTABLISHED a PARTIALLY_ESTABLISHED; se il record si inverte o si disperde (es. 3-2, 2-3 in modo non sistematico), la spiegazione "state_capacity_alignment" perde forza a favore di "risultato E15 fortemente seed-dependent"
falsification_condition: Antigravity vince ≥50% dei nuovi match contro Codex o Copilot senza modifiche alla propria submission → falsifica la generalità della diagnosi POLICY_REALIZATION/IMPLEMENTATION_FIDELITY di E15 e sposta l'attribuzione verso variabilità di seed (prezzi di mercato, spawn weeds, RNG) più che verso un difetto sistematico della policy
evidence_that_must_be_recorded: (1) executed transaction ledger per ordine (tipo, quantità richiesta, quantità eseguita, prezzo unitario realizzato); (2) crop_surface_maintained e pasture_surface_maintained per giorno (non solo massimo di episodio); (3) success/failure flag per azione dispatchata, almeno per HARVEST e WATER; (4) money_trajectory già presente, mantenuta; (5) step/day esatto di operational_divergence_onset ed economic_lock_in_onset con soglia dichiarata esplicitamente prima dell'analisi, non ricostruita a posteriori
```

Ho deliberatamente **escluso** dal disegno minimo qualunque variante di policy (es. sweep di `livestock_headcount` a 7/10/13) perché richiederebbe generare nuovo codice/policy, non autorizzato in questa fase e non necessario per il guadagno di informazione più urgente (generalizzazione + osservabilità). Questi sweep restano il passo naturale **successivo**, condizionato all'autorizzazione della revisione MODEL_SPEC (Fase C del piano post-E15 già delineato in `E15_FINAL_TOURNAMENT_SYNTHESIS.md` §11).

---

## F. Epistemic audit

### SUPPORTED
- La capacità nominale posseduta (land/workforce/livestock) presa da sola non predice `final_money` in nessuno dei tre match.
- Watering estremamente basso (~30-34/720 step) co-occorre, in 2 repliche indipendenti (seed e avversario diversi), con collasso della superficie coltivata mantenuta e con la sconfitta.
- Oltre una soglia elevata di watering/manutenzione, ulteriori incrementi non discriminano più il risultato (M2: 475 perde contro 446).
- `state_capacity_alignment` è, qualitativamente, il concetto più coerentemente associato all'esito nei tre match, pur senza formula operazionale.
- I dati di mercato registrati in tutti e tre i match sono conteggi di ordini richiesti, non un ledger di transazioni eseguite.
- Antigravity non realizza, nella propria submission frozen, la propria stessa policy dichiarata Rank 1 (`irrigation_dispatch_priority`).
- Nessuna asimmetria strutturale P0/P1 è stata individuata a livello di codice/meccaniche di gioco (analisi statica, non statistica).

### PROVISIONAL
- Il "modello a due regimi" (sotto/sopra soglia operativa) come descrizione dell'insieme dei tre match.
- Pasture/livestock dovrebbero essere dimensionati in funzione di crop/cash/workforce piuttosto che come target fisso.
- Il timing dell'investimento (deployable_capital_window) conta più dell'ammontare assoluto di cash trattenuto.
- `worker_action_monetization_rate` come proxy macro utile, in attesa della sua forma "netta" (mai calcolata) e di un ledger reale.

### UNRESOLVED
- Qualunque valore soglia numerico preciso per watering, crop-surface o livestock (gli intervalli osservati sono ampi e i punti intermedi non sono mai stati campionati).
- Profittabilità reale (netta) del flusso Wheat, del costo feed, dei prodotti livestock (Milk/Wool/Fertilizer) — bloccata dall'assenza di un ledger eseguito.
- Differenziale di margine tra specie (Cow vs Sheep).
- Attribuzione causale tra le variabili che crescono simultaneamente nella policy Antigravity (land, workforce, livestock, dispatch).
- Se il pattern 2-0/1-1/0-2 di E15 generalizza a seed diversi da quelli testati.
- Se il costo di opportunità del "field cleanliness" sia mai negativo quando interagisce realmente con superficie produttiva (nei match osservati non si è mai verificata questa interazione in modo isolabile).

### DO_NOT_INFER
- Che 439 WATER, 4 animali, 5 pasture, 9 hands o 2 quadranti siano target ottimali universali da copiare in una revisione MODEL_SPEC.
- Che 2 quadranti siano sempre superiori a 3 come legge generale dell'ambiente.
- Che il MODEL_SPEC Copilot sia "il modello corretto" perché la submission Copilot ha vinto 2–0.
- Che il MODEL_SPEC Antigravity sia falsificato nel suo complesso: la sua `MODEL_VALIDITY` resta `PARTIALLY_SUPPORTED`, il fallimento osservato è primariamente di `POLICY_REALIZATION`/`IMPLEMENTATION_FIDELITY`.
- Che il churn di Wheat sia profittevole o dannoso: nessun ledger lo dimostra in un senso o nell'altro.
- Che l'endgame inventory liquidation abbia un ruolo causale indipendente nel gap finale (in ogni match il gap economico è già consolidato ben prima della fase di endgame).
- Che esista una soglia temporale universale ("Day 12") di lock-in economico valida su tutti gli episodi/esperimenti, inclusi quelli pre-E15.
- Che una qualunque relazione `SUPPORTED` in un singolo match si estenda automaticamente oltre il seed/avversario in cui è stata osservata.

---

**Chiusura:** ricostruzione dell'evidenza, feature discrimination, initial bounding, identificazione dei confounder e proposta di disegno per il prossimo round comune sono completati. Nessun file del repository è stato modificato durante l'analisi; nessuna `MODEL_SPEC` è stata proposta; nessuna policy vincitrice è stata dichiarata; nessun parametro ottimale è stato fissato.
