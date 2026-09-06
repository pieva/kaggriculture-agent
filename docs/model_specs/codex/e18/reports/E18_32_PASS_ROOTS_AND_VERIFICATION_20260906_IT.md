# E18.32 — radici dei PASS e verifica della correzione

## Perimetro ed evidenza

Ultima pubblicata: E18.31 UNIFIED V11, submission 56050866. Diagnosi sui sei
replay già acquisiti (106069705, 106070638, 106071466, 106072386, 106073291,
106074233), inclusa la sconfitta contro Malte Bories. Non è un aggiornamento
di tutti i replay disponibili su Kaggle. Nessun nuovo Top770 consumato.

La ricostruzione del controller coincide con **4.314/4.314 batch pubblici**:
719 per partita. Gli stati osservati ricostruiscono code, cursori e prenotazioni.
Fonte: `../artifacts/derived/E18_32_PUBLISHED_PASS_ROOT_AUDIT_20260906.json`.

| Condizione immediata del PASS, D5–D10 | Occorrenze, 6 replay | Quota |
|---|---:|---:|
| Coda personale esaurita | 1.367 | 77,45% |
| Prossima azione trattenuta dall'ora nominale | 293 | 16,60% |
| COLLECT_FERTILIZER in testa alla coda bloccata | 105 | 5,95% |
| Totale | 1.765 | 100% |

"Coda esaurita" non dimostra che tutta la fattoria sia priva di lavoro né che
tutti quei PASS possano diventare ricavi. In 636 PASS risultano già terminati
FEED, CARE e raccolta fertilizzante su tutti gli animali osservati; questo non
esclude raccolti di latte/lana o lavoro colturale ancora disponibile.

## Residui confermati e loro ruolo effettivo

| Elemento | Stato nel pubblicato | Conseguenza |
|---|---|---|
| Ore, assegnatari e ordine delle code E18.28 C | Attivi | Il dispatcher interviene solo sulle finestre libere delle vecchie code |
| Organico giornaliero BoostD10 | Attivo | Capacità assunta non riconciliata col lavoro osservato |
| Calendario di colture e conversioni | Attivo come programma di base | 12 tile MELON a lunga maturazione, avvio NE a lotti; lavoro diverso dalla seconda metà del mese |
| Target di azioni e provenienza dei replay nella config | Metadati, non confronto online | Nessuna lettura delle curve o degli score Top770 durante la partita |
| Vecchi override del mercato D11/D12/D13 | Bypassati da UNIFIED E18.31 | Non attribuire loro acquisti correnti solo perché le classi sono ereditate |
| Blackout e rinvii di servizi del calendario | Materializzati nelle traiettorie | Mercato e ammissione unici, programma agricolo non ancora interamente state-driven |

Il piano congelato contiene già 102 PASS in D8, 96 in D9 e 103 in D10. Sono
slot nominali dell'oracolo, non azioni realmente emesse dal pubblicato. Rendono
comunque evidente il residuo strutturale: comprate le mucche, non scompare
automaticamente la capacità assunta sulla vecchia traiettoria.

## Radici e correzioni

1. **Capacità e lavoro non riconciliati.** Code dedicate a poche attività e
   organico prefissato convivono con espansioni decise online. Ricomporre i
   lavori completi per tile, conservando tutte le obbligazioni, e assumere meno
   persone solo con un percorso fattibile e margine di recupero. Limite sempre
   12 manovali; verificare PASS/slot e resa, non solo i PASS assoluti.
2. **Investimento e rientro dei ricavi separati dal percorso.** Una mucca porta
   lavoro, ma un percorso compatto può ritardare il DROP del latte che la
   finanzia. Inserire gli investimenti sostenibili nello stesso certificato
   della manutenzione. I ricavi necessari devono rientrare in tempo per
   acquisto, trasporto, posa, FEED e CARE; mantenere capacità per questa crescita.
3. **Prenotazioni mantenute oltre il servizio.** Il vecchio titolare aspetta
   l'intera missione dell'altro lavoratore, anche dopo la raccolta confermata.
   Rilasciare ogni servizio alla conferma osservata, conservando il vincolo
   sul trasporto e sull'inventario. L'emissione da sola non è conferma.
4. **Ore nominali che nascondono dipendenze reali.** Soprattutto finanziamento
   e apertura del nuovo quadrante: eliminare gli orari non rende eseguibili
   le attività. Programma originale come fallback quando la terra è chiusa
   o la nuova assegnazione non certifica un guadagno sicuro.

## Esperimenti conservati

- V1 CLOCK: eliminazione ore nominali a mix/organico invariati. Seed 180903001,
  entrambi i seat: PASS D5–D10 295 → 316, tre morti crop. Respinta.
- V1 FERTILITY: PASS D5–D10 invariati a 295; non selezionata per questa priorità.
  COMBINED eredita le perdite CLOCK. Nessuna delle tre entra nel bundle finale.
- V2 DEMAND: meno PASS e zero perdite nello smoke, ma mucche D8/D9 6/7 invece
  di 7/8. Respinta: manutenzione compattata senza capacità di crescita adeguata.
- V3–V5: investimenti inclusi, rilascio prenotazioni e domanda animale osservata.
  D8 ripristinato, ancora ritardo D9 per consegna tardiva del latte. Non selezionate.
  V4 include quattro errori del runner: alias `E18.2` non valido, poi corretto
  in `E18.2/V4D`. Non sono partite giocate o risultati esclusi dal confronto.
- V6/V7: consegna dei ricavi prima della scadenza dell'investimento. Smoke su
  entrambi gli avversari, poi gate esteso. V7 aggiunge il controllo generale
  dell'orizzonte biologico per le nuove mucche, senza cambiare gli esiti V6
  sui casi comuni.

Sorgenti V2/V3/V5 respinte in `../artifacts/source/`; JSON con risultati e hash.

## Limiti

Colture e date del programma originario restano il controllo: **non è stata
riscritta tutta la strategia sui 30 giorni**. La certificazione usa la stessa
regola ogni giorno, senza avversario, seed, autore o replay. Differenze di esito
dipendono da lavoro e cassa. Non ottimizza uno scarto numerico da Top770.

Due seat dello stesso seed non sono osservazioni indipendenti. Nel motore
ufficiale, l'occupazione delle tile può cambiare il consumo RNG e i negozi:
il confronto interno non sostituisce una futura verifica pubblica autorizzata.
Nessun upload, promozione o intervento sulle altre linee congelate.

## Esito finale

### V7 — verifica conclusa, non selezionata come chiusura

28/28 casi sul motore originale: sette seed, due seat, due avversari. Tutti i
controlli safety pass; cassa 78.750,29 → 78.898,00 (+0,188%), 28 delta positivi.
PASS D1–D10 428,93 → 313,07 (-27,01%); D5–D10 294,93 → 230,07 (-21,99%).
Mucche e consistenze colturali giornaliere identiche al controllo. Tuttavia
un FEED in meno in D2 riduce di un'unità la lana raccolta: regressione da non
nascondere dietro il risparmio dei salari. Bundle storico V7 preservato in
`submission/submission_codex_e18_32_770.py`; parità 2.876 batch e file-loader
pass, non pubblicato. Non usare questo file come candidato finale corrente.

### Verifica della regressione e V9

La prova V8 sulla prenotazione esclusiva del magazzino non recupera quel FEED
e aggiunge attese: non selezionata. La prima ipotesi di doppia prenotazione
non spiega quindi questa perdita. Traccia causale separata, non deduzione
dalla sola correlazione: `../artifacts/derived/E18_32_D2_FEED_TRACE_20260906.json`.

In D2 il controllo parte con cassa 25 e un grano; consegna il primo fertilizzante
a H5 e compra altro grano nello stesso batch. Il percorso compattato consegna
invece a H21/H22: alimentare tutti i pascoli diventa troppo tardi. V9 estende
la verifica finanziaria alla manutenzione, non solo alla crescita: se il cibo
degli animali già presenti dipende da incassi da consegnare, non ammettere una
compattazione puramente geometrica. Nessuna eccezione per giorno o coordinate.
È una protezione conservativa; non risolve le carenze FEED già nel controllo.

### V9 — verifica completa sul motore originale

**28/28 safety pass**, sette seed di sviluppo, due seat, E18.16 ed E18.2/V4D.
Zero errori, morti crop, fughe, missioni incomplete o violazioni di cap/topologia;
ledger riconciliati. Settantuno test mirati pass. Colture e mucche hanno
consistenze giornaliere identiche in tutti i 28 confronti. Raccolti di WHEAT,
CARROT, MELON, STRAWBERRY e WOOL identici per ogni coppia; latte medio
212,71 → 212,82. Tutti i casi conservano 12 manovali da D16 a D30.

| KPI medio | E18.31 V11 | E18.32 V9 | Lettura |
|---|---:|---:|---|
| PASS D1–D10 | 428,93 | 322,07 | -24,91% |
| PASS / slot D1–D10 | 24,41% | 19,96% | -4,45 punti percentuali |
| MOVE D1–D10 | 664,00 | 636,86 | nessuna sostituzione dei PASS con più trasporti |
| Slot effettivi D1–D10 | 1.757,00 | 1.613,43 | meno assunzioni quando il carico lo consente |
| Azioni produttive richieste D1–D10 | 560,07 | 562,07 | non confondere richieste con ricavo incrementale |
| Salari D1–D10 | 579,00 | 427,29 | -151,71 |
| PASS D5–D10 | 294,93 | 230,07 | -21,99% |
| PASS D11–D15 | 126,46 | 136,68 | regressione locale visibile, con meno MOVE e stessi lavori |
| PASS D16–D30 | 285,54 | 281,89 | nessuna crescita dell'organico nascosta |
| PASS D1–D30 | 840,93 | 740,64 | miglioramento complessivo |
| Cassa finale | 78.750,29 | 78.931,18 | +180,89 / +0,230% |
| Vittorie interne | 16/28 | 16/28 | nessuna nuova vittoria |

Cassa migliore in tutte le 28 coppie, delta minimo +118. Non sono 28 seed
indipendenti. Per avversario: E18.16 +0,187% (14/14 delta positivi), E18.2/V4D
+0,276% (14/14). Il guadagno resta piccolo e principalmente di efficienza,
non una nuova fonte di produzione. Nessuna promozione dell'incumbent.

| Giorno | PASS E18.31 | PASS E18.32 | Manovali E18.31 → E18.32 | Mucche, entrambe |
|---|---:|---:|---|---:|
| D1 | 43 | 43 | 5 → 5 | 2 |
| D2 | 38 | 28 | 4 → 4 | 2 |
| D3 | 3 | 3 | 4 → 4 | 2 |
| D4 | 50 | 18 | 5 → 3 | 3 |
| D5 | 25 | 25 | 5 → 5 | 4 |
| D6 | 42 | 24 | 5 → 4 | 4 |
| D7 | 42 | 42 | 9 → 9 | 4 |
| D8 | 60 | 24 | 8 → 6 | 7 |
| D9 | 60 | 60 | 10 → 10 | 8 |
| D10 | 65,93 | 55,07 | 11 → 9,71 | 9 |

**Il problema non è risolto integralmente.** D1/D3/D5/D7/D9 restano invariati;
D12 peggiora da 36,50 a 47,71 PASS, mentre cala il trasporto e i raccolti restano
invariati. Non scegliere nuove regole per far aderire queste curve al Top.
La prossima ipotesi, nello stesso filone anti-PASS, è esplicitare le dipendenze
tra produzione, consegna, liquidità, apertura del terreno e rilascio dei lavori:
il semplice fallback conserva proprio le attese ancora visibili in D7/D9.

Riepilogo riproducibile:
`../artifacts/derived/E18_32_READY_WORK_SUMMARY_RELEASE_V9_20260906.json`.
Gate: `../artifacts/derived/E18_32_READY_WORK_GATE_RELEASE_V9_DEVELOPMENT_20260906.json`.
Nuovo file: `submission/submission_codex_e18_32_770_v9.py`, 284.395 byte,
SHA-256 `4d2d32ac41b38af5f4f632ef9e8dd9af2ebd37f7e7bcb1795c2c31cda4e92789`.
Parità standalone/file-loader V9 completata: quattro casi, 2.876 batch
identici per metodo, zero errori/missioni incomplete; chiamata massima 0,819 s.
Fonte `../artifacts/derived/E18_32_SUBMISSION_PARITY_V9.json`; nessun upload Kaggle.

Decisione successiva: V9 conservata come controllo, non conforme alla richiesta
di policy agricola unica. La diagnosi Q0 e la bonifica architetturale sono in
`E18_33_LEGACY_POLICY_AUDIT_20260906_IT.md`; specifica E18.33 nel MODEL_SPEC.
