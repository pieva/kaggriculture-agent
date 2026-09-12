# Audit della 774 prima della pubblicazione

Data: 12 settembre 2026. Oggetto: `artifacts/fixed774_reconstruction.py`, SHA256 `6b8d6fe182da707b309570c6e02ca0df29ca8673969ac6fc9fdcb2853e4f0346`.

**Esito: nessun errore bloccante di esecuzione rilevato nel replay disponibile. La build è utilizzabile come confronto della ricostruzione topologica, ma presenta incoerenze evidenti negli acquisti, nel coordinamento e nell'identificazione. Non rappresenta ancora un esperimento con un animale in meno.** Nessuna pubblicazione eseguita; file congelato invariato.

## 1. Il numero di animali non diminuisce

Il limite impostato è 19 risorse bovini/ovini, contro 18 pascoli della 774; l'oca è separata da questo limite. Nella partita entrambe le politiche comprano 8 mucche, 11 pecore e 1 oca. Entrambe terminano con 8 mucche, 10 pecore e 1 oca collocate, più una pecora nel deposito. Non si osservano fughe.

La 774 elimina il pascolo `(4,7)` ma riempie quello precedentemente vuoto `(6,3)` in Q1, osservato a D13 H6. La 775 mantiene un pascolo vuoto. Pertanto la riduzione del carico animale attesa non avviene. La pecora residua costa 500 ed è uno spreco condiviso anche dalla 775; non è una perdita aggiuntiva esclusiva della 774.

Prima di presentarla come variante biologica alleggerita servono un obiettivo esplicito sul numero di animali e acquisti/collocamenti coerenti. Abbassare soltanto il cap a 18 eliminerebbe la riserva eccedente, ma consentirebbe comunque 18 bovini/ovini collocati più l'oca: da solo non garantisce un animale attivo in meno rispetto a questa 775.

Riferimenti: bundle riga 11610; `src/agricola/strategy/codex/codex_e17_topology_cap_662.py`, `_filter_market`; replay e ledger della partita `Fixed774_E18_180911301`.

## 2. Il piano continua a trattare il target come un pascolo

Il filtro modifica 45 comandi sulla casella `(4,7)`: 19 PASS, 13 WATER, 8 PLANT, 4 HARVEST e 1 DIG. Sono conteggi di sostituzioni, non un bilancio completo di tutte le azioni eseguite sulla casella.

Esempi verificati: D12 H17 PLACE SHEEP diventa WATER; D12 H18 FEED e H19 CARE diventano PASS. La routine animale continua fino a D28. Le visite recuperate per il grano hanno utilità, ma le 19 sostituzioni in PASS dimostrano che la rimozione del pascolo non libera automaticamente il lavoro. Non si attribuisce un costo monetario senza un controfattuale.

La sostituzione D21 H8 HARVEST → WATER **non è un errore evidente**: il grano è stato seminato a D20, ha solo un giorno e il motore richiede due giorni per raccoglierlo.

Riferimento: `AUDIT.json`, `filter_changes`; funzione `_filter_unit_actions` del controller ereditato.

## 3. Metadati errati da correggere prima del packaging

Il bundle dichiara `MODEL_VERSION='CODEX-E20-774-Fixed774'` e `BUILD_METADATA.topology='7-7-2'`, pur eseguendo 774. La sostituzione testuale del generatore cambia `772` ma non `7-7-2`; la successiva sostituzione dell'identità non trova più la stringa dopo il cambio E20V39 → Fixed774.

La telemetria conserva inoltre l'identità E18 e `topology_reclaim_enabled=false`: il reclaim è forzato dall'overlay, quindi quel flag non descrive da solo la topologia effettiva. Sono errori di tracciabilità, non cause dimostrate del risultato economico. Correggerli in una copia di rilascio identificata come ricostruzione moderna, conservando questo originale e il suo hash.

Riferimenti: bundle righe 11629–11631; `reconstruct_fixed_774.py`; `AUDIT.json`.

## 4. Finale: rischio nel codice, non incidente osservato

L'overlay chiama il controller di cap anche da D29, bypassando il passthrough terminale E18. `_filter_unit_actions` può sostituire un comando non di movimento sul target quando esiste un task agricolo, senza proteggere esplicitamente la consegna. Nel replay **zero sostituzioni del filtro a D29–D30**, nessun prodotto vendibile residuo nel deposito o negli inventari finali. Non classificare questo rischio come una vendita effettivamente persa nella partita verificata.

## Verifiche eseguite

- Caricamento autonomo del bundle tramite `exec`, senza `__file__`.
- Invocazione dell'ingresso pubblico `agent` su tutte le 719 osservazioni salvate: zero differenze rispetto alle azioni del replay prodotto con `create_agent`.
- Reset a inizio episodio: nuova istanza e azione iniziale corretta.
- Tutti i 720 stati rispettano il massimo 7/7/4/0; finale 774 confermato.
- Zero errori tecnici/fallback riportati dalla telemetria del controller. Massimo locale della riproduzione circa 22 ms; non è una misura dell'ambiente Kaggle.
- Partita salvata: 72.473 contro 75.765 della E18 nello stesso match, differenza −3.292. Un solo seed/ruolo non stima il rendimento competitivo.

Audit riproducibile con `audit_fixed774.py`; risultati dettagliati in `AUDIT.json`. Nessuna nuova simulazione o seed consumato. Non sono stati verificati qui il ruolo 1 del candidato, il caricamento remoto Kaggle o una distribuzione di avversari. La vecchia 774 storica non è stata recuperata: questa rimane la ricostruzione moderna già documentata.

## Indicazione operativa

Per pubblicare una baseline diagnostica: correggere l'identificazione in una copia di rilascio e mantenere espliciti i limiti sopra. Per pubblicare la variante che riduce davvero gli animali e il loro lavoro: prima intervenire su acquisti, collocamenti e routine di servizio, poi confrontare la nuova versione separatamente. Mescolare queste correzioni nel bundle congelato renderebbe il report corrente riferito a un codice diverso.
