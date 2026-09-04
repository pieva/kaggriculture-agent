# E18 — Claude lifecycle-safety V3: report di sviluppo

- **Data:** 2026-09-04
- **Candidata:** `CLAUDE-E18.3-LIFECYCLE-SAFETY-V1`
- **Ruolo epistemico:** `DEVELOPMENT_ONLY_NON_QUALIFYING`
- **Predecessore:** `CLAUDE-E18.2-OPPONENT-REACTIVE-V2`
- **MODEL_SPEC:** `docs/model_specs/claude/MODEL_SPEC_CLAUDE_E18_3_LIFECYCLE_SAFETY_V1.md`
- **Sorgente:** `src/agricola/strategy/claude/e18_lifecycle_safety_v3.py`
- **Config:** `docs/model_specs/claude/e18/configs/CLAUDE_E18_3_LIFECYCLE_SAFETY_V1.json`
- **Runner:** `docs/model_specs/claude/e18/tools/run_claude_e18_v3_lifecycle_safety_dev_matrix.py`
- **Artifact:** `docs/model_specs/claude/e18/artifacts/derived/E18_CLAUDE_LIFECYCLE_SAFETY_V3_DEV_MATRIX.json`
- **Test:** `docs/model_specs/claude/e18/tests/test_claude_e18_lifecycle_safety_v3.py` (13/13 PASS)
- **Holdout/final-confirmation:** non consumati. Nessuna submission Kaggle.
  Nessuna modifica al manifest comune.

---

## 1. File concorrenti registrati (non miei, non corretti)

Dettaglio completo in MODEL_SPEC V3 Sezione 0: riorganizzazione di
repository su larga scala già in corso da altre sessioni all'apertura di
questo lavoro. Non toccato nulla di quell'elenco.

## 2. Audit diagnostico (prima di scrivere qualunque fix)

Il match peggiore del torneo Claude/Copilot/Antigravity (seed `180903002`,
seat 0 vs Copilot E18.2, 4 perdite verificate) è stato tracciato turno per
turno. Due cause distinte e verificate, non ipotesi:

1. **Identità del worker instabile.** Le chiavi `hand:i` erano un indice di
   lista ricostruito ogni turno da `observation["farms"][seat]["hands"]`,
   il cui ordine non è stabile; lo stesso incarico `FEED_NEEDED` saltava
   fisicamente da un worker all'altro turno dopo turno, senza mai
   convergere.
2. **Il timeout di stallo non riconosceva un `PICKUP` bloccato.** Il
   contatore incrementava solo su `PASS`; un worker fermo alla shed a
   riemettere `PICKUP WHEAT` con la shed a zero scorte per un'intera
   giornata non veniva mai riassegnato.

Dettaglio completo in MODEL_SPEC V3 Sezione 1.

## 3. Modifiche implementate

1. `_track_worker_identities`: identità persistente per abbinamento greedy
   alla posizione precedente più vicina (distanza `<=1`), azzerata a ogni
   cambio di giorno insieme a `_assignments`;
2. `PICKUP` trattato come `PASS` ai fini del contatore di stallo
   (`assignment_stall_timeout`).

Layer 1-4 (snapshot D4-D8, classificatore, selettore sticky, lifecycle
KEEP/HARVEST/ROTATION_DIG, buffer di grano proattivo, cap di superficie
coltivata, coda di emergenza) invariati byte-per-byte da V2. Dettaglio in
MODEL_SPEC V3 Sezione 2.

## 4. Matrice di sviluppo (28 match: 7 seed × 2 seat × 2 avversari congelati)

| Avversario | Record | Denaro medio candidata | Denaro medio avversario | Min–max | Run <10.000 | Perdite verificate |
|---|---:|---:|---:|---:|---:|---:|
| Copilot E18.2 | 14-0-0 | 13.279,57 | 260,00 | 9.348–17.521 | 2/14 | 6 |
| Antigravity E18.1 | 14-0-0 | 11.845,43 | 8.239,71* | 8.888–15.162 | 4/14 | 7 |
| **Complessivo** | **28-0-0** | **12.562,50** | — | 8.888–17.521 | 6/28 | **13** |

\* media semplice dei denari avversario riportati nei singoli match.

Zero errori tecnici e zero fallback su tutti i 28 match.

### 4.1 Confronto con il torneo che ha aperto questo ciclo (stessi avversari)

| | V2 (torneo Claude/Copilot/Antigravity) | V3 (questa matrice) | Delta |
|---|---:|---:|---:|
| Perdite zootecniche verificate | 24/28 | **13/28** | **-45,8%** |
| Denaro medio complessivo | 14.236,36 | 12.562,50 | -11,8% |
| Record complessivo | 27-1-0 | 28-0-0 | +1 vittoria |

Il gate di sicurezza migliora sostanzialmente ma non si chiude: le perdite
scendono quasi a metà senza toccare lifecycle, buffer di grano, cap di
superficie o code di emergenza — coerente con una causa isolata nel solo
layer di dispatch. Il denaro medio cala leggermente (-11,8%): atteso e
accettabile, non un regresso nascosto — i due fix rendono più worker
realmente disponibili per compiti di sicurezza (`FEED_NEEDED`) invece di
restare intrappolati su un incarico fantasma o in un loop di `PICKUP`,
riducendo marginalmente il tempo speso su crop/harvest. Nessun matchup
sotto la soglia informativa di 10.000 in media.

## 5. Gate

```text
TECHNICAL_GATE: PASS
SAFETY_GATE: FAIL (migliorato, non chiuso: 13/28 vs 24/28 di V2)
LIFECYCLE_GATE: PASS (fixture invariate da V2, tutte verdi)
DYNAMIC_GATE: INFORMATIVO (un solo regime attivato: avversari deboli, atteso)
ECONOMIC_GATE: INFORMATIVO (12.562,50 medi, M1 16.000 non raggiunta)
PROMOTION_RECOMMENDATION: ITERATE
```

**TECHNICAL_GATE — PASS.** Zero errori tecnici, zero fallback su 28/28
match; 13/13 test unitari passano, incluse le fixture di riproduzione dei
due meccanismi corretti e la regressione end-to-end sul match di diagnosi
(0 perdite verificate, era 4 su V2).

**SAFETY_GATE — FAIL (bloccante, non negoziabile).**
`verified_livestock_losses = 13` su 28 match (richiesto: `0`). Migliora del
45,8% rispetto ai 24/28 del torneo di apertura senza toccare nessun'altra
leva, confermando che le due cause diagnosticate (Sezione 2) erano reali e
distinte. Una terza causa residua è stata tracciata e diagnosticata
(MODEL_SPEC V3 Sezione 5: abbinamento greedy non ottimale sotto
affollamento di worker vicini) ma **non corretta** in questo ciclo, per non
combinare più fix non isolati nello stesso passaggio.

**LIFECYCLE_GATE — PASS.** Le quattro fixture richieste (late Strawberry →
DIG, Strawberry con resa pendente → HARVEST prima di DIG, Wheat non
raccolto al primo yield, Wheat raccolto al target di resa) passano
identiche a V2: il layer non è stato toccato e non è regredito.

**DYNAMIC_GATE — informativo, non un difetto di questa iterazione.** Un
solo regime (`LOW_PRESSURE_BALANCED`) attivato in tutti i 28 match: atteso
contro due avversari classificati come a bassa pressione dal classificatore
(coerente con l'assenza di regime alternativo osservata anche nel torneo di
apertura). Il selector non è nello scope di V3.

**ECONOMIC_GATE — informativo.** Media complessiva `12.562,50`, sotto la
soglia M1 di 16.000 ma senza alcun matchup sotto 10.000 in media (soglia
M1 per-matchup superata). Gap dal target 100.000: `87.437,50`. Non è lo
scope di questa iterazione (safety), ma il calo dell'11,8% rispetto al
torneo di apertura è coerente con il fix, non un regresso indipendente
(Sezione 4.1).

**PROMOTION_RECOMMENDATION — ITERATE.** Miglioramento di sicurezza reale,
verificato causalmente (audit prima del fix, regressione end-to-end dopo),
non un artefatto di un singolo seed. Il gate di sicurezza resta però
bloccante e non è chiuso: non promuovibile. Non `REJECT` perché entrambe le
cause diagnosticate sono state corrette con verifica puntuale e la terza
causa residua è già isolata e descritta, non un'ignoto architetturale.

## 6. Prossimi passi consigliati, in ordine

1. **Matching a costo minimo per l'identità dei worker.** Sostituire
   l'abbinamento greedy per distanza minima con un matching ottimale (es.
   algoritmo ungherese) sulle distanze worker-precedenti↔worker-correnti:
   la causa residua (MODEL_SPEC V3 Sezione 5) è un fallimento di
   abbinamento sotto affollamento, non un problema di soglia.
2. Ripetere la matrice di sviluppo con il fix aggiornato e verificare
   `verified_livestock_losses == 0` in 28/28 prima di considerare il gate
   di sicurezza chiuso.
3. Non toccare lifecycle, buffer di grano, cap di superficie o selector di
   regime finché il punto 1 non è chiuso, per non ripetere l'errore di
   combinare cause non isolate già registrato nei cicli E17 V4→V5→V6 e
   Claude E18 V1→V2.

## 7. SHA-256 di sorgente, config, runner e artefatti

| File | SHA-256 |
|---|---|
| `src/agricola/strategy/claude/e18_lifecycle_safety_v3.py` | `90EF14B8D98BEAE93E59A8CCBD1A6E6516FF92B36D2097E8F0C5E3E701BC05DD` |
| `docs/model_specs/claude/e18/configs/CLAUDE_E18_3_LIFECYCLE_SAFETY_V1.json` | `4F64CB7DC37029D5A7B359A77C14E6A6E786474F09F0DC5528609BC79186F904` |
| `docs/model_specs/claude/e18/tools/run_claude_e18_v3_lifecycle_safety_dev_matrix.py` | `4523A831814D02FE4FE3563EA2DB34C530219C8C79C174494F6B7FA3769338A1` |
| `docs/model_specs/claude/e18/artifacts/derived/E18_CLAUDE_LIFECYCLE_SAFETY_V3_DEV_MATRIX.json` | `1344F495052503D52A43FFF380F894E89B49947193E83A19E5DD4D6A84FC87AF` |
| `docs/model_specs/claude/e18/tests/test_claude_e18_lifecycle_safety_v3.py` | `D6BC9CE5F8B960C695A12CBCC6FEEC8D8488B3F69C2AA3A2E95955485B9BDFCC` |

## 8. Cosa NON è stato fatto

- Nessun seed holdout o final-confirmation consumato (solo i 7 seed di
  sviluppo E18 `180903001`-`180903007`).
- Nessuna submission Kaggle.
- Nessuna modifica al manifest comune (`E18_COMMON_MANIFEST_V1.json`).
- Nessuna lettura di sorgente, config o MODEL_SPEC Copilot/Antigravity;
  entrambi affrontati solo come avversari black-box tramite le rispettive
  factory pubbliche.
- Nessuna modifica a V1, V2 o ai file di altri agenti.
- Nessun terzo regime introdotto; nessuna soglia di config ritoccata.
- Il gate di sicurezza non è stato dichiarato chiuso nonostante il
  miglioramento: la causa residua è documentata, non nascosta.
