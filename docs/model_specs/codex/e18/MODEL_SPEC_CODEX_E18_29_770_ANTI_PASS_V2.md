# E18.29 B2 — anti-PASS con priorità del servizio

Esito: REJECTED_BEHAVIORALLY_INERT. Smoke due seat identico a B per tutti i
719 batch: zero FERTILIZE preempted, stessa morte Wheat. Non estesa agli
altri seed né al controllo E18.2. V3 sostituisce questa ipotesi dopo la
traccia esatta degli spawn M11/M12 e dei due MOVE di correzione.

Preregistrazione dopo il gate B, prima del test B2 (2026-09-05).
B migliora tutti i 14 profili economicamente, ma la diagnosi strumentata del
seed 180903001 seat 0 rileva una morte Wheat aggiuntiva: servizio D21,
visibile D22. PLANT slitta a H24; WATER resta oltre la giornata.
Il fertilizzante extra rende eseguibili task prima saltati e consuma il
margine che assorbiva la correzione della posizione iniziale degli hands.

B resta evidenza positiva economica, **non idonea al rilascio per questa
regressione di servizio**. Non confondere WEED H24 con diagnosi di sete:
la morte è stata verificata direttamente nel refresh del motore.

B2 conserva esattamente dispatcher e missioni B. Unica differenza: prima di
FERTILIZE, simula l'orario di completamento della coda restante rispettando
timestamp e distanze dalle posizioni reali. Se non può terminare entro H24
(H23 a D30), salta il boost opzionale lasciando il fertilizzante disponibile.
FEED, WATER, PLANT e gli altri task mantengono l'ordine parent. Nessuna
condizione su seed, seat, coordinate o giorno specifico del difetto.
Il calcolo presume task validi: non è una garanzia contro ogni futuro ritardo.

Gate: unit test del calendario e della priorità, smoke seed 180903001 due
seat contro E18.16; poi stessa matrice development sette seed × due seat,
riutilizzando i parent congelati. Controllo E18.2/V4D seed 180903001 due seat.
Registrare i task FERTILIZE sacrificati e aggiungere l'audit delle morti crop
al refresh su ogni partita. Richiedere zero morti per sete, zero fughe,
cap/topologia/residui/missioni corretti e delta economico positivo in tutti
i casi matched contro E18.28 C. Misurare anche B2−B, senza occultare un costo
della sicurezza. Nessun holdout, nuova submission, commit o push.
