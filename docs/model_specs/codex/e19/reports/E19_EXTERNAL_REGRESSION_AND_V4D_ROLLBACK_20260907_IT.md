# Regressione E19 e ripristino E18.2 V4D

Il proprietario richiede di ripubblicare invariata
`submission/submission_codex_e18_2_capacity_governed_v4d.py`, verificare
i risultati e poi rivalutare la direzione di sviluppo. File SHA256:
`c5fb1fc4966b81f238cdd0de4ca5e15b16ea6b8ae077a08ecc881f8729fd01f7`.
Il file non presenta differenze rispetto al checkout Git. Nessuna modifica
al controller è stata inserita nella nuova submission.

## Risultati verificati prima del ripristino

Kaggle mostra E19 V2 Complete, score 697,2; vecchia E18.2 V4D Complete,
score 1162,9; E18.32 V9 879,5; E18.31 872,7. Sono rating osservati nello
stesso momento, non ricavi né percentuali di rendimento. La nuova V4D deve
essere valutata separatamente: ripubblicare non garantisce lo stesso rating.

Il problema competitivo E19 era già presente nel gate locale:

| Avversario | V/P/S E19 | Cassa E19 media | Cassa avversario media |
|---|---:|---:|---:|
| E18.16 | 0/0/14 | 73.210,57 | 109.160,57 |
| E18.2/V4D | 0/0/14 | 63.486,86 | 117.808,00 |

Il +7,760% rispetto alla 770 con lo stesso core era un confronto fra due
controller deboli. Il superamento di topologia, sicurezza e parità non
costituiva evidenza sufficiente di competitività. Il segnale di 28 sconfitte
su 28 avrebbe dovuto pesare di più nella decisione di pubblicazione.

La cronologia esterna E19 mostra vittorie e sconfitte, quindi il solo rating
non prova un crash sistematico. Non è ancora stato raccolto e analizzato
un corpus esterno completo: non attribuire il divario a specifici errori
di mercato, servizio o generalizzazione senza replay e contabilità.

## Direzione da studiare prima di altre submission sperimentali

1. Conservare V4D come riferimento competitivo e verificare la nuova
   elaborazione, le prime partite e la posizione effettiva in classifica.
2. Ricostruire da replay comparabili dove E19 perde cassa rispetto a V4D:
   avvio D1–D10, acquisti e impieghi del capitale, mix produttivo, rese
   raccolte/vendute, FEED/CARE/WATER mancati, movimenti e PASS, chiusura.
3. Parametrizzare progressivamente la V4D, con parità comportamentale come
   primo obiettivo. Cambiare un solo meccanismo per volta e usare ablation
   verificabili; non riscrivere di nuovo tutto il core sulla base del rating.
4. Adottare un gate competitivo contro V4D e un pannello diversificato,
   includendo entrambe le posizioni e un campione non usato per tuning.
   Sicurezza e parità restano condizioni necessarie, non criterio di promozione.

La ricevuta aggiornata del ripristino è
`artifacts/derived/E18_2_V4D_RESUBMISSION_20260907.json`.

## Esito tecnico della nuova submission

Kaggle **Complete**, score iniziale **600,0**. La cronologia mostra una sola
partita seed 0, esplicitamente etichettata Validation, tra due agenti dello
stesso proprietario. Non sono ancora visibili partite classificate della
nuova submission: validazione superata non significa recupero di rating.
Posizione osservata prima dell'elaborazione: **4316**, score **697,2**.
