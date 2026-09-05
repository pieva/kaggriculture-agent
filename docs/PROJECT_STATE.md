# PROJECT_STATE — Kaggriculture

## Stato operativo — 2026-09-05, checkpoint anti-PASS

**Linea attiva Codex, target 770, cap 14 animali / massimo 12 manovali.**
Antigravity, Claude e Copilot congelati. Priorità autorizzata: riprogettare
assegnazione e ciclo di vita delle missioni, non cambiare topologia.

| Ruolo | Versione | Stato |
|---|---|---|
| Ultima pubblicata | E18.28 C / 56036993 | immutabile, verifica esterna; non promossa |
| Ultimo sviluppo | E18.29 B3 | +7,68% matched locale, mortalità residua; non pubblicata |
| Nuovo sviluppo | E18.30 mission dispatcher | specifica e avvio nucleo isolato; gate end-to-end da eseguire |
| Controlli | E18.16, E18.2 | benchmark interni e riferimento esterno storico |

Corpus E18.28 congelato: 30 replay (17 LOSS, 13 WIN), 21.570 batch shadow
identici al pubblicato, ledger 29/30 verificati inclusi tutti i LOSS. Nelle
sconfitte, D15-D30 746,3 PASS medi: 83,5% code esaurite, 16,5% attese.
Due fallimenti payroll/HIRE D11 lasciano WATER/HARVEST a manovali assenti.
Analisi completa, limiti e prossime azioni:
`docs/model_specs/codex/e18/reports/E18_28_EXTERNAL_PASS_CAUSES_AND_NEXT_ACTIONS_IT.md`.

Non estrapolare score correnti dai report storici e non presentare la riduzione
dei PASS come guadagno economico acquisito. E18.29 non risolve il difetto
strutturale; nuovo motore da validare contro più campioni e seed, senza tuning
su Top770. Crescita progressiva mucche ancora non risolta, non priorità attuale.

Handoff autorevole: `docs/NEW_SESSION.md`. Specifica agente:
`docs/model_specs/codex/e18/MODEL_SPEC_CODEX_E18_30_770_MISSION_DISPATCHER_V1.md`.
Reporting comune V3: due curve, Top770 vs candidata, 21 pannelli e KPI operativi.
Processo: confronto interno, migliore candidata eleggibile pubblicata ogni giorno
e analisi strategica quotidiana dei top; nessun nuovo upload in questo checkpoint.

La cronologia precedente e i vecchi stati CURRENT sono archiviati in
`docs/history/PROJECT_STATE_PRE_ANTI_PASS_20260905.md`; non sono priorità attive.
La Foundation non viene alterata per mascherare difetti di implementazione:
restano separati capacità strutturale/servibile, scorte, cassa e deadline.
Closeout e verifiche: `docs/model_specs/codex/e18/reports/E18_ANTI_PASS_CHECKPOINT_20260905_IT.md`.
