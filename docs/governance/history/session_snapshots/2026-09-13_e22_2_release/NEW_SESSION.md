# Ripresa: E22 Q0 — sviluppo e traiettorie conclusi il 13 settembre

## Ultimo mandato: verifica e pubblicazione E22.2

Revisione passata su 10.066 azioni nei 14 replay con caricatore Kaggle reale: zero divergenze, mutazioni delle osservazioni, fughe o errori contabili. Bundle invariato. Restano singoli giorni senza alimentazione e due fertilizzanti trasportati a fine partita; nessun residuo di latte/lana raccolti. [Revisione](model_specs/codex/e22/reports/e22_2_release/REVIEW.md).

Pubblicazione autorizzata esplicitamente dall’utente ed eseguita il 13 settembre 2026: Kaggle mostra il file `submission_codex_e22_2_pascoli.py` con hash corretto e stato **Pending**. [Registro pubblicazione](model_specs/codex/e22/reports/e22_2_release/PUBLICATION.json). Nessun rating esterno ancora disponibile. Le indicazioni storiche di mancata pubblicazione sotto sono superate da questo mandato; nessun nuovo invio autorizzato automaticamente.

## Nomi correnti scelti dall'utente

- **E22.1 — Pollai**: versione pubblicata, submission **56206528**; tre oche nei tre pollai Q0, mix totale 8C6S3G. Bundle mnemonico `submission/submission_codex_e22_1_pollai.py`.
- **E22.2 — Pascoli**: precedente **8C9S v1**, variante scelta per i tre pascoli Q0, inviata a Kaggle per verifica esterna il 13 settembre; una pecora in ciascuna casella (4,1), (3,2), (2,3), mix totale 8C9S. Bundle mnemonico `submission/submission_codex_e22_2_pascoli.py`. **Non è la variante con calendario esterno v2.**

I bundle mnemonici sono copie a byte invariati; i percorsi storici restano validi per gli strumenti già creati. [Registro degli hash](model_specs/codex/e22/VERSIONS.json). [Report corrente E22.2 contro E22.1](model_specs/codex/e22/reports/e22_2_vs_e22_1/REPORT.html): 14 partite seriali esistenti riutilizzate dopo verifica dell'identità, senza nuove simulazioni. E22.1 vince 10/14, E22.2 4/14; cassa media 92.631,86 contro 92.985,00, margine medio E22.2 +353,14 e mediana −2.092. I due ruoli danno lo stesso esito per seed: sette seed, non quattordici osservazioni indipendenti. E22.1 rimane il riferimento di confronto; E22.2 inviata a Kaggle su richiesta esplicita successiva, seed di conferma ancora intatti.

## Ultimo mandato concluso: applicazione del calendario esterno

L'utente ha chiesto di utilizzare il calendario ricorrente nei sei replay. Implementata **8C9S calendario v2**: (3,2) D11 H20, (4,1) D11 H21, (2,3) D12 H7; raccolte D17/20/23/26/29 per le prime due, D18/21/24/27/30 per la terza. Il percorso D12 è adattato senza nuove assunzioni, anticipando l'acquisto della pecora a H1 e affidandola all'operaio 1; latte consegnato H11. [Specifica v2](model_specs/codex/e22/q0_calendar_v2_specs.md).

Tutte le 14 partite seriali su 180911301–307 nei due ruoli rispettano i collocamenti e i cinque giorni di raccolta per casella. Zero fughe/errori contabili; 8C9S sempre. Rispetto alla v1 sono invariati quantitativi piantati/raccolti/acquistati e assunzioni giornaliere. Risultato contro E22: 4/14 vittorie, media **+130,57**, mediana **−2.324**; delta margine vs v1 **−222,57**, peggiore su tutti i sette seed (entrambi i ruoli). Delta medio della sola cassa del candidato −149,29; il resto del delta margine è la risposta del controllo nel mercato condiviso. Confronto tramite partite contro lo stesso E22, non incontro diretto v1-v2.

**Decisione: calendario implementato e conservato come variante interna, non promuovere v2.** La ricorrenza non dimostra ottimalità nel nostro 8C9S; nessun guadagno produttivo, differenze nei tempi di consegna/vendita. E22 e v1 invariate, nessuna pubblicazione; 180912401–407 ancora riservati. [Dashboard v2 aperta e verificata](model_specs/codex/e22/reports/q0_8c9s_calendar_v2/REPORT.html), [verifiche](model_specs/codex/e22/reports/q0_8c9s_calendar_v2/VERIFICATION.json).

## Braccio precedente e analisi esterna

Questa sezione aggiorna e supera le piste operative più sotto, conservate come contesto. Nella worktree è stata sviluppata e testata **8C9S v1** senza modificare E22 pubblicata **56206528**. [Specifica](model_specs/codex/e22/q0_8c9s_specs.md). [Report KPI 30 giorni](model_specs/codex/e22/reports/q0_8c9s_v1/REPORT.html).

14 partite seriali sui seed esposti 180911301–307, due ruoli: 4/14 vittorie, +353,14 medio, −2.092 mediano, zero fughe e zero errori contabili. Mix sempre 8C9S, +64 lane e −78 uova rispetto a E22. **Non promuovere v1:** vantaggio su soli due seed di sette, cinque negativi; riservati e non usati 180912401–407. Nessuna pubblicazione Kaggle, nessun braccio 6C10S implementato. Il bundle v1 modifica anche le quantità massime SELL WOOL prima di D11; non è un confronto della sola struttura.

Richiesta aggiuntiva dell'utente conclusa: [tipologie e traiettorie dei pascoli esterni](model_specs/codex/e22/reports/external_pasture_trajectories/REPORT.html). Censimento dei 20 replay disponibili, estrazione dettagliata dei sei con tre pascoli Q0. Tutti costruiscono (2,3) D11 H15 e lo popolano con pecora D12 H7; raccolte D18/21/24/27/30. Pecore collocate D11 in (3,2) e, quando presente, (4,1): raccolte D17/20/23/26/29. Le submission 56165125 e 56205921 condividono 186 richieste/esiti di servizio Q0, lasciano (4,1) vuoto, ma differiscono nel piano globale. 56171606 chiude 6C10S dopo una fuga in (5,2): non confondere i mix finali con lo stesso piano. [Template osservato](model_specs/codex/e22/reports/external_pasture_trajectories/OBSERVED_TEMPLATE.json). Percorsi completi degli operai e calendari per casella nei JSON/CSV del report.

Fonti lette senza modificarle: `C:/Users/pietr/Projects/kaggriculture-agent/docs/NEW_SESSION.md`, report `external_e22_20260913` e relativi replay del checkout originale. Tutti i nuovi file appartengono alla worktree. Le dashboard sono state aperte e verificate nel browser tramite server locale, nessuna azione Kaggle.

## Contesto precedente

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
