# E20.1 — percorsi e CARE con beneficio produttivo

La candidata locale è **E20v28**, congelata in `submission/submission_codex_e20_772_e20v28_candidate.py`. Il suo stato di promozione dipende dai gate di sviluppo e conferma: il solo congelamento non certifica un miglioramento fuori campione. La precedente E20v18 resta disponibile senza modifiche.

## Esito definitivo

**E20.1 non è promossa.** La conferma indipendente contro l'avversario comune E18 chiude a 55.001,86 contro 58.398,86 di E19 (−5,82%), con un solo seed positivo su sette. Lo stress si riduce a 3,79 contro 4,71 transizioni per partita e non ci sono perdite animali. Nel torneo di 42 partite E18 vince 20/28 incontri, E19 13/28 ed E20.1 9/28.

La scomposizione appaiata riconcilia il deficit di 3.397: vendite −1.991,64, acquisti +1.529,43, assunzioni −124,07, terreno e saldo delle azioni sul campo invariati. Il latte raccolto aumenta ma i suoi incassi diminuiscono; la lana aumenta in entrambe le grandezze. La prossima ipotesi da verificare riguarda il margine di Q2 e la monetizzazione, mantenendo separati sviluppo e nuovi seed di conferma.

Il controllo 770 completato e verificato sugli stessi dieci seed di sviluppo, in posizione 0, chiude a 68.041,80 contro 77.660,50 della 772: la differenza è positiva in nove casi su dieci. Questo screen non sostituisce la conferma indipendente e non dimostra che il solo pianificatore migliori E19.

[Report finale](reports/e20_1/REPORT.html) · [Torneo e 22 KPI](reports/e20_1_confirmation/REPORT.html).

## Contratto conservato

- Apertura assistita E19 identica fino a D11 incluso.
- Target 7–7–2; Q2 riservato alla mucca in (4,5) e alla pecora in (4,6), da D12.
- Mix target 10 mucche / 6 pecore, massimo 12 braccianti, intenzioni colturali originali e stessa gestione terminale.
- Decisioni basate sullo stato osservato; nessun riconoscimento del seed o accesso a prezzi futuri.

## Due interventi

**Inserimento dei tile lontani a parità di urgenza.** Il pianificatore V48 ordinava le proposte per priorità e coordinate. E20.1 conserva la priorità e usa, come secondo criterio, la distanza dal lavoratore attuale più vicino, in ordine decrescente; le coordinate restano lo spareggio deterministico. Cambia l'ordine di inserimento sia nei percorsi sia nei certificati che utilizzano la medesima funzione. Costi di viaggio, approvvigionamento, budget residui e ordine delle visite protette restano verificati. Non riserva lavoratori futuri.

**Filtro dei CARE con incremento produttivo impossibile.** Prima di proporre CARE, verifica che esista una produzione da dopodomani fino al termine e che il bonus non saturi già la capacità disponibile oltre l'unità di produzione base. Tiene conto della produzione della notte successiva: il vecchio bonus viene consumato prima di immagazzinare quello del CARE odierno. Non elimina i CARE in blocco e non assume prezzi futuri. È un filtro di beneficio nullo, non una stima completa del costo opportunità del lavoro.

## Diagnosi e ablation

Il replay diagnostico della E20v18 sul seed 180910101 riproduce 719 azioni senza alterazioni. Le dieci transizioni crop→weed dopo stress sono sul bordo orientale di Q1. Esistono ripetuti scarti di proposte WATER raggiungibili nel tempo disponibile; il dato, da solo, non dimostra che tutti gli altri impegni potessero essere completati simultaneamente.

Sono conservate cinque varianti nuove, ciascuna provata inizialmente su tutti i dieci seed conosciuti:

| Variante | Intervento isolato |
|---|---|
| E20v24 | Estensione a D12 della protezione e dell'accesso fuori coda per colture stressate ancora produttive |
| E20v25 | Solo accesso fuori coda, con priorità originali |
| E20v26 | Inserimento dei tile lontani per primi, a parità di urgenza |
| E20v27 | Solo filtro CARE senza incremento produttivo possibile |
| E20v28 | Combinazione dei percorsi E20v26 e del filtro E20v27 |

Le prime due varianti azzerano lo stress nel primo screen ma peggiorano la cassa: interventi urgenti fuori dalle code alterano il rinnovo delle colture e la distribuzione del lavoro. La terza riduce molto lo stress; la quarta migliora la cassa ma non raggiunge da sola il requisito di stress rispetto a E19. La combinazione viene quindi verificata con scambio dei ruoli. Lo [screen completo](reports/e20_1/screen/REPORT.md) conserva anche le prove scartate.

## Validazione e controllo della topologia

Il [protocollo](E20_1_PROTOCOL.json) separa i dieci seed ormai esposti dai sette nuovi seed 180910201–180910207. I ruoli sono appaiati, non considerati seed indipendenti. Il gate richiede cassa media almeno E19, mediana positiva delle differenze per seed, miglioramento nella maggioranza dei seed, stress non superiore a E19 e zero perdite animali. La coda inferiore dei risultati resta riportata separatamente.

Il controllo **C770** utilizza il medesimo file E20.1 congelato, senza riserve o animali Q2, con target 14 e mix 9 mucche / 5 pecore. Non è una nuova candidata ufficiale E19. Il confronto sui seed già noti serve a distinguere il contributo del pianificatore da quello della topologia.

La parità standalone confronta tutte le 719 azioni su due seed e due ruoli. Il lettore dei replay ricostruisce il campo condiviso `step`, serializzato soltanto nel ruolo 0, senza copiare i dati privati dell'avversario. I limiti intragiornalieri della topologia e l'apertura sono verificati su tutta la coorte.

Il gate di sviluppo su 20 partite complete è superato: E20.1 76.866,3 contro E19 72.406,3 (+6,16%), otto seed positivi su dieci, mediana delle differenze per seed +3.109,5, stress 2,30 contro 3,55 e zero perdite animali. Il minimo individuale resta inferiore a E19 (42.295 contro 44.679): questo limite non viene nascosto dalla media.

### Completezza e tempi di esecuzione

Sul portatile a quattro core, la sovrapposizione di simulazioni e verifiche ha esaurito il budget extra di alcuni agenti. Il solo stato finale DONE dell'ambiente non garantisce 719 chiamate: l'audit controlla esplicitamente anche questo conteggio. Cinque casi incompleti del primo lotto di conferma e due del controllo C770 sono conservati nelle sottocartelle `invalid_under_load`. Non sono prove economiche valide. Il lotto viene completato con un solo processo e gli stessi limiti di gioco, ripetendo gli stessi casi con gli stessi bundle, senza modificare la candidata. Nel primo caso E19 ripetuto, l'overage scende da 60,87 a 4,75 secondi e le chiamate da 483 a 719. Il protocollo registra l'emendamento operativo e i casi coinvolti.

## Artefatti

- [Screen delle cinque varianti](reports/e20_1/screen/REPORT.html)
- [Sviluppo appaiato](reports/e20_1/development/REPORT.html)
- [Conferma appaiata su seed nuovi](reports/e20_1/confirmation/REPORT.html)
- [Torneo indipendente e 22 KPI](reports/e20_1_confirmation/REPORT.html)
- [Confronto con controllo 770](reports/e20_1/topology_control/REPORT.html)

I report di conferma e controllo vengono prodotti solo dopo il completamento delle rispettive partite. Nessuna nuova submission esterna è implicita in questo esperimento.
