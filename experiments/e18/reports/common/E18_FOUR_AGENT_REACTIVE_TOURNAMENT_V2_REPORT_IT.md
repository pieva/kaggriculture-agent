# E18 — torneo reattivo a quattro V2

## Decisione

Il round robin development è completo: 84 match, sei coppie, sette seed e
entrambi i seat. Nessuno dei quattro agenti supera il gate congiunto
economico, dinamico e di sicurezza.

Codex domina il denaro (`125.983,74`, 42-0) ma sul nuovo pool termina sempre
in `6-6-2`: il risultato economico non dimostra una scelta architetturale
reattiva. Claude dimostra invece la migliore causalità architetturale, ma
resta a `6.467,48` e perde 31 animali verificati. Copilot dichiara due regimi
ma produce sempre `2.840` e nessuna azione produttiva. Antigravity è stato
eseguito in tutti i round: è 0-42, con denaro zero e quasi soltanto `PASS`;
prima di poter competere richiede un nuovo gate di compatibilità col motore.

Holdout e final confirmation non sono stati consumati.

## Protocollo

- partecipanti congelati: Codex E18.1, Claude E18.1, Copilot E18.1 e
  Antigravity E17 obsoleto;
- seed development preregistrati: `180903001`-`180903007`;
- entrambi i seat per ogni coppia;
- sei coppie × sette seed × due seat = 84 match;
- nessuna sostituzione di run;
- target economico: 100.000;
- gate separati: schema/errore, sicurezza, denaro, regimi attivati,
  divergenza delle azioni e divergenza dell'architettura condizionate
  all'avversario.

## Classifica complessiva

| Agente | Match | W-L-T | Media | Min-max | Target | Regimi | Perdite bestiame |
|---|---:|---:|---:|---:|---:|---:|---:|
| Codex E18.1 | 42 | 42-0-0 | 125.983,74 | 75.921-154.740 | 125,98% | 1 | 0 |
| Claude E18.1 | 42 | 26-16-0 | 6.467,48 | 34-16.593 | 6,47% | 2 | 31 |
| Copilot E18.1 | 42 | 16-26-0 | 2.840,00 | 2.840-2.840 | 2,84% | 2 | 0 |
| Antigravity E17 | 42 | 0-42-0 | 0,00 | 0-0 | 0,00% | 1 statico | 0 |

`losses` nella classifica del JSON indica sconfitte di partita;
`verified_livestock_losses` è la metrica distinta delle perdite zootecniche.

## Tutti i testa-a-testa

| Coppia | Record primo agente | Media primo | Media secondo | Delta primo |
|---|---:|---:|---:|---:|
| Codex-Claude | 14-0 | 139.404,57 | 3.763,64 | +135.640,93 |
| Codex-Copilot | 14-0 | 116.762,71 | 2.840,00 | +113.922,71 |
| Codex-Antigravity | 14-0 | 121.783,93 | 0,00 | +121.783,93 |
| Claude-Copilot | 12-2 | 7.194,07 | 2.840,00 | +4.354,07 |
| Claude-Antigravity | 14-0 | 8.444,71 | 0,00 | +8.444,71 |
| Copilot-Antigravity | 14-0 | 2.840,00 | 0,00 | +2.840,00 |

## Round Antigravity

Antigravity compare in 42 match: 14 contro ognuno degli altri agenti, 21
come P0 e 21 come P1. Sono coperti tutti i sette seed.

| Avversario | Match | Record AG | Media AG | Media avversario |
|---|---:|---:|---:|---:|
| Codex E18.1 | 14 | 0-14 | 0,00 | 121.783,93 |
| Claude E18.1 | 14 | 0-14 | 0,00 | 8.444,71 |
| Copilot E18.1 | 14 | 0-14 | 0,00 | 2.840,00 |

Il profilo terminale è sempre privo di colture, animali, strutture e hands.
I replay locali mostrano 707-716 `PASS` per episodio e soltanto 1-4 `DIG`
nei campioni ispezionati. Il controller dichiara `STATIC_CROP_FIRST`, non
prende decisioni di regime e non monetizza. Il dato non va interpretato come
stima della qualità storica di Antigravity: dimostra che il vecchio adattatore
E17 non è un concorrente operativo valido nel protocollo E18 corrente.

## Gate dinamici

| Agente | Azioni condizionate | Architettura condizionata | ≥2 regimi | Sicurezza | Economico | Esito |
|---|---:|---:|---:|---:|---:|---:|
| Codex | 14/14 | 7/14 | no | pass | pass | fail |
| Claude | 14/14 | 14/14 | sì | **fail** | **fail** | fail |
| Copilot | 7/14 | 10/14 | sì | pass | **fail** | fail |
| Antigravity | 7/14 | 7/14 | no | pass tecnico | n/a obsoleto | fail |

Per Antigravity la divergenza apparente deriva dallo stato/seat e non da un
selector: il solo regime osservato è `STATIC_CROP_FIRST`. Non gli viene
attribuito un gate di promozione.

## Delta e prossima iterazione

### Claude

Punti da conservare: snapshot pubblico D4-D8, una decisione sticky, due regimi
effettivamente selezionati e divergenza 14/14 sia nelle azioni sia
nell'architettura. Lacune: media pari al 6,47% del target, 31 perdite
verificate, 35 cali giornalieri di animali sui tile e output terminale quasi
nullo (`0,29` crop medi). La V2 deve riparare prima il servizio del bestiame e
la monetizzazione; aggiungere altri regimi aumenterebbe solo la complessità.

### Copilot

Punti da conservare: namespace autonomo, zero errori/fallback e selector con
due etichette. Lacune: denaro costante a 2.840, zero azioni produttive, zero
crop/animali/hands di picco, backlog lifecycle terminale 25 e divergenza delle
azioni 7/14. Il selector sta modificando metadati e movimento, non una
economia agricola. La V2 deve prima superare fixture end-to-end minime
`DIG→PLANT→WATER→HARVEST→SELL`.

### Antigravity

Punto da conservare: indipendenza del namespace e zero errori formali. Lacuna
bloccante: incompatibilità operativa con il motore E18. La nuova versione va
costruita in un nuovo file/config, con un compatibility smoke test di 720 turni
che provi azioni produttive e denaro positivo, prima di introdurre snapshot e
regimi.

### Codex

Punti da conservare: 125,98% del target, zero perdite e robustezza 42-0.
Lacuna: sul pool corrente il selector sceglie sempre `6-6-2`; i tre avversari
producono action stream diversi, ma non abbastanza pressione classificata per
attivare `7-7-0`. La prossima modifica Codex resta sospesa fino alla
stabilizzazione Kaggle e all'analisi completa dei replay esterni, perché la
calibrazione locale da sola ha già prodotto un falso positivo di reattività.

## Artefatti

- JSON: `experiments/e18/artifacts/derived/common/E18_FOUR_AGENT_REACTIVE_TOURNAMENT_V2.json`;
- CSV: `experiments/e18/artifacts/derived/common/E18_FOUR_AGENT_REACTIVE_TOURNAMENT_V2.csv`;
- runner: `experiments/e18/tools/common/run_e18_four_agent_reactive_tournament_v2.py`;
- test integrità: `experiments/e18/tests/test_e18_four_agent_reactive_tournament_v2.py`.
