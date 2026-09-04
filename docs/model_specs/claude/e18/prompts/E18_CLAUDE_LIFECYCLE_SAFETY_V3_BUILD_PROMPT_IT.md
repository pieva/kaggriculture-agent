# Prompt Claude — E18 lifecycle e sicurezza zootecnica V3

Sei responsabile esclusivamente della linea Claude E18. Costruisci una nuova
candidate `CLAUDE-E18.3-LIFECYCLE-SAFETY-V1` a partire da V2, senza
modificare o riscrivere V1, V2, file Codex/Copilot/Antigravity o submission
esistenti. Crea soltanto nuovi path V3 nel namespace Claude.

## Prima di modificare

1. Leggi integralmente:
   - `experiments/e18/reports/common/E18_CLAUDE_COPILOT_ANTIGRAVITY_TOURNAMENT_V1_REPORT_IT.md`;
   - `experiments/e18/artifacts/derived/common/E18_CLAUDE_COPILOT_ANTIGRAVITY_TOURNAMENT_V1.json`;
   - `experiments/e18/reports/common/E18_CLAUDE_COPILOT_CANDIDATE_INTAKE_IT.md`
     (requisito lifecycle originario, ancora valido);
   - `docs/model_specs/claude/e18/reports/E18_CLAUDE_OPPONENT_REACTIVE_V2_DEVELOPMENT_REPORT_IT.md`;
   - `docs/model_specs/claude/MODEL_SPEC_CLAUDE_E18_2_OPPONENT_REACTIVE_V2.md`;
   - sorgente, config e test Claude V2 (`src/agricola/strategy/claude/e18_opponent_reactive_v2.py`).
2. Esegui `git status --short` e registra nel report i file concorrenti già
   presenti. Non correggerli, non ripristinarli e non attribuirli a errori
   della tua sessione.

## Evidenza che la V3 deve spiegare

Dal torneo Claude/Copilot/Antigravity (42 match, 7 seed development,
entrambi i seat, Codex escluso di proposito):

- Claude V2 chiude `27-1-0`, media `14.236,36`, range `1.063–21.029`;
- contro Antigravity: `13-1-0`, media `13.567,50` (delta +5.159,43);
- contro Copilot: `14-0-0`, media `14.905,21` (delta +14.645,21);
- **`verified_livestock_losses = 24` su 28 match** — il check di sicurezza
  fallisce nonostante il vantaggio economico; non è compensabile con una
  media alta;
- un solo regime attivato (`LOW_PRESSURE_BALANCED`): il layer
  opponent-reactive resta inerte contro avversari deboli, comportamento
  atteso, non un difetto da correggere in questa iterazione;
- `peak_crops_mean = 24,61`, più basso di Antigravity (32,07) a parità di
  vittorie: margine di crescita sulla superficie coltivata utile, non
  soltanto sulla sicurezza.

Dal requisito lifecycle mai chiuso (intake Claude/Copilot, ancora valido):
manca `KEEP/HARVEST/DIG/REPLANT` sulle piante vive, non si usa
`max_lifespan_step`, si raccoglie appena `yield_units > 0` senza target di
resa, lo shutdown è a soglia fissa di cinque giorni residui.

## Obiettivo causale

Conserva i cinque livelli pubblici di V2 (snapshot D4-D8, regime sticky,
ledger animali, coda di emergenza, telemetria giornaliera) e aggiungi due
meccanismi indipendenti, senza toccare il selector di regime:

1. **Lifecycle esplicito sulle piante vive**: decisione `KEEP/HARVEST/DIG/
   REPLANT` per ogni tile coltivata, basata su `max_lifespan_step` osservato
   e su un target di resa per harvest (non semplice `yield_units > 0`).
   Fixture obbligatoria: `late Strawberry → DIG → Wheat → WATER → HARVEST`.
   Nessuna pianta fuori servizio urgente deve convertirsi in weed
   (`starved_to_weed = 0` nelle fixture); resa media Wheat per harvest
   almeno 3,5 nel micro-benchmark.
2. **Chiusura della fuga zootecnica osservata in questo torneo**: usa
   l'audit già previsto in V2 (ledger giornaliero per animale/struttura) per
   isolare la causa esatta delle 24 perdite su 28 match — non un tuning
   cieco delle soglie. Riproduci la perdita su almeno due seed
   rappresentativi prima di correggere, poi dimostra `0/28` sugli stessi
   seed.

Non introdurre un terzo regime né logica di osservazione avversario
aggiuntiva: l'obiettivo è chiudere lifecycle e sicurezza a parità di
architettura reattiva.

## Gate obbligatori

Esegui soltanto i sette seed development E18, entrambi i seat, contro
Copilot E18.2 e Antigravity E18.1 (gli stessi avversari di questo torneo).
Holdout e final confirmation restano vietati.

- tecnico: zero errori, fallback e azioni non valide;
- **sicurezza: `verified_livestock_losses == 0` in 28/28** — gate bloccante,
  non negoziabile;
- lifecycle: `starved_to_weed = 0` nelle fixture, resa media Wheat ≥3,5,
  invarianti 6-6-2 e zero fughe per le linee mixed-farming;
- economico M1 informativo: media ≥16.000, nessun matchup sotto 10.000;
- efficienza: nessun inventario vendibile terminale materiale; report di
  `productive_actions`, movimenti, `PASS`, backlog e weed per matchup.

Una media economica alta non compensa una perdita animale residua.

## Deliverable

- nuovo source V3 e factory callable;
- config JSON V3;
- MODEL_SPEC V3;
- test unitari e fixture end-to-end (incluse le fixture lifecycle e la
  riproduzione delle 24 perdite prima/dopo il fix);
- runner development riproducibile contro Copilot E18.2 e Antigravity
  E18.1;
- artifact JSON+CSV e report italiano con SHA-256;
- verdetti separati `TECHNICAL`, `SAFETY`, `LIFECYCLE`, `ECONOMIC` e
  decisione finale `ITERATE/REJECT/PROMOTE`.

Non creare submission Kaggle, non usare holdout/final e non modificare il
manifest comune: consegna asset autonomi per il prossimo torneo.
