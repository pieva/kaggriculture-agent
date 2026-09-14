# New Session — E23, torneo a cinque completato

## Aggiornamento 14 settembre 2026 — riferimento corrente

**Torneo concluso: 140/140.** [Report finale](model_specs/codex/e23/reports/tournament5_v1/REPORT.html). Vittorie su 56: E22.1 8C6S3G 40; E23.1 9C5S3G 34; E22.2 8C9S 30; E23.3 7C10S 24; E23.2 6C11S 12. Nessun pareggio. 7C10S supera 6C11S 12–2, ma perde contro E22.2 4–10. Nessuna E23 promossa o pubblicata. Tutti i 280 lati hanno mix corretto, zero fughe e contabilità riconciliata; Q2 Grano raccolto ovunque. I processi del torneo e dell'aggiornamento report sono terminati; non riavviare gli incontri già completi. [Implementazione e limiti](model_specs/codex/e23/IMPLEMENTATION.md). Le note di avvio seguenti sono storiche.

**Ultimo mandato: torneo a cinque.** Aggiunta E23.3 7C10S alle due E23 e due E22, cambiando solo la mucca (6,4) in pecora. [Report corrente](model_specs/codex/e23/reports/tournament5_v1/REPORT.html), 140 incontri pianificati e 12 già completati riutilizzati dal torneo a quattro. Runner `docs/model_specs/codex/e23/tools/run_tournament4.py --five`; per il report `docs/model_specs/codex/e23/tools/report_tournament4.py --five`. La parte seguente che indica 84 incontri precede l'estensione dell'utente.

Ripartire dal [README E23](model_specs/codex/e23/README.md) e dal [torneo E22/E23](model_specs/codex/e23/reports/tournament4_v1/REPORT.html). Ramo `codex/e23-evolution-tournament`, checkout `C:/Users/pietr/Projects/kaggriculture-agent`. E23.1 9C5S3G ed E23.2 6C11S implementate e congelate dopo quattro collaudi; 84 incontri ufficiali pianificati, eseguiti uno alla volta. Conteggio aggiornato nel report e nei file `matches/E*.json`; runner riprendibile `docs/model_specs/codex/e23/tools/run_tournament4.py`.

Le baseline correnti sono **E22.1 Q2 Grano 56228842** e **E22.2 fix Q2 Grano 56231638**, importate byte-identiche dalla worktree `C:/Users/pietr/.codex/worktrees/756c/kaggriculture-agent`. Il pollaio Q2 è già sostituito con grano. La documentazione E22 aggiornata è nella suddetta worktree. Nessuna E23 pubblicata; semi 180911301–307 esposti, 180912401–407 riservati e inutilizzati. I paragrafi seguenti descrivono la precedente ripresa E22 e sono storici.

## Mandato corrente

L'utente autorizza una nuova attività dedicata a sviluppare E22 sostituendo i tre pollai in Q0 con pascoli. Preservare E22 pubblicata, submission **56206528**, come controllo. Produrre una variante interna, verificarne esecuzione e confronto economico prima di proporre un test esterno.

## Analisi conclusa

[Report E22, grafici sui 30 giorni](model_specs/codex/e22/reports/external_e22_20260913/REPORT.html). Storico congelato di 78 partite: 46 vittorie, 32 sconfitte; massimo rating osservato 2279,59, rating dopo l'ultimo episodio congelato 2223,85. Audit di 20 replay selezionati: 16 posizioni temporali equidistanti più casi segnalati ed estremi; campione diagnostico, non casuale. Quaranta lati verificati contabilmente senza discrepanze, 14.380 azioni E22 tutte conformi alla baseline.

Quattro avversari del campione mostrano tre pascoli Q0 e pollaio Q2: E22 perde tutti e quattro, ma questa selezione non prova causalmente la superiorità dei pascoli. Riferimenti numerici e dettagli in FAMILIES.json e SUMMARY.json nella directory del report.

## Caso guida e differenze da isolare

Episodio **108561064**, avversario **56165125**: 130.059 contro 121.069 di E22. Tre coordinate zero-based: **(4,1), (3,2), (2,3)**; Q0 significa x<5,y<5. Pollaio Q2 **(3,7)**, costruito D29 H5 e senza animale.

Avversario finale **6 mucche e 10 pecore**, E22 **8 mucche, 6 pecore e 3 oche**. Il pascolo (4,1) resta vuoto, senza fuga. Pecore in (3,2) a D11 H20 e (2,3) a D12 H7. Le differenze interessano anche il mix sulle coordinate preesistenti e la pianificazione, non solo tre tipi di struttura.

Vantaggio avversario: lana +16.393; uova −4.366; latte −1.303; altri ricavi −2.509; acquisti +2.118; lavoro −1.343; totale +8.990. Acquisti grano: 3.621 contro 5.269, senza attribuire il delta al solo autoconsumo.

## Sviluppo e verifica

1. Leggere il bundle E22 `submission/submission_codex_e22_s56165462_observed_v1.py` e la specifica `docs/model_specs/codex/e22/mod_specs.md`. Provenienza del piano: submission 56165462, episodio 108518933. Non usare nomi di competitor.
2. Costruire un primo braccio che isoli i tre pascoli Q0: mantenere le 8 mucche e le 6 pecore di E22, aggiungere fino a 3 pecore al posto delle oche, rivedendo acquisti, alimentazione, cure, raccolte e vendite pertinenti. Verificare accessibilità, cassa e finestre produttive; non limitarsi a sostituire BUILD_COOP con BUILD_PASTURE.
3. Tenere distinto un eventuale secondo braccio che riproduca il mix 6C10S del caso guida. Non riempire automaticamente il pascolo vuoto e attribuire poi il risultato alla replica osservata.
4. Verificare il caricatore reale, l'assenza di fughe, l'esecuzione delle nuove strutture e la chiusura. Confrontare con E22 su seed accoppiati, entrambi i ruoli, una simulazione alla volta. Seed 180911301–307 già esposti; 180912401–407 riservati alla conferma.
5. Report KPI D1–D30: margine, lavoro, grano comprato e raccolto, produzione e vendite latte/lana/uova, prezzi realizzati, animali effettivi e rimanenze. Aprire l'HTML nel browser quando consentito; non aggirare blocchi di accesso UI.

## Dati e ambiente

I file nuovi del report sono nel checkout originale `C:/Users/pietr/Projects/kaggriculture-agent/docs/model_specs/codex/e22/reports/external_e22_20260913/`. In una nuova worktree leggerli da quel percorso, perché non ancora committati. Replay locali in `C:/Users/pietr/Projects/kaggriculture-agent/data/replays/json/e22_external_20260913/`. Python disponibile nel checkout originale: `.venv/Scripts/python.exe`. Non modificare i file del checkout originale dalla nuova attività; sviluppare nella propria worktree.

E19 è archiviata; E20.9fix è solo un riferimento. Non riprendere le vecchie piste. Nessuna nuova submission Kaggle è stata autorizzata con questa richiesta di sviluppo.
