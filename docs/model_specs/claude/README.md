# Indice MODEL_SPEC Claude

> **Linea congelata dal 2026-09-04 — `FROZEN_PERFORMANCE_GAP`.** Le candidate
> restano riproducibili e consultabili, ma nessuna è attiva per sviluppo o
> submission. Lo scongelamento richiede una nuova ipotesi preregistrata che
> superi insieme i gate economico e di sicurezza.

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

Gli asset riproducibili specifici di Claude sono in `e17/` ed `e18/`. Claude
condivide i manifest e i protocolli comuni, ma mantiene autonomi modello,
feature consumate, planner, priorità, routing e implementazione.

Le candidate degli altri agenti possono essere usate soltanto come avversari
black-box nei runner comuni; non sono componenti della policy Claude.
