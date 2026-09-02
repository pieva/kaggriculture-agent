# MODEL_SPEC — Codex E17.1 3Q Reactive Guarded V1

- **Versione:** `CODEX-E17.1-3Q-REACTIVE-GUARDED-V1`
- **Candidate ID:** `CODEX_E17_1_3Q_REACTIVE_GUARDED_V1`
- **Stato:** FROZEN FOR REACTIVE TOURNAMENT
- **Natura:** derivazione reattiva dichiarata della Codex V9
- **Famiglia causale modificata:** `WHEAT_FEED_SERVICEABILITY`
- **Foundation:** C2.1

## 1. Scopo e non-scopo

La policy conserva la routine 3Q della
`CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY` come provider dell'azione di default.
Non prova a riscrivere colture, topologia, tempi di espansione o logistica. Il
solo obiettivo è recuperare due divergenze osservabili che una schedule
open-loop non può prevedere:

1. acquisto di Wheat richiesto ma non riscontrato nello stato successivo;
2. animale a rischio di fuga all'ultima ora, non già coperto da un `FEED`
   programmato sullo stesso tile.

La reattività non è assunta superiore alla V9. Se nessuno dei due segnali è
presente, il batch emesso deve essere identico al batch V9.

## 2. Contratto runtime

Factory:

```python
from agricola.strategy.codex.codex_e17_reactive_guarded import (
    create_codex_e17_reactive_agent,
)

policy = create_codex_e17_reactive_agent(run_context=None, config_path=None)
action = policy(observation, configuration)
```

Il risultato mantiene lo schema Kaggriculture:

```python
{"farmer": ["PASS"], "hands": [], "market": []}
```

Ogni eccezione ordinaria viene contenuta al confine episodio con un safe
`PASS`; `KeyboardInterrupt` e `SystemExit` non vengono intercettati.

## 3. Collegamento alla Foundation C2.1

La Foundation resta descrittiva e condivisa; non contiene la strategia.

| Artefatto Foundation | Uso nel candidato |
|---|---|
| ontologia | interpreta farm, animali, inventari, mercato e quadranti |
| feature model | deriva Wheat aggregato, fame, feed richiesti, cash e limite ordini |
| macchina a stati | usa clock canonico e transizione fra due osservazioni successive |
| observation contract | valida clock, player binding, configuration e fingerprint |
| ledger E17 | registra i comandi emessi e conserva `UNKNOWN` quando l'esito non è attribuibile |

Non viene reintrodotto `decision_lifecycle`: la decisione è una pipeline
locale `OBSERVE -> DEFAULT -> GUARD -> EMIT -> MEASURE`.

## 4. Stato agent-local

Il candidato conserva solo:

- ultimo acquisto Wheat richiesto;
- Wheat totale prima della richiesta;
- `FEED` e vendite Wheat richiesti nello stesso batch;
- contatori e record degli override;
- errori e fallback.

Non indicizza le azioni per seed o avversario. Il numero di step serve al
clock e alla correlazione fra osservazioni, non come chiave di una nuova
routine.

## 5. Inferenza conservativa del mancato acquisto

Al turno successivo viene calcolato un limite inferiore prudente dello stock
atteso senza l'acquisto:

```text
expected_without_buy =
    wheat_before - feed_requested - wheat_sell_requested

inferred_fill = min(requested_buy,
                    wheat_now - expected_without_buy)
unfilled = requested_buy - inferred_fill
```

Le quantità `FEED` e `SELL` vengono sottratte anche se potrebbero non essere
state eseguite. Eventuali raccolti Wheat non vengono imputati. La stima tende
quindi a non dichiarare una mancata esecuzione in caso di ambiguità.

## 6. Ordine degli override

1. ottenere una copia profonda del batch V9;
2. risolvere l'eventuale acquisto Wheat precedente;
3. individuare animali con `consecutive_unfed >= 1` e `fed_today == false`;
4. sottrarre i tile già coperti da un `FEED` V9;
5. solo a fine giornata, usare un lavoratore già sul tile e dotato di Wheat;
6. solo in presenza di fill shortfall o rischio EOD, proteggere la riserva:
   ridurre una vendita Wheat, aumentare/aggiungere un acquisto e, come ultima
   risorsa, rinviare un acquisto animale;
7. registrare hash before/after, feature e reason code.

Reason code ammessi:

- `CRITICAL_FEED_OVERRIDE`;
- `WHEAT_SALE_REDUCED`;
- `WHEAT_BUY_INCREASED`;
- `WHEAT_BUY_APPENDED`;
- `ANIMAL_PURCHASE_DEFERRED`.

## 7. Parametri congelati

| Parametro | Valore |
|---|---:|
| `feed_reserve_rounds` | 1 |
| `critical_unfed_threshold` | 1 |
| `max_extra_wheat_per_step` | 6 |
| `operating_cash_floor` | 100 |
| `market_fill_tracking` | true |
| `allow_critical_feed_override` | true |
| `allow_animal_purchase_deferral` | true |

La configurazione canonica è
`experiments/e17/configs/codex/CODEX_E17_1_3Q_REACTIVE_GUARDED_V1.json`.

## 8. Invarianti

- sorgente e config della V9 non vengono mutate;
- nessun override fuori dalla famiglia Wheat/feed;
- nessun accesso a decision path avversari;
- nessun seed holdout o final usato nello sviluppo;
- ledger passivo e decisione restano separati;
- un tile già coperto da `FEED` non riceve un override duplicato;
- la spesa aggiuntiva rispetta floor cash, cap per step e limite ordini;
- ogni batch modificato incrementa un contatore e produce provenance.

## 9. Validazione e limiti epistemici

Sui sette seed development e due seat contro `INERT_PASS_POLICY`:

```text
RUNS: 14
MEAN_FINAL_MONEY: 139420.2857
V9_MEAN_FINAL_MONEY: 139420.2857
MEAN_DELTA: 0
MIN_FINAL_MONEY: 77542
MAX_FINAL_MONEY: 181339
TECHNICAL_ERRORS: 0
DERIVED_EOD_ESCAPES: 0
THREE_QUADRANTS: 14/14
LEDGER_RECORD_COVERAGE: 100%
NATURAL_OVERRIDES: 0
```

L'assenza di override contro l'avversario inerte è un risultato desiderato:
dimostra la conservazione della baseline, non l'efficacia competitiva della
guardia. L'attivazione è verificata con test controfattuali sintetici. Il
valore competitivo deve essere misurato nel torneo holdout e non è ancora un
risultato.

Un mirror aggiuntivo development contro la stessa V9 ha prodotto 14 run,
media identica `88576.2857`, delta matched medio zero, zero errori e zero
fughe. Anche qui non sono stati osservati acquisti Wheat parziali: gli unici
esiti non pari (`+68/-68` sullo stesso seed) si invertono con il seat e sono
classificati come seat effect, non come effetto della guardia.
