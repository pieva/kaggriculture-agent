# E18.29 B3 — anti-PASS e assegnazione alle posizioni reali

## Esito verificato

B3 è il migliore sviluppo anti-PASS, non ancora candidata al rilascio.
14/14 delta economici positivi contro il parent E18.28 C: cassa media
74.491,57→80.212,57 (+5.721, +7,68%); worst +3.197. PASS medi
1.568,07→1.148,07 (−26,78%), MOVE 3.053→3.299,86 (+8,09%).
FEED/WATER eseguiti e costo personale invariati; fertilizzante raccolto
106,57→170,86, interamente consegnato senza perdite nei DROP.

Lo scambio M11/M12 si attiva una volta per partita e rimuove la regressione
D21 di B: B3−B +143,57 medio. Nessun errore, fuga animale, violazione
770/cap14/max12hands, missione incompleta o stock terminale residuo.
Resta la Sheep mancante ereditata nei profili seed180903007.

Audit crop: 13/14 profili senza morti per sete; seed180903005 seat1 perde
una Strawberry (4,8) al refresh D12→D13. La riesecuzione del parent
conferma lo stesso evento con identici 719 batch al baseline congelato:
difetto ereditato, non regressione. Il gate assoluto zero perdite crop
resta comunque FAIL; non viene cambiato retroattivamente. Prossima
priorità: prenotazione indivisibile PLANT→WATER e acknowledgement in D12.

Controllo E18.2/V4D: parent60.612→B3 67.745 (+7.133, +11,77%) in entrambi
i seat; nessuna morte crop. Sconfitte dirette contro E18.2 2/2. Su E18.16
le vittorie sono 4/14 contro 1/14 del parent: progresso, non dominio.
52 test unitari/regressione superati. Tutti i sorgenti, piani e l'artefatto
E18.28 pubblicato conservano gli hash del manifest. Nessun upload, holdout,
commit/push o pulizia cache in questo sviluppo.

Report: `reports/E18_29_ANTI_PASS_DEVELOPMENT_REPORT_IT.md`.
Riepilogo e provenienza: `artifacts/derived/E18_29_ANTI_PASS_SUMMARY.json`.
Config: `configs/CODEX_E18_29_770_ANTI_PASS_V3.json`.

## Preregistrazione e implementazione

Preregistrata prima del test B3. Supera V2 come candidata, non come evidenza:
B e B2 rimangono conservate. B2 è inerte sullo smoke, con la stessa morte
Wheat: il worker interessato non ha FERTILIZE nella propria coda.

La traccia completa D21 chiarisce il difetto: parent M11 nasce (4,4), mentre
B M11 nasce (5,5) e M12 (4,4). M11 spende H3-H4 per tornare al pickup
nominale; il mangime è disponibile (24 Wheat), non è una carenza di cassa.
I due MOVE spostano DIG/PLANT/WATER oltre la giornata. Il cambiamento dello
stato e dell'occupazione agli accessi shed modifica gli spawn; il piano
nominale non riassegna le code. La precedente spiegazione basata su una
fertilizzazione nella coda M11 è falsificata, non va mantenuta come causa.

B3 usa B senza la guardia FERTILIZE B2. Quando i due ultimi hands sono appena
comparsi, entrambi con coda non iniziata e inventario vuoto, confronta le
due assegnazioni possibili delle loro code complete alle posizioni reali.
Scambia solo se l'identità originale sfora e lo scambio fa terminare
entrambe entro H24 (H23 D30). Tiene fissi task, date, mix, acquisti e
obbligazioni aggregate. Nessun caso speciale per D21, coordinate o seed.
Le righe del piano immutabile non vengono modificate; solo la mappa runtime
delle due code. DROP e pickup continuano a usare il worker fisico osservato.

Test: budget con correzioni di posizione, zero scambio quando entrambe le
code stanno nel budget, blocco dopo avvio o con inventario, idempotenza e
immutabilità del piano. Smoke seed180903001 due seat; se sicuro, altri sei
seed development due seat; E18.2/V4D seed180903001 due seat. Audit crop al
refresh su ogni partita B3, zero morti per sete/fughe/residui/missioni
incomplete, prefix D1-D6 identico e delta positivo contro E18.28 C in tutti
i profili. Misurare B3−B. Nessun holdout o nuova submission.
