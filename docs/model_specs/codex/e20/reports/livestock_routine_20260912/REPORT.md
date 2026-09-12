# E18 o E20: allevamento, regolarità del lavoro e prossima ricerca

12 settembre 2026. Analisi dei 14 scontri E18–E20.2, sette seed esposti e due ruoli. Nessuna nuova versione, simulazione o submission. E18 indica il bundle congelato E18.2 Capacity-Governed V4D, topologia 775; non tutte le revisioni storicamente chiamate E18.

**Raccomandazione: sospendere gli upgrade E20 e aprire un round mirato sulla E18 775, preceduto dall'audit delle sue missioni e del rendimento dei servizi.** La maggiore presenza di animali sembra compatibile con il controller e con assegnazioni più stabili. Non abbiamo però dimostrato che aggiungere animali renda di per sé più efficiente una strategia.

## Evidenza normalizzata

Medie per partita. Azioni e costi sono totali della fase; consistenze medie dei checkpoint giornalieri. D30 è escluso dalla fase stabile per evitare che la liquidazione e il taglio dell'organico confondano i servizi ordinari.

| Misura | E18 D12–19 | E20.2 D12–19 | E18 D20–29 | E20.2 D20–29 |
|---|---:|---:|---:|---:|
| Animali collocati, oca inclusa | 19 | 16 | 19 | 16 |
| Caselle coltivate medie | 52,88 | 56,30 | 51,30 | 43,16 |
| Persone medie | 13 | 12,80 | 13 | 13 |
| PASS richiesti | 167 | 306,29 | 36 | 215,71 |
| PASS / comandi lavoratori | 7,06% | 13,45% | 1,22% | 7,34% |
| MOVE richiesti | 1138 | 1074,29 | 1524 | 1639,50 |
| FEED riusciti | 144 | 127,57 | 180 | 149,07 |
| FEED / animale-giorno | 94,74% | 99,67% | 94,74% | 93,17% |
| CARE riuscite | 149 | 110 | 165 | 88,93 |
| CARE / animale-giorno | 98,03% | 85,94% | 86,84% | 55,58% |
| WATER riusciti | 270 | 286,86 | 307 | 297,64 |
| HARVEST riusciti, azioni non unità | 101 | 98,29 | 201 | 229,86 |
| Spesa assunzioni | 3008 | 2813,14 | 3760 | 3760 |
| Perdite colture per sete verificate | 6 | 0 | 15,86 | 2 |

Le esposizioni animale-giorno usano il checkpoint dei 22 KPI, non ogni variazione infra-giornaliera: sono una normalizzazione descrittiva, non il conteggio esatto delle obbligazioni FEED. In D12–D29 le consistenze sono stabili. I 19 animali E18 sono 8 mucche, 10 pecore e un'oca: non 19 bovini/ovini né tutti gli animali acquistati. E20.2 ha 10 mucche e 6 pecore.

**Il vantaggio FEED è soprattutto dimensionale.** E18 serve più animali, ma in D12–D19 la copertura normalizzata è inferiore a E20.2. In D20–D29 le coperture sono vicine. Inoltre solo circa il 95% delle richieste FEED/CARE di E18 produce un'esecuzione contabilizzata, contro il 100% di E20.2 in queste fasi. E18 non è universalmente migliore nella correttezza del servizio.

**Il vantaggio CARE non si esaurisce con il numero di animali.** In D20–D29 E18 esegue circa 76 CARE in più: applicando il tasso E20.2 ai tre animali aggiuntivi se ne spiegano circa 17; le altre 59 riflettono maggiore intensità di servizio, con questa specifica decomposizione descrittiva. Cambiano anche le specie e la regola E20.2 che da D20 esclude nuove CARE a prezzo corrente del prodotto pari a 1. Quindi più CARE non identifica automaticamente maggiore efficienza o redditività.

E18 mantiene più colture nel finale, ma perde anche più colture per sete. E20.2 esegue più HARVEST: il conteggio delle azioni non misura da solo quantità raccolta, durata della coltura o valore venduto. Il vantaggio di cassa E18 coesiste con un difetto di sicurezza agronomica; è un punto concreto da analizzare.

## Quanto sono davvero routinarie le assegnazioni?

Misura ricostruita dai replay: quota delle combinazioni lavoratore–casella–FEED/CARE del giorno che esistevano anche il giorno precedente, indipendentemente dall'ora. Si confrontano indici di assegnazione dei lavoratori, non identità persistenti fra giornate. Sono richieste e non solo esecuzioni riuscite.

| Persistenza assegnazione | E18 | E20.2 |
|---|---:|---:|
| D12–D19 | 17,78% | 8,66% |
| D20–D29 | 22,29% | 7,74% |

Il segnale è coerente con maggiore stabilità delle assegnazioni in E18. Non significa una routine rigidamente identica ogni giorno: imponendo anche la stessa ora, le ripetizioni D20–D29 sono appena 1,24% in E18 e 1,50% in E20.2. La regolarità sembra riguardare chi serve quali caselle più del calendario orario esatto.

Nel finale E18 combina tre animali aggiuntivi, circa otto caselle coltivate aggiuntive, 115 MOVE in meno e 180 PASS in meno a pari organico e costo delle assunzioni. È evidenza descrittiva di una migliore organizzazione complessiva in quella fase. Non permette di attribuire il vantaggio al solo allevamento: cambiano controller, distribuzione delle specie, colture, percorsi e calendario commerciale.

Il meccanismo plausibile è la compatibilità fra attività locali ricorrenti e rotte già organizzate: FEED, CARE, fertilizzante e raccolta animale possono essere serviti nella stessa zona; sostituire pascoli con colture introduce semina, irrigazione, maturazione, rinnovo e consegna con scadenze differenti. Liberare caselle e lavoratori funziona soltanto se il nuovo ciclo viene completato. Per misurare il risparmio di spostamenti specificamente attribuibile a questo meccanismo occorre un intervento controllato sulle assegnazioni, non questa correlazione.

## Collegamento con la cassa

Il vantaggio finale E18 è +3539: +18290,7 vendite meno 14422,4 maggiori acquisti e 329,4 maggiori assunzioni. D12–D19 ne genera +2679,7, circa il 76%; D20–D30 aggiunge +859,3. Il vistoso divario operativo tardivo non spiega quindi da solo dove nasce il vantaggio economico.

Fra i maggiori ricavi E18 figurano lana +6407,1, fertilizzante +3179,1, uova +1176,4 e latte appena +85. Il mix più orientato alle pecore è rilevante; i ricavi non sono utili netti e non isolano il rendimento delle CARE. Anche il grano va trattato separatamente: raccolti simili, ma E18 ne acquista e rivende molto di più.

Nel motore locale, CARE imposta il servizio del giorno; il bonus si accumula soltanto se l'animale è anche nutrito e viene consumato/reset nella sequenza di produzione. Contano data della prossima produzione, limite di accumulo del prodotto, raccolta, consegna e vendita entro il termine. Un servizio eseguito può non tradursi in ricavo incrementale. Il prezzo corrente pari a 1, d'altro canto, non dimostra che un bonus prodotto più avanti sarà privo di valore.

I negozi futuri dipendono dallo stesso RNG usato per le infestanti: politiche differenti possono cambiare la domanda anche a seed uguale. Le differenze di cassa totali restano reali nel motore, ma non sono effetti a prezzi e domanda invariati. Un controllo sintetico con negozi fissati è solo diagnostico.

## Rilettura dei tentativi storici

Questa è una revisione dei report conservati, non una riesecuzione né una certificazione retroattiva sul motore corrente. Campioni e avversari differiscono; non sommare questi risultati in una classifica unica.

| Esperimento | Evidenza conservata | Conseguenza per il prossimo round |
|---|---|---|
| E18.2 775, recupero sul posto | +3389,71 contro V4D, 14/14; deviazioni verso task distanti e recupero di pascoli precedenti respinti | Preservare le rotte è già una leva con evidenza positiva sulla base vincente |
| E18.3, riduzione delle topologie | 772 −14,31% contro controllo matched; altre riduzioni peggiori | La forma finale non basta; filtri sul controller non ripianificano il ciclo liberato |
| E18.11–16, ramo 770 | WATER extra senza output; hand Q2 −1165; cap risorse + FEED insieme migliorano +1,18% | Correggere obbligazioni e risorse coerentemente; non aggiungere servizi o personale a priori |
| E18.27 V3, ramo 770 | +13,44% sul proprio parent contro E18.16, ma zero vittorie dirette su E18.16; contro V4D solo due casi | Migliorare un parent debole non dimostra miglioramento della E18 775 |
| E18.29 B3, ramo 770 | +5721 sul parent, −420 PASS, +246,86 MOVE; sicurezza globale fallita per difetto ereditato di PLANT→WATER | Missioni chiuse e raccolta fertilizzante interessanti; non trasferire la patch senza isolare vincoli e sicurezza |
| H001, un HIRE omesso D20 | E18 +7930 ma solo 144 di salario risparmiato; più stress e una fuga | Non ridurre organico usando quel guadagno; gran parte del delta è nei flussi successivi |
| H002, rinvio vendita fragole | E18 −391/−162 nei due seed; lavoro identico | La monetizzazione è una leva distinta dal lavoro, senza regola universale di rinvio |
| H003–H006 | E18 già prioritizza fragole; inferenza concorrente con poca copertura; H006 completo riguarda E19, +18,5 medio | Nessuna ottimizzazione pronta da applicare alla E18 775 |
| E20.3–E20.7 | Nessun gate di adozione superato; E20.7 controller E18 adattato a 772 perde 7/7 seed | Altro segnale contro il trasferimento senza ridisegno; non prova inferiorità universale della 772 |

L'affermazione «abbiamo già esaurito E18» è quindi troppo forte: una parte importante della ricerca passata era sulla 770. La base 775 ha invece una storia positiva del recupero locale e difetti ancora misurabili. Una 772 ben progettata potrebbe comunque essere competitiva; i nostri test non escludono questa possibilità.

## Decisione prima della prossima versione

1. **Base di ricerca E18 775 congelata.** E20.2 resta confronto secondario. Nessuna nuova variante in questa analisi; il limite massimo E20.10 resta valido se si riapre quel ramo.
2. **Primo audit: missioni crop incomplete D12–D19.** Localizzare le sei perdite medie verificate: PLANT, acqua iniziale, scadenza successiva, posizione e impegni dei lavoratori. Cercare un completamento sul posto o dentro la rotta esistente. Non aggiungere manodopera né eliminare pascoli come ipotesi implicita.
3. **Audit separato del ciclo animale.** Per specie e casella ricostruire CARE→bonus→produzione→raccolta→vendita, bonus azzerati o bloccati dal limite, FEED non riusciti e capitale in animali non collocati. Questo distingue servizi remunerativi da routine senza ritorno. La presente analisi non completa ancora questa attribuzione marginale.
4. **Solo dopo, una modifica alla volta.** Misurare rispetto alla E18 invariata cassa propria e margine contro avversari reattivi, perdite, produzione venduta e costo logistico. Utilizzare i seed già esposti per diagnosi; preregistrare e congelare prima della conferma indipendente. Non imporre PASS più bassi come criterio di successo economico.

Preferirei iniziare dal completamento sicuro delle missioni crop, preservando il sottosistema animale che già funziona. L'ipotesi CARE va prima quantificata: né massimizzarla né ridurla indiscriminatamente. Non propongo di sommare immediatamente le patch storiche.

## Fonti e riproducibilità

- [Dati per partita, fase, definizioni e hash](ANALYSIS.json), generati da [script di analisi](../../tools/analyze_livestock_routine.py).
- [Torneo e traiettorie dei 22 KPI](../e20_2_confirmation/REPORT.html), [contabilità della cassa](../e20_2_confirmation/CASH_GAP.md).
- [E18.2 775](../../../e18/reports/E18_2_CAPACITY_GOVERNED_V4D_DEV_REPORT_IT.md), [ablation topologie](../../../e18/reports/E18_3_CODEX_INTERNAL_TOPOLOGY_ABLATION_REPORT_IT.md).
- [WATER e FEED nel ramo 770](../../../e18/reports/E18_770_WATER_OPTIMIZATION_POST_TOP3_EVIDENCE_REPORT_IT.md), [E18.27](../../../e18/reports/E18_27_D10_D15_CONSOLIDATED_V3_REPORT_IT.md), [E18.29](../../../e18/reports/E18_29_ANTI_PASS_DEVELOPMENT_REPORT_IT.md).
- [H001](../../../evolution/reports/diagnostic_20260910/H001_REPORT.md), [H002](../../../evolution/reports/H002/REPORT.md), [H003](../../../evolution/reports/H003/REPORT.md), [H004](../../../evolution/reports/H004/REPORT.md), [H005](../../../evolution/reports/H005/REPORT.md), [H006 completo](../../../evolution/reports/H006_FULL/REPORT.md).

Le 14 partite comprendono sette seed con ruoli appaiati, non 14 repliche indipendenti. Medie descrittive senza nuova selezione su holdout. Nessun bundle modificato.
