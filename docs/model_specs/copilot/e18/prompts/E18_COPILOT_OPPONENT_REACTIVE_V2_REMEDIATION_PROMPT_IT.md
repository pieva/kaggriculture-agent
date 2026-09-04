# Prompt Copilot — E18 opponent-reactive V2

Sei responsabile esclusivamente della linea Copilot E18. Costruisci
`COPILOT-E18.2-OPPONENT-REACTIVE-V2` in nuovi file, senza modificare la V1 o
asset Claude/Codex/Antigravity.

## Prima di modificare

1. Leggi report e artifact del torneo:
   - `experiments/e18/reports/common/E18_FOUR_AGENT_REACTIVE_TOURNAMENT_V2_REPORT_IT.md`;
   - `experiments/e18/artifacts/derived/common/E18_FOUR_AGENT_REACTIVE_TOURNAMENT_V2.json`.
2. Leggi sorgente, config e test Copilot V1.
3. Registra `git status --short`; preserva ogni modifica concorrente. Crea
   source/config/test/report V2 separati e non riscrivere `__init__.py` se non
   strettamente necessario.

## Evidenza che la V2 deve spiegare

- 42 match, 16-26, denaro `2.840` in ogni singola partita;
- 0-14 contro Codex, 2-12 contro Claude, 14-0 contro Antigravity;
- picchi medi di crop, animali e hands tutti pari a zero;
- zero azioni produttive terminalmente osservate, backlog lifecycle 25;
- due etichette (`BALANCED`, `EXPANSION`) ma divergenza delle azioni soltanto
  7/14; architettura 10/14;
- zero errori, fallback e perdite zootecniche;
- quattro rilievi lint V1 da non propagare: import test inutilizzato,
  annotazione quotata e due `SIM102`.

Il selector cambia regime e movimento, ma non attiva una catena economica.

## Ordine di sviluppo obbligatorio

### Gate 0 — compatibilità produttiva

Prima di lavorare sulla reattività, crea smoke test di 720 turni che dimostrino
nel motore reale almeno una catena completa:

`DIG → PLANT → WATER → HARVEST → SELL`

e, se mantieni mixed farming, una catena sicura:

`BUILD → BUY → FEED/CARE → COLLECT/SELL`

Il gate richiede azioni produttive >0, crop di picco >0, denaro diverso dal
valore statico 2.840 e nessun backlog terminale non spiegato. Se fallisce,
fermati e diagnostica il contratto azione/osservazione: non aggiungere logica
di regime.

### Gate 1 — economia autonoma

Costruisci una baseline Copilot V2 funzionante contro inert e Antigravity,
con allocazione persistente dei worker, destinazioni raggiungibili e priorità
su raccolta/vendita. Misura resa per crop tile, movimenti per azione produttiva,
`PASS`, weed, inventory residua e backlog giornaliero.

### Gate 2 — reattività causale

Solo dopo Gate 0-1, applica snapshot pubblico D4-D8 e scelta sticky. I regimi
devono cambiare almeno due leve economiche verificabili — footprint realmente
coltivato e budget workforce/servizio — non soltanto etichetta o traiettoria.
Vieta nome, rating, replay ID, seed e memoria cross-episode.

## Gate di torneo

Usa i soli seed development `180903001`-`180903007`, entrambi i seat, contro
Codex E18.1, Claude E18.1 e Antigravity E17 congelati.

- tecnico: zero errori/fallback e Ruff pulito sui nuovi file;
- produttivo: almeno una catena completa in ogni run e `money_stdev > 0` sul
  pool quando stato/seed differiscono;
- dinamico: ≥2 regimi, una decisione tracciabile, divergenza azioni e
  architettura ≥12/14;
- sicurezza: zero perdite verificate;
- economico M1: media ≥15.000 e nessun matchup sotto 8.000;
- M2 informativo: ≥25.000; target lungo: 100.000.

Non conteggiare come reattività la variabilità casuale o dipendente dal seat.
Fornisci controfattuali a parità di stato iniziale che cambino soltanto lo
snapshot avversario e producano azioni/allocazioni differenti.

## Deliverable

- source e factory V2 autonomi;
- config V2 con soglie motivate dai dati;
- test unitari, smoke test end-to-end e test controfattuali;
- runner 42-match development;
- artifact JSON+CSV, report italiano e SHA-256;
- verdetti separati tecnico/produttivo/dinamico/sicurezza/economico.

Nessuna submission Kaggle, nessun holdout/final, nessuna modifica al manifest
comune.
