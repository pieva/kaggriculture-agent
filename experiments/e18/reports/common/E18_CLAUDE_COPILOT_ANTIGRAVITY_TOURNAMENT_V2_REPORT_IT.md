# E18 — torneo di sviluppo Claude/Copilot/Antigravity V2

## Decisione

Nessun candidato è promosso: round robin diagnostico, verifica
**indipendente sul motore reale** dell'ultima candidata di ciascuna linea
dopo il ciclo di sviluppo aperto dal torneo V1 — Claude E18.3
lifecycle-safety, Copilot E18.8 economic-recovery V5, Antigravity E18.2
capacity-governed. Nessun risultato self-reportato dai singoli agenti è
stato accettato senza replay: l'artifact V2 di Copilot era già stato
segnalato come sintetico nell'intake originale, quindi ogni numero qui
viene da questo stesso harness comune, mai dai runner interni di ciascuna
linea. Codex resta escluso di proposito. Holdout/final non consumati.

## Protocollo

- partecipanti: `CLAUDE_E18_3`, `COPILOT_E18_8`, `ANTIGRAVITY_E18_2`;
- 7 seed development, entrambi i seat, 3 coppie, 42 match reali;
- runner: `experiments/e18/tools/common/run_e18_claude_copilot_antigravity_v2_tournament.py`
  (stesso harness del torneo V1, avversari sostituiti).

## Risultati

| Agente | Record | Denaro medio | Min–max | Stdev | Regimi attivati | Perdite zootecniche | Peak hands medi |
|---|---:|---:|---:|---:|---|---:|---:|
| Copilot E18.8 | 28-0-0 | 21.548,96 | 18.660–22.896 | 1.119,74 | `CARROT_LOOP` | 0 | 1,0 |
| Claude E18.3 | 11-17-0 | 11.247,21 | 7.106–17.029 | 2.365,70 | `LOW_PRESSURE_BALANCED` | 12 | 7,1 |
| Antigravity E18.2 | 3-25-0 | 9.209,00 | 5.376–15.615 | 1.940,89 | `BALANCED_SERVICE`, `EXPANSION_TEMPO` | 0 | 6,6 |

## Testa a testa

| Matchup | Record | Media A | Media B | Delta A |
|---|---:|---:|---:|---:|
| Copilot vs Claude | 14-0-0 | 22.320,50 | 11.271,43 | +13.654,64 (lettura Copilot) |
| Copilot vs Antigravity | 14-0-0 | — | 8.665,86 | +13.654,64 |
| Claude vs Antigravity | 11-3-0 | 11.223,00 | 9.752,14 | +1.470,86 |

Copilot spazza entrambi gli avversari 14-0; Claude batte Antigravity con
margine più stretto di quanto la sola classifica suggerisca (11-3, non un
dominio netto).

## Gate diagnostici

Solo **Copilot E18.8** supera tutti e quattro i controlli diagnostici
(zero errori/fallback, zero perdite, media ≥15.000). Claude fallisce sulla
sicurezza (12 perdite), Antigravity sulla soglia economica.

## Confronto con l'auto-verifica di ciascuna linea

- **Copilot** aveva riportato `14-0` contro Antigravity nel proprio test
  interno; qui perde `0-14`. La differenza si spiega con l'avversario:
  il test interno di Copilot usa una versione Antigravity diversa da
  `ANTIGRAVITY_E18_2`. Il numero assoluto di Copilot (media ~21-22k) è
  però confermato in modo indipendente da questo harness — non un
  artefatto sintetico come l'artifact V2 originale.
- **Antigravity** aveva riportato un'ablation interna controllata (governor
  on/off, stesso pool di avversari): media `10.051,86` con governor attivo
  contro `9.405,00` disattivo, **delta +646,86 (+6,9%)**. Coerente con
  quanto osservato qui: il governor produce un guadagno reale ma piccolo,
  non sufficiente a spostare il livello assoluto (`9.209,00` qui, contro
  `9.218,46` di V1 sullo stesso ordine di grandezza) quando l'avversario è
  molto più forte.

## Letture causali per agente

**Copilot** vince nettamente con un'architettura deliberatamente minima:
`hire_target = 2` (farmer + un solo hand, mai di più — `peak_hands_mean =
1,0` conferma la disciplina, non un guasto), una sola coltura (`CARROT`,
ciclo di resa 2-3 giorni, il più veloce disponibile) e **zero bestiame**
(sidesteppa interamente la logistica di alimentazione che affligge Claude).
`peak_crops_mean = 15,75`, il più basso dei tre: la vittoria non viene dalla
scala ma dall'affidabilità — un loop `DIG→PLANT→WATER→HARVEST→SELL` corto e
mai congestionato. Il soffitto è però evidente: lontanissimo dal target
100.000, e la config non lascia margine di crescita — nessuna leva di
scala è stata ancora introdotta.

**Claude** mantiene il vantaggio di superficie (`peak_crops_mean = 19,86`)
e di manodopera (7,1 media) ma le 12 perdite zootecniche residue (causa già
diagnosticata e non ancora corretta: abbinamento greedy dell'identità non
ottimale sotto affollamento) bastano a farlo perdere quasi tutti i match
contro Copilot e una parte contro Antigravity. Un solo regime attivato:
entrambi gli avversari restano sotto la soglia di pressione del
classificatore.

**Antigravity** resta tecnicamente ineccepibile (zero errori, fallback,
perdite; due regimi realmente attivati; divergenza azione e architettura
12/14 entrambe) ma con un tetto economico quasi invariato rispetto a V1
(9.209 contro 9.218,46) nonostante il nuovo capacity governor. La propria
ablation controllata conferma che il governor funziona (+6,9%) ma la leva è
troppo piccola: il collo di bottiglia è strutturale, non di capacità
marginale — `peak_crops_mean = 34,64` è il più alto dei tre eppure produce
il denaro più basso, segno che la conversione superficie→raccolto→vendita
resta inefficiente indipendentemente dal recovery on-tile.

## Artefatti

- `experiments/e18/artifacts/derived/common/E18_CLAUDE_COPILOT_ANTIGRAVITY_TOURNAMENT_V2.json`;
- `experiments/e18/artifacts/derived/common/E18_CLAUDE_COPILOT_ANTIGRAVITY_TOURNAMENT_V2.csv`;
- `experiments/e18/tools/common/run_e18_claude_copilot_antigravity_v2_tournament.py`.

## Linee di sviluppo suggerite

- **Claude**: chiudere la causa residua già diagnosticata (matching a
  costo minimo al posto del greedy) prima di qualunque altra leva —
  `docs/model_specs/claude/MODEL_SPEC_CLAUDE_E18_3_LIFECYCLE_SAFETY_V1.md`
  Sezione 5.
- **Antigravity**: la leva di capacità è confermata ma insufficiente da
  sola; serve una leva strutturale sulla conversione superficie→raccolto
  (perché 34,6 crop di picco producono meno soldi dei 15,75 di Copilot),
  non un secondo incremento di capacità marginale.
- **Copilot**: la base a 2 lavoratori è solida e pulita; la prossima
  iterazione deve dimostrare che può scalare (più lavoratori, più
  superficie, eventualmente una seconda coltura) senza reintrodurre i
  problemi di congestione che hanno affondato le versioni precedenti — non
  toccare il loop CARROT che già funziona finché la scala non è verificata
  con lo stesso rigore (audit prima del fix, non tuning cieco).
