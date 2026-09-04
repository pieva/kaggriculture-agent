# E18.2 — analisi dei replay Kaggle recenti

## Verdetto

La submission `submission_codex_e18_2_capacity_governed_v4d.py` è completa a
`1215,9`, sopra V4D (`1131,7`, `+7,44%`) e sopra E18.1 (`853,6`). Il rating
conferma il vantaggio economico esterno di E18.2 rispetto ai controlli
precedenti, ma i replay recenti mostrano che il vantaggio non deriva ancora da
una risposta strutturale all'avversario.

Negli otto incontri più recenti visibili al 2026-09-04 la submission è `3-5`.
I quattro replay più recenti sono stati verificati integralmente: schema valido,
720 step, stato `DONE/DONE`, Episode ID coerente e stato terminale per entrambi i
player. Sono evidenza diagnostica esterna, non holdout.

## Corpus analizzato

| Ora CEST | Episode | Seat | Avversario | Esito | Codex | Avversario | SHA-256 |
|---|---:|---:|---|---|---:|---:|---|
| 06:55 | `105365487` | P1 | Victor Hotz | WIN | 84.131 | 65.279 | `A37225AD492D717562780627F04407A193F970E5EBEA0897EC6269E655DEBDE3` |
| 06:16 | `105355836` | P0 | Emre Kurubaş | LOSS | 49.202 | 59.609 | `4C4B3DAD13B5830F90F1DE372152DC0607851E963B68D44617985276CD221D8F` |
| 04:26 | `105331333` | P1 | moonzfxs | LOSS | 73.514 | 79.208 | `708F38AA0675C7CB744FDD8C39AAB6756E6226D628C6591B6934C41EF9F55874` |
| 03:54 | `105323917` | P1 | moonzfxs | WIN | 56.272 | 55.493 | `942FEFC8098BB94A7C70FF4876611B084561E8827528276C6CA1427D13BAB3E1` |

Il campione chiude `2-2`, con score medio Codex `65.779,75`, score medio
avversario `64.897,25` e margine medio `+882,5`. La coppia contro moonzfxs è
particolarmente utile: lo stesso avversario e la stessa topologia `6-6-2`
producono un win e un loss senza una risposta apprezzabile della struttura
Codex.

## Profilo strutturale

E18.2 è quasi invariabile nei quattro replay:

- topologia finale sempre `7-7-5`, con `19` pascoli, `18` animali e `10` hands;
- `596-602` unità raccolte, media `599,75`;
- `2,582-2,603` unità per harvest, media pesata `2,588`;
- `3.590-3.595` movimenti, media `3.592,25`;
- `686-695` PASS, media `690`;
- `121` PASS su tile già pronto per `HARVEST` in ogni replay;
- `119` transizioni di raccolta e `39` uscite a weed per episodio;
- `226-231` late unwatered tile-days, media `228,75`.

Gli avversari coprono invece tre geometrie: `6-7-0`, `6-0-6` e `6-6-2`.
Hanno in media meno pascoli (`13,25`) e workforce simile (`9,5` hands), ma
raccolgono `814` unità medie. Il confronto aggregato è:

| KPI medio | E18.2 | Avversari | Delta E18.2 |
|---|---:|---:|---:|
| Harvested units | 599,75 | 814,00 | `-26,32%` |
| Harvest transitions | 119,00 | 148,25 | `-19,73%` |
| Crop-service actions | 1.490,00 | 1.602,25 | `-7,01%` |
| Move actions | 3.592,25 | 3.503,25 | `+2,54%` |
| PASS | 690,00 | 539,00 | `+28,01%` |
| Late unwatered tile-days | 228,75 | 173,50 | `+31,84%` |
| Weed exits | 39,00 | 22,00 | `+77,27%` |

## Diagnosi

La capacità nominale non è il vincolo: Codex dispone di almeno altrettanti
worker e di più superficie zootecnica. Il vincolo è la conversione della
capacità in servizio colturale. E18.2 conserva la traiettoria V4D quasi
open-loop; la recovery locale corregge alcuni PASS, ma non cambia ownership,
sequenza di servizio o allocazione del lavoro quando l'avversario adotta una
geometria diversa.

Il risultato esterno converge con la diagnosi locale di E18.4 V1:

- E18.4 dimostra che `7-7-2` è costruibile e sicura, ma il dispatcher globale
  produce `+29,35%` move e `-20,95%` productive;
- E18.2 evita quella regressione, ma resta ferma a circa 600 unità raccolte e
  accumula backlog di harvest e acqua;
- gli avversari più produttivi usano meno pascoli, ma il vantaggio osservato è
  spiegato da rotazione e servizio, non dalla geometria da sola.

La prossima candidate non deve quindi modificare topologia, mercato o batching.
Deve sostituire esclusivamente l'assegnazione globale greedy con un dispatcher
persistente e locale. La specifica è in
`docs/model_specs/codex/MODEL_SPEC_CODEX_E18_4_STATE_DRIVEN_772_V2.md`.

## Evidence boundary

- la lista Kaggle e il rating sono snapshot esterni del 2026-09-04;
- i quattro replay sono `EXTERNAL_DIAGNOSTIC_NOT_HOLDOUT`;
- nomi, rating, Episode ID e memoria cross-episode non sono feature ammesse;
- nessun holdout/final è stato consumato;
- nessuna nuova submission è autorizzata da questa analisi.
