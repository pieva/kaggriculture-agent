# V51 — assegnazioni complete al giorno 29

Sviluppo locale su V49F. Nessuna modifica alla baseline congelata, nessuna
submission. Il risultato di ciascuna revisione è nel relativo report:
[A](reports/pass_reduction_v51/REPORT_V51A_IT.md),
[B](reports/pass_reduction_v51/REPORT_V51B_IT.md),
[C](reports/pass_reduction_v51/REPORT_V51C_IT.md).

V51C supera i gate strategici su sei casi di sviluppo e quattro casi di
validazione, due seed nuovi per entrambi i posti. Delta medi di sviluppo:
cash +345, PASS −53, MOVE −34,33. Delta medi di validazione: cash +64,50,
PASS −45,50, MOVE −61. Servizi e deficit biologici invariati nella validazione.
Il seed 260909201 peggiora (cash −164, PASS +15) in entrambi i posti;
260909202 migliora (cash +293, PASS −106). Non è un beneficio uniforme.
Il runtime standard seriale passa in entrambi i posti: 719 azioni identiche
al replay, overage 32,75 e 44,93 secondi entro il budget di 60. V51C è quindi
candidata locale verificata, non pubblicata. Evidenza nel
[report finale](reports/pass_reduction_v51/REPORT_V51_IT.html).

Il controllore pianifica dopo il riscontro delle azioni precedenti e prima
della scelta delle nuove missioni. Solo D29, con almeno un aiutante osservato,
le visite FEED, CARE, WATER e HARVEST sono inserite in percorsi completi.
Ogni percorso è una sola missione attiva: contiene i prelievi esatti per tutte
le visite, le mosse e l'eventuale scarico richiesto dalla policy ereditata.
Le azioni sono confermate dalle osservazioni attraverso il controllore esistente.

Il packing usa le scorte osservate meno le risorse già impegnate, assegna
l'inventario trasportato solo al suo lavoratore, esclude dalla nuova capacità
i lavoratori attivi e mantiene un turno di margine. Le destinazioni ancora
contenute nelle missioni impegnate vengono escluse dalle offerte successive.
Le attività facoltative restano al dispatcher ereditato nei posti liberi.

La revisione A perde le irrigazioni prima del raccolto quando incontra il
ripiego HARVEST della stessa destinazione. La B conserva la visita completa.
La C aggiunge il dimensionamento dei nuovi aiutanti per le sole visite residue,
con lo stesso packing e senza assumere acquisti futuri. Il numero trovato
non autorizza azioni dei nuovi aiutanti prima della loro presenza osservata.

Limiti: algoritmo greedy, nessuna prova di ottimalità; gli input e gli output
sono osservati ma i prezzi successivi possono variare. Il rientro segue il
criterio della baseline, incluso il trasferimento notturno quando ammesso.
L'ammissione di crescita e attività facoltative resta ereditata e va verificata
nei replay completi. Migliorare il packing non dimostra da solo una maggiore
redditività o la riduzione dei PASS.

[Protocollo e gate](reports/pass_reduction_v51/PROTOCOL_IT.md).
