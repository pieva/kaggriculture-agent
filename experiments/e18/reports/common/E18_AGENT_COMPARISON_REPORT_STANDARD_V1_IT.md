# E18 — formato standard di confronto tra agenti V1

Stato: ADOTTATO dal proprietario il 2026-09-05. Standard comune di reporting,
non modifica di policy, promozione o autorizzazione a nuovi test/submission.
I report specifici restano in `docs/model_specs/<agent>/<evento>/reports/`;
qui risiedono soltanto le regole condivise. Non è un template personale Codex.

## Struttura obbligatoria

1. Identità delle versioni, fonti, campione, protocollo e limiti del confronto.
2. Quattordici grafici delle consistenze/cassa D1-D30, nell'ordine sotto.
3. Tabella economica e operativa con i KPI storici pertinenti, unità e finestre.
4. Diagnosi: evidenza osservata, probabile causa, impatto economico e rimedio
   verificabile separati. Impatti non misurati dichiarati come tali.
5. Gate, regressioni, limiti, dati e comandi riproducibili.

La tabella integra i grafici: consistenza, produzione, raccolta, consegna e
vendita sono grandezze diverse. Un maggior numero di tile non prova una
maggiore produttività. Mantenere separati risultato del match e rating Kaggle.

## Grafici D1-D30: ordine e definizioni

| N. | Chiave | Etichetta / definizione |
|---:|---|---|
| 1 | `money` | Cassa al checkpoint, non patrimonio né rating |
| 2 | `people` | Hands presenti + farmer; 12 hands corrispondono a 13 persone |
| 3 | `crop_tiles` | Tile con coltura presente, somma delle cinque specie |
| 4 | `occupied_livestock_tiles` | Animali collocati sulle tile, non shed/inventari |
| 5 | `COW` | Mucche collocate |
| 6 | `SHEEP` | Pecore collocate |
| 7 | `GOOSE` | Oche collocate |
| 8 | `empty_pastures` | Strutture PASTURE senza animale |
| 9 | `MELON` | Tile a meloni |
| 10 | `WHEAT` | Tile a grano |
| 11 | `STRAWBERRY` | Tile a fragole |
| 12 | `CARROT` | Tile a carote |
| 13 | `TOMATO` | Tile a pomodori |
| 14 | `empty_coops` | Strutture COOP senza oca; non animali inutilizzati nello shed |

Due colonne su desktop, una su mobile; tutte le dimensioni visibili insieme.
Mantenere le specie a zero, con zero esplicito; un dato assente è N/D, non zero.
Colori e stili delle versioni invarianti in tutti i pannelli, legenda unica,
tooltip con entrambe le serie, scale comuni tra serie nello stesso pannello.
Scala e unità leggibili anche su mobile e nei temi chiaro/scuro.

Default aggregato: mediana puntuale e banda min-max osservata, campione indicato.
La banda non è un intervallo di confidenza e la mediana non è necessariamente
la traiettoria di un singolo episodio. Per spiegare un evento mostrare anche
il caso individuale o le transizioni, senza dedurre azioni dalla sola mediana.

Convenzione congelata del confronto corrente: H24, indice replay `24*D-1`.
In D1-D29 è lo stato precedente all'ultimo batch giornaliero; D30 è terminale
e la cassa coincide con il reward. Non chiamare tutti i punti "fine giornata
post-azioni". Eventuali report post-refresh/post-batch usano una convenzione
distinta ed esplicita, mai mescolata alla serie storica.

## KPI delle tabelle storiche da conservare

| Famiglia | KPI usati nei confronti | Presentazione / cautela |
|---|---|---|
| Campione e risultato | N match/profili, W-L-T, denaro finale medio e mediano, min-max, delta assoluto e %, quota del target dichiarato | Separare ogni matchup e delta matched; niente vantaggio attribuito alla diversa composizione degli avversari |
| Economia temporale | Cassa D10/D20/D30, variazione D20-D30; flussi D21-D30 | Integrare D15/D25 e finestra D25-D30 per la diagnosi corrente; distinguere checkpoint da finestra di azioni |
| Superficie | Crop finali e di picco, crop tile-days totali e D21-D30, weed finali e tile-days | Specificare somma dei checkpoint giornalieri; se integrata sui turni, dare durata/normalizzazione diversa |
| Lavoro | Comandi unità, MOVE, PASS e quota PASS, produttive, MOVE/produttiva, servizio crop e altre produttive | Normalizzare opcodes e denominatori prima di confrontare |
| Produzione | PLANT/WATER/HARVEST/DIG comandati e riusciti, ack rate, unità raccolte, unità/HARVEST riuscito, unità raccolte per 1.000 MOVE | Separare quantità per prodotto dalle somme eterogenee; un HARVEST può produrre più unità |
| Qualità crop | Unwatered tile-days e quota su crop, water-stressed tile-days, uscite a WEED, starvation, rotazioni su coltura viva | Unwatered al checkpoint non prova da solo una scadenza WATER mancata; definire e verificare le transizioni |
| Animali e sicurezza | Animali finali, pascoli costruiti/occupati, vuoti, perdite verificate, errori e fallback | Perdita verificata su tile + shed + inventari, distinta da trasferimento o calo sui soli tile |
| Architettura (storico) | Regimi attivati, profili finali, divergenza di azioni e architettura condizionata all'avversario | Facoltativi nella linea fixed-770: nessun obbligo di cambiare topologia per far crescere questo KPI |

Negli approfondimenti recenti aggiungere FEED/CARE eseguiti e scadenze mancate,
quantità prodotte/vendute per prodotto, ricavi e acquisti effettivi per prodotto,
costo hands/terreni, prezzo medio realizzato, residui terminali separati per
tile, shed e inventari. Sono complementi diagnostici, non dati già presenti
in ogni tabella storica o automaticamente calcolati dal solo report grafico.

### Normalizzazioni obbligatorie

- `MOVE`: raggruppare gli spostamenti direzionali effettivamente presenti nel
  motore sotto la stessa etichetta; usare conteggi di comandi unità, non di turni.
- `produttive_normalizzate`: comandi diversi da MOVE e PASS, inclusi PICKUP,
  DROP e PLACE. È un conteggio di richieste non-MOVE/PASS, non una prova di
  esecuzione utile. Alcuni runner locali storici escludevano queste tre azioni:
  conservare il campo legacy ma non confrontarlo direttamente con il normalizzato.
- `servizio_crop_comandato`: PLANT + WATER + HARVEST + DIG, secondo il benchmark
  storico E18.6. HARVEST/DIG vanno poi separati per target se serve distinguere
  coltura, animale e struttura: l'aggregato opcode non garantisce il target crop.
- Ack rate = riusciti / comandati, per opcode e stessa finestra; zero richieste
  dà N/D. Rendere espliciti i criteri di riuscita dell'estrattore.
- MOVE/produttiva e unità/1.000 MOVE: indicare se media dei rapporti individuali
  o rapporto dei totali. Default nuovo: rapporto dei totali del campione;
  per riproduzione storica preservare e dichiarare il metodo originale.
- I vecchi "incassi/spese lordi" derivati dai delta positivi/negativi di cassa
  sono proxy: vendite e acquisti nello stesso batch possono compensarsi.
  Nei nuovi report preferire fill effettivi e riconciliazione del ledger;
  senza dati sufficienti scrivere "flussi di cassa osservati, proxy".
- Residui non venduti non hanno automaticamente un valore monetizzabile pari
  alla quantità per l'ultimo prezzo: considerare capacità, percorso e impatto
  degli ordini. Non sommare stime di impatto che si sovrappongono.

## Finestre, confrontabilità e controlli

- Tabelle per partita e per D1-D10, D11-D20, D21-D30. Per le priorità correnti
  aggiungere D10-D15 e D25-D30; le finestre sovrapposte non si sommano.
- Annotare versione/config/hash, engine, data di acquisizione, episode ID,
  seat, seed, avversario, N, dati mancanti e criterio topologico. Pubblico
  "Top770" è un alias, non un filtro: dichiarare final-770 o 770 persistente.
- Test interni: stesso pool preregistrato, stessi seat/opponenti, delta matched;
  separare development, holdout e final. Nessun nuovo consumo autorizzato qui.
- Top pubblico vs locale: confronto descrittivo, non causale. Prezzi, seed e
  avversari diversi possono modificare il denaro anche con identiche quantità.
- Verificare 30 punti per episodio, somme delle specie = totali, strutture
  occupate + vuote = totale strutture. Un COOP vuoto non è un pascolo vuoto.
- Per diagnosi di fughe o specie assenti controllare anche shed/inventari e
  transizioni intragiornaliere; non dedurre assenza totale dai soli 30 snapshot.
- Per diagnosi di un gradino usare ledger, tile e azioni prima/dopo l'evento;
  il tratto interpolato di un grafico non è una nuova osservazione.
- Ogni numero deve avere fonte e definizione; N/D espliciti e gate/regressioni
  visibili. Lo standard non impone di inventare KPI indisponibili.

## Riferimento approvato e fonti storiche

Esempio grafico approvato (E18.27 V3 vs Top770, 14 pannelli):
[report e nota diagnostica](../../../../docs/model_specs/codex/e18/reports/E18_27_TOP770_D01_D30_COMPLETE_KPI_IT.md).
Il report collega l'export HTML con dati incorporati e il dataset verificabile.
Riutilizzare ordine, definizioni e convenzioni, sostituendo esplicitamente
versioni, campioni e dati; non riutilizzare i numeri dell'esempio.

Fonti del censimento KPI:

- [Benchmark Codex latest vs E17 V4D](../../../../docs/model_specs/codex/e18/reports/E18_CODEX_LATEST_VS_E17_V4D_BENCHMARK_REPORT_IT.md).
- [Gap analysis topology-matched E18.6](../../../../docs/model_specs/codex/e18/reports/E18_6_770_MATCHED_TOP3_GAP_ANALYSIS_IT.md).
- [Diagnosi sconfitte E18.16](../../../../docs/model_specs/codex/e18/reports/E18_16_KAGGLE_LOSS_DIAGNOSTIC_2026_09_04_IT.md).
- [Torneo quattro agenti V2](E18_FOUR_AGENT_REACTIVE_TOURNAMENT_V2_REPORT_IT.md).
- [Torneo architetture dinamiche V1](E18_DYNAMIC_ARCHITECTURE_TOURNAMENT_V1_REPORT_IT.md).

Schema della tabella operativa da compilare:

| KPI (unità; finestra; metodo) | Versione candidata, N | Riferimento, N | Delta | Evidenza / limite |
|---|---:|---:|---:|---|
| Da compilare con i KPI pertinenti sopra | N/D | N/D | N/D | Fonte e definizione |

Schema diagnostico: `criticità → evidenza → causa ipotizzata → impatto
misurato/stimato/non quantificato → rimedio → test/ablation di verifica`.
