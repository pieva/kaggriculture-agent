# Prompt Antigravity — E18 capacità e throughput V2

Sei responsabile esclusivamente della linea Antigravity E18. Costruisci
`ANTIGRAVITY-E18.2-CAPACITY-GOVERNED-V1` a partire dal reboot V1 (Gate A e B
già superati), senza modificare i file V1 o asset Claude/Codex/Copilot.
Crea soltanto nuovi path V2 nel namespace Antigravity.

## Prima di modificare

1. Leggi integralmente:
   - `experiments/e18/reports/common/E18_CLAUDE_COPILOT_ANTIGRAVITY_TOURNAMENT_V1_REPORT_IT.md`;
   - `experiments/e18/artifacts/derived/common/E18_CLAUDE_COPILOT_ANTIGRAVITY_TOURNAMENT_V1.json`;
   - `docs/model_specs/antigravity/e18/artifacts/derived/E18_ANTIGRAVITY_REACTIVE_V1_GATE_A.json`;
   - `docs/model_specs/antigravity/e18/artifacts/derived/E18_ANTIGRAVITY_REACTIVE_V1_GATE_B.json`;
   - `docs/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_E18_1_REACTIVE_REBOOT_V1.md`;
   - `docs/model_specs/codex/e18/reports/E18_2_CAPACITY_GOVERNED_V4D_DEV_REPORT_IT.md`
     (precedente strutturale: stessa leva causale su un'altra linea);
   - sorgente e config V1
     (`src/agricola/strategy/antigravity/antigravity_e18_reactive_reboot_v1.py`).
2. Esegui `git status --short` e registra i file concorrenti già presenti;
   non correggerli né attribuirli a questa sessione.

## Evidenza che la V2 deve spiegare

Gate A (audit contratto motore, 6 run): `PASS` — 720 turni completati,
zero errori/fallback, catena osservata in tutti i run, `productive_actions`
e `peak_crops` positivi, denaro >2.840 almeno una volta.

Gate B (economia indipendente, 28 match contro inert e Antigravity E17):
`PASS` — media `10.712,71`, min `5.971`, max `18.347`, zero errori/fallback,
nessun run a denaro zero.

Nel torneo Claude/Copilot/Antigravity (42 match, 7 seed development,
entrambi i seat, Codex escluso di proposito), il primo confronto reale
contro peer E18 attivi:

- record `15-13-0`, media `9.218,46`, range **stretto** `6.442–12.079`
  (stdev `1.612,98`) — coerente con Gate B, ma il tetto massimo non si
  sposta granché anche nei match vinti;
- **zero errori, fallback e perdite zootecniche verificate**: la base
  lifecycle è corretta e stabile;
- entrambi i regimi realmente attivati (`BALANCED_SERVICE`,
  `EXPANSION_TEMPO`), `unique_action_streams = 22/28`: la reattività di
  base funziona;
- contro Copilot E18.2: `14-0-0`, media `10.028,86` — vince nettamente
  un avversario strutturalmente bloccato, non è un segnale di forza
  economica assoluta;
- contro Claude E18.2: `1-13-0`, media `8.408,07` contro `13.567,50` — perde
  la maggioranza dei match per margine economico, non per errori o crash;
- `peak_crops_mean = 32,07` è **più alto** di Claude (24,61): la superficie
  coltivata non è il collo di bottiglia, la conversione in denaro sì.

La lettura è la stessa del precedente Codex E18.2: correttezza lifecycle e
geometria non bastano da sole a raggiungere un livello economico solido; la
leva mancante è il **controllo di capacità/servizio**, non un nuovo regime
né altra correttezza sulle piante vive.

## Obiettivo causale

Conserva la base V1 (lifecycle, task scan, i due regimi, lo snapshot
avversario) e aggiungi un unico meccanismo nuovo, senza cambiare topologia
né aggiungere un terzo regime:

1. Introduci un **controllo di capacità/servizio locale**: quando un
   worker si trova già sul tile di un task disponibile (crop maturo da
   raccogliere, weed da rimuovere, animale da servire) ma non è il task
   assegnato dal dispatch corrente, permettigli di servirlo **senza
   `MOVE`** e senza alterare gli altri comandi già pianificati — esattamente
   il principio "recovery on-tile-only" validato su Codex E18.2 (righe 13-24
   del suo report), non deviazioni che spostano un worker già impegnato.
2. Misura separatamente l'effetto di questa leva rispetto alla baseline V1:
   stesso seed, stesso seat, con e senza il controllo di capacità attivo,
   per dimostrare che l'incremento economico viene dalla capacità e non da
   varianza casuale.
3. Non toccare selector di regime, snapshot avversario o lifecycle: se il
   controllo di capacità non basta a muovere la media oltre la fascia
   9-12k, documenta il risultato negativo invece di aggiungere altre leve
   nello stesso ciclo.

## Gate obbligatori

Esegui soltanto i sette seed development E18, entrambi i seat, contro
Claude E18.2 e Copilot E18.2 (gli stessi avversari di questo torneo).
Holdout e final confirmation restano vietati.

- tecnico: zero errori, fallback e azioni non valide (invariante già
  raggiunto in V1, non regredire);
- sicurezza: zero perdite zootecniche verificate (invariante già raggiunto);
- causalità: controllo di capacità dimostrato con confronto diretto
  con/senza a parità di seed/seat, non semplice miglioramento medio;
- economico M1 informativo: media ≥15.000, nessun matchup sotto 8.000;
- confronto diretto: media superiore alla baseline V1 (`9.218,46`) in
  almeno 12/14 match contro ciascun avversario.

## Deliverable

- nuovo source V2 e factory callable;
- config JSON V2;
- MODEL_SPEC V2 con la diagnosi capacità/throughput;
- test unitari e fixture per il controllo di capacità on-tile;
- runner development riproducibile contro Claude E18.2 e Copilot E18.2;
- artifact JSON+CSV e report italiano con SHA-256;
- verdetti separati `TECHNICAL`, `SAFETY`, `CAPACITY`, `ECONOMIC` e
  decisione finale `ITERATE/REJECT/PROMOTE`.

Non creare submission Kaggle, non usare holdout/final e non modificare il
manifest comune: consegna asset autonomi per il prossimo torneo.
