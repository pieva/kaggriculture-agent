# Acquisizione esterna programmata — 12 settembre 2026, ore 17:00 Europe/Rome

Richiesta esplicita: pubblicare 774, acquisire le misure dopo un'ora e confrontare dinamica della cassa e tutti i 22 KPI con i replay esterni 770/772/775. Pubblicazione eseguita verso le 15:01 locali; Kaggle Complete. Submission **56185961**. Ricevuta: `../../artifacts/PUBLICATION_RECEIPT.json`.

## Identità congelate

| Serie | Submission | Versione |
|---|---:|---|
| 770 | 56101593 | V48 esterna, stessa linea del confronto precedente |
| 772 | 56142698 | E20.1 loaderfix; NON E20.2 locale |
| 774 | 56185961 | E21 Repair2, packaging con ingresso Kaggle finale |
| 775 | 56147218 | E18.2 V4D, ripubblicazione invariata del 10 settembre |

Esiste anche una 770 V51 più recente nella lista Kaggle; non mescolarla a V48. Le righe identificate sopra sono la coorte primaria esplicitata al proprietario. Confrontare topologie e versioni distinte, non chiamarle genericamente strategie top.

Bundle pubblicato `submission/submission_codex_e21_774_repair2.py`, SHA256 `5af967e001e3576cae7ab3c26aa9f2d9e953ba2ba6b66441a8ca1287d0365674`. L'originale R2 resta invariato; aggiunto soltanto `kaggle_submission_agent` come ultimo callable. Kaggle `get_last_callable` verificato su 4 replay / 2876 azioni senza differenze. Non usare il bundle diagnostico grezzo per una nuova submission.

## Dati già disponibili

Acquisiti 20 episodi pubblici completati recenti per ciascuno dei riferimenti 770/772/775: 60 replay, tutti 720 stati/DONE e con farms/private/market/town/day/hour. 770: 20/20 finali 770. 772: 20/20 finali 772. 775: 19/20 finali 775 e uno 575; conservare l'anomalia, non escluderla per selezione favorevole. `INVENTORY.json` contiene ID, ruoli, metadati, topologia giornaliera, percorsi e hash; `BASELINE_INVENTORY.json` conserva il primo cutoff. Raw in `data/replays/json/e21_external_comparison/`.

`DATA_PREFLIGHT.json` verifica hash/campi dei 60 replay e il calcolo dei 22 KPI e della parità contabile su un episodio per ciascuna serie. Il controllo contabile integrale del corpus va completato nel rapporto programmato. I dati competitivi 774 devono essere acquisiti al richiamo: il 600 iniziale è soltanto validazione.

## Procedura del richiamo

1. Leggere ricevuta, inventario e questo handoff. Conservare il cutoff iniziale; nessun upload, modifica policy, simulazione o tuning.
2. Eseguire `.venv/Scripts/python.exe docs/model_specs/codex/e21/acquire_external_comparison.py --include774`. Selezione congelata: ultimi 20 episodi PUBLIC completati per esatta submission, ordine createTime/ID decrescente, team diversi; nessun filtro per risultato/topologia. La history completa scaricata mantiene anche esclusi e partite in corso. Se meno di 20 partite 774, analizzare tutte quelle disponibili e dichiarare n.
3. Per ogni replay completo usare `profile(replay, seat)` da `docs/model_specs/codex/e20/tools/analyze_first_external.py`; salva un derivato per episodio/ruolo con ledger, 22 KPI, terminale, starvation. Il motore memorizza alcuni campi condivisi solo nell'osservazione del ruolo 0; per replay di policy idratare `step`, senza inventare dati futuri. Non escludere errori contabili silenziosamente: riportarli e limitare le grandezze non verificabili.
4. `FIELDS` da `docs/model_specs/codex/e19/tools/build_assisted_complete_kpi.py` definisce i 22 KPI. Cassa finale e profilo D1–30, variazioni giornaliere, fasi D1–11/D12–19/D20–29/D30, mediana/intervallo e singoli replay. Contabilità: vendite/acquisti per prodotto, quantità e prezzi realizzati, manodopera, terra, stock terminali, domanda pubblica e avversario. Distinguere FEED/CARE/WATER riusciti dai richiesti. Per crop_tiles correggere l'etichetta storica in «Caselle coltivate».
5. Q0/Q1: riusare la logica di attribuzione delle caselle e azioni verificata in `build_trajectory_report.py`; i 21 KPI additivi devono riconciliarsi con i quattro quadranti, cassa globale non allocabile arbitrariamente. Non chiamare questa funzione direttamente sui metadati esterni: adattarne l'estrazione al replay pubblico e conservare gli ID.
6. Creare report HTML/Markdown, 22 pannelli leggibili, dati CSV/JSON e manifest. Mettere in evidenza numerosità, diversa distribuzione di avversari/seed, mercato e anomalie della topologia. Nessuna stima causale del solo pascolo da coorti diverse. Se mancano replay 774, produrre un resoconto della lacuna; se pochi, rapporto preliminare esplicito.
7. Aggiornare README E21 e NEW_SESSION con il risultato. Disattivare l'automazione `774-acquisizione-e-confronto-esterno-dopo-un-ora` dopo questo controllo, preservando tutti i suoi campi. Notificare completamento o problema concreto, non aggiornamenti invariati. Nessun commit/push autorizzato.

L'automazione è una heartbeat della stessa conversazione, impostata alle 17:00 locali. È giornaliera solo come meccanismo di pianificazione e deve essere messa PAUSED al completamento del singolo controllo richiesto.
