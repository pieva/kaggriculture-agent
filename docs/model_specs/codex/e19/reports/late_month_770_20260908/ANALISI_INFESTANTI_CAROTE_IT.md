# V25: infestanti e successione a carote, D16–D30

## Esito

L'aggiornamento anticipa la messa a coltura di Q2, ma non riserva ancora
lavoro per raccogliere e rinnovare le colture alle loro scadenze. La chiusura
non ha una successione alle carote coordinata con la liberazione dei terreni.
Nessuna modifica alla policy in questa analisi.

Audit completo: seme180903001, posizione0. Rerun con risultati identici al
caso originale, poi719azioni riprodotte esattamente dalla policy strumentata.
Gli altri cinque casi sono confrontati dai ledger e dai KPI già disponibili;
la classificazione causale per casella sottostante riguarda un solo replay.

## Infestanti: quattro categorie, non solo irrigazione

| Origine, nel replay analizzato | Nuovi eventi |
|---|---:|
| Grano scaduto con prodotto ancora presente | 19 |
| Fragole scadute con prodotto ancora presente | 4 |
| Fragole dopo raccolto finale, prodotto già zero | 17 |
| Fragola morta per mancanza d'acqua | 1 |

Sono41eventi, non41caselle presenti contemporaneamente: alcune infestanti
vengono eliminate. Nel caso analizzato aD30 ne restano30. La media sei casi
è27,33. Il precedente indicatore «perdite colture per acqua» conta solo
l'ultima riga: non è un indicatore completo delle perdite agronomiche.

A D17 H5 otto caselle di grano seminato aD12 diventano infestanti. Il loro
termine di maturazione era D16; la scadenza di decadimento inizia D17.
Nessun lavoratore raccoglie su quelle caselle al momento dell'evento.
A D16 ci sono84PASS e nessuna nuova semina, aD17 altri68PASS. Il raccolto
non viene assicurato prima della scadenza pur in presenza di tempo inattivo.
Il grafico mostra7infestanti aD17 perché una delle otto viene già rimossa.

Il motore sottrae una unità di prodotto ogni due tick dopo max_lifespan_step
finché la pianta diventa WEED. L'acqua non sposta questa scadenza.
Le19+4caselle rappresentano fallimenti di raccolta tempestiva, non soltanto
una diversa scelta di irrigazione. Il numero di eventi non misura da solo
le unità e il valore economico persi nell'intero decadimento.

A D29 H1 invece14fragole diventano infestanti con yield_units già zero;
altre3 aD30. Qui il prodotto è già stato raccolto: pulire soltanto per
abbassare il grafico può non avere ritorno entro fine partita. Il problema
produttivo è se una sostituzione anticipata avrebbe fruttato più dell'ultimo
ciclo di fragole, non il solo aspetto del terreno aD30.

## Rinnovo e raccolta sono ancora accoppiati male

La policy biologica propone contratti HARVEST–DIG/PLANT–WATER; il filtro
V22/V25 impedisce che una HARVEST semplice sostituisca un contratto di rinnovo
assegnato. Le missioni NEW_ROTATION devono superare il certificato di capacità
per l'intero nuovo lavoro. A D16 l'audit registra69rifiuti del certificato
per proposte di crescita, non69lavori distinti. Questo documenta un ostacolo
nel passaggio tra ciclo vecchio e nuovo: l'urgenza del raccolto va protetta
anche quando la risemina non può essere autorizzata. Non abbiamo isolato con
un'ablation quanti degli otto fallimenti D17 dipendano da ciascun filtro.

## Carote: poche, anticipate, quasi nessuna nuova semina nella finestra finale

Nel caso180903001 si seminano5carote aD23,4 aD24 e1 aD27. Nessuna aD25,
D26 oD28. Le prime vengono raccolte aD26–D27; non costituiscono quindi una
campagna estesa di chiusura. Nei semi002/003 ce ne sono ancora meno.

Le carote richiedono2giorni per il primo raccolto e3per il ciclo massimo:
una semina aD26/D27 prepara il raccolto aD29/D30; aD28 resta solo il ciclo
accorciato. Dopo quella finestra la mancata successione non si recupera.

A D26 la V25 disattiva piano e code biologiche e torna alla policy di chiusura
V16. Questa confronta valori previsti delle colture, non un programma di
conversione alle carote. Nel caso001, aD26H1 stima grano121,13 contro
carote94,54 (valori di ammissione, NON ricavi realizzati) e preferisce grano.
A D27 le carote diventano preferibili,94,54 contro86,54, ma viene eseguita
una sola semina. A D28 entrambe sono positive, eppure nessuna nuova semina
passa:572rifiuti del certificato di capacità durante le rivalutazioni e
zero accettazioni. Non è quindi sufficiente aumentare il valore delle carote.

A D26/D27/D28 il caso001 ha rispettivamente12/9/30PASS. La capacità locale
residua, gli spostamenti e i servizi già impegnati rendono inammissibili molti
nuovi cicli; queste verifiche vanno fatte prima, preparando le caselle e i
lavoratori quando la finestra utile è ancora aperta. I conteggi di chiamate
ripetute a preparatore/certificato non sono conteggi di lavori indipendenti.

Il seme003 conferma che non è solo indisponibilità generale di semina:
aD26 esegue14nuove semine di GRANO e10DIG; le carote rimangono4e vengono
raccolte aD27. La scelta economica e la capacità influenzano entrambe il mix.

## Confronto con Top770-001

Il profilo visualizzato mantiene infestanti prossime a zero e porta le
carote fino a38caselle nella chiusura. La V25 lascia invece accumulare13
infestanti già aD25 nei tre semi, mentre le carote hanno mediana4caselle.
Questo divario è precedente ai residui terminali e rappresenta un problema
concreto di continuità produttiva. L'assenza di infestanti nel Top non basta
a ricostruire la sua precisa sequenza di azioni: replay grezzi Top non disponibili
localmente. Non attribuiamo al Top regole interne non osservate.

## Correzione indicata, da verificare con una nuova variante

1. Prenotare la raccolta prima del decadimento, separandola dall'ammissione
   della risemina. Non perdere prodotto perché il nuovo ciclo non passa.
2. Per ogni casella prevedere: ultima raccolta, eventuale rinuncia all'ultima
   produzione di fragole, DIG, semina successiva, acqua, raccolta e consegna.
3. Da D23 preparare la transizione D26–D30 con confronto tra ciclo residuo di
   fragole, grano e carote, includendo capacità e tempi reali. Il piano di
   chiusura deve ereditare impegni e disponibilità, senza ricominciare da zero.
4. Misurare separatamente prodotto decaduto, morte per acqua, infestanti
   ripulibili in tempo per una nuova coltura e residui senza produzione futura.
   Non ottimizzare il solo numero di infestanti finali.

Audit riproducibile: audit.json; script ../../tools/analyze_v25_late_month.py.
Replay ../../artifacts/derived/daily_routes_v25_audit_20260908/replay.json.
