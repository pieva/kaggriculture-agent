# E18.30 — primo nucleo anti-PASS, contratti Gate 0

2026-09-05. Stato: **CORE_CONTRACTS_PASS / RUNTIME_ADAPTER_PENDING**.
Avviato dopo commit/push del checkpoint e della correzione freeze, `f036cd6`.
Nessun upload, holdout o modifica a E18.28 C pubblicata.

## Implementato

`tools/e18_30_mission_dispatcher.py` separa missioni semantiche, offerte di
rotta e assegnazioni. Ledger condiviso tra worker realmente osservati;
recupero missioni orfane, bloccate o prive di nuova verifica. DONE richiede
conferma osservata: nessun avanzamento automatico per tempo trascorso,
comando emesso o coda terminata. Deduplica per ID e budget comune impediscono
doppi impegni di scorte, spazio shed o claim esclusivi tile/ciclo.

Priorità: conservare missioni attive fattibili, poi safety, deadline,
valore per slot complessivo e costo di rotta. Criterio greedy deterministico,
non ottimo globale. Ridurre PASS non sostituisce l'obiettivo economico.

## Verifiche

- 25 test unitari, 0,18 s: HIRE non confermato, worker assente, pool condiviso,
  blocco temporaneo, retry con nuova rotta, stale offer, dipendenze, consegna
  oltre deadline, duplicati, budget e rilascio claim obsoleti.
- Uno dei test esercita 100 scenari sintetici permutati, con risorse, scadenze
  e roster diversi: nessun doppio incarico o superamento delle capacità e
  indipendenza dall'ordine degli input. Nessun ID/seed/coordinate Kaggle usato.
- Suite repository/integrità dataset/reporting con il nucleo completo:
  **98 pass in 26,49 s**. La suite dedicata del nucleo contiene 25 test.
- Checkpoint base prima del nuovo codice: 327 pass repository/Codex E18/common,
  dopo la rimozione cache. Verificati 193 freeze byte-identici in Git.

## Limiti e prossimo passo

Il nucleo **non è ancora un agente Kaggle**. L'adattatore deve fornire ID
persistenti dei worker, conferme osservate e offerte fresche per le rotte
complete residue: viaggio, prerequisiti, servizio, inventario e consegna.
Capacità correnti prima delle prenotazioni; claim delle sole risorse ancora
necessarie, non di quelle già consumate. Un trasferimento con merci in viaggio
richiede recovery esplicita dell'adattatore, non semplice spostamento della coda.

Prossimo passo: adattare le missioni già nel piano E18.28 C senza cambiarne
gli obiettivi economici; validare nel motore e verificare OFF action parity.
Poi ablation redistribuzione, payroll/HIRE e nuove missioni, separatamente;
gate matched su più seed e campioni interni. Non trasferire MOVE assolute.

Non dimostrati recupero dei due casi D11, riduzione PASS D15-D30, eliminazione
delle morti crop o maggiore cassa. Il Gate 0 completo richiede anche OFF parity;
i gate economici non sono stati eseguiti in questa tranche.
