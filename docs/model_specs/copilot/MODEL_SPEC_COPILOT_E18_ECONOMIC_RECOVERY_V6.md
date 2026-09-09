# MODEL_SPEC Copilot E18 — Economic Recovery V6

```text
AGENT_OWNER: COPILOT
MODEL: Copilot E18 economic recovery V6
VERSION: COPILOT-E18.10-ECONOMIC-RECOVERY-V6
STATUS: DRAFT / NEXT CANDIDATE
FOUNDATION_BASELINE: C2.1 reconciled
ROUND: E18
IMPLEMENTATION: src/agricola/strategy/copilot/e18_economic_recovery_v6.py
```

## 1. Obiettivo

La nuova candidate prende il punto di blocco osservato nel report di confronto con Codex V48: il loop di colture è stabile ma troppo chiuso e non scala verso redditività e resistenza di lungo periodo. La linea V6 introduce tre correzioni deliberate:

1. buffer di liquidità più ampio prima di fare investimenti di scala;
2. riordino delle semine in batch più robusto per mantenere il throughput senza crollare in `PASS` o in cash starvation;
3. gate di livestock dopo aver raggiunto una soglia minima di stabilità economica e presenza di pascoli disponibili.

## 2. Ipoesi di sviluppo

- La criticità principale del V5 non è un singolo bug tecnico, ma il fatto che il candidato ha raggiunto un plateau di coltivazione senza mai trasformare il cash in scala di produzione.
- Il divario del report mostra che il V5 arresta la crescita intorno a 11–12 tile coltivate, senza quasi mai costruire un patrimonio animale o una struttura di scala.
- Per questo la V6 aggiunge un gating esplicito: prima di comprare animali, si richiede che il denaro superi un `cash_buffer` e che ci siano pascoli liberi.
- La scelta del crop continua a essere dinamica, ma con un punteggio che tiene conto del rapporto prezzo / costo / maturazione, per evitare di fissarsi solo su un crop ad hoc.

## 3. Decisioni implementate

- `BUY_SEED` in batch (`seed_batch`) invece di 1 unità per volta.
- `HIRE` leggermente più aggressivo nelle prime giornate (`hire_target = 3`, `early_hire_days = 4`).
- `SELL` delle produzioni mature quando il prezzo è noto.
- `BUY_ANIMAL` solo dopo `livestock_day` e solo se ci sono pascoli vuoti e il cash supera il `cash_buffer`.
- Priorità di task: `DIG` > `HARVEST` > `WATER` > `PLANT`, con assegnazione per vicinanza al farmer e alle hands.

## 4. Files

- runtime: `src/agricola/strategy/copilot/e18_economic_recovery_v6.py`
- config: `docs/model_specs/copilot/e18/configs/COPILOT_E18_10_ECONOMIC_RECOVERY_V6.json`
- test: `docs/model_specs/copilot/e18/tests/test_copilot_e18_economic_recovery_v6.py`

## 5. Stato

La candidate è un draft di sviluppo: mira a migliorare il loop economico piuttosto che a proclamarsi già vincente. Il passaggio successivo utile è il benchmark locale con seed multiple per valutare se il gating di livestock e l’aumento di batch di semi producono un vero recupero di cassa nel D10–D20.
