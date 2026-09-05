# MODEL_SPEC Codex E18.11 — 7-7-0 invalid-command WATER recovery

## Ipotesi

Il benchmark 7-7-0 con i top e la diagnosi passiva di E18.10 V2 indicano che
non restano opportunità incrementali `PASS→WATER` fuori dal guard protetto.
Restano invece in media 15 worker-turn per partita in cui un worker è già su
una Strawberry viva, secca e senza resa, ma il provider emette un comando
locale sicuramente ineseguibile: 10 `FERTILIZE` senza fertilizzante, 3
`HARVEST` senza resa, 1 `PLACE` su pianta e 1 `PLANT` su cella occupata.

E18.11 converte esclusivamente questi comandi in `WATER`. Non introduce MOVE,
non ritarda MOVE, non cambia PASS, market, topologia, cap, fill o calendario.
Le quattro celle di accesso allo shed sono escluse e un target già assegnato a
WATER nello stesso turn non viene duplicato.

## Controllo e gate

Il controllo diretto è E18.10 V2. La matrice usa i sette seed development e
entrambi i seat; holdout e final restano intatti. Gate A richiede:

- topologia/fill esatti `7-7-0` e safety non peggiore del controllo;
- zero override di comandi fattibili e zero route/market/cap mutation;
- attivazione in tutti i match;
- WATER almeno `+1%` e crop service almeno `+0,5%`;
- late unwatered almeno `-1%`, harvest e unità non inferiori;
- MOVE non superiore, money medio non sotto `-2%`, worst matched almeno `-5%`.

Gate B conserva i target assoluti di convergenza al benchmark Top-3. Nessun
upload Kaggle è autorizzato da questa specifica.

## Esito development gate — 2026-09-04

Gate A e Gate B falliscono. Le 168 conversioni in 14 match sono meccanicamente
sicure (`FERTILIZE` 112, `HARVEST` 42, `PLANT` 14), ma non modificano il
lifecycle: money identico a `65.220,07`, WATER `+0,97%`, crop service
`+0,32%`, late unwatered, harvest e unità invariati. Anche PASS peggiora da
`849,00` a `852,00`.

La variante è quindi respinta: recuperare comandi localmente invalidi aumenta
il contatore WATER, ma non genera output. E18.10 V2 resta il controllo.
