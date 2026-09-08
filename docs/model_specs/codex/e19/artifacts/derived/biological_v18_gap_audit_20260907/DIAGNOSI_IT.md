# Audit V18 — pascoli, rinnovi e acqua

Caso180903001 posizione0 riprodotto: sides/KPI/ledger/risultati di entrambi i
partecipanti identici all'originale. Tutte719chiamate complete. Probe aggiuntivo
sulle osservazioni registrate finoD18: azioni identiche, assert per ogni turno.
Nessuna modifica al modello congelato.

## Pascoli

Tutti i sei casi hanno8mucche/4pecore e2pascoli vuoti dopoD11. Il profilo vuole
9mucche/5pecore. Nel caso strumentatoD12H1 cassa libera15.366, opportunità
animali con guadagni stimati positivi; due pascoli candidati (6,3)/(3,2).
A D12:240offerte NEW_ANIMAL nelle chiamate di costruzione delle offerte;
360preparazioni di percorsi animale riuscite, ma zero valutazioni del loro
certificato e zero ammissioni. Sono conteggi di tentativi ripetuti, NON360missioni
fisiche o posti disponibili contemporaneamente. Si fermano nella graduatoria.
NEW_ANIMAL ha rango0; tutti i SERVICE hanno almeno1, le consegne e le semine
brevi consumano le altre opportunità. I PASS residui arrivano senza che sia
riservato uno spazio eseguibile per questo impegno pluriturno. DaD17 la pecora
viene anche esclusa dal vecchio filtro economico; daD23 anche la mucca nel caso.
Quindi la mancanza di guadagno tardiva è successiva al rinvio iniziale.
FEED medio12 D16–D24 è coerente con tutti i12animali esistenti: parte del divario
vs14Top è proprio la mandria incompleta, non alimentazioni mancate dei14animali.

## Grano

Nessuna morte per acqua nella coorteV18. D22 resta1casella in tutti6casi;
aD23 risale3–5. Non è zero letterale ma quasi azzeramento. TraD20 eD22 nel
caso strumentato non si semina. Le raccolte semplici competono con il rinnovo:
SERVICE con priority4 ottiene rango3 (2+1), NEW_ROTATION con priority4 rango2.
A D15 ci sono271offerte ripetute di rotazione ma nessun certificato NEW_ROTATION
nel probe. La raccolta semplice viene favorita; dopo aver liberato la casella,
la semina ritorna un investimento di rango0. Perciò calendario e intenzione
persistente non rendono ancora atomico il rinnovo. Cassa ampiamente positiva.

## Acqua

MedieD15–D23: V18 42,04coltivate/26,81WATER; Top61/46,89. WATER per casella
osservata0,638 vs0,769. Rapporti descrittivi su snapshot giornalieri: differenze
di mix/età e raccolti intragiornalieri impediscono una scomposizione causale.
Minore superficie spiega una parte sostanziale, ma non tutta la differenza.
Nel replay strumentato, riapplicata anche l'ultima azione del giorno:
D16due, D20una eD21tre annuali restano senz'acqua pur soddisfacendo needs_water
nella policy. Altri giorniD15–D23 zero omissioni rispetto a quella regola.
Nessuna morte per acqua; zero morti NON implica massima resa. Il grosso delle
colture non irrigate a fine giornata non è una violazione della regola della
policy: questa tollera un giorno asciutto fuori finestre di resa/bonus. Non
assumere però che la regola sia la strategia ottimale del Top, i cui replay
completi non sono localmente disponibili.

## Conseguenza progettuale

Prima di nuove quote: completamento dei2pascoli come impegno del piano con
slot/input riservati; rinnovo grano HARVEST+PLANT+WATER indivisibile nell'ammissione,
con recupero prioritario se interrotto; controllo finale delle irrigazioni che
incrementano resa/bonus, distinto da quelle di pura sopravvivenza. La versione
non viene corretta in questo audit: prima registrate e provate le cause.
