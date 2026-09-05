# E18 — formato standard di confronto tra agenti V2

Per i nuovi report usare [V3](E18_AGENT_COMPARISON_REPORT_STANDARD_V3_IT.md):
solo Top770 vs versione sotto esame, WATER/FEED giornalieri e niente diagramma
Cause PASS. V2 resta conservato come definizione storica dei pannelli 1–19.

Richiesta del proprietario del 2026-09-05: estendere il
[formato V1](E18_AGENT_COMPARISON_REPORT_STANDARD_V1_IT.md) con cinque grafici
diagnostici. Le definizioni, le tabelle operative e i limiti del V1 restano
validi. Ora il formato standard comprende **19 pannelli**, tutti visibili.

Ai quattordici pannelli V1 aggiungere nell'ordine:

| N. | Chiave | Definizione |
|---:|---|---|
| 15 | MOVE | Comandi direzionali per giornata esecutiva, somma di tutte le unità |
| 16 | PASS | Comandi PASS per giornata esecutiva, somma di tutte le unità |
| 17 | unwatered_tiles_h24 | Tile PLANT con watered_today falso al checkpoint H24 |
| 18 | verified_animal_losses | Perdite reali al refresh, verificate sul post-azioni e attribuite al giorno di servizio precedente |
| 19 | weed_tiles | Tile WEED presenti al checkpoint H24 |

MOVE/PASS e perdite sono flussi giornalieri, non cumulate. Non irrigate e
WEED sono consistenze. D1-D29 H24 precede l'ultimo batch: una tile non
irrigata al checkpoint può ancora ricevere WATER nel batch conclusivo.
Non chiamare questo numero "morti per sete" o "scadenze mancate certe".
Conservare anche `water_stressed_tiles_h24` nel dataset per approfondimento.

Il grafico delle perdite non confonde i trasferimenti tile→shed/inventario
con fughe. Nell'audit del motore, il confronto è tra stato dopo le azioni
delle unità e stato dopo il refresh; gli spostamenti volontari sono già
applicati. Per motori diversi rivalidare questa classificazione.

Le WEED possono derivare da spawn spontaneo, starvation o scadenza naturale
delle colture: il solo conteggio non dimostra la causa. Approfondire il
lifecycle quando un incremento è rilevante per la decisione economica.

Implementazione comune:
`experiments/e18/tools/common/replay_daily_operational_kpi.py`.
Nessun cambiamento automatico a policy, pool di seed, stato di promozione o Git.
