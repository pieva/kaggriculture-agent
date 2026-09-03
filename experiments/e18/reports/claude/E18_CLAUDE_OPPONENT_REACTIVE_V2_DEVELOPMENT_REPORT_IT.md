# E18 — Claude opponent-reactive V2: report di remediation

- **Data:** 2026-09-03
- **Candidata:** `CLAUDE-E18.2-OPPONENT-REACTIVE-V2`
- **Ruolo epistemico:** `DEVELOPMENT_ONLY_NON_QUALIFYING`
- **Predecessore:** `CLAUDE-E18.1-OPPONENT-REACTIVE-V1`
- **MODEL_SPEC:** `docs/model_specs/claude/MODEL_SPEC_CLAUDE_E18_2_OPPONENT_REACTIVE_V2.md`
- **Sorgente:** `src/agricola/strategy/claude/e18_opponent_reactive_v2.py`
- **Config:** `experiments/e18/configs/claude/CLAUDE_E18_2_OPPONENT_REACTIVE_V2.json`
- **Runner:** `experiments/e18/tools/claude/run_claude_e18_v2_opponent_reactive_dev_matrix.py`
- **Artifact:** `experiments/e18/artifacts/derived/claude/E18_CLAUDE_OPPONENT_REACTIVE_V2_DEV_MATRIX.json`
- **Test:** `experiments/e18/tests/test_claude_e18_opponent_reactive_v2.py` (33/33 PASS)
- **Holdout/final-confirmation:** non consumati. Nessuna submission Kaggle.
  Nessuna modifica al manifest comune.

---

## 1. File concorrenti registrati (non miei, non corretti)

Come richiesto dal prompt, `git status --short` all'apertura del lavoro
mostrava file di altre sessioni già presenti (torneo a quattro agenti,
candidate Codex/Copilot E18.1, pulizia replay grezzi). Dettaglio completo
in MODEL_SPEC V2 Sezione 0. Non è stato toccato nulla di quell'elenco.

## 2. Audit diagnostico (prima di scrivere qualunque fix)

Due seed tracciati giorno per giorno contro Codex E18.1 (V1, prima di
qualunque modifica): `180903001` e `180903003`. Trovate due cause
distinte e verificate, non ipotesi:

1. **Buffer di grano reattivo, non proattivo.** Un `SHEEP` piazzato a D11
   con zero grano in shed (`_wheat_stock_orders` V1 si attivava solo con
   `animal_headcount > 0`, cioè dopo il primo acquisto), rimasto non
   nutrito D11 e D12, fuggito D13.
2. **Nessun limite fra superficie coltivata e capacità di servizio.**
   Fino a 38 tile concorrenti con 10-11 lavoratori, `MOVE` (4.055) circa
   3× la somma di tutte le azioni produttive; un match è collassato a
   `hands=0` per 9 giorni consecutivi con denaro bloccato a `138`.

Dettaglio completo in MODEL_SPEC V2 Sezione 1.

## 3. Modifiche implementate

1. Buffer di grano proattivo: si accumula da quando esiste una struttura
   zootecnica (non da quando esiste già un animale), e un nuovo acquisto
   animale attende che il buffer esista già;
2. coda di emergenza: `BUY_LAND` e `BUY_SEED` sospesi quando un animale
   non è ancora stato nutrito oggi (`HIRE`/grano/`SELL` restano attivi);
3. superficie coltivata limitata a `max_serviceable_crop_tiles_per_worker`
   (default `3,0`) per lavoratore assunto corrente;
4. telemetria economica giornaliera (`raccolto`, `venduto`, inventario
   residuo, tile servite, backlog, `MOVE`/`PASS`) esposta in
   `telemetry_snapshot()["daily_log"]`.

Layer 1-3 (snapshot D4-D8, classificatore, selettore sticky) e la
decisione lifecycle KEEP/HARVEST/DIG invariati byte-per-byte da V1.
Dettaglio in MODEL_SPEC V2 Sezione 2.

## 4. Matrice di sviluppo (42 match: 7 seed × 2 seat × 3 avversari congelati)

| Avversario | Record | Denaro medio candidata | Denaro medio avversario | Min–max | Run <10.000 | Perdite verificate | Animali di picco medi |
|---|---:|---:|---:|---:|---:|---:|---:|
| Codex E18.1 | 0-14-0 | 7.452,79 | 121.089,86 | 568–10.400 | 13/14 | 12 | 2,71 |
| Copilot E18.1 | 13-1-0 | 15.341,43 | 2.840,00 | 2.075–20.671 | 1/14 | 20 | 1,93 |
| Antigravity E17 | 14-0-0 | 14.357,07 | 0,00 | 1.674–17.740 | 1/14 | 16 | 2,43 |
| **Complessivo** | 27-15-0 | **12.383,76** | — | 568–20.671 | 15/42 | **48** | — |

Zero errori tecnici e zero fallback su tutti i 42 match.

### 4.1 Confronto con V1 sugli stessi tre avversari (torneo a quattro, riferimento)

| | V1 (torneo comune) | V2 (questa matrice) | Delta |
|---|---:|---:|---:|
| Denaro medio complessivo | 6.467,48 | 12.383,76 | **+91,5%** |
| vs Codex E18.1 | 3.763,64 | 7.452,79 | **+98,0%** |
| vs Copilot E18.1 | 7.194,07 (12-2) | 15.341,43 (13-1) | **+113,3%** |
| vs Antigravity E17 | 8.444,71 (14-0) | 14.357,07 (14-0) | **+70,0%** |
| Perdite zootecniche verificate | 31 | **48** | **peggiorato** |

Il livello economico migliora in modo sostanziale e consistente su tutti
e tre i matchup — non un solo seed fortunato. Ma le perdite zootecniche
**peggiorano**, non migliorano: il fix del buffer di grano risolve il
gap di stock iniziale (verificato: la stessa causa isolata nell'audit non
si ripresenta più identica), ma non la servibilità continuativa per
tutta la partita, specialmente quando l'avversario è debole
(Copilot/Antigravity: crescita di cassa più rapida → acquisti animali più
frequenti → più esposizione allo stesso rischio residuo per capo). I
picchi di animali restano piccoli (1,9-2,7 medi): non è un problema di
scala del gregge, è un problema di affidabilità del servizio per singolo
capo che il buffer di grano da solo non risolve.

## 5. Gate

```text
TECHNICAL_GATE: PASS
SAFETY_GATE: FAIL
DYNAMIC_GATE: FAIL
ECONOMIC_GATE: FAIL
PROMOTION_RECOMMENDATION: ITERATE
```

**TECHNICAL_GATE — PASS.** Zero errori tecnici, zero fallback, zero
azioni non valide su 42/42 match; 33/33 test unitari passano, incluse
tutte le fixture di remediation richieste.

**SAFETY_GATE — FAIL.** `verified_livestock_losses = 48` (richiesto: `0`
in 42/42). Peggiora rispetto ai 31 di V1 sullo stesso pool di avversari,
nonostante il fix del buffer di grano sia verificato causalmente
sull'audit originale. Vedi Sezione 4.1 per l'analisi del perché.

**DYNAMIC_GATE — FAIL.** Due regimi realmente attivati
(`LOW_PRESSURE_BALANCED` contro Copilot/Antigravity,
`HIGH_PRESSURE_WHEAT_TEMPO` contro Codex), una decisione per run in
`42/42`, divergenza di action stream condizionata `14/14` (soglia
richiesta `≥12/14`, superata). Ma la divergenza di architettura
condizionata è `11/14`, sotto la soglia richiesta `≥12/14`: il gate
dinamico complessivo non passa per questo solo sotto-controllo.

**ECONOMIC_GATE — FAIL.** Milestone M1 non raggiunta: media complessiva
`12.383,76` (richiesto `≥16.000`) e il matchup contro Codex E18.1 resta
sotto `10.000` di media (`7.452,79`, richiesto nessun matchup sotto
quella soglia). M2 (`≥25.000`) non raggiunta a maggior ragione. Gap dal
target `100.000`: `87.616,24`.

**PROMOTION_RECOMMENDATION — ITERATE.** Miglioramento economico reale e
verificato su tutti e tre i matchup (non un artefatto di un seed), causa
delle due lacune originali diagnosticata e corretta con verifica
puntuale sull'audit. Ma la sicurezza zootecnica è peggiorata in
aggregato ed è un gate esplicitamente più importante del denaro
("Una media alta non compensa una perdita animale o un gate dinamico
fallito"): non promuovibile. Non `REJECT` perché non c'è evidenza di un
difetto architetturale irrecuperabile — anzi, l'architettura a 5 livelli
resta solida (divergenza di azioni 14/14, due regimi, zero errori) — e il
miglioramento economico è reale, non un collasso nascosto da una media
favorevole.

## 6. Prossimi passi consigliati, in ordine

1. **Servibilità continuativa, non solo stock iniziale.** Il buffer di
   grano risolve il gap alla prima acquisizione ma non spiega perché un
   gregge piccolo (1,9-2,7 capi di picco) continui a perdere animali per
   tutta la partita. Serve un audit dedicato — stessa disciplina di
   Sezione 2, non tuning alla cieca — su un match con perdite alte contro
   Copilot/Antigravity (es. seed `180903001` vs `COPILOT_E18_1`, 4
   perdite verificate), per capire se il gap è di distanza dal worker più
   vicino, di priorità competitiva con altri backlog, o di timing
   giorno/notte.
2. **Divergenza di architettura 11/14 → 12/14+:** capire quali 3 gruppi
   seed-seat non divergono e se serve un segnale di regime più sensibile
   o se è varianza attesa vicino alla soglia.
3. **M1 economico:** il gap principale resta contro Codex E18.1
   (`7.452,79` contro `10.000` richiesti); non toccare altre leve finché
   il punto 1 (sicurezza) non è chiuso, per non ripetere l'errore di
   combinare cause non isolate già registrato nel ciclo E17 V4→V5→V6.
4. Non introdurre un terzo regime né altre leve non richieste da questa
   diagnosi.

## 7. SHA-256 di sorgente, config, runner e artefatti

| File | SHA-256 |
|---|---|
| `src/agricola/strategy/claude/e18_opponent_reactive_v2.py` | `4018C844A7EB88FA456461D76C1D5F6F889F5930C13196389F3AA78E0448E4E7` |
| `experiments/e18/configs/claude/CLAUDE_E18_2_OPPONENT_REACTIVE_V2.json` | `B84C2AC415BF095834B34640D10185AD09A0942AC033BAA64630E7A2B2B71C00` |
| `experiments/e18/tools/claude/run_claude_e18_v2_opponent_reactive_dev_matrix.py` | `CA29DC16B352559293288167B53AD4F75439BB33E4D4380906434F8A7A0F0C56` |
| `experiments/e18/artifacts/derived/claude/E18_CLAUDE_OPPONENT_REACTIVE_V2_DEV_MATRIX.json` | `F8045432DB986CF17F13385B2CFACC7FD043743EE2358B4FE9E4D741F259184F` |
| `experiments/e18/tests/test_claude_e18_opponent_reactive_v2.py` | `F17EE0BCCB608000849F2DA570EC8847691FBF1899E347C77B7C51AADF62E60E` |

## 8. Cosa NON è stato fatto

- Nessun seed holdout o final-confirmation consumato (solo i 7 seed di
  sviluppo E18 `180903001`-`180903007`).
- Nessuna submission Kaggle.
- Nessuna modifica al manifest comune (`E18_COMMON_MANIFEST_V1.json`).
- Nessuna lettura di sorgente, config o MODEL_SPEC Codex/Copilot/
  Antigravity; tutti e tre affrontati solo come avversari black-box
  tramite le rispettive factory pubbliche.
- Nessuna modifica a V1 o ai file di altri agenti.
- Nessun terzo regime introdotto.
