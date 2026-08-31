# Codex C2 V7 — Kaggle Manifest

```text
MANIFEST_VERSION: codex.c2.kaggle.v2
MANIFEST_STATUS: CLOSED
AGENT_ID: CODEX
AGENT_VERSION: CODEX-C2-COMPACT-Q0-ROUTINE-V7
FOUNDATION_CHECKPOINT: f391ee2
SUBMISSION_FILE: submission/submission_codex.py
SUBMISSION_ENTRYPOINT: agent
PACKAGE_READINESS: TECHNICALLY_BUILDABLE_ECONOMICALLY_BLOCKED
BUILD_VERDICT: BUILD_NOT_READY
KAGGLE_AUTHORIZED: NO
```

## Artifact identity

```text
SHA256: 965E03566E2F8C2FAF04A9A275781D2953F03C66288031700BDB59E49A5A0427
BYTES: 130649
CONFIG_SCHEMA: model_spec_c2.codex.compact_q0.v1
MODEL_SPEC_SHA256: 5F6A3E5199589408CF43D4BBE13C629B6B978B095046BAE4D912006F8248D1F7
FOUNDATION_CHECKPOINT: f391ee2
```

## Package checks

- single-file standalone: PASS;
- isolated import and callable entrypoint: PASS;
- embedded compact controller/config: PASS;
- source/standalone exact parity: PASS;
- local engine status P0/P1: PASS;
- terminal lifecycle: `TERMINAL_CLOSED`;
- error/fallback: zero;
- economic gate: `FAILURE` at mean 39.265,67;
- animal-escape gate: FAIL, 24.

Non sono state effettuate submission, sostituzioni, browser automation o
letture leaderboard. Il manifest è deliberatamente chiuso.

```text
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
COMMIT_AUTHORIZED: NO
PUSH_AUTHORIZED: NO
NEXT_GATE: NEW_AUTHORIZED_BUILD
```
