# E17.2 — Ablation isolata dell'handoff D27

Data: 2026-09-02

Ruolo evidenza: `DEVELOPMENT_ONLY`

Verdetto: `FAIL — D27_REJECTED / V4D_D28_RETAINED`

## Sintesi

L'anticipo integrale del dispatcher V4D da D28 a D27 è tecnicamente valido ma
economicamente regressivo. La candidata D27 ottiene `133.290,33` contro
`135.096,83` del controllo D28: `−1.806,50` (`−1,337%`). Tutti i sei
confronti matched sono negativi.

I gate di sicurezza, tracciabilità, attivazione ed efficienza relativa passano;
falliscono i due gate economici. In base alla preregistrazione, D27 non viene
sottoposta allo stress multi-regime e non sostituisce V4D D28.

## Disegno

- tre seed development, entrambi i seat;
- candidata D27 e controllo V4D D28;
- avversario inerte;
- 12 episodi e 6 coppie matched;
- unica differenza funzionale di config: `activation_day 28 → 27`;
- nessun seed holdout/final, nessuna submission.

Il loader della candidata confronta la config con V4D e rifiuta qualsiasi
altra mutazione funzionale.

## Risultati matched

| Seed | Seat | D27 | D28 | Delta | Delta % |
|---:|---:|---:|---:|---:|---:|
| 26090101 | 0 | 182.156 | 184.546 | −2.390 | −1,295% |
| 26090101 | 1 | 182.156 | 184.546 | −2.390 | −1,295% |
| 26090102 | 0 | 121.296 | 123.643 | −2.347 | −1,898% |
| 26090102 | 1 | 121.296 | 123.643 | −2.347 | −1,898% |
| 26090103 | 0 | 78.885 | 79.116 | −231 | −0,292% |
| 26090103 | 1 | 113.953 | 115.087 | −1.134 | −0,985% |

## Effetto operativo

| Metrica | D27 | V4D D28 | Differenza |
|---|---:|---:|---:|
| MOVE | 3.061 | 2.134 | +927 |
| servizi | 1.175 | 743 | +432 |
| MOVE/service | 2,605 | 2,872 | −0,267 |
| HARVEST | 443 | 395 | +48 |
| WATER | 238 | 72 | +166 |
| FEED | 228 | 114 | +114 |
| DROP | 216 | 138 | +78 |
| ledger unità | 4.962 | 3.198 | +1.764 |
| market batch | 84 | 71 | +13 |
| unità SELL richieste | 683 | 706 | −23 |

Il rapporto MOVE/service migliora, ma non perché venga svolto meno lavoro: il
dispatcher prende controllo per 24 ore aggiuntive e genera molti più servizi
e MOVE. L'aumento dell'attività non si traduce in reward.

## Diagnosi causale

L'effetto strutturale è perfettamente coerente in tutte le coppie:

- livestock finale invariato: Q0/Q1/Q2 = `8/6/5`;
- massimo hands invariato: `12`;
- crop Q1 e Q2 invariati;
- D27 termina con **una crop Q0 in meno in 6/6 casi**.

Il controllo lascia ancora al provider V9 la giornata 27, durante la quale la
routine completa un'azione strutturale/di coltivazione che l'handoff integrale
sopprime. La candidata compensa con più WATER, FEED e HARVEST, ma richiede 23
unità SELL in meno e non recupera il valore della tile Q0 perduta.

Questa è la distinzione importante: anticipare il controllo state-driven non
equivale automaticamente a diventare più reattivi. Se il dispatcher sostituisce
azioni strutturali ancora valide del provider, l'adattamento locale distrugge
valore pianificato.

## Sicurezza

- errori, fallback e action shape invalide: `0`;
- fughe animali: `0`;
- perdite crop EOD: `77`, identiche al controllo;
- residui vendibili terminali: `0`;
- violazioni non-SELL: `0`;
- ledger unità e mercato: copertura `100%`;
- action stream divergenti: `6/6`;
- esiti unitari D27: 4.085 `EXECUTED`, 5 `NOT_EXECUTED`, 872 `UNKNOWN`.

## Gate

Passano tutti i gate tecnici, il floor matched `≥ −2%`, il costo relativo e la
prova di attivazione. Falliscono:

- `mean_reward_not_below_v4d_d28`;
- `at_least_four_of_six_matched_nonnegative` (`0/6`).

Verdetto complessivo: `FAIL`.

## Decisione successiva

V4D D28 resta la candidata interna congelata. Un nuovo tentativo D27, se
autorizzato, dovrà essere selettivo: preservare le azioni strutturali utili del
provider e applicare il routing state-driven solo dove un fatto osservato
giustifica l'override. Non è ammesso rilassare i gate né correggere la soglia
post-hoc.

## Artefatti

- piano:
  `experiments/e17/design/E17_CODEX_D27_HANDOFF_ABLATION_PLAN_V1.md`;
- config:
  `experiments/e17/configs/codex/CODEX_E17_2_POST_FEED_CAPACITY_BATCHED_ROUTING_V5_D27.json`;
- sorgente:
  `src/agricola/strategy/codex/codex_e17_post_feed_capacity_routing_v5_d27.py`;
- runner:
  `experiments/e17/tools/codex/run_codex_e17_d27_handoff_ablation_development.py`;
- metriche:
  `experiments/e17/artifacts/derived/codex/E17_2_D27_HANDOFF_ABLATION_DEVELOPMENT_METRICS.json`.
