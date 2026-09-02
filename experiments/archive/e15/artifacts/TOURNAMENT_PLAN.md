# E15 Tournament Execution Plan & Governance Protocol

- **Experiment Phase**: E15.0 (Pre-Match Tournament Freeze)
- **Status**: `FROZEN_PRE_MATCH` (Execution Pending Formal Authorization)
- **Tournament Authority**: Multi-Agent Strategy Governance
- **Semantic Source of Truth**: `docs/model_specs/ONTOLOGY.md` (64 canonical concepts)
- **Freeze Reference**: `experiments/archive/e15/artifacts/freeze/FREEZE_MANIFEST.md`

---

## 1. Tournament Structure & Match Pairings

The tournament follows an exact 3-match single round-robin design where each candidate competes twice (once as Player 0, once as Player 1):

| Match ID | Player 0 (P0) | Player 1 (P1) | Submission P0 | Submission P1 | Seed (Pre-Declared) |
|---|---|---|---|---|:---:|
| **M1** | Antigravity | Codex | `experiments/archive/e16/artifacts/freeze/legacy_submissions/submission_antigravity.py` | `submission/submission_codex.py` | `1113294977` |
| **M2** | Codex | Copilot | `submission/submission_codex.py` | `submission/submission_copilot.py` | `3033283457` |
| **M3** | Copilot | Antigravity | `submission/submission_copilot.py` | `experiments/archive/e16/artifacts/freeze/legacy_submissions/submission_antigravity.py` | `3122977751` |

### Position Balance
- **Antigravity**: M1 (P0), M3 (P1)
- **Codex**: M2 (P0), M1 (P1)
- **Copilot**: M3 (P0), M2 (P1)

---

## 2. Pre-Declared Seed Provenance

The seeds for all three matches are fixed prior to any execution and derived via SHA256 deterministic seeding:
- **M1 Seed**: `1113294977` (`SHA256("E15_MATCH_1_ANTIGRAVITY_VS_CODEX_SEED")[:8]`)
- **M2 Seed**: `3033283457` (`SHA256("E15_MATCH_2_CODEX_VS_COPILOT_SEED")[:8]`)
- **M3 Seed**: `3122977751` (`SHA256("E15_MATCH_3_COPILOT_VS_ANTIGRAVITY_SEED")[:8]`)
- **Strict Rule**: No seed rerolls or post-hoc seed substitutions are permitted.

---

## 3. Tournament Ranking & Classification Criteria

### 3.1 Primary Ranking Criterion
- **Match Wins (W-L Record)**: The agent with the highest number of head-to-head match victories takes 1st place.

### 3.2 Tie-Breaking Criterion (Signed Money Differential)
In the event of a three-way tie (all agents finish 1–1), the final ranking is determined by the **aggregate signed final-money differential**:

$$D_i = \sum_{m \in \text{Matches}(i)} \left( \text{final\_money}_i^{(m)} - \text{final\_money}_{\text{opponent}}^{(m)} \right)$$

- Calculated strictly over the two matches played by agent $i$.
- No additional sudden-death matches or alternative tie-breakers are permitted.

---

## 4. Post-Match Verification & Empirical Verdict Protocol

Following each match execution, evaluation proceeds according to the structured multi-agent protocol:

```
MATCH EXECUTION (720 steps)
       │
       ▼
RAW REPLAY & TELEMETRY JSON
       │
       ▼
NEUTRAL FORENSIC ANALYSIS (ChatGPT)
       │
       ▼
INDEPENDENT PARTICIPANT FEEDBACK (P0 & P1 Agents)
       │
       ▼
CONSENSUS SYNTHESIS (ChatGPT)
       │
       ▼
E15 VERDICT PER DISCRIMINATED CONCEPT_ID
```

### 4.1 Permitted Verdicts for Canonical Concepts
For each `concept_id` actively discriminated in a match, the post-match evaluation must assign exactly one of:
1. `SUPPORTED`: Empirical replay data confirms the model's hypothesized mechanism and expected economic direction.
2. `WEAKENED`: Empirical data contradicts the expected magnitude or direction of the effect.
3. `NOT_DISCRIMINATED`: Both agents adopted similar choices or the mechanism was not activated on this seed.
4. `CONFOUNDED`: Multiple simultaneous causal factors prevent unambiguous attribution.
5. `INCONCLUSIVE`: Metric data was unobservable or observation noise prevents rigorous evaluation.

### 4.2 Non-Equivalence Principle
- **Match Victory $\neq$ Model Validity**: A winning agent's model may contain false causal assumptions that were masked by other dominant factors.
- **Match Defeat $\neq$ Model Falsification**: A losing agent's individual parametric hypotheses may still be empirically correct despite global loss.

---

## 5. Output Directory Structure

Each match outputs full telemetry into isolated directories:
```text
results/e15/
├── freeze/
│   ├── FREEZE_MANIFEST.md
│   ├── ONTOLOGY_E15_FROZEN.md
│   ├── MODEL_SPEC_ANTIGRAVITY_E15_FROZEN.md
│   ├── MODEL_SPEC_CODEX_E15_FROZEN.md
│   ├── MODEL_SPEC_COPILOT_E15_FROZEN.md
│   ├── submission_antigravity_E15_FROZEN.py
│   ├── submission_codex_E15_FROZEN.py
│   └── submission_copilot_E15_FROZEN.py
├── M1_antigravity_vs_codex/
│   ├── match_metadata.json
│   ├── raw_replay.json
│   ├── telemetry.json
│   └── summary.json
├── M2_codex_vs_copilot/
│   ├── match_metadata.json
│   ├── raw_replay.json
│   ├── telemetry.json
│   └── summary.json
├── M3_copilot_vs_antigravity/
│   ├── match_metadata.json
│   ├── raw_replay.json
│   ├── telemetry.json
│   └── summary.json
├── P0_P1_ENVIRONMENT_AUDIT.md
└── TOURNAMENT_PLAN.md
```
