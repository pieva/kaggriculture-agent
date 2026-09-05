# E18 — ricostruzione strategica del Top 3 corrente

## Verdetto

Il confronto aggiorna e rafforza la conclusione della E18.5: ridurre la
topologia da `7-7-2` a `6-6-2` non risolve il collo di bottiglia logistico di
Codex. I tre leader osservati adottano geometrie incompatibili fra loro, ma
convergono su un throughput molto superiore: meno move, circa il 50% di azioni
produttive in più e fra il 73% e il 79% di raccolto in più rispetto alla E18.5.

La nuova linea causale raccomandata non è quindi un'altra ablation di
topologia. Deve partire dal controllo E18.2/V4D e intervenire sul ciclo
colturale e sulla conversione del tempo-worker in lavoro utile, conservando
inizialmente la geometria del controllo.

## Evidenza e perimetro

Snapshot pubblico Kaggle del `2026-09-04T10:21:06+02:00`:

| Rank | Player | Owner | Rating |
|---:|---|---|---:|
| 1 | Crop Dusta | Rishi Gottumukkala | 3032,3 |
| 2 | Giulio Ravasio | Giulio Ravasio | 2967,3 |
| 3 | Top770 | Top770 | 2960,4 |

Il corpus contiene undici replay recenti, tutti completi (`720` step,
`DONE/DONE`): quattro Crop–Giulio, quattro Crop–Top770 e tre Giulio–Top770. Ne
derivano otto profili Crop Dusta, sette Giulio e sette Top770, con entrambi i
seat coperti per ogni player. I replay grezzi sono stati usati in una cache
temporanea; nel repository restano soltanto artifact derivati e SHA-256.

Questa è evidenza osservazionale di discovery. Non permette di vedere codice,
inventario privato o stato fra episodi e non identifica causalmente perché una
policy vinca. In particolare, rating leaderboard, reward del singolo replay e
money di un runner locale sono quantità diverse.

## Confronto sintetico

| Profilo | N | W-L nel campione | Score medio | Topologia prevalente | Move | Produttive | Move/prod. | Harvest | Harvest/1k move |
|---|---:|---:|---:|---|---:|---:|---:|---:|---:|
| Crop Dusta | 8 | 6-2 | 91.907,6 | variabile; moda `5-4-2` | 4.058,5 | 3.237,3 | 1,2569 | 917,4 | 226,6 |
| Giulio Ravasio | 7 | 2-5 | 93.852,6 | `7-5-0` | 3.350,3 | 3.311,9 | 1,0118 | 886,6 | 265,1 |
| Top770 | 7 | 3-4 | 91.013,9 | `7-7-0` | 3.405,4 | 3.377,0 | 1,0099 | 897,3 | 264,3 |
| Codex E18.5 6-6-2 | 14 dev | 0-14 | 49.179,4 | `6-6-2` fissa | 4.451,9 | 2.223,1 | 2,0026 | 513,1 | 115,3 |

Il record W-L degli undici replay non ricostruisce la classifica: il rating
usa una storia molto più ampia. È però informativo che Crop Dusta chiuda 6-2
negli scontri selezionati, mentre Giulio realizzi lo score medio più alto pur
perdendo cinque partite, alcune con margine ridotto.

Rispetto a E18.5:

- Crop esegue `-8,8%` move e `+45,6%` produttive; il rapporto scende del
  `37,2%` e il raccolto per 1.000 move sale del `96,6%`;
- Giulio esegue `-24,7%` move e `+49,0%` produttive; il rapporto scende del
  `49,5%` e il raccolto per 1.000 move sale del `130,0%`;
- Top770 esegue `-23,5%` move e `+51,9%` produttive; il rapporto scende del
  `49,6%` e il raccolto per 1.000 move sale del `129,3%`.

Questi delta sono descrittivi: i leader giocano live fra loro, E18.5 contro un
controllo locale fisso. La semantica delle action e delle unità raccolte è
compatibile, ma non lo è il disegno sperimentale.

## Crop Dusta — analisi approfondita

### Osservazioni

Crop Dusta non usa una topologia canonica. Gli otto replay producono otto
action shape diverse e sette topologie finali: `5-1-0`, `5-4-2` due volte,
`5-5-5`, `6-5-8`, `6-8-5`, `8-4-0` e `9-7-3`. Q2 contiene pascoli in sei
profili su otto; i pascoli finali vanno da 6 a 19. La vecchia descrizione di
Crop come singolo layout distribuito è quindi superata.

L'apertura è invece molto stabile e aggressiva:

| Giorno | Crop medi | Pascoli medi | Animali medi | Mix medio dominante |
|---|---:|---:|---:|---|
| D1 | 13,0 | 5,0 | 5,0 | 8 Wheat, 5 Melon |
| D5 | 19,9 | 5,1 | 5,1 | ingresso Strawberry |
| D10 | 59,2 | 10,8 | 10,1 | 26,1 Wheat, 25,6 Strawberry, 7,5 Melon |
| D15 | 56,0 | 12,4 | 12,2 | 31,5 Strawberry, 18,8 Wheat |
| D20 | 55,0 | 14,0 | 13,2 | Strawberry/Wheat, Tomato situazionale |
| D25 | 53,9 | 14,0 | 13,2 | ritorno Wheat e prima liquidazione Carrot |
| D30 | 6,5 | 14,0 | 8,8 | liquidazione quasi completa |

Il terzo quadrante è disponibile a D9 in tutti gli otto profili e i dodici
worker a D10. Crop vende in valore circa `71,3%` prodotti agricoli e `28,7%`
prodotti zootecnici. Raccoglie in media 917,4 unità: 525,9 Wheat, 204,6
Strawberry, 77,9 Carrot, 69,5 Melon e 39,5 Tomato. Non risultano colture vive
estirpate prima della fine (`0` rotazioni medie), mentre il rapporto fra late
unwatered tile-days e late crop tile-days è `29,2%`, migliore del `38%` circa
di Giulio e Top770.

Crop non è il leader delle move normalizzate: `1,2569` è peggiore di Giulio e
Top770. Compensa con espansione tre giorni più precoce, più superficie
colturale già a D10 e riallocazione variabile del capitale fra pascoli e crop.
Nella fase D21–D30 migliora a `1,1913`, con 1.338,8 azioni produttive medie.

### Inferenza supportata

La ricostruzione più parsimoniosa è un controller guidato dallo stato e dal
capitale disponibile:

1. bootstrap comune D1–D9, con forza lavoro e frontiera colturale anticipate;
2. espansione pasture non fissata a un solo quadrante, ammessa anche in Q2;
3. regime agricolo Wheat/Melon iniziale, Strawberry/Wheat centrale e
   liquidazione Wheat/Carrot tardiva, con Tomato solo quando lo stato lo
   rende conveniente;
4. riduzione terminale sia dei crop sia di una parte degli animali;
5. priorità alla crescita e al rendimento assoluto, accettando più percorrenza
   di Giulio e Top770.

Gli otto action shape unici dimostrano adattamento all'episodio, non
adattamento causale all'identità dell'avversario. La variabilità può essere
guidata da prezzi, capitale, esiti delle action o farm pubblica avversaria; i
replay non separano questi meccanismi.

### Cosa non copiare alla cieca

Il valore di Crop non deriva da `9-7-3`, `5-4-2` o da qualsiasi altra
geometria singola. Nemmeno le 104,5 `PASS` medie su tile localmente
harvest-ready provano spreco: il proxy non vede priorità globali, inventario o
sincronizzazione. Copiare layout o soglie da un episodio distruggerebbe il
segnale più importante, cioè la capacità di cambiare assetto.

## Giulio Ravasio — strategia ricostruita

### Osservazioni

Giulio rappresenta un archetipo quasi opposto a Crop:

- zero pascoli in Q2 in tutti i sette replay;
- topologie `7-5-0` in tre casi, `7-7-0` in due, poi `7-2-0` e `10-7-0`;
- pascoli sempre pieni a fine partita: 12,86 pascoli e 12,86 animali medi;
- terzo quadrante a D12, dodici worker normalmente a D10;
- soltanto tre action shape, con la stessa shape in cinque replay su sette;
- 3.350,3 move e 3.311,9 produttive, rapporto `1,0118`; nella fase D21–D30
  le produttive superano le move (`0,9600`);
- 886,6 unità raccolte e 265,1 unità per 1.000 move;
- valore venduto bilanciato: `54,7%` crop e `45,3%` prodotti zootecnici.

Il calendario agricolo è estremamente leggibile. A D1 mantiene 12 Melon e 7
Wheat con quattro pascoli; a D5 i crop restano 19 e i pascoli salgono a sei;
a D10 passa a 20 Strawberry, 12 Melon e 5 Wheat; a D15 raggiunge circa 60
crop, divisi fra 37 Strawberry e 23 Wheat; a D25 torna Wheat-heavy, con circa
35 Wheat, 21 Strawberry e 4 Carrot; a D30 restano 1,4 Wheat medi. Non usa
Tomato nel campione. La raccolta media è 522 Wheat, 255,9 Strawberry, 72
Melon e 36,7 Carrot.

### Inferenza supportata

La policy di Giulio sembra una macchina a fasi con routing molto locale:

1. livestock compatto in Q0/Q1, Q2 riservato ai crop;
2. crescita dei pascoli più lenta di Crop, ma fill completo e mantenuto fino
   al termine;
3. target colturali per fase quasi deterministici;
4. piccoli rinnovi di colture vive (`3,7` medi), non rotazione aggressiva;
5. bilanciamento economico crop/livestock e liquidazione colturale finale;
6. lunghi blocchi di lavoro utile per destinazione, coerenti con un rapporto
   move/produttive vicino a uno.

La ripetizione della stessa action shape in cinque partite suggerisce che gran
parte dell'efficienza venga da un template robusto, non da re-planning globale
continuo. Le variazioni di topologia possono essere esiti condizionati da
capitale e contesa, non necessariamente quattro target espliciti. Top770
mostra un archetipo quasi identico e costituisce un controllo importante: la
firma efficiente non è esclusiva di Giulio.

Il campione non dimostra che `7-5-0` sia ottimale. Giulio è 1-3 contro Crop e
1-2 contro Top770 nei replay selezionati, pur essendo secondo in leaderboard e
avendo lo score medio più alto. La stabilità competitiva può dipendere dalla
minor varianza su una popolazione di avversari molto più ampia.

## Top770 — terzo comparatore

Top770 conferma il segnale di Giulio: zero pascoli Q2, `7-7-0` in quattro
replay su sette, 14,86 animali medi, tre action shape con una shape ripetuta
cinque volte, rapporto move/produttive `1,0099` e 264,3 raccolti per 1.000
move. Produce leggermente più lavoro e raccolto di Giulio nel campione, ma con
score medio inferiore. Le due policy osservate appartengono allo stesso
archetipo operativo; non c'è evidenza per affermare codice o strategia
condivisi.

## Confronto con la conclusione 6-6-2

La E18.5 aveva migliorato le move soltanto dello `0,57%` e il rapporto
move/produttive dello `0,82%`. Il nuovo benchmark spiega perché: rimuovere due
pascoli aveva lasciato invariato il dispatcher che genera trasferimenti e
manteneva un rapporto di circa due move per azione utile.

I leader falsificano due letture troppo forti:

- **“più compatto è sempre meglio”**: Giulio e Top770 sono compatti, ma Crop è
  primo con pasture Q2 in sei replay su otto e topologie fino a 19 pascoli;
- **“la dispersione impone molte move”**: Crop mantiene una struttura più
  dispersa ma usa comunque 393 move in meno e produce 1.014 azioni utili in
  più di E18.5.

Resta valida una conclusione più stretta: una linea compatta alla Giulio può
essere un buon regime, ma soltanto se nasce insieme a calendario agricolo,
fill completo, batching locale e liquidazione. La topologia da sola non è un
trattamento sufficiente.

## Direzione causale raccomandata

Questo report comune non assegna un identificativo di versione a un singolo
agente. Le eventuali specifiche Codex derivate sono mantenute sotto
`docs/model_specs/codex/`.

### Base e variabile causale

- base obbligatoria: E18.2/V4D, non il dispatcher E18.4/E18.5 respinto;
- topologia inizialmente invariata rispetto al controllo;
- unica famiglia modificata: priorità del ciclo colturale per fase e
  completamento locale di task compatibili prima di un nuovo trasferimento;
- nessun selector basato sull'identità dell'avversario o sui replay offline.

### Regimi da implementare

- `EXPAND`, fino al raggiungimento di 12 worker e tre quadranti;
- `STRAWBERRY_CAPACITY`, con espansione della superficie e servizio stabile;
- `WHEAT_RECOVERY`, orientato a raccolto e input zootecnici;
- `LIQUIDATE`, con stop a nuove colture non recuperabili, raccolta, deposito e
  vendita terminale.

I target di Crop e Giulio sono fixture di attivazione, non action table da
replicare. Ogni override deve registrare stato, task scelto, alternativa
scartata e motivo della priorità.

### Gate development proposti

Contro E18.2/V4D, sugli stessi seed e seat development:

- move/productive `≤ 1,20` e almeno `5%` migliore del controllo matched;
- productive action `≥ 3.000` oppure `+10%` sul controllo, usando la soglia
  più severa;
- harvested units `≥ 720` oppure `+20%` sul controllo;
- harvested units per 1.000 move `≥ 200`;
- late unwatered/crop-tile almeno `10%` migliore del controllo;
- money matched non negativo nel complesso e nessun match sotto `-5%` senza
  diagnosi preregistrata;
- zero errori, fallback, perdite verificate, residui vendibili terminali e
  regressioni di fill/safety;
- holdout, final e upload ancora bloccati.

Solo dopo il pass di questa linea è sensato isolare un secondo trattamento
Giulio-like `Q2_CROP_ONLY`, confrontando `7-5-0`/`7-7-0` con la geometria del
controllo senza cambiare nuovamente il lifecycle controller.

## Asset

- artifact JSON:
  `experiments/e18/artifacts/discovery/E18_CURRENT_TOP3_STRATEGY_BENCHMARK_2026_09_04.json`;
- profili CSV:
  `experiments/e18/artifacts/discovery/E18_CURRENT_TOP3_STRATEGY_PROFILES_2026_09_04.csv`;
- builder:
  `experiments/e18/tools/common/build_e18_current_top3_strategy_benchmark.py`;
- test:
  `experiments/e18/tests/test_e18_current_top3_strategy_benchmark.py`.
