# E18 — torneo di sviluppo Claude/Copilot/Antigravity V1

## Decisione

Nessun candidato è promosso o qualificato: il round robin è puramente
diagnostico, con l'unico scopo di dare ad Antigravity E18.1 (appena uscito
dai Gate A/B di compatibilità motore) un termine di confronto reale contro i
due peer che non aveva mai affrontato, e di indirizzare la prossima
iterazione di ciascuna delle tre linee. Codex è escluso di proposito: resta
il riferimento di livello, non un partecipante di questo giro. Holdout e
final-confirmation non sono stati consumati.

## Protocollo

- partecipanti: `CLAUDE_E18_2` (opponent-reactive V2), `COPILOT_E18_2`
  (opponent-reactive V2), `ANTIGRAVITY_E18_1` (reactive reboot V1);
- 7 seed development (`180903001`–`180903007`), entrambi i seat, 3 coppie,
  `42` match sul motore reale (`kaggle_environments/kaggriculture`);
- target economico locale 100.000 (informativo, non gate di promozione);
- gate applicati sono diagnostici (`DIAGNOSTIC_ONLY_NO_PROMOTION`): zero
  errori/fallback, zero perdite zootecniche verificate, soglia M1 15.000
  informativa.

## Risultati

| Agente | Record | Denaro medio | Min–max | Stdev | Regimi attivati | Perdite zootecniche |
|---|---:|---:|---:|---:|---|---:|
| Claude E18.2 | 27-1-0 | 14.236,36 | 1.063–21.029 | 4.097,13 | `LOW_PRESSURE_BALANCED` | 24 |
| Antigravity E18.1 | 15-13-0 | 9.218,46 | 6.442–12.079 | 1.612,98 | `BALANCED_SERVICE`, `EXPANSION_TEMPO` | 0 |
| Copilot E18.2 | 0-28-0 | 260,00 | 260–260 | 0,00 | `EXPANSION` | 0 |

Nessuno dei tre passa la soglia informativa M1 (15.000). Claude fallisce
inoltre il check di sicurezza `zero_verified_livestock_losses` (24 perdite
su 28 match); Antigravity e Copilot lo superano.

## Testa a testa

| Matchup | Record | Media A | Media B | Delta A |
|---|---:|---:|---:|---:|
| Claude vs Antigravity | 13-1-0 | 13.567,50 | 8.408,07 | +5.159,43 |
| Claude vs Copilot | 14-0-0 | 14.905,21 | 260,00 | +14.645,21 |
| Antigravity vs Copilot | 14-0-0 | 10.028,86 | 260,00 | +9.768,86 |

## Letture causali per agente

**Claude** vince ampiamente (27-1) ma con `peak_crops_mean` più basso di
Antigravity (24,61 contro 32,07) e soprattutto con 24 perdite zootecniche
verificate su 28 match: il vantaggio economico attuale convive con un difetto
di sicurezza attivo, indipendente dal lavoro lifecycle già pianificato. Un
solo regime (`LOW_PRESSURE_BALANCED`) si attiva contro avversari deboli: il
layer opponent-reactive resta inerte in questo contesto, comportamento atteso
e non un difetto di per sé.

**Antigravity** è tecnicamente pulito — zero errori, fallback e perdite,
entrambi i regimi realmente attivati — e batte Copilot 14-0 nonostante sia
appena uscito dal reboot. Il tetto economico resta però basso e stretto
(6.442–12.079): la leva lifecycle di base funziona (coerente con Gate A/B),
il vincolo è throughput/capacità, non correttezza.

**Copilot** mostra `money_mean = 260,00` con **stdev zero** su tutti i 28
match, indipendentemente dall'avversario, e `peak_hands_mean = 0,0`: non
assume manodopera in nessuna delle 28 partite. `unique_action_streams` è
21/28, quindi l'azione non è statica byte-per-byte, ma l'esito economico lo
è — un blocco strutturale early-game a monte di qualunque logica di
regime o lifecycle, e più severo di quanto la V2 (già una remediation della
V1) avesse risolto.

## Artefatti

- `experiments/e18/artifacts/derived/common/E18_CLAUDE_COPILOT_ANTIGRAVITY_TOURNAMENT_V1.json`;
- `experiments/e18/artifacts/derived/common/E18_CLAUDE_COPILOT_ANTIGRAVITY_TOURNAMENT_V1.csv`;
- `experiments/e18/tools/common/run_e18_claude_copilot_antigravity_v1_tournament.py`.

## Prossimi passi

Prompt di sviluppo dedicati per ciascuna linea, con l'evidenza di questo
torneo come punto di partenza obbligato:

- `docs/model_specs/claude/e18/prompts/E18_CLAUDE_LIFECYCLE_SAFETY_V3_BUILD_PROMPT_IT.md`;
- `docs/model_specs/copilot/e18/prompts/E18_COPILOT_ZERO_HANDS_DIAGNOSIS_V3_PROMPT_IT.md`;
- `docs/model_specs/antigravity/e18/prompts/E18_ANTIGRAVITY_CAPACITY_THROUGHPUT_V2_PROMPT_IT.md`.
