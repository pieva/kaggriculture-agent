# Checkpoint V51C — 9 settembre 2026

Stato salvato prima di commit e push sul ramo `codex/v51-benchmark-checkpoint`.

## Candidata e pubblicazione

V51C pubblicata: submission **56124996**, Complete, rating osservato **942,1**.
Bundle: `submission/submission_codex_e19_770_v51_candidate.py`.
SHA256: `43d5c6c3b70cf2940afaa83f3a243cba75e52f89db459d31ecb96187c4f13fda`.
V49F resta la baseline locale; V50 è un esperimento respinto. Le varianti
intermedie sono conservate come evidenza, non candidate da pubblicare.

## Risultati salvati

- Validazione locale V51C: sei casi di sviluppo, quattro di validazione,
  parità di 719 azioni e runtime standard nei due posti. Report congelato:
  `model_specs/codex/e19/reports/pass_reduction_v51/REPORT_V51_IT.html`.
- Audit esterno: 42 partite, 22 vittorie e 20 sconfitte, cassa media 79.977,83;
  PASS 33,18/giorno, quota 13,94%. Report:
  `model_specs/codex/e19/reports/v51_external_20260909/REPORT_V51_REPLAY_KPI_IT.html`.
- Benchmark: 15 replay distinti di tre nuovi leader. Top770-004 Himanshu Kumar,
  Top770-005 pensukesan, Top770-006 kanno. Corpus completi e sensibilità solo
  770 separati; confronto descrittivo, non appaiato. Sintesi e tre report da
  22 KPI: `model_specs/codex/e19/reports/top_v51_20260909/REPORT_TOP_V51_IT.html`.

La cassa V51C è riconciliata. Resta una discrepanza locale di 1 nella cassa
dell'avversario Scorpi, episodio 107183104, transizione 566, documentata.
Verificati dati, hash, collegamenti e payload dei grafici; rendering browser
non certificato, poiché la policy aveva bloccato l'apertura dei file locali.

## Punto di ripresa

La chiusura D29 è migliorata, ma D16–D25 resta il divario principale:
V51C PASS 27,08 e MOVE 154,18/giorno, contro circa 4–8 e 113 dei leader.
Più personale e spesa, meno WATER e CARE. Il divario permane nei soli 770,
pur con mix animale differente. Prossima attività da avviare: diagnosi dei
servizi e dei percorsi nella fase produttiva, prima di proporre una variante.
Non tagliare personale senza verificare carico e copertura biologica.

Nessuna nuova variante o submission è stata prodotta dopo questo benchmark.
Tutti i corpus aperti e i seed locali di validazione sono esposti: consultare
il registro comune prima di selezionare un nuovo controllo indipendente.

## Repository e riproduzione

Codice, test, bundle, risultati, profili derivati, CSV, grafici e manifest
sono conservati in Git. Replay pubblici riscaricabili in `data/replays/json`,
simulazioni complete in `scratch` e log di esecuzione restano locali e ignorati.
Non sono stati cancellati audit o esperimenti necessari alla provenienza.
Gli script di download e i protocolli nelle cartelle dei report identificano
gli input; la riproduzione locale completa richiede gli artefatti indicati
nei rispettivi `REPRODUCE_IT.md` e il motore congelato.

Controllo pre-commit: **27 test V49–V51 passati**. Pytest ha segnalato soltanto
l'impossibilità di aggiornare la propria cache locale.
