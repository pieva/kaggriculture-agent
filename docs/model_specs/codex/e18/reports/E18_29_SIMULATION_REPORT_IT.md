# E18.29 B3 — report della simulazione D1–D30

[Grafici interattivi: Top770 vs E18.29 B3, 21 standard + 4 diagnostici](E18_29_B3_SIMULATION_REPORT_D01_D30.html)

Revisione V2 del report: due sole serie, nessun diagramma Cause PASS, WATER/FEED riusciti al giorno aggiunti. Il confronto matched con E18.28 rimane esclusivamente nelle tabelle. Standard corrente: `experiments/e18/reports/common/E18_AGENT_COMPARISON_REPORT_STANDARD_V3_IT.md`.

E18.29 B3 ed E18.28 C: 14 profili matched, sette seed × due seat contro E18.16. Top770: cinque replay final-770 congelati, confronto descrittivo, non una rilevazione aggiornata della leaderboard. Nessuna nuova simulazione o modifica della policy per generare questo report.

Grafici standard: mediana puntuale e min-max osservato. Non sono intervalli di confidenza; una mediana non è una partita reale. Stock H24 D1–D29 prima dell'ultimo batch, D30 terminale. MOVE, PASS e flussi usano la giornata dell'azione.

Le tile non irrigate al checkpoint non sono automaticamente deadline mancate o colture morte: possono non richiedere WATER quel giorno oppure riceverlo nell'ultimo batch. Il delta fra checkpoint della cassa non coincide necessariamente con il flusso del giorno del ledger. I 14 profili comprendono due seat per seed, non 14 seed indipendenti.

## Sintesi operativa

| KPI | E18.29 B3 · n14 | E18.28 C · n14 | Top770 · n5 |
|---|---:|---:|---:|
| Cassa finale media ($) | 80.212,57 | 74.491,57 | 80.634,20 |
| Cassa finale mediana ($) | 77.530,00 | 70.868,00 | 75.629,00 |
| Comandi unità / partita | 7.389,00 | 7.389,00 | 7.304,00 |
| PASS / partita | 1.148,07 | 1.568,07 | 514,00 |
| PASS / 100 comandi (rapporto dei totali) | 15,54 | 21,22 | 7,04 |
| MOVE / partita | 3.299,86 | 3.053,00 | 3.473,00 |
| Altre azioni richieste / partita (non prova di utilità) | 2.941,07 | 2.767,93 | 3.317,00 |
| FEED riusciti | 325,14 | 325,14 | 326,00 |
| WATER riusciti | 1.156,86 | 1.156,86 | 1.146,00 |
| CARE riusciti | 249,86 | 249,86 | 335,00 |
| FERTILIZE riusciti | 59,57 | 32,00 | 62,00 |
| Fertilizzante raccolto, verificato | 170,86 | 106,57 | N/D |
| Fertilizzante venduto | 111,29 | 74,57 | 293,40 |
| Costo manodopera ($) | 6.858,00 | 6.858,00 | 6.298,00 |
| Crop tile-days ai checkpoint | 1.286,79 | 1.286,79 | 1.350,00 |
| WEED tile-days ai checkpoint | 41,43 | 41,43 | 0,60 |

## KPI aggiunti e perché

1. Quota PASS: distingue inattività e semplice aumento del numero di lavoratori. Il grafico è giornaliero, la tabella usa il rapporto dei totali.
2. WATER e FEED giornalieri: azioni riuscite, sommate su tutte le unità. Distinti dalle richieste e dalle consistenze. I totali sono riconciliati con il ledger operativo. Nessun diagramma Cause PASS; i contatori restano solo nei derivati per audit.
3. Flusso netto per 100 comandi: ricavi meno acquisti, personale, terra e più variazioni monetarie delle azioni. Include investimenti; non è il rendimento marginale di un singolo lavoratore o un premio per ridurre gli slot.
4. Fertilizzante raccolto: quantità realmente acquisita, non numero di comandi. Per Top770 il dato verificato è assente: N/D, mai zero.
5. Fertilizzante utilizzato: FERTILIZE riusciti. Permette di vedere se la raccolta extra alimenta i boost del piano, oltre alla vendita.

WATER/FEED entrano nello standard comune V3 su richiesta del proprietario. Quota PASS, flusso netto e fertilizzante raccolto/utilizzato restano quattro approfondimenti aggiuntivi.

## PASS: miglioramento parziale, gap ancora aperto

Totali medi per partita nella finestra, non somma delle mediane. Quota PASS = rapporto dei totali PASS/comandi. Le finestre si sovrappongono e non vanno sommate.

| Finestra | E18.29 PASS | E18.28 PASS | Top770 PASS | E18.29 quota % | Top770 quota % |
|---|---:|---:|---:|---:|---:|
| D15-D30 | 347,29 | 734,71 | 209,00 | 7,41 | 4,56 |
| D16-D30 | 333,00 | 720,43 | 199,00 | 7,47 | 4,59 |
| D25-D30 | 110,50 | 202,50 | 43,00 | 6,23 | 2,59 |

Da D15 a D30 la B3 riduce i PASS del 52,73% contro il parent, ma resta al 66,17% sopra Top770. È una riduzione, non la risoluzione del problema. I cohort Top770 sono diversi: questo gap è descrittivo, non una stima causale del profitto perso.

## Mucche progressive: risorse non ancora validate

La B3 mantiene la sequenza D1–D10 2,2,2,2,4,4,4,4,4,9. La cassa D1–D11 coincide con quella del parent in tutti i 14 profili; i nuovi incassi iniziano D12, quindi non finanziano retroattivamente D3–D9. Non esiste ancora una soluzione validata di crescita progressiva.

I tentativi precedenti D/E, smoke seed180903001 in entrambi i seat, arrivavano a 8 Cow D10 e perdevano una Sheep al refresh D11→D12. D chiudeva a 74.300, E a 69.912, contro C 77.898. La disponibilità nominale per comprare non dimostra la copertura di mangime, pickup, PLACE e FEED. Questi tentativi non dimostrano che una progressione sicura sia impossibile, ma non sono adottabili.

Prossimo esperimento proposto, non eseguito in questo report: bilancio impegnato D1–D10 con riserve separate per hire/semi/mangime, costo e slot completi BUY→PICKUP→PLACE→FEED, e anticipi ammessi solo con servizio garantito. Misurare cow-days, ricavi latte, acquisti mangime, PASS/MOVE e sicurezza; testare gli stessi seed/seat interni, senza nuovi dati pubblici per il tuning.

## Missioni extra: tabella di controllo

Su tutti i 14 profili: 900 missioni iniziate, 900 completate; 900 unità raccolte. 3,78 MOVE extra per unità raccolta (rapporto dei totali). Il costo MOVE delle missioni non coincide con il delta totale di MOVE: cambiano anche le azioni del piano a valle.

## Guasti: non affidarsi alla sola mediana

La mediana delle morti crop è zero, ma un evento esiste. I casi individuali e l'incidenza vanno sempre riportati accanto alle traiettorie aggregate.

| Seed | Seat | Giorno di servizio | Tile (x,y, base 0) | Coltura | Esito |
|---|---:|---:|---|---|---|
| 180903005 | 1 | D12 | (4, 8) | STRAWBERRY | morte per sete verificata al refresh |

E18.29: 1/14 profili con morte crop (7,14%). Lo stesso evento D12 è stato verificato nel parent selezionato; gli altri 13 parent non hanno questo audit specifico salvato. Non confrontare 1/1 parent con 1/14 candidata come tassi rappresentativi. Top770: N/D per questa diagnosi. Gate economico positivo; gate assoluto zero morti crop non superato.

## Telemetria da aggiungere al prossimo simulatore

Priorità 1: deadline PLANT→primo WATER e FEED, ritardo in turni, numero di task scaduti e minimo margine della coda; separare richiesti, eseguiti e confermati. Questo è il KPI più utile per prevenire il difetto D12.
Priorità 2: copertura Wheat in obbligazioni FEED finanziate e prelievi per-worker; copertura di cassa di hire/feed/semi già impegnati. Cash assoluto non prova che una missione sia finanziabile.
Priorità 3: latenza e quantità HARVEST→DROP→SELL per prodotto, compresi residui e perdite da shed pieno. Serve una provenienza di lotti: non è identificabile esattamente dai soli saldi aggregati.
Priorità 4: distribuzione della saturazione e del margine residuo per worker, non solo media della squadra; visualizzare code che sforano accanto a worker inattivi.

Non aggiungerei punteggi sintetici o un 'profitto per tile' ottenuto assegnando arbitrariamente costi condivisi: renderebbero meno chiara l'attribuzione causale.

## Diagnosi e riproducibilità

Il beneficio anti-PASS è concentrato D16–D30; D7–D11 rimane sostanzialmente invariato. Più fertilizzante rende eseguibili fertilizzazioni prima saltate. L'assegnazione delle code ai due ultimi hands corregge il ritardo D21; il difetto ereditato PLANT→WATER D12 resta la priorità prima di un rilascio.

La scomposizione suggerisce due indagini distinte: D7 prevale l'attesa calendario (circa 51,6 PASS/partita); D8–D10 prevalgono code proprie esaurite (102, 94 e 103,1 PASS/partita). Per D7 va verificato il vincolo temporale; per D8–D10 la distribuzione e la copertura del lavoro. Non basta aggiungere missioni: prima bisogna dimostrare che esistano attività finanziabili, utili e chiudibili entro le deadline.

[Report economico e ablation](E18_29_ANTI_PASS_DEVELOPMENT_REPORT_IT.md) · [Tentativi di mucche progressive](E18_28_FULL_SEASON_REPORT_IT.md) · [Model spec V3](../MODEL_SPEC_CODEX_E18_29_770_ANTI_PASS_V3.md). Dati e SHA-256 delle fonti: `../artifacts/derived/E18_29_B3_SIMULATION_REPORT_D01_D30_V2.json`. Il report non dipende dai download grezzi Kaggle.

Rigenerazione: `python -m docs.model_specs.codex.e18.tools.build_e18_29_simulation_report --fragment <percorso-assoluto.html>`, poi il renderer visualize sul frammento per l'export HTML. Test: `pytest docs/model_specs/codex/e18/tests/test_e18_29_simulation_report.py`.

QA della revisione: test dati e vincolo due serie; controllo a 360 e 736 px, light/dark. Esito separato: `../artifacts/derived/E18_29_SIMULATION_REPORT_QA_V2.json`. L'audit V1 rimane storico e non certifica questa revisione.
