# E17.1 — Esibizione development a tre delle policy reattive

- **Data:** 2026-09-02
- **Ruolo epistemico:** `DEVELOPMENT_ONLY_NON_QUALIFYING`
- **Matrice:** 42/42 match completati
- **Holdout consumato:** no
- **Final confirmation consumata:** no
- **Torneo ufficiale:** bloccato dai gate falliti di Claude V2

## 1. Perché l'esibizione non è il torneo ufficiale

Claude V2 è una policy nativa, reattiva e strategicamente indipendente. Il suo
audit tecnico è positivo: 25 test passati, lint pulito, hash di source e config
coerenti con il freeze, zero errori tecnici e nessun import o action table di
altri agenti. Tuttavia il development gate Claude è `FAIL`:

- media contro opponent inert: 14.445,29, sotto il target di 50.000;
- tre fughe EOD derivate;
- attivazione 3Q in 13/14 run, non in tutte.

Il protocollo originale vieta di usare l'holdout prima dell'ammissione di
entrambe le candidate. È stata quindi eseguita una matrice seat-balanced sui
soli sette seed development già consumati, secondo
`E17_REACTIVE_TOURNAMENT_CANDIDATE_AMENDMENT_2.md`.

## 2. Partecipanti e matrice

| ID breve | Policy | Stato prima dell'esibizione |
|---|---|---|
| `CODEX_V9` | `CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY` | controllo congelato |
| `CODEX_REACTIVE` | `CODEX-E17.1-3Q-REACTIVE-GUARDED-V1` | development gate PASS |
| `CLAUDE_V2` | `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V2` | freeze con gate FAIL |

La matrice comprende tre coppie, sette seed e due orientamenti di seat:

```text
3 × 7 × 2 = 42 match
```

Non sono state eliminate o sostituite run. Tutte le policy sono state eseguite
con source e config hash-verificati prima del primo match.

## 3. Classifica sintetica

| Policy | W–T–L | Denaro medio | Mediana | Min–Max | 3Q | Fughe | MOVE/prod. | Hands max | Errori |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Codex V9 | 15–12–1 | 112.149,21 | 103.729,5 | 58.522–186.869 | 28/28 | 0 | 1,2473 | 12 | 0 |
| Codex reattivo | 15–12–1 | 112.149,21 | 103.729,5 | 58.522–186.869 | 28/28 | 0 | 1,2473 | 12 | 0 |
| Claude V2 | 0–0–28 | 11.777,64 | 11.780,5 | 9.244–14.194 | 28/28 | 2 | 2,9719 | 8 | 0 |

V9 e Codex reattivo sono primi ex aequo. La singola vittoria e sconfitta nel
loro testa-a-testa sono lo stesso effetto seat simmetrico di 68 unità sul seed
`26090103`; il delta medio è esattamente zero.

## 4. Testa-a-testa

| Coppia | Esito | Delta monetario medio del primo |
|---|---:|---:|
| Codex V9 vs Codex reattivo | 1–12–1 | 0 |
| Codex V9 vs Claude V2 | 14–0–0 | +123.944,5 |
| Codex reattivo vs Claude V2 | 14–0–0 | +123.944,5 |

In nessuno dei 28 match del Codex reattivo è scattato un override e non è
stato rilevato un acquisto Wheat non eseguito. Di conseguenza l'esibizione non
misura il beneficio della guardia: conferma soltanto che, quando il trigger non
si presenta, la candidate conserva esattamente il comportamento V9.

## 5. Timing, densità e topologia terminale

| Policy | Q1 mediano | Q2 mediano | Crop tile finali medie | Animali finali medi |
|---|---:|---:|---:|---:|
| Codex V9 | D6 | D11 | 13,93 | 19,00 |
| Codex reattivo | D6 | D11 | 13,93 | 19,00 |
| Claude V2 | D2 | D11 | 2,29 | 1,00 |

Tile terminali medie classificate `NON_PRODUCTIVE` per quadrante, su 25 tile:

| Policy | Q0/NW | Q1/NE | Q2/SW |
|---|---:|---:|---:|
| Codex V9 | 10,07 | 17,00 | 14,00 |
| Codex reattivo | 10,07 | 17,00 | 14,00 |
| Claude V2 | 20,21 | 19,64 | 20,86 |

Claude anticipa Q1 ma non converte l'espansione in densità produttiva. Il
limite dominante è il costo di servizio: circa tre movimenti per azione
produttiva, otto hands massimi, poche colture terminali e un solo animale
medio. Sotto contesa Claude migliora la copertura 3Q a 28/28 rispetto al
13/14 passivo, ma conserva due fughe e resta economicamente molto distante.

## 6. Collegamento con l'evidenza Kaggle

Lo snapshot esterno fornito dal proprietario mostra:

| Submission | Rating osservato |
|---|---:|
| Codex E17.0 / V9 | 1.089,7 |
| Codex E17.1 reattivo | 1.353,6 |
| Delta | **+263,9 (+24,2%)** |

Il risultato esterno è forte evidenza operativa a favore della guardia
reattiva, ma non è una prova matched-pair: seed, avversari e stato del rating
non sono identici. La combinazione delle due evidenze è comunque informativa:

- localmente, in assenza del trigger, la guardia è neutrale;
- su Kaggle, dove la contesa è reale, la candidate ottiene un vantaggio
  materiale;
- il benchmark locale corrente non riproduce ancora la specifica scarsità che
  rende utile la reazione.

## 7. Decisioni

1. mantenere congelate V9 e Codex E17.1 reattivo;
2. considerare il risultato Kaggle una priorità di analisi tramite replay,
   senza attribuzione causale definitiva finché non sono osservati i trigger;
3. non ammettere Claude V2 all'holdout;
4. richiedere una Claude V3 autonoma che riduca movimento e retry, aumenti
   capacità produttiva e hands, completi 3Q in ogni development run e azzeri
   le fughe;
5. eseguire il torneo ufficiale soltanto dopo un nuovo freeze Claude con tutti
   i gate PASS;
6. preservare integralmente i sei seed holdout e i quattro final-confirmation.

## 8. Artefatti

- risultati JSON: `experiments/e17/artifacts/derived/common/E17_REACTIVE_THREE_WAY_DEVELOPMENT_EXHIBITION.json`;
- risultati CSV: `experiments/e17/artifacts/derived/common/E17_REACTIVE_THREE_WAY_DEVELOPMENT_EXHIBITION.csv`;
- runner: `experiments/e17/tools/common/run_e17_reactive_three_way_development_exhibition.py`;
- amendment: `experiments/e17/reviews/common/E17_REACTIVE_TOURNAMENT_CANDIDATE_AMENDMENT_2.md`.

SHA-256:

```text
JSON   C6D854CA1CEDB47C4D6DEBD8770ACE7378EED9D69083502A9489D3F34A46E4A9
CSV    8464CB7BD23031EB8EBDE6A7F38EDFA0D1E443E76D367B79BE1A92F3485F4E83
RUNNER 9E4E9A9FEC9A31157E94EA2BF3507C6256E9C289A85CDC145CA158E4D929C10D
```
