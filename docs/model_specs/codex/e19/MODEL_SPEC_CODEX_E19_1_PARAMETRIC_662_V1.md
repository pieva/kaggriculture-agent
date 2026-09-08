# E19.1 — prima configurazione parametrica 662

Avvio autorizzato dal proprietario il 2026-09-07: «Sviluppa la E19 allora».
La richiesta supera il prerequisito di completamento/pubblicazione E18.
E18.33 V24 resta un controllo interno non promosso, non una release finale.
È confermata la precedente autorizzazione a pubblicare E19 quando soddisfacente.

## Trattamento iniziale

Profilo `configs/CODEX_E19_1_662_V1.json`: unica differenza rispetto al profilo
E18 V2_BOOTSTRAP è K=6 invece di 7. Target globale 14, pesi COW:SHEEP 9:5,
tre quadranti, massimo 12 manovali; avvio 2 COW/2 SHEEP, WHEAT/CARROT fino
al primo raccolto osservato. Nessun calendario o programma per quadrante.
La capacità per ordine di acquisto è min(K, max(0, P-K*rango)): 6/6/2.

Il bundle V1 contiene esattamente lo stesso kernel/controller di E18 V24;
gli hash del core devono coincidere nei manifest. Il builder comune produce
file autosufficienti: nessuna importazione dei piani storici a runtime.

## Protocollo e decisione

Screening sul seed 180903001, entrambi i seat e due avversari E18.16/E18.2.
Poi sette seed development 180903001–180903007, entrambi i seat/due avversari,
28 casi completi. Conservare tutti gli esiti. Confronto matched con E18 V24
770 congelata; aggiungere E18.31 come controllo economico storico. Non
attribuire causalmente tutti i delta alla geometria: i percorsi possono
alterare i successivi consumi casuali del motore e quindi prezzi/negozi.

Misure: 662 effettivamente popolata, cap animali/manovali, zero perdite
biologiche, contabilità, errori e missioni terminali, cassa finale/minima,
COW/SHEEP/colture giornaliere, FEED/CARE/WATER, raccolti, PASS/MOVE e runtime.
Il runner conserva le missioni residue per distinguere errori reali da
semplici differenze dei contatori. Parità source/bundle/file-loader prima
della pubblicazione. Nessun benchmark esterno nuovo consumato in sviluppo.

Una candidata soddisfacente deve almeno superare sicurezza e chiusura,
raggiungere la topologia richiesta e non presentare una regressione economica
materiale non spiegata rispetto al controllo 770. Il superamento della parità
o dei soli test di configurazione non costituisce approvazione del rilascio.
La prima pubblicazione avrà il ruolo di baseline E19 per benchmark esterni,
senza dichiarazione anticipata di superiorità sui Top.

## Revisione V2 del core comune

V1 resta il controllo puro del cambio K. V2 mantiene lo stesso profilo e
corregge la prenotazione delle quantità PICKUP pendenti, incluso il surplus
di grano trasportato. È costruito anche `submission_codex_e19_control_770_v2.py`
con core identico e K=7 per il confronto matched. Questo file è un controllo
di sviluppo, non la dichiarazione di una nuova release finale E18.

Per benchmark successivi fissare SHA256 di bundle, manifest, configurazione
del motore, seed e seat. Confrontare entrambe le posizioni e conservare tutte
le partite, incluse anomalie e timeout. Separare vittorie/cassa da KPI di
costruzione e servizio. Non ottimizzare sul campione esterno mentre lo si
usa come prova di generalizzazione. La valutazione esterna resta successiva
alla prima pubblicazione E19.
