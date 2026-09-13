# Ripresa: evoluzione di E22

La prossima sessione analizza come far evolvere **E22**, campione pubblicato come submission **56206528**. La pulizia e il salvataggio Git sono autorizzati nella sessione del 13 settembre; non avviare nuove simulazioni o pubblicazioni sulla base delle vecchie istruzioni archiviate.

Leggere [PROJECT_STATE](PROJECT_STATE.md) e [specifica E22](model_specs/codex/e22/mod_specs.md). Bundle corrente: `submission/submission_codex_e22_s56165462_observed_v1.py`. La rinomina documentale conserva esattamente le 719 azioni pubblicate; hash originali e verifica sono nel registro di rilascio.

Il rating 2000 è stato raggiunto. Screenshot utente successivi mostrano 2232,2 (posizione 1126) e separatamente 2266 nel pannello Games: sono rilevazioni storiche, non uno score aggiornato. Preservare la baseline come controllo.

## Punto di partenza

Analizzare il replay **108559326**, contro submission **56204740**: sconfitta 71.697–75.080, piano simile ma non identico (533/719 gruppi lavoratori, 421/719 azioni complete). [Evidenza](model_specs/codex/e22/reports/shared_plan_108559326/REPORT.md). Individuare dove nasce il divario e distinguere fallimenti di esecuzione, decisioni produttive e differenze di mercato; la somiglianza finale non dimostra identità né paternità del piano.

Formulare poi una sola ipotesi di sviluppo alla volta: robustezza all'esecuzione/cassa, monetizzazione della chiusura, oppure diversificazione guidata dal valore atteso al raccolto e dal valore del grano come alimento. Non assumere già dimostrato un beneficio della rotazione. Nessun vincolo ereditato obbliga a una particolare topologia; ogni modifica va confrontata con E22 congelata.

## Variante strutturale da confrontare

Priorità aggiunta dall'utente: [episodio 108561064](https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56206528&episodeId=108561064). Osservazione visiva da verificare nei dati: molte varianti mantengono il pollaio in Q2 e sostituiscono i tre pollai in Q0 con pascoli. Identificare la submission avversaria, ricostruire coordinate e tempi di costruzione, specie effettivamente collocate, lavoro, alimentazione e ricavi sui 30 giorni. Confrontare con E22 e con l'episodio 108559326; distinguere variante del piano da azioni fallite. Non assumere un vantaggio economico dalla sola somiglianza visiva. Conservare la notazione Q0/Q2 dell'utente e verificarne la corrispondenza alle coordinate.

## Metodo e preferenze

- Una simulazione per volta sul laptop. Seed 180911301–307 già esposti; 180912401–407 riservati alla conferma.
- Report KPI con grafici sui 30 giorni e selettore degli incontri, non sole tabelle. Aprire l'HTML nel browser visibile quando consentito; non aggirare eventuali blocchi di policy.
- Identificare la provenienza esterna tramite ID submission: sorgente del piano **56165462**, episodio **108518933**. Azioni pubbliche ricostruite, non codice del competitor acquisito.
- E20.9fix è soltanto un controllo di regressione. Gli esperimenti E19 e l'analisi esterna estesa sono chiusi; non riprenderli senza una nuova motivazione.

La cronologia precedente è in [archivio](governance/history/session_snapshots/2026-09-13_e22_cleanup/EXPERIMENT_LOG.md); non costituisce istruzioni correnti.
