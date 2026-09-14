# Registro esperimenti

> Handoff 2026-09-14: stato operativo in `docs/NEW_SESSION.md`. Report finale: http://127.0.0.1:8771/tournament5_v1/REPORT.html . Prossimo mandato: indicatori osservabili per colmare il gap con i top, usando i dati salvati; budget da concordare prima di nuove simulazioni. Checkpoint analitico verificato in `docs/model_specs/codex/e23/ANALYSIS_CHECKPOINT.zip`.


## 14 settembre 2026 — Chiusura torneo E23/E22 a cinque

Completati 140 incontri: dieci abbinamenti × sette semi esposti × due posti, 56 partite per versione. Vittorie: E22.1 8C6S3G 40; E23.1 9C5S3G 34; E22.2 8C9S 30; E23.3 7C10S 24; E23.2 6C11S 12. Nessun pareggio. 7C10S vs 6C11S 12–2, +1.432,43 monete medie; contro E22.2 4–10, −916 medie. E23.1 contro E22.1 4–10, −982,71 medie; E23.2 contro E22.2 2–12, −2.244,29 medie. Nessuna candidata promossa o pubblicata.

Verificati 280 lati, tutti con mix atteso e Q2 Grano raccolto; zero fughe, errori di cassa e differenze di ricompensa nei 70 controlli di posto invertito. Sei collaudi separati e 4.314 azioni E23 verificate; 12 incontri riutilizzati dall'avvio a quattro. Archivi e hash registrati. Una simulazione alla volta; dopo 56 risultati ottimizzato solo il salvataggio JSON/gzip, con contenuto JSON identico e policy/engine invariati. Semi riservati non usati. [Report e dati](model_specs/codex/e23/reports/tournament5_v1/REPORT.html).

## 14 settembre 2026 — Estensione a cinque partecipanti

Su richiesta dell'utente, E23.3 **7C10S** completa il percorso 8C9S → 7C10S → 6C11S. Cambia solo (6,4); (5,2) resta mucca. Stesso executor e adattamento vendite della 6C11S. Due collaudi vs E22.2, seed 180911301, posti invertiti: +147 monete entrambi, mix atteso, nessuna fuga. 1.438 azioni riprodotte, nessuna mutazione. Questi sono collaudi, non prova di superiorità.

[Torneo a cinque](model_specs/codex/e23/reports/tournament5_v1/REPORT.html): 140 incontri, 10 coppie × 7 semi × 2 posti. I quattro file precedenti sono invariati; 12 risultati ufficiali già completati vengono riutilizzati con provenienza e hash. Torneo a quattro interrotto per l'estensione, senza cancellare risultati.

## 14 settembre 2026 — E23, due evoluzioni e torneo a quattro

E23.1: 8C6S3G → 9C5S3G in (6,2). E23.2: 8C9S → 6C11S in (6,4) e (5,2). Conservati percorsi e colture delle ultime E22 Q2 Grano; adattati servizi e vendite, condiviso executor riparato E22.2. Quattro collaudi: mix attesi, 11 manovali finali, zero fughe, contabilità riconciliata, 2.876 azioni E23 conformi e senza mutazioni. Sul primo seme entrambe perdono contro il parent; nessuna selezione o modifica dopo il congelamento.

[Torneo ufficiale](model_specs/codex/e23/reports/tournament4_v1/REPORT.html): 84 incontri, 6 abbinamenti, 7 semi esposti, entrambi i posti. Risultati e hash salvati per incontro; tutti i risultati inclusi. Le E23 restano locali. I semi riservati non partecipano.

## 13 settembre 2026 — Consolidamento E22

E22, submission **56206528**, è il campione pubblicato e ha superato rating 2000. Riferimento pubblico del piano: submission **56165462**, episodio **108518933**. La pulizia modifica etichette e documentazione, con parità verificata delle 719 azioni. Nessuna modifica strategica o nuova pubblicazione.

Gli esperimenti sulla linea E19 non sono promossi e sono chiusi. I relativi bundle sperimentali sono raccolti in `submission/archive/e19_rejected/`; sorgenti e risultati sintetici restano come evidenza storica. E20.9fix rimane soltanto un controllo. La prossima sessione riguarda l'evoluzione di E22.

- [Cronologia completa precedente](governance/history/session_snapshots/2026-09-13_e22_cleanup/EXPERIMENT_LOG.md).
- [Rilascio E22](model_specs/codex/e22/reports/e22_release/PUBLICATION.json).
- [Parità dopo pulizia](model_specs/codex/e22/reports/e22_release/CLEANUP_VERIFICATION.json).
- [Confronto con E20.9fix](model_specs/codex/e22/reports/e22_vs_e209fix/REPORT.html).
- [Ultimo confronto interno archiviato](model_specs/codex/e19/e19_2/reports/triangle_v52c/SUMMARY.json).
- [Replay 108559326, confronto iniziale](model_specs/codex/e22/reports/shared_plan_108559326/REPORT.md).

Le etichette nominali del riferimento esterno sono sostituite con ID numerici. I contenuti grezzi locali conservano i byte originali; gli hash storici si riferiscono agli originali, non alle copie documentali con etichette aggiornate. [Manifest degli artefatti locali](governance/history/LOCAL_ARTIFACTS_20260913.json).

## Audit esterno E22 e ipotesi Q0

Completati 20 audit sui 78 incontri pubblici congelati: 40 lati senza errori di cassa e 14.380 azioni E22 identiche. [Report](model_specs/codex/e22/reports/external_e22_20260913/REPORT.html). Richiesta nuova attività per la variante pascoli Q0; nessuna modifica alla baseline né pubblicazione in questo audit.
