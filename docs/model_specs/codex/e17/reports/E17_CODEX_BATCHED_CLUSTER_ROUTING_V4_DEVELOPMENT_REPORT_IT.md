# E17.2 — batching, cluster e capacità shed: report V4

- **Data:** 2026-09-02
- **Ruolo evidenza:** `DEVELOPMENT_ONLY`
- **Controllo:** `CODEX-E17.2-REACTIVE-SERVICE-ROUTING-CORE-V3-D28`
- **Candidata promossa internamente:** `CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28`
- **Holdout/final confirmation:** non usati
- **Kaggle:** nessuna submission preparata o caricata

## 1. Domanda causale

La V3 ha raggiunto equivalenza economica con un dispatcher realmente
state-driven, ma impiega tre MOVE per servizio. Questo round verifica
se sia possibile raccogliere più output per viaggio senza perdere vendite,
saturare lo shed o compromettere il servizio biologico.

L'engine non impone una capacità massima agli inventari dei worker. La soglia
corretta non è quindi un numero arbitrario di oggetti trasportati, ma la
pressione aggregata sulla capacità finita dello shed e lo slack necessario a
completare `HARVEST→rientro→DROP`.

## 2. Ablation eseguite

| Variante | Trattamento | Media | Delta di riferimento | MOVE/servizio | Verdetto |
|---|---|---:|---:|---:|---|
| V3 | rientro immediato | 134.351,33 | — | 3,000 | controllo |
| V4A | batching EOD/deadline | 130.953,00 | −2,529% vs V3 | 2,676 | FAIL |
| V4B | V4A + affinità quadrante | 130.954,33 | +0,001% vs V4A | 2,682 | FAIL |
| V4C | V4A + trigger capacità, carrier Wheat sempre protetti | 130.953,00 | −2,529% vs V3 | 2,676 | FAIL |
| **V4D** | **V4C + rilascio carrier dopo feed completo** | **135.096,83** | **+0,555% vs V3** | **2,872** | **PASS** |

V4B dimostra che una preferenza topologica debole non produce il guadagno:
riduce marginalmente il tasso di cambio cluster, ma aggiunge quattro MOVE e
non modifica materialmente il reward. Non viene incorporata nella candidata.

## 3. Perché V4A fallisce

Sul seed diagnostico `26090101`, immediatamente prima dell'EOD D28:

| Stato | V3 | V4A |
|---|---:|---:|
| Denaro | 163.026 | 156.717 |
| Unità nello shed | 43 | 41 |
| Unità nei worker | 51 | 98 |
| Carico potenziale complessivo | 94 | 139 |

Lo shed può contenere 100 unità. Il deposito EOD della V4A può quindi
conservare soltanto 59 delle 98 unità trasportate e scarta l'overflow. La
riduzione dei MOVE è reale, ma deriva da un batching incompatibile con il
vincolo di stoccaggio.

## 4. Perché V4C non si attiva

V4C introduce il trigger a 85% e un target post-vendita al 50% della capacità.
Il trigger scatta in tutti i sei episodi candidati, ma i worker con output
trasportano anche Wheat. La protezione assoluta dei carrier produce zero DROP
D28 e zero batch attivi: V4C resta comportamentalmente equivalente a V4A.

Questo è un risultato causale utile: il vincolo non è la mancanza del segnale
di capacità, ma l'estensione temporale eccessiva della guardia Wheat.

## 5. Meccanismo V4D

V4D mantiene protetti i carrier finché almeno un animale nello snapshot D28
risulta non alimentato. Quando tutti gli animali hanno `fed_today == true`, il
Wheat residuo non ha più uso biologico nel giorno e il carrier può rientrare.

Il flush usa isteresi:

1. `shed + inventari droppabili >= 85` attiva il rientro;
2. durante l'avvicinamento, vendite coordinate liberano spazio nello shed;
3. il latch resta attivo fino al deposito;
4. il market considera anche i DROP eseguiti nello stesso batch;
5. D29 continua a raccogliere finché il percorso completo verso lo shed è
   compatibile con la deadline.

Acquisti, HIRE, unlock, topologia, composizione Q2 e ordini non-SELL restano
invariati.

## 6. Risultati matched V4D

| Seed | Seat | V4D | V3 | Delta |
|---:|---:|---:|---:|---:|
| 26090101 | 0 | 184.546 | 183.784 | +762 |
| 26090101 | 1 | 184.546 | 183.784 | +762 |
| 26090102 | 0 | 123.643 | 122.757 | +886 |
| 26090102 | 1 | 123.643 | 122.757 | +886 |
| 26090103 | 0 | 79.116 | 78.436 | +680 |
| 26090103 | 1 | 115.087 | 114.590 | +497 |

Il delta è positivo in `6/6` confronti. La media sale da `134.351,33` a
`135.096,83`: `+745,50`, pari a `+0,555%`.

## 7. Efficienza e sicurezza

| Indicatore | V4D | V3 | Delta |
|---|---:|---:|---:|
| MOVE | 2.134 | 2.256 | −122 |
| Servizi | 743 | 752 | −9 |
| MOVE/servizio | **2,872** | 3,000 | −4,26% |
| HARVEST | 395 | 331 | +64 |
| DROP totali | 138 | 205 | −67 |
| DROP D28 | 72 | 66 | +6 |
| HARVEST con inventario positivo | 161 | 0 | +161 |
| Crop loss EOD derivate | 77 | 77 | 0 |
| Fughe EOD strette | 0 | 0 | 0 |
| Residuo vendibile terminale | 0 | 0 | 0 |

I 251 rilasci post-feed sono decisioni worker-callback osservate durante i
percorsi, non 251 DROP fisici. I 12 eventi di trigger producono 36 batch di
flush attivi.

Il ledger unità copre `3198/3198` record; quello market `71/71`. Gli outcome
unità sono 2.796 `EXECUTED`, 402 `UNKNOWN`, zero `NOT_EXECUTED`. Gli outcome
market sono 62 `EXECUTED`, 9 `UNKNOWN` terminali e zero `NOT_EXECUTED`.
Errori, fallback, forme invalide e violazioni degli ordini non-SELL sono zero.

## 8. Decisione

Tutti i gate preregistrati V4D passano. V4D sostituisce V3 come candidata
interna E17.2. Le V4A, V4B e V4C restano evidenza negativa e non devono essere
presentate come candidate.

Il risultato non autorizza ancora D27 o Kaggle. Il prossimo esperimento deve
mantenere congelata V4D e stressarla nei regimi development controllati di
scarsità Wheat, pressione sugli output e liquidità. Solo se il vantaggio
logistico non diventa una regressione sistematica in quei regimi si potrà
considerare un handoff più precoce.

## 9. Artefatti

- piano: `docs/model_specs/codex/e17/design/E17_CODEX_BATCHED_CLUSTER_ROUTING_PLAN_V1.md`;
- policy: `src/agricola/strategy/codex/codex_e17_batched_cluster_routing_v4.py`;
- config promossa: `docs/model_specs/codex/e17/configs/CODEX_E17_2_POST_FEED_CAPACITY_BATCHED_ROUTING_V4D_D28.json`;
- test: `docs/model_specs/codex/e17/tests/test_codex_e17_batched_cluster_routing_v4.py`;
- runner V4D: `docs/model_specs/codex/e17/tools/run_codex_e17_post_feed_capacity_routing_v4d_development.py`;
- metriche V4D: `docs/model_specs/codex/e17/artifacts/derived/E17_2_POST_FEED_CAPACITY_ROUTING_V4D_DEVELOPMENT_METRICS.json`;
- metriche V4A/V4B: `docs/model_specs/codex/e17/artifacts/derived/E17_2_BATCHED_CLUSTER_ROUTING_V4_DEVELOPMENT_METRICS.json`;
- metriche V4C: `docs/model_specs/codex/e17/artifacts/derived/E17_2_CAPACITY_AWARE_BATCHED_ROUTING_V4C_DEVELOPMENT_METRICS.json`.
