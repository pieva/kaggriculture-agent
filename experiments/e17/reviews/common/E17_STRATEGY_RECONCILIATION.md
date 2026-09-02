# Reconciliation delle review strategiche E17

- **Data:** 2026-09-02
- **Integration owner:** Codex
- **Review disponibili:** `3/3`
- **Verdetto:** `RECONCILED / FREEZE_AUTHORIZED`

## Verdetti indipendenti

| Agente | Verdetto | Correzioni richieste |
|---|---|---:|
| Antigravity | `ACCEPT_WITH_CHANGES` | 3 |
| Codex | `ACCEPT_WITH_CHANGES` | 6 |
| Copilot | `ACCEPT_WITH_CHANGES` | 8 |

Nessuna review respinge l'impianto causale. Tutte approvano: nessun archetipo
preselezionato, effetti principali prima delle interazioni, replay Top 3 usati
solo per discovery, seat bilanciati, seed preregistrati, ledger prima della
policy e gate di indipendenza prima del torneo.

## Decisioni riconciliate

### Ledger

Sono recepite tutte le richieste convergenti:

- schema `E17_LEDGER_V1`, serializzazione JSON canonica e fingerprint versionati;
- `command_id`, `batch_index`, `action_batch_sha256` e step osservato;
- denominatore pari a tutti i comandi emessi, incluso `PASS`, senza contare
  slot/unità privi di comando;
- `EXECUTED` solo con effetto attribuibile, `NOT_EXECUTED` solo con evidenza
  negativa, altrimenti `UNKNOWN`;
- quantità richiesta/eseguita per fill parziali;
- separazione fra record coverage e classified-outcome coverage;
- eventi di fuga EOD registrati separatamente come `DERIVED`.

`LEDGER_RECORD_COVERAGE == 100%` è obbligatorio in E17.0. Il market outcome
coverage deve essere dichiarato senza trasformare gli `UNKNOWN`; il target
100% resta valido soltanto quando dimostrabile con evidenza univoca.

### Seed, opponent e promozione

- E17.0 usa soltanto development seed e contract fixture.
- Holdout e final confirmation restano non consumati nel manifest V1.
- L'opponent passivo è congelato come callable condiviso con source hash.
- Il mirror specifica source/config/routine hash della freeze avversaria.
- Errori restano nel denominatore e non sono sostituibili.
- I gate tecnici sono comuni; target economici e di rating sono agent-local.
- Il target mirror Codex viene rinominato e definito come media del denaro
  finale sui run paired entrambi-seat contro la freeze V9.

### Causalità

Ogni RQ frozen distingue trattamento, invarianti, mediatori ammessi, outcome
primario e stop rule. Acquisto, attivazione e popolamento di Q2 non possono
essere modificati insieme senza dichiararlo come trattamento composito.

### Indipendenza

Sono distinti tre deliverable:

1. `MEASUREMENT_PARITY` per Codex V9 congelata;
2. `NATIVE_BASELINE_CONSTRUCTION` per Antigravity e Copilot dentro E17.0;
3. `POLICY_OPTIMIZATION` da E17.1 in poi, non autorizzata.

Le baseline native non devono essere pari a Codex; devono essere deterministe,
congelate, conformi allo schema e prive di import/copie di deliberazione
altrui. Il torneo indipendente resta chiuso finché almeno due policy non
superano una review di dipendenze e provenance.

## Esito

Le correzioni sono incorporate in:

- `experiments/e17/design/E17_STRATEGY_FROZEN_V1.md`;
- `experiments/e17/manifest/E17_COMMON_MANIFEST_V1.json`.

```text
THREE_AGENT_REVIEWS: 3/3
REQUIRED_CHANGES_RECONCILED: 8/8 famiglie
STRATEGY_STATUS: FROZEN_V1
E17_0_AUTHORIZED: YES
E17_1_AUTHORIZED: NO
POLICY_OPTIMIZATION_AUTHORIZED: NO
```
