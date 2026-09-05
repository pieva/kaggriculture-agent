# MODEL SPEC — Codex E18.27 770 D10-D15 Cashflow V3

## Stato verificato, 2026-09-05

`IMPLEMENTED__DEVELOPMENT_MEAN_GAIN__ZERO_ESCAPES__ROBUSTNESS_GATE_FAIL__NO_UPLOAD`.

E18.27 V3 è implementata e confrontata con E18.26 contro E18.16, E18.25 ed
E18.2/V4D. È un avanzamento della linea development, non una promozione né
un sostituto del campione pubblicato. Nessun holdout/final-confirmation,
submission, commit o push. D30 non è stato modificato.

## Trattamento effettivo

- HARVEST Melon D11 anziché D13; almeno 11 hands in D11-D12.
- Tutte le semine Q2 vengono pianificate D12, dopo l'incasso D11 e l'acquisto
  del terreno. Nel caso base raggiunge 38 Strawberry a D12.
- SELL Melon nello stesso batch dei DROP realmente emessi: quantità dagli
  inventari osservati, non dalla resa prevista. Nessun ordine aggiuntivo
  espelle payroll/feed se i dieci slot sono già occupati.
- Fino a D9, il mercato vede i fabbisogni futuri E18.26; da D10 quelli del
  nuovo piano. La parità dell'action stream D1-D9 è verificata in tutti i
  confronti, non soltanto la parità delle consistenze.
- Rimangono 770, cap 14 risorse animali, massimo 12 hands. Le regole di
  ritiro, fertilizzazione, servizio e chiusura D16-D30 sono ereditate;
  cambiano età/stati e quindi le traiettorie che ne conseguono.

V1 isolava il solo anticipo del raccolto: zero fughe nello smoke, ma 29
Strawberry e vendita Melon ancora D12. V2 aggiungeva attivazione Q2 e vendita
same-batch, ma modificava ordini prima di D10 tramite lookahead. V3 corregge
questa retroazione, mantenendo il piano offline V2. Tutte le varianti e i
risultati intermedi sono conservati.

## Esiti matched

18 casi matched unici / 36 episodi parent+candidata. La ripetizione dello
smoke seed 1 nella matrice più ampia è verificata e deduplicata.

| Avversario | Casi | E18.26 media | E18.27 V3 media | Delta | Casi positivi |
|---|---:|---:|---:|---:|---:|
| E18.16, sette seed × due seat | 14 | 60.964,64 | 69.156,00 | +13,44% | 10/14 |
| E18.25, seed 180903001 × due seat | 2 | 63.096,00 | 75.002,50 | +18,87% | 2/2 |
| E18.2/V4D, seed 180903001 × due seat | 2 | 56.543,00 | 57.680,00 | +2,01% | 1/2 |

Le colonne E18.26/E18.27 sono il denaro della nostra policy contro lo stesso
avversario, non il suo reward. Nel diretto E18.16 ottiene media 86.316 contro
69.156 V3 (V3 perde 14/14); E18.2/V4D ottiene 85.694 contro 57.680 (V3 perde
2/2). E18.2/V4D è un controllo competitivo storico, non un comparatore
architetturale omogeneo e non modifica il target 770.

## Cosa è risolto e cosa no

PASS in tutti i 18 profili candidati: zero errori tecnici, zero fughe,
copertura FEED D11-D15 di ogni animale presente, cap 14, massimo 12 hands,
topologia 770 D15/D30 e prefisso D1-D9 identico. Nel seed base, i 71 Melon
sono raccolti e venduti nelle azioni D11 per 12.445; la cassa H24 è 3.956 e
diventa 10.321 includendo l'ultimo batch D11, registrato allo step successivo.
Non confondere il confine grafico H24 con una vendita biologicamente D12.

FAIL ancora aperti:

1. Robustezza economica: contro E18.16 i seed 180903003 e 180903004
   regrediscono in entrambi i seat; worst delta -21.920. Contro V4D il seat 1
   regredisce di 1.392. Il risultato medio non autorizza la promozione.
2. Completamento crop D15: non esatto nei due seat del seed 180903004 e nel
   seat 1 del seed 180903005. Controllare acknowledgement e recupero della
   singola tile, senza compensazioni di conteggio o cambi di topologia.
3. Riempimento: seed 180903007 arriva a D10 con 12 animali e un pascolo vuoto;
   entrambe le versioni terminano a 13 (9 Cow + 4 Sheep). V3 non recupera
   l'acquisizione/placement mancato. Non è una fuga e non c'è un animale
   inutilizzato nello shed terminale: risorse massime candidate 13.
4. Planner legacy: picco 62 crop entro D13 e output shadow 885 restano FAIL
   (61 crop a D15, output 868). Sicurezza e percorsi passano; i target
   mancati restano esposti e non vengono riscritti per ottenere PASS.

La prevenzione delle fughe è dimostrata nel campione; un refill generale,
una riserva finanziaria universale e la superiorità sugli incumbent no.

## Diagnosi della regressione e prossima ripresa

Nel seed 180903004 seat 0, V3 è avanti al parent di 1.115 a D15 e 2.164 a
D20, ma chiude a -14.504. In D16-D30 vende più Milk (144 contro 96), incassando
meno (10.148 contro 20.442), e più Strawberry (142 contro 116), incassando
meno (8.703 contro 16.057). Il prezzo medio realizzato Milk è 70,47 contro
212,94; Strawberry 61,29 contro 138,42. Il volume Wheat venduto scende da
353 a 316. Sono fatti contabili: non identificano da soli quanto dipenda
dalla nostra offerta, dalla risposta avversaria o dalla dinamica di mercato.

Prima di una promozione: chiudere acknowledgement crop e recupero dei posti
già vuoti nella finestra D10-D15; mantenere distinta la verifica economica
D20-D30. La successiva chiusura entro D30 deve essere una nuova ablation,
con missioni raccolto/consegna/vendita prima del taglio hands. Non attribuire
l'intera regressione all'ultimo giorno: nel seed 4 il vantaggio si deteriora
già tra D20 e D25. Nessun tuning specifico sul numero del seed e nessun
rilascio cumulativo che nasconda l'effetto di ciascuna correzione.

## Artefatti e riproduzione

- config: `configs/CODEX_E18_27_770_D10_D15_CASHFLOW_V3.json`;
- controller e builder: `tools/e18_27_d10_d15_cashflow_controller.py`;
- runner: `tools/run_e18_27_d10_d15_cashflow_gate.py`;
- test: `tests/test_codex_e18_27_d10_d15_cashflow.py`;
- piano: `artifacts/derived/E18_27_770_D10_D15_CASHFLOW_PLAN_V3.json`;
- dati: `artifacts/derived/E18_27_D10_D15_DEVELOPMENT_V3.json`,
  `E18_27_D10_D15_SMOKE_V3.json`, `E18_27_D10_D15_V4D_V3.json`;
- sintesi: `artifacts/derived/E18_27_D10_D15_CONSOLIDATED_V3.json`;
- report: `reports/E18_27_D10_D15_CONSOLIDATED_V3_REPORT_IT.md`.

Il runner accetta `--variant V3`, `--seeds`, `--seats`, `--opponents` e
`--jobs 2`. I worker del benchmark sono processi isolati, non agenti; l'audit
del mercato modifica callback temporanee, quindi non è eseguito in thread
concorrenti nello stesso processo. Gli artefatti sono scritti da un solo
processo. Test mirati e regressioni E18.26/E18.22: 15 PASS; lint dei nuovi
moduli: PASS.
