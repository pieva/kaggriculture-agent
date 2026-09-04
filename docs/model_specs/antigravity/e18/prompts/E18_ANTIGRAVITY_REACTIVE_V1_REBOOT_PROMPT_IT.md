# Prompt Antigravity — E18 reactive reboot V1

La linea Antigravity E17 è ammessa al torneo soltanto come riferimento
obsoleto. Costruisci una nuova `ANTIGRAVITY-E18.1-REACTIVE-REBOOT-V1` in un
namespace E18 autonomo. Non tentare di promuovere o ritoccare direttamente
`antigravity_e17_native_3q.py`.

## Evidenza bloccante

Nel torneo comune Antigravity ha giocato tutti i round previsti:

- 42 match totali, 14 contro ciascun avversario;
- 21 come P0 e 21 come P1, tutti i sette seed development;
- record 0-42, denaro medio/min/max `0`;
- profilo terminale: zero crop, animali, strutture e hands;
- campioni con 707-716 `PASS`, 1-4 `DIG` e quasi nessun movimento;
- un solo regime dichiarato: `STATIC_CROP_FIRST`;
- zero errori formali, ma incompatibilità operativa col protocollo E18.

Prima di parlare di reattività devi dimostrare che l'agente sa giocare nel
motore corrente.

## Fase A — audit del contratto motore

1. Leggi il runner e almeno due record Antigravity completi nell'artifact:
   - `experiments/e18/tools/common/run_e18_four_agent_reactive_tournament_v2.py`;
   - `experiments/e18/artifacts/derived/common/E18_FOUR_AGENT_REACTIVE_TOURNAMENT_V2.json`.
2. Traccia le prime 96 decisioni e individua perché `DIG` non prosegue in
   `PLANT/WATER/HARVEST/SELL`: schema azione, coordinate, inventario,
   persistenza del task o parsing dell'osservazione.
3. Scrivi una diagnosi riproducibile prima di modificare la strategia.
4. Crea un nuovo adattatore/factory E18; non mascherare eccezioni con `PASS`.

### Gate A obbligatorio

Su tre seed development e entrambi i seat:

- 720 turni completati, zero errori/fallback;
- catena `DIG→PLANT→WATER→HARVEST→SELL` osservata;
- `productive_actions > 0`, crop di picco >0, money >2.840 almeno una volta;
- telemetria coerente tra azioni richieste e azioni accettate dal motore.

Se Gate A fallisce, consegna la diagnosi e fermati. Non implementare selector.

## Fase B — economia indipendente

Raggiunto Gate A, costruisci una policy Antigravity E18 minimale ma completa:
task persistenti, workforce commisurata al backlog, lifecycle esplicito,
vendita tempestiva e controllo weed. Mixed farming è opzionale in questa
fase; se introdotto, richiede zero perdite verificate.

Gate B sui sette seed development contro inert e il vecchio Antigravity:
media ≥10.000, nessun run a zero, inventory vendibile terminale minima e
telemetria di resa/movimenti/`PASS`/backlog.

## Fase C — architettura reattiva

Solo dopo A e B, aggiungi:

- snapshot una tantum D4-D8 della sola farm pubblica avversaria;
- due regimi sticky, ad esempio servizio conservativo ed espansione, che
  cambino footprint e allocazione workforce realmente eseguiti;
- test controfattuali a parità di seed/seat;
- nessun nome, rating, replay ID, seed o stato cross-episode.

Torneo completo contro Codex E18.1, Claude E18.1 e Copilot E18.1 sui sette
seed e due seat:

- zero errori/fallback e, se applicabile, zero perdite zootecniche;
- ≥2 regimi e divergenza azioni/architettura ≥12/14;
- M1 economico ≥15.000; M2 ≥25.000; target lungo 100.000;
- nessun matchup a denaro zero.

## Isolamento e deliverable

Prima di editare, registra `git status --short`. Non modificare file concorrenti
di Claude/Copilot/Codex o l'E17 obsoleto. Crea soltanto:

- source/factory/config Antigravity E18 nuovi;
- MODEL_SPEC con diagnosi del contratto;
- test Gate A, lifecycle e controfattuali;
- runner e artifact development;
- report italiano con SHA-256 e verdetti separati `COMPATIBILITY`,
  `TECHNICAL`, `DYNAMIC`, `SAFETY`, `ECONOMIC`.

Non usare holdout/final, non creare submission Kaggle e non modificare il
manifest comune.
