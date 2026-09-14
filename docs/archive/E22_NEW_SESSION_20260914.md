# Ripresa — E22.2 pubblicata, 13 settembre 2026

## E22.1 Q2 Grano v1 inviata — 14 settembre 2026, 12:36:55

**Nuova versione sviluppata, verificata e inviata a Kaggle; stato Pending.** Bundle `submission_codex_e22_1_q2_grano_v1.py`, SHA256 `5db3ef642ddf8cac5a8797ee92baea40a7caa6ab9eb1908db482b7fdc3c4b18a`. ID non ancora disponibile nella UI; non ripetere l'invio. [Evidenza](../model_specs/codex/e22/reports/e22_1_q2_grano_v1/PUBLICATION.json).

E22.1 originale conservata. Nuovo grano (3,7), D28 H8 → raccolta D30 H10 → vendita H22; mix 8C6S3G, stessa manodopera. 20 scenari completi nel loader reale confermano +68,15 medio (+32…+83); 14 confronti diretti contro E22.1: **14/14 vittorie, +73,43 medio**. Tutti i 34 test completati, ledger e parità verificati, nessun seme riservato. 14.380 azioni equivalenti al test diagnostico. Nessuna stima di rating esterno.

[Report 22 KPI + prezzi, 35 viste](../model_specs/codex/e22/reports/e22_1_q2_grano_v1/REPORT.html). Prossimo riscontro: attendere elaborazione Kaggle e acquisire risultati esterni; nessun monitor automatico attivato. E22.2 fix v1 è già Complete, submission 56228129.

## Pubblicazione fix e coltura finale Q2 — 14 settembre 2026

**E22.2 fix v1 pubblicata: 56228129, Complete**, bundle invariato SHA256 a9bdbcf5d0e2fefc7ecd2154336a69bf876ef52c7b8fcda2df81749abd492ac9. Invio 11:58:50 Europe/Rome; rating iniziale non stabilizzato. [Evidenza](../model_specs/codex/e22/reports/e22_2_fix_v1/PUBLICATION.json). Nessun altro bundle inviato.

**Audit E22.1 Q2:** pollaio (3,7) costruito D29 H5, sempre vuoto nei 20 replay. (4,5) ha fragole fino a D29 H3. Test diagnostico con motore, 20 baseline + 20 grano + 20 carote, D28–D30: successione in (3,7), semina D28 H8, 2 unità raccolte D30 H10 e vendute entro chiusura; nessuna nuova assunzione. Cassa netta +68,15 media grano (+32…+83), +72,30 carote (+25…+119), entrambi positivi 20/20. Grano adiacente in (3,6), (4,7), (2,6); stesso giro del lavoratore 10, consegna accorpata D30 H22. Preferenza pratica grano per continuità del calendario; nessuna superiorità generale dimostrata rispetto alle carote. Nessuna modifica ai bundle: solo esperimenti locali. [Report](../model_specs/codex/e22/reports/e22_1_q2_coop_20260914/REPORT.html).

Le sezioni successive documentano lo stato storico precedente alla pubblicazione.

## Correzioni locali E22.2 — 14 settembre 2026

**E22.2 fix v1 completata e verificata, non pubblicata.** Bundle `submission/submission_codex_e22_2_fix_v1.py`, SHA256 `a9bdbcf5d0e2fefc7ecd2154336a69bf876ef52c7b8fcda2df81749abd492ac9`. E22.2 pubblicata (56212495) conserva esattamente i byte precedenti; mix del fix 8C9S, tre pascoli Q0 con pecore.

Corretti finanziamento delle assunzioni e recupero del pasto D2, infestanti prima della semina, disponibilità atomica dei semi, risemina/irrigazione del grano D16 e irrigazione della fragola D21, spazio per il rientro notturno, consegna/vendita finale. **20/20 scenari diagnostici: 8C9S, zero fughe, zero lavoratori mancanti, zero PLANT falliti, zero crop→weed per stress e zero scarti** (prima: 24 lane, 18 grani, due fertilizzanti scartati). Scorte finali vuote; pasti mancanti isolati 576→480 giorni-animale. Dieci test mirati passati; 68 ledger contabili verificati.

Confronto diretto reale con E22.1, stessi sette semi esposti in entrambi i lati: **4/14 vittorie, margine medio −180,29 e mediano −2738**; E22.2 pubblicata aveva 4/14, +353,14 e −2092. Le correzioni meccaniche non dimostrano un miglioramento competitivo. I 20 scenari esterni usano azioni avversarie congelate e prezzi ricalcolati: sono diagnostica, non nuovi risultati Kaggle. Semi riservati non utilizzati.

[Report 22 KPI + prezzi](../model_specs/codex/e22/reports/e22_2_fix_v1/REPORT.html) · [Verifiche e hash](../model_specs/codex/e22/reports/e22_2_fix_v1/VERIFICATION.json). Prossimo lavoro: valutazione strategica/economica; nessuna pubblicazione aggiuntiva effettuata.

Precisazione sui top: **Khalid = 56220723**, famiglia E22.1, 14 pascoli e quattro pollai; 8C6S3G in 2/5, 9C5S3G in 3/5. Q3 sud-est aperto solo in 2/5 replay, ordine D19 H2. [Dettaglio](../model_specs/codex/e22/reports/top_2750_3000_20260914/KHALID_VS_E22_1.md).

## Aggiornamento esterno — 14 settembre 2026

**E22.2 Complete, rating ultimo nello storico 1706,92; E22.1 2147,08.** Storici congelati: E22.2 52 vittorie su 92 incontri competitivi, E22.1 74/151; un self-play per versione escluso. Le frequenze non sono confronti appaiati: le due versioni affrontano avversari diversi e hanno una diversa durata di esposizione.

Analizzati gli ultimi 20 replay competitivi di ciascuna versione, senza filtro per esito. E22.2 9/20 vittorie, cassa media 90.045,3, avversari rating medio 1754,8; E22.1 8/20, cassa 87.833,1, avversari 2162,0. **Il rating favorisce E22.1; la cassa media grezza non dimostra superiorità di E22.2.** [22 KPI, volumi e prezzi](../model_specs/codex/e22/reports/external_e22_2_20260914/REPORT.html).

Difetto E22.2 in 2/20 replay (108729054, 108777186): cassa D2 H1 pari a 3, due manovali assunti su tre richiesti; manca la costruzione del pascolo (2,4) a D2 H6, PLACE COW fallisce D4 H24, una mucca resta in magazzino (7C9S). In entrambi i replay si perdono anche 12 lane per overflow a D26–27. Nessuna fuga E22.2; tre fughe E22.1. Zero residui terminali di latte/lana/uova non significa vendita integrale: il report include l’audit degli scarti. Nessuna divergenza dal bundle e nessun errore contabile negli 80 lati analizzati. Nessuna modifica strategica o simulazione nuova.

[Atlante top 2750–3000](../model_specs/codex/e22/reports/top_2750_3000_20260914/REPORT.html): cinque submission selezionate per score distribuito, cinque replay ciascuna, 173.471 righe di traiettorie e 469 collocamenti. 56220723 (2814,1) è il riferimento più regolare: 14 pascoli/4 pollai in 5/5, mix 9C5S3G o 8C6S3G, zero fughe; tre pollai occupati Q0 e un pollaio vuoto (3,7). Le altre famiglie mostrano più variabilità e perdite. Non assumere ottimalità dai pattern ricorrenti. Prossima evoluzione da discutere: recupero delle assunzioni/costruzioni mancate, scelta della specie e calendario di vendita, mantenendo separati gli interventi.

Le sezioni del 13 settembre sotto restano contesto storico; questo aggiornamento supera i riferimenti al solo score iniziale 600.


## Stato corrente

- **E22.1 — Pollai**, controllo pubblicato **56206528**: tre pollai Q0 con oche; totale 8 mucche, 6 pecore, 3 oche. Bundle `submission/submission_codex_e22_1_pollai.py`.
- **E22.2 — Pascoli**, submission **56212495**, stato **Complete** verificato su Kaggle: originale 8C9S v1; pecora in ciascuno dei tre pascoli (4,1), (3,2), (2,3), totale 8 mucche e 9 pecore. Bundle `submission/submission_codex_e22_2_pascoli.py`, hash `df6991a5619f09e91bef6b6ac7034ade10f87c59e577d49c19cf197cd5cd2dcd`.
- **Calendario esterno v2**: esperimento distinto, non selezionato e non pubblicato.

[Registro versioni](../model_specs/codex/e22/VERSIONS.json) · [Pubblicazione](../model_specs/codex/e22/reports/e22_2_release/PUBLICATION.json) · [Revisione](../model_specs/codex/e22/reports/e22_2_release/REVIEW.md).

Il primo score visualizzato per E22.2 è 600,0: dato iniziale, non valutazione stabilizzata. Episodio osservato disponibile: 108620991. Il prossimo lavoro utile è analizzare un campione esterno di E22.2 confrontandolo con E22.1; attendere il mandato dell’utente prima di avviare nuove simulazioni, modifiche strategiche o pubblicazioni.

## Evidenze e limiti

[Confronto E22.2 contro E22.1](../model_specs/codex/e22/reports/e22_2_vs_e22_1/REPORT.html): 14 partite seriali, seed esposti 180911301–307 in entrambi i ruoli. E22.2 vince 4/14, media margine +353,14, mediana −2.092. I ruoli danno esiti identici: sette seed indipendenti. Nessuna superiorità interna regolare dimostrata; pubblicazione diagnostica esplicitamente richiesta dall’utente.

Revisione del file pubblicato: parità di 10.066 azioni con caricatore reale, determinismo, osservazioni immutate, zero fughe/errori contabili e tutto il latte/lana raccolto venduto. Restano giorni isolati senza alimentazione, due fertilizzanti residui e assenza di recupero generale dalle divergenze di cassa/stato. Le vendite lana cambiano anche prima di D11. I seed 180912401–407 sono ancora riservati e non usati.

[Traiettorie esterne](../model_specs/codex/e22/reports/external_pasture_trajectories/REPORT.html): sei replay con tre pascoli, calendario ricorrente. [Calendario v2](../model_specs/codex/e22/reports/q0_8c9s_calendar_v2/REPORT.html): implementato e verificato, ma margine medio +130,57, peggiore di v1 di 222,57; non scelto. La ricorrenza non prova ottimalità.

## Repository e riproduzione

Codice, report e verifiche sono versionati. I replay grezzi compressi rimangono locali, conservati senza cancellazioni, con [manifest](../model_specs/codex/e22/reports/e22_2_release/LOCAL_ARTIFACTS.json). Gli strumenti e i requisiti per rigenerare i report sono descritti nel [README](../model_specs/codex/e22/README.md). Non modificare automaticamente il checkout originale.

[Stato progetto](../PROJECT_STATE.md) · [Registro esperimenti](../EXPERIMENT_LOG.md) · [Contesto precedente archiviato](../governance/history/session_snapshots/2026-09-13_e22_2_release/NEW_SESSION.md).
