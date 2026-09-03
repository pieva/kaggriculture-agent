# E17.3 — Torneo development Codex / Claude / Copilot

- **Data:** 2026-09-03
- **Stato:** AUTHORIZED BY OWNER
- **Ruolo:** development diagnostic, non qualificante
- **Antigravity:** escluso su richiesta del proprietario fino al 2026-09-04
- **Holdout/final confirmation:** non autorizzati e non consumati

## Partecipanti congelati per il round

| ID torneo | Implementazione | Motivazione |
|---|---|---|
| `CODEX_662` | `CODEX-E17.3-TOPOLOGY-FILL-662-V2` | candidata Kaggle corrente, topologia 6-6-2 e controllo reale 14/14 |
| `CLAUDE_V3` | `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V3` | migliore linea Claude completa; V4 è esclusa perché il suo spot-check è negativo (-8,9%) |
| `COPILOT_NATIVE` | `COPILOT-E17.0-NATIVE-3Q-CROP-BASELINE-V1` | baseline nativa Copilot congelata con gate E17.0 PASS |

Le policy non vengono modificate dopo l'avvio del torneo. Il confronto misura
le implementazioni as-built, non la qualità astratta dei rispettivi planner.

## Matrice preregistrata

Si usano soltanto i sette seed `development` di
`experiments/e17/manifest/E17_COMMON_MANIFEST_V1.json`:

```text
26090101, 26090102, 26090103, 1838889274, 1619968655, 710418712, 562040596
```

Per ognuna delle tre coppie si eseguono entrambi gli orientamenti di seat:

```text
3 coppie × 7 seed × 2 orientamenti = 42 match
```

Nessuna run può essere rimossa o sostituita. Antigravity non viene importato,
eseguito o incluso nei risultati.

## Metriche

- vittorie, sconfitte, pareggi, denaro medio/mediano/minimo e sensibilità al seat;
- giorno di sblocco Q1/Q2, picco hands, crop e animali;
- MOVE, azioni produttive, PASS e rapporto MOVE/produttive;
- fughe EOD derivate, errori tecnici e fallback;
- profilo terminale per quadrante, crop, animali, pascoli vuoti e weed;
- per Codex: pascoli target costruiti/riempiti, celle crop recuperate e breach Q2.

## Interpretazione

Il ranking competitivo è accompagnato da un'analisi dei meccanismi. Un agente
può vincere il round ma mantenere un rischio strutturale; analogamente una
baseline debole può esporre una capacità riusabile. Le raccomandazioni devono
separare punti di forza osservati, limiti osservati e ipotesi da testare.

## Output

- `experiments/e17/artifacts/derived/common/E17_THREE_AGENT_DEVELOPMENT_TOURNAMENT_V2.json`
- `experiments/e17/artifacts/derived/common/E17_THREE_AGENT_DEVELOPMENT_TOURNAMENT_V2.csv`
- `experiments/e17/reports/common/E17_THREE_AGENT_DEVELOPMENT_TOURNAMENT_V2_REPORT_IT.md`
