# E18.33 — audit dei vincoli ereditati e diagnosi Q0

## Esito e perimetro

**La policy agricola attuale non è comune ai quadranti.** E18.31 ed E18.32
usano ancora il piano materializzato E18.28 C. Gli adattamenti online correggono
assegnazione, acquisti e servizi, ma non sostituiscono la generazione del lavoro.
Il problema non si risolve cancellando alcune chiavi JSON: date, colture,
coordinate e lavoratori sono già incorporati nelle righe `trajectory`.

Mandato del proprietario: analizzare e definire la nuova base comune, partendo
da Q0. Questo documento **non certifica un nuovo agente implementato**.
E18.32 V9 resta un controllo interno non pubblicato, non conforme al nuovo
requisito; il suo gate prestazionale non ne dimostra la conformità architetturale.

Fonti: codice locale e sei replay E18.31 già acquisiti, nessun nuovo benchmark.
Gli screenshot hanno seed 1541058082, assente dal corpus locale esaminato:
non è stato identificato il loro episodio/versione. Il comportamento raffigurato
è coerente con il vecchio piano, ma non è prova della versione eseguita.

## Q0: fatti verificati nei sei replay dell'ultima pubblicata

Osservazione Dn H24, prima dell'ultimo batch eseguibile del giorno; D30 H24 è
terminale. Pascoli qui significa strutture, tutte popolate nei checkpoint.

| Periodo | Q0 pascoli | Q0 colture | Tile Q0 senza coltura/animale | Q1 e Q2 |
|---|---:|---:|---:|---|
| D1–D3 | 4 | 19 | 2 | ancora chiusi |
| D4 | 5–6 | 19 | 0–1 | ancora chiusi |
| D5–D10 | 6 | 19 | 0 | Q1 raggiunge 7 pascoli + 18 colture a D10 |
| D11–D13 | 6 | 7 | 12 | Q1 pieno; Q2 ha 25 colture da D12 |
| D14 | 7 | 12 | 6 | Q1 e Q2 pieni |
| D15–D16 | 7 | 18 | 0 | configurazione 770 completa |

Le tile senza produzione includono eventuali erbacce: in un replay una delle
12 tile diventa WEED. Non confondere terreno libero, pascolo vuoto e coltura
immatura. Nel piano congelato D4 ha ancora quattro pascoli; l'E18.31 pubblicata
ne anticipa uno o due a seconda delle risorse osservate.

Cause dimostrate dal programma:

1. I quattro animali iniziali sono scelti in ordine serpentino, nelle righe
   y=2 e y=3. I posti `(3,4)` e `(4,4)`, vicini al magazzino, sono lasciati ai
   due acquisti originariamente previsti a D5. Non è una graduatoria del costo
   delle visite FEED/CARE lungo il ciclo di vita.
2. Il settimo pascolo Q0, `(2,4)`, ospita WHEAT fino alla conversione D14.
   È una pecora; l'espansione online anticipa le mucche, mentre per le pecore
   ripopola soltanto strutture già costruite. Il rinvio resta quindi attivo.
3. Le 12 tile MELON sono raccolte a D11, ma le due semine sostitutive rimangono
   fissate a D14 e D15, sei tile per giorno. E18.27 aveva anticipato il raccolto
   da D13 a D11 senza anticipare questa risemina: una dipendenza temporale non
   aggiornata, non una necessità biologica della tile dopo HARVEST.
4. Q1 ha 18 STRAWBERRY a lotti D7–D10; Q2 ha 7 WHEAT e 18 STRAWBERRY a D12.
   Questo spiega perché i loro stock non hanno la stessa interruzione di Q0.
   Le colture pluriraccolto hanno comunque una vita produttiva finita.

A D12 la cassa dei sei replay è 17.288–18.967 e Q0 ha ancora solo sette
colture: manca una decisione di riattivazione nel programma. La cassa disponibile
non dimostra da sola che ogni possibile nuova coltura sia sostenibile o redditizia.

**Limite causale importante:** 1.619 dei 1.765 PASS D5–D10 (91,73%) vengono
emessi quando Q0 ha già tutte le 25 tile occupate da colture o animali.
Il vuoto dopo i meloni spiega un difetto successivo, non tutto il picco iniziale.
Occupazione, produttività, finestre di servizio e dimensionamento del personale
devono essere valutati insieme. L'audit precedente classifica il 77,45% di quei
PASS come coda personale esaurita: non prova l'assenza di opportunità agricole.

Dati riproducibili:
`../artifacts/derived/E18_32_Q0_UTILIZATION_AUDIT_20260906.json`, generati da
`../tools/audit_e18_32_q0_utilization.py`; i sei hash raw sono nel JSON.

## Inventario dei residui, ordinato per priorità strutturale

| Priorità | Residuo e punto di consumo | Stato effettivo | Disposizione per la nuova linea |
|---|---|---|---|
| P0 | `pasture_targets`, `late_q0_pasture`, `late_q0_pasture_day`; E18.18 `_define_animal_calendar`, E18.31 `pasture_plan` da PLACE | Date/specie/coordinate materializzate e ancora consultate | Sostituire con budget globale, capacità locale uniforme, scelta dinamica della tile e missioni osservate |
| P0 | `melon_coords`, `opening_wheat_coords`, `q0_early_strawberry`, `q1_strawberry`, `q2_wheat`, `q2_strawberry` | Mix e ruoli imposti dall'identità del quadrante | Unico selettore delle colture su ogni tile ammissibile; nessuna maschera specie/coordinate |
| P0 | MELON D11, risemina D14/15, conversione D14, Q1 D7–10, `q2_plant_day=12` | Calendario effettivo nella trajectory | Eventi raccolto/terreno disponibile/finanziamento → rivalutazione, senza date di attivazione strategiche |
| P0 | `routes`, `daily_hands`, `requirements`, ore nominali, next-row fence, ritorno all'origine | Consumo online; E18.32 compatta solo una parte e conserva il fallback | Pool unico di missioni generate dallo stato; deadline materiali, organico da carico e crescita |
| P0 | PLANT_WATER offerto solo per un PLANT già in coda; COW anticipate solo su target del piano | Un terreno vuoto senza riga programmata non genera una nuova semina | Generatore di opportunità su TUTTE le tile, non solo recupero di attività già pianificate |
| P0 | `{COW:9,SHEEP:5}` ripetuto nel mercato; filtro COW; orizzonte di otto giorni anche per ripopolare SHEEP | Vincoli online attivi, non semplici metadati | Target animale derivato dal medesimo budget pascoli; dati biologici per specie; niente codice diverso per espansione pecore |
| P1 | `d10_wheat_fast_cycle_days`, `d10_full_water_through_day`, `skip_water_cells_by_day`, conversione fragole D6 | Materializzati in WATER/HARVEST/PLANT/DIG | Età, resa, rischio e liquidità; nessun ciclo copiato da giorni del benchmark |
| P1 | `animal_care_blackout_days`, `q2_water_defer_days`, cap fertilizzante per giorno/coltura, `fertilizer_budget_by_crop`, parità di raccolta | Influenzano il programma di base; il pool può aggiungere servizi, senza cancellare il difetto del generatore | Servizi con valore marginale e deadline biologica, stessa regola in ogni quadrante |
| P1 | `minimum_hands_by_day`, `force_peak_hands_from_day/through_day` | Organico di controllo e limite superiore di ricerca per la compattazione V9 | Capacità calcolata con manutenzione E investimenti; tenere solo massimo globale 12 |
| P1 | `strawberry_retire_day`, `annual_replant_last_day`, `terminal_crop_clear_day`, `late_crop`, ramo D25–D30 | Date e mix finali attivi nel piano | Orizzonte residuo e ricavi effettivamente consegnabili; niente DIG terminale senza beneficio |
| P1 | BUY_LAND condizionato a righe del piano per oggi/domani, ordine NE/SW duplicato | Ammissione economica online, domanda di terra ancora dipendente dalla trajectory | Valutare il prossimo terreno legalmente acquistabile per opportunità certificate |
| P2 | `jesse_d10_action_targets`, `daily_available_action_slots`, provenance, `crop_checkpoints`, `animal_checkpoints` | Riferimenti/controlli del planner, non lettura del Top online | Fuori dalla configurazione della policy; restano solo in evidenze e controlli storici |
| P2 | Override mercato E18.26/E18.27/E18.28, `opening_reference`, `prefix_reference`, flag dei trattamenti | Vecchi `_market_orders` bypassati da UNIFIED; oggetti/piani ancora ereditati | Non attribuire loro gli ordini attuali; nuova policy senza ereditare questi controller né caricare tali piani |
| P2 | `animal_feed_blackout_days=[]` e altri flag inerti | Nessun blackout FEED attuale; vuoto non significa causa attiva | Non propagare chiavi prive di ruolo nella nuova configurazione |

La regola CARE del pool confronta anche il prezzo del prodotto con il costo
di più FEED. Nella nuova valutazione il FEED già dovuto non va addebitato di
nuovo al solo CARE: contano bonus realmente incassabile, saturazione della resa
e costo incrementale di servizio. Analogo divieto di doppio conteggio per
fertilizzante venduto oppure usato, mai entrambe le valorizzazioni.

## Cosa NON è un fossile

- Dati di maturazione, intervalli e limite di produzione, regole di morte/fuga,
  durata del fertilizzante e ordine azioni → mercato → refresh: contratto motore.
- Geometria del magazzino, ordine legale di acquisto dei terreni e attivazione
  reale dei lavoratori: vincoli di ambiente, da adattatore, non preferenze Q0/Q1.
- Orizzonte dell'episodio e ultimo batch eseguibile: indispensabili per valorizzare
  la chiusura; diverso da una regola arbitraria «stop semine a D28».
- Target corrente 14 pascoli, capacità locale uniforme 7, massimo 12 manovali:
  parametri di profilo espliciti, non maschere di coordinate o calendari.
- Storici, replay, hash e baseline: evidenza da preservare, non configurazione
  eseguibile della nuova policy.

## Bonifica e confini

La nuova configurazione E18.33 è definita da zero, non ottenuta con merge o
`deepcopy` della E18.28. Schema chiuso: chiavi sconosciute, coordinate, programmi
giornalieri e profili separati per quadrante sono rifiutati. Dati del motore,
policy e protocollo sperimentale devono essere tre sorgenti separate.

Non si modificano o cancellano i file congelati: altrimenti perderemmo parità
con submission pubblicate e controlli. La bonifica effettiva del runtime sarà
completata solo quando il nuovo agente non importerà la catena dei controller
trajectory e non caricherà alcun piano storico, neppure come fallback.

Specifica normativa:
`../MODEL_SPEC_CODEX_E18_33_COMMON_RESOURCE_POLICY_V1.md`.
Profilo pulito: `../configs/CODEX_E18_33_COMMON_RESOURCE_POLICY_V1.json`.
La configurazione è specificata e validata (34 test dello schema passati);
sono definiti anche due scenari economici iniziali comuni, non calibrati sui Top.
Integrazione e rendimento restano
da verificare. Nessuna nuova submission, nessun cambio della topologia live.

## Punti sorgente per ripetere l'ispezione

- `../tools/e18_18_capacity_trajectory_planner.py`: inizializzazione layout,
  `_define_crop_calendar`, `_define_animal_calendar`, `_crop_bundles`,
  `_animal_bundles`, `_should_water`, `_route_day7_unlock`.
- `../tools/e18_27_d10_d15_cashflow_controller.py`: override del raccolto e
  `q2_plant_day`; `../tools/e18_28_full_season_controller.py`: planner C,
  riferimenti e chiusura; `../artifacts/derived/E18_28_FULL_SEASON_C_PLAN_V1.json`.
- `../tools/e18_31_assignment_controller.py`: `pasture_plan`,
  `_offers_for_worker`; `../tools/e18_31_unified_investment_controller.py`:
  `_market_orders`; `../tools/e18_31_obligation_controller.py`: filtro CARE.
- `../tools/e18_32_demand_routing_controller.py`: `_bundles`, `_new_day`,
  fallback e ricerca dell'organico sul roster storico.
- Motore locale: `.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/`
  `kaggriculture.py`, tabelle CROPS/ANIMALS e refresh; reward terminale = cassa.
