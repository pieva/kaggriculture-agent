# E18 — torneo delle architetture dinamiche V1

## Decisione

`CODEX-E18.1-OPPONENT-REACTIVE-662-770-V1` supera il gate tecnico e
architetturale development. La candidata viene congelata come **submission
Kaggle diagnostica**, non come sostituzione già dimostrata della baseline
6-6-2: nel testa-a-testa omogeneo perde il `4,14%`, mentre supera 100k contro
Claude e Copilot. Holdout e final confirmation non sono stati consumati.

## Protocollo

- seed E18 development: `180903001`–`180903007`;
- entrambi i seat, senza sostituzione di run;
- 56 match: E18 contro controllo 6-6-2, Claude V3 e Copilot Native, più
  Claude–Copilot;
- target economico locale: 100.000;
- gate congiunto: score, errori, perdite verificate, riempimento, attivazione
  del selector, divergenza condizionata di action stream e topologia;
- avversario osservato soltanto tramite la farm pubblica corrente; nessun
  nome, rating, replay ID, seed, inventario privato o memoria cross-episode.

Il selector fotografa al D6 quadranti, hands, crop, animali, pascoli e weed
pubblici. Sotto pressione 8 sceglie `6-6-2`; da 8 in su sceglie `7-7-0`.
La decisione è sticky. Lo slot `(2,4)` è costruito ma, nel ramo ad alta
pressione, viene riempito soltanto a D28: questa guardia elimina il ciclo
morte/refill osservato nel primo prototipo e mantiene 14/14 terminale.

## Risultati economici

| Agente | Run | W-L-T | Media | Mediana | Min–max | Quota target |
|---|---:|---:|---:|---:|---:|---:|
| Codex E18 reactive | 42 | 28-14-0 | 111.654,45 | 119.768,50 | 55.695–151.362 | 111,65% |
| Codex 6-6-2 control | 14 | 14-0-0 | 83.928,71 | 75.984 | 59.314–116.268 | 83,93% |
| Claude V3 | 28 | 13-15-0 | 12.850,18 | 14.733 | 43–19.926 | 12,85% |
| Copilot Native | 28 | 1-27-0 | 9.812,46 | 8.847 | 8.261–15.183 | 9,81% |

Il medio globale E18 non è una stima neutrale: contiene più matchup deboli
del controllo. I confronti diretti sono la lettura corretta:

| Matchup E18 | Record | Media E18 | Media avversario | Delta E18 |
|---|---:|---:|---:|---:|
| vs 6-6-2 control | 0-14-0 | 80.456,43 | 83.928,71 | −3.472,29 (−4,14%) |
| vs Claude V3 | 14-0-0 | 127.072,71 | 10.292,86 | +116.779,86 |
| vs Copilot Native | 14-0-0 | 127.434,21 | 10.967,93 | +116.466,29 |

La lacuna più importante verso un target robusto di 100k resta quindi il
regime forte/simmetrico: mancano `19.543,57` alla candidata E18 nel diretto
contro 6-6-2. Claude richiede circa `7,78×` la propria media globale e
Copilot `10,19×`; qui non basta una regolazione di soglia.

## Gate dinamico e sicurezza

Tutti i controlli preregistrati passano:

- decisione topologica una volta per run: 42/42;
- modalità attivate: `6-6-2` 28/42, `7-7-0` 14/42;
- mapping avversario: Claude 14/14 `6-6-2`, controllo 14/14 `6-6-2`,
  Copilot 14/14 `7-7-0`;
- action stream condizionato all'avversario: 14/14 gruppi seed/seat
  divergenti;
- topologia condizionata: 14/14 gruppi divergenti;
- profili finali E18: 2; action stream: 27; profili di conteggio azioni: 20;
- regimi pubblici osservati per run: 2,67; transizioni medie: 3,95;
- 14/14 pascoli costruiti e riempiti in media, zero empty terminali;
- zero errori, fallback, breach Q2, cali di animali sui tile e perdite
  verificate su `tile + shed + inventari`.

Il vecchio KPI `animal_escapes`, basato solo sui tile, aveva inizialmente
scambiato un trasferimento tile→shed per una fuga. Il runner conserva ora
`tile_animal_day_drops` separato da `verified_livestock_losses`; il gate usa
il secondo.

## Delta architetturali degli altri agenti

### Claude V3

Claude produce 28 action stream su 28 e otto profili finali, con divergenza
per avversario in 14/14 gruppi azione e 10/14 topologia. Questa variabilità è
un effetto dello stato condiviso, non un selector esplicito: non espone
snapshot di regime, decisione sticky o causal activation. Inoltre registra
19 perdite verificate, 51 cali giornalieri sui tile e media weed 9,18.

Punto di forza: task selection state-driven e comportamento effettivamente
variabile. Lacune: controllo causale della variante, sicurezza zootecnica,
serviceability e scala economica. La prossima candidate deve dichiarare
feature pubbliche, decisione, alternativa di policy e prova di divergenza,
non limitarsi a mostrare più profili terminali.

### Copilot Native

Copilot è indipendente e stabile: zero errori e perdite. Tuttavia resta
crop-only, ha una sola topologia finale, nove action stream/profili e diverge
per avversario soltanto in 6/14 gruppi; la topologia non diverge mai. Le weed
medie di picco sono 34,29 e la media economica è 9.812,46.

Punto di forza: controller nativo semplice, deterministico e senza dipendenza
Codex. Lacune: nessun selector opponent-aware, nessun mixed-farming, lifecycle
che trasforma troppa superficie in weed e distanza `10,19×` dal target.

## Requisiti per il prossimo torneo

Una nuova candidate Claude o Copilot non sarà valutata solo sul denaro. Deve
fornire:

1. entry point, config, hash e descrittore indipendenti;
2. snapshot dell'avversario limitato alle feature pubbliche;
3. almeno due regimi con decisione o transizione tracciabile;
4. fixture che producano action stream diversi a parità di seed/seat;
5. divergenza topologica o di allocazione del lavoro quando causalmente
   prevista, non semplice variabilità terminale;
6. zero errori, fallback e perdite verificate;
7. lifecycle `KEEP/HARVEST/DIG/REPLANT`, con weed exit e resa per harvest;
8. confronto per classe di avversario e non solo media aggregata;
9. nessun uso di holdout/final senza autorizzazione.

## Artefatti

- JSON: `experiments/e18/artifacts/derived/common/E18_DYNAMIC_ARCHITECTURE_TOURNAMENT_V1.json`;
- CSV: `experiments/e18/artifacts/derived/common/E18_DYNAMIC_ARCHITECTURE_TOURNAMENT_V1.csv`;
- runner: `experiments/e18/tools/common/run_e18_dynamic_architecture_tournament_v1.py`;
- candidate: `src/agricola/strategy/codex/codex_e18_opponent_reactive_topology.py`;
- config: `docs/model_specs/codex/e18/configs/CODEX_E18_1_OPPONENT_REACTIVE_662_770_V1.json`;
- standalone: `submission/submission_codex_e18_opponent_reactive_662_770.py`;
- SHA-256 standalone: `06727C1673EC289A323CE403596FAB8B272539535D27C9CEE74B8C917B78791B`;
- parità: 719/719 contro Claude (`6-6-2`) e 719/719 contro Copilot
  (`7-7-0`), import isolato PASS.

