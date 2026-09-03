# Prompt Claude — E18 opponent-reactive V2

Sei responsabile esclusivamente della linea Claude E18. Costruisci una nuova
candidate `CLAUDE-E18.2-OPPONENT-REACTIVE-V2` partendo dall'evidenza del torneo
a quattro, senza modificare o riscrivere V1, file Codex/Copilot/Antigravity o
submission esistenti.

## Prima di modificare

1. Leggi integralmente:
   - `experiments/e18/reports/common/E18_FOUR_AGENT_REACTIVE_TOURNAMENT_V2_REPORT_IT.md`;
   - `experiments/e18/artifacts/derived/common/E18_FOUR_AGENT_REACTIVE_TOURNAMENT_V2.json`;
   - `experiments/e18/reports/claude/E18_CLAUDE_OPPONENT_REACTIVE_V1_DEVELOPMENT_REPORT_IT.md`;
   - `docs/model_specs/claude/MODEL_SPEC_CLAUDE_E18_1_OPPONENT_REACTIVE_V1.md`;
   - sorgente, config e test Claude V1.
2. Esegui `git status --short` e registra nel report i file concorrenti già
   presenti. Non correggerli, non ripristinarli e non attribuirli a errori
   della tua sessione.
3. Crea soltanto nuovi path V2 nel namespace Claude. Il commento storico su
   `MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE_V6.md` non autorizza alcuna modifica a
   quel file o al relativo report di rifiuto.

## Evidenza che la V2 deve spiegare

- V1 nel torneo comune: 42 match, 26-16, media `6.467,48`, range
  `34-16.593`, 31 perdite zootecniche verificate;
- contro Codex: `3.763,64`, 0-14;
- contro Copilot: `7.194,07`, 12-2;
- contro Antigravity: `8.444,71`, 14-0;
- due regimi realmente attivati; divergenza azioni 14/14 e architettura
  14/14; zero errori e fallback;
- output terminale medio: 2,93 animali, 0,29 crop, 4,17 weed;
- il selector funziona, il servizio e la monetizzazione no.

## Obiettivo causale

Conserva i cinque livelli pubblici della V1 e modifica soltanto i meccanismi
necessari a chiudere due cause: perdita di animali già posseduti e incapacità
di convertire il lavoro agricolo in ricavo. Non aggiungere un terzo regime.

Implementa:

1. un ledger giornaliero per ogni animale/struttura con distanza dal worker,
   scadenza di `FEED/CARE`, task prenotato ed esito; nessun acquisto se il
   servizio dell'esistente non è garantito;
2. una coda di emergenza che prevarica espansione e crop quando un animale è
   a rischio, con fixture che riproducano le perdite V1;
3. telemetria denaro e resa per giorno: raccolto, venduto, inventory residua,
   crop tile servite, backlog, movimenti e `PASS`;
4. un audit su almeno due seed rappresentativi per localizzare la prima
   divergenza economica V1→V2; niente tuning cieco delle soglie;
5. lifecycle esplicito `KEEP/HARVEST/DIG/REPLANT`, ma superficie piantata
   limitata alla capacità di irrigazione/raccolta realmente disponibile;
6. mantenimento dello snapshot pubblico D4-D8 e della decisione sticky, senza
   nome, rating, replay ID, seed o memoria cross-episode.

## Gate obbligatori

Esegui soltanto i sette seed development E18, entrambi i seat, contro i tre
avversari congelati Codex E18.1, Copilot E18.1 e Antigravity E17. Holdout e
final confirmation restano vietati.

- tecnico: zero errori, fallback e azioni non valide;
- sicurezza: `verified_livestock_losses == 0` in 42/42;
- causalità: due regimi attivati, una decisione per run, divergenza azioni e
  architettura almeno 12/14;
- economico M1: media complessiva ≥16.000 e nessun matchup sotto 10.000;
- economico M2 informativo: ≥25.000; target lungo: 100.000;
- efficienza: nessun inventario vendibile terminale materiale e report di
  `productive_actions`, movimenti, `PASS`, backlog e weed per matchup.

Una media alta non compensa una perdita animale o un gate dinamico fallito.

## Deliverable

- nuovo source V2 e factory callable;
- config JSON V2;
- MODEL_SPEC V2;
- test unitari e fixture end-to-end;
- runner development riproducibile;
- artifact JSON+CSV e report italiano con SHA-256;
- verdetti separati `TECHNICAL`, `SAFETY`, `DYNAMIC`, `ECONOMIC` e decisione
  finale `ITERATE/REJECT/PROMOTE`.

Non creare submission Kaggle, non usare holdout/final e non modificare il
manifest comune: consegna asset autonomi per il prossimo torneo.
