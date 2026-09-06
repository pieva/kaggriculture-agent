# E18.33 — policy comune di pascoli, colture e capacità

Stato 2026-09-06: **KERNEL E PROTOTIPO NATIVO IMPLEMENTATI, gate fallito;
non candidato pubblicabile.** La specifica normativa non è ancora implementata
integralmente: vedere sezione 9 e checkpoint delle prove.
Supera il mandato di continuare ad adattare le code E18.28 tramite E18.32.
E18.31 ed E18.32 V9 pubblicate restano controlli immutabili; E18.32 V9
(56056189, Complete) è solo controllo provvisorio, non benchmark E19.
L'analisi dei residui è in `reports/E18_33_LEGACY_POLICY_AUDIT_20260906_IT.md`.

Aggiornamento più recente: prove native V6–V9 e bootstrap esplicito minimo,
97 test mirati E18.32/E18.33 passati. Il profilo V2 limita il primo avvio a
due COW/due SHEEP e WHEAT/CARROT fino al primo raccolto confermato. Il profilo
V3 estende il rilascio al rinnovo completo del primo ciclo e a condizioni
finanziarie: quattro casi, rilascio D16–D17, nessuna 770, economia fallita.
**V3 è una sonda respinta, non una nuova prescrizione normativa.** L'avvio
non deve imporre blocchi globali di medio termine, neppure con condizioni di
stato anziché date. Archivi V6/V7/V8/V9 e risultati non vanno sovrascritti.
Dettaglio: `reports/E18_CLOSEOUT_AND_BOOTSTRAP_20260906_IT.md`.

## 1. Principio vincolante

Q0, Q1 e Q2 usano gli stessi generatori di opportunità, criteri economici,
servizi biologici e assegnatore. **Nessun programma per quadrante.**
La disponibilità del terreno abilita le decisioni; non avvia un calendario
«giorno locale 1, 5, 14» che riproduca quello vecchio.

A parità di stato, geometria relativa, budget, risorse, quota di pascoli e
orizzonte residuo, rinominare il quadrante non deve cambiare la decisione.
Questo non impone consistenze identiche: Q1 si attiva più tardi, con cassa e
orizzonte differenti. Tali differenze devono essere spiegate da input osservati,
non da rami `if Q0`, `if Q1`, `if Q2` nel modello economico.

Input ammessi: osservazione corrente e memoria causale della sola partita,
regole motore verificate, profilo globale. Vietati: seed, autore, replay,
score/curve del benchmark, piani di altre release, calendario di acquisti o
coordinate strategiche precalcolate. Il giorno serve a ricavare età e tempo
residuo, non a cambiare policy a metà mese.

## 2. Profilo globale e topologia derivata

Profilo iniziale: obiettivo `P=14` pascoli popolati, capacità uniforme per
quadrante `K=7`, massimo tre quadranti e dodici manovali. Il cap totale degli
animali è derivato da P: **non esiste un secondo 14 indipendente**.
Contare animali collocati, in magazzino, trasportati e acquisti prenotati senza
doppio conteggio. Un animale acquistato deve avere una missione di collocamento
finanziata e realizzabile; niente acquisti soltanto per raggiungere uno stock.

Per mantenere la concentrazione concordata senza configurare `[7,7,0]`,
assegnare capacità nell'ordine in cui i terreni sono resi disponibili dal motore:

`budget_pascoli(rango) = min(K, max(0, P - K * rango))`, rango iniziale zero.

Il rango è una proprietà dell'acquisizione, non il nome Q0/Q1/Q2. La stessa
funzione si applica a tutti; i budget sono obiettivi di assetto, non ordini di
acquisto incondizionati. Non spostare animali già collocati per ottimizzare
nuovamente un ordinamento geometrico a ogni turno.

| Profilo di contratto | Terreno 1 | Terreno 2 | Terreno 3 |
|---|---:|---:|---:|
| P=14, K=7, corrente | 7 | 7 | 0 |
| P=15, K=7, test sintetico | 7 | 7 | 1 |
| P=14, K=6, test di generalità | 6 | 6 | 2 |

I profili alternativi non autorizzano una nuova topologia in partita. Con P=15,
Q2 deve produrre una candidatura al pascolo senza modificare codice, date o
coordinate; la posa avviene quando terra, liquidità e capacità lo consentono,
non automaticamente se tali prerequisiti mancano.

Per non mantenere cap specie incompatibili con P, il profilo conserva il mix
di riferimento come pesi globali COW:SHEEP = 9:5. Quote intere con metodo dei
maggiori resti: P=14 → 9/5; P=15 → 10/5. È una scelta di profilo esplicita,
non un vincolo biologico. L'ordine degli acquisti fra specie con quota residua
dipende da rendimento, liquidità e lavoro; entrambe usano la stessa policy.
GOOSE/COOP non sono introdotti in questa tranche.

## 3. Ciclo decisionale unico

Ogni osservazione riconcilia conferme, posizioni, cassa, semi, prodotti,
inventari e missioni. Rigenerare le opportunità interessate da raccolto,
vendita, sblocco, morte/fuga, acquisto, assunzione o scadenza; il cambio giorno
aggiorna obblighi e capacità osservati, non seleziona un altro programma.

Un unico libro delle risorse distingue:

- risorse osservate libere, impegnate, in transito e ricavi soltanto attesi;
- servizi già dovuti, nuove attività ammesse e alternative non ancora finanziate;
- deadline biologiche, di finanziamento e ultimo istante eseguibile.

Le azioni/rotte sono l'OUTPUT di queste decisioni, non una trajectory di input.
È ammesso un rollout futuro generato dallo stato e rivalutato; non una tabella
di ordini congelata prima della partita. La funzione economica è l'incremento
prudente della cassa finale rispetto all'alternativa, non il numero di PASS
eliminati o la somiglianza a una curva esterna.

## 4. Policy comune dei pascoli

1. **Generazione:** quota locale/globale residua, animale mancante in struttura
   esistente o opportunità di nuova attivazione. Valutare COW e SHEEP con i
   rispettivi dati biologici, senza soglia unica di otto giorni.
2. **Scelta della tile:** enumerare terreno disponibile, pascoli vuoti, erbacce
   e colture candidate alla conversione. Confrontare costo del completamento,
   costo delle visite ripetute e della consegna, opportunità colturale persa.
   A pari stato e valore preferire la minore distanza di servizio dal magazzino;
   coordinate solo come ultimo spareggio deterministico, mai come lista target.
   Q0 deve quindi rivalutare per prime anche le posizioni centrali finora rinviate.
3. **Ammissione integrata:** confrontare crescita e rinnovo colture nello stesso
   problema di liquidità/capacità. Certificare acquisto → trasporto → eventuale
   DIG/BUILD → PLACE → primo FEED, e il successivo ciclo di mantenimento e ricavo.
   CARE entra per il suo beneficio marginale. L'investimento stesso crea lavoro:
   non ridurre prima il personale ignorando questa domanda potenziale.
4. **Finanziamento:** proteggere i servizi esistenti e il loro approvvigionamento.
   Latte/lana/fertilizzante diventano denaro spendibile soltanto dopo una
   sequenza di consegna/vendita legalmente eseguibile. Certificare il saldo a
   ogni passo, non soltanto la somma a fine giorno. In caso di impossibilità,
   servire le attività esistenti e spiegare il rinvio, senza fallback al piano.
5. **Servizio:** FEED da stato osservato e deadline; CARE in funzione del bonus
   ancora incassabile; HARVEST prima della saturazione/perdita o per finanziare
   un impegno; raccolta fertilizzante se utile alla vendita o a una coltura.
   Stesse regole, nessun blackout per giorno o quadrante.
6. **Ripristino:** un pascolo vuoto genera subito una candidatura di riempimento.
   Non è obbligatorio un acquisto antieconomico a fine partita. Ogni rifiuto ha
   una causa osservabile e viene rivalutato quando cambiano i prerequisiti.

Il settimo pascolo non è «speciale»: compete con il valore del raccolto presente
e con le altre opportunità. La quota non giustifica distruggere prematuramente
una coltura produttiva né bloccare per giorni una tile senza missione ammessa.

## 5. Policy comune delle colture

**Stesso insieme di specie e stesso selettore in tutti i quadranti.** Nessun
obbligo «12 meloni in Q0», «18 fragole in Q1» o «7 grani in Q2». Non si vietano
i meloni perché assenti in un benchmark. La composizione diventa un risultato
della valutazione economica, della maturazione e delle risorse.

### Attivazione e scelta

Ogni tile senza produzione viene rivalutata, comprese quelle appena raccolte.
Per ciascuna specie ammessa confrontare:

- costo dei semi e tempo del primo ricavo realmente vendibile;
- resa incrementale, raccolti residui e durata del ciclo secondo il motore;
- PLANT, primo WATER, mantenimento, raccolto, consegna e rinnovo necessari;
- denaro immobilizzato e rischio di sottrarlo a FEED, salari o crescita ammessa;
- grano necessario agli animali: autoconsumo evita un acquisto, non genera
  contemporaneamente un ricavo di vendita; stessa contabilità per fertilizzante;
- costo-opportunità della terra e capacità futura richiesta lungo il ciclo.

I prezzi futuri non sono noti: usare i due scenari preregistrati sotto, includendo
impatto dei propri volumi sul mercato. Non usare prezzi futuri del replay o
assumere che il prezzo corrente valga per un intero lotto.

Nessuna nuova semina senza certificare PLANT → primo WATER e mantenimento
sostenibile. Una coltura breve su area destinabile a pascolo è ammessa soltanto
se il piano comune non rileva un investimento migliore già realizzabile e se
il suo valore considera l'eventuale conversione. La prenotazione durevole della
tile nasce da una missione ammessa, non da una data futura del vecchio piano.

### Irrigazione, raccolto e rinnovo

- WATER distingue prevenzione della perdita e incremento di resa. Non ripetere
  un servizio già confermato; mai usarlo solo per sostituire un PASS.
- FERTILIZE deve aumentare una resa ottenibile nella sua finestra reale, al netto
  della vendita alternativa e del costo del servizio; niente budget per giorno.
- HARVEST confronta ricavo attuale, incremento attendendo, liquidità necessaria,
  saturazione, decadimento e valore del ciclo successivo. Nessun raccolto fissato
  a D11 oppure ogni due giorni per imitare una traiettoria.
- Dopo raccolto annuale, la tile torna immediatamente al selettore. Se la nuova
  semina è ammessa, concatenare HARVEST → PLANT → WATER quando fattibile; altrimenti
  registrare quale risorsa impedisce il rinnovo e rivalutarlo alla prossima
  variazione utile. Vietato un intervallo imposto D11 → D14.
- Per le pluriraccolto calcolare produzioni residue e scadenza effettiva: non
  assumerle perpetue. Sostituire quando il nuovo ciclo vale più della continuazione,
  includendo DIG e raccolto residuo, non a un giorno assegnato alla coordinata.
- WEED è stato da gestire quando libera una capacità redditizia, non un lavoro
  da eseguire ovunque per consumare manodopera.

Q2 applica tutto quanto sopra: con budget pascoli zero, tutte le sue tile possono
essere valutate per colture; con budget uno, il confronto coltura/pascolo cambia
su una tile selezionata online, senza sostituire la policy del quadrante.

### Prima valutazione economica preregistrata, comune a pascoli e colture

Il termine di confronto è il portafoglio di impegni già ammessi, non l'inattività
di tutta la fattoria. Valutare ogni alternativa fino al termine eseguibile,
con gli stessi obblighi e la stessa contabilità in entrambi i rami.

`delta_cassa_s = cassa_finale(portafoglio + alternativa, s) - cassa_finale(portafoglio, s)`.

Due scenari, uguali per ogni tile, specie e giorno:

1. **Neutro condizionale:** curva di mercato verificata nello stato corrente,
   includendo i propri acquisti/vendite per unità; nessuna previsione di ordini
   futuri dell'avversario o di eventi non ancora osservati.
2. **Prudente storico della sola partita:** ricavi valutati al minore fra la
   quotazione neutra e la minima quotazione osservata finora per quel prodotto;
   costi di acquisto al maggiore fra neutra e massima osservata. Stessi spread,
   arrotondamenti e vincoli motore. Nessuna finestra «D5–D10» né dati cross-episode.

Questi scenari sono ipotesi diagnostiche, non limiti garantiti dei prezzi futuri.
Nessuna previsione può sbloccare una spesa ora senza una sequenza finanziaria
materialmente fattibile. Riesaminare la missione prima di ogni acquisto.

Per attività discrezionali richiedere `min(delta_cassa_s) > 0` e fattibilità
del servizio/finanziamento in entrambi gli scenari. Servizi già ammessi e
prevenzione di perdite non vengono cancellati perché una nuova previsione di
prezzo peggiora: si gestiscono nel portafoglio delle obbligazioni.

Scegliere il maggiore incremento prudente fra alternative ammissibili; a parità,
maggiore incremento per azione aggiuntiva, poi incasso più tempestivo e costo
di rotta minore. Dopo ogni ammissione ricalcolare le risorse residue e i margini:
non sommare offerte che usano gli stessi semi, tile, animali o slot. Il costo
incrementale comprende salari effettivamente aggiunti e opportunità escluse,
non un costo monetario inventato per ogni movimento.

Questa è l'ipotesi iniziale V1, da implementare e sottoporre ad ablation: non
si cambiano scenari o criteri dopo aver guardato i risultati senza registrare
una nuova variante. Il rollout biologico e la stima di capacità devono prima
passare verifiche sul motore; finché mancano, nessun margine è un guadagno provato.

## 6. Capacità, acquisto terreni e chiusura

Il pool assegna missioni ai lavoratori realmente osservati e può acquistare
capacità aggiuntiva entro il massimo globale. Considera prima tutte le
opportunità sostenibili, inclusa crescita animale; non assume un roster del
benchmark e non risolve l'anti-PASS soltanto assumendo meno persone.
Numero dei lavoratori e superficie attivata si determinano insieme.

Proteggere deadline di sopravvivenza e obblighi ammessi; fra alternative fattibili
scegliere il maggior incremento economico con costi di rotta e salari reali.
Una scelta al solo rapporto valore/MOVE non basta: può ritardare la consegna
che finanzia il cibo. Risorse, semi e servizi sono riservati una volta sola;
PLANT concorrenti devono rispettare la validazione atomica dei semi del motore.
Un servizio confermato libera il suo vincolo anche se il trasporto prosegue.

BUY_LAND usa il prossimo terreno legalmente acquistabile e richiede un piano
di utilizzo sostenibile. Valutare prima il margine del terreno già posseduto,
senza imporre di occuparlo tutto quando le alternative sono antieconomiche.
L'acquisto non deve dipendere da una futura riga PLANT della trajectory.

La chiusura usa tempo residuo e ultimo batch effettivo. Il reward locale è la
cassa, non il valore delle colture in campo: includere raccolto/consegna/vendita,
senza attribuire liquidazione automatica agli asset. Nessun CLEAR, riduzione
del personale o cambio coltura imposto da D25/D28/D30. Una semina tardiva o un
CARE senza ricavo consegnabile non è utile, anche se riduce i PASS.

PASS è ammissibile solo quando nessuna missione utile è fattibile per quella
unità. Deve essere diagnosticabile con prerequisito mancante, deadline,
assenza di valore incrementale o risorsa riservata. Non sono spiegazioni valide
«Q0 non attivo per quel ruolo», «non è D14», «coda personale terminata».

## 7. Bonifica della configurazione e dipendenze

Profilo pulito: `configs/CODEX_E18_33_COMMON_RESOURCE_POLICY_V1.json`;
schema chiuso omonimo `.schema.json`. Il profilo contiene solo obiettivi globali,
limiti e insieme delle specie, non biologia duplicata o valori del benchmark.
La validazione strutturale non dimostra fattibilità: l'adattatore deve anche
verificare target rispetto a dimensioni del terreno, cap locale e limite terreni.

La nuova implementazione non deve ereditare i controller E18.18–E18.32 né
caricare `trajectory`, `calendar`, `reference_plan` o `treatment_config`.
Riuso ammesso: primitive indipendenti di percorso, missioni, riconciliazione e
adattamento al motore, estratte e testate senza importare il planner storico.
Fallback: manutenzione sicura guidata dallo stato, mai riattivazione del vecchio
programma. Tutti i file storici restano immutabili e utilizzabili dal runner
come avversari/controlli esterni alla policy nuova.

## 8. Applicazione iniziale a Q0 e criteri di verifica

Q0 è il primo caso diagnostico, non una nuova eccezione nel codice produttivo.

1. **Contratto puro:** validatore delle chiavi; prova di rinomina dei quadranti
   e trasformazione della geometria relativa; stesso input economico/biologico
   → stesse decisioni salvo spareggi equivalenti. Rango/quote si trasformano
   insieme allo stato. Mai pretendere stessa decisione con cassa diversa.
2. **Generalità strutturale:** P 14 → 15 genera il quindicesimo pascolo sul
   terzo terreno, se fattibile, senza altro parametro cambiato; vicino alla fine
   o senza fondi deve spiegare perché non lo ammette. Nessun upload a 15 pascoli.
3. **Q0, shadow diagnostico:** valutare apertura, le tile centrali vuote, il
   settimo pascolo ancora a grano e ogni uscita dal raccolto dei meloni. Registrare
   alternative, margine, costo di servizio, vincolo e momento di rivalutazione.
   Replay già consumati utilizzabili per diagnosi, non per profitto controfattuale.
4. **Q0, prova interna isolata:** un eventuale trattamento Q0-only vive SOLO nel
   test harness e condivide risorse globali, senza duplicare obbligazioni con il
   controllo. Serve all'attribuzione causa/effetto, non è un agente rilasciabile.
   Non cambiare contemporaneamente pesi del mix, cap animali e limite persone.
5. **Q1/Q2, verifica di trasferimento:** chiamare le stesse funzioni, senza
   copia del programma Q1. Q1 è un controllo di non regressione su servizio,
   continuità colturale ed economia; il suo stock apparentemente buono non prova
   che il calendario sia ottimale.
6. **Gate integrato:** simulazioni complete su campioni interni E18.16 ed
   E18.2/V4D, due seat, seed development preregistrati 180903001–007. Confronti
   con E18.31 e V9: safety assoluta, cap, liquidità, cassa finale e distribuzione
   dei delta per avversario, PASS/slot, lavoro utile riuscito, MOVE, salari,
   animali-giorno produttivi, rinnovo e terreno inattivo. Non richiedere identità
   delle vecchie consistenze colturali: cambiare la policy può cambiarle.

Nuovi KPI diagnostici per quadrante: ore-tile disponibili improduttive,
tempo HARVEST→PLANT/WATER, tempo pascolo vuoto→PLACE/FEED, costo di servizio per
tile e ciclo, contributo economico senza doppio conteggio, opportunità redditizie
rinviate con relativa causa. Distinguere quante azioni riescono, quante sono
solo richieste e quante generano valore. PASS da solo non è un gate economico.

Nessuna promozione con nuove morti/fughe, missioni incomplete, superamento dei
cap o bug di liquidità. Nessuna promozione dal solo calo dei PASS assoluti.
Richiesti beneficio economico robusto e trasferibilità, non aderenza a Top770.
I due scenari e il criterio di ammissione V1 sopra sono preregistrati PRIMA del
nuovo gate. Congelare l'implementazione e il protocollo delle misure prima
dell'esecuzione, senza scegliere a posteriori i casi favorevoli.

## 9. Stato delle consegne

Completati: audit del codice/piano/replay, specifica comune, profilo senza
calendari, kernel e adattatore nativo senza ereditarietà/caricamento dei vecchi
controller e piani. **67 test passati**: 34 profilo, 22 kernel, 11 contratto
motore/regressioni. Implementate generazione di opportunità dallo stato e prime
prove sul motore originale, non la totalità del modello normativo sopra.

Undici partite diagnostiche, conservati tutti i risultati. Il prototipo V5 su
quattro casi ha zero morti/fughe ma resta a 6-5-0, cassa media -12,95% rispetto
alla E18.31 matched e due missioni terminali incomplete. **Nessuna candidata
eleggibile, nessuna submission.** Il target configurato 770 non è stato raggiunto.
Dettagli e provenienza nel
[checkpoint nativo](reports/E18_33_NATIVE_POLICY_CHECKPOINT_20260906_IT.md).

**Da implementare e verificare:** valutazione cronologica completa del portafoglio
nei due scenari, costo residuo delle sostituzioni, certificato congiunto di
finanziamento/rotte/capacità che includa la crescita, chiusura delle missioni,
trasferimento completo, gate economico preregistrato e standalone. Le stime
locali dell'adattatore non sono equivalenti alla policy definita nelle sezioni
precedenti. Nessun risultato V9 è presentato come risultato E18.33.

E19 resta una verifica successiva del medesimo codice su 770/772/662:
[roadmap parametrica](../e19/MODEL_SPEC_CODEX_E19_PARAMETRIC_VALIDATION_DRAFT.md).
Non cambiare topologia durante il consolidamento E18 e non incorporare curve
dei benchmark nella funzione obiettivo o nei parametri operativi.
