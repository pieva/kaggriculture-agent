# E21 774 — passaggio alla nuova chat

Stato salvato il 12 settembre 2026. L'utente aprirà personalmente una nuova chat. Questa sessione non implementa E21, non crea task, non esegue submission, commit o push.

## Richiesta accettata

Studiare una E21 con topologia pascoli **7-7-4**, partendo dalla E18 vincente **7-7-5**. Prima ristudiare il vecchio tentativo 774 e confrontarne la strategia con la nuova impostazione: pianificazione biologica, obbligazioni di servizio, missioni complete, risorse prenotate e contabilità economica. E21 nasce come esperimento diagnostico; non è obbligata a battere E18 per produrre conoscenza utile.

Domanda: il pascolo marginale genera valore oppure la sua rimozione rompe l'organizzazione del lavoro ereditata? Non assumere che PASS, FEED, CARE o il numero di animali siano singolarmente la causa del risultato economico.

## Base e provenienza

- Base immutabile: `submission/submission_codex_e18_2_capacity_governed_v4d.py`.
- SHA256: `c5fb1fc4966b81f238cdd0de4ca5e15b16ea6b8ae077a08ecc881f8729fd01f7`.
- La 775 non è stata trovata ottimizzando i 22 KPI: deriva dalla routine del competitor keiz, replay pubblico 104498819, distillata nella Codex V9, corretta sul FEED D8, poi evoluta in E17 V4D e E18.2. Le revisioni hanno migliorato logistica e recupero sul posto conservando la geometria.
- Fonti: `docs/governance/history/model_spec_c2/codex/CODEX_V9_0_FINAL_REPORT_IT.md`; `docs/model_specs/codex/e17/reports/E17_CODEX_BATCHED_CLUSTER_ROUTING_V4_DEVELOPMENT_REPORT_IT.md`; `docs/model_specs/codex/e18/reports/E18_2_CAPACITY_GOVERNED_V4D_DEV_REPORT_IT.md`.
- Quindi l'evidenza riguarda il pacchetto geometria + routine + correzioni, non l'ottimalità generale della 775. Molte ottimizzazioni storiche chiamate E18 erano sulla 770, non sulla 775 vincente.

## Prima attività: archeologia del vecchio 774

Il report E18.2 documenta una 774 con recupero di un pascolo Q2, interrotta dopo pochi match con regressioni fino a circa 60k. La spec menziona circa 35–60k. Non trattare questi estremi come una media, una suite completa o un risultato riprodotto adesso.

Punti di accesso reali nel repository (alcuni vecchi report contengono percorsi precedenti al riordino):

- `src/agricola/strategy/codex/codex_e18_capacity_governed_v4d.py`: reclaim sperimentale, validazione target `(4,7)`, disabilitato nella configurazione congelata; esiste rollback a DENSE_V4D se non riesce a finanziare il lavoro.
- `docs/model_specs/codex/e18/configs/CODEX_E18_2_CAPACITY_GOVERNED_V4D_V1.json`.
- `docs/model_specs/codex/e18/MODEL_SPEC_CODEX_E18_2_CAPACITY_GOVERNED_V4D_V1.md`.
- `docs/model_specs/codex/e18/tools/run_e18_2_capacity_governed_v4d_gate.py`.
- `docs/model_specs/codex/e18/artifacts/derived/E18_2_CAPACITY_GOVERNED_V4D_DEV_GATE_V1.json`: gate della candidata finale; non assumere che contenga anche i bracci 774 abortiti.

Recuperare con ricerca e storia Git la configurazione effettivamente eseguita, eventuali log/replay e il primo punto di divergenza. Distinguere codice superstite, vecchia variante esatta e ricostruzione moderna. Se mancano i replay originali, dichiararlo. Verificare specie/posizione esclusa, momento dell'intervento, acquisti residui, cap animali, rifornimenti, semina, assegnazioni e rollback. Il target `(4,7)` è una traccia di codice, non una certificazione della run storica.

## Disegno proposto, da rendere concreto dopo l'archeologia

Confrontare separatamente:

1. E18 775 invariata, controllo congelato.
2. E21 774 senza coltivare la casella liberata: acquisti e obbligazioni del solo animale escluso resi coerenti; esplicitare ciò che cambia. Non confondere animale non acquistato, mai collocato, pascolo demolito e animale perso.
3. E21 774 con una missione agricola completa sulla casella liberata: scelta coltura, seme, lavoratore, acqua, crescita, raccolta, consegna e vendita entro termine. Non inserire una semplice PLANT senza copertura del ciclo.

Il primo confronto misura una riduzione coerente dell'allevamento; il secondo il contributo del riuso agricolo. Non chiamare il delta valore puro del pascolo: le reazioni del controller, dell'avversario e del mercato sono parte dell'effetto. Conservare inizialmente le rotte degli altri animali e il resto del piano dove fattibile; ogni necessario cambiamento va dichiarato e tracciato, non nascosto dietro un cap.

Pianificazione biologica richiesta:

- distinguere FEED di sopravvivenza, CARE opzionale e bonus prodotto/raccolto/venduto;
- prenotare acqua e copertura dopo PLANT, controllare scadenze e fine vita;
- considerare capacità del deposito, inventari, mangime, orari di assunzione, consegna e liquidazione;
- misurare spillover sulle altre caselle e sui lavoratori, non soltanto sulla casella rimossa;
- usare solo osservazioni disponibili alla policy, senza negozi futuri o ordini avversari contemporanei;
- iniziare con un confronto documentato fra vecchia strategia 774 e nuova strategia prima di generare il bundle.

## Evidenza recente da non perdere

Analisi descrittiva di 14 diretti E18–E20.2, sette seed con ruoli appaiati:

- E18 +3539 di margine medio; circa il 76% del vantaggio nasce D12–D19.
- D20–D29: 19 vs 16 animali, 51,3 vs 43,2 colture medie, 36 vs 216 PASS, 1524 vs 1640 MOVE, pari organico e costo delle assunzioni.
- FEED per animale-giorno 94,7% vs 93,2%; CARE 86,8% vs 55,6%. Il maggior FEED è soprattutto dimensionale; il maggior CARE non dimostra ritorno marginale positivo.
- Persistenza lavoratore–casella–FEED/CARE fra giornate 22,3% vs 7,7%, ma non rigidità oraria. Segnale descrittivo di assegnazioni stabili, non prova causale del vantaggio animale.
- E18 ha più perdite crop per sete verificate: audit PLANT→WATER D12–D19 e CARE→bonus→vendita ancora da completare.
- Report e dati: `docs/model_specs/codex/e20/reports/livestock_routine_20260912/REPORT.md`, `ANALYSIS.json`, `MANIFEST.json`.
- Contabilità: `docs/model_specs/codex/e20/reports/e20_2_confirmation/CASH_GAP.md` e JSON. Maggiori ricavi grano non significano maggiori raccolti: E18 compra e rivende di più.

Il motore usa lo stesso RNG giornaliero per infestanti e apertura negozi: cambiare caselle vuote può cambiare la domanda futura anche a seed uguale. Verificare le traiettorie dei negozi. Un calendario negozi fissato artificialmente è utile solo per diagnosi; escluso da ranking e gate di submission. Il test precedente E20.3 a negozi fissati è documentato, non da confondere con partite ufficiali.

## Metodo e limiti

- Preregistrare ipotesi, campione, invarianti e controlli prima dei risultati. Una simulazione per volta sul laptop.
- Ricostruire esattamente controllo e prefisso previsto; verificare hash bundle/replay, 719 chiamate, stato terminale, errori, topologia e perdite. Non nascondere fallback o ritorni a 775.
- 22 KPI leggibili con identità seed/ruolo/avversario e fasi D1–11, D12–19, D20–29, D30. Collegare risultati a vendite, acquisti, assunzioni e stock, non soltanto conteggi delle azioni.
- Seed 180911301–307 già esposti; 180912401–407 restano inutilizzati e riservati a conferma indipendente dopo congelamento. I ruoli non sono repliche indipendenti.
- Nessuna promozione automatica. Un fallimento economico spiegato è un risultato diagnostico valido; non iterare indefinitamente fino a vincere sul campione.

E20 è ferma a E20.7: nessun upgrade E20.3–E20.7 adottato; E20.7 margine medio −9662 vs E18, 0/7 seed positivi. E20.8–E20.10 non generate, nessuna E20.11 autorizzata. Il limite massimo E20.10 resta valido per quel ramo, non è un invito a completarlo. E18 resta il candidato competitivo; E20.2 il riferimento esplorativo E20. Nessuna submission inviata in questa sessione.

## Stato del workspace

Modifiche e artefatti delle sessioni precedenti sono ancora non committati; controllare `git status` e preservare tutto, incluso `docs/model_specs/codex/e20/reports/external_first_20260910/REPORT.pdf` dell'utente. Non pulire o sovrascrivere i bundle congelati. Nessun commit/push richiesto con questo passaggio. Consultare il contratto engine aggiornato in `docs/foundation/ENGINE_CONTRACT.md` e i percorsi correnti, non copiare alla cieca percorsi storici.
