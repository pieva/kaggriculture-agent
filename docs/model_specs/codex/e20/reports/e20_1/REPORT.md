# E20.1 — sviluppo, conferma e traiettorie dei 22 KPI

**Non promossa: il gate indipendente non è superato.**

La candidata E20v28 conserva la topologia 7–7–2 e l'apertura di E19 fino a D11. Su 20 partite di sviluppo raggiunge 76.866,30 contro 72.406,30 di E19 (+6,16%). Su 14 confronti appaiati indipendenti contro E18, il delta diventa -5,82%; seed con delta positivo: 1/7.

[Apri il torneo interattivo con i 22 KPI](../e20_1_confirmation/REPORT.html) · [Confronto indipendente appaiato](confirmation/REPORT.html)

## Cosa cambia

1. A parità di urgenza, il pianificatore inserisce prima i tile più lontani dal lavoratore disponibile più vicino. Conserva le priorità e i vincoli di costo e capacità; modifica lo stesso ordinamento nei percorsi e nei certificati.
2. Il piano omette CARE quando non può aggiungere produzione: bonus già saturo oppure nessuna produzione residua utile. Tiene conto del consumo notturno del vecchio bonus prima di immagazzinare quello odierno.

Q2 resta una mucca in (4,5) e una pecora in (4,6). Target 10 mucche e 6 pecore, massimo 12 braccianti. Le intenzioni colturali di Q0/Q1 e l’apertura assistita sono conservate; i servizi effettivi dopo D11 cambiano con il pianificatore.

## Sviluppo e prove scartate

Cinque nuove varianti sono state provate su tutti i dieci seed già conosciuti, prima di scegliere la combinazione. L’estensione della protezione idrica e il solo accesso fuori coda azzerano lo stress ma peggiorano la cassa del 16,69% e del 20,36% rispetto a E19 nel primo screen. I percorsi distanti e il filtro CARE vengono invece verificati separatamente e poi combinati.

| Modello, sviluppo appaiato | Cassa media | Stress / partita | Perdite animali |
|---|---:|---:|---:|
| E19 | 72.406,30 | 3,55 | 0 |
| E20 precedente | 72.281,75 | 9,70 | 0 |
| E20.1 | 76.866,30 | 2,30 | 0 |

Rispetto alla E20 precedente, lo stress di sviluppo scende da 9,70 a 2,30; WATER varia di 16,25 azioni per stagione, CARE di -22,50, MOVE di -15,25. Il risultato non dipende dal semplice aumento dei WATER o dalla riduzione dei PASS.

[Screen completo](screen/REPORT.html) · [Sviluppo in entrambi i ruoli](development/REPORT.html) · [Ablation appaiata dei percorsi](paired_ablation/REPORT.html)

## Conferma su sette seed nuovi

| Modello contro E18 | Cassa media | Mediana | Minimo | Stress / partita | Perdite animali |
|---|---:|---:|---:|---:|---:|
| E19 | 58.398,86 | 52.088,50 | 36.786,00 | 4,71 | 0 |
| E20.1 | 55.001,86 | 44.655,50 | 33.991,00 | 3,79 | 0 |

Differenza media E20.1−E19: -3.397,00; mediana delle differenze per seed: -3.442,00; peggiore differenza per seed: -15.335,50. Gli scambi di ruolo non sono nuove repliche indipendenti.

La candidata è stata congelata prima di questa coorte. Nessuna variazione di strategia, parametri o seed durante la conferma. Il gate richiede economia almeno E19, mediana positiva delle differenze, miglioramento nella maggioranza dei seed, stress non superiore a E19 e zero perdite animali.

## Dove cambia la cassa, a parità di avversario

Rispetto a E19, E20.1 cambia le vendite di -1.991,64, gli acquisti di 1.529,43, le assunzioni di -124,07 e gli acquisti di terreno di 0,00; il saldo delle azioni sul campo cambia di 0,00. Queste componenti riconciliano la differenza finale di cassa.

| Prodotto | Quantità raccolta E19 | Quantità raccolta E20.1 | Delta incassi E20.1−E19 |
|---|---:|---:|---:|
| WHEAT | 319,57 | 315,64 | -700,07 |
| MELON | 72,00 | 72,00 | 0,00 |
| STRAWBERRY | 238,71 | 236,71 | -1.531,00 |
| MILK | 243,50 | 255,86 | -1.540,57 |
| WOOL | 129,00 | 144,93 | 1.347,36 |

Quantità raccolta e incassi sono grandezze distinte: dividere queste colonne non restituisce necessariamente il prezzo delle vendite. La scomposizione è contabile; non attribuisce causalmente tutto il delta a un singolo intervento, perché il mercato e l’avversario reagiscono. [Dati della scomposizione](ECONOMIC_DECOMPOSITION.json).

Il problema residuo da verificare è il margine economico di Q2 e la monetizzazione della produzione. In questa coorte E20.1 raccoglie più latte ma ne ricava meno, mentre la lana aumenta sia in quantità sia in incassi; diminuiscono anche gli incassi delle fragole. Una successiva revisione può confrontare il mix dei due pascoli e le decisioni di vendita con questo pianificatore, usando prezzi osservati e nuovi seed di conferma. È un’ipotesi di lavoro, non un miglioramento già dimostrato.

## Torneo E18 / E19 / E20.1

| Modello | Vittorie / partite | Cassa media complessiva |
|---|---:|---:|
| E18 | 20 / 28 | 60.978,89 |
| E19 | 13 / 28 | 61.443,11 |
| E20.1 | 9 / 28 | 59.671,43 |

42 partite, 7 seed e tutte le coppie in entrambi i ruoli. La classifica include due avversari diversi per modello; il confronto economico appaiato sopra mantiene invece fisso E18. Il report interattivo presenta tutti i 22 KPI, mediana e intervallo min–max, e tabelle per le tre fasi D1–D10, D11–D20 e D21–D30.

## Il controllo con lo stesso pianificatore e topologia 770

Sui dieci seed già esposti, in posizione 0 contro E18, C770 chiude a 68.041,80 e la 772 E20.1 a 77.660,50: differenza 9.618,70, positiva in 9/10 casi. Stress 3,90 contro 2,40; perdite animali 0 contro 0.

C770 usa lo stesso bundle e gli stessi due interventi, ma senza animali o riserve Q2, target 14 e mix 9 mucche / 5 pecore. È un controllo di ricerca, non una nuova versione ufficiale di E19. Il confronto non misura il mero margine contabile di due animali: cambiano anche colture, percorsi, mercato e risposta dell’avversario. È uno screen su seed conosciuti, non una seconda conferma indipendente.

[Controllo topologico e 22 KPI](topology_control/REPORT.html)

## Verifiche e completezza

- Apertura identica e limiti intragiornalieri 7–7–2 verificati su tutta la coorte di sviluppo; nella conferma l’apertura viene confrontata nelle 14 condizioni con avversario comune E18.
- Parità completa delle 719 azioni fra sorgente e standalone su due seed e due ruoli. Nove test di contratto superati, compreso il divieto di accesso a file esterni durante la creazione del bundle.
- I ledger riconciliano i saldi con l’engine. WATER, FEED e CARE derivano dalle esecuzioni riuscite, non dalle proposte.
- 7 tentativi sotto carico sono archiviati perché uno degli agenti non ha ricevuto tutte le 719 chiamate. Gli stessi casi sono stati ripetuti con un solo processo e con identici bundle, seed e limiti di gioco. I tentativi incompleti non entrano nelle medie. Non è stato escluso alcun seed dal protocollo.

Il campo condiviso `step`, salvato dal replay soltanto nel ruolo 0, viene ricostruito anche per il ruolo 1 senza copiare dati privati. Questo corregge il lettore di validazione; il bundle non è stato modificato.

## Decisione e artefatti

E20.1 resta sperimentale. Il miglioramento nello sviluppo non soddisfa il gate indipendente e non giustifica la sostituzione automatica dei riferimenti. I risultati operativi e i casi negativi sono conservati nel report, senza reinterpretare a posteriori la soglia di promozione.

[Bundle E20.1](../../../../../../submission/submission_codex_e20_772_e20v28_candidate.py) · [Specifica](../../E20_1_SPEC.md) · [Protocollo](../../E20_1_PROTOCOL.json) · [Verifica indipendente](../../artifacts/E20_1_CONFIRMATION_VERIFICATION.json)

SHA256 della candidata: `83d3f548a3a704c60ad27dd61dfc1e9badf230c1129623161f965025878e3ba1`. Nessuna nuova submission Kaggle.
