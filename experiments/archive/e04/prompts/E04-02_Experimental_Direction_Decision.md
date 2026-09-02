# E04-02 — Experimental Direction Decision

## Contesto

È stata completata la Competitive Gap Analysis documentata in:

`docs/experiments/E04-01_Competitive_Gap_Analysis.md`

L'audit ha identificato quattro gap principali:

1. **Gap spaziale e lavorativo** — E03 utilizza 4 delle 25 tile già disponibili nel quadrante NW e non utilizza `HIRE`;
2. **Gap di orizzonte temporale** — E03 continua ad acquistare e seminare anche quando la coltura non può più maturare entro la fine dell'episodio;
3. **Gap economico** — la formula ROI di E03 utilizza `yield_units = 2.0`, non corrispondente alle rese effettive e al comportamento delle colture ongoing;
4. **Gap metrologico** — il benchmark locale contro `pass`, `random` e `starter` non è più sufficientemente discriminante rispetto alla performance Kaggle.

La Competitive Gap Analysis ha proposto come direzione:

`Horizon & Accurate ROI Agent`

Questa proposta deve ora essere sottoposta a **REVIEW decisionale prima di procedere al PLAN**.

---

## Problema metodologico da risolvere

Il progetto segue il principio:

> **Una modifica strategica principale per esperimento.**

La proposta `Horizon & Accurate ROI Agent` sembra introdurre contemporaneamente due modifiche:

1. **Horizon Awareness**
   - impedire investimenti in colture che non possono produrre entro la fine dell'episodio;

2. **Accurate ROI**
   - sostituire l'assunzione `yield_units = 2.0` con il modello di resa reale, includendo eventualmente le colture ongoing.

Queste due modifiche hanno:

- cause differenti;
- regole decisionali differenti;
- metriche specifiche differenti;
- effetti economici potenzialmente distinguibili.

La stessa E04-01 le considera entrambe altamente isolabili.

Non assumere quindi che debbano essere implementate insieme.

---

# Obiettivo

Determinare **una sola variabile strategica principale** da sperimentare in E04.

Questa attività è esclusivamente un **decision gate**.

Non:

- modificare il codice;
- implementare E04;
- creare ancora l'Implementation Plan;
- modificare test o benchmark;
- eseguire nuovi esperimenti;
- effettuare commit, push o tag.

Utilizzare le evidenze già raccolte in E04-01 e il codice dell'ambiente solo quando necessario per verificare un'affermazione.

---

# 1. Separazione delle candidate E04

Considerare separatamente almeno le seguenti tre candidate.

## Candidate A — End-of-Season Horizon

Singola variabile:

> Introduzione della consapevolezza dell'orizzonte temporale residuo nella decisione di acquistare e seminare.

Mantenere invariati:

- footprint E03 a 4 tile;
- singolo farmer;
- formula ROI corrente;
- logica di vendita;
- priorità operative E03.

Valutare quanto capitale E03 perde effettivamente a causa di semi o colture che non producono entro lo step 720.

---

## Candidate B — Accurate ROI / Yield Model

Singola variabile:

> Correzione del modello economico utilizzato per selezionare la coltura.

Mantenere invariati:

- footprint E03 a 4 tile;
- singolo farmer;
- assenza di horizon awareness;
- vendita immediata;
- priorità operative E03.

Determinare quali elementi minimi devono essere corretti per rendere il modello ROI coerente con le meccaniche reali.

Prestare particolare attenzione alla distinzione tra:

- `max_yield`;
- tempo di maturazione;
- colture ongoing;
- rendimento cumulativo.

Non ampliare automaticamente questa candidata introducendo altre ottimizzazioni economiche.

---

## Candidate C — Initial NW Scaling

Singola variabile:

> Aumento del footprint produttivo oltre le 4 tile di E03 utilizzando esclusivamente terreno già sbloccato nel quadrante NW.

Vincoli:

- **non utilizzare `BUY_LAND`**;
- **non introdurre `HIRE`**;
- mantenere la logica economica E03;
- mantenere invariata la gestione dell'orizzonte temporale;
- mantenere invariata la logica di vendita.

L'obiettivo non deve necessariamente essere passare immediatamente da 4 a 25 tile.

Determinare quale incremento controllato del footprint possa essere gestito da un singolo farmer mantenendo:

- irrigazione;
- raccolta;
- semina;
- movimento;

senza introdurre starvation o perdita di efficienza operativa.

Considerare quindi possibili footprint intermedi, ad esempio:

`4 → 6 → 8 → ...`

ma senza eseguire ancora esperimenti.

---

# 2. Non accorpare Scaling e HIRE

La Competitive Gap Analysis associa correttamente scaling e forza lavoro come problema strutturale complessivo.

Dal punto di vista sperimentale, tuttavia:

> **aumentare il numero di tile e introdurre farm hands nello stesso esperimento introdurrebbe due variabili.**

Per E04, `HIRE` deve pertanto rimanere fuori dalla Candidate C.

Se l'analisi dimostra che il singolo farmer costituisce il limite principale dello scaling, registrare `HIRE` come possibile candidata per una successiva iterazione.

Non assegnarle automaticamente un numero di esperimento futuro.

---

# 3. Confronto delle tre candidate

Produrre una matrice decisionale:

| Criterio | Horizon | Accurate ROI | Initial NW Scaling |
|---|---:|---:|---:|
| Gap supportato da evidenza | | | |
| Impatto economico potenziale | | | |
| Impatto competitivo potenziale | | | |
| Isolabilità sperimentale | | | |
| Misurabilità locale | | | |
| Rischio operativo | | | |
| Complessità implementativa | | | |
| Dipendenza da altre meccaniche | | | |
| Capacità di spiegare il gap Kaggle | | | |

Utilizzare valutazioni motivate, non punteggi arbitrari.

Per ogni giudizio indicare brevemente l'evidenza proveniente da E04-01 o dal codice dell'ambiente.

---

# 4. Stimare l'ordine di grandezza dell'impatto

Senza modificare il codice e senza eseguire nuovi benchmark, cercare di determinare l'ordine di grandezza potenziale delle tre candidate.

Non è richiesta una previsione precisa.

L'obiettivo è distinguere tra interventi presumibilmente:

- **marginali**;
- **incrementali**;
- **significativi**;
- **strutturali**.

In particolare verificare criticamente l'affermazione contenuta in E04-01 secondo cui Horizon produrrebbe circa `+$300–$800`.

Determinare se questa stima è:

- direttamente derivata da dati osservati;
- calcolabile dal comportamento corrente;
- soltanto indicativa;
- non supportata.

Non trasformare una stima non verificata in un dato sperimentale.

---

# 5. Separare performance dell'agente e qualità del benchmark

E04-01 ha identificato il benchmark locale come un **gap metrologico critico**.

Il miglioramento della metrologia non costituisce una nuova strategia dell'agente e deve quindi essere trattato separatamente dalla variabile sperimentale E04.

Valutare se il benchmark corrente:

`pass / random / starter`

sia ancora sufficiente per discriminare il miglioramento delle candidate A, B e C.

Per ciascuna candidata indicare:

- quali metriche locali rimangono valide;
- quali metriche sono ormai sature;
- quali nuove metriche sarebbero necessarie;
- se è necessario introdurre un avversario locale più competitivo.

---

# 6. Valutare un Competitive Benchmark Agent

E04-01 suggerisce la possibile creazione di un:

`synthetic_expansion_agent`

Valutare questa proposta esclusivamente come **strumento di misurazione**, non come parte della strategia E04.

Stabilire:

1. se è necessario prima del benchmark E04;
2. quali caratteristiche minime dovrebbe possedere;
3. se può essere deterministico e riproducibile;
4. come evitare che il benchmark venga costruito specificamente per favorire E04;
5. quali metriche dovrebbe aggiungere rispetto a `starter`.

Non implementarlo in questa fase.

---

# 7. Decisione E04

Al termine dell'analisi scegliere **una e una sola** tra:

- `End-of-Season Horizon`;
- `Accurate ROI / Yield Model`;
- `Initial NW Scaling`;

oppure dichiarare che le evidenze disponibili non consentono ancora una scelta.

La decisione deve essere motivata principalmente in termini di:

1. capacità di affrontare il principale gap residuo di E03;
2. probabilità di produrre un miglioramento competitivo significativo;
3. isolabilità;
4. misurabilità;
5. rischio sperimentale;
6. valore informativo dell'esperimento anche in caso di risultato negativo.

Non privilegiare automaticamente la candidata più semplice da implementare.

Non privilegiare automaticamente la candidata con il minor rischio.

L'obiettivo dichiarato è ottenere un **cambio di passo competitivo**, non soltanto migliorare marginalmente il Mean Final Money locale.

---

# 8. Definizione preliminare dell'ipotesi

Per la sola candidata selezionata formulare:

### Experimental Variable

Una singola variabile chiaramente definita.

### Hypothesis

Una frase falsificabile nel formato:

> Se introduciamo **X**, mantenendo invariato il resto della policy E03, allora **Y** dovrebbe migliorare perché **Z**.

### Primary Metric

Una metrica primaria.

### Secondary Metrics

Massimo 3 metriche secondarie.

### Control

Indicare esplicitamente:

`E03 MultiTileROIAgent`

come baseline di controllo.

### Success Criterion

Proporre un criterio quantitativo preliminare.

Il criterio sarà validato o corretto nella successiva fase PLAN.

---

# 9. Decisione sulla metrologia

Separatamente dalla scelta strategica E04, concludere con una delle seguenti decisioni:

### A — Benchmark corrente sufficiente

Motivare perché.

oppure:

### B — Benchmark competitivo necessario prima di E04

Definire esclusivamente i requisiti del benchmark aggiuntivo.

Non implementarlo.

Questa decisione non deve essere conteggiata come seconda variabile strategica di E04, poiché riguarda l'infrastruttura di valutazione e non la policy dell'agente.

---

# Deliverable

Salvare l'analisi completa in:

`docs/experiments/E04-02_Experimental_Direction_Decision.md`

Il documento deve contenere:

1. **Review della raccomandazione E04-01**
2. **Candidate A — Horizon**
3. **Candidate B — Accurate ROI**
4. **Candidate C — Initial NW Scaling**
5. **Decision Matrix**
6. **Expected Impact Analysis**
7. **Benchmark Adequacy Review**
8. **E04 Strategic Decision**
9. **Preliminary Experimental Hypothesis**
10. **Measurement Infrastructure Decision**
11. **Open Questions**

---

# Stop condition

Al termine:

**FERMARSI.**

Non creare l'Implementation Plan.

Non modificare il codice.

Non modificare il benchmark.

Non implementare un competitive opponent.

Non eseguire benchmark aggiuntivi.

Non eseguire commit, push o tag.

Presentare:

- la candidata E04 selezionata;
- la motivazione;
- l'ipotesi preliminare;
- la decisione sulla metrologia;

e attendere approvazione.

Solo dopo la REVIEW umana si potrà autorizzare la fase **PLAN**.