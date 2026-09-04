# MODEL SPEC — ANTIGRAVITY-E18.2-CAPACITY-GOVERNED-V1

## 1. Identificazione e Namespace

- **Candidato**: `ANTIGRAVITY-E18.2-CAPACITY-GOVERNED-V1`
- **Candidate ID**: `ANTIGRAVITY_E18_2_CAPACITY_GOVERNED_V1`
- **Policy Version**: `ANTIGRAVITY-E18.2-CAPACITY-GOVERNED-V1`
- **Base Policy**: `ANTIGRAVITY-E18.1-REACTIVE-REBOOT-V1`
- **Autore**: Antigravity Pair Programmer
- **Data**: 2026-09-04
- **Stato**: `DEVELOPMENT_CANDIDATE`
- **Ruolo**: `CAPACITY_GOVERNED_THROUGHPUT`
- **Source**: `src/agricola/strategy/antigravity/antigravity_e18_capacity_governed_v2.py`
- **Config**: `docs/model_specs/antigravity/e18/configs/ANTIGRAVITY_E18_2_CAPACITY_GOVERNED_V1.json`

---

## 2. Diagnosi Causale e Contesto di Sviluppo

Nel torneo diagnostico a tre (Claude E18.2, Copilot E18.2, Antigravity E18.1), Antigravity ha dimostrato la piena correttezza tecnica e geometrica:
- Record `15-13-0`, media `$9.218,46`, range `6.442–12.079` (stdev `1.612,98`);
- Zero errori tecnici, zero fallback, zero perdite zootecniche;
- Entrambi i regimi reattivi attivati (`BALANCED_SERVICE`, `EXPANSION_TEMPO`);
- Vittoria netta contro Copilot E18.2 (`14-0-0`, media `$10.028,86`);
- Sconfitta contro Claude E18.2 (`1-13-0`, media `$8.408,07` contro `$13.567,50`);
- **Anomalia causale chiave**: `peak_crops_mean = 32,07` per Antigravity contro `24,61` per Claude. La superficie coltivata era superiore (+30%), ma il denaro finale inferiore (-38%).

Analogamente al precedente strutturale Codex E18.2, la correttezza del lifecycle da sola non basta: il collo di bottiglia è il **controllo di capacità e servizio locale (throughput)**, non la topologia né l'introduzione di un terzo regime.

---

## 3. Architettura del Governatore di Capacità On-Tile

L'architettura V2 estende la V1 tramite un layer di capacity-governance post-dispatch che preserva l'invarianza di base quando disabilitato (`capacity_governor_enabled: false` produce parità byte-for-byte con la V1).

```
[Observation]
      │
      ▼
[Base Chassis V1] (Lifecycle, Task Scan, Dual Regimes, Dynamic HIRE)
      │
      ▼ (Planned Unit Actions)
[Capacity Governor Overlay]
      │
      ├─► Se day >= terminal_passthrough_day (D28) ──► Passthrough Diretto
      ├─► Se governor_enabled == False ───────────────► Passthrough Diretto
      │
      └─► Scansione Lavoro On-Tile:
            ├─ Controlla worker con comando MOVE o PASS
            ├─ Esclude worker con carico >= 2 o in rotta di scarico shed
            ├─ Se sul tile corrente è presente un task non servito:
            │     • WEED ───────────────► ["DIG"]
            │     • PLANT (matura) ─────► ["HARVEST"]
            │     • PLANT (non irrigata)► ["WATER"]
            └─ Sostituisce il comando SENZA MOVE e senza alterare gli altri worker
      │
      ▼
[Action Emessa] (Farmer, Hands, Market)
```

### Regole di Invarianza e Sicurezza
1. **Nessun `MOVE` estraneo**: I worker non vengono mai deviati verso altre caselle; il servizio viene erogato esclusivamente *sul tile già occupato*.
2. **Nessuna alterazione degli altri worker**: L'azione degli altri operai già pianificata dal dispatch rimane inalterata.
3. **Protezione della rotta di scarico**: Gli operai che trasportano raccolto verso lo shed (`carrying >= 2` o endgame D27+ / H22+) non vengono mai intercettati, preservando il ciclo di monetizzazione allo shed.
4. **Passthrough terminale**: A partire dal giorno 28, il governatore entra in passthrough puro per consentire le vendite e la liquidazione finale senza interferenze.

---

## 4. Matrice dei Cancelli di Validazione

| Ambito | Criterio | Soglia / Requisito |
|---|---|---|
| **TECHNICAL** | Errori runtime, eccezioni, fallback, azioni invalide | `0` (Invariante rigoroso) |
| **SAFETY** | Perdite zootecniche verificate | `0` (Invariante rigoroso) |
| **CAPACITY** | Verifica causale con/senza governatore | Esecuzione a parità di seed/seat con/senza governatore |
| **ECONOMIC M1** | Media economica sui 7 seed development | Informativo: $\ge \$15.000$, nessun matchup $< \$8.000$ |
| **HEAD-TO-HEAD** | Confronto vs baseline V1 ($9.218,46) | Superiore a V1 in almeno 12/14 match per avversario |

---

## 5. Protocollo di Valutazione Rigorosa

- **Seed autorizzati**: Esclusivamente i 7 seed preregistrati di sviluppo E18 (`180903001`–`180903007`).
- **Avversari**: `CLAUDE_E18_2` e `COPILOT_E18_2` (28 match complessivi, entrambi i seat P0 e P1).
- **Holdout e Final Confirmation**: Rigorosamente vietati.
- **Decisione Finale**: Determinata oggettivamente sulla base dell'evidenza empirica (`ITERATE`, `REJECT`, o `PROMOTE`).
