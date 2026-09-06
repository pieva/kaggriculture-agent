# E18.31 — chiusura operativa della verifica esterna iniziale

2026-09-06. Richiesta eseguita senza cambiare le policy della V11 verificata.

## Risultati consegnati

- Report desktop storico aggiornato a V4, 22 grafici: FEED e CARE distinti.
- Submission E18.31 **56050866**, Complete; receipt/hash e parità standalone conservati.
- Sei primi replay competitivi congelati: 5 WIN / 1 LOSS, zero perdite biologiche,
  tutti i ledger monetari riconciliati. Nessuna promozione dell'incumbent.
- Registro comune monouso: storico Top770-001 consumato; 14 nuovi autori
  sottoposti a screening, primo qualificato Top770-002 (4/5 exact770).
- Cinque replay del nuovo riferimento conservati, quattro nel nuovo report
  desktop pubblico contro sei nostri. Anche questo ciclo ora è esposto/consumato.
- NEW_SESSION, PROJECT_STATE, indice e MODEL_SPEC E18.31 allineati.
- Nessun nuovo commit/push, nessuna modifica ai tre agenti congelati o alla Foundation.

## Verifiche

55 test mirati pass (runtime E18.30, tre controller E18.31 e reporting).
Entrambi i report passano QA a 360, 736 e 1024 px in light/dark: 22 pannelli,
44 curve, 1.320 punti; nessun overflow o overlap; tooltip/legenda verificati.
Nel nuovo report FEED e CARE ispezionati anche visivamente.

Il file pubblicato resta SHA-256
`59dcf7b9fb380f60460a2b300fc9043fe6ce816be2c28004a82971420650ed63`.
Ricontrollati immutati anche E18.28 pubblicata e i tre controller V11.
`git diff --check` senza errori. Il working tree conserva lavoro precedente e
nuovi risultati non committati: pulizia non significa cancellare modifiche.

## Pulizia effettivamente eseguita

Rimossi 38 JSON pubblici usati soltanto per lo screening:
**1.234.785.677 byte**. Ogni path è stato risolto sotto `data/replays/json`,
verificato contro ID/nome file, dimensione e SHA-256 prima della rimozione.
Catalogo e documento di riferimento creati prima di eliminare i raw. Non sono
stati spostati nel cestino; sono recuperabili tramite URL Kaggle se ancora
disponibili. Tutte le sintesi di screening, anche negative, rimangono.

Conservati 11 JSON dello studio corrente, **337.536.587 byte**: sei nostri e
cinque del Top770-002, incluso il non-770. Cache esclusa da Git.

Rimosse anche cache rigenerabili Python/pytest: prima pulizia 211 file,
4.771.423 byte; dopo le verifiche 32 file, 555.100 byte ricreati dai test.
Nessuna rimozione di sorgenti, specifiche, risultati unici o freeze precedenti.

Riferimenti:
`E18_31_PUBLIC_TOP002_DIAGNOSTIC_20260906_IT.md`,
`E18_31_PUBLIC_REPLAY_REFERENCE_20260906_IT.md` e
`../artifacts/derived/E18_31_PUBLIC_REPLAY_RECOVERY_CATALOG_20260906.json`.

## Prossimo sviluppo

Stessa 770 e massimo 12 manovali. Priorità conservata: assegnazione e
espansione produttiva come scelta integrata, non una correzione dei PASS
separata dall'investimento. Le nuove evidenze suggeriscono prove interne su
capacità D5–D10, copertura CARE e scorta grano; verificare economia e safety,
non imporre le traiettorie del nuovo Top. Nessun riutilizzo dei due benchmark
consumati come verifica indipendente di future release. I nuovi replay della
submission continuano ad arrivare su Kaggle; nessuna automazione aggiunta.
