# Torneo di chiusura post-3Q — Report finale

## Esito

Il torneo congelato è stato completato: 42/42 match, sette seed preregistrati, tutte le coppie in entrambi i seat, nessuna selezione post-hoc.

| Posizione descrittiva | Agente | W-L-T | Media | Mediana | Min | Max |
|---:|---|---:|---:|---:|---:|---:|
| 1 | Antigravity V4 | 26-2-0 | 89.280,86 | 95.444 | 58.570 | 120.350 |
| 2 ex aequo | Codex V9 | 2-14-12 | 88.576,29 | 95.396 | 58.522 | 118.524 |
| 2 ex aequo | Copilot V2 | 2-14-12 | 88.576,29 | 95.396 | 58.522 | 118.524 |

Stabilità tecnica comune:

```text
ERRORS: 0
FALLBACKS: 0
ANIMAL_ESCAPES: 0
PEAK_HANDS: 12
PEAK_CROPS: 55
PEAK_ANIMALS: 19
```

## Lettura causale corretta

Il risultato non rappresenta tre strategie indipendenti. Le tre freeze dichiarano lo stesso hash di routine:

```text
C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4
```

Codex e Copilot sono equivalenti azione-per-azione e producono gli stessi valori economici a parità di seat. Antigravity usa la medesima sequenza ma aggiunge una liquidazione dello shed negli step 717–719. Per questo tutte le metriche operative sono identiche:

| KPI medio | Antigravity | Codex | Copilot |
|---|---:|---:|---:|
| Azioni produttive | 2.842 | 2.842 | 2.842 |
| Azioni operative | 3.261 | 3.261 | 3.261 |
| PASS | 677 | 677 | 677 |
| MOVE / productive | 1,2477 | 1,2477 | 1,2477 |
| MOVE / operational | 1,0874 | 1,0874 | 1,0874 |

Il delta medio Antigravity rispetto alla routine base è circa **+704,57**. È attribuibile alla liquidazione terminale e alla sua interazione order-sensitive con il seat, non a una diversa architettura 3Q. Su ciascun confronto diretto Antigravity chiude 13-1; la sola inversione si verifica sul seed `26090103` in una delle due assegnazioni di seat.

Codex–Copilot chiude con 12 pareggi e una vittoria per parte: nei due match non pari prevale il seat 0. Questo conferma sia l'identità strategica sia la necessità del bilanciamento dei seat.

## Verdetto dei gate

```text
FROZEN_HASH_GATE: PASS
42_MATCH_COMPLETION_GATE: PASS
SEAT_BALANCE_GATE: PASS
TECHNICAL_STABILITY_GATE: PASS
STRATEGIC_INDEPENDENCE_GATE: FAIL
```

Il torneo è valido come:

- replica riproducibile dell'ultimo round 3Q;
- stima causale dell'effetto della liquidazione terminale;
- controllo della sensibilità al seat;
- baseline di chiusura prima del ritorno agli esperimenti post-E16.

Non è valido come:

- attribuzione comparativa a tre strategie agent-local;
- prova che Antigravity o Copilot abbiano sviluppato autonomamente la densità 3Q;
- motivo per accettare o respingere i candidati Foundation C2.1;
- promozione automatica su Kaggle.

## Implicazioni per il prossimo torneo indipendente

Antigravity e Copilot devono sostituire il riuso della routine Codex con implementazioni proprie. Prima del freeze saranno obbligatori:

1. nessun import di routine o planner di altri agenti;
2. action table e routine hash differenti;
3. disclosure della provenance;
4. standalone isolato e parità con il source proprietario;
5. manifest preregistrato con gli stessi seed e seat, più eventuale holdout non osservato;
6. separazione tra telemetria comune e policy agent-local.

Il target iniziale realistico per le nuove implementazioni indipendenti è preservare zero fughe e stabilità tecnica, raggiungere una media competitiva almeno pari a 85K e dimostrare un profilo operativo non identico. Solo in seguito è sensato confrontare target superiori di rendimento.

## Artefatti

- manifest: `POST_3Q_CLOSURE_TOURNAMENT_MANIFEST.md`;
- risultati completi: `POST_3Q_CLOSURE_TOURNAMENT_RESULTS.json`;
- tabella match: `POST_3Q_CLOSURE_TOURNAMENT_RESULTS.csv`;
- freeze: directory `freeze/`;
- runner: `scripts/run_post_3q_closure_tournament.py`.

La riconciliazione Foundation resta intenzionalmente sospesa in attesa dei feedback indipendenti.
