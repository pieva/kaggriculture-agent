# Checkpoint E18 — stato, pulizia e ripartenza anti-PASS

Data: 2026-09-05. Richiesta del proprietario: salvare lo stato, pulire il
repository, allineare Git e ripartire immediatamente con il nuovo assegnatore.

## Stato salvato

`docs/NEW_SESSION.md` e `docs/PROJECT_STATE.md` sono gli ingressi operativi;
la cronologia precedente è preservata in `docs/history/`, senza blocchi CURRENT
contraddittori nell'handoff attivo. Indici Codex, README E18 e manifest comune
allineati a 770, E18.28 C pubblicata, E18.29 B3 non promossa ed E18.30 nuova
linea di sviluppo. Strategie specifiche restano nel namespace Codex/E18.
Specifiche E17/E18 ricollocate nelle directory evento, con riferimenti aggiornati.

Diagnosi congelata: 30 replay E18.28, 17 sconfitte e 13 vittorie; 21.570
batch shadow identici, 29/30 ledger verificati. Conservati dataset, eccezione
di audit monetario, risultati negativi, piani, fonti e report V3. Nessuna
promozione o modifica al file E18.28 pubblicato. Non risolto il tema mucche.

## Pulizia effettiva

- Eliminati esattamente 22 raw nella cache repository, 675.043.617 byte
  (643,77 MiB), alle 20:01:48 UTC, dopo verifica SHA-256, dimensioni e confine
  di ogni percorso. Nessuna cancellazione ricorsiva; tutti recuperabili
  tramite il catalogo comune `E18_REPLAY_DOWNLOAD_CATALOG_20260905.json`.
- Eliminati i soli quattro HTML QA E18_28_360/736_light/dark; conservati
  generatore, report finale e QA E18.29. Rigenerabili, non evidenza unica.
- Cache replay in sottodirectory ora ignorate da Git come quelle nella radice.
- I 30 raw E18.28 in Downloads sono fuori dal repository e restano disponibili;
  percorsi, hash e URL nel manifest della diagnosi V2. Nessuna pulizia generica
  della directory Downloads. I derivati preliminari restano etichettati non validi
  per l'analisi; i risultati pubblicati usano esclusivamente V2.

Il monitor dei primi replay `e18-28-primi-replay-e-allineamento` è PAUSED:
la soglia di tre replay è superata e il closeout viene completato qui.

## Verifiche

Suite `tests`, `docs/model_specs/codex/e18/tests`, `experiments/e18/tests`:
**327 passed in 273,86 s**, eseguita dopo la rimozione delle cache.
`compileall` sui tool/test E18 e modulo E18.17: pass. Tutti i nuovi JSON
parsabili; scansione mirata di nomi sensibili e pattern token/chiavi private
senza riscontri. `git diff --check` pulito. SHA-256 E18.28 pubblicata verificato
immutato. Dopo fetch, HEAD e origin/main coincidevano su 1a1e523, senza divergenza.
Le modifiche accumulate sono specifiche/report/tool/test E18, migrazioni di
namespace e relativi indici: nessun cambiamento estraneo incluso intenzionalmente.
Eccezioni `.gitattributes` preservano i byte dei freeze E18 (derivati/config,
analizzatore con hash registrato e submission pubblicata): la normalizzazione
CRLF/LF altererebbe gli SHA-256 di provenienza. Il codice ordinario resta LF.
Commit/push del checkpoint precedono l'implementazione del nucleo E18.30.
Nessun upload nuovo e nessun holdout consumato.

## Ripartenza

E18.30 è una riprogettazione per missioni, non un riempitivo dei PASS.
Prima tranche: ledger/assegnatore puro, lavoratori reali, recupero orfani,
prerequisiti, claim, deadline e acknowledgement. Adattatore runtime e verifica
economica end-to-end sono gate successivi: non dichiarare risolto il difetto
per il solo superamento dei test del nucleo.
