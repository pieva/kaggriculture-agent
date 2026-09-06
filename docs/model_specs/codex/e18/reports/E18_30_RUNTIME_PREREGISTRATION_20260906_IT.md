# E18.30 — preregistrazione integrazione online, 2026-09-06

Prima dei run economici. Parent E18.28 C immutabile; no upload/holdout.

- OFF: delega diretta al parent, 719 batch di parità per ogni smoke.
- RESCUE: pool per WATER già pianificati, già dovuti e a rischio deadline
  (owner assente oppure ETA della sua coda oltre H24, H23 a D30). Nessun
  nuovo obiettivo colturale, acquisto o cambiamento a HIRE/FEED/mix/topologia.
  Solo worker senza inventario e con coda esaurita o gap futuro sufficiente;
  percorso completo incluso ritorno quando rimane lavoro parent nello stesso giorno.
- POOL: stessa RESCUE + missioni isolate di fertilizzante disponibile e non
  già prenotato dal piano. Raccolta, consegna e ritorno se necessario entro H23,
  prenotazione dello shed; conferma inventario e audit motore. Variante distinta
  per non attribuire alla sola redistribuzione il ricavo delle nuove missioni.

Entrambe da D7, dopo H2; non cambiare apertura o espansione delle mucche.
Identità worker (giorno, slot): il motore svuota le hands a ogni refresh e
aggiunge le assunzioni in coda intraday. Il numero previsto non vale come capacità.
Movimento consentito su tutte le tile in-bounds, incluse LOCKED: percorso
ortogonale minimo verificato nel motore, non ipotesi di assenza ostacoli.

Smoke preregistrato: seed 180903001, due seat, avversari E18.16 ed E18.2/V4D,
varianti PARENT/OFF/RESCUE/POOL. Tutti i risultati, inclusi fallimenti, preservati.
Poi gate development sette seed × due seat per la candidata plausibile; soglie
economiche e safety della specifica invariate. HIRE/payroll resta ablation
successiva, non una correzione già attuata né una ragione per tacere le morti crop.

## Seconda tranche: CROP_POOL, dopo il gate V1 e prima dei run V2

POOL V1 supera il gate economico 14/14 (+7456,21 medio) ma non il safety:
permane una fragola morta anche nel parent. Conservati codice V1 e tutti i run.
La causa osservata è PLANT H23 + WATER H24 senza margine per il ritardo di percorso.

CROP_POOL aggiunge al POOL esclusivamente missioni complete per PLANT seguito da
WATER sullo stesso target già previsto dal piano, quando l'ETA dell'owner supera
la deadline giornaliera. Nessun filtro per seed/giorno/coordinata. Il target deve
essere libero (o WEED con DIG incluso), i semi osservati disponibili e non già
impegnati dalle PLANT del batch. Conferma della semina prima della WATER; rimozione
dell'obbligo donor solo dopo conferma osservata. Percorso completo e ritorno
compatibili con il prossimo incarico; nessuna nuova coltura o modifica HIRE/mix.
Corretto anche l'ETA: i cursori già avanzati si proiettano dopo il comando baseline
selezionato, non dalla posizione precedente. Le modalità V1 conservano l'ETA V1.

Verifica prima il caso di regressione e poi tutti i 14 casi development, più il
controllo E18.2/V4D sui due seat del seed smoke. Non sono holdout né evidenza esterna.
Soglie immutate: non promuovere con crop/animal deaths o missioni incomplete.
