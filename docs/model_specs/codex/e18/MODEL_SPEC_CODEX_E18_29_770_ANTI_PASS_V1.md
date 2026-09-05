# E18.29 V1 — anti-PASS a missione chiusa

Stato: B non idonea al rilascio per una regressione WATER; prima
preregistrazione conservata. Specifica corrente: V3, assegnazione degli spawn.
Il gate economico B è positivo in 14/14 profili (+5.577,43 medio), ma la
diagnosi del seed180903001 P0 rileva una Wheat morta al refresh D21→D22.
Parent immutabile: E18.28 C, submission 56036993; piano
`artifacts/derived/E18_28_FULL_SEASON_C_PLAN_V1.json`.
Nessuna nuova submission in questa sessione; nessun holdout.

## Ipotesi e perimetro

Nel precedente smoke parent, 1.370/1.558 PASS seguono l'esaurimento della
coda produttiva del singolo worker. Questo non prova che ogni slot sia
recuperabile: D7-D10 WATER/CARE sono già ampiamente pianificati. Un generico
riempimento trasformerebbe PASS in MOVE senza necessariamente creare valore.

Prima famiglia causale: recupero del fertilizzante disponibile e non già
assegnato, con consegna allo shed. Il piano limita la raccolta a 7 in D12,
3 in D16 e zero da D17, pur conservando capacità inutilizzata. Il prodotto
aggiuntivo può essere venduto o sostituire acquisti attraverso il mercato
parent invariato. Non aggiungere contemporaneamente CARE, semine, raccolti
crop anticipati, assunzioni, acquisti o modifiche alle date del piano.

Varianti preregistrate:

- OFF: strumentazione senza trattamento; parità completa con E18.28 C.
- A: missioni aggiuntive soltanto D7-D12.
- B: stessa regola D7-D30, ablation temporale separata.

## Contratto del dispatcher

Agire solo su PASS con nessun task non-PASS residuo nella coda giornaliera
del worker e inventario vuoto. Escludere raccolte ancora assegnate ad altri
worker, comandi emessi nello stesso batch e tile già prenotate. Richiedere
animale e fertilizzante osservati realmente disponibili. Nessun anticipo
del calendario né furto di risorse FEED/WATER.

Prenotare prima di partire l'intera missione: percorso Manhattan al pascolo,
COLLECT_FERTILIZER, accesso shed, DROP, rientro nella posizione iniziale.
Termine entro H23, lasciando H24 libero; D30 H24 è terminale, non eseguibile.
Confermare raccolta e rientro sull'osservazione seguente; abortire e rientrare
se il target non è più disponibile. Non impegnare una nuova missione con
meno slot del costo completo o shed prossimo a saturazione. I DROP devono
esporre quantità osservate al mercato parent, non previsioni del piano.

Restano 770, 14 pascoli, cap 14 animali complessivi, massimo 12 hands più
farmer. Non modificare i file congelati E18.28 né le altre linee agente.

## Gate e criteri

Unit test: OFF, code future, prenotazioni, stato reale, budget completo,
inventario, acknowledgement, consegna/rientro, D30. Smoke seed 180903001,
entrambi i seat, parent/A/B contro E18.16. Solo se positivo e sicuro,
estendere B ai seed development 180903001-180903007 × entrambi i seat.
Controllo avversario E18.2/V4D sul seed 180903001 × due seat.

Misurare denaro finale matched, PASS/MOVE e azioni produttive, fertilizzante
raccolto/venduto/acquistato, cassa per giorno, servizio FEED/WATER, fughe,
residui e missioni incomplete. Parità D1-D6 obbligatoria. OFF deve essere
identico al parent per tutti i 719 batch. Nessun errore, fuga aggiuntiva,
violazione topologica/cap o residuo introdotto. Per selezionare B richiedere
delta economico medio positivo e nessuna regressione matched nel development;
la riduzione dei PASS da sola non è successo. Il controllo E18.2 resta un
test di robustezza, non autorizza automaticamente la promozione.

I risultati, anche negativi, vengono salvati in artefatti E18.29 separati.
Il monitor dell'upload E18.28 e l'allineamento globale restano un workflow
distinto: non includere sviluppi E18.29 incompleti in commit automatici.
