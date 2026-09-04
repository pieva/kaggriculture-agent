# Prompt Copilot — E18 diagnosi zero-hands V3

Sei responsabile esclusivamente della linea Copilot E18. Costruisci
`COPILOT-E18.3-DISPATCH-DIAGNOSIS-V1` in nuovi file, senza modificare V1, V2
o asset Claude/Codex/Antigravity. Questa iterazione è **diagnostica prima
che correttiva**: non sei autorizzato a introdurre o modificare logica di
regime finché il Gate 0 non passa.

## Prima di modificare

1. Leggi report e artifact del torneo:
   - `experiments/e18/reports/common/E18_CLAUDE_COPILOT_ANTIGRAVITY_TOURNAMENT_V1_REPORT_IT.md`;
   - `experiments/e18/artifacts/derived/common/E18_CLAUDE_COPILOT_ANTIGRAVITY_TOURNAMENT_V1.json`;
   - `docs/model_specs/copilot/e18/prompts/E18_COPILOT_OPPONENT_REACTIVE_V2_REMEDIATION_PROMPT_IT.md`
     (la stessa diagnosi era già stata posta a V1: non è stata chiusa da V2);
   - `docs/model_specs/copilot/e18/reports/E18_COPILOT_OPPONENT_REACTIVE_V2_REPORT_IT.md`;
   - sorgente, config e test Copilot V2
     (`src/agricola/strategy/copilot/e18_opponent_reactive_v2.py`).
2. Registra `git status --short`; preserva ogni modifica concorrente. Crea
   soltanto source/config/test/report V3 separati.

## Evidenza che la V3 deve spiegare

Dal torneo Claude/Copilot/Antigravity (42 match, 7 seed development,
entrambi i seat, Codex escluso di proposito):

- Copilot V2 chiude `0-28-0`, **`money_mean = 260,00` con deviazione
  standard zero su tutti i 28 match**, indipendentemente dall'avversario
  (Claude o Antigravity) e dal seed;
- **`peak_hands_mean = 0,0`**: in nessuna delle 28 partite viene assunta
  manodopera;
- `peak_crops_mean = 1,0`: la coltivazione non decolla in nessun run;
- `unique_action_streams = 21/28`: l'azione non è statica byte-per-byte
  (il selector cambia qualcosa), ma l'esito economico lo è — il blocco è a
  monte del dispatch produttivo, non nella scelta del regime;
- un solo regime dichiarato attivo (`EXPANSION`) nonostante la config ne
  preveda almeno due: la selezione avviene ma non produce nessuna
  conseguenza economica osservabile;
- zero errori, fallback e perdite zootecniche: il blocco non è
  un'eccezione o un crash, è una decisione di dispatch che non converte mai
  in HIRE/PLANT/HARVEST.

Questo è lo **stesso sintomo già diagnosticato su V1** (`money = 2.840` fisso
in ogni singola partita, azioni produttive terminali a zero) che la
remediation V2 doveva chiudere con il Gate 0 "compatibilità produttiva". Il
valore statico è cambiato (`2.840` → `260`) ma il difetto strutturale — zero
conversione in economia reale — è ancora presente. Non ripetere lo stesso
tuning che ha già fallito due volte.

## Ordine di sviluppo obbligatorio

### Gate 0 — perché zero hands (bloccante, priorità assoluta)

Prima di qualunque altro lavoro, istruisci un trace completo di una singola
partita (seed `180903001`, seat 0, vs inert) e rispondi con evidenza
riproducibile a: perché il worker iniziale non viene mai assegnato a un
task che porti a `HIRE`? È un guard economico mai soddisfatto, una
condizione di attivazione del task-scan che non scatta, una priorità che
non viene mai raggiunta, o un errore di lettura dell'osservazione
(coordinate, inventario, farm pubblica)? Scrivi la diagnosi prima di
toccare qualunque soglia numerica.

Smoke test 720 turni richiesto, nel motore reale, con almeno una catena
completa:

`HIRE → DIG → PLANT → WATER → HARVEST → SELL`

Il gate richiede azioni produttive >0, crop di picco >0, denaro diverso dal
valore statico osservato (`260,00`) e `peak_hands_mean > 0` su almeno un
seed. Se fallisce, fermati: non aggiungere logica di regime sopra un
dispatch che non produce mai lavoro.

### Gate 1 — economia autonoma

Solo dopo Gate 0, costruisci una baseline V3 funzionante contro inert e
Antigravity E18.1, con allocazione persistente dei worker, destinazioni
raggiungibili e priorità su raccolta/vendita. Misura resa per crop tile,
movimenti per azione produttiva, `PASS`, weed, inventory residua e backlog
giornaliero.

### Gate 2 — reattività causale

Solo dopo Gate 0-1, riapplica snapshot pubblico D4-D8 e scelta sticky. I
regimi devono cambiare almeno due leve economiche verificabili — footprint
realmente coltivato e budget workforce/servizio — non soltanto l'etichetta.
Vieta nome, rating, replay ID, seed e memoria cross-episode.

## Gate di torneo

Usa i soli seed development `180903001`-`180903007`, entrambi i seat, contro
Claude E18.2 e Antigravity E18.1 (gli stessi avversari di questo torneo).

- tecnico: zero errori/fallback;
- produttivo: almeno una catena completa in ogni run e `money_stdev > 0` sul
  pool quando stato/seed/avversario differiscono — il difetto principale da
  chiudere;
- dinamico: ≥2 regimi realmente attivati con conseguenza economica
  osservabile;
- sicurezza: zero perdite verificate;
- economico M1 informativo: media ≥15.000 e nessun matchup sotto 5.000.

## Deliverable

- source e factory V3 autonomi;
- report di diagnosi Gate 0 con trace riprodotto e causa isolata;
- test unitari, smoke test end-to-end;
- runner development riproducibile contro Claude E18.2 e Antigravity E18.1;
- artifact JSON+CSV, report italiano e SHA-256;
- verdetti separati `DIAGNOSIS`, `TECHNICAL`, `PRODUCTIVE`, `DYNAMIC`,
  `SAFETY`, `ECONOMIC`.

Nessuna submission Kaggle, nessun holdout/final, nessuna modifica al
manifest comune.
