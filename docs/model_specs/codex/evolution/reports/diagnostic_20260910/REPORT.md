# E18, E19, E20.1: banco diagnostico a tre

E18 e il riferimento principale. 42 partite esistenti, sette seed gia esposti, tutti gli accoppiamenti e ruoli. Nessun nuovo candidato. Le differenze descrivono comportamenti completi; non isolano la causa e non sono una validazione indipendente.

Finestre senza doppio conteggio: D15-D19, D20-D24, D25-D30. Cassa ai confini esatti del giorno, ultimo confine terminale. Ogni variazione di cassa e riconciliata con vendite - acquisti - manodopera - terreno + effetti monetari delle azioni. I 22 KPI conservano i checkpoint storici, che precedono l ultima azione giornaliera.

| Modello | Cassa finale media |
|---|---:|
| E18 | 60978.9 |
| E19 | 61443.1 |
| E20.1 | 59671.4 |

## D15-D19

| Modello | Cassa generata | Vendite | Acquisti | Manodopera | MOVE | PASS | Coltivate medie |
|---|---:|---:|---:|---:|---:|---:|---:|
| E18 | 15308.2 | 22893.9 | 5705.6 | 1880.0 | 745.0 | 51.0 | 53.4 |
| E19 | 11381.4 | 14403.8 | 1142.4 | 1880.0 | 731.0 | 187.5 | 58.2 |
| E20.1 | 11241.1 | 14202.1 | 1081.0 | 1880.0 | 738.4 | 144.0 | 57.2 |

## D20-D24

| Modello | Cassa generata | Vendite | Acquisti | Manodopera | MOVE | PASS | Coltivate medie |
|---|---:|---:|---:|---:|---:|---:|---:|
| E18 | 13450.9 | 20513.4 | 5182.5 | 1880.0 | 740.0 | 21.0 | 53.0 |
| E19 | 15040.2 | 18503.1 | 1582.9 | 1880.0 | 784.0 | 100.2 | 52.9 |
| E20.1 | 14699.2 | 18047.6 | 1468.4 | 1880.0 | 795.5 | 94.8 | 52.5 |

## D25-D30

| Modello | Cassa generata | Vendite | Acquisti | Manodopera | MOVE | PASS | Coltivate medie |
|---|---:|---:|---:|---:|---:|---:|---:|
| E18 | 18906.1 | 25614.2 | 4685.1 | 2023.0 | 934.5 | 55.6 | 43.8 |
| E19 | 18812.2 | 21932.5 | 1229.0 | 1891.4 | 831.9 | 189.0 | 30.8 |
| E20.1 | 18217.1 | 21928.3 | 1824.3 | 1886.9 | 855.9 | 150.1 | 27.6 |

## Confronti con lo stesso avversario

Delta secondo modello meno primo; ruoli mediati dentro ogni seed. Sette unita diagnostiche, non quattordici repliche indipendenti. L avversario reagisce alla partita: anche questo confronto non e un intervento causale isolato.

| Primo | Secondo | Avversario comune | Delta cassa | Seed positivi |
|---|---|---|---:|---:|
| E19 | E20.1 | E18 | -3397.0 | 1/7 |
| E18 | E19 | E20.1 | +4801.5 | 5/7 |
| E18 | E20.1 | E19 | +2069.1 | 4/7 |

## Scomposizione del divario E20.1 rispetto a E19, avversario E18

| Finestra | Delta cassa generata | Delta vendite | Delta acquisti | Delta manodopera |
|---|---:|---:|---:|---:|
| D15-D19 | -689.0 | -744.9 | -55.9 | +0.0 |
| D20-D24 | -1186.1 | -1229.4 | -43.2 | +0.0 |
| D25-D30 | -719.5 | -195.9 | +525.8 | -2.1 |

Qui il costo dei manovali non spiega il divario D15-D24: e uguale. La differenza contabile e soprattutto nelle vendite. D25-D30 contribuiscono anche maggiori acquisti. Questo localizza la domanda, ma non distingue ancora volumi prodotti, prezzi di vendita e tempi di consegna.

E18 resta il riferimento esterno di progetto. Il torneo interno non dimostra una sua superiorita universale: i modelli scambiano maggiore produzione/vendite con minori acquisti. La selezione futura deve conservare il dettaglio per avversario, finestra e seed.

[Primo esperimento da stato salvato](H001_REPORT.md) - [Protocollo del metodo](../../PROTOCOL.md).

[22 KPI per partita, con identita dell avversario](daily_22_kpi.csv) - [Dati e contrasti per seed](data.json) - [Traiettorie dei 22 KPI, torneo originale](../../../e20/reports/e20_1_confirmation/REPORT.html).
