# E17.1 — Piano statico V4 (archetipo shiggriculture 6-6-2): tempi e dimensionamenti medi

- **Data:** 2026-09-02, aggiornato 2026-09-03.
- **Stato:** IMPLEMENTATO ED ESEGUITO (2026-09-03) — la topologia SW/Q2
  di Sezione 0 è stata tradotta in codice
  (`src/agricola/strategy/claude/e17_reactive_3q_v4.py`, MODEL_SPEC V4) e
  testata su 4 seed contro Codex black-box. **Esito negativo in
  aggregato** (`-8,9%` di denaro medio vs V3, segno incoerente fra seed):
  la matrice completa a 7 seed NON è stata eseguita, per protocollo
  (Sezione 5). Dettaglio:
  `docs/model_specs/claude/e17/reports/E17_1_CLAUDE_REACTIVE_V4_DEVELOPMENT_REPORT_IT.md`.
  Le Sezioni 1-6 sotto restano il piano originale (provenance), non
  aggiornate retroattivamente.
- **Fonti:** `docs/model_specs/claude/e17/reports/E17_TOP3_PARAMETER_SYNTHESIS_IT.md`,
  `experiments/e17/reports/common/E17_CROSS_AGENT_RECONCILIATION_AND_TOP3_PROFILES_IT.md`,
  tracciamento diretto della nostra V3 (`e17_reactive_3q_v3.py`, config
  frozen) su seed `26090101`, sessione corrente; screenshot Kaggle live
  del 2026-09-03 in `data/screenshots/` (Sezione 0).
- **Archetipo scelto (revisionato 2026-09-03):** **shiggriculture** — bestiame
  quasi simmetrico Q0/Q1 (6 tile ciascuno) più un nucleo minimo non-zero in
  Q2 (2 tile adiacenti allo Shed), misurato su uno screenshot Kaggle live
  (match vinto, rating `1283 (+5)`, denaro finale `127.357` — il più alto
  osservato tra tutte le schermate del 2026-09-03). Sostituisce l'archetipo
  OceanMix (Sezioni 1-6, sotto), che restava un'ipotesi costruita sui nove
  replay offline di discovery E17 e assumeva Q2 esclusivamente a coltura.
  Vedi Sezione 0 per l'evidenza e il perché della revisione.

---

## 0. Aggiornamento 2026-09-03 — nuovo archetipo osservato: shiggriculture (6-6-2)

**Origine:** il proprietario ha fornito dieci screenshot Kaggle live del
2026-09-03, catturati durante la revisione di partite recenti. Erano evidenza
transitoria e non sono mantenuti nel repository; i conteggi consolidati sono
riportati in questo documento. Non sono i nove replay offline di discovery
già usati per la sintesi Top3 (`E17_TOP3_PARAMETER_SYNTHESIS_IT.md`): sono
partite Kaggle vive più recenti, con farm terminali a `720/720` step.

**Osservazione 1 — la nostra submission live (Codex, non Claude) è già 3Q
piena, non 2Q.** Il farm marcato `1` in sei delle dieci schermate è
`Pietro Valocchi`, cioè la submission Kaggle correntemente in gioco
(rating osservato `1055`-`1283`, coerente con gli snapshot Codex E17 già
registrati in `docs/PROJECT_STATE.md`). Il suo layout è **identico e
deterministico** nelle sei partite (`070620`, `070643`, `070721`, `070822`,
`070739`, `072409`; ricontrollo pixel-per-pixel su crop 2×), con denaro
finale `86.492`-`121.043` a seconda dell'esito. Conteggio tile a pascolo
per quadrante: **NW 7 / NE 6 / SW 5** (18 tile totali, SE mai sbloccato,
coerente col vincolo 3Q del progetto). Questo smentisce l'assunzione
OceanMix di Q2 crop-only: la submission Codex live mette bestiame ovunque,
con una densità quasi bilanciata.

**Osservazione 2 — esistono comunque archetipi avversari a 2Q puro (Q2
crop-only), coerenti con OceanMix.** `hisatarosu` (`070918`, vinto
`1187 (+39)`, denaro `118.775`) e `iVl44d` (`070952`, vinto `1201 (+4)`,
denaro `102.159`) hanno bestiame **solo in NW/NE, zero in SW**. L'ipotesi
Q2-crop-only non è quindi falsificata in generale: coesiste con archetipi
3Q pieni nello stesso pool di avversari.

**Osservazione 3 — shiggriculture è la via di mezzo, ed è quella con
rating e denaro più alti osservati.** Dallo screenshot `070643` (farm
marcato `1` in basso, `[Win] shiggriculture 1283 (+5)`, denaro `127.357`),
ricontato riga per riga su crop 2×:

| Quadrante | Tile pascolo | Righe (1=NW, 6-10=SW) |
|---|---:|---|
| NW (Q0) | **6** | riga3: 1, riga4: 2, riga5: 3 |
| NE (Q1) | **6** | riga3: 1, riga4: 2, riga5: 3 |
| SW (Q2) | **2** | riga6: 2 (adiacenti allo Shed), righe 7-10: 0 |

**Stato epistemico:** CONFERMATO per conteggio (rilettura pixel-per-pixel,
consistente con la griglia visibile), ma da **un solo screenshot/un solo
match**, quindi un solo campione dell'archetipo shiggriculture — a
differenza del 7-6-5 di Pietro Valocchi, verificato su sei partite
indipendenti. Non sappiamo se shiggriculture ripete questo pattern in
altre partite; trattarlo come rappresentativo dell'intero suo stile
richiederebbe più campioni, che qui non abbiamo.

**Conseguenza per il piano:** le Sezioni 1-6 sotto restano il ragionamento
originale sull'archetipo OceanMix (Q2 strettamente a zero animali) e sono
mantenute come provenance, ma il target quantitativo di Sezione 3 è ora
sostituito dal profilo 6-6-2: **Q2 non è più vincolato a zero animali**,
riceve un piccolo nucleo (indicativamente 2 tile, aperto tardi e vicino
allo Shed) invece di restare esclusivamente a coltura. Il target economico
di denaro rimane quello di `E17_1_CLAUDE_REACTIVE_V4_100K_IMPROVEMENT_PLAN.md`
(indicativo `100.000`): sia la submission Codex live (fino a `121.043`)
sia shiggriculture (`127.357`) lo superano già con topologie diverse, il
che rafforza che il gap Claude-Codex quantificato in quel documento
(`10,53×`) è dominato da altre cause (movimento, workforce — Sezione 2 di
quel piano), non dalla sola scelta se popolare Q2.

---

## 1. Scoperta che ridefinisce la priorità del piano

Prima di questa sessione, l'ipotesi guida era: "il gregge finale è troppo
piccolo (4,36 contro 15,35 medio Top3), quindi bisogna far crescere la
workforce e il numero di animali verso il target finale." Tutti i tentativi
in questa direzione (rampe, target statici, gate di cassa) hanno
**peggiorato** il risultato, in un caso del 18% sulla matrice completa.

Confrontando **la traiettoria di cassa giorno per giorno**, non solo i
valori finali, emerge una causa diversa e più precisa:

| Giorno | OceanMix (cassa media) | Nostra V3 (stesso giorno, seed `26090101`) | Rapporto |
|---|---:|---:|---:|
| D10 | 15.820,75 | 309 | **51×** |
| D15 | 26.126 | 5.669 | 4,6× |
| D20 | 49.138 | 7.254 | 6,8× |
| D29 (finale) | 82.535 | 18.264 | 4,5× |

**Osservazione chiave:** la tempistica di sblocco dei quadranti è già
quasi identica alla nostra — 2Q (NE) a D5-D6 come OceanMix, 3Q (SW)
esattamente a D11 come OceanMix (verificato: la nostra V3 raggiunge
`quadrants=2` a D5, `quadrants=3` a D11). **Non è un problema di
calendario di espansione.** Anche la workforce tocca brevemente 12 a D11
(il picco comune ai tre top player), ma poi fluttua (12→11→12→9) invece di
restare stabile.

La differenza che salta all'occhio è un'altra: **a D10 la nostra V3 ha
zero animali**, mentre la topologia D10 di OceanMix (Sezione 4 della
fonte) mostra già **Q0 C14,75/A6,75/I3,5** — quasi 7 animali già presenti
e produttivi. Il gregge precoce, non la dimensione finale del gregge né la
workforce, è il candidato più credibile per il moltiplicatore 51× a D10:
WOOL/EGG/MILK da ~7 animali per 20+ giorni consecutivi è un flusso di
cassa cumulato enorme rispetto a nessun animale per i primi 27 giorni
(la nostra V3 compra il primo animale solo a D27-29).

**Questo capovolge la priorità del piano**: non "far crescere il gregge
finale", ma "avere un piccolo nucleo di 5-7 animali funzionante il prima
possibile", anche a costo di un gregge finale più piccolo del target
Top3.

---

## 2. Tensione con i vincoli già scoperti in questa sessione

Ogni tentativo di anticipare gli acquisti zootecnici in questa sessione ha
causato collassi, perché il costo Fibonacci del HIRE e le riserve di
cassa rendono l'economia iniziale estremamente fragile. Il piano statico
deve quindi essere esplicito su **come** OceanMix può permettersi 7
animali a D10 senza le stesse risorse iniziali della nostra V3 (stesso
capitale di partenza, $3.000):

- **Ipotesi più plausibile**: OceanMix non massimizza la workforce
  nei primissimi giorni. Se tiene la manodopera bassa (3-5 mani) mentre
  stabilisce le prime strutture e i primi animali, il costo Fibonacci
  giornaliero resta piccolo (`sum(fib(0..4))=12` contro `sum(fib(0..8))=88`
  per 9 mani), lasciando molto più margine di cassa per gli acquisti
  zootecnici nella stessa finestra. Non abbiamo ancora il dato
  giorno-per-giorno degli `hands` di OceanMix (solo i picchi), quindi
  questa resta un'**ipotesi da verificare**, non un fatto.
- **Rischio già dimostrato**: comprare animali "presto" senza aver prima
  verificato la sostenibilità di cassa ha causato, in questa sessione,
  collassi ripetuti (denaro a $35-400, workforce a 0). Qualunque
  implementazione futura deve introdurre l'anticipo zootecnico come
  **unica variabile mutata**, con la workforce lasciata alla formula V3
  già stabile, e testata sulla matrice completa a 7 seed prima di
  dichiararla sicura — non sui soli 4 seed di spot-check, che in questa
  sessione hanno nascosto due collassi gravi.

---

## 3. Piano statico — tempi e dimensionamenti target (traiettoria di cassa OceanMix, topologia rivista shiggriculture 6-6-2)

| Fase | Giorno | Target quadranti | Target workforce | Target animali (per quadrante) | Target coltura |
|---|---|---|---|---|---|
| Bootstrap | D0-D5 | NW (dato) | 3-5 (non forzare oltre) | 0 → avvio prime strutture COOP/PASTURE in NW appena la cassa lo permette | semina WHEAT/altre secondo densità già in uso |
| Apertura NE | D6 | NW+NE (2Q) | segue la formula floor/load V3 (già raggiunge ~7-9 qui) | **primi 2-3 animali in NW**, non attendere `core_established` a piena densità | prosegue |
| Consolidamento | D6-D10 | 2Q | verso 9-12 (V3 già lo tocca a D11) | **crescita verso 6-7 in NW**, eventuale avvio in NE | Q0/Q1 verso densità 55-70% |
| Apertura SW | D11 | 3Q (SW) | picco 12 | 6-7 in NW, 6-7 in NE (12-14 totali split ~6/6); **revisione 2026-09-03: aprire anche 2 tile pascolo in SW vicino allo Shed** (evidenza shiggriculture 6-6-2, Sezione 0), non 0 come nell'ipotesi OceanMix originale | SW prevalentemente a coltura ma non esclusivamente: 2 tile pascolo + resto a densità verso 100% entro D15 |
| Maturità | D15-D25 | 3Q | 10-12 stabile (non far scendere a 9 come osservato) | mantenimento 14, sostituzione capi persi | Q0/Q1/SW dense, liquidazione differita |
| Chiusura | D25-D29 | 3Q | riduzione naturale (shutdown/liquidazione, invariato da V3) | liquidazione differenziata (vendita prodotti, non animali vivi se possibile) | liquidazione |

### Checkpoint di verifica (non gate operativi, criteri di successo del piano)

| Giorno | Cassa target indicativa (da OceanMix, con margine) | Nostra V3 attuale |
|---|---:|---:|
| D10 | avvicinarsi a `5.000-8.000` (non serve eguagliare 15.820, ma uscire dall'ordine di grandezza attuale) | 309 |
| D15 | avvicinarsi a `15.000-20.000` | 5.669 |
| D20 | avvicinarsi a `30.000-40.000` | 7.254 |
| D29 | target finale onesto: `40.000-60.000` in questa prima iterazione, non 82.535 subito | 18.264 |

**Nota 2026-09-03:** questa traiettoria giorno-per-giorno resta quella di
OceanMix (unico archetipo di cui abbiamo dati D10-D29 intermedi, dai nove
replay di discovery); non abbiamo la stessa granularità per la submission
Codex live o per shiggriculture, solo il loro stato terminale (Sezione 0:
rispettivamente `121.043` e `127.357` a fine partita, entrambi sopra il
target indicativo `100.000`). Il target finale onesto `40.000-60.000` resta
quindi la stima più bassa e più prudente per una prima iterazione V4; non va
alzato a `100.000+` sulla sola base della topologia 6-6-2, che informa la
**forma** del piano (dove aprire pascolo), non la **velocità economica**
raggiungibile da Claude con la sua workforce/movimento attuali.

Questi checkpoint D10-D20 sono **criteri di verifica in fase di sviluppo**
(controllare se una modifica sta avvicinando o allontanando la
traiettoria reale da questi valori), non soglie che il codice deve
leggere: usarli come gate diretti nel codice ripeterebbe l'errore già
commesso con le soglie di cassa piatte.

---

## 4. Cosa il piano NON cambia rispetto alla V3

Per isolare la causa e non ripetere l'errore di modificare troppe cose
insieme (osservato più volte in questa sessione):

- **Timing di espansione territoriale**: lasciato invariato
  (`_expansion_guard`, density-gated) — già allineato al calendario
  Top3.
- **Formula di workforce**: lasciata alla formula floor/load-driven V3
  già stabile su tutta la matrice, **non** sostituita da un target fisso
  o da una rampa (il tentativo di rampa Fibonacci-aware isolata ha dato
  -18% sulla matrice completa nella sessione precedente, nonostante
  sembrasse neutra su 4 seed).
- **Riserve di cassa esistenti** (`hire_reserve`, `land_purchase_reserve`,
  `animal_purchase_reserve`): lasciate ai valori V3, che proteggono da
  collassi già documentati. Il piano propone di **anticipare quando**
  la logica di acquisto zootecnico viene consultata (prima, non dopo,
  la piena densità di `core_established`), non di abbassare le riserve
  che la proteggono.

## 5. Unica variabile da introdurre, in isolamento

**Ipotesi causale singola da testare per prima** (protocollo di ablation
già consolidato nel progetto): sostituire il gate `_core_established`
davanti a `_animal_orders` con una soglia **più permissiva e dedicata**
per i primi 2-3 animali soltanto (es. "almeno 1 struttura pronta e
`plant_tiles_count > 0`", senza richiedere la densità piena richiesta per
`BUY_LAND`), lasciando il resto della funzione (ratchet zero-rischio,
riserva dedicata, un acquisto per chiamata) **esattamente come in V3**.
Nessun'altra modifica nello stesso esperimento.

### Protocollo di test per questa singola modifica

1. Spot-check su 2 seed development con tracciamento giorno-per-giorno
   (money, animal_headcount, weed) fino a D15, per verificare che non si
   riproduca il collasso da cassa-pinned già visto.
2. Se stabile, estendere a tutti e 4 i seed di spot-check già usati in
   questa sessione.
3. **Solo se stabile su tutti e 4**, eseguire la matrice completa a 7
   seed × 2 seat (14 run) prima di dichiarare qualunque miglioramento —
   obbligatorio dopo l'esperienza di questa sessione, dove i 4 seed di
   spot-check hanno nascosto due collassi gravi visibili solo sulla
   matrice completa.
4. Riportare il risultato onestamente anche se negativo, come richiesto
   dal protocollo del progetto.

**Nota 2026-09-03 sulla sequenza:** l'apertura di un piccolo pascolo in SW
(Sezione 0, evidenza 6-6-2) è una variabile causale diversa da quella
testata qui (il gate `_core_established` anticipato in NW) e va introdotta
in un esperimento separato, **dopo** aver validato questa prima modifica
sulla matrice completa — non insieme, per non ripetere il pattern già
osservato in questa sessione di variazioni aggregate non attribuibili.

---

## 6. Cosa resta esplicitamente fuori da questo piano

- Non tocca la topologia di NE. **Revisione 2026-09-03**: SW non è più
  vincolato a "solo coltura" per costruzione — l'evidenza shiggriculture
  (Sezione 0) mostra un piccolo nucleo pascolo anche in SW nel match con
  il denaro più alto osservato. Questo implica che `max_quadrants_for_livestock`
  dovrebbe diventare `3` (non più `2`) quando si implementerà questa
  revisione, punto non ancora tradotto in codice/config in questo
  documento di piano.
- Non introduce nuove specie animali o crop.
- Non modifica la logica di piazzamento già corretta e verificata in
  questa sessione (rivalidazione specie-aware, consegna forzata per un
  worker inattivo che trasporta un animale) — quei fix restano validi
  indipendentemente da questo piano e possono essere reintrodotti nello
  stesso esperimento se il gate di `_core_established` anticipato da
  solo non basta a far atterrare gli animali comprati.
- Non fissa ancora un target numerico di denaro finale da dichiarare
  come successo: i checkpoint di Sezione 3 sono indicativi, il giudizio
  finale resta la matrice completa a 7 seed.
