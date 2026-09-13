# Stato del progetto — 13 settembre 2026

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
