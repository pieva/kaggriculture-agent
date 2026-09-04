# E17.2 — Piano preregistrato di stress V4D su regimi di mercato controllati

Stato: `EXECUTED_FROM_PREREGISTRATION / PASS`

Ruolo epistemico: `DEVELOPMENT_ONLY`

Data: 2026-09-02

## 1. Domanda causale

Verificare se il miglioramento di `CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28`
rispetto al controllo `CODEX-E17.2-REACTIVE-SERVICE-ROUTING-CORE-V3-D28`
rimane robusto quando il mercato è sottoposto a pressioni controllate, prima di
autorizzare qualsiasi esperimento con attivazione anticipata a D27.

V4D e V3 restano congelati durante l'intera matrice. Il test non autorizza modifiche
alla policy, uso di seed holdout/final, submission Kaggle, commit o push.

## 2. Freeze

| Oggetto | SHA-256 |
|---|---|
| sorgente V4D/V4 family | `9350F8B327B972C703136EB6411F03C74B2A80F6A75A9D99C3E4CA614A60B2A4` |
| config V4D | `CA7A6E13CF991185E823325D8220E0682388AC18EB446BB206C0A30ACAB45595` |
| sorgente V3 | `80D909104402473503E1945A6F9EE200DF1CEA5ABA9C66B43C5F6A8AA61A6E91` |
| config V3 | `AD2A79602A610D35C2D44F200AEA36B9949F41D1EA67EC43EAB873B007A2EF8D` |
| definizione storica dei regimi E17.1 | `5B80BE31181F9A681D85884C5F62DA0E4208E6219429434885F9CD859857B212` |

## 3. Matrice sperimentale

- seed development: `26090101`, `26090102`, `26090103`;
- seat: `P0`, `P1`;
- policy: V4D candidata, V3 controllo;
- regimi: `INERT`, `WHEAT_SCARCITY`, `OUTPUT_PRESSURE`, `LIQUIDITY_STRESS`;
- totale: `3 × 2 × 2 × 4 = 48` episodi;
- pairing: stesso seed, seat e regime per candidata e controllo;
- sostituzione di run falliti: vietata.

I regimi riusano senza variazioni `MarketRegimeOpponent` di E17.1:

- `INERT`: avversario passivo;
- `WHEAT_SCARCITY`: V9 congelato con acquisto aggiuntivo di 10 Wheat;
- `OUTPUT_PRESSURE`: V9 congelato con vendita dei propri output disponibili;
- `LIQUIDITY_STRESS`: combinazione delle due pressioni precedenti.

Queste sono pressioni di mercato prodotte dall'avversario, non mutazioni dirette
dello stato privato della policy in esame.

## 4. Metriche

- reward e delta matched V4D−V3;
- media e delta percentuale per regime e complessivi;
- quota di casi matched non negativi;
- comandi MOVE, servizi e rapporto MOVE/service;
- trigger di capacità, batch attivi e rilasci post-feed dei carrier Wheat;
- comandi e ledger di unità/mercato;
- errori, fallback, action shape invalide, fughe EOD;
- residuo vendibile terminale e preservazione degli ordini non-SELL;
- tempi di sblocco e struttura finale dei tre quadranti.

## 5. Gate preregistrati

V4D supera lo stress soltanto se tutti i gate seguenti sono veri:

1. tutti i gate comuni di sicurezza sono verdi in ognuno dei quattro regimi;
2. reward medio complessivo V4D non inferiore a V3;
3. reward medio V4D non inferiore a V3 nel regime `INERT`;
4. almeno tre regimi su quattro hanno delta medio non negativo;
5. il peggior delta medio percentuale di regime è almeno `-1%`;
6. almeno il `75%` dei 24 confronti matched ha delta non negativo;
7. MOVE/service complessivo V4D è strettamente inferiore a V3;
8. trigger di capacità e rilascio post-feed sono osservati in tutti i regimi.

I gate comuni richiedono: zero errori tecnici, zero fallback, zero action shape
invalide, zero fughe animali, copertura unitaria dei ledger unità e mercato,
zero violazioni della preservazione non-SELL e zero residui vendibili terminali.

## 6. Regola decisionale

- `PASS`: V4D è ammessa come baseline congelata per il successivo test causale D27.
- `FAIL`: D27 resta bloccato; si documenta il regime e il meccanismo del fallimento.

Nessuna soglia può essere modificata dopo l'esecuzione della matrice.

## 7. Esito registrato

La matrice preregistrata è stata eseguita integralmente: `48/48` episodi,
tutti gli otto gate `PASS`. V4D è quindi ammessa come baseline congelata per
il successivo test causale D27. Il dettaglio è nel report
`docs/model_specs/codex/e17/reports/E17_CODEX_V4D_CONTROLLED_MARKET_STRESS_REPORT_IT.md`.
