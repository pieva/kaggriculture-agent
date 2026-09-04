# Copilot E18 — torneo di confronto con Claude e Antigravity e aree di miglioramento

## Obiettivo

Questo documento raccoglie il confronto diretto tra la linea Copilot E18 e le ultime versioni disponibili di Claude e Antigravity, definendo il punto di partenza operativo per il nuovo candidato Copilot E18.3. La lettura è orientata a capire dove Copilot deve migliorare prima di introdurre la reattività di regime.

## Protocollo di riferimento

Il repository già contiene il round robin diagnostico più aggiornato:

- partecipanti: `CLAUDE_E18_2`, `COPILOT_E18_2`, `ANTIGRAVITY_E18_1`;
- 7 seed development (`180903001`–`180903007`), entrambi i seat;
- 3 coppie, 42 match real-engine;
- gate diagnostici: zero errori/fallback, zero perdite zootecniche verificate, obiettivo economico informativo da 15.000.

File di riferimento:

- `experiments/e18/tools/common/run_e18_claude_copilot_antigravity_v1_tournament.py`;
- `experiments/e18/artifacts/derived/common/E18_CLAUDE_COPILOT_ANTIGRAVITY_TOURNAMENT_V1.json`;
- `experiments/e18/reports/common/E18_CLAUDE_COPILOT_ANTIGRAVITY_TOURNAMENT_V1_REPORT_IT.md`.

## Risultati consolidati

| Agente | Record | Denaro medio | Min–max | Stdev | Regimi attivati | Perdite zootecniche |
|---|---:|---:|---:|---:|---|---:|
| Claude E18.2 | 27-1-0 | 14.236,36 | 1.063–21.029 | 4.097,13 | `LOW_PRESSURE_BALANCED` | 24 |
| Antigravity E18.1 | 15-13-0 | 9.218,46 | 6.442–12.079 | 1.612,98 | `BALANCED_SERVICE`, `EXPANSION_TEMPO` | 0 |
| Copilot E18.2 | 0-28-0 | 260,00 | 260–260 | 0,00 | `EXPANSION` | 0 |

## Valutazione del nuovo Copilot

La curva di Copilot è il chiaro punto di debolezza: `money_mean = 260,00` con `stdev = 0` in tutti i 28 match, indipendentemente dall'avversario. Il problema non è un semplice deficit quantitativo, ma un blocco strutturale: `peak_hands_mean = 0,0`, `peak_crops_mean = 1` e nessuna vera attivazione di `Q1`/`Q2`.

In pratica il controller non riesce a trasformare il suo potenziale di label e regime in manodopera reale, terreno coltivato e flusso economico. Il risultato è identico in ogni match: il motore non riesce a costruire la base produttiva preventiva.

## Aree di miglioramento per Copilot

### 1) Gate di assunzione della manodopera

Il problema più urgente è il `hire dispatch` morto. Il candidato Copilot E18.3 entra in diagnosi con il requisito obbligatorio: quando `hands == 0`, il controller deve emettere un ordine `HIRE` e passare poi subito a un ciclo produttivo. Senza questo passo, nessuna logica di regime, crop lifecycle o market routing può essere economica.

Obiettivo di correttivo:

- `HIRE` in apertura quando la forza lavoro è zero;
- budget netto dedicato alla prima assunzione;
- check specifico evitante il plateau su denaro statico.

### 2) Forza lavoro allocata e sostenibile

Nel torneo, Copilot non impiega mai manodopera, ne consegue:

- `peak_hands_mean = 0`;
- nessuna capacità di servizio dei tile;
- nessun backlog di raccolta/ vendita;
- nessuna scala di `Q1`/`Q2`.

L'area di intervento è la baselining del workforce e la sua allocazione persistente a `DIG`, `PLANT`, `WATER`, `HARVEST`:

- ogni hired hand deve avere un target produttivo;
- il budget di lavoro deve crescere con il servizio attivo;
- la capacità di coltivazione deve essere compatibile con `water` e `harvest` giornalieri.

### 3) Lifecycle del coltivo e throughput del terreno

Il primo controllo economico deve arrivare da una catena plausibile:

`DIG -> PLANT -> WATER -> HARVEST -> SELL`

Con una crescita del terreno coltivato in funzione della capacità servita, non solo del contesto di label. Se la superficie cresce senza servizio, il sistema moltiplica movimento e pass ma non produce output.

Le priorità sono:

- `PLANT` solo se la capacità di irrigazione e raccolta è disponibile;
- `WATER` in tempo reale e non solo come azione di label;
- `HARVEST` prima della scadenza del raccolto;
- `SELL` con backlog ridotto e inventory emergente.

### 4) Distanza tra regime e budget reale

I risultati mostrano che la logica di regime in Copilot non riesce a trasformare una scelta di politica in un cambiamento di footprint reale. Il problema è a monte del regime: non c'è una base di lavoro su cui il regime possa applicarsi. Per questo il nuovo percorso deve rispettare il gate diagnostico e introdurre la reattività solo dopo aver risolto la base:

- prima `HIRE` e task reali;
- poi workforce + capacity;
- poi snapshot avversario e selezione sticky;
- infine regime causale e full loop economico.

### 5) Controlli di sicurezza economica

Copilot non ha registrato perdite zootecniche, ma l'assenza di manodopera rende la sicurezza del confronto meno rilevante del vero problema: non c'è economia. La sicurezza futura deve comunque essere costruita in modo coerente con le linea di lavoro:

- zero errori e fallback;
- no over-commit su terra/animali senza servizio;
- no growth di superficie senza raccolta.

## Posizionamento del nuovo percorso Copilot

Il nuovo candidato `COPILOT-E18.3-DISPATCH-DIAGNOSIS-V1` è il passaggio corretto perché entra esattamente nel punto di blocco osservato dal torneo: la mancanza di `HIRE` in fase early game. Dopo questa correzione, l'iterazione successiva non deve mai tornare a cambiare etichette senza dimostrare un reale cambiamento di:

- footprint coltivato;
- budget workforce / servizio;
- backlog di raccolta e vendita;
- q1/q2 activation reale.

## Verdetto operativo

Tra Claude, Antigravity e Copilot, l'elemento più chiaro è che Copilot non ha ancora un early-game economic loop. Claude ha un vantaggio economico ma fallisce nella sicurezza; Antigravity è tecnico e pulito ma limitato in throughput. Copilot quindi ha il maggiore gap di base, ma anche il più alto potenziale di miglioramento se la prima leva da correggere è il `HIRE` e la pipeline produttiva reali.

Questa è la direzione corretta per il prossimo tuning del Copilot E18: meno regime, più contratto di lavoro e attività concreta; poi regime dinamico; poi confronto con i top agent dell'ultimo torneo.
