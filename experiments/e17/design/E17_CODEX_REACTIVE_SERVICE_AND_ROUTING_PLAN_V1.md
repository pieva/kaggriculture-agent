# E17.2 — piano causale `REACTIVE_SERVICE_AND_ROUTING`

- **Data:** 2026-09-02
- **Stato:** `EXECUTED / CORE V2 DEVELOPMENT GATES PASS / NOT KAGGLE READY`
- **Candidata finale development:** `CODEX-E17.2-REACTIVE-SERVICE-ROUTING-CORE-V2`
- **Controllo congelato:** `CODEX-E17.1-TRUE-REACTIVE-V2`
- **Famiglia causale modificata:** `REACTIVE_SERVICE_AND_ROUTING`
- **Holdout e final confirmation:** vietati

## 1. Ipotesi

La V2 reagisce ai regimi di mercato, ma le azioni delle unità restano fornite
da una sequenza per step. L'ipotesi E17.2 è che una coda di servizio costruita
dallo stato corrente possa recuperare azioni inattive o non fattibili e
proteggere deadline biologiche senza cambiare acquisti, mercato, unlock,
placement o topologia pianificata.

La quota di allevamento Q2 resta un outcome. Non viene introdotta alcuna soglia
che imponga un numero di animali o tile per quadrante.

## 2. Trattamento ammesso

La candidata può modificare soltanto `farmer` e `hands`:

1. preserva ogni azione strutturale del provider che sia fattibile;
2. anticipa WATER e FEED quando distanza, servizio e deadline EOD esauriscono
   lo slack disponibile;
3. organizza il prelievo di Wheat dallo shed quando un animale critico non è
   servibile dagli inventari delle unità;
4. sostituisce `PASS` o un comando non fattibile con una coda produttiva
   osservata: HARVEST, WATER, FEED, COLLECT_FERTILIZER, CARE;
5. mantiene un'assegnazione soltanto finché il task resta dovuto e la sospende
   se il provider propone un'azione strutturale fattibile.

Il blocco `market` emesso dalla V2 deve restare byte-equivalente. Sono vietate
modifiche a HIRE, acquisti, vendite, unlock, BUILD, PLACE, PLANT, DIG e
FERTILIZE quando la proposta strutturale è fattibile.

## 3. Ordine di priorità

```text
CRITICAL_WATER
CRITICAL_FEED
HARVEST
WATER
FEED
COLLECT_FERTILIZER
CARE
```

I task critici sono piante o animali non serviti con contatore consecutivo
almeno pari a uno. Il routing critico si attiva quando le azioni necessarie,
incluso l'eventuale passaggio dallo shed, raggiungono il tempo residuo della
giornata meno il buffer preregistrato.

## 4. Evidenza e confronto

Usare esclusivamente seed `development` del manifest E17, entrambi i seat e
controllo matched sulla stessa configurazione. Il primo benchmark usa
`INERT_PASS_POLICY` per isolare l'esecuzione; un secondo probe può usare i
regimi development già definiti per V2. Nessun seed può essere rimosso dopo
l'esecuzione.

Metriche primarie:

- reward e delta matched rispetto a V2;
- comandi unità modificati e ragioni;
- quota `EXECUTED / NOT_EXECUTED / UNKNOWN` delle modifiche;
- `PASS` o comandi non fattibili recuperati;
- WATER/FEED critici risolti e debito residuo a EOD;
- fughe animali e perdite di colture derivabili pre/post EOD;
- invarianza del blocco market rispetto alla proposta V2;
- Q0/Q1/Q2, workforce e timing unlock come outcome.

## 5. Gate preregistrati

```text
TECHNICAL_ERRORS == 0
INVALID_ACTION_SHAPES == 0
MARKET_MUTATION_COUNT == 0
STRUCTURAL_FEASIBLE_MUTATION_COUNT == 0
OVERRIDE_TRACEABILITY_COVERAGE == 1.0
EXECUTION_CLASSIFICATION_COVERAGE == 1.0
ANIMAL_ESCAPES == 0
INERT_MEAN_DELTA_VS_V2 >= -5%
NATURAL_ROUTING_OVERRIDE_COUNT > 0
NATURAL_SERVICE_OVERRIDE_COUNT > 0
SAME_INITIAL_STATE_DETERMINISM == PASS
HOLDOUT_USED == false
FINAL_CONFIRMATION_USED == false
```

Il superamento dei gate prova soltanto la validità development della famiglia.
Non autorizza una submission Kaggle né l'attivazione dell'holdout.

## 6. Amendement dopo gli smoke test development

La preregistrazione V1 assumeva che piccoli detour potessero convivere con le
coordinate implicite della routine. Il primo seed development ha falsificato
questa assunzione:

| Variante esplorativa | Reward | Controllo | Esito |
|---|---:|---:|---|
| override idle/invalid aggressivo | 8.497 | 183.102 | respinta |
| sole deadline senza rientro | 46.670 | 183.102 | respinta |
| detour con rientro e servizi normali | 123.858 | 183.102 | respinta |
| detour critici soltanto | 176.990 | 183.102 | entro −5%, ma ridondante |
| lookahead dei servizi già coperti | 183.102 | 183.102 | nessun override naturale |

La causa è architetturale: anche le finestre `PASS` appartengono alla
sincronizzazione posizionale. Una deviazione apparentemente locale rende
inaffidabili i comandi successivi. Per questo la V2 non sovrappone percorsi a
una routine attiva: effettua un handoff completo delle unità a un dispatcher
state-driven, lasciando invariato il blocco market della V2.

## 7. Attivazione progressiva V2

L'handoff è stato misurato sul medesimo seed development, quindi i valori sono
tuning e non validazione indipendente:

| Giorno handoff | Reward | Delta vs 183.102 |
|---:|---:|---:|
| 20 | 90.924 | −50,34% |
| 22 | 111.398 | −39,16% |
| 24 | 128.436 | −29,86% |
| 26 | 147.298 | −19,55% |
| 28 | 164.906 | −9,94% |
| 29 | 180.585 | −1,37% |

La V2 congelata per il benchmark development attiva il core al giorno 29.
Nella finestra terminale genera soltanto task osservabili di `HARVEST` e
`DROP_INVENTORY`; non modifica mercato, topologia, acquisti, workforce o
unlock. Le strutture per WATER, FEED, staging Wheat, BUILD, PLACE, DIG e PLANT
sono implementate e testabili, ma la loro attivazione anticipata non è ancora
promossa.

## 8. Esito benchmark V2

Su tre seed development, entrambi i seat e controllo matched:

- candidata `131.947,17`, controllo `134.060,17`;
- delta medio `−2.113` (`−1,576%`), minimo matched `−2.517`;
- 750 comandi di routing e 252 servizi terminali;
- 1.434 record unità, tutti classificati: 990 `EXECUTED`, 444 `UNKNOWN`,
  zero `NOT_EXECUTED`;
- zero errori, fallback, forme invalide, mutazioni market e fughe;
- 19 animali finali invariati; crop finali medi 12,83 contro 13,83.

Tutti i gate tecnici e il limite di regressione passano. La candidata resta
`DEVELOPMENT_ONLY`: prova un handoff reattivo controllato, non ancora un core
economicamente equivalente sull'intero episodio.
