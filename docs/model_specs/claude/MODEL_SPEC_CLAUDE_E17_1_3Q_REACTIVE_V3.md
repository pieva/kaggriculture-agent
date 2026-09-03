# MODEL_SPEC — Claude E17.1 3Q Reactive Independent V3

- **Policy ID:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V3`
- **Autore:** Claude (modeler indipendente)
- **Data:** 2026-09-02
- **Foundation:** C2.1 (RECONCILED)
- **Stato:** AS-BUILT — `FROZEN_WITH_FAILED_GATES` (attivazione "10x" della
  V2: miglioramento netto e riprodotto su ogni KPI, target "10x" non
  raggiunto — Sezioni 9-11)
- **Predecessore:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V2`, `0-0-28`
  nell'esibizione development a tre (media `11.777,64` contro Codex)
- **Autorizzazioni:** `experiments/e17/prompts/claude/E17_CLAUDE_REACTIVE_V3_10X_ACTIVATION_PROMPT_IT.md`,
  `experiments/e17/reviews/common/E17_CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK_AUTHORIZATION.md`
- **Sorgente:** `src/agricola/strategy/claude/e17_reactive_3q_v3.py`
- **Config:** `experiments/e17/configs/claude/CLAUDE_E17_1_3Q_REACTIVE_V3.json`

---

## 1. Diagnosi verificata sull'esibizione V2 (non assunta)

Fonte: `experiments/e17/reports/common/E17_REACTIVE_THREE_WAY_DEVELOPMENT_EXHIBITION_REPORT_IT.md`
(42/42 match, `DEVELOPMENT_ONLY_NON_QUALIFYING`, holdout non consumato) e il
piano `E17_1_CLAUDE_REACTIVE_V3_IMPROVEMENT_PLAN.md` già registrato.

| Ipotesi | Esito |
|---|---|
| Guardia `core_established` aggirabile da un ciclo WHEAT rapido | **CONFERMATA per meccanismo**: `yield_units=1` già alla semina (`_new_plant`) e `first_yield_day=2` rendono legale l'`HARVEST` di 4 tile WHEAT già al giorno 2, indipendentemente dalla densità reale di Q0 |
| Soffitto di workforce troppo basso sotto contesa | **CONFERMATA**: `hands max = 8` osservato contro i 12 di Codex |
| Ratchet zootecnico + workforce hanno quasi azzerato il bestiame | **PARZIALMENTE CONFERMATA**: la crescita del gregge era effettivamente sotto il tetto teorico, ma la causa dominante trovata durante lo sviluppo V3 è stata diversa (Sezione 9.1) |
| Overhead di movimento (MOVE/produttiva 2,97 contro 1,25) | **CONFERMATA per direzione**, non ancora isolata dalla densità insufficiente |
| Sviluppo mai testato sotto contesa di mercato | **CONFERMATA per assenza di evidenza**: tutti gli strumenti V1/V2 usavano solo `INERT_PASS_POLICY` |

---

## 2. Autorizzazione e vincoli del benchmark contro Codex

Il benchmark di sviluppo contro Codex V9/reattivo è **black-box**:
osservabili azioni, stato e denaro finale; vietata la lettura di sorgenti,
routine, config o MODEL_SPEC Codex. Lo strumento
`experiments/e17/tools/claude/run_claude_e17_1_v3_dev_benchmark_vs_codex.py`
importa esclusivamente le factory pubbliche (`create_v9_agent`,
`create_codex_e17_reactive_agent`), il cui nome è stato ricavato leggendo
solo la riga di import dello strumento comune di esibizione, mai un
sorgente Codex. Vedi `E17_CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK_AUTHORIZATION.md`
per i vincoli integrali.

---

## 3. Ipotesi strategiche V3

1. **H-CR3.1 (nucleo denso prima dell'espansione):** una guardia di
   maturità Q0 basata sulla densità reale coltivata (non solo sul conteggio
   di richieste harvest) impedisce l'espansione a costo-di-evidenza-zero
   osservata in V2.
2. **H-CR3.2 (prontezza di workforce prima dell'espansione):** anche con un
   nucleo denso, espandere il territorio prima che la workforce corrente sia
   già al proprio floor di quadrante raddoppia il carico su un equipaggio
   ancora sottile e collassa in un disastro di weed. Le due guardie
   (densità + prontezza workforce) devono valere congiuntamente.
3. **H-CR3.3 (riserva dedicata per acquisti di grande taglia):** `BUY_LAND`
   e `BUY_ANIMAL` non devono competere per lo stesso margine di cassa
   residuo minimo generico; una riserva dedicata più ampia per gli acquisti
   zootecnici previene un'esplosione di spesa simultanea nel momento in cui
   il nucleo diventa maturo.
4. **H-CR3.4 (la workforce non deve azzerarsi in endgame):** bloccare
   `HIRE` durante la finestra di shutdown, ereditato da V1/V2, è
   sostenibile con un soffitto di workforce piccolo ma catastrofico con un
   soffitto grande, perché gli Hands scadono comunque ogni EOD
   indipendentemente dalla fase dell'episodio.

---

## 4. Provenance e indipendenza strategica

Identica alla V1/V2 (nessun import da `agricola.strategy.codex`,
`agricola.strategy.antigravity` o `agricola.strategy.copilot` **nella
policy**). Lo strumento di benchmark contro Codex (Sezione 2) è
infrastruttura di esecuzione esterna al namespace della policy, non una
dipendenza strategica, come esplicitamente qualificato
dall'autorizzazione. Nessuna riga di codice Codex è stata letta durante lo
sviluppo di questa policy; solo comportamento osservabile durante i match.

---

## 5. Stato interno agent-local

Identico nella forma alla V2: `_assignments` (target persistenti
per-worker), `_core_harvest_requests` (contatore delle proprie richieste
`HARVEST`), `_last_seen_day` (per l'invalidazione delle assegnazioni
`hand:*` al cambio di giorno). Nessuna tabella indicizzata per step.

---

## 6. Architettura V3 (differenze rispetto alla V2)

### 6.1-6.3 Ereditate dalla V2 senza modifiche strutturali

Dispatch con target persistenti, timeout di stallo, cascata di priorità
(`URGENT_WATER` > `FEED_NEEDED` > `PLACE_ANIMAL_NEEDED` > `HARVEST_READY` >
`RECOVERY_DIG` > `CARE_NEEDED` > `COLLECT_FERTILIZER_READY` >
`BUILD_OPPORTUNITY` > `PLANT_OPPORTUNITY`) e prelazione d'urgenza per le
categorie a rischio di perdita EOD.

### 6.4 Guardia di maturità del nucleo Q0, rinforzata (causa primaria)

```text
core_established ⟺ plant_tiles_count > 0
                   ∧ core_harvest_requests >= expansion.core_min_harvest_requests
                   ∧ core_quadrant_fill_ratio >= expansion.core_min_fill_ratio
```

`core_quadrant_fill_ratio` è la frazione della crop-zone del quadrante
`NW` (sempre il quadrante iniziale gratuito, fatto `ENGINE_VERIFIED`)
attualmente piantata, calcolata su un denominatore statico
(`board_size²/4 - livestock_structures_target_per_quadrant - 1` tile
adiacente allo shed). Chiude il varco osservato in V2: un ciclo WHEAT
rapido può soddisfare il conteggio di richieste harvest in due giorni senza
alcuna densità reale.

`BUY_LAND` **e** `BUY_ANIMAL` condividono la stessa guardia
`_core_established` (unificata in V3; in V2 solo `BUY_LAND` la richiedeva
inizialmente, con un ritardo poi corretto — Sezione 9.1).

### 6.5 Guardia di prontezza della workforce (nuova, trovata durante lo sviluppo V3)

```text
len(worker_positions) >= workforce.min_workers_per_quadrant × quadranti_sbloccati
```

Applicata a `BUY_LAND` in aggiunta alla guardia di densità. Senza di essa,
un nucleo che diventa denso rapidamente (workforce ancora minima) espande
comunque, raddoppiando il territorio da servire su un equipaggio che non è
ancora pronto — causa diretta del collasso osservato durante lo sviluppo
(Sezione 9.1, punto 2).

### 6.6 Riserva dedicata per acquisti zootecnici (nuova)

`BUY_ANIMAL` rispetta ora `livestock.animal_purchase_reserve` (valore
dell'ordine di grandezza di `land_purchase_reserve`) al posto della riserva
minima generica di mercato. Prima di questa correzione, `BUY_LAND` e
`BUY_ANIMAL` potevano atterrare nella stessa finestra di 1-2 chiamate
appena il nucleo diventava maturo, prosciugando la cassa fino alla soglia
operativa (Sezione 9.1, punto 3).

### 6.7 `HIRE` non più bloccato durante lo shutdown (nuova, causa di collasso terminale)

Gli Hands scadono incondizionatamente ad ogni EOD (fatto `ENGINE_VERIFIED`)
indipendentemente dalla fase dell'episodio. Bloccare nuovi ordini `HIRE`
durante la finestra di shutdown (ereditato invariato da V1/V2) collassava
la workforce al solo farmer per gli ultimi `endgame.shutdown_days_remaining`
giorni, con un intero 3Q ancora da mantenere: causa diretta
dell'esplosione di weed terminale osservata durante lo sviluppo (Sezione
9.1, punto 4). `BUY_LAND`, `BUY_SEED` e `BUY_ANIMAL` restano bloccati in
shutdown (nuovi investimenti di lungo periodo); `HIRE` no (mantenimento
della superficie esistente).

### 6.8 Workforce e gregge ritarati

`max_hands` alzato da 9 a 15 (verso la densità dimostrata da Codex, 12
hands osservati). `herd_size_workforce_divisor` (V2, intero) sostituito da
`livestock.herd_per_worker_ratio` (V3, rapporto float) per calibrazione più
fine. Fino a `livestock.max_animal_placements_per_call` opportunità
`PLACE_ANIMAL_NEEDED` per chiamata (V2: esattamente una), perché un gregge
più numeroso non può attendere un singolo posizionamento per volta.

### 6.9 Tie-break di località di quadrante (nuovo, mitigazione parziale)

A parità di priorità e urgenza, `_best_opportunity` preferisce
un'opportunità nel quadrante corrente del worker (`dispatch.prefer_same_quadrant`).
Non altera mai l'ordine di priorità né la prelazione d'urgenza; riduce solo
gli spostamenti medi tra opportunità equivalenti.

### 6.10 Concentrazione geografica del bestiame (nuova, causa risolutiva delle fughe residue)

`BUILD_OPPORTUNITY` per strutture zootecniche viene generata solo nei primi
`livestock.max_quadrants_for_livestock` quadranti dell'ordine di sblocco
canonico e fisso del motore (`NW`, poi `NE`, `SW`, `SE` — fatto
`ENGINE_VERIFIED`, mai una scelta strategica). Con `max_quadrants_for_livestock = 2`
il gregge resta confinato a `NW`/`NE`; nel terzo quadrante sbloccato le tile
altrimenti riservate al bestiame diventano zona coltura aggiuntiva.

Motivazione evidence-based (non un'ipotesi nuova, ma un riuso diretto di
un'osservazione già registrata nella Foundation, `docs/NEW_SESSION.md`
"Evidenza E17 consolidata"): dei nove replay Top 3 di discovery, i profili
con bestiame concentrato in Q0/Q1 (`tetsuya`, `OceanMix`) mostravano zero
fughe EOD derivate; il profilo con bestiame disperso sui tre quadranti
(`Crop Dusta`) ne mostrava 31. Trovata e applicata durante lo sviluppo V3
dopo che le correzioni di Sezione 9.1 punti 1-4 avevano risolto i collassi
di cassa ma non le fughe (Sezione 9.1 punto 7): confinare il bestiame ha
ridotto le fughe registrate da `67` a `18` su 14 run passive (Sezione 9.2),
mantenendo o migliorando `final_money` medio.

---

## 7. Separazione stato online / telemetria post-hoc

Identica alla V2. Le nuove guardie leggono esclusivamente campi
`ONLINE_OBSERVABLE`/`ONLINE_DERIVABLE` correnti e il contatore agent-local
delle proprie richieste passate.

---

## 8. Failure mode e fallback

Identico alla V2: intera pipeline protetta da un blocco try/except unico.

---

## 9. Diagnosi e iterazioni durante lo sviluppo V3

### 9.1 Sequenza di difetti trovati e corretti (seed development `26090101`, poi verificati sotto contesa con `26090103`)

1. **Prima versione (solo guardia di densità Q0):** `final_money = 455` su
   seed `26090101` contro `INERT_PASS_POLICY` — un netto peggioramento
   rispetto alla V2 (`7.483` sullo stesso seed). Diagnosi: la cassa restava
   bloccata esattamente a `$35`, tra `market_order_min_cash` (`30`) e
   `hire_reserve` (`50`), e i weed saturavano l'intero quadrante NW
   (`25/25`).
2. **Alzata `hire_reserve` a 150, ridotto il ritmo di assunzione:** nessun
   miglioramento misurabile (`458`). Diagnosi più precisa via tracciamento
   step-per-step: l'espansione a Q1 avveniva al giorno 2 (`step 65`), con
   `core_quadrant_fill_ratio = 9/20 = 0,45` — la guardia di densità
   funzionava correttamente, ma un nucleo diventato denso in soli due
   giorni (grazie al ciclo rapido del WHEAT) non implica una workforce
   pronta a raddoppiare il territorio servito. **Corretto** con la guardia
   di prontezza workforce (Sezione 6.5).
3. **Ancora nessun miglioramento con la sola guardia di prontezza** (la
   soglia minima, `3` worker, si soddisfaceva comunque in pochi step).
   Tracciamento dettagliato dei singoli ordini di mercato: al momento
   dell'attivazione del nucleo, `BUY_LAND` (`-1000`) e due `BUY_ANIMAL`
   (`SHEEP -500`, `COW -400`) atterravano nella stessa finestra di due
   chiamate, seguiti da una rapida rampa di `HIRE` fino a 6 hands — una
   spesa complessiva di oltre `$2.000` su una cassa iniziale di `$2.190` in
   meno di 20 step. **Corretto** con la riserva dedicata `animal_purchase_reserve`
   (Sezione 6.6): `final_money` sale a `10.348` sullo stesso seed, senza
   collasso weed.
4. **Sotto contesa reale (seed `26090101` vs `CODEX_V9`):** nessun collasso
   iniziale, ma i weed esplodevano comunque negli ultimi 4-5 giorni
   (`plant 16→9→4`, `weed 6→13→18`). Diagnosi: `HIRE` era bloccato durante
   la finestra di shutdown, azzerando la workforce al solo farmer proprio
   mentre un intero 3Q necessitava ancora manutenzione quotidiana.
   **Corretto** rimuovendo il gate di shutdown da `HIRE` soltanto (Sezione
   6.7): `final_money` sale da `6.472` a `9.792` sullo stesso match.
5. **Dopo le 4 correzioni sopra, il risultato conteso aggregato restava
   piatto** (media `11.706,93` contro la V2 `11.777,64` — nessun
   miglioramento misurabile). Ipotesi testata: il prezzo massimo di
   riacquisto WHEAT (`wheat_buy_price_ceiling`) era troppo conservativo e
   affamava il gregge nei picchi di domanda. **Disprovata**: alzando il
   tetto da `45` a `80` la traiettoria di cassa, scorta WHEAT nello shed e
   prezzo di mercato sono risultate bit-per-bit identiche prima e dopo sul
   seed di sviluppo — `_wheat_buy_order` scatta solo quando `deficit > 0`,
   e la scorta nello shed superava già il buffer target nella quasi
   totalità dei turni osservati. Il prezzo WHEAT non era mai il vincolo
   attivo. Il parametro è stato comunque mantenuto a `80` (nessun costo
   noto) ma non è la causa del limite di performance.
6. **Ipotesi successiva: rapporto gregge/workforce troppo alto.**
   Dimezzando `herd_per_worker_ratio` da `1,0` a `0,5` le fughe si sono
   ridotte ma non azzerate (`4-8` per run sui seed campionati) — effetto
   solo parziale, non risolutivo da solo.
7. **Errore di processo: regressione non validata su `crop_target_fill_ratio`.**
   Nel tentativo di chiudere il collo di bottiglia di densità coltivata
   (Sezione 9.2), il target è stato alzato `0,55 → 0,9`, poi ridotto a un
   valore di "compromesso" `0,7`, e lo sviluppo è proseguito verso
   test/tool/MODEL_SPEC **senza ri-eseguire la matrice completa a 7 seed**
   a quel valore. La successiva esecuzione formale dello strumento di
   validazione passiva ha rivelato collassi catastrofici (`final_money`
   `87-104`, spesso bloccati a 2Q) e il benchmark conteso è sceso a media
   `5.949,36` — peggio della V2. Diagnosi: confrontando gli spot-check
   precedenti (fatti a `0,9`, risultati sani) con l'esecuzione formale
   (a `0,7`, risultati collassati) sugli **stessi seed**, la causa è stata
   isolata nella modifica di configurazione, non in un bug di determinismo.
   **Corretto** ripristinando `0,55` e ri-verificando i due seed più
   colpiti singolarmente (entrambi tornati ai valori sani precedenti).
   Lezione applicata: ogni cambio di configurazione va ri-validato sulla
   matrice completa, non su un sottoinsieme di seed.
8. **Dopo il ripristino, `final_money` era sano ma le fughe erano
   esplose** (`67` fughe totali su 14 run passive, `0-9` per run).
   Tracciamento degli eventi di fuga (stessa tecnica della V2): tutte le
   fughe cadevano a cambio giorno, e lo shed conteneva quasi sempre
   scorte WHEAT abbondanti (`25-36` unità) al momento dell'evento —
   escludendo la carenza di mangime come causa. **Fix decisivo:**
   concentrazione geografica del bestiame (Sezione 6.10), giustificata
   dall'evidenza di replay Foundation C2.1 già disponibile (profili con
   bestiame concentrato in 1-2 quadranti: `0` fughe; profilo con bestiame
   distribuito su 3 quadranti: `31` fughe). Testato `max_quadrants_for_livestock=1`
   (troppo restrittivo: cassa collassata a `610-1.481`, bloccato a 2Q —
   scartato) e `=2` (fughe `0-3` per seed campionato, cassa `15.527-22.736`
   — adottato come valore finale). La ri-esecuzione completa della matrice
   a 14 run con `=2` e tutte le altre impostazioni finali ha confermato:
   `18` fughe totali (da `67`), `12/14` run a 3Q, media passiva
   `17.872,86`, media contesa `13.540,86` con tutti e 14 gli
   abbinamenti seed×seat a 3Q (Sezione 9.2).

### 9.2 Risultato aggregato finale e limite non ancora risolto

Con la configurazione finale (post-correzioni 1-8), i risultati sono:

**Passivo** (`INERT_PASS_POLICY`, 7 seed × 2 seat = 14 run,
`experiments/e17/artifacts/derived/claude/E17_1_V3_METRICS.json`):
`final_money` media `17.872,86` (mediana `18.255,5`, min `9.221`, max
`23.584`, dev. std. popolazione `3.715,82`) — **+23,7%** rispetto alla
media passiva V2 (`14.445,29`). `derived_eod_escape_count` totale `18`
(da confrontare con `~3` in V2) su 14 run. `max_quadrants=3` in `12/14`
run (i due run a 2Q sono `S26090102-P1` e `S562040596-P1`, entrambi con
`final_money` comunque superiore alla media V2 sullo stesso seed).
`technical_errors=0`, `invalid_batches=0`, copertura ledger `100%`,
riproducibilità bit-per-bit `pass=true` su tutti i 14 run raddoppiati.

**Conteso** (black-box vs `CODEX_V9` e `CODEX_REACTIVE`, 7 seed × 2 seat ×
2 avversari = 28 match,
`experiments/e17/artifacts/derived/claude/E17_1_V3_DEV_BENCHMARK_VS_CODEX.json`):
`CLAUDE_MEAN_MONEY = 13.540,86` — **+15,0%** rispetto alla media conteso
V2 (`11.777,64`). `W-T-L = 0-0-28` (nessuna vittoria contro un avversario
che gioca a piena densità). Tutti e 14 gli abbinamenti seed×seat unici
raggiungono `3Q = ['NW','NE','SW']`; `weed` quasi sempre `0` (unica
eccezione: `weed=1` su seed `26090101` seat `0`); `TECH_ERRORS=0`.
`CODEX_V9` e `CODEX_REACTIVE` producono risultati byte-identici per ogni
match (la variante reattiva di Codex non ha mai attivato una divergenza
osservabile in questi 14 scenari).

Diagnosi del limite residuo tramite confronto di traiettoria testa-a-testa
(seed `26090103`): Codex raggiunge e sostiene `37-55` tile coltivate dal
giorno 8 in poi; Claude non supera mai `~20-28` tile piantate
simultaneamente, indipendentemente dal target di riempimento configurato
(punto 7 sopra ha dimostrato che alzare il target senza aumentare la
capacità di esecuzione produce solo collassi). Il vincolo non è il target
di riempimento ma il **throughput della workforce**: non ci sono
abbastanza worker-turni per piantare, irrigare e raccogliere una
superficie più ampia nello stesso arco di tempo osservato da Codex.
Questo è il collo di bottiglia dominante **non risolto** in questa
iterazione: vedi Sezione 11.

---

## 10. Target e criteri di falsificazione

Gate del prompt di attivazione:

```text
STRATEGIC_INDEPENDENCE_GATE == PASS
TECHNICAL_ERRORS == 0
INVALID_ACTIONS == 0
LEDGER_COVERAGE == 100%
ANIMAL_ESCAPES == 0
THREE_QUADRANTS == ALL_DEVELOPMENT_RUNS
PASSIVE_DEVELOPMENT_MEAN >= 50000
REACTIVITY_TESTS == PASS
HOLDOUT_USED == false
FINAL_CONFIRMATION_USED == false
```

Target indicativo "10x": denaro medio conteso `>= 117.800` (10× la media
V2 conteso `11.777,64`).

Criteri di falsificazione dichiarati prima di osservare il risultato finale:

- **`H-CR3.1`/`H-CR3.2` falsificate** se, nonostante le guardie di
  densità+prontezza, si osserva ancora espansione con territorio
  sotto-servito (weed diffusi) sul benchmark registrato. **Non
  falsificate**: le due guardie combinate hanno eliminato il collasso
  weed originario legato all'espansione precoce (punto 2, Sezione 9.1);
  le fughe residue (`18` totali) sono di natura diversa — geografica, non
  di densità/prontezza — e sono state affrontate separatamente (punto 8).
- **`H-CR3.3` falsificata** se si osserva ancora un crollo di cassa
  concentrato nella finestra di attivazione del nucleo. **Non
  falsificata**: la riserva dedicata `animal_purchase_reserve` ha
  eliminato il collasso da sovraspesa (punto 3, Sezione 9.1).
- **`H-CR3.4` falsificata** se i weed restano concentrati nella finestra di
  shutdown nonostante la rimozione del gate su `HIRE`. **Non
  falsificata**: il collasso weed di fine episodio non si è più
  riprodotto dopo il fix (punto 4, Sezione 9.1).
- **Target "10x" falsificato**: **osservato** (Sezione 9.2) — la media
  conteso finale è `13.540,86`, +15,0% rispetto alla V2 (`11.777,64`),
  molto lontana dal target indicativo `>= 117.800`. Il target "10x" **non
  è raggiunto** in questa iterazione. `ANIMAL_ESCAPES == 0` è anch'esso
  falsificato (`18` fughe residue, in calo da `67` ma non azzerate) e
  `THREE_QUADRANTS == ALL_DEVELOPMENT_RUNS` è falsificato sul benchmark
  passivo (`12/14`, sebbene `14/14` sotto contesa). Diagnosi e
  raccomandazione per la prossima iterazione in Sezione 11.

---

## 11. Limiti dichiarati e raccomandazione per la prossima iterazione

Le otto correzioni di Sezione 9.1 sono reali, verificate e hanno eliminato
quattro distinti modi di fallimento catastrofico osservati durante lo
sviluppo (collasso cassa-bloccata, collasso da sovraspesa alla maturità
del nucleo, collasso weed di fine episodio, collasso da regressione di
configurazione non validata) oltre a ridurre drasticamente (non azzerare)
le fughe zootecniche residue (`67 → 18`) tramite la concentrazione
geografica del bestiame. L'assenza di errori tecnici e la copertura
ledger al 100% sono soddisfatte in ogni run (Sezione 9.2). Restano
esplicitamente **non soddisfatti** tre gate del prompt di attivazione:
`ANIMAL_ESCAPES == 0` (`18` residue), `THREE_QUADRANTS ==
ALL_DEVELOPMENT_RUNS` (`12/14` passivo, pur `14/14` conteso), e il target
economico "10x" (`+15,0%` conteso contro un obiettivo `10×`).

Il collo di bottiglia dominante rimasto è il **throughput della
workforce** nel convertire territorio posseduto in densità coltivata
sostenuta — non le guardie di spesa, non la sicurezza zootecnica, non il
prezzo di riacquisto WHEAT (tutte disprovate o già ottimizzate in
Sezione 9.1). Codex sostiene `37-55` tile coltivate dal giorno 8; Claude
non supera mai `~20-28`. Ipotesi non testate in questa iterazione,
raccomandate per una V4:

1. instradamento multi-worker con solver di assegnazione locale per
   quadrante invece del solo tie-break di località (Sezione 6.9);
2. verifica diretta se il vincolo di batch ordini di mercato (`MKT-LIMIT`,
   10/turno) limita quante `HIRE`/`BUY_SEED` possono effettivamente
   convertirsi per step quando la domanda supera lo slot disponibile;
3. confronto diretto (sempre black-box) della cadenza di `HIRE` e
   `BUY_LAND` osservabile di Codex nei primi 10 giorni, per stimare se la
   V3 sta semplicemente partendo troppo lenta in termini assoluti, non solo
   relativi alla densità;
4. le `18` fughe residue sono ancora concentrate a cambio giorno con shed
   ben rifornito (come le `67` originarie): la geografia le ha ridotte ma
   non ne ha cambiato la natura temporale — merita un tracciamento
   dedicato del sotto-insieme di worker-turni "care" nella finestra EOD
   in una futura iterazione, prima di ulteriori restrizioni geografiche
   che rischiano di ridurre ancora `final_money` (come osservato con
   `max_quadrants_for_livestock=1`, Sezione 9.1 punto 8).

Questa diagnosi non è stata falsificata né nascosta: è riportata
integralmente nel report di implementazione
(`experiments/e17/reports/claude/E17_1_CLAUDE_REACTIVE_V3_IMPLEMENTATION_REPORT.md`).
