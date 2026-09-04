# E17.2 — Piano preregistrato dell'ablation isolata di handoff D27

Stato: `EXECUTED_FROM_PREREGISTRATION / FAIL`

Ruolo epistemico: `DEVELOPMENT_ONLY`

Data: 2026-09-02

## 1. Ipotesi

Anticipare da D28 a D27 l'attivazione del routing state-driven V4D può
aumentare l'adattamento logistico senza ridurre il reward, la sicurezza o
l'efficienza. L'intervento riguarda il giorno di handoff del dispatcher, non
il giorno di sblocco Q2, la topologia o la quota livestock.

## 2. Unica mutazione ammessa

`CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V5-D27` replica i parametri
funzionali di V4D e modifica soltanto:

- `activation_day: 28 → 27`;
- metadati identificativi e causal family.

Il loader rifiuta qualsiasi altra divergenza dalla config V4D congelata.

## 3. Freeze

| Oggetto | SHA-256 |
|---|---|
| sorgente candidata D27 | `38F78316A2CE6E44258C3A972A8FFBE3AF672F07F0883924459A6F4B946CB0D8` |
| config candidata D27 | `028D5F4175DA9757C639C49DAA6CCD58031C94D9C806CE343DB95A0A6B11F717` |
| sorgente controllo V4D | `9350F8B327B972C703136EB6411F03C74B2A80F6A75A9D99C3E4CA614A60B2A4` |
| config controllo V4D | `CA7A6E13CF991185E823325D8220E0682388AC18EB446BB206C0A30ACAB45595` |

## 4. Matrice

- seed development: `26090101`, `26090102`, `26090103`;
- entrambi i seat;
- candidata D27 contro controllo V4D D28;
- opponent: `INERT_PASS_POLICY`;
- 12 episodi, 6 confronti matched;
- nessuna sostituzione di run e nessun seed holdout/final.

Il test inerte isola l'effetto temporale. Un eventuale PASS autorizzerà uno
stress multi-regime successivo, non la promozione diretta a holdout o Kaggle.

## 5. Gate preregistrati

La candidata D27 passa soltanto se:

1. tutti i gate comuni di sicurezza sono verdi;
2. reward medio non inferiore a V4D D28;
3. almeno 4/6 delta matched sono non negativi;
4. il peggior delta percentuale matched è almeno `−2%`;
5. `MOVE/service` non è superiore al controllo;
6. gli action stream divergono in 6/6 coppie, provando l'attivazione causale;
7. il ledger unità della candidata contiene più record del controllo, come
   conseguenza attesa delle 24 ore aggiuntive di routing;
8. il meccanismo post-feed di capacità resta osservabile.

I gate comuni richiedono zero errori, fallback, action shape invalide, fughe,
residui vendibili e violazioni non-SELL, oltre alla copertura 100% dei ledger
unità e mercato.

## 6. Decisione

- `PASS`: D27 può essere sottoposta allo stesso stress dei quattro regimi.
- `FAIL`: D27 viene respinta e V4D D28 resta la candidata interna.

Le soglie non possono essere cambiate dopo l'esecuzione.

## 7. Esito registrato

La matrice è stata completata (`12/12`). Sicurezza e attivazione passano, ma
reward e robustezza matched falliscono: media `−1,337%`, delta negativi `6/6`.
D27 non accede allo stress multi-regime e V4D D28 resta la candidata interna.
