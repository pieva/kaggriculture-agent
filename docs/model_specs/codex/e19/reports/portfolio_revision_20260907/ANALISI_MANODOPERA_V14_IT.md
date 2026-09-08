# V14: audit operativo della manodopera

Il difetto riguarda il coordinamento delle persone e la completezza del ciclo produttivo. La superficie recuperata non dimostra che il portafoglio sia gestibile. L'analisi precedente non aveva spiegato adeguatamente CARE, PASS e infestanti insieme.

## Confronto D16–D24

Medie giornaliere per partita: sei prove V14, cinque replay storici Top770-001. Confronto descrittivo, non esperimento a mercato identico.

| Operazione | V14 | Top770-001 |
|---|---:|---:|
| MOVE richiesti | 163,85 | 141,67 |
| PASS richiesti | 37,74 | 17,33 |
| CARE riusciti | 2,11 | 14,00 |
| HARVEST riusciti | 11,81 | 24,56 |
| HARVEST senza raccolto | 6,93 | 0,00 |
| FERTILIZE riusciti | 0,56 | 5,44 |
| FEED riusciti | 11,44 | 14,00 |
| WATER riusciti | 46,44 | 46,00 |

## Riproduzione strumentata

Caso 180903001, posizione0: KPI, ledger e risultati di entrambi i giocatori identici al run originale. D16–D30: 601 PASS, tutti senza missione attiva; 62 coincidono con esaurimento del budget di ricerca. Non attribuire tutti i PASS al solo budget. 78 PASS D16–D27 avvengono con lavoratore senza missione su un animale non curato: non sono spiegabili dalla sola distanza dal lavoro.

140 HARVEST D16–D30 falliscono su WEED. Esempio D17 H8–H15: lo stesso lavoratore continua HARVEST su WEED. `_acknowledge` invalida WATER/FERTILIZE quando la pianta scompare, ma non invalida HARVEST: la missione rimane fino al reset giornaliero.

28 nuove infestazioni nel caso, tutte per scadenza/deperimento: 13 grano, 6 fragole, 9 carote; zero per mancata acqua e zero da terreno vuoto. Origini ricostruite riapplicando azioni, decadimento e refresh con il motore ufficiale. Il conteggio è di eventi, non dello stock finale. Questo caso non dimostra le medesime proporzioni negli altri cinque.

## Meccanismi nel codice

- Il certificato riserva FEED/WATER, non CARE/raccolta/fertilizzazione. Il ripiego dopo i rifiuti ammette solo servizi biologici brevi; senza tali offerte termina le assegnazioni.
- CARE riceve un valore aggiunto nel pacchetto FEED+CARE, ma una volta alimentato l'animale il CARE isolato eredita il valore minimo1 se non vi sono prodotti/fertilizzante da raccogliere. Il beneficio futuro non è valorizzato coerentemente.
- Le rotazioni hanno precedenza nel primo elemento del punteggio; in V14 la priorità4 delle raccolte in scadenza non ha più un livello distinto. Quindi dichiarare una raccolta in scadenza non garantisce che venga servita prima delle altre missioni.
- La ricerca limitata restituisce False sia per mancata fattibilità sia per budget esaurito. Sono esiti diversi e vanno distinti.
- DIG sulle infestanti viene proposto nel pacchetto di nuovo impianto; una semina respinta lascia anche il terreno non ripulito. La pulizia va comunque valutata rispetto all'uso futuro del terreno, non eseguita per migliorare il grafico.

## Irrigazione: cosa il grafico non dimostra

`unwatered_tiles_h24` legge lo stato H24 prima dell'ultima azione della giornata. Non misura le omissioni effettive dopo tutte le azioni, né quante omissioni siano consecutive. Il motore trasforma la pianta in WEED dopo due refresh consecutivi senza acqua; le nuove piante partono già con contatore1 e necessitano acqua subito. Le colture ripetute producono la quantità base anche senza acqua nel singolo giorno tollerato; il bonus fertilizzante richiede acqua nel giorno opportuno. WATER sulle annuali aumenta la resa solo nella finestra prevista. Perciò il profilo arancione alto non prova danni, né prova assenza di danni. Servono sequenze per casella, ultima azione, eventi di produzione e bonus. Non attribuire a Top001 una causa esatta senza questi dati; il materiale mostrato non è Top007.

## Correzione da perseguire

Prima correggere invalidazione delle missioni e assegnazione del lavoro già disponibile. Poi pianificare congiuntamente servizi produttivi e scadenze, incluse CARE e raccolte; valorizzare il beneficio marginale evitando doppi conteggi. Distinguere lavoro impossibile da ricerca non eseguita. Ammettere espansioni solo con capacità per tutto il ciclo, non per la sola sopravvivenza del giorno corrente. Verificare la modifica sullo stesso caso e successivamente sulla coorte, con tutti i KPI. Nessuna nuova variante di policy implementata o promossa in questo audit.

Fonti: artifacts/derived/portfolio_v14_operations_audit_20260907/{replay.json,operations_analysis.json,portfolio_v14_audit_180903001_0.json}; strumenti run_portfolio_v14_operations_audit.py e analyze_portfolio_v14_operations.py nella directory tools E19. I moduli congelati V14 non sono stati modificati.
