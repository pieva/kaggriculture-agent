# Manifest congelato — torneo 3Q a tre agenti

Il presente manifest è scritto prima dell'esecuzione. Nessun seed, match o outlier può essere rimosso dopo l'osservazione dei risultati.

```text
PROTOCOL: C2_3Q_THREE_WAY_V9_FROZEN_V1
EPISODE_STEPS: 720
TURNS_PER_DAY: 24
SEAT_BALANCED: YES
PAIRS: ANTIGRAVITY-CODEX, ANTIGRAVITY-COPILOT, CODEX-COPILOT
SEEDS: 26090101, 26090102, 26090103, 1838889274, 1619968655, 710418712, 562040596
MATCHES_PER_PAIR: 14
TOTAL_MATCHES: 42
MATCHES_PER_AGENT: 28
POST_HOC_SELECTION: NO
```

## Candidate congelate

### Codex

```text
ENTRYPOINT: results/model_spec_c2/codex/freeze/submission_codex_v9_tournament.py
VERSION: CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY
SHA256: AC541588EF9746F00C9FE6CDA378DB4DF793347CDB5FEE8FF2FCA5EC1847C421
PARITY: 719/719
ISOLATED_IMPORT: PASS
```

### Antigravity

```text
ENTRYPOINT: src/agricola/strategy/antigravity/agent_c2_100k_central.py
POLICY: src/agricola/strategy/antigravity/antigravity_3q_central_cluster.py
VERSION: ANTIGRAVITY-C2-3Q-CENTRAL-CLUSTER-100K-V3.0
AGENT_SHA256: 5C1D58C5E7C8A1D68BFC45F9B98A4A2D253094A01F097A85B8B6B733F287F541
POLICY_SHA256: 648F0E7D1E4514188012C911564812301FA167A13E4CAEC6EA7AA1FC81278B0F
```

### Copilot

```text
ENTRYPOINT: src/agricola/strategy/copilot/three_quadrant.py
VERSION: COPILOT-C2-3Q-CENTRAL-CLUSTER-13W-V1.0
SHA256: C7F22759D6DEB530BE55A1364029AE058B41E5FBC659784164523ACFCED162E6
```

Copilot eredita `Antigravity3QCentralClusterPolicy`; il torneo misura due entrypoint/versioni distinte, ma il report deve dichiarare questa dipendenza e non presentare la parità tra i due come validazione indipendente dell'architettura.
