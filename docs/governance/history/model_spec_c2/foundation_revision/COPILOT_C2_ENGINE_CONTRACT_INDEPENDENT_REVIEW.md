# COPILOT C2 â€” ENGINE CONTRACT INDEPENDENT REVIEW

```text
AGENT_ID: COPILOT
DOCUMENT_TYPE: INDEPENDENT_ENGINE_CONTRACT_REVIEW
PHASE: REVIEW
TASK_ID: C2-ENGINE-CONTRACT-INDEPENDENT-REVIEW
STATUS: FROZEN â€” SUBMITTED FOR RECONCILIATION
FOUNDATION_MODIFICATION_AUTHORIZED: NO
MODEL_SPEC_MODIFICATION_AUTHORIZED: NO
CODE_MODIFICATION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

## Executive verdict

L'audit di Codex Ã¨ nel complesso un documento utile e `source-grounded` nella sua parte semantica. La maggior parte delle affermazioni critiche alla Foundation correnti Ã¨ verificata dal source runtime: clock, inventory, animal production, fertilizer dynamics e inventory overflow sono coerenti con il codice. Tuttavia, il documento non Ã¨ ancora pronto a fungere da contratto `canonico` senza un correzione di provenance: il fingerprint aggregato atteso non si riproduce con la formula specificata e il manifest dichiarato.

```text
ENGINE_IDENTITY_MATCH: NO
REVIEW_VERDICT: ACCEPT_WITH_CORRECTIONS
```

---

## 1. What is confirmed

### Clock and transition semantics

Confirmed by `kaggriculture.py`:

- `step` is the engine counter and `day = step // turns_per_day` in the interpreter;
- `hour = step % turns_per_day` in the valid current state;
- `next_step = step + 1` and then `obs0.day = next_step // turns_per_day`, `obs0.hour = next_step % turns_per_day`;
- EOD trigger is `if (step + 1) % turns_per_day == 0`;
- `_end_of_day` resets daily flags after the refresh cycle.

This supports the auditâ€™s `CLOCK` contract and its `step == day * turnsPerDay + hour` invariant.

### Inventory and supported species

Confirmed by source:

```python
CROPS = {"WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON"}
ANIMALS = {"GOOSE", "COW", "SHEEP"}
PRODUCTS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"]
```

`CHICKEN` is absent from `ANIMALS` and is therefore correctly classified as `NOT_SUPPORTED`.

### Feed / care / production semantics

Confirmed by `_daily_refresh_animals`:

```python
base = 1
bonus = tile.pop("pending_care_bonus", 0) if tile["fed_today"] else 0
tile["yield_units"] = min(a["max_held"], tile["yield_units"] + base + bonus)
```

This confirms that base output is still generated on a scheduled production day even when `fed_today == False`, if the animal has not escaped and the schedule matches. `FEED` is not the gate for base output; it prevents escape and allows a bonus to be consumed, while `CARE` accumulates `pending_care_bonus` when fed + cared on the same day.

### Fertilizer semantics

Confirmed by source:

- `FERTILIZE` sets `tile["fertilized_until_day"] = max(tile.get(...), day + 2)`;
- during `_apply_unit_action` watering window, a fertilized crop adds `+2` instead of `+1` on the watered day;
- therefore the uplift is `+1` relative to the base increment, not `+2 additional units` beyond the normal cycle.

This supports the auditâ€™s claim that the effective gain is `BASE_INCREMENT_TOTAL = 1`, `FERTILIZED_INCREMENT_TOTAL = 2`, `FERTILIZER_UPLIFT = +1`.

### Inventory overflow

Confirmed by source:

- `DROP` in `_apply_unit_action` drops only the room-available portion and discards the rest;
- `_drop_inventories_to_shed` does the same at EOD;
- `PLACE` to the shed takes `min(n, room)` and leaves excess with the worker inventory.

This is the right distinction between `MANUAL DROP` / `EOD AUTO-DROP` and `PLACE` to shed.

---

## 2. Contradiction found

The only clear issue preventing unconditional acceptance is the aggregate engine fingerprint.

```text
CLAIM:
The auditâ€™s aggregate SHA256 `4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d` is reproducible using the declared manifest and formula.

SOURCE_SYMBOL:
Section 2, fingerprint / manifest logic

SOURCE_EVIDENCE:
sha256(UTF8(join("\n", sort(relative_path + "\t" + file_sha256))))

REPRODUCTION:
I re-ran the declared hash calculation with the listed manifest and the result was `1c58e32f8e156f9049c7a14aefe54d8fb244c4bc5441d95b491432f21886a13d`, not the reported value.

IMPACT:
This is a provenance failure, not a biological semantic failure. It weakens the claim that the contract is frozen for a precise runtime identity.

PROPOSED_CORRECTION:
Fix the manifest / path set / aggregation step, or explicitly mark the aggregate as `UNREPRODUCED` rather than `VERIFIED`.

SEVERITY:
P3
```

This is important because the audit intends to support downstream Foundation decisions with engine identity evidence.

---

## 3. Required answers to the review questions

1. Il fingerprint engine Ã¨ riproducibile?
   - No, non nel modo pubblicato. I singoli file mascherano correttamente, ma lâ€™aggregate non si riproduce.

2. Il clock contract Ã¨ corretto?
   - SÃ¬.

3. Esiste qualche off-by-one biologico?
   - Non rilevato in questa review.

4. `CHICKEN=NOT_SUPPORTED` Ã¨ corretto?
   - SÃ¬.

5. Il ledger include tutte le specie supportate?
   - SÃ¬, per il runtime verificato.

6. Animal base production senza FEED Ã¨ confermata?
   - SÃ¬, confermata.

7. La semantica CARE / pending bonus Ã¨ corretta?
   - SÃ¬.

8. Fertilizer total=2/uplift=+1 Ã¨ corretto?
   - SÃ¬.

9. La finestra fertilizer `d..d+2` Ã¨ corretta?
   - SÃ¬.

10. Manual DROP puÃ² perdere overflow?
   - SÃ¬.

11. PLACE conserva lâ€™eccedenza?
   - SÃ¬.

12. Ci sono altre P0 contradiction non individuate?
   - Non rilevate.

13. Ci sono P0 Codex che in realtÃ  non sono P0?
   - Nessuna di semantica; la singola criticitÃ  rilevata riguarda la provenance, non il comportamento engine.

14. Il period ledger Ã¨ sufficientemente source-grounded?
   - In sostanza sÃ¬, ma con due caveat: (a) fix hash provenance; (b) keep all periods config-relative rather than universal step counts.

15. Il ledger separa correttamente engine facts e policy choices?
   - SÃ¬, in principio.

16. La tripartizione della serviceability Ã¨ corretta?
   - SÃ¬, come distinzione logica, purchÃ© venga usata come policy context e non come fatto engine.

17. La discrepancy matrix Ã¨ completa abbastanza per iniziare Ontology revision?
   - In grande parte sÃ¬, ma la correzione del fingerprint Ã¨ obbligatoria prima di usarlo come prova `hard`.

18. Esiste qualche fatto ancora `UNRESOLVED` che deve bloccare il freeze?
   - La risposta semantica Ã¨ `NO`; la risposta di provenance Ã¨ `SI`, nel senso che lâ€™audit richiede una correzione formale prima di essere presentato come `frozen` senza eccezioni.

---

## 4. Discrepancy matrix summary

```text
DISCREPANCY_ID: AGG-01
CODEX_CLASSIFICATION: ACCEPTED ENGINE CONTRACT
REVIEWER_CLASSIFICATION: ACCEPT_WITH_CORRECTION
CURRENT_FOUNDATION_CLAIM_VERIFIED: yes, for single-file engine hashes
ENGINE_EVIDENCE_VERIFIED: yes, source-grounded semantics match runtime
RECOMMENDED_CHANGE_VALID: yes, fix the aggregate hash provenance and language
NOTES: the aggregate hash mismatch is a documentation/provenance issue, not a semantic engine bug
```

```text
DISCREPANCY_ID: CLK-01
CODEX_CLASSIFICATION: ACCEPTED
REVIEWER_CLASSIFICATION: ACCEPTED
CURRENT_FOUNDATION_CLAIM_VERIFIED: yes
ENGINE_EVIDENCE_VERIFIED: yes
RECOMMENDED_CHANGE_VALID: no change required
NOTES: step/day/hour relationship is correct
```

```text
DISCREPANCY_ID: ANI-01
CODEX_CLASSIFICATION: ACCEPTED
REVIEWER_CLASSIFICATION: ACCEPTED
CURRENT_FOUNDATION_CLAIM_VERIFIED: yes
ENGINE_EVIDENCE_VERIFIED: yes
RECOMMENDED_CHANGE_VALID: no change required
NOTES: base animal production and feed/care semantics are correct
```

```text
DISCREPANCY_ID: FER-01
CODEX_CLASSIFICATION: ACCEPTED
REVIEWER_CLASSIFICATION: ACCEPTED
CURRENT_FOUNDATION_CLAIM_VERIFIED: yes
ENGINE_EVIDENCE_VERIFIED: yes
RECOMMENDED_CHANGE_VALID: no change required
NOTES: fertilizer effect is +1 uplift on top of base +1 production
```

```text
DISCREPANCY_ID: INV-01
CODEX_CLASSIFICATION: ACCEPTED
REVIEWER_CLASSIFICATION: ACCEPTED
CURRENT_FOUNDATION_CLAIM_VERIFIED: yes
ENGINE_EVIDENCE_VERIFIED: yes
RECOMMENDED_CHANGE_VALID: no change required
NOTES: overflow loss and place semantics are correctly captured
```

---

## 5. Final recommendation

```text
VERDICT: ACCEPT_WITH_CORRECTIONS
SUPPORTED:
- clock contract
- species inventory
- feed/care semantics
- fertilizer uplift semantics
- inventory overflow semantics
- non-universal periodic reasoning
PARTIALLY_SUPPORTED:
- aggregate provenance
- claim that the ledger is fully frozen without provenance correction
NOT_SUPPORTED:
- aggregate hash as printed
FINAL_RECOMMENDATION:
- accept the semantically correct engine ledger;
- correct the manifest/fingerprint provenance before using it as a hard contract;
- keep period values config-relative and do not seek final canonical step counts in this phase.
```

Conclusion: the contract is semantically strong and should be carried forward after a narrow provenance correction. It is not blocked by a biological contradiction; it is blocked only by an unresolved validation issue in the auditâ€™s identity proof.
