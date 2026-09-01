# COPILOT C2 3Q CENTRAL CLUSTER

```text
AGENT_ID = COPILOT
MODEL_SPEC_VERSION = COPILOT-C2-3Q-CENTRAL-CLUSTER-13W-V1.0
FOUNDATION_CHECKPOINT = f391ee2
STATUS = REJECTED FOR PERFORMANCE; REQUIRES Q2 DISPATCH REDESIGN
```

## Decisione progettuale

La specifica di handover identifica correttamente il costo della dead-zone nel
quadrante SW e il salto salariale oltre 13 unita totali. Il candidato Copilot
adotta quindi il cluster centrale 3Q, ma rende esplicito il limite operativo:
un farmer e dodici hand, senza il quattordicesimo worker.

| Modulo | Risorse | Owner |
|---|---|---|
| Q0 | 3 mucche, 3 pecore, 18 colture | crop W1-W3; livestock W4-W5 |
| Q1 | 3 mucche, 3 pecore, 18 colture | crop W6-W8; livestock W9-W10 |
| Q2 | 7 pecore, 8 colture concentriche | non attivabile con il dispatch corrente |

I 19 pascoli sono `Q0(3,4..)+Q1(6,4..)+Q2[(3,5),(4,6),(3,6),(4,7),
(3,7),(2,5),(2,6)]`; le otto colture Q2 sono nel relativo anello compatto.
Nessun pascolo o coltura sovrascrive uno shed.

## Guardie

1. Q1 non e acquistato prima di day 6; Q2 non prima di day 11.
2. Ogni acquisto conserva il floor operativo configurato e la forza lavoro
   resta a 13 unita complessive, evitando il gradino Fibonacci successivo.
3. Il feed mantiene una riserva di due round.
4. I prodotti finiti e il concime nello shed sono venduti prima degli acquisti.
5. Q2 e ammesso solo tra day 11 e 14, con almeno $3,500 di liquidita
   prevista e $300 dopo il costo terreno.

## Protocollo di valutazione

`scripts/run_3q_triangular_tournament.py` esegue Antigravity-Copilot,
Codex-Copilot e Antigravity-Codex su tre seed, in entrambi i posti per ogni
coppia: 18 match. I risultati sono prodotti soltanto quando il runner viene
eseguito, in `COPILOT_3Q_TRIANGULAR_RESULTS.json`; questa specifica non
attribuisce risultati non ancora misurati.

## Esito della verifica

Contro avversario passivo, quattro seed e entrambi i seat, la media e
`$66,285.50`, inferiore al target di `$90,000`. Il tentativo di assegnare Q2 a
W12 ha popolato il modulo ma ha prodotto sette fughe: la variante e stata
ritirata. La policy corrente non deve essere considerata un candidato 3Q
competitivo; serve un dispatcher che garantisca feed, pickup e placement Q2
entro il budget giornaliero, con una nuova validazione end-to-end.
