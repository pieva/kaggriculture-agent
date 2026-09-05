# E18.27 V3 / Top770 — produzione e monetizzazione D25-D30

Data: 2026-09-05. Stato: **diagnosi completata; nessuna nuova policy implementata**.

## Perimetro e metodo

Top770 è l'alias documentale del comparatore esterno già selezionato, non una
nuova selezione della leaderboard. Coorte final-770 invariata: episodi
105405557, 105384058, 105398563, 105391568, 105565293. Le eventuali analisi
storiche di episodi non-770 restano esplicitamente escluse da questa coorte.

Il confronto locale usa E18.27 V3 ed E18.26 contro E18.16: sette seed
development 180903001–180903007, entrambi i seat, 14 profili per versione.
Non sono partite matched contro Top770: prezzi, seed e avversari differiscono.
Le differenze di ricavo pubblico/locale non sono stime causali del beneficio.

Consistenze: checkpoint H24, indice 24×D−1. Flussi: azioni attribuite al giorno
del pre-stato, compreso l'ultimo batch. A D30 cassa e reward coincidono.
I ledger sono quelli già verificati contro tutti i saldi registrati; le nuove
tracce annuali applicano le azioni unità a copie dei pre-stati dei replay e
contano soltanto semine, WATER, fertilizzazioni e HARVEST riusciti. Hash dei
cinque replay verificati; nessun replay o piano congelato modificato.

## 1. Il problema non è soltanto l'ultimo DROP

Mediane per checkpoint; le mediane possono cambiare episodio lungo la curva.
Persone = hands più farmer; 13 persone equivalgono al cap di 12 hands.

| Giorno | Crop E18.27 / Top770 | Carrot E18.27 / Top770 | Persone E18.27 / Top770 | HARVEST riusciti E18.27 / Top770 |
|---|---:|---:|---:|---:|
| D25 | 61 / 61 | 0 / 0 | 13 / 13 | 25 / 21 |
| D26 | 51 / 61 | 0 / 14 | 10 / 12 | 12 / 31 |
| D27 | 39 / 61 | 0 / 26 | 12 / 12 | 15 / 21 |
| D28 | 29 / 59 | 0 / 38 | 9 / 12 | 24 / 36 |
| D29 | 0 / 27 | 0 / 27 | 10 / 12 | 16 / 27 |
| D30 | 0 / 2 | 0 / 2 | 3 / 12 | 9 / 28 |

Il divario di occupazione riparte da D26, dopo un D25 quantitativamente
allineato. E18.27 non apre cicli annuali dopo D25; non produce mai carote.
Il planner conserva `annual_replant_last_day=25` e `terminal_crop_clear_day=29`.
Inoltre seleziona WHEAT esplicitamente nel reimpianto: alzare il solo cutoff
non introduce CARROT, né garantisce le missioni di raccolta e vendita.

| Produzione/servizio D25-D30 | E18.27 V3, mediana [range] | Top770 |
|---|---:|---:|
| Nuove semine annuali | 11 | 54 |
| Raccolto Wheat + Carrot, unità | 184 | 260 in tutti i replay |
| Raccolto Strawberry | 48 [46–48] | 63 |
| Raccolto Milk | 54 | 81 |
| Raccolto Wool | 30 [24–30] | 40 |
| Fertilizer venduto, unità | 0 | 85 [85–86] |
| Costo totale assunzioni | 840 | 1.536 |

Il riferimento produce 76 annuali in più (+41,3% rispetto a 184), ma non è
corretto chiamarle tutte carote aggiuntive: una parte sostituisce il grano.
Le 54 semine comprendono 12 a D25 e 42 a D26-D29; le due a D29 non maturano.
Il costo assunzioni differisce di 696 nella finestra: è un costo osservato
del riferimento, non il preventivo dimostrato per il nostro routing.

## 2. Ricostruzione della scelta Carrot/Wheat

La nuova verifica allinea gli stessi 42 slot di semina D26-D29 nei cinque
replay, per step e coordinate. Gli eventi WATER e HARVEST — giorni, ore,
worker e quantità — sono identici. Sei slot sono sempre CARROT; 36 cambiano
specie. Questi 36 slot spostano **87 unità** tra WHEAT e CARROT, con due slot
terminali improduttivi. È una prova di riuso della medesima pianificazione
dei cicli annuali per due specie, non di una diversa topologia.

| Modalità osservata | Replay | Semine D26-D29 C / W | Raccolto D25-D30 C / W | Totale annuali |
|---|---:|---:|---:|---:|
| Carote prevalenti | 3 | 42 / 0 | 99 / 161 | 260 |
| Grano prevalente | 2 | 6 / 36 | 12 / 248 | 260 |

Nei tre casi con molte carote, all'inizio delle semine D26 i prezzi C/W
sono 56/39, 50/40 e 46/44, e c'è un PET_CAFE. Negli altri due sono 37/43 e
45/47, senza PET_CAFE. Sia il premio di prezzo sia la domanda dei negozi sono
compatibili con la selezione osservata: cinque replay non identificano la
funzione decisionale o una soglia universale. I sei slot sempre a carote,
anche quando il grano quota di più, impediscono di ridurre tutta la strategia
a «compra il seme del prodotto più caro».

## 3. Carote: produzione reale, non resa massima nominale

Nella modalità prevalente, le 42 semine si distribuiscono in 14/12/14/2 a
D26/D27/D28/D29. Si raccolgono 40 tile: 19 a età 2 e 21 a età 3. Le rese
effettive sono 19 tile×2 + 20 tile×3 + 1 tile×1 = **99 unità**.
Nessuna concimazione delle carote. Le due semine D29 restano immature;
ricevono anche quattro WATER complessivi D29-D30 senza poter produrre cash.

| Giorno | Semine Carrot | Raccolto Carrot, unità | Vendite Carrot, unità |
|---|---:|---:|---:|
| D25 | 0 | 0 | 0 |
| D26 | 14 | 0 | 0 |
| D27 | 12 | 0 | 0 |
| D28 | 14 | 3 | 0 |
| D29 | 2 | 41 | 6 |
| D30 | 0 | 55 | 93 |

Quindi 93/99 unità, circa il 94%, sono monetizzate in D30. Senza la capacità
di consegna/vendita finale, aggiungere queste semine non produce il beneficio.
Il ricavo delle 99 carote varia da 4.670 a 5.432; il costo dei 42 semi è 840.
Il contributo prima di lavoro, logistica e costo opportunità è 3.830–4.592,
**non un profitto incrementale previsto per E18.27**. Nella modalità ridotta
si raccolgono/vendono 12 carote, ricavo 437–550 e costo semi 120.

## 4. Regole dell'engine e ultimo giorno utile

Riferimento primario: engine installato, hash nel dataset diagnostico;
funzioni `_new_plant`, `_apply_unit_action`, `_decay_plants` e
`_daily_refresh_plants`. Non è una verifica di eventuali aggiornamenti online.

| Regola | CARROT | WHEAT |
|---|---:|---:|
| Costo seme | 20 | 10 |
| Età minima HARVEST | 2 giorni | 2 giorni |
| Giorni di WATER che aumentano la resa | età 2 e 3 | età 2, 3 e 4 |
| Resa con WATER completo, senza fertilizzante, a età 2 / 3 | 2 / 3 | 2 / 3 |
| Resa normale al termine della finestra | 3 | 4 |
| Cap assoluto con fertilizzante | 4 | 6 |
| Inizio decay | inizio età 4 | inizio età 5 |

CARROT **non matura prima** del WHEAT: entrambi sono raccoglibili a età 2.
Nel finale il vantaggio potenziale è il prezzo relativo a parità di percorso
e calendario; il seme costa però 10 in più. Prima di età 2 il WATER preserva
la pianta, ma non aumenta la resa; non va comunque saltato fino a causare due
refresh consecutivi senza acqua. FERTILIZE aggiunge lavoro e ha un costo
opportunità: il cap 4 non è la resa da assumere automaticamente.

Limite agronomico, prima dei vincoli logistici:

- Semina D26: primo raccolto D28, ultimo giorno prima del decay D29.
- Semina D27: primo raccolto D29, possibile età 3 in D30.
- Semina D28: raccolto soltanto D30, a età 2; serve WATER prima di HARVEST
  per ottenere la seconda unità normale, e resta da completare la consegna.
- Semina D29: primo raccolto D31, quindi vietata in una stagione di 30 giorni.

Nel replay standard ci sono 720 stati e 719 batch di azioni: l'ultimo batch
parte da D30 H23 e produce lo stato terminale H24. Non prenotare un'azione
nel terminale H24. Il cutoff di ogni tile deve includere WATER/HARVEST,
tragitto verso lo shed, DROP e SELL; la maturazione da sola non basta.

## 5. Priorità e prove per E18.28

1. **Continuità annuale D26-D28.** È il gap produttivo principale misurato:
   42 slot tardivi nel riferimento contro zero, ma soltanto 40 maturabili.
   Preparare un piano di missioni con riutilizzo delle tile annuali liberate,
   senza anticipare lo sgombero delle Strawberry per inseguire un target
   numerico. Ammettere una missione solo se interamente monetizzabile.
2. **Capacità e monetizzazione terminale.** Sono prerequisiti della continuità:
   il riferimento tiene 11 hands più farmer fino a D30, noi 2 hands più
   farmer in D30. Prenotare il lavoro a ritroso; non assumere 11 hands come
   obbligo fisso se meno persone completano le missioni. Oggi rimangono
   trasportati 6 Milk e 4 Wool in 12/14 casi; negli altri due, 6 Milk,
   2 Wool e 1 Wheat. Residui reali, non denaro già guadagnato.
3. **Selettore Carrot/Wheat sulle stesse missioni.** Confrontare incasso
   marginale previsto alla vendita, costo seme, quantità della coorte,
   domanda dei negozi, disponibilità di mangime e saturazione di mercato.
   La quotazione corrente non è il prezzo realizzato di un lotto futuro.
   Nessuna decisione basata sul seed o sull'identità dell'avversario.
4. **Servizio animale/Fertilizer come ablation distinta.** 81 contro 54 Milk
   raccolti, 85–86 Fertilizer venduti contro zero: sono opportunità separate
   dalla scelta delle carote, da confrontare per resa per azione e logistica.

Per identificare causa/effetto: A = consegne/vendite e workforce delle missioni
esistenti, senza nuove semine; B = annuali tardive solo WHEAT con logistica
dimensionata; C = stesso piano B, con sola scelta CARROT/WHEAT. Confrontare
B con A per la continuità e C con B per la specie. Non combinare nuove regole
Strawberry, FEED/CARE e Fertilizer nella prima prova delle carote.

Congelare D1-D24 anche negli ordini di mercato: il lookahead degli acquisti
può modificare l'apertura se si aggiungono semi al calendario futuro.
Conservare 770, cap 14 animali, massimo 12 hands e i difetti D10-D15 noti come
stratificazione diagnostica, senza correggerli di nascosto durante questo test.

Usare gli stessi sette seed development, entrambi i seat, controllo E18.27
e roster interno congelato. Verificare prefisso completo, no fughe/errori,
cicli PLANT→ACK→WATER→HARVEST→DROP→SELL, overflow, prodotti non monetizzati,
ricavo netto e worst-case. Nessun holdout, upload o promozione autorizzato dal
solo risultato di questa analisi; valgono i gate e la policy già documentati.

## 6. Cosa non si può concludere

Il netto D25-D30 mediano è 25.913 per E18.27 e 15.771 per Top770, nonostante
la produzione inferiore di E18.27: i mercati pubblici e locali sono diversi.
Il solo D30 è 857 contro 6.149, ma neppure questa differenza è tutta
recuperabile. Non sommare mediane di prodotti/giornate come se appartenessero
alla stessa partita. I confronti interni matched restano decisivi.

## Artefatti

- Dataset: `../artifacts/derived/E18_27_TOP770_D25_D30_CARROT_DIAGNOSIS.json`.
- Analizzatore riproducibile: `../tools/analyze_e18_27_top770_d25_d30.py`.
- Specifica prossima fase: `../MODEL_SPEC_CODEX_E18_28_770_LATE_ANNUAL_MISSIONS_V1.md`.

Nessuna strategia, config di runtime, piano congelato o submission cambiati.
