# Stato del progetto — 14 settembre 2026

> Handoff 2026-09-14: stato operativo in `docs/NEW_SESSION.md`. Report finale: http://127.0.0.1:8771/tournament5_v1/REPORT.html . Prossimo mandato: indicatori osservabili per colmare il gap con i top, usando i dati salvati; budget da concordare prima di nuove simulazioni. Checkpoint analitico verificato in `docs/model_specs/codex/e23/ANALYSIS_CHECKPOINT.zip`.


## Aggiornamento E23

**Torneo a cinque completato e verificato (140 incontri).** Classifica per vittorie su 56: E22.1 40, E23.1 34, E22.2 30, E23.3 24, E23.2 12. La 7C10S è migliore della 6C11S nel loro confronto (12–2), ma non migliora E22.2 (4–10). Nessuna E23 promossa; tutte restano bundle locali congelati. Zero fughe e discrepanze contabili su 280 lati, mix e Q2 Grano corretti ovunque. [Esiti finali](model_specs/codex/e23/reports/tournament5_v1/REPORT.html).

Esteso su richiesta a **tre E23 e torneo a cinque**: aggiunta E23.3 7C10S (pecora al posto della mucca in (6,4)). Due collaudi superati, 1.438 azioni aggiuntive verificate. [Torneo corrente da 140 incontri](model_specs/codex/e23/reports/tournament5_v1/REPORT.html); riutilizzati i 12 risultati completi del precedente torneo.

Sviluppate due candidate locali: E23.1 9C5S3G ed E23.2 6C11S. [Stato, bundle e torneo a quattro](model_specs/codex/e23/README.md). Controlli attuali E22.1 Q2 Grano 56228842 ed E22.2 fix Q2 Grano 56231638. Quattro collaudi verificati, torneo seriale da 84 incontri; conteggio effettivo nel report. Nessuna nuova pubblicazione. Il seguito conserva lo stato storico del 13 settembre.

**E22 è il campione corrente.** Pubblicata e Complete, submission [56206528](https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56206528). La prossima fase è studiarne l'evoluzione mantenendo una baseline congelata.

Il rating 2000 è stato superato: evidenza iniziale 2024; screenshot successivi dell'utente mostrano 2232,2 con posizione 1126 e, separatamente, 2266 nel pannello Games. Non sono letture live né una stima stabilizzata.

## Implementazione e provenienza

[Bundle E22](../submission/submission_codex_e22_s56165462_observed_v1.py): piano temporale di 719 azioni, ricostruito dalle azioni pubbliche della submission **56165462**, episodio **108518933**. Usa giorno e ora; non adatta il piano al mercato o agli insuccessi osservati. La parità originale è stata verificata su 20 replay (14.380 azioni).

La pulizia sostituisce le etichette nominali con riferimenti numerici. Cambiano nome del file e docstring, non le azioni. L'hash della pubblicazione originale resta `7abb5c797a16b76c80c352578012641aa081fb004c994e6bd7a9c3810bc3712a`; non attribuirlo al file rinominato. [Registro e verifica](model_specs/codex/e22/reports/e22_release/CLEANUP_VERIFICATION.json).

## Evidenze utili

- Contro E20.9fix: 4/4 vittorie interne, margine medio +9.685. [Grafici](model_specs/codex/e22/reports/e22_vs_e209fix/REPORT.html).
- Ultimo confronto con due varianti interne scartate: E22 vince 8/8, senza fughe; il risparmio di lavoro da solo non spiega la superiorità. Dettagli conservati nell'archivio degli esperimenti, nessuna variante promossa.
- Replay **108559326**, avversario **56204740**: E22 perde 71.697–75.080. Coincidono 533/719 gruppi di azioni lavoratori e 421/719 azioni complete. [Analisi iniziale](model_specs/codex/e22/reports/shared_plan_108559326/REPORT.md). L'episodio aggiorna il rating di E22 da 2251,15 a 2229,93; non è necessariamente l'ultimo rating della submission.

## Direzione e organizzazione

Studiare anche la variante segnalata nell’episodio 108561064 (pollaio Q2 conservato, tre pollai Q0 sostituiti da pascoli: osservazione utente da verificare). Studiare dapprima l'origine del divario nel replay, poi progettare modifiche isolate e verificabili a E22. Le ipotesi su reattività, diversificazione, autoconsumo e chiusura rimangono da validare; nessuna nuova variante implementata con questa pulizia.

[NEW_SESSION](NEW_SESSION.md) contiene la ripresa; [specifica E22](model_specs/codex/e22/mod_specs.md) descrive la baseline; [EXPERIMENT_LOG](EXPERIMENT_LOG.md) è l'indice storico. Le istruzioni dei rami scartati sono archiviate, non priorità operative. Replay grezzi, copie ridondanti e report pesanti restano locali con [manifest](governance/history/LOCAL_ARTIFACTS_20260913.json); non sono inclusi nel clone Git.

## Analisi E22 conclusa e sviluppo Q0 autorizzato

78 partite congelate, 46 vittorie e 32 sconfitte; audit 20 replay / 40 lati senza discrepanze. [Report](model_specs/codex/e22/reports/external_e22_20260913/REPORT.html). Quattro casi con pascoli sulle tre coordinate Q0, tutti vincenti contro E22 nel campione selezionato. Caso guida 108561064, submission 56165125: 6C10S contro 8C6S3G, +8.990 monete soprattutto dalla lana. Non è un confronto isolato di topologia. L’utente ha autorizzato una nuova attività dedicata: [New Session](NEW_SESSION.md) specifica un primo braccio 8C9S e distingue la replica 6C10S.
