# Indice MODEL_SPEC Claude

> **Linea abbandonata dal 2026-09-09 — `ABANDONED_PERFORMANCE_GAP`.** Le
> candidate restano riproducibili e consultabili, ma la linea è chiusa per
> decisione del proprietario: nessuna nuova iterazione, tuning o submission.
> Un torneo dal vivo di E18.4 contro Codex V48 aveva trovato zero bestiame
> collocato in tutte le 14 partite: causa isolata in un verbo di mercato
> invalido presente dalla primissima versione E18. La correzione
> (`MODEL_SPEC_CLAUDE_E18_5_WHEAT_MARKET_FIX_V1.md`) è verificata come
> corretta a livello di motore, ma il torneo di verifica ha mostrato che
> **peggiora** il risultato economico (−67,7% di cassa media rispetto a
> E18.4: senza freno di quantità, l'acquisto di grano diventa incontrollato).
> Nel torneo a tre vie E18.5 vs E18.4 vs Codex V48
> ([report](../../../experiments/e18/reports/common/E18_CLAUDE_E18_5_VS_E18_4_VS_CODEX_V48_D01_D30_COMPLETE_KPI.html))
> entrambe restano molto al di sotto di Codex. Ipotesi falsificata dalla
> verifica; il freno di quantità mancante resta documentato come causa nota
> ma non più perseguito su questa linea.

| Stato | File | Uso |
|---|---|---|
| REJECTED | `MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE.md` | V1, gate economico e zootecnico falliti |
| DEVELOPMENT / FAILED GATES | `MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE_V2.md` | remediation V2 |
| DEVELOPMENT / FAILED GATES | `MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE_V3.md` | attivazione 10x e workforce readiness |
| DEVELOPMENT / FAILED GATES | `MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE_V4.md` | piano statico V4 |
| DEVELOPMENT / NOT PROMOTED | `MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE_V5.md` | sviluppo V5 |
| REJECTED | `MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE_V6.md` | regressione V6 |
| DEVELOPMENT | `MODEL_SPEC_CLAUDE_E18_1_OPPONENT_REACTIVE_V1.md` | candidata opponent-reactive V1 |
| FAILED INTAKE | `MODEL_SPEC_CLAUDE_E18_2_OPPONENT_REACTIVE_V2.md` | candidata V2 con gate real-engine falliti |
| ITERATE / SAFETY GATE FAILED | `MODEL_SPEC_CLAUDE_E18_3_LIFECYCLE_SAFETY_V1.md` | due fix di dispatch verificati (identità worker, stallo `PICKUP`); `SAFETY_GATE` migliora da 24/28 a 13/28 ma resta `FAIL` (richiesto 0/28) |
| PROPOSED / DEVELOPMENT | `MODEL_SPEC_CLAUDE_E18_4_CAPACITY_CERTIFIED_V1.md` | gate di capacità giornaliera ispirato al confronto con Codex V48, isolato da tutto il resto di V3; torneo dal vivo vs Codex V48 (14 partite): 0 bestiame collocato in tutte le partite, causa isolata (vedi E18.5) |
| NOT PROMOTED — HYPOTHESIS FALSIFIED | `MODEL_SPEC_CLAUDE_E18_5_WHEAT_MARKET_FIX_V1.md` | candidata più recente: corregge il verbo di mercato del grano (`BUY_WHEAT` invalido → `BUY_PRODUCT WHEAT`), verificato dal motore; ma il torneo dal vivo vs Codex V48 mostra cassa media −68% (11.147→3.598): senza freno di quantità l'acquisto di grano è incontrollato (418-1.068 unità/partita) e in 10/14 partite priva anche Codex del proprio grano |

Gli asset riproducibili specifici di Claude sono in `e17/` ed `e18/`. Claude
condivide i manifest e i protocolli comuni, ma mantiene autonomi modello,
feature consumate, planner, priorità, routing e implementazione.

Le candidate degli altri agenti possono essere usate soltanto come avversari
black-box nei runner comuni; non sono componenti della policy Claude.
