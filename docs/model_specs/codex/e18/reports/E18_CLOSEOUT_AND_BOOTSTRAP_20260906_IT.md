# E18 — chiusura della sessione e prova di autonomia

2026-09-06. **La nuova E18 parametrica non è conclusa e non è un benchmark E19.**
Il proprietario ha autorizzato, in caso di mancato superamento dei gate entro
l'ora disponibile, la pubblicazione della E18.32 V9 come controllo provvisorio.
Quel bundle è immutabile e conserva il calendario storico: non dichiararlo
conforme alla policy unica E18.33. Stato dell'upload nel receipt separato.

## Prove della policy comune

V6 introduce una verifica dei percorsi giornalieri che riserva lavoro anche
alla crescita, senza simulare manovali non osservati. Sul caso seed 180903001,
seat 0 contro E18.16: 770 raggiunta in D11, zero perdite, cassa 62.283, PASS
1.309. Il certificato corrente è soltanto giornaliero, non il portafoglio futuro.

Su successiva indicazione del proprietario è stata resa esplicita una piccola
configurazione di avvio. V7: tetto iniziale due mucche e due pecore, colture
WHEAT/CARROT fino al primo raccolto confermato. Profilo
`CODEX_E18_33_COMMON_RESOURCE_POLICY_V2_BOOTSTRAP.json`; nessuna data, coordinata
o riavvio del programma all'acquisto di Q1. Gli animali iniziali sono un tetto,
non acquisti da forzare senza fondi o capacità.

Sul medesimo caso V7: uscita dall'avvio a **D4 H9**, cassa 87.160 contro 85.073
di E18.31 matched (+2,45%), zero perdite/incomplete. Tuttavia 770 soltanto in
D14, 1.337 PASS e nove tile colturali terminali: singolo smoke positivo per
cassa, non soluzione dei KPI macro e non prova di autonomia robusta.

V8 ha provato valore esplicito dei servizi e approvvigionamento del grano non
accessibile al lavoratore incaricato: 69.866, 1.478 PASS, zero perdite nel caso
provato. Intervento composto e peggiorativo; conservato, non selezionato.
I relativi test verificano il sorgente V8 archiviato, non alterano il controllo.

## Estensione dell'avvio per misurare l'autonomia

Su richiesta del proprietario, V9 estende il profilo V7 con una sola diversa
condizione di rilascio: tutte le tile del primo ciclo iniziale raccolte e
rinnovate almeno una volta, dotazione iniziale completata, cassa sufficiente
alla stima della prossima manutenzione, ultima giornata completa con saldo
di cassa non negativo. Profilo
`CODEX_E18_33_COMMON_RESOURCE_POLICY_V3_AUTONOMY.json` (formato schema v2).
Nessuna scadenza imposta; dopo il rilascio l'avvio non si riattiva.

È una **sonda diagnostica**, non una prova che la policy sia davvero autonoma.
Il rinnovo riguarda l'intero primo gruppo di tile, non un singolo raccolto.
Le successive altre tile rinnovate sono contate separatamente: il contatore
totale può superare le 21 iniziali. L'acquisto di nuovi terreni non ricrea
il gruppo iniziale né cambia il programma per quadrante.

Quattro partite complete: seed 180903001, due seat, E18.16 ed E18.2/V4D.
Tutti i risultati, inclusi i fallimenti, sono in
`artifacts/derived/E18_CLOSEOUT_GATE_E18_33_V9_AUTONOMY_20260906.json`.
Il criterio di rilascio non è stato adattato dopo aver visto i risultati.

| Avversario | Seat | Rilascio avvio | Cassa finale | Strutture pascolo finali | PASS |
|---|---:|---|---:|---|---:|
| E18.16 | 0 | D16 H14 | 22.615 | 6-4-0 | 1.680 |
| E18.16 | 1 | D16 H14 | 44.568 | 4-3-0 | 1.488 |
| E18.2/V4D | 0 | D17 H1 | 47.446 | 5-2-0 | 1.532 |
| E18.2/V4D | 1 | D17 H1 | 46.280 | 4-3-0 | 1.445 |

Cassa media 40.227,25 contro 82.560 di E18.31 sugli stessi quattro casi:
-51,28%. Le strutture non attestano animali vivi: nel primo caso si osservano
36 perdite colturali e dieci fughe, con dieci missioni incomplete; nell'ultimo
una perdita colturale. La prima riga ha chiamata massima 60,002 s, le altre
5,376/6,766/5,943 s: budget di calcolo da diagnosticare prima di attribuire
la regressione integralmente alle decisioni economiche.

**Esito: estensione non eleggibile.** Nessun caso raggiunge la 770. Nei due
casi contro E18.16 il rilascio avviene soltanto a D16 H14, pur con cassa già
ampiamente disponibile: aspettare il rinnovo dell'ultima tile prolunga troppo
il vincolo iniziale e ritarda gli investimenti animali. Dopo il rilascio restano
insufficienze di assegnazione e capacità. Un criterio guidato dallo stato può
comunque imporre di fatto una restrizione a medio termine: questa variante
non va adottata come policy di produzione.

La misura corretta è quindi «tempo di rilascio dell'avvio assistito», non
«giorno di autonomia raggiunta». Vanno valutati anche servizio, rinnovi,
redditività e crescita dopo quel punto. Sono emersi inoltre tempi di chiamata
superiori al secondo previsto dal motore, fino a circa 60 s in un caso:
necessario un gate sul budget di esecuzione e sulla riserva di tempo, non basta
`errors == 0`. Non attribuire tutte le perdite al solo piano agricolo senza
distinguere la componente di budget computazionale.

## Verifica diretta Q0 della versione provvisoria E18.32 V9

Nuova simulazione sul motore originale, seed 180903001 seat 0 contro E18.16.
Cassa 85.199, PASS 752, MOVE 3.393, zero morti/fughe/missioni incomplete.
Serie per quadrante in `E18_CLOSEOUT_GATE_E18_32_V9_Q0_20260906.json`.

| Giorni / checkpoint | Pascoli Q0 | Colture Q0 | Tile libere Q0 |
|---|---:|---:|---:|
| D1–D3 | 4 | 19 | 2 |
| D4 | 5 | 19 | 1 |
| D5–D10 | 6 | 19 | 0 |
| D11–D13 | 6 | 7 | 12 |
| D14 | 7 | 12 | 6 |
| D15–D28 | 7 | 18 | 0 |
| D29 | 7 | 6 | 12 |
| D30 | 7 | 0 | 18 |

Checkpoint H24 prima dell'ultimo batch D1–D29, terminale D30. **Q0 non è
bonificato:** restano attivazione ritardata del settimo pascolo e vuoto fra
raccolto e risemina; il calo finale non è prova di optimalità economica.
Questa evidenza è coerente con il ruolo di controllo provvisorio, non con
l'accettazione come benchmark parametrico E19.

## Confronto esterno e verifica della pubblicazione

Formato desktop V4.1: Top770-002 già consumato contro una sola versione sotto
esame, E18.32 V9. Ventidue pannelli, WATER/FEED/CARE separati, tile coltivate
e totali nello stesso pannello. Quattordici simulazioni interne contro E18.16
vs quattro replay esterni exact770; regimi e seed diversi, confronto descrittivo.
Mediane/min–max osservati non sono intervalli di confidenza. Non è stata
dimostrata equivalenza statistica o assenza di scostamenti significativi.
Dataset: `E18_32_CLOSEOUT_TOP002_KPI_V4_1_20260906.json`.

Scostamenti descrittivi rilevanti: somma delle mediane giornaliere PASS
D5–D10 237 contro 117; D10 PASS 62 contro 25, nove COW contro 8,5, 37 tile
colturali per entrambi. D30 cassa mediana 79.682,5 contro 97.348,5 (-18,15%).
Non si tratta di coppie matched; non trasformare queste differenze in una
stima causale del valore delle singole policy.

Il report riusa il renderer standard già verificato nelle sessioni precedenti.
Il controllo visivo live di questa rigenerazione è stato bloccato dalla policy
del browser sull'apertura di file locali; non dichiararlo ripetuto con successo.

Il bundle provvisorio è `submission/submission_codex_e18_32_770_v9.py`,
SHA-256 `4d2d32ac41b38af5f4f632ef9e8dd9af2ebd37f7e7bcb1795c2c31cda4e92789`.
Manifest e parità preesistenti verificati; 2.876 batch identici source/bundle
e file-loader su quattro casi, massimo misurato 0,819 s. Gate completo V9
congelato: 28 casi safety pass, cassa +0,230% rispetto a E18.31 matched.
In questa sessione 97 test mirati E18.32/E18.33 passati prima della pubblicazione.
Ripetizione finale: 97/97, schema bootstrap V2/V3 incluso; ulteriori 64/64
regressioni E18.30/E18.31 passate. Totale dei due gruppi: 161 test.
Sorgenti V9 controller/kernel archiviati e kernel V7/V8 ricostruito con hash
identico a quello della prova congelata. Nessun risultato respinto eliminato.
Nessun nuovo Top consumato, nessuna partita E19 avviata.

**Upload confermato:** submission 56056189, Complete, 2026-09-06 13:27:24 UTC;
score iniziale osservato 600,0 non interpretabile come verifica economica.
Ricevuta: `E18_32_KAGGLE_UPLOAD_RECEIPT_V9_20260906.json`. Un solo invio;
manifest di build storico preservato e superato dal receipt soltanto per lo
stato esterno. Non duplicare la submission.

## Ripartenza

Non prolungare ancora un blocco globale dell'avvio per mascherare la policy
incompleta. Separare gli impegni iniziali già ammessi dalla libertà di valutare
i nuovi investimenti. Servono valutazione residua del portafoglio, finanziamento
e capacità futuri, continuità dei rinnovi e budget computazionale verificato.
Il confronto E19 rimane subordinato a una E18 comune davvero eleggibile.
