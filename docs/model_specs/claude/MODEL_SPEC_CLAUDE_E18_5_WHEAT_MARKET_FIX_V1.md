# MODEL_SPEC — Claude E18.5 Wheat-Market-Fix V1

- **Policy ID:** `CLAUDE-E18.5-WHEAT-MARKET-FIX-V1`
- **Autore:** Claude (modeler indipendente)
- **Data:** 2026-09-09
- **Foundation:** C2.1 (RECONCILED), esperimento E18
- **Predecessore:** `CLAUDE-E18.4-CAPACITY-CERTIFIED-V1`
- **Sorgente:** `src/agricola/strategy/claude/e18_wheat_market_fix_v5.py`
- **Config:** `docs/model_specs/claude/e18/configs/CLAUDE_E18_5_WHEAT_MARKET_FIX_V1.json`
- **Test:** `docs/model_specs/claude/e18/tests/test_claude_e18_wheat_market_fix_v5.py`
- **Stato:** `NOT PROMOTED — HYPOTHESIS FALSIFIED BY VERIFICATION`. Il bug
  è corretto e verificato (unità + motore reale: l'ordine `BUY_PRODUCT
  WHEAT` viene ora davvero eseguito dal motore). **Ma il torneo di
  verifica dal vivo mostra che la cassa media della candidata *peggiora*
  rispetto a V4** (11.147 → 3.598, −68%), a causa di un effetto non
  anticipato: l'acquisto di grano non ha alcun freno giornaliero e ne
  compra 400-1.000+ unità a partita, quasi mai convertite in bestiame
  utile (Sezione 7). Non promossa. Nessuna matrice di sviluppo a 7 seed
  contro gli avversari congelati E18 eseguita. Nessuna submission Kaggle.

---

## 0. Provenienza e contesto

Questa versione nasce dalla verifica dal vivo di E18.4 richiesta
dall'utente nella stessa sessione: un torneo di 14 partite (7 seed di
sviluppo × 2 ruoli) tra E18.4 e Codex V48 ha mostrato
`occupied_livestock_tiles` **esattamente a zero in tutte e 14 le partite**
(mediana, minimo e massimo), nonostante pascoli e pollai vengano
effettivamente costruiti in ogni partita (`empty_pastures`/`empty_coops`
sempre > 0). Vedi
[E18_CLAUDE_E18_4_VS_CODEX_V48_D01_D30_COMPLETE_KPI.html](../../../experiments/e18/reports/common/E18_CLAUDE_E18_4_VS_CODEX_V48_D01_D30_COMPLETE_KPI.html).

Tracciando il ledger di una partita completa
(`experiments/e18/artifacts/derived/common/e19_vs_codex_v48_paired_kpi_20260909/CLAUDE_E18_4_180903001_0.json`)
il grano acquistato a mercato (`bought_units["BUY_PRODUCT:WHEAT"]`) risulta
**zero su ogni giorno campionato** (D1, D5, D10, D15, D20, D25, D30) di una
partita di 30 giorni.

## 1. Obiettivo e ipotesi

**Obiettivo:** correggere l'unica causa isolabile e verificata dietro
l'assenza totale di bestiame nella linea E18, senza toccare nessun altro
meccanismo (disciplina già seguita da questa linea: mai combinare più
cause non isolate nella stessa versione).

**Causa radice, verificata contro il codice sorgente dell'engine**
(non ipotizzata): il parser degli ordini di mercato
(`kaggle_environments/envs/kaggriculture/kaggriculture.py`, funzione
`_parse_order`, righe 631-649) riconosce esattamente sei tipi di ordine:
`HIRE`, `BUY_LAND`, `BUY_SEED`, `BUY_PRODUCT`, `BUY_ANIMAL`, `SELL`. Per
qualunque altro valore restituisce `None`: l'ordine viene scartato in
silenzio, senza errore né telemetria. `_wheat_stock_orders` (il buffer di
grano proattivo introdotto in E18.2) emetteva `["BUY_WHEAT", qty]` —
un verbo mai esistito nel motore. Il grano si compra con
`["BUY_PRODUCT", "WHEAT", qty]`, esattamente come `FERTILIZER`
(`kaggriculture.py:598`, i due soli item ammessi da `BUY_PRODUCT`).

**Portata del bug:** verificato identico, copiato invariato, in tutte e
quattro le versioni precedenti della linea E18:

| File | Riga |
|---|---:|
| `e18_opponent_reactive_v1.py` | 1219 |
| `e18_opponent_reactive_v2.py` | 1317 |
| `e18_lifecycle_safety_v3.py` | 1324 |
| `e18_capacity_certified_v4.py` | 1340 |

Ogni acquisto proattivo di grano che questa linea ha mai tentato, dalla
prima versione E18 in poi, è stato uno scarto silenzioso — per questo il
gate di `_animal_orders` (`shed.WHEAT >= feed_security_buffer_per_animal`)
poteva essere soddisfatto solo dal grano incidentalmente raccolto dalla
propria rotazione colturale, mai dal buffer proattivo che la remediation
V2 credeva di aver costruito.

**Ipotesi (non confermata dalla verifica, Sezione 7):** correggendo solo
questo verbo, senza toccare soglie, gate o altri meccanismi, il buffer di
grano proattivo avrebbe dovuto iniziare a funzionare come originariamente
descritto, sbloccando l'economia zootecnica. Il torneo di verifica dal
vivo (Sezione 7) mostra che il verbo ora funziona esattamente come
previsto — ma il meccanismo che lo usa non ha mai avuto un freno di
quantità giornaliero, e senza quel freno la correzione produce un
acquisto di grano incontrollato che **peggiora** il risultato economico
invece di migliorarlo. L'ipotesi originale era incompleta, non sbagliata
nella diagnosi del verbo: correggeva la causa isolata correttamente
identificata, ma quella causa non era l'unica cosa che serviva perché il
buffer di grano si comportasse in modo economicamente sensato.

**Limiti dichiarati:** una correzione verificata non è una promozione. Il
divario di densità colturale (Codex mantiene ~2× le caselle coltivate di
Claude a parità di terreno) e il picco di PASS a D30 (manodopera non
ridotta durante `in_liquidation`/`in_shutdown`), entrambi identificati nel
torneo E18.4, restano intenzionalmente non affrontati qui — a cui si
aggiunge ora il freno di quantità mancante in `_wheat_stock_orders`
(Sezione 7), il vero prossimo passo isolato da affrontare prima di
qualunque nuova ipotesi su bestiame o densità colturale.

## 2. Strategia

Invariata da E18.4 (Sezione 8 di
[MODEL_SPEC_CLAUDE_E18_4_CAPACITY_CERTIFIED_V1.md](MODEL_SPEC_CLAUDE_E18_4_CAPACITY_CERTIFIED_V1.md)):
stessa pianificazione della produzione, degli investimenti e della
manodopera, stesso orizzonte intra-episodio, stesso gate di capacità
giornaliera introdotto in V4. Questa versione non modifica *come* si
pianifica; corregge *se* un ordine di mercato specifico viene mai
eseguito dal motore.

## 3. Decisioni

**Unica modifica** (`_wheat_stock_orders`,
`e18_wheat_market_fix_v5.py`):

```diff
- orders.append(["BUY_WHEAT", int(qty)])
+ orders.append(["BUY_PRODUCT", "WHEAT", int(qty)])
```

Nessun parametro, soglia, priorità o vincolo è cambiato rispetto a V4: la
configurazione (`CLAUDE_E18_5_WHEAT_MARKET_FIX_V1.json`) è identica a
quella di V4 salvo gli identificativi.

## 4. Reazioni

Invariate da V4: fallback tecnico, stall-timeout, coda di emergenza,
chiusura di partita. Nessuna nuova reazione introdotta.

## 5. Coerenza con la Foundation

Questa correzione **allinea** il codice a un fatto `ENGINE_VERIFIED` già
presente nella Foundation ma non rispettato dall'implementazione: il
Feature Model (`MKT-08`, prezzo di acquisto per specie) e l'Ontologia
(`wheat_operating_flow`: "grano per gli animali... acquistabile") non
documentano un verbo di mercato proprio; è la State Machine
(`../../foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md`,
sezione "Market, Capitale e Monetizzazione") a elencare esplicitamente
`BUY_PRODUCT` fra gli ordini ammessi. Il bug era quindi un'implementazione
non conforme al contratto dell'engine già documentato, non un gap della
Foundation stessa.

## 6. Stato di realizzazione

**Implementato:** il verbo di mercato corretto per il grano.

**Non implementato / proposto per il futuro:** tutto quanto già elencato
come non toccato in E18.4 (matching ottimale dell'identità worker,
certificazione per-missione della capacità, riduzione della manodopera in
`in_liquidation`), il divario di densità colturale osservato nel torneo
E18.4, e — priorità immediata, diagnosticata in Sezione 7 — un freno di
quantità/giorno mancante in `_wheat_stock_orders`, senza il quale questa
stessa correzione peggiora il risultato economico verificato invece di
migliorarlo.

## 7. Verifica eseguita in questa revisione

**Test automatici**, eseguiti realmente con
`.venv/Scripts/python.exe -m pytest`:
- `test_claude_e18_wheat_market_fix_v5.py`: 25 test unitari + 2 test a
  motore reale (regressione sul match peggiore già tracciato in V2/V3/V4,
  seed `180903002`; verifica che l'ordine `BUY_PRODUCT WHEAT` compaia
  realmente nel flusso di azioni registrato dal motore) — **27/27 PASS**.
- Intera directory `docs/model_specs/claude/e18/tests/` (V1-V5):
  **127/127 PASS**, nessuna regressione incrociata. Questi test
  verificano che il verbo sia corretto e accettato dal motore; **non**
  misurano l'effetto economico su una partita intera, che richiede il
  torneo seguente.

**Torneo dal vivo di verifica**, stessa dashboard usata per V4 (nessuno
strumento nuovo creato, solo esteso — Sezione 8): 14 partite (7 seed di
sviluppo × 2 ruoli) contro Codex V48, tramite
[run_e19_vs_codex_v48_paired_kpi.py](../../../experiments/e18/tools/common/run_e19_vs_codex_v48_paired_kpi.py)
e
[build_e19_vs_codex_v48_kpi_reports.py](../../../experiments/e18/tools/common/build_e19_vs_codex_v48_kpi_reports.py).
Report:
[E18_CLAUDE_E18_5_VS_CODEX_V48_D01_D30_COMPLETE_KPI.html](../../../experiments/e18/reports/common/E18_CLAUDE_E18_5_VS_CODEX_V48_D01_D30_COMPLETE_KPI.html).

**Risultato: l'ipotesi non è confermata.** Cassa finale su 14 partite
(media/mediana/min/max):

| | V4 (candidata) | V5 (candidata) | Delta |
|---|---:|---:|---:|
| Media | 11.147 | **3.598** | **−67,7%** |
| Mediana | 11.896 | 2.833 | −76,2% |
| Minimo | 7.800 | 81 | — |
| Massimo | 13.695 | 11.168 | — |

Anche la cassa dell'avversario Codex V48 nella stessa serie di partite
cala (media 133.660 → 83.061, −37,9%): un effetto sul lato avversario
osservabile solo perché il confronto è appaiato e dal vivo, non contro un
replay esterno fisso.

**Causa identificata, quantificata direttamente dal ledger di ogni
partita:** `_wheat_stock_orders` non ha alcun freno che limiti l'acquisto
a una quantità sensata per il numero di animali realmente posseduti. Su
14 partite la candidata acquista fra **418 e 1.068 unità di grano**,
spendendo fra **12.984 e 41.642** di cassa — cifre enormemente superiori
al fabbisogno di 0-4 animali (buffer nominale 3 unità/animale). In
**10 delle 14 partite**, Codex V48 stesso chiude con **zero animali
collocati** a D30 (`occupied_livestock_tiles`, contro il suo normale 14),
segno che l'acquisto ininterrotto di grano da parte della candidata
compete per la stessa risorsa condivisa di mercato e può privare
l'avversario del grano necessario ai propri animali. Non è stato isolato
il meccanismo esatto per cui il freno esistente
(`wheat_stock >= target_stock`) non impedisce acquisti ripetuti — resta
un'ipotesi verosimile, non confermata riga per riga, che lo scarico
automatico di fine giornata (capacità shed 100, condivisa con altri beni
raccolti) distrugga l'eccedenza ogni notte, azzerando di fatto la scorta
visibile e reinnescando l'acquisto il giorno seguente.

**Conseguenza per lo sviluppo:** questa correzione non va promossa da
sola. Il prossimo passo isolato e diagnosticato è aggiungere un freno di
quantità/giorno a `_wheat_stock_orders` (o correggerne la condizione di
arresto) — una causa distinta da quella di questa versione, da affrontare
nella propria versione separata, non qui.

**Non eseguito:** la matrice di sviluppo a 7 seed contro gli avversari
congelati E18 (Copilot/Antigravity) richiesta dal protocollo per un
verdetto di gate; nessuna partita economica oltre a quelle elencate sopra.

## 8. File di implementazione

| File | Ruolo | Parte della strategia implementata | Categoria |
|---|---|---|---|
| [e18_wheat_market_fix_v5.py](../../../src/agricola/strategy/claude/e18_wheat_market_fix_v5.py) | Controller identico a V4 salvo il verbo di mercato del grano | Sezione 3 | Runtime |
| [observation_contract.py](../../../src/agricola/core/observation_contract.py) | Parsing e normalizzazione policy-neutral dell'osservazione, invariato | Ingresso dati | Runtime (condiviso) |
| [CLAUDE_E18_5_WHEAT_MARKET_FIX_V1.json](e18/configs/CLAUDE_E18_5_WHEAT_MARKET_FIX_V1.json) | Configurazione, identica a V4 salvo gli identificativi | Sezione 3 | Configurazione |
| [test_claude_e18_wheat_market_fix_v5.py](e18/tests/test_claude_e18_wheat_market_fix_v5.py) | Fixture riprodotte da V4 (non regressione) più fixture nuove sul verbo corretto e verifica a motore reale | Sezione 7 | Test |
| [run_e19_vs_codex_v48_paired_kpi.py](../../../experiments/e18/tools/common/run_e19_vs_codex_v48_paired_kpi.py) | Strumento di verifica comune (registry estensibile), esegue le 14 partite dal vivo contro Codex V48 | Sezione 7 | Builder (strumento di verifica) |
| [build_e19_vs_codex_v48_kpi_reports.py](../../../experiments/e18/tools/common/build_e19_vs_codex_v48_kpi_reports.py) | Genera il report a 22 pannelli dai profili delle 14 partite | Sezione 7 | Builder (strumento di verifica) |

**Submission:** nessuna.
