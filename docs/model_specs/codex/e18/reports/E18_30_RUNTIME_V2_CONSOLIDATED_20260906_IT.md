# E18.30 CROP_POOL V2 — integrazione e verifica interna

Data: 2026-09-06. **Sviluppo avviato e prima candidata funzionante verificata**;
non in attesa di score o replay. Parent pubblicato E18.28 C immutabile (56036993).
Topologia 770, cap 14 animali, massimo 12 manovali. Nessun upload/holdout.

## Risultato matched, sette seed × due seat contro E18.16

| KPI | Parent E18.28 C | E18.30 CROP_POOL V2 | Variazione |
|---|---:|---:|---:|
| Cassa finale media | 74.491,57 | 81.976,00 | +7.484,43 / +10,05% |
| PASS totali medi | 1.568,07 | 1.090,29 | -30,47% |
| PASS D15–D30 medi | 734,71 | 303,57 | -58,68% |
| MOVE medi | 3.053,00 | 3.291,93 | +7,83% |
| Vittorie contro E18.16 | 1/14 | 5/14 | +4 |
| Morti crop totali | 1 | 0 | difetto ereditato eliminato nei casi testati |
| Perdite animali | 0 | 0 | invariato |

14/14 delte economiche positive; worst assoluto +4.471, worst percentuale +4,87%.
Gate economico preregistrato e safety entrambi PASS. Il risultato avversario medio
nei match V2 è 83.787,36: il gap coi campioni non è ancora chiuso. Le seat sono
controlli di posizione, non quattordici seed indipendenti.

Controllo E18.2/V4D, seed 180903001 e due seat: candidata 69.768, parent 60.612
(+15,11%), avversario 83.466. Safety 2/2, vittorie 0/2. Non estrapolare la robustezza
contro E18.2 da questo solo seed. Sono tutti confronti development, non score Kaggle.

## Cosa è cambiato e perché rende

1. RESCUE: redistribuzione di WATER pianificati a rischio su lavoratori realmente
   presenti, in finestre che ammettono tutta la missione. Nello smoke senza deficit
   è identica al parent: non attribuirle ricavi che non ha prodotto.
2. POOL V1: impiego dei PASS in missioni complete di fertilizzante disponibile,
   non prenotato, con consegna e ritorno prima del successivo incarico legacy.
   Prenotazione shed, zero overflow/inventario abbandonato nei gate. Guadagno medio
   +7.456,21, ma una morte crop ereditata: **safety FAIL**, risultato conservato.
3. CROP_POOL V2: tratta semina e prima irrigazione come un incarico indivisibile.
   Se l'owner non può chiuderlo entro il giorno, lo offre prima ad altri lavoratori;
   include DIG se serve e sottrae dalle scorte i semi già impegnati nel batch.
   Semina, irrigazione e completamento richiedono conferma osservata.

Decomposizione verificata del caso smoke E18.16 P0: 94 nuove missioni fertilizzante
concluse, 241 MOVE aggiuntive; 35 FERTILIZE e 18 PICKUP del piano prima senza scorta
diventano eseguibili. Raccolto extra: 28 Strawberry e 34 Wheat. Delte di cassa:
vendite FERTILIZER +2.608, Strawberry +5.619, Wheat +361, minori acquisti Wheat
+1.063; totale esatto **+9.651**. Non è il semplice valore del fertilizzante venduto:
la disponibilità aggiuntiva migliora anche la produzione già pianificata.

La fragola persa nel parent e in POOL è un esempio del difetto strutturale:
PLANT nominale H23 e WATER H24 senza margine per ritardo di percorso. Nel caso di
regressione V2 il worker 7 acquisisce la missione a D12 H6 e la completa con conferma
a H13. Nessuna condizione su giorno/coord/seed nella regola. Cassa del caso:
parent 93.250, POOL 100.926, CROP_POOL 101.321. V2 è action-identical a POOL
in 15/16 casi; il solo caso differente recupera la coltura e +395 di cassa.

## Verifiche e limiti

- 44 test dedicati (25 core + 19 runtime); suite completa 371 pass in 254,94 s.
- OFF: 2.876/2.876 batch identici; apertura D1–D6 immutata in tutti i confronti.
- Nei 16 casi V2: zero errori, morti crop, perdite animali, missioni incomplete,
  cap violati, topologie modificate o prodotti stranded nello shed/inventari finali.
- Nessuna diminuzione giornaliera nei conteggi motore di WATER/FEED/CARE rispetto
  al parent. V2 recupera dieci WATER nel caso della fragola salvata; FEED e CARE
  invariati. Questi conteggi non sono una dimostrazione universale sulle deadline.
- Cassa incrementale riconciliata col ledger motore in ogni confronto matched.
- File autonomo senza dipendenze repository: quattro casi (seed 001 e 005, due seat),
  2.876 azioni identiche al source e altre 2.876 identiche nel caricatore `.py` Kaggle.
  Nessun errore; mediane 2–3,3 ms/chiamata. Picco locale 0,959 s durante prove
  concorrenti, vicino al budget nominale 1 s; inizializzazione seriale misurata
  cinque volte 0,264–0,297 s. Ricontrollare il margine runtime prima dell'upload.

Il motore è ancora ibrido: protegge le code legacy e introduce il pool nei PASS
effettivi. Restano circa 304 PASS da D15 e una parte rilevante nell'apertura,
congelata in questa ablation. HIRE dopo H2, riserva payroll e risposta ai fallimenti
di assunzione non sono stati modificati. Non dichiarare risolti i due casi pubblici
low-cash senza stress online specifici e generici. Nessun tuning sul Top770.

## Artifact e riproducibilità

- Grafici mobile aggiunti su richiesta: 21 pannelli standard V3, esclusivamente
  Top770 (5 replay storici final-770) vs E18.30 CROP_POOL V2 (14 casi development).
  Dataset `E18_30_TOP770_D01_D30_KPI_V3_MOBILE.json`; generatore
  `../tools/build_e18_30_mobile_kpi.py --output-dir <directory-immagini>`.
  Cinque test dati superati e verifica visiva dei sette gruppi di grafici.
  Curve mediane, fasce min-max: la cassa finale mediana E18.30 è 79.523, non
  la media 81.976 della tabella. Top770 mediana 75.629; il confronto pubblico/locale
  non permette di dedurre superiorità a parità di mercato/avversario.
  PASS D15–D30: media per partita 303,57 E18.30 contro 209 Top770; gap residuo.
- Specifica: `../MODEL_SPEC_CODEX_E18_30_770_MISSION_DISPATCHER_V1.md`.
- Preregistrazione: `E18_30_RUNTIME_PREREGISTRATION_20260906_IT.md`.
- Report matched completo: `E18_30_DEVELOPMENT_SUMMARY_V2_20260906_IT.md` e relativo
  JSON in `../artifacts/derived/` (incluse tutte le varianti e i fallimenti V1).
- Run V1: `E18_30_MISSION_GATE_SMOKE_V1_20260906.json`,
  `E18_30_MISSION_GATE_DEVELOPMENT_V1_20260906.json`.
- Run V2: `E18_30_MISSION_GATE_CROP_STRESS_V2_20260906.json`,
  `E18_30_MISSION_GATE_CROP_DEVELOPMENT_V2_20260906.json`,
  `E18_30_MISSION_GATE_CROP_CONTROL_V2_20260906.json`.
- Source V1 immutabile: `../artifacts/source/E18_30_MISSION_RUNTIME_V1.py`, SHA
  `963093cee439b4e5adefb68fe442500d9f7b575cbd83c00ed4e62a2a4706f31e`.
- Builder/verifica: `../tools/build_e18_30_submission.py`,
  `../tools/verify_e18_30_submission.py`. Manifest e prova parità:
  `E18_30_SUBMISSION_MANIFEST_V2.json`, `E18_30_SUBMISSION_PARITY_V2.json`.
- File locale: `submission/submission_codex_e18_30_770.py`, SHA
  `5c47e641aed7d2e619a356a187654f3fe2bfaed3e1302c5f978d2ee742ce01de`.
  **NON pubblicato; non incumbent promosso.** Nessun raw replay scaricato o cancellato.

Prossimi passi: stress online low-cash/roster, estensione confronto E18.2,
poi HIRE/payroll come ablation separata. Il miglioramento economico del fertilizzante
non giustifica altre missioni se non possono chiudere servizio/consegna in tempo.
Stato e indice aggiornati; cambiamenti della tranche nel working tree, nessun
nuovo commit/push. Ultimo checkpoint pubblicato `b8aaf70`.
