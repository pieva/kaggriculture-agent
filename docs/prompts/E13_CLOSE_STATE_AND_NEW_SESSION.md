# E13 — CHIUSURA STATO E NEW SESSION

## Obiettivo

Chiudere ordinatamente la sessione corrente del progetto Kaggriculture dopo l'analisi forense multi-agent dell'episodio Kaggle `101971376`, salvando:

1. evidenze e conclusioni E13 consolidate;
2. stato operativo corrente;
3. decisioni metodologiche;
4. questioni ancora aperte;
5. `NEW_SESSION.md` autosufficiente per ripartire domani senza ricostruire il contesto dalla chat.

Questa attività è **documentazione e chiusura di sessione**, non BUILD strategico.

---

## 1. Safety preliminare

Prima di modificare file:

```powershell
git branch --show-current
git status --short
git diff --stat
```

Il working tree contiene modifiche preesistenti e output prodotti da più agenti.

NON:

- reset;
- clean;
- stash;
- revert;
- sovrascrivere output E13 degli altri agenti;
- modificare `.venv`;
- modificare strategy code;
- modificare submission;
- fare tuning;
- fare upload Kaggle.

Non fare commit/push automaticamente. Al termine mostra lo stato e proponi l'eventuale commit, ma attendi approvazione umana.

---

# 2. Evidenza primaria da consolidare

L'episodio di riferimento è:

- `episode_id`: `101971376`
- `seed`: `1630102796`
- Pietro Valocchi: `$7,123`
- Harith Al-Ani: `$133,049`
- gap: `$125,926`
- ratio: `18.68x`
- raw replay: `docs/benchmark/101971376.json`

Usare come fonti le tre analisi indipendenti già prodotte:

- `results/e13/episode_101971376/antigravity/`
- `results/e13/episode_101971376/codex/`
- `results/e13/episode_101971376/copilot/`

Leggere ora tutte e tre le analisi e i relativi CSV/evidence matrix. La fase blind è terminata.

Non modificare i loro output originali.

---

# 3. Convergenza multi-agent da documentare

La sintesi deve distinguere chiaramente:

## 3.1 Fatti convergenti

I tre agenti convergono almeno sui seguenti punti, da verificare contro i file prima di registrarli:

- final money `$7,123` vs `$133,049`;
- il gap non nasce nel late game;
- Q2 non è una spiegazione causale sufficiente;
- workforce, livestock e superficie acquistata non spiegano da soli il risultato;
- Harith converte molto più efficacemente capacità disponibile in azioni produttive, output, SELL e reinvestimento;
- Harith: `1,145 WATER`;
- Pietro: `79 WATER`;
- Harith explicit/estimated SELL value circa `$171,870`;
- Pietro circa `$83,418`;
- la differenza fondamentale è nel **productive/economic throughput**, non nella sola capacità fisica acquistata.

Verificare le definizioni precise usate dai singoli parser prima di dichiarare due metriche perfettamente equivalenti.

## 3.2 Divergenza interpretativa da preservare

Non appiattire la differenza:

- Antigravity individua un **causal onset operativo** già nel Day 1, con loop/dispatch inefficiente e mancata irrigazione;
- Copilot individua anch'esso una **material divergence nel Day 1**, con `21` productive tiles Harith vs `8` Pietro alla boundary del turn 23;
- Codex usa una soglia più conservativa e colloca il **economic lock-in** al Day 12, quando il vantaggio è già persistente in cash, superficie produttiva, land e livestock.

Registrare quindi la distinzione:

`Day 1 = causal/operational onset`

`Day 12 = economic lock-in / structural persistence`

Non trattarla come semplice contraddizione tra agenti.

---

# 4. Nuova conclusione E13

Documentare come conclusione centrale, con status appropriato:

> La nostra carenza principale osservata nell'episodio 101971376 non è la quantità di capacità acquistata, ma la conversione della capacità disponibile in lavoro produttivo e monetizzazione.

Catena economica di riferimento:

`worker-turn → productive action → output/inventory → SELL → cash → reinvestment → compounded capacity`

Questa catena deve sostituire come lente primaria le interpretazioni semplicistiche basate isolatamente su:

- numero di Hands;
- numero di animali;
- Q1/Q2;
- superficie posseduta;
- weeds;
- productive tiles senza monetizzazione.

NON trasformare ancora questa conclusione in nuova strategia.

---

# 5. Evidenze quantitative da preservare

Registrare almeno:

### Irrigazione

- Harith: `1,145 WATER`
- Pietro: `79 WATER`
- delta: `+1,066`
- rapporto: circa `14.5x`

### SELL

- Harith: circa `$171,870`
- Pietro: circa `$83,418`
- delta: circa `$88,452`

Specificare `explicit` / `estimated` secondo la terminologia dei parser e le limitazioni sui prezzi dinamici.

### Day 1

Copilot:

- Harith: `21 productive tiles`
- Pietro: `8 productive tiles`
- entrambi ancora nel solo quadrante iniziale.

### Crop-care

Codex:

- Harith: `1,333`
- Pietro: `259`
- delta: `+1,074`

Non equiparare automaticamente `crop-care` a `WATER`: sono metriche differenti ma convergenti sullo stesso fenomeno di throughput.

### Antigravity

Preservare come evidenze da verificare/qualificare:

- loop di `HARVEST` improduttivo nella nostra policy nel Day 1;
- cash-crop revenue Harith molto superiore;
- forte BUY_PRODUCT WHEAT della nostra policy;
- maggiore monetizzazione Fertilizer/Wool/Milk da parte di Harith.

Se una cifra è supportata da un solo parser, etichettarla come evidenza single-agent, non come consenso dei tre.

---

# 6. Cosa E13 falsifica o indebolisce

Registrare esplicitamente che l'episodio indebolisce/falsifica come spiegazioni sufficienti:

- “serve semplicemente Q2”;
- “servono semplicemente più Hands”;
- “servono semplicemente più animali”;
- “serve semplicemente usare più superficie”;
- “basta tenere il campo pulito”;
- “il gap nasce soprattutto nel late game”.

La formulazione corretta è che queste variabili possono essere **capacity enablers**, ma devono essere valutate attraverso la loro conversione in throughput economico.

---

# 7. Cosa rimane non dimostrato

Preservare le limitazioni:

- intento/funzione di utilità interna di Harith: non osservabile;
- causalità monetaria precisa per singola causa: non identificabile senza counterfactual;
- costo HIRE/BUY_LAND e P/L transazionale: usare la prudenza indicata dai parser quando non direttamente osservabile;
- opportunity cost delle azioni non eseguite: inferito, non osservato;
- “stessa architettura”: valido solo a livello macroscopico/visivo, NON come equivalenza della policy operativa;
- non è ancora dimostrato che correggere WATER/dispatch sia sufficiente a raggiungere performance competitive;
- rimane aperta la discrepanza Local ↔ Kaggle.

---

# 8. Separare due problemi per la prossima sessione

`NEW_SESSION.md` deve distinguere nettamente:

## A. E13 — Competitive Throughput

Domanda:

> Perché, nello stesso episodio/seed/mercato, Harith converte capacità simile in `$133,049` mentre noi chiudiamo a `$7,123`?

E13 ha ora una diagnosi forte: differenza enorme di productive/economic throughput, già visibile dal Day 1.

## B. Local ↔ Kaggle Fidelity

Problema separato:

- candidate Antigravity locale seed `0`: `$37,543`
- primo episodio Kaggle seed `0`: `$8,690`

Questa discrepanza NON deve essere confusa con il confronto Pietro vs Harith dell'episodio `101971376`.

Serve una futura analisi dedicata same-code/same-seed local-vs-Kaggle per trovare la prima divergenza di state/action.

---

# 9. Decisione per domani

Non avviare ora E14.

La prossima sessione deve partire da una fase di consolidamento/DEFINE.

Ordine raccomandato:

1. consolidare formalmente le tre evidence matrix E13;
2. proporre il delta minimo a `MODEL_SPEC`;
3. definire **Economic Throughput** come lente/metrica primaria, senza ancora cambiare policy;
4. audit mirato del perché la nostra policy produce `79 WATER` contro `1,145`;
5. verificare il loop `HARVEST`/dispatch/pathfinding indicato da Antigravity;
6. solo dopo definire un E14 BUILD stretto e falsificabile;
7. mantenere separata la successiva analisi Local ↔ Kaggle Fidelity.

Il BUILD futuro NON deve essere “un'altra nuova architettura” senza prima aver isolato il meccanismo.

---

# 10. Aggiornamenti documentali

Aggiorna i documenti di stato esistenti appropriati, preservandone struttura e convenzioni.

In particolare:

- `NEW_SESSION.md`
- `PROJECT_STATE.md`, se esiste ed è il documento canonico di stato;
- eventuale experiment log/version log già usato dal repository per registrare E13.

Non modificare `docs/MODEL_SPEC.md` in questa chiusura: il delta deve essere proposto e discusso domani, non applicato automaticamente.

Se manca un documento atteso, non inventare una nuova tassonomia documentale: segnala la mancanza.

---

# 11. Requisiti di NEW_SESSION.md

`NEW_SESSION.md` deve essere autosufficiente e consentire di aprire domani una nuova chat senza recuperare questa conversazione.

Deve includere almeno:

- obiettivo generale Kaggriculture;
- metodologia agent-supervised e benchmark-first;
- stato sintetico E12/X1.12–X1.15 necessario a capire E13;
- replay benchmark principali;
- episodio `101971376` e perché è decisivo;
- risultati Antigravity/Codex/Copilot;
- convergenze;
- divergenze interpretative;
- conclusione Economic Throughput;
- evidenze quantitative principali;
- ciò che è falsificato/indebolito;
- ciò che resta NOT_OBSERVABLE;
- distinzione Competitive Throughput vs Local↔Kaggle Fidelity;
- working-tree safety;
- environment canonico;
- cosa NON fare;
- primo task preciso della prossima sessione.

Evita cronache verbose di comandi. Conserva invece decisioni, numeri, provenance e razionale.

---

# 12. Verifica finale

Al termine eseguire:

```powershell
git diff --check
git status --short
git diff --stat
```

Verificare esplicitamente:

- nessuna strategy modificata da questa attività;
- nessuna submission modificata;
- `.venv` intatta;
- `docs/MODEL_SPEC.md` intatto;
- raw replay intatti;
- output originali dei tre agenti intatti;
- `NEW_SESSION.md` aggiornato;
- stato E13 documentato.

NON fare commit/push senza approvazione.

---

# 13. Output finale

Rispondi con:

1. documenti aggiornati;
2. sintesi di ciò che è stato salvato;
3. eventuali discrepanze trovate tra le tre analisi;
4. conferma delle safety conditions;
5. `git status --short`;
6. proposta di commit message, **senza eseguire il commit**.

Chiudi con:

`E13 SESSION STATE SAVED — READY FOR NEXT SESSION`
