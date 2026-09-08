# Strategia Codex 770 — pianificazione biologica e percorsi di lavoro

Questa specifica descrive il comportamento implementato nella V48. Il nome
identifica la policy riproducibile, non una promessa di prestazioni. Il codice
rimane invariato durante questa revisione documentale.

## Impostazione strategica

**Pianificare i cicli biologici e organizzare la manodopera necessaria a
completarli.** Una semina o un nuovo animale impegnano lavoro nei giorni
successivi: l'investimento deve comprendere i servizi, la raccolta e la
consegna che ne rendono possibile il ritorno economico.

L'ordine delle decisioni è quindi: produzione desiderata → calendario dei
lavori → capacità e distribuzione della manodopera → investimenti ammissibili.
Se il carico non è sostenibile, occorre rivedere il piano produttivo o la
capacità disponibile prima di assumere nuovi impegni.

Questa è l'impostazione di riferimento. La V48 la realizza parzialmente con
intenzioni colturali, calendari e verifiche giornaliere: non dispone ancora
di una verifica completa della capacità lungo tutti i cicli biologici.

## Obiettivo e ambito

Il modello cerca di ottenere un risultato economico attraverso una fattoria
con assetto obiettivo 7-7-0 dei pascoli nei tre quadranti utilizzati. Combina
un avvio assistito, intenzioni colturali persistenti e assegnazione giornaliera
del lavoro. La topologia obiettivo non garantisce che gli asset siano sempre
popolati o che tutte le colture previste siano effettivamente seminate.

La strategia è ibrida: il piano biologico propone cosa mantenere produttivo;
lo stato osservato e la capacità residua determinano quali lavori ammettere.
Non è un calendario completo, fisso e ottimizzato per tutte le partite.

## Pianificazione della produzione

- **Avvio:** mantiene il controllo assistito fino a D11; i moduli successivi
  intervengono sulla gestione produttiva e sulla distribuzione del lavoro.
- **Colture:** conserva intenzioni per casella, con obiettivi nominali di 23
  caselle di grano e 38 di fragole. Sono proposte subordinate alla fattibilità,
  non consistenze garantite. Le nuove semine devono poter maturare lasciando
  tempo per raccolta e consegna prima della fine.
- **Calendario biologico:** ricava produzione, ultima raccolta e giorni utili
  per fertilizzare dalle regole del gioco e dalla data di semina o insediamento.
- **Servizi:** genera lavori di alimentazione, cura, irrigazione e raccolta
  sulla base delle necessità osservate. Il piano delle fragole include anche
  irrigazione alternata secondo posizione e giorno.
- **Successione:** distingue colture ancora produttive da colture esaurite e
  tenta di combinare rinnovo e servizio nella stessa visita quando ammissibile.

## Pianificazione della manodopera

Il piano distribuisce responsabilità territoriali compatte sulle persone
effettivamente presenti. Una partizione iniziale segue le caselle per righe
alternate e pesa maggiormente le caselle con animali; non rappresenta una
stima esatta del carico biologico futuro.

I percorsi giornalieri raggruppano visite e contabilizzano spostamenti,
comandi e prelievi dal deposito. Restano validi fino al completamento o alla
loro invalidazione. Il calcolo non presume assunzioni future.

Prima di ammettere una missione, il dispatcher verifica che rimanga capacità
per gli obblighi giornalieri. La verifica alternativa per inserimento considera
anche missioni già attive, inventari e budget residui e cerca di collocare i
servizi FEED, CARE e WATER ancora necessari. È una verifica del giorno corrente,
non una garanzia di fattibilità dell'intero mese.

## Componenti reattive e rapporto con il piano

La componente reattiva serve a mantenere eseguibile il piano quando lo stato
reale diverge dalle previsioni. Non dovrebbe ricalcolare continuamente la
strategia né abbandonare gli impegni biologici per un'opportunità immediata.

| Situazione | Risposta della V48 | Limite da controllare |
|---|---|---|
| Cambiano giorno, terreni disponibili o numero di lavoratori | Aggiorna il piano osservato e le responsabilità territoriali. | Il ricalcolo può non riflettere tutto il carico futuro. |
| Una missione compete con servizi già dovuti | Verifica la capacità residua per gli obblighi del giorno. | Un vincolo troppo restrittivo può scartare lavoro utile e generare PASS. |
| Risorse o tempo non consentono una nuova coltura | Filtra le proposte di crescita e successione. | Il terreno può rimanere vuoto se non viene trovata un'alternativa fattibile. |
| Una coltura termina il ciclo | Valuta rinnovo e servizi nella stessa visita. | La successione deve essere tempestiva senza sacrificare raccolte o servizi. |
| Nessuna missione viene selezionata | Conserva i meccanismi di recupero e PASS del controller. | Non c'è ancora una diagnosi completa che distingua attese inevitabili da blocchi del planner. |

La proprietà da verificare è che il recupero risolva gli scostamenti con lavoro
produttivo. Un aumento di MOVE o di servizi non necessari non costituisce una
correzione del problema PASS.

## Chiusura della partita

Il piano viene aggiornato al variare del giorno, dei quadranti disponibili e
del numero di lavoratori. Le proposte di crescita sono filtrate in base a
risorse, stato delle caselle e tempo rimasto. Il controller conserva meccanismi
di recupero, consegna e PASS quando nessuna missione viene selezionata.

Verso la chiusura, le nuove colture sono scelte in funzione della maturazione
residua; grano e carote possono sostituire investimenti con ritorno troppo
lontano. Le priorità terminali valorizzano raccolta e consegna. In D28–D30,
la V48 può proporre WATER seguito da HARVEST sulle colture annuali quando
l'acqua aumenta ancora la resa: il lavoro completo deve essere fattibile;
la guardia evita di degradarlo a una sola irrigazione priva della raccolta.

## Limiti del comportamento implementato

Le intenzioni colturali e la verifica dei percorsi non eliminano i PASS
evitabili. Il modello non dispone ancora di una spiegazione completa, per
persona e ora, delle attese né di un dimensionamento della manodopera che
garantisca equilibrio fra carico biologico futuro e capacità disponibile.
Questi sono limiti della strategia descritta, non funzionalità già risolte.

## Come si controlla l'ottimizzazione

Il risultato economico finale misura l'esito del modello. Per capire perché
cambia, l'analisi segue l'intera catena produttiva e distingue le fasi di avvio,
produzione e chiusura. Una media mensile favorevole non basta se nasconde
giorni con servizi scoperti o capacità inutilizzata.

| Aspetto | Cosa verificare |
|---|---|
| Piano biologico | Produzioni previste ed effettive, raccolte tempestive, continuità della successione, perdite produttive e infestanti. |
| Capacità di lavoro | Lavoro necessario rispetto a persone e tempo disponibili, carico per giorno e distribuzione fra persone. |
| Esecuzione | PASS e MOVE, lavori scartati e servizi completati rispetto a quelli necessari. |
| Economia | Cassa nel tempo, costo della manodopera, investimenti e ricavi; risultato finale. |

L'ottimizzazione segue questi passaggi:

1. Identificare uno scostamento preciso, con giorno, stato e azioni che lo
   producono. Per i PASS, distinguere assenza di lavoro utile, carenza di
   risorse, tempi di viaggio, sovracapacità e blocchi di assegnazione.
2. Formulare una causa verificabile e una modifica coerente con il piano.
   Dichiarare prima del confronto quale comportamento dovrebbe cambiare
   e quali risultati non devono peggiorare.
3. Confrontare la variante con la baseline congelata sugli stessi casi,
   esaminando anche le traiettorie dei KPI e i singoli fallimenti.
4. Confermare il beneficio su casi nuovi. Se non si conferma, rivedere
   l'ipotesi; non promuovere la variante soltanto perché migliora un KPI.

Per una modifica mirata ai PASS, la riduzione deve riguardare attese evitabili
e accompagnarsi a un uso produttivo della capacità. Vanno protetti raccolte,
FEED, CARE, WATER necessario e risultato economico. I motivi dei PASS e il
confronto fra carico previsto e realizzato richiedono ancora telemetria più
completa: il protocollo non implica che tutti questi controlli siano già automatici.

## Benchmark e criteri di confronto

| Confronto | Scopo | Limite |
|---|---|---|
| Variante contro V48 congelata | Isolare gli effetti delle modifiche, usando gli stessi seed e posti di gioco. | Sono casi di sviluppo quando vengono usati per correggere la variante. |
| Riferimento storico V4D | Mantenere continuità con i confronti locali precedenti. | Superarlo non dimostra da solo competitività esterna. |
| Replay dei Top | Confrontare calendari, utilizzo del terreno, servizi e gestione delle persone; formulare ipotesi. | Partite e condizioni differenti non permettono di attribuire causalmente il vantaggio a una singola scelta. |
| Casi locali nuovi e confronto esterno Kaggle | Verificare se il miglioramento si mantiene fuori dai casi di sviluppo. | I casi diventano esposti una volta usati per orientare le correzioni. |

Il confronto deve mostrare tutti i casi previsti, non soltanto quelli
favorevoli, con numerosità e dispersione dei risultati. Seed uguali non
garantiscono condizioni identiche dopo azioni differenti. Nei replay Top
si distinguono topologia durante la produzione e topologia finale; eventuali
coorti miste devono essere dichiarate.

Il [registro dei benchmark Top](../../../../experiments/e18/reports/common/E18_TOP770_BENCHMARK_ROTATION_REGISTER_IT.md)
registra gli autori già analizzati per evitarne il riuso come prova indipendente.
Gli esiti numerici e le decisioni di promozione appartengono ai report; questa
specifica conserva il metodo e i criteri con cui interpretarli.

## File che codificano la strategia

Questi sono tutti i 18 sorgenti incorporati nella submission, verificabili
nel [manifest del bundle](artifacts/derived/v48_external_manifest.json).
La presenza di versioni precedenti nei nomi indica dipendenze effettivamente
riutilizzate dalla V48.

| Responsabilità | Sorgente |
|---|---|
| Core parametrico e controller | [submission_codex_e19_control_770_v2.py](../../../../submission/submission_codex_e19_control_770_v2.py) |
| Avvio assistito e creazione della policy | [submission_codex_e18_770_assisted_start_v1_candidate.py](../../../../submission/submission_codex_e18_770_assisted_start_v1_candidate.py) |
| Continuità produttiva di base | [productive_continuity.py](tools/productive_continuity.py) |
| Successione delle colture | [portfolio_succession_v14.py](tools/portfolio_succession_v14.py) |
| Esecuzione del portafoglio produttivo | [portfolio_execution_v14.py](tools/portfolio_execution_v14.py) |
| Vincoli di ammissione del portafoglio | [portfolio_governed_v14.py](tools/portfolio_governed_v14.py) |
| Raggruppamento dei lavori | [portfolio_batched_v14.py](tools/portfolio_batched_v14.py) |
| Coordinamento dei lavori concorrenti | [portfolio_concurrent_v14.py](tools/portfolio_concurrent_v14.py) |
| Logistica del portafoglio | [portfolio_logistics_v14.py](tools/portfolio_logistics_v14.py) |
| Piano giornaliero di base | [portfolio_day_plan_v14.py](tools/portfolio_day_plan_v14.py) |
| Limiti di pianificazione | [portfolio_bounded_v14.py](tools/portfolio_bounded_v14.py) |
| Gestione terminale di base | [portfolio_terminal_v14.py](tools/portfolio_terminal_v14.py) |
| Gestione della manodopera e valore dei servizi | [portfolio_workforce_v16.py](tools/portfolio_workforce_v16.py) |
| Scheduler di base | [portfolio_scheduler_v16.py](tools/portfolio_scheduler_v16.py) |
| Intenzioni colturali, calendario biologico e responsabilità territoriali | [biological_plan_770_v48.py](tools/biological_plan_770_v48.py) |
| Costo e composizione dei percorsi, acqua produttiva | [daily_routes_770_v48.py](tools/daily_routes_770_v48.py) |
| Ammissione ed esecuzione delle missioni | [daily_route_dispatch_770_v48.py](tools/daily_route_dispatch_770_v48.py) |
| Verifica alternativa per inserimento dei lavori | [daily_route_scheduler_770_v48.py](tools/daily_route_scheduler_770_v48.py) |

Il builder parte dallo scheduler V48 e incorpora le dipendenze importate.
I moduli installano progressivamente funzioni sul core: per capire una scelta
finale occorre considerare anche gli override, non soltanto il modulo di base.

## Produzione e verifiche

| Scopo | File |
|---|---|
| Generazione del bundle | [build_v48_submission.py](tools/build_v48_submission.py) |
| Agente standalone risultante | [submission_codex_e18_770_v48_external.py](../../../../submission/submission_codex_e18_770_v48_external.py) |
| Benchmark locale | [run_daily_routes_770_v48.py](tools/run_daily_routes_770_v48.py) |
| Parità fra policy e bundle | [run_v48_external_parity.py](tools/run_v48_external_parity.py) |
| Verifica acqua produttiva | [test_productive_water_v48.py](tests/test_productive_water_v48.py) |
| Verifica dell'audit biologico | [test_crop_lifecycle_audit_v48.py](../../../../tests/test_crop_lifecycle_audit_v48.py) |

## Documenti complementari

- [Stato del progetto](../../../PROJECT_STATE.md): risultati correnti e lavoro successivo.
- [Piano operativo e inventario delle analisi](../../../foundation/V48_PLANNING_AND_BUILD_IT.md): priorità PASS, benchmark, report e conservazione degli artefatti.
- [Roadmap parametrica storica](MODEL_SPEC_CODEX_E19_PARAMETRIC_VALIDATION_DRAFT.md): mandati e decisioni precedenti; non descrive la strategia implementata nella V48.
