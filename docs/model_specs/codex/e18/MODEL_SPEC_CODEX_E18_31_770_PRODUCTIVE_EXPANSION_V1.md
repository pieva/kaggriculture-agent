# E18.31 — capacità produttiva ed espansione integrate

Data: 2026-09-06. **Pubblicata per diagnosi esterna, non promossa.**

UNIFIED V11: submission Kaggle **56050866**, Complete, upload 08:35:23 UTC.
Standalone SHA-256 `59dcf7b9fb380f60460a2b300fc9043fe6ce816be2c28004a82971420650ed63`.
Parità source/standalone e caricatore Kaggle: quattro casi, 2.876 batch per
metodo; nessuna modifica alle policy rispetto al gate V11. Receipt:
`artifacts/derived/E18_31_KAGGLE_UPLOAD_RECEIPT_V11_20260906.json`.

Prima diagnosi pubblica: sei replay, 5 WIN / 1 LOSS; nessuna perdita biologica
verificata, tutti i ledger riconciliati. Anticipo mucche confermato D8 7–8,
D9 8–9, ma PASS D5–D10 ancora 294,17 medi. Nuovo confronto Top770-002 n4
su cinque replay selezionati topologicamente, con tre oche aggiuntive e
mercati differenti: non test causale a parità di mix. CARE intermittente
D19–D25 e scorta/vendita del grano da investigare come policy generali.
Report: `reports/E18_31_PUBLIC_TOP002_DIAGNOSTIC_20260906_IT.md`.
Standard V4 a 22 pannelli; Top770-001 e Top770-002 consumati per release
successive. Nessuna nuova policy implementata per aderire a queste curve.

## Mandato corrente

PASS e ritardo delle mucche sono da trattare congiuntamente. L'espansione animale
può creare lavoro e reddito per la capacità già pagata; non si deve attendere una
soluzione indipendente dei PASS. Conferme, risorse e deadline sono vincoli della
stessa decisione, non una fase sostitutiva dell'investimento. Focus diagnostico
D5–D10; stesse regole di ammissione per tutti i 30 giorni. Non passare ad altri
filoni prima di una soluzione verificata dei due problemi.

7-7-0, 14 pascoli, cap 14 animali, mix 9 COW / 5 SHEEP, massimo 12 manovali.
Nessun nuovo target giornaliero copiato da Top770. Baseline E18.30 CROP_POOL V2;
E18.28 C e relativa submission rimangono immutabili.

## Diagnosi verificata

Nel campione interno seed 180903001, seat 0, E18.30 contro E18.16:

| Giorno | PASS | Code esaurite | Attese calendario | Blocchi PICKUP |
|---|---:|---:|---:|---:|
| D5 | 39 | 31 | 5 | 3 |
| D6 | 57 | 56 | 1 | 0 |
| D7 | 65 | 14 | 51 | 0 |
| D8 | 103 | 102 | 1 | 0 |
| D9 | 97 | 94 | 1 | 2 |
| D10 | 105 | 103 | 1 | 1 |

Il dispatcher precedente recupera prevalentemente fertilizzante escluso dal
calendario: prima di D12 quasi tutto è prenotato, da D17 la raccolta pianificata
è zero. Questo spiega il successo asimmetrico, senza attribuire tutti i PASS alla
stessa causa. Le mucche rimangono invece legate ai collocamenti D5 e D10; in D9
una mucca già comprata resta nel deposito. D5–D6 il quadrante iniziale è pieno:
l'incremento successivo dipende anche da spazio, non dalla sola cassa.

Traccia: `artifacts/derived/E18_31_ASSIGNMENT_GATE_BASELINE_FOCUS_V1_20260906.json`.

## Implementazione sperimentale

- `tools/e18_31_assignment_controller.py`: missioni complete su capacità libera,
  consegna dei prodotti, anticipo raccolte, ACTIVATE_COW con PICKUP, eventuale
  DIG/BUILD, PLACE, FEED, CARE; conferme osservate e prenotazioni. Riparazione dei
  pascoli già costruiti ma vuoti, senza comprare animali privi di collocamento.
- `tools/e18_31_obligation_controller.py`: il mangime già consumato o trasportato
  non viene ricomprato come se fosse ancora un obbligo del deposito; guardia di
  margine per CARE aggiuntiva, dipendente dai prezzi e dalla specie, non dal giorno.
- `tools/e18_31_unified_investment_controller.py`: mercato unico, senza gli override
  calendarizzati ereditati: obblighi correnti, assunzioni, obiettivi di terreno
  imminenti, espansione eseguibile, approvvigionamento D+1. Acquisti confermati
  liberano la possibilità di finanziare un secondo lavoratore senza attendere la
  fine del primo trasporto. I target colturali e di organico del piano rimangono
  controlli della sperimentazione; non dichiarare riscritta l'intera strategia.

Le correzioni del raccordo includono: pickup animali sottratti alla coda del
lavoratore corretto; DROP valorizzati sull'inventario reale; DIG non deve rimuovere
una semina delegata già confermata; PLANT richiede tempo per la prima WATER;
le identità dei manovali sono append-only, anche quando una coda intermedia è vuota.

## Evidenza e stato dei gate

Preregistrazione: `reports/E18_31_PREREGISTRATION_20260906_IT.md`.
Esperimenti V1–V6 respinti e preservati. V9 mercato unificato iniziale respinto:
un errore nel filtro delle assunzioni saltava gli slot vuoti, perdendo anche
manovali successivi con obblighi. Corretto e coperto da test; non usare i suoi KPI.

V7 integrata: 28 partite su motore non modificato, sette seed di sviluppo, due
seat e due campioni interni. Zero errori, morti crop, fughe o missioni incomplete;
cap, riempimento finale e topologia verificati. Contro E18.16, 14 confronti appaiati:
PASS D5–D10 467,79 → 297,07; mucche medie D8 4 → 5, D9 4 → 7,71; D10 resta 9.
Una parte della riduzione PASS deriva da minori assunzioni in D10: distinguere
slot disponibili, MOVE e servizio produttivo. Cassa media 81.976 → 80.845,50
(-1,38%): **gate economico non superato**, non promuovere per i soli KPI operativi.
Controllo E18.2 appaiato disponibile solo sul seed 180903001: due casi, +6,66%;
gli altri dodici casi E18.2 sono stress del candidato, non delta imputabili.

Report: `reports/E18_31_ASSIGNMENT_SUMMARY_V7_INITIAL_20260906_IT.md`.
Freeze sorgente: `artifacts/source/E18_31_ASSIGNMENT_CANDIDATE_V7.py`.

V8 obblighi/margine: smoke sicuro, non superiore sul singolo scenario (81.951).
V10 mercato unificato con organico corretto: due smoke sicuri, 85.170 ciascuno;
mucche 4 in D4, 6 in D8, 7 in D9, 9 in D10; organico D10 preservato a 11 hands.
Non sono prove sufficienti di superiorità economica. V11 aggiunge rilascio della
prenotazione monetaria dopo conferma e deduplica obblighi mangime già prenotati.
I risultati successivi devono restare distinti dai 28 casi V7.

V11 completata: 28/28 safety nel simulatore originale. Contro E18.16, 14 coppie
su sette seed: PASS D5–D10 467,79 → 294,93; MOVE 371 → 478; slot effettivi
1.246 → 1.247. Mucche D8 4 → 7 e D9 4 → 8, D10 invariato a 9; organico
giornaliero D5–D10 invariato. Cassa media 81.976 → 81.965,64 (-0,013%):
**vantaggio economico robusto non dimostrato**, non promuovere. I due casi
E18.2 con baseline matched migliorano del 14,73%; gli altri dodici non hanno
baseline E18.30 abbinata. Le due seat non sono seed indipendenti.

Report corrente: `reports/E18_31_UNIFIED_V11_CHECKPOINT_20260906_IT.md`.
Sintesi rigenerabile: `reports/E18_31_ASSIGNMENT_SUMMARY_UNIFIED_V11_20260906_IT.md`.
Nel caso diagnostico seed 180903001 / E18.16 / seat 0 restano 295 PASS D5–D10:
229 code esaurite, 46 attese calendario, 20 attese fertilizzante. Sono cause
immediate, non 295 azioni economicamente recuperabili. La prossima verifica
resta sull'ammissione di lavoro produttivo e sui vincoli orari residui, non
sull'imitazione di una curva Top770. Il programma crop/roster è ancora legacy.

50 test mirati pass al checkpoint (31 nuovi contratti E18.31 e 19 runtime
E18.30); non è una nuova esecuzione della suite completa né una verifica
standalone/submission.

## Randomness: limite del confronto a seed uguale

Il motore originale crea un RNG giornaliero, lo usa per le sole tile vuote e
successivamente per il sorteggio dei negozi. Cambiare occupazione cambia quindi
anche il campione della domanda. Fonte locale: `kaggriculture.py`, `_end_of_day`,
righe 871–891 del pacchetto installato. Questo non annulla l'esito ufficiale e
non giustifica nascondere regressioni: richiede più scenari e diagnostica distinta.

`tools/run_e18_31_crn_diagnostic.py` consuma una estrazione per coordinata in un
contesto di test in memoria, mantenendo i negozi uguali tra trattamenti. Il file
del motore e la submission non vengono modificati. Questi test **non sono replay
Kaggle né gate ufficiali**. Su V7: sette coppie E18.16/seat 0, negozi identici;
delta medio -496,29, cinque delta negativi. Anche con domanda allineata V7 non
dimostra superiorità. Due morti crop nella baseline CRN, nessuna nel candidato:
non confondere questo regime con la safety della baseline nel motore originale.

Nel medesimo regime supplementare, V11 contro le sette baseline CRN già
congelate: negozi identici in tutte le coppie, delta medio +811,57 (+1,14%),
5/7 seed positivi e due negativi. Zero perdite biologiche nel candidato.
È un segnale favorevole all'integrazione, non una prova di superiorità nel
motore originale e non un motivo per scartare le sue regressioni.

Holdout interno non consumato. Il successivo mandato del proprietario autorizza
l'upload diagnostico sopra documentato; nessun commit/push o cambio degli agenti
congelati. I corpus pubblici aperti sono esposti, non holdout.
