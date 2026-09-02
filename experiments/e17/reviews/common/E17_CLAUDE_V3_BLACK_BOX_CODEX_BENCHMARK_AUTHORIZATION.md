# E17.1 — Autorizzazione Claude V3 al benchmark Codex black-box

- **Data:** 2026-09-02
- **Decisione:** `AUTHORIZED_DEVELOPMENT_ONLY`
- **Candidata interessata:** futura `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V3`
- **Stato implementazione:** `NOT_STARTED`
- **Holdout/final confirmation:** `FORBIDDEN / NOT_CONSUMED`

## Decisione

Claude è autorizzato a usare Codex V9 congelato e/o Codex E17.1 reattivo
congelato come avversari **black-box** durante lo sviluppo della propria V3.
L'autorizzazione serve a misurare la robustezza sotto contesa, non a trasferire
la strategia Codex nella policy Claude.

## Operazioni consentite

- eseguire match sui soli seed development già consumati;
- invocare le factory pubbliche delle candidate Codex da un runner di
  benchmark esterno alla policy Claude;
- osservare stato pubblico, azioni ed esiti prodotti dal normale contratto di
  gioco;
- analizzare i ledger della propria policy e le metriche aggregate comuni;
- confrontare denaro finale, W/L/T, timing Q1/Q2, hands, topologia, densità,
  fughe, errori, MOVE/produttive e indicatori di mercato;
- eseguire ablation preregistrate che modifichino una sola famiglia causale.

## Operazioni vietate

- aprire, leggere, cercare, riassumere o copiare sorgenti, routine, schedule,
  action table, config o MODEL_SPEC Codex;
- importare codice Codex nel decision path della policy Claude;
- ricostruire la strategia Codex tramite dump o imitazione delle sequenze di
  azioni;
- modificare le candidate Codex congelate;
- usare seed holdout o final-confirmation;
- presentare un confronto development come selezione ufficiale o prova
  causale conclusiva.

L'import della sola factory pubblica Codex nel runner di benchmark è
infrastruttura di esecuzione e non costituisce dipendenza strategica. Il
sorgente del runner deve restare separato dal namespace della policy.

## Gate invariati per Claude V3

```text
STRATEGIC_INDEPENDENCE_GATE == PASS
TECHNICAL_ERRORS == 0
INVALID_ACTIONS == 0
LEDGER_COVERAGE == 100%
ANIMAL_ESCAPES == 0
THREE_QUADRANTS == ALL_DEVELOPMENT_RUNS
PASSIVE_DEVELOPMENT_MEAN >= 50000
REACTIVITY_TESTS == PASS
HOLDOUT_USED == false
FINAL_CONFIRMATION_USED == false
```

Il risultato competitivo development deve essere riportato integralmente,
anche quando negativo, ma non introduce da solo una soglia di promozione
post-hoc.

## Limiti della decisione

Questa decisione autorizza il metodo di sviluppo V3. Non avvia
l'implementazione, non sblocca il torneo holdout, non autorizza una submission
Kaggle e non modifica la Foundation C2.1.
