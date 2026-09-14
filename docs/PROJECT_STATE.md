# Stato del progetto — E22 chiusa, E23 pronta, 14 settembre 2026

**Ultima verifica di chiusura:** E22.1 Q2 Grano v1 Complete, submission **56228842**; E22.2 fix v1 Complete, **56228129**. I riferimenti Pending nelle sezioni precedenti sono storici.

## Direzione della prossima sessione

**E23: nuova architettura basata sul confronto con i top 2750–3000.** [Brief e sequenza di lavoro](model_specs/codex/e23/README.md). E22 resta congelata come controllo; nessuna implementazione E23 iniziata. [NEW_SESSION](NEW_SESSION.md) è stato riscritto per questa ripresa; la cronologia precedente è archiviata.

Le indicazioni di pubblicazione sotto sono osservazioni datate, non un monitor live. Prima attività E23: recuperare i risultati delle due submission recenti senza reinviarle. Repository ripulito dalle cache riproducibili tramite regole Git e cataloghi con hash; report, sorgenti ed evidenze restano versionati.

## E22.1 Q2 Grano v1 inviata — 14 settembre 2026, 12:36:55

**Nuova versione sviluppata, verificata e inviata a Kaggle; stato Pending.** Bundle `submission_codex_e22_1_q2_grano_v1.py`, SHA256 `5db3ef642ddf8cac5a8797ee92baea40a7caa6ab9eb1908db482b7fdc3c4b18a`. ID non ancora disponibile nella UI; non ripetere l'invio. [Evidenza](model_specs/codex/e22/reports/e22_1_q2_grano_v1/PUBLICATION.json).

E22.1 originale conservata. Nuovo grano (3,7), D28 H8 → raccolta D30 H10 → vendita H22; mix 8C6S3G, stessa manodopera. 20 scenari completi nel loader reale confermano +68,15 medio (+32…+83); 14 confronti diretti contro E22.1: **14/14 vittorie, +73,43 medio**. Tutti i 34 test completati, ledger e parità verificati, nessun seme riservato. 14.380 azioni equivalenti al test diagnostico. Nessuna stima di rating esterno.

[Report 22 KPI + prezzi, 35 viste](model_specs/codex/e22/reports/e22_1_q2_grano_v1/REPORT.html). Prossimo riscontro: attendere elaborazione Kaggle e acquisire risultati esterni; nessun monitor automatico attivato. E22.2 fix v1 è già Complete, submission 56228129.

## Pubblicazione fix e coltura finale Q2 — 14 settembre 2026

**E22.2 fix v1 pubblicata: 56228129, Complete**, bundle invariato SHA256 a9bdbcf5d0e2fefc7ecd2154336a69bf876ef52c7b8fcda2df81749abd492ac9. Invio 11:58:50 Europe/Rome; rating iniziale non stabilizzato. [Evidenza](model_specs/codex/e22/reports/e22_2_fix_v1/PUBLICATION.json). Nessun altro bundle inviato.

**Audit E22.1 Q2:** pollaio (3,7) costruito D29 H5, sempre vuoto nei 20 replay. (4,5) ha fragole fino a D29 H3. Test diagnostico con motore, 20 baseline + 20 grano + 20 carote, D28–D30: successione in (3,7), semina D28 H8, 2 unità raccolte D30 H10 e vendute entro chiusura; nessuna nuova assunzione. Cassa netta +68,15 media grano (+32…+83), +72,30 carote (+25…+119), entrambi positivi 20/20. Grano adiacente in (3,6), (4,7), (2,6); stesso giro del lavoratore 10, consegna accorpata D30 H22. Preferenza pratica grano per continuità del calendario; nessuna superiorità generale dimostrata rispetto alle carote. Nessuna modifica ai bundle: solo esperimenti locali. [Report](model_specs/codex/e22/reports/e22_1_q2_coop_20260914/REPORT.html).

Le sezioni successive documentano lo stato storico precedente alla pubblicazione.

## Correzioni locali E22.2 — 14 settembre 2026

**E22.2 fix v1 completata e verificata, non pubblicata.** Bundle `submission/submission_codex_e22_2_fix_v1.py`, SHA256 `a9bdbcf5d0e2fefc7ecd2154336a69bf876ef52c7b8fcda2df81749abd492ac9`. E22.2 pubblicata (56212495) conserva esattamente i byte precedenti; mix del fix 8C9S, tre pascoli Q0 con pecore.

Corretti finanziamento delle assunzioni e recupero del pasto D2, infestanti prima della semina, disponibilità atomica dei semi, risemina/irrigazione del grano D16 e irrigazione della fragola D21, spazio per il rientro notturno, consegna/vendita finale. **20/20 scenari diagnostici: 8C9S, zero fughe, zero lavoratori mancanti, zero PLANT falliti, zero crop→weed per stress e zero scarti** (prima: 24 lane, 18 grani, due fertilizzanti scartati). Scorte finali vuote; pasti mancanti isolati 576→480 giorni-animale. Dieci test mirati passati; 68 ledger contabili verificati.

Confronto diretto reale con E22.1, stessi sette semi esposti in entrambi i lati: **4/14 vittorie, margine medio −180,29 e mediano −2738**; E22.2 pubblicata aveva 4/14, +353,14 e −2092. Le correzioni meccaniche non dimostrano un miglioramento competitivo. I 20 scenari esterni usano azioni avversarie congelate e prezzi ricalcolati: sono diagnostica, non nuovi risultati Kaggle. Semi riservati non utilizzati.

[Report 22 KPI + prezzi](model_specs/codex/e22/reports/e22_2_fix_v1/REPORT.html) · [Verifiche e hash](model_specs/codex/e22/reports/e22_2_fix_v1/VERIFICATION.json). Prossimo lavoro: valutazione strategica/economica; nessuna pubblicazione aggiuntiva effettuata.

Precisazione sui top: **Khalid = 56220723**, famiglia E22.1, 14 pascoli e quattro pollai; 8C6S3G in 2/5, 9C5S3G in 3/5. Q3 sud-est aperto solo in 2/5 replay, ordine D19 H2. [Dettaglio](model_specs/codex/e22/reports/top_2750_3000_20260914/KHALID_VS_E22_1.md).

## Aggiornamento esterno — 14 settembre 2026

**E22.2 Complete, rating ultimo nello storico 1706,92; E22.1 2147,08.** Storici congelati: E22.2 52 vittorie su 92 incontri competitivi, E22.1 74/151; un self-play per versione escluso. Le frequenze non sono confronti appaiati: le due versioni affrontano avversari diversi e hanno una diversa durata di esposizione.

Analizzati gli ultimi 20 replay competitivi di ciascuna versione, senza filtro per esito. E22.2 9/20 vittorie, cassa media 90.045,3, avversari rating medio 1754,8; E22.1 8/20, cassa 87.833,1, avversari 2162,0. **Il rating favorisce E22.1; la cassa media grezza non dimostra superiorità di E22.2.** [22 KPI, volumi e prezzi](model_specs/codex/e22/reports/external_e22_2_20260914/REPORT.html).

Difetto E22.2 in 2/20 replay (108729054, 108777186): cassa D2 H1 pari a 3, due manovali assunti su tre richiesti; manca la costruzione del pascolo (2,4) a D2 H6, PLACE COW fallisce D4 H24, una mucca resta in magazzino (7C9S). In entrambi i replay si perdono anche 12 lane per overflow a D26–27. Nessuna fuga E22.2; tre fughe E22.1. Zero residui terminali di latte/lana/uova non significa vendita integrale: il report include l’audit degli scarti. Nessuna divergenza dal bundle e nessun errore contabile negli 80 lati analizzati. Nessuna modifica strategica o simulazione nuova.

[Atlante top 2750–3000](model_specs/codex/e22/reports/top_2750_3000_20260914/REPORT.html): cinque submission selezionate per score distribuito, cinque replay ciascuna, 173.471 righe di traiettorie e 469 collocamenti. 56220723 (2814,1) è il riferimento più regolare: 14 pascoli/4 pollai in 5/5, mix 9C5S3G o 8C6S3G, zero fughe; tre pollai occupati Q0 e un pollaio vuoto (3,7). Le altre famiglie mostrano più variabilità e perdite. Non assumere ottimalità dai pattern ricorrenti. Prossima evoluzione da discutere: recupero delle assunzioni/costruzioni mancate, scelta della specie e calendario di vendita, mantenendo separati gli interventi.

Le sezioni del 13 settembre sotto restano contesto storico; questo aggiornamento supera i riferimenti al solo score iniziale 600.


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
