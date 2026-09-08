# Analisi dei PASS della 770 V22 a D12–D13

Il picco principale è D12: 126 PASS contro 20 del Top770-001 (6,3 volte).
A D13 sono 53 contro 25 (2,12 volte). Questi valori sono identici nei sei
casi locali V22 e nei cinque profili storici Top001 usati dal report.
La ricostruzione interna ora per ora riguarda seme 180903001, posizione 0.
La policy strumentata riproduce esattamente le azioni originali fino al passo312.
Non è stata modificata la policy né eseguita una nuova variante.

## Contabilità dei tempi

| Misura | D12 | D13 |
|---|---:|---:|
| Azioni disponibili dei lavoratori effettivamente presenti | 290 | 283 |
| PASS | 126 (43,4%) | 53 (18,7%) |
| PASS senza missione assegnata | 119 | 52 |
| PASS per attesa input al deposito | 7 | 0 |
| PASS per attesa seme | 0 | 1 |
| PASS nelle ultime sei ore | 57 | 48 |
| MOVE | 78 | 109 |
| PLANT | 2 | 26 |
| WATER | 27 | 40 |
| FEED / CARE | 14 / 14 | 14 / 14 |

Le azioni disponibili sono calcolate sui lavoratori presenti a ogni ora;
le assunzioni progressive spiegano perché non sono 13×24. I PASS non sono
prevalentemente attese di acquisto. Il minimo di cassa osservato è 15.420 a
D12 e 15.873 a D13: non provano che ogni investimento sia ammissibile, ma
non mostrano esaurimento della cassa.

## 1. La nuova terra non entra nel piano fino al giorno successivo

A D12 H1 sono sbloccati NW e NE: 34 colture e 36 intenzioni colturali.
A H2 viene emesso BUY_LAND; a H3 SW è osservato come sbloccato. Tuttavia,
le intenzioni rimangono 36 fino a H24. Solo a D13 H1 diventano 61.

Causa nel codice: `observe_plan` in `biological_plan_770_v18.py` ritorna
subito se il giorno non cambia (`if stamp==core.day:return`). Non invalida
il piano quando cambia il terreno disponibile. `planned_growth` genera
le semine dalle intenzioni: le 25 nuove caselle non sono quindi candidati
alla semina per tutta la parte restante di D12. Si piantano soltanto due
fragole; a D13 arrivano 26 PLANT e la superficie finale osservata è 61
(23 grano, 38 fragole).

Questo è un ritardo deterministico di pianificazione, non una pausa
imposta dai cicli biologici. Non attribuiamo arbitrariamente tutti i119
PASS senza missione a questo difetto: quantificare quanti siano recuperabili
richiede un confronto con il piano corretto, comprensivo di tempi e input.

## 2. La mappa biologica delle persone è congelata sul solo fattore

La stessa funzione calcola `compact_owners(...,len(core.positions))` a
inizio giornata, quando è presente il solo fattore. Tutte le aree hanno
owner=0 a D12 e a D13, anche dopo le assunzioni.

La V22 ricalcola le code dei percorsi sulle assunzioni osservate e ogni sei
ore, ma non questa mappa biologica sottostante. Non significa che tutti i
lavori siano materialmente eseguiti dal fattore: il percorso assegna anche
ai manovali. Significa che i due livelli usano responsabilità incoerenti.
La mappa obsoleta influenza `_planned_owner` nello scoring e il prelievo
aggregato di grano in `planned_prepare`. Il suo impatto marginale sui PASS
non è stato isolato con un'ablation.

## 3. Le code impediscono di redistribuire tempestivamente il lavoro

`route_prepare` rifiuta una destinazione se appartiene alla coda di un
altro lavoratore o non è la testa della propria. Nell'audit a D12 H10,
H11, H13 e H14 rispettivamente 4, 5, 4 e 4 persone emettono PASS senza
missione: per queste persone non emerge alcun percorso ammissibile e le
chiamate di preparazione rifiutate risultano soggette al vincolo di coda.
Restano colture non irrigate e alcuni FEED/CARE non ancora eseguiti.

Questo dimostra che il controller non tratta tutto il lavoro residuo come
redistribuibile. Non dimostra che ogni lavoratore libero possa raggiungere
ogni servizio utile: distanza, input e scadenze vanno verificati. Le chiamate
al preparatore sono ripetute nel ciclo di selezione e NON sono conteggi di
PASS o di lavori distinti; non si sommano alla contabilità precedente.

## 4. D13 ha soprattutto una coda finale di inattività

A D13 nelle prime dodici ore c'è un solo PASS, dovuto al seme: il piano
esteso alimenta realmente il lavoro. 48 dei53 PASS si concentrano tra H19
e H24. A D12 sono57 nelle stesse ore.

La capacità non è bilanciata nel corso della giornata: alcuni percorsi
finiscono prima, altri continuano. A D13 H24 restano23 colture non irrigate
nello stato precedente all'azione. Ma `needs_water` non richiede acqua ogni
giorno su ogni pianta: considera stress consecutivo, età delle annuali e
produzione/fertilizzazione delle perenni. Una coltura non irrigata non è
automaticamente un lavoro obbligatorio saltato. Nei due giorni FEED e CARE
arrivano entrambi a14: qui non è corretto attribuire il picco alla loro
mancata esecuzione. Il maggior WATER di Top richiede anche confronto di
età, fertilizzazione e date di produzione, non solo superficie.

## Intervento indicato dall'analisi

1. Aggiornare le intenzioni all'osservazione di nuova terra; aggiornare la
   capacità/assegnazione sulle assunzioni. Conservare i cicli già avviati.
2. Collegare ogni impegno biologico a una durata che comprenda spostamento,
   approvvigionamento e scadenza; misurare carico residuo per persona.
3. Permettere un trasferimento verificato del lavoro quando qualcuno finisce
   prima; mantenere la prenotazione delle urgenze fino al completamento.
4. Valutare il residuo fisiologico solo dopo questi interventi: completamento
   dei servizi, distribuzione oraria, superficie e cassa, non PASS da soli.

Il Top mostra che esiste una combinazione più efficiente, ma i suoi KPI
aggregati non rivelano l'esatta policy interna. Non è stata ricostruita una
sua assegnazione oraria da replay grezzi, che non sono disponibili localmente.

## Evidenze riproducibili

- `hourly_audit.json`: azioni, PASS per lavoratore, missioni, code, inventari,
  piano biologico, terreno osservato e ordini, per ciascuna ora dei due giorni.
- Generatore: `../../tools/analyze_v22_pass_d12_d13.py`.
- Replay sorgente: `../../artifacts/derived/daily_routes_v22_audit_20260907/replay.json`.
- Policy V22 e moduli storici lasciati immutati. Nessuna promozione o upload.
