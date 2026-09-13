# D11 e ripetibilità di s56165462

## Scontro diretto già analizzato: 108480607, submission 56166543

Il delta di cassa non è costante dopo D11: DB−E20 = −669 a D10, +6.132 a D11, +4.710 a D12, +6.733 a D19, +9.067 a D29 e +10.946 a D30. Se si osserva una serie cumulativa dei meloni, questa resta invece piatta dopo le ultime vendite a D12.

Entrambi raccolgono 72 meloni a D11. Gli ordini SELL MELON sono identici ai passi 250, 251, 252, 253, 254, 256: quantità richieste 6, 24, 12, 6, 6, 6. Il motore vende soltanto dal deposito; il prodotto ancora trasportato non è vendibile tramite questi ordini.

E20.9 vende effettivamente 30 meloni per 7.155 monete a D11, poi 36 per 4.921 a D12. s56165462 vende 60 per 13.943, poi 12 per 2.023. Ricavi totali: 12.076 contro 15.966, differenza 3.890. La differenza di cassa giornaliera include anche gli altri prodotti e i costi.

La divergenza operativa è nella consegna. Al passo 252, per esempio, un nostro lavoratore resta con 6 meloni a (4,4) e riceve PICKUP WHEAT; altri portatori si trovano lontano dal deposito. Non basta raggiungere l'area del deposito: occorre scaricare. Al passo 263 E20.9 ha ancora 42 meloni negli inventari e nessuno nel deposito. Al passo 264, senza ordine di vendita, ne ha 36 nel deposito e nessuno negli inventari; il deposito è pieno a 100. Il motore `_drop_inventories_to_shed` scarta l'eccedenza. s56165462 passa invece da 12 trasportati a 12 in deposito, senza perdita di meloni. Questo identifica la perdita delle sei unità, prima rimasta aperta nel report KPI.

Interpretazione: consegne mancate o tardive impediscono di eseguire il piano di vendita, spostano la monetizzazione a prezzi inferiori e provocano overflow. Non è una diversa scelta esplicita del prezzo di vendita. Occorre ancora identificare l'origine nel pianificatore E20.9 della sequenza di consegne mancate, prima di proporre una correzione.

## Submission indicata dall'utente: 56165462

È diversa da 56166543. Metadati acquisiti dall'API pubblica: 289 replay pubblici completi contro altri team. Campione congelato: episodio 108518933 più i 19 più recenti diversi da esso, senza filtro sul risultato. Non sono stati verificati tutti i 289 replay.

- **20/20** con i medesimi 719/719 gruppi di comandi dei lavoratori, rispetto a 108518933.
- **20/20** con i medesimi 719/719 gruppi di ordini di mercato.
- **20/20** con identiche strutture e coordinate animali nei 30 snapshot giornalieri.
- **20/20** con identiche specie e coordinate degli animali nei 30 snapshot.
- **19/20** con identiche colture/coordinate/date di semina nei 30 snapshot; episodio 108502716 coincide soltanto in 13/30 snapshot colturali, pur mantenendo tutti i comandi identici.
- Cassa finale nel campione: 61.522–126.645. Piano emesso uguale non implica stesso risultato o stessa esecuzione.

Il riferimento è incluso nei conteggi: sono 19 confronti indipendenti dal confronto del riferimento con sé stesso, non 20 repliche aggiuntive. Non implica indipendenza statistica fra partite né dimostra assenza di rami mai attivati.

Fonti riproducibili: [protocollo](CONSISTENCY_PROTOCOL.json), [risultati e hash](CONSISTENCY_56165462.json), [metadati](history_56165462.json). I tre replay precedenti della submission 56166543 mostravano invece comandi dei lavoratori quasi identici (99,4–99,6%), non esattamente identici: non aggregare i due risultati.
