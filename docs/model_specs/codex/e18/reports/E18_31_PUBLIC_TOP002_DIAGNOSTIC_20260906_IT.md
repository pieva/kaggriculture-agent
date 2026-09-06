# E18.31 UNIFIED V11 — verifica pubblica e nuovo Top770-002

Data 2026-09-06. Release **pubblicata, non promossa**. Nessuna policy cambiata
durante acquisizione e confronto. Target nostro: 770, 14 pascoli, cap 14
animali, massimo 12 manovali (13 persone incluso farmer). Non significa
12 manovali costanti dal primo giorno.

## Pubblicazione verificata

[Submission 56050866](https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56050866),
caricata alle 08:35:23 UTC, stato Complete. File
`submission/submission_codex_e18_31_770.py`, SHA-256
`59dcf7b9fb380f60460a2b300fc9043fe6ce816be2c28004a82971420650ed63`.
Prima dell'upload: quattro casi, 2.876 batch source/standalone identici e
altrettanti tramite il caricatore Kaggle; nessun errore, tutti DONE.

Primo campione esterno congelato: sei partite competitive consecutive, cinque
vittorie e una sconfitta; self-test escluso. Non è una stima stabile del rating.

| Episodio | Avversario | Cassa E18.31 | Cassa avversario | Esito |
|---|---|---:|---:|---|
| 106069705 | one | 133.549 | 67.033 | WIN |
| 106070638 | Pranav Gupta | 84.423 | 25.380 | WIN |
| 106071466 | cobrapigeon | 97.358 | 90.067 | WIN |
| 106072386 | Ahmed Samir | 108.807 | 105.255 | WIN |
| 106073291 | Malte Bories | 84.745 | 87.206 | LOSS |
| 106074233 | draven | 110.985 | 86.975 | WIN |

Tutti i sei replay completano 720 stati, hanno ledger monetario riconciliato,
zero morti crop e zero fughe animali verificate. Tutti mantengono exact770
nei 16 checkpoint D15–D30. La sconfitta non è esclusa dal report.

## Scelta del nuovo riferimento

Top770-001 storico è consumato. Il nuovo **Top770-002** corrisponde all'autore
identificato nel registro comune, submission **56044235**. È il primo candidato
che supera lo screening preregistrato: quattro finali 770 su cinque, ciascuno
con 16/16 checkpoint D15–D30 exact770. Lo screening non ha usato economia o
somiglianza con le nostre traiettorie per scegliere il riferimento.

| Episodio Top770-002 | Seat | Topologia finale | Cassa | Morti crop | Fughe |
|---|---:|---|---:|---:|---:|
| 106077622 | 0 | 770 | 66.332 | 1 | 0 |
| 106076806 | 0 | 770 | 102.846 | 1 | 0 |
| 106073019 | 1 | 770 | 100.098 | 1 | 13 |
| 106068545 | 1 | 10-7-0 | 95.184 | fuori dalle curve | fuori dalle curve |
| 106064835 | 1 | 770 | 94.599 | 1 | 0 |

La quinta partita resta nel corpus e nel denominatore dello screening.
Le quattro curve 770 provengono da due seat e tre avversari distinti; due
partite sono contro lo stesso avversario. Non sono quattro prove indipendenti
di una policy universale. Il campione contiene una vittoria e tre sconfitte
contro avversari molto più forti di quelli incontrati dalla nostra submission.

**Confondenti espliciti:** Top770-002 aggiunge tre oche/COOP e quindi supera
il nostro cap di 14 animali; 770 descrive solo i pascoli. Mantiene 12 manovali
a regime ma in chiusura il suo personale varia. Questo è un confronto
architetturale descrittivo, non un'ablation a identico mix/cap/mercato.
La selezione di un candidato 4/5 dopo più screening può sovrastimare la sua
stabilità fuori campione: non usare quel rapporto come probabilità futura.

## Report desktop standard V4

22 pannelli D1–D30, sempre due curve. WATER, FEED e CARE riusciti sono
separati. Mediana puntuale e intervallo min–max, non intervallo di confidenza.
Il report iniziale chiude il confronto storico: 14 simulazioni interne V11
contro E18.16 e cinque replay Top770-001. Il nuovo report usa esclusivamente
sei replay pubblici della nostra submission e quattro del Top770-002.
Non sono scontri diretti fra E18.31 e Top770-002: ogni coorte ha altri avversari.

Le consistenze sono checkpoint H24 prima dell'ultimo batch per D1–D29 e
terminale per D30. I flussi comprendono invece tutte le azioni del giorno.
Colture non irrigate a H24 non equivale a colture morte: il servizio può ancora
avvenire nell'ultimo batch. D30 senza colture può indicare raccolta/liquidazione,
non necessariamente perdita economica. Le perdite sono auditate separatamente.

## KPI economici e operativi

### Rigenerazione V4.1 — acquisto Q1 e Q2

Stessi sei replay nostri e quattro Top770-002: nessuna nuova simulazione,
selezione o validazione. Il pannello 03 conserva le tile coltivate e aggiunge
le totali sbloccate, con quattro curve (due quantità per i due agenti).
Gli altri 21 pannelli e tutte le loro serie restano numericamente identici.

Acquisti verificati nelle transizioni dei JSON, con giorno/ora dell'azione:

| Quadrante | E18.31 n6 | Top770-002 n4 |
|---|---|---|
| Q1 / NE, capacità 50 tile | D7 H7 in 6/6 replay | D7 H7 in 4/4 replay |
| Q2 / SW, capacità 75 tile | D11 H2 in 3/6; D11 H17 in 3/6 | D12 H2 in 4/4 |

L'acquisto di Q2 è quindi anticipato nella nostra submission di 9–24 ore,
non ritardato. Questo non dimostra che la capacità venga usata con pari
efficienza: per questo le due quantità sono sovrapposte. Coltivate esclude
pascoli/COOP e animali, conservati negli altri pannelli.

Dataset completo e audit degli acquisti:
`../artifacts/derived/E18_31_DESKTOP_PUBLIC_TOP002_LAND_V4_1.json`.
Desktop corrente nella directory della sessione:
`top002-land/e18-31-top002-land-preview.html`.
Generatori: stesso comando del report pubblico con `--land-overlay` e
`--label PUBLIC_TOP002_LAND`. Sei test reporting pass; QA su sei combinazioni
larghezza/tema pass, 22 pannelli / 46 curve / 1.380 punti, inclusi tooltip a
quattro quantità e toggle indipendenti per agente e quantità. Fonte pubblicata
immutata, nessuna modifica dell'agente o nuovo upload.

### Sintesi economico-operativa

Medie per partita, salvo le perdite che sono totali del campione. Denominatori:
sei partite E18.31 e quattro Top770-002 770. PASS/MOVE contano comandi;
WATER/FEED/CARE contano esecuzioni verificate. Non sommare indicatori sovrapposti.

| KPI | E18.31 pubblica, n6 | Top770-002 770, n4 |
|---|---:|---:|
| Cassa finale media | 103.311,17 | 90.968,75 |
| Cassa finale mediana | 103.082,50 | 97.348,50 |
| Range cassa finale | 84.423–133.549 | 66.332–102.846 |
| Vendite lorde D1–D30 | 136.736,83 | 117.098,50 |
| Costo HIRE/payroll D1–D30 | 6.858 | 5.555,75 |
| PASS D1–D30 | 841,83 | 548,50 |
| PASS / slot comandati | 11,39% | 7,68% |
| PASS D5–D10 | 294,17 | 117 |
| PASS D16–D30 | 288,17 | 214,50 |
| MOVE D1–D30 | 3.451,83 | 3.209,25 |
| WATER riusciti D1–D30 | 1.165 | 1.097 |
| FEED riusciti D1–D30 | 332,50 | 340 |
| CARE riusciti D1–D30 | 270,33 | 357,25 |
| FERTILIZE riusciti D1–D30 | 63,83 | 95,50 |
| Morti crop verificate, totale | 0/6 partite | 4/4 partite |
| Fughe animali verificate, totale | 0/6 partite | 13 in 1/4 partite |

**La cassa maggiore della candidata non dimostra superiorità sul Top.** Per
esempio il ricavo unitario aggregato del latte venduto è 141,65 contro 58,24;
per Strawberry 221,59 contro 147,56. Sono prezzi realizzati (vendite/quantità),
influenzati da mercati, tempi e policy commerciali differenti, non prezzi
controllati. Non attribuire tutto il differenziale alla produttività.

## Prime ipotesi diagnostiche generali

1. **Capacità produttiva e PASS iniziali.** Nei sei replay pubblici abbiamo
   7–8 mucche in D8 e 8–9 in D9: l'anticipo non è limitato al benchmark storico.
   Rimangono 282–300 PASS D5–D10. Il nuovo riferimento ha meno PASS e più
   colture già in D7–D8: medie 30,5/36,5 contro 24/29 nostre. Anche organico e
   MOVE differiscono: i suoi MOVE D5–D10 sono 555 contro 477, quindi non ogni
   PASS evitato è trasformato in produzione. Ipotesi da provare internamente:
   ammissione congiunta di nuove colture/animali usando capacità residua,
   alimentazione, WATER, costo dei tragitti e incasso prima della scadenza.
   Non introdurre quote di tile o mucche per giorno copiate dal Top.

2. **CARE sacrificata dopo D18.** In D19, D20, D23 e D25 le nostre medie CARE
   sono 1,17 / 2,17 / 1 / 1, mentre il FEED è 14 / 14 / 10 / 14. Questo
   identifica una perdita di servizio specifica, non genericamente assenza
   di lavoro o di mangime. Il riferimento fa circa 16,5 CARE/giorno, ma su
   16,5 animali a regime. Ipotesi: conflitto di assegnazione fra manutenzione
   del bestiame, raccolte e trasporti; distinguere successi, prerequisiti e
   priorità prima di concludere la causa. Rimedio da testare: CARE ammessa per
   valore marginale atteso e raggiungibilità, insieme alle scadenze obbligatorie
   FEED/WATER. Non togliere safety per aumentare un semplice contatore.

3. **Grano come prodotto e mangime.** Le spese BUY_PRODUCT:WHEAT sono 13.701
   contro 4.904,50 per partita; vendiamo anche più grano. È una possibile
   inefficienza di scorta/vendita/riacquisto, non ancora una perdita dimostrata:
   prezzi e fabbisogni differiscono. Verificare nel simulatore una riserva
   endogena per FEED, collegata alle scadenze e al valore netto di vendita,
   non una scorta fissa presa dal Top.

4. **Carote finali e valorizzazione.** Noi raccogliamo 83 unità e ne vendiamo
   82,67; il riferimento raccoglie/vende 91. Ricavi medi 3.994,50 contro
   4.522,50. Al netto dei soli semi acquistati nell'intera partita: 3.354,50
   contro 3.912,50. Non sono margini completi: mancano attribuzione di lavoro,
   acqua, fertilizzante, spostamenti e costo opportunità. La prossima prova
   deve ottimizzare l'ultimo ciclo vendibile entro l'orizzonte, non piantare
   fino a una data fissa o mantenere colture invendibili nel fotogramma finale.

La safety del nuovo Top non va imitata: 13 fughe in un replay e una morte
crop in ognuno dei quattro. Non introdurre oche o nuove topologie in questa
tranche; conservarne solo l'evidenza economica per un futuro esperimento.

## Provenienza, rotazione e riproduzione

- Registro comune: `experiments/e18/reports/common/E18_TOP770_BENCHMARK_ROTATION_REGISTER_IT.md`.
- Corpus nostri: `../artifacts/derived/E18_31_EXTERNAL_SUBMISSION_FIRST6_20260906.json`.
- Corpus nuovo riferimento, inclusi i cinque: `../artifacts/derived/E18_31_EXTERNAL_TOP002_FULL_20260906.json`.
- Serie grafiche: `../artifacts/derived/E18_31_DESKTOP_HISTORICAL_V4.json` e `E18_31_DESKTOP_PUBLIC_TOP002_V4.json`.
- Sintesi numerica: `../artifacts/derived/E18_31_PUBLIC_TOP002_SUMMARY_20260906.json`.
- Recupero dei 49 replay acquisiti: `E18_31_PUBLIC_REPLAY_REFERENCE_20260906_IT.md` e catalogo hash associato.
- Generatori: `tools/build_e18_31_desktop_report.py`, `tools/summarize_e18_31_public.py`.

I report desktop sono nella directory durevole della sessione:
`C:/Users/pietr/.codex/visualizations/2026/09/04/01a06ad3-93d8-77d0-a3b0-65d6af39fd46/`:
`e18-31-historical-preview.html` e `top002/e18-31-top002-preview.html`.
QA a 360/736/1024 px, light/dark: 22 pannelli, 44 curve, 1.320 marcatori,
nessun overflow/overlap, tooltip e legenda verificati. FEED/CARE ispezionati.

Top770-002 è stato esposto in questo unico ciclo, poi consumato: nessun nuovo
test di release future sul medesimo autore o su un alias diverso. Trasferire
le ipotesi generali ai campioni interni e verificare la prossima release su
nuovi avversari pubblici. Il holdout interno non è stato consumato. Nessun
commit/push, nessun cambio ai tre agenti congelati.
