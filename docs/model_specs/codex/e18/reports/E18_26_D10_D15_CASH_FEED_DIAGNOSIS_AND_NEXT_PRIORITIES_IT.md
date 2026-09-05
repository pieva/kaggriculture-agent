# E18.26 — diagnosi cassa/FEED e priorità D10-D15, poi chiusura D30

Data: 2026-09-05. Stato: analisi consolidata e indirizzo del proprietario;
nessuna nuova policy implementata, candidata promossa o submission eseguita.

## Decisione corrente

La prossima versione deve concentrarsi sulla finestra D10-D15. Soltanto dopo
averne verificato gli effetti nei confronti interni si apre un trattamento
separato sulla chiusura entro D30. Non combinare le due famiglie causali nel
primo esperimento. Restano target 7-7-0, 14 pascoli, cap complessivo di 14
animali, mix 9 Cow + 5 Sheep e massimo 12 hands più il farmer.

Questa decisione supera la precedente indicazione di intervenire prima sul
solo Wheat D13 congelando integralmente D1-D10. Il problema inizia prima:
occorre preparare in D10 il ciclo di incasso D11-D12. D1-D9 rimane il controllo
congelato; D10 rientra nella finestra del trattamento. Eventuali necessità di
modificare giorni precedenti vanno documentate e trattate separatamente.

## Evidenze e provenienza

- Dataset canonico: `../artifacts/derived/E18_26_JESSE_770_D01_D30_CLOSURE.json`.
- Report D30: `E18_26_TOP770_D01_D30_CLOSURE_IT.md`.
- Top770: cinque replay storici con topologia finale pasture 7-7-0,
  `105405557`, `105384058`, `105398563`, `105391568`, `105565293`.
- E18.26: contro E18.16, seed development `180903001`, entrambi i seat;
  reward congelati `54761` e `53968`.
- Verifica aggiuntiva della maturazione: riesecuzione invariata E18.26 seat 0
  contro E18.16 sullo stesso seed; reward `54761 / 81797`, zero errori del
  controller. Non è un test di una correzione né un controfattuale di cassa.
- I flussi giornalieri usano il giorno prima dell'azione. I checkpoint H24
  usano l'indice `24*D-1`: l'ultimo batch della giornata è registrato nel
  primo stato della successiva. Non sommare flussi e saldi con confini diversi.

Il replay corrente `105717134` non appartiene a questa coorte omogenea e non
va sostituito ai cinque riferimenti solo perché aperto nel browser.

Impronte SHA-256 dei riferimenti al salvataggio:

- dataset D30: `2007120DFEFA0F58BB656C9182E4FA633AEBCB8ABA23B8FD2BC1467A345B9E73`;
- piano E18.26 `../artifacts/derived/E18_26_770_JESSE_BOOST_D10_PLAN_V1.json`:
  `4B6BFB018E69EC0F7B2AA8D816F1AECF946EBBEE77E02EA3E74E6169A3A15616`;
- motore locale `.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py`
  (path dalla root del repository):
  `BC8A54879EF02C7EA64B8B333D6A976F0EA65C4949149D01F463F23BCCEE653E`.

## 1. Origine del gradino di cassa D11

| KPI | Top770, cinque replay final-770 | E18.26, due seat contro E18.16 |
|---|---:|---:|
| Tile Melon iniziali | 12 | 12 |
| Melon raccolti, unità complessive | 72 | 72 |
| Giorno del raccolto | D11 | D13 |
| Vendite Melon | 60 in D11 + 12 in D12 | 36 in D13 + 36 in D14 |
| Incasso Melon in D11 | 13.000–14.575 | 0 |
| Incasso Melon complessivo | 14.267–16.717 | 11.262 |
| Cassa H24 D11 | mediana 18.935 | 1.128 |
| Persone H24 D11-D12, hands + farmer | 12 | 9 |

In D11 Top770 vende anche 12 Milk, per 1.814–2.748. La componente principale
del gradino è quindi la monetizzazione dei Melon, non una produzione
complessiva di Melon superiore. I 72 Melon locali vengono poi venduti: una
parte del divario è ritardo di incasso e viene recuperata in D14.

L'incasso complessivo locale è inferiore di 3.005–5.455 a quello dei replay
Top770, ma questa differenza NON è una stima causale del costo di due giorni
di ritardo: seed, avversario, prezzi e contesa di mercato non sono appaiati.

### Causa concreta nel piano

`../tools/e18_18_capacity_trajectory_planner.py` usa
`melon_harvest_day = int(self.config.get("melon_harvest_day", 13))`;
la configurazione E18.26 non modifica tale default. Il raccolto resta quindi
calendarizzato a D13 anche quando lo stato consente di anticiparlo.

Il motore consente HARVEST Melon dall'età 10 giorni, cioè D11 per le semine
D1. Nella riesecuzione locale invariata:

| Stato osservato | Tile a resa 6 | Tile a resa 5 | Tile a resa 4 | Yield totale sulle tile |
|---|---:|---:|---:|---:|
| Inizio D11, indice 240 | 0 | 11 | 1 | 59 |
| H24 D11, indice 263 | 10 | 2 | 0 | 70 |
| Dopo l'ultimo batch D11, indice 264 | 11 | 1 | 0 | 71 |
| Inizio D13, indice 288 | 12 | 0 | 0 | 72 |

Attendere D13 porta da 71 a 72 unità rispetto alla fine delle azioni D11,
ma mantiene immobilizzati prodotto e tile. Non è necessario attendere D13
per la maturazione minima. L'anticipo va comunque pianificato tile per tile,
includendo WATER, raccolto, trasporto e vendita: non basta cambiare una data.

L'uguaglianza aggregata di PLANT/WATER con Top770 non prova parità di servizio
per tile, età, yield o liquidità. Quei conteggi diventano KPI diagnostici,
non vincoli da pareggiare a costo di ritardare l'incasso.

## 2. Cassa, mangime e origine dei pascoli vuoti

| Momento | Evidenza eseguita |
|---|---|
| D11 | Acquisto terreno 2.000 e semi Strawberry 900 prima dell'incasso principale dei Melon; 13 FEED eseguiti. |
| D12 | Nessun acquisto di prodotto Wheat; zero FEED su 13 animali; cassa H24 236. |
| D13 | Soltanto 8 FEED su 13; cassa al checkpoint H24 9. |
| Ultimo batch D13, registrato allo step 312 | SELL di 36 Melon, BUY_SEED di 26 Wheat e BUY_PRODUCT di 5 Wheat; il mangime acquistato non può essere distribuito prima del refresh. |
| Passaggio D13-D14 | Fuga di 3 Cow e 2 Sheep, ciascuno al secondo giorno senza FEED: 13 animali diventano 8. |
| D14 | Piazzata una Sheep già prevista: 8 diventano 9, con cinque pascoli vuoti. |

Il percorso causale supportato è ritardo degli incassi e spese anticipate,
seguiti da mancata disponibilità/consegna del mangime entro le scadenze. La
causa immediata delle fughe è dimostrata dallo stato degli animali. Non è
stato però ancora eseguito un controfattuale che provi che la sola aggiunta
di cassa, senza ripianificare i percorsi, eviterebbe tutte le fughe.

Distinguere acquisto e FEED: il mercato viene eseguito dopo le azioni delle
unità. Comprare il Wheat nell'ultimo batch D13 è troppo tardi per usarlo
prima del refresh che fa scappare gli animali.

### Perché i vuoti persistono

Da D14 a D30 non viene acquistato alcun animale, anche quando la cassa
risale a 11.630 in D14 e a mediana 24.186,5 in D20. I cinque posti vuoti
persistono ai 17 checkpoint D14-D30, pari a 85 posti-giornata osservati.
Non è quindi una spiegazione sufficiente dire che mancano soldi per
ripopolare: manca una risposta del piano alle perdite effettive.

Prevenzione e recupero sono distinti. La prevenzione protegge gli animali
già acquistati; un nuovo acquisto deve invece recuperare prezzo, feed,
servizio e trasporto entro D30. Con primo yield Cow a 8 giorni e Sheep a 6,
non ogni refill tardivo è economicamente conveniente. Ogni vuoto deve avere
una decisione esplicita con motivazione, costo e scadenza, non essere ignorato.

## 3. Piano prioritario della prossima versione: D10-D15

Sequenza di lavoro, con ablation distinguibili dentro la medesima finestra:

1. **Preparare e anticipare gli incassi Melon.** Verificare lo stato per tile
   in D10, assegnare WATER/HARVEST in D11 e prenotare consegne/vendite D11-D12.
   Il riferimento operativo è 60 unità vendute in D11 e completamento in
   D12; quantificare eventuali sacrifici di yield e non forzare 72 in D11
   se lo stato o il percorso non lo consentono.
2. **Finanziare gli obblighi prima dell'espansione.** Riservare risorse per
   rinnovi hands, feed e consegne entro scadenza. Sbloccare terreno e comprare
   semi solo sul residuo disponibile dopo gli obblighi. Usare il Wheat
   raccolto quando realmente disponibile al worker, non quando solo maturo.
3. **Conservare il servizio e riattivare le tile liberate.** Non far discendere
   la riduzione hands dall'omissione dei raccolti nel piano. Prenotare le
   missioni e poi dimensionare la manodopera. Misurare il percorso verso
   14 animali e 61 crop, target D15 `38 Strawberry + 23 Wheat`, senza violare
   cap, riserva di servizio o copertura WATER.
4. **Gestire le deviazioni.** Registrare FEED a rischio e ogni pascolo vuoto.
   La prova primaria deve prevenire le fughe; la risposta a perdite forzate
   si verifica separatamente con fixture, senza mascherare fughe tramite
   acquisti sostitutivi nel gate principale.

Per isolare l'effetto, mantenere invariate le regole D16-D30 durante questa
fase. Lo stato e i risultati successivi possono naturalmente cambiare come
conseguenza di D10-D15: vanno misurati fino al termine, non congelati a forza.

### KPI e gate del confronto interno

- Congelare parent E18.26 e avversari; partire dal confronto riproducibile
  contro E18.16 ed E18.25, seed development 180903001, entrambi i seat.
  Estendere poi alla matrice development preregistrata e ai campioni interni
  previsti dal protocollo, incluso E18.2/V4D prima di una conclusione competitiva.
- Conservare D1-D9; registrare separatamente ogni delta di D10. D10 resta
  riferimento strutturale `12 Melon + 20 Strawberry + 5 Wheat`, 13 animali e
  11 hands più farmer. Non usare la sola uguaglianza PLANT/WATER come gate.
- Registrare per giorno e turno maturazione/yield, HARVEST, stock raccolto,
  consegne, vendite eseguite, prezzo realizzato, cassa minima e scadenze.
- FEED coperto in D11-D15 per ogni animale presente, zero fughe nell'intero
  episodio, target 9 Cow + 5 Sheep a D15 e a fine partita; cap risorse 14,
  target pasture 7-7-0, massimo 12 hands, zero errori/fallback tecnici.
- Misurare tile crop e pascoli vuoti, ritardi di attivazione, WATER mancati,
  ore-worker, MOVE/PASS, spesa payroll/feed e ricavi per famiglia di prodotto.
- Confrontare cassa D11-D15 e reward D30 matched con E18.26 contro lo stesso
  avversario/seed/seat. Un miglioramento transitorio ottenuto vendendo feed
  necessario o distruggendo capacità successiva non è un PASS.
- Richiedere delta finale positivo in entrambi i seat nello smoke e tenuta
  nella matrice successiva. Superare E18.26 non equivale a superare E18.16 o
  il controllo E18.2/V4D: dichiarare separatamente questi verdetti.
- Nessun consumo holdout/final-confirmation o upload della candidata ancora
  fallita. Resta la policy quotidiana esistente, dopo i gate applicabili;
  questa nota non avvia automazioni né submission.

## 4. Seconda fase, distinta: chiusura entro D30

Avviarla sul migliore sviluppo D10-D15 verificato e congelato. Non limitarsi
all'ultimo giorno: pianificare a ritroso da D30 le ultime maturazioni,
raccolte, consegne e vendite; ogni modifica preparatoria a D26-D29 o prima
deve essere esplicita e appartiene solo a questa seconda ablation.

Evidenze già disponibili: Top770 mantiene 12 persone fino a D30, esegue 28
HARVEST nell'ultima giornata e realizza flussi netti 5.122–8.562; E18.26
chiude con 3 persone, 4 HARVEST e flusso -81/+70. I valori economici pubblici
sono osservazionali; non rappresentano un miglioramento locale garantito.

Priorità: completare missioni prima di tagliare hands; anticipare il cutoff
delle sole semine che non possono maturare ed essere vendute; recuperare
Fertilizer e prodotti trasportati; evitare servizi terminali senza ritorno
entro il termine. Il numero di hands deve derivare dalle missioni residue,
non essere una copia obbligatoria del numero Top770. Nessuna nuova topologia,
nessuna copia delle due coop vuote di Top770, nessuna ipotesi di SELL degli
animali o valorizzazione automatica dello stock finale: il reward è cash.

Gate separato: incremento matched del reward contro la baseline già
corretta D10-D15, nessuna regressione dei suoi gate, residui terminali
quantificati e giustificati, costo del personale commisurato alle missioni
completate. Non accettare più cassa D29 se riduce l'incasso finale D30.

## Stato per la ripresa

E18.26 resta una candidata development con gate strutturale e incumbent
falliti. Le diagnosi sono salvate; il prossimo lavoro è costruire e
verificare il trattamento D10-D15 sopra definito. La chiusura D30 è una fase
successiva. Nessun codice strategico, config o piano congelato è stato
modificato in questo salvataggio; nessun commit/push eseguito.
