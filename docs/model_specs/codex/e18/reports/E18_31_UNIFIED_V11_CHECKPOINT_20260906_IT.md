# E18.31 UNIFIED V11 — investimento e capacità produttiva

Data: 2026-09-06. Sviluppo interno, non pubblicato e non promosso.
Baseline: E18.30 CROP_POOL V2, non la submission pubblica E18.28.

## Decisione e risultato

La correzione del proprietario è incorporata: anticipare le mucche può creare
lavoro per manodopera già pagata. Non attendere di risolvere prima i PASS.
Disponibilità della tile, acquisto, trasporto, collocamento, alimentazione,
tempo utile alla produzione e cassa fanno parte della stessa decisione.

Il candidato anticipa la crescita e riduce i PASS senza tagliare l'organico
D5–D10. Non è però una soluzione completa: il vantaggio economico medio sul
controllo principale rimane sostanzialmente nullo e molti PASS persistono.

## Confronto nel simulatore originale

28 partite: sette seed di sviluppo 180903001–180903007, due seat, due campioni
interni E18.16 ed E18.2/V4D. Nessun dato Top770 nelle nuove regole. Nessun
holdout consumato. Tutti i 28 casi superano safety: zero errori, morti crop,
perdite animali e missioni incomplete; cassa riconciliata, cap rispettati,
14 animali finali e topologia 7-7-0 verificati.

Le medie seguenti sono i 14 confronti appaiati contro E18.16, non 14 seed
indipendenti. Il numero di mucche è rilevato a fine giornata.

| Giorno | PASS E18.30 | PASS V11 | Mucche E18.30 | Mucche V11 | Manovali, entrambe |
|---|---:|---:|---:|---:|---:|
| D5 | 39,29 | 25,00 | 4 | 4 | 5 |
| D6 | 57,29 | 42,00 | 4 | 4 | 5 |
| D7 | 65,57 | 42,00 | 4 | 4 | 9 |
| D8 | 103,00 | 60,00 | 4 | 7 | 8 |
| D9 | 97,00 | 60,00 | 4 | 8 | 10 |
| D10 | 105,64 | 65,93 | 9 | 9 | 11 |

| KPI medio | E18.30 | V11 |
|---|---:|---:|
| PASS D5–D10 | 467,79 | 294,93 |
| MOVE D5–D10 | 371,00 | 478,00 |
| Slot lavorativi effettivi D5–D10 | 1.246 | 1.247 |
| Azioni diverse da MOVE/PASS D5–D10 | 407,21 | 474,07 |
| Mucche-giorno D5–D10, snapshot giornalieri | 29 | 36 |
| PASS D1–D15 | 801,00 | 555,29 |
| PASS D16–D30 | 289,29 | 282,93 |
| Cassa finale | 81.976,00 | 81.965,64 |
| Vittorie contro E18.16 | 5/14 | 12/14 |

PASS D5–D10 circa -37%; non tutto il recupero è servizio: ci sono 107 MOVE
aggiuntive. Anche le altre azioni non equivalgono automaticamente a ricavi.
La differenza di uno slot riflette il momento di assunzione, non un aumento
del target giornaliero. Le mucche-giorno sono una proxy, non ore esatte di
produttività o ricavi aggiuntivi attribuibili.

Cassa finale: -10,36 medi (-0,013%), 7/14 delta positivi. Le maggiori vittorie
non provano da sole un incremento assoluto di reddito: cambia anche il
risultato dell'avversario. Il motore accoppia occupazione, RNG e negozi.

Contro E18.2/V4D sono disponibili baseline E18.30 solo sul seed 180903001:
due confronti appaiati, 69.768 → 80.047 (+14,73%), nessuna vittoria in questi
due casi. Gli altri dodici casi candidati sono stress di sicurezza, non
confronti economici appaiati. Nessuna conclusione generale da un solo seed.

## Perché non è ancora risolto

Nel caso diagnostico seed 180903001 / E18.16 / seat 0 rimangono:

| Giorno | Coda esaurita | Attesa calendario | Attesa fertilizzante | PASS |
|---|---:|---:|---:|---:|
| D5 | 19 | 3 | 3 | 25 |
| D6 | 37 | 1 | 4 | 42 |
| D7 | 16 | 22 | 4 | 42 |
| D8 | 53 | 2 | 5 | 60 |
| D9 | 57 | 3 | 0 | 60 |
| D10 | 47 | 15 | 4 | 66 |
| Totale | 229 | 46 | 20 | 295 |

Queste sono classificazioni immediate del comando, non una prova di lavoro
remunerativo disponibile per ogni PASS. Non confondere 229 code esaurite con
229 azioni utili certamente perse.

La nuova ammissione di investimento non cambia a metà mese. Persistono invece
obiettivi crop, organico e orari nominali del piano precedente. La riduzione
asimmetrica della versione E18.30 dipendeva anche dal fertilizzante: quasi tutto
prenotato nel programma iniziale, nessuna raccolta pianificata da D17. V11
ammette opportunità in entrambi i periodi, ma non riscrive l'intera strategia.

D5–D6 lo spazio iniziale è occupato da 19 colture e 6 animali. Il numero di
mucche non può crescere solo grazie alla liquidità: occorre una destinazione
realmente libera e accessibile. D8–D9 il candidato sfrutta nuove destinazioni
senza aspettare il collocamento calendarizzato D10.

Il prossimo intervento rimane nello stesso filone: verificare quali attese
orarie siano ancora necessarie dopo l'osservazione dei prerequisiti e quali
code esaurite nascondano missioni con rendimento netto positivo, includendo
trasporto e manutenzione. Nessun riempimento dei turni fine a sé stesso,
nessuna data/quantità obbligatoria copiata da Top770.

## Diagnostica supplementare della variabilità

Nel motore originale il RNG giornaliero è consumato dalle sole tile vuote
prima di sorteggiare i negozi. Cambiando occupazione si possono quindi cambiare
i negozi anche a seed uguale. Questo non autorizza a ignorare regressioni.

Test CRN separato: consumo RNG per tutte le coordinate, applicazione erbacce
solo alle tile eleggibili. Patch in memoria del test, non modifica del pacchetto
installato e mai componente dell'agente. Non è un replay né il gate Kaggle.

Contro le sette baseline CRN congelate, V11 mantiene negozi identici in tutte
le coppie; delta cassa per seed:

| Seed | Delta V11 − E18.30 |
|---|---:|
| 180903001 | +3.963 |
| 180903002 | +3.557 |
| 180903003 | +238 |
| 180903004 | -1.632 |
| 180903005 | +99 |
| 180903006 | +168 |
| 180903007 | -712 |

Media +811,57 (+1,14% su baseline 71.193), 5/7 positivi. Zero perdite biologiche
nel candidato; la baseline CRN ha due morti crop complessive, diversamente
dal suo campione originale. Segnale favorevole, non superiorità dimostrata.

## Provenienza, test e limiti

- `../artifacts/derived/E18_31_ASSIGNMENT_GATE_UNIFIED_V11_DEVELOPMENT_20260906.json`:
  28 casi originali, azioni aggregate, tracce D5–D10, ledger e hash sorgenti.
- `../artifacts/derived/E18_31_ASSIGNMENT_SUMMARY_UNIFIED_V11_20260906.json`:
  confronto appaiato e controlli safety riproducibili.
- `../artifacts/derived/E18_31_CRN_DIAGNOSTIC_UNIFIED_V11_20260906.json` e
  `../artifacts/derived/E18_31_CRN_DIAGNOSTIC_V7_20260906.json` (solo BASELINE):
  regime supplementare, da non mescolare alle medie originali.
- 50 test mirati pass: 31 nuovi contratti E18.31 e 19 runtime E18.30.
  La suite completa storica di 371 test non è stata rieseguita qui.

Le revisioni precedenti, incluse quelle respinte, restano evidenza storica.
Nessuna E18.31 standalone/submission è stata costruita o caricata. Nessun
commit/push in questa tranche; altri agenti e baseline congelate preservati.
