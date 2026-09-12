# E21 — rilettura della vecchia 774 prima dell'implementazione

Aggiornamento successivo: [verifica con replay e ricostruzioni diagnostiche](reports/trajectory_774_772_775/REPORT.html). Il target ospita una pecora in 14/14 replay E18. La ricostruzione persistente riempie un altro pascolo vuoto a D13, recuperando il numero totale di animali; la sola riattivazione del ramo superstite non ammette il reclaim. Le lacune storiche descritte sotto restano valide.

12 settembre 2026. Analisi statica di documenti, codice, artefatti e storia Git locale. Nessuna policy modificata, simulazione, submission, commit o push. Base E18 verificata: SHA256 `c5fb1fc4966b81f238cdd0de4ca5e15b16ea6b8ae077a08ecc881f8729fd01f7`.

## Evidenza recuperata e limiti

Il [report E18.2](../e18/reports/E18_2_CAPACITY_GOVERNED_V4D_DEV_REPORT_IT.md) descrive una 774 interrotta dopo i primi match, con regressioni fino a circa 60k contro V4D. La [spec](../e18/MODEL_SPEC_CODEX_E18_2_CAPACITY_GOVERNED_V4D_V1.md) indica circa 35–60k. Sono estremi riferiti dagli autori, non una media verificata adesso né una suite completa.

Il gate JSON conservato contiene 56 match della candidata finale: i due modi con effetti sulle azioni sono DENSE_V4D e RECOVERY; tutte le 56 occorrenze della candidata terminano in RECOVERY. Non costituisce un archivio dei bracci 774 abortiti.

La storia del sorgente, seguita attraverso i riordini, arriva al checkpoint `9d9172f`: già lì il loader esige reclaim disabilitato e il servizio è limitato al tile corrente. La ricerca per nomi anche nei file ignorati e nella storia Git non ha recuperato un bundle/config eseguibile identificato come la prima 774, né replay originali attribuibili a quel tentativo. I percorsi storici del checkpoint erano sotto `experiments/e18/`. I file storici con 774 nel nome trovati in E19 riguardano invece l'episodio 107152774.

Pertanto specie esclusa, acquisti effettivi, prima divergenza giorno/ora, assegnazioni e rollback della run abortita restano NON VERIFICATI. Riattivare oggi il codice superstite sarebbe una ricostruzione moderna, non una riproduzione certificata della vecchia variante.

## Meccanismo verificabile nel codice superstite

Fonti: [overlay E18](../../../../../src/agricola/strategy/codex/codex_e18_capacity_governed_v4d.py), [filtri ereditati](../../../../../src/agricola/strategy/codex/codex_e17_topology_cap_662.py), [config congelata](../e18/configs/CODEX_E18_2_CAPACITY_GOVERNED_V4D_V1.json).

- Il target è `(x=4,y=7)` in Q2. L'ammissione richiede tile vuoto o bloccato: il ramo intende evitare una futura costruzione, non demolire un pascolo occupato.
- La decisione è giornaliera, da `day >= 6`, con almeno 6 persone, margine sintetico di capacità almeno 2, pressione pubblica avversaria almeno 18 e permanenza minima nel modo. Questi numeri sono indici del codice: `day=6` corrisponde a D7 nel report umano, non D6.
- Il margine è persone meno una funzione di infestanti, sete, fame e raccolti pronti. Non è un calendario del lavoro residuo né una prenotazione di risorse e scadenze.
- L'envelope passa da 19 a 18 target; il cap aggregato COW/SHEEP diventa 18 prima dello sblocco di tre quadranti e 19 dopo. Conta animali su tile, nel deposito e trasportati; esclude l'oca. Non è un cap rigoroso di 18 animali e non identifica quale specie eliminare. Riduce soltanto gli acquisti futuri, nell'ordine proposto dal provider.
- I filtri bloccano BUILD_PASTURE e PLACE fuori dai target e servizi animali sulla casella recuperata. Sulla casella un task agricolo può sostituire un comando non-MOVE; i movimenti della routine restano. Non c'è qui una revisione completa dei pickup, del mangime e degli impegni del provider.
- Coltura prevista WHEAT; backfill una tantum di un seme, costo stimato 15 e cassa minima 3000. Compiti locali HARVEST, DIG, WATER, PLANT vengono scelti sullo stato corrente. L'overlay non prenota l'intero ciclo irrigazione–raccolta–consegna–vendita prima della semina.
- Se il batch introduce PASS rispetto al provider, annulla il reclaim, ripristina i target densi e restituisce l'azione originale. Il rollback riguarda l'envelope e il batch corrente: non riavvolge eventuali interventi precedenti.
- Da `day >= 28` (D29 umano) passa direttamente al provider, saltando anche i filtri. Il ramo superstite non garantisce dunque una 774 persistente al terminale.

Questi meccanismi spiegano perché il solo cambio di cap non costituisca una nuova pianificazione. Non dimostrano quale meccanismo abbia causato le perdite storiche, in assenza delle traiettorie originali.

## Distinzione decisiva: pascoli e animali

La [diagnosi recente](../e20/reports/livestock_routine_20260912/REPORT.md) conta in E18 19 animali, ma sono 8 mucche, 10 pecore e un'oca. I 19 pascoli non equivalgono a 19 bovini/ovini collocati. La riduzione 775→774 può eliminare un posto vuoto oppure un animale: occorre stabilire occupazione e utilizzo nel tempo di `(4,7)` prima di definire il trattamento. Non è ancora accertato qui che quella casella ospiti l'animale marginale.

La 775 deriva dalla routine keiz distillata in V9 e dalle revisioni logistiche E17 V4D/E18: l'evidenza riguarda geometria e controller insieme. V4D protegge il mangime fino al FEED completato e coordina deposito/vendita; alterare il numero di slot può interferire con questi impegni.

## Confronto da concretizzare per E21

| Aspetto | Codice superstite 774 | E21 richiesta dal brief |
|---|---|---|
| Trattamento | Envelope condizionale su routine densa | Casella, occupazione, specie e momento espliciti |
| Animali | Cap aggregato con riserva +1 | Acquisto, trasporto, collocazione e servizi coerenti col trattamento |
| Lavoro | Sostituzioni locali, rollback se nuovi PASS | Missioni con lavoratore, materiali e scadenze coperte |
| Coltura | Proposta PLANT e servizi successivi reattivi | Ammissione del ciclo fino alla vendita entro termine |
| Persistenza | Rollback e passthrough terminale | Topologia verificata fino al termine, transizioni registrate |
| Economia | Regressioni storiche non ricostruite | Saldi, quantità, prezzi, scorte e spillover riconciliati |

Prima di generare il bundle: ricostruire sui replay E18 esistenti la storia del target e la sua prima costruzione/collocazione, i relativi acquisti e vettori, le rotte e i servizi. Completare gli audit PLANT→WATER D12–19 e CARE→bonus→vendita ancora aperti. Definire quindi il prefisso invariato e il primo evento autorizzato a divergere.

I confronti restano distinti: E18 congelata; 774 senza coltivare la casella, con obbligazioni coerenti; stessa 774 con missione agricola completa. Se si rimuove solo uno slot vuoto, dichiararlo e non attribuire un risparmio animale inesistente. Conservare le rotte degli altri animali dove possibile e misurare ogni spillover.

Preregistrare campione e criteri prima delle nuove simulazioni; una simulazione per volta, 719 chiamate per agente, controllo esatto, assenza di errori e verifica topologica fino al terminale. I seed 180911301–307 sono esposti; 180912401–407 restano riservati. Le caselle vuote possono modificare i negozi attraverso il RNG condiviso: confrontare anche le traiettorie commerciali. Un calendario artificialmente fissato resta solo diagnosi. E18 rimane il riferimento competitivo; E21 non deve essere iterata indefinitamente fino a vincere.
