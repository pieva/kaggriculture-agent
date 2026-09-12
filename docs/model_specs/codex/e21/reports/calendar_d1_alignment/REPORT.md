# Calendario comune da D1: verifica 772 e774

Analisi dei20 replay pubblici già acquisiti per ciascuna versione, confrontati con il calendario comune dei nove esterni; rappresentante107083439. Coorti diverse: le differenze non misurano un effetto causale. Nessuna nuova pubblicazione.

## 772:20 replay

Primo giorno con semine diverse dal calendario comune: {11: 19, 8: 1}. Si confrontano le semine effettive, non solo le piante ancora presenti.

| Giorno | Semine identiche | Fragole seminate nostre/comune | Grano seminato nostro/comune | Meloni seminati nostri/comune | Persone nostre/comune |
|---|---:|---:|---:|---:|---:|
| D1 | 20/20 | 0.00/0 | 7.00/7 | 12.00/12 | 6.00/6 |
| D2 | 20/20 | 0.00/0 | 0.00/0 | 0.00/0 | 5.00/4 |
| D3 | 20/20 | 0.00/0 | 3.00/3 | 0.00/0 | 5.00/5 |
| D4 | 20/20 | 0.00/0 | 4.00/4 | 0.00/0 | 6.00/6 |
| D5 | 20/20 | 0.00/0 | 3.00/3 | 0.00/0 | 5.00/5 |
| D6 | 20/20 | 4.00/4 | 0.00/0 | 0.00/0 | 6.00/5 |
| D7 | 20/20 | 8.00/8 | 5.00/5 | 0.00/0 | 9.00/8 |
| D8 | 19/20 | 3.95/4 | 4.00/4 | 0.00/0 | 9.00/8 |
| D9 | 20/20 | 4.00/4 | 1.00/1 | 0.00/0 | 11.00/9 |
| D10 | 20/20 | 0.00/0 | 4.00/4 | 0.00/0 | 12.00/9 |
| D11 | 0/20 | 1.00/0 | 8.00/7 | 0.00/0 | 12.00/12 |
| D12 | 0/20 | 9.55/13 | 3.50/11 | 0.00/0 | 13.00/11 |
## 774:20 replay

Primo giorno con semine diverse dal calendario comune: {4: 4, 11: 16}. Si confrontano le semine effettive, non solo le piante ancora presenti.

| Giorno | Semine identiche | Fragole seminate nostre/comune | Grano seminato nostro/comune | Meloni seminati nostri/comune | Persone nostre/comune |
|---|---:|---:|---:|---:|---:|
| D1 | 20/20 | 0.00/0 | 7.00/7 | 12.00/12 | 6.00/6 |
| D2 | 20/20 | 0.00/0 | 0.00/0 | 0.00/0 | 5.00/4 |
| D3 | 20/20 | 0.00/0 | 3.00/3 | 0.00/0 | 5.00/5 |
| D4 | 16/20 | 0.00/0 | 3.80/4 | 0.00/0 | 6.00/6 |
| D5 | 20/20 | 0.00/0 | 3.00/3 | 0.00/0 | 5.00/5 |
| D6 | 16/20 | 3.80/4 | 0.00/0 | 0.00/0 | 6.00/5 |
| D7 | 20/20 | 8.00/8 | 5.00/5 | 0.00/0 | 9.00/8 |
| D8 | 20/20 | 4.00/4 | 4.00/4 | 0.00/0 | 9.00/8 |
| D9 | 20/20 | 4.00/4 | 1.00/1 | 0.00/0 | 11.00/9 |
| D10 | 20/20 | 0.00/0 | 4.00/4 | 0.00/0 | 12.00/9 |
| D11 | 0/20 | 1.00/0 | 8.00/7 | 0.00/0 | 12.00/12 |
| D12 | 0/20 | 1.00/13 | 12.00/11 | 8.00/0 | 13.00/11 |

## Conseguenza per l’allineamento

**Il piano deve partire da D1 per entrambe le versioni.** L'apertura non è più un prefisso intoccabile fino a D11: occorre pianificare semina, acqua, raccolta, trasporto, organico e liberazione delle caselle prima del picco D12. Le semine D1 corrette possono restare uguali; non è necessario cambiarle per dichiarare il piano attivo dall'inizio.

La772 coincide nelle semine per tutti i primi10 giorni in20/20 replay; nella774 alcuni ritardi compaiono già aD6. A D11 entrambe seminano8 grani e1 fragola contro7 grani e0 fragole del comune. A D12 tutti i20 replay774 seminano8 meloni/12grani/1fragola; il comune0meloni/11grani/13fragole. Quindi la774 contiene anche una scelta colturale divergente, non solo un'espansione tardiva.

## Compatibilità della774

LaRepair2 conserva18 pascoli, uno vuoto, più1pollaio:19 strutture,18 animali e56 altre caselle nei tre quadranti. Il comune arriva a58 colture quando resta con17 strutture animali. Il suo picco colturale non può essere copiato integralmente sulla774. Il target D12 di33fragole+21grani entra nelle56caselle; il picco successivo richiede ridurre la quota di grano o cambiare struttura. L'utente ha scelto di mantenere774: il calendario va adattato alla capacità, mantenendo8C/9S/1G e il pascolo vuoto. La772 con16pascoli ha59caselle disponibili.

## Stato delle prove

La variante772 con passaggio aD12 è stata fermata su indicazione dell'utente dopo un solo confronto completo (66774 contro80178). Non è una suite conclusa.

Il primo prototipo772 con piano daD1 ha realizzato12meloni+7grani aD1 ma è fallito sul mantenimento animale e sui checkpoint successivi. Correzione tecnica C2: non chiedere HARVEST prima dell'età minima della coltura, anche se yield_units è già positivo. Risultati e22KPI nei report dedicati. Un prototipo che non realizza la topologia e il calendario non valuta il loro rendimento. Non trasferire automaticamente un controller tecnicamente invalido alla774.

[Prototipo772 D1](../calendar772_d1/REPORT.html) · [Correzione tecnica772 D1 C2](../calendar772_d1_c2/REPORT.html).

Esito772 D1 C2:719 chiamate, zeroerrori core, geometria772 e10C/6S recuperate, zero perdite crop e fughe. Il calendario resta fuori tempo:2fragole aD6,11 aD9,31 aD12 (obiettivi4/20/33). Cassa30295 contro80178; suite fermata al primo caso secondo protocollo. La correzione tecnica risolve le raccolte premature, non la capacità di eseguire il piano. La774 ha ora il medesimo requisito di pianificazione daD1 documentato, ma non una variante D1 implementata o validata.
