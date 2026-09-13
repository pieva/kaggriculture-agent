# Stato del progetto — 13 settembre 2026

**E22.1 — Pollai è il riferimento competitivo; E22.2 — Pascoli è pubblicata per verifica esterna.** Pubblicata e Complete, submission [56206528](https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56206528). La prossima fase è studiarne l'evoluzione mantenendo una baseline congelata.

Il rating 2000 è stato superato: evidenza iniziale 2024; screenshot successivi dell'utente mostrano 2232,2 con posizione 1126 e, separatamente, 2266 nel pannello Games. Non sono letture live né una stima stabilizzata.

## Implementazione e provenienza

[Bundle E22](../submission/submission_codex_e22_s56165462_observed_v1.py): piano temporale di 719 azioni, ricostruito dalle azioni pubbliche della submission **56165462**, episodio **108518933**. Usa giorno e ora; non adatta il piano al mercato o agli insuccessi osservati. La parità originale è stata verificata su 20 replay (14.380 azioni).

La pulizia sostituisce le etichette nominali con riferimenti numerici. Cambiano nome del file e docstring, non le azioni. L'hash della pubblicazione originale resta `7abb5c797a16b76c80c352578012641aa081fb004c994e6bd7a9c3810bc3712a`; non attribuirlo al file rinominato. [Registro e verifica](model_specs/codex/e22/reports/e22_release/CLEANUP_VERIFICATION.json).

## Evidenze utili

- Contro E20.9fix: 4/4 vittorie interne, margine medio +9.685. [Grafici](model_specs/codex/e22/reports/e22_vs_e209fix/REPORT.html).
- Ultimo confronto con due varianti interne scartate: E22 vince 8/8, senza fughe; il risparmio di lavoro da solo non spiega la superiorità. Dettagli conservati nell'archivio degli esperimenti, nessuna variante promossa.
- Replay **108559326**, avversario **56204740**: E22 perde 71.697–75.080. Coincidono 533/719 gruppi di azioni lavoratori e 421/719 azioni complete. [Analisi iniziale](model_specs/codex/e22/reports/shared_plan_108559326/REPORT.md). L'episodio aggiorna il rating di E22 da 2251,15 a 2229,93; non è necessariamente l'ultimo rating della submission.

## Evoluzione Q0 e pubblicazione E22.2

E22.2 (originale 8C9S v1) sostituisce i tre pollai Q0 con tre pascoli di pecore: totale 8 mucche e 9 pecore. Submission [56212495](https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56212495), stato **Complete**; score iniziale osservato 600,0, non stabilizzato. [Registro versioni](model_specs/codex/e22/VERSIONS.json).

14 partite locali contro E22.1: 4/14 vittorie, media +353,14, mediana −2.092, su sette seed esposti nei due ruoli. La pubblicazione è diagnostica, autorizzata dall’utente dopo revisione; non è una promozione per superiorità interna. File invariato e verificato su 10.066 azioni; zero fughe/errori contabili, latte e lana raccolti interamente venduti. [Report](model_specs/codex/e22/reports/e22_2_vs_e22_1/REPORT.html) · [Revisione e pubblicazione](model_specs/codex/e22/reports/e22_2_release/REVIEW.md).

Il calendario ricorrente nei sei replay esterni è stato implementato come v2, ma è risultato peggiore della v1 di 222,57 di margine medio. Rimane esperimento interno distinto. Seed 180912401–407 non usati. Prossimo obiettivo da concordare: analisi esterna di E22.2.

[NEW_SESSION](NEW_SESSION.md) contiene la ripresa corrente; [EXPERIMENT_LOG](EXPERIMENT_LOG.md) conserva l’indice storico. Replay grezzi locali conservati con hash nel [manifest E22.2](model_specs/codex/e22/reports/e22_2_release/LOCAL_ARTIFACTS.json); report e strumenti restano versionati.
