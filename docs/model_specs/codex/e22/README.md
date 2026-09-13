# E22 — versioni e risultati

- [Versioni e hash](VERSIONS.json): E22.1 Pollai e E22.2 Pascoli.
- [Confronto selezionato](reports/e22_2_vs_e22_1/REPORT.html), [sintesi Markdown](reports/e22_2_vs_e22_1/REPORT.md).
- [Revisione](reports/e22_2_release/REVIEW.md) e [pubblicazione](reports/e22_2_release/PUBLICATION.json).
- [Traiettorie esterne](reports/external_pasture_trajectories/REPORT.html).
- [Calendario v2 non selezionato](reports/q0_8c9s_calendar_v2/REPORT.html).

I percorsi storici 8C9S v1 restano validi per i generatori. I bundle mnemonici sono copie a byte invariati. I report storici conservano lo stato al momento della loro creazione; lo stato corrente è nel registro VERSIONS.json.

## Riproduzione

Dalla radice del repository, usare Python con le dipendenze del progetto. `tools/report_q0_pastures.py`, `tools/report_q0_calendar_v2.py` e `tools/report_e22_2_vs_e22_1.py` rigenerano i rispettivi report dai risultati conservati. I report HTML sono consultabili senza server e includono i grafici.

`tools/prepublish_e22_2.py` rilegge i 14 replay v1 locali, non simula nuove partite. I replay compressi esclusi da Git sono elencati con hash in `reports/e22_2_release/LOCAL_ARTIFACTS.json`; conservarli per la verifica esatta. I JSON dei risultati per partita restano versionati. I simulatori `compare_q0_pastures.py` e `compare_q0_calendar_v2.py` richiedono un mandato separato prima dell’esecuzione; i seed di conferma non sono stati usati.

Per l’estrazione esterna, `tools/analyze_external_pastures.py` legge il percorso originale configurato nella variabile ORIGINAL; richiede i replay/profili esterni locali del 13 settembre. I dettagli derivati dei sei replay sono già inclusi nei report. Nessuna cache o credenziale Kaggle è necessaria per leggere i risultati versionati.
