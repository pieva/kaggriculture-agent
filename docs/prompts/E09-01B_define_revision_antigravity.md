# E09-01 — DEFINE REVISION — Correzione Baseline e Disegno Sperimentale

## Contesto

Il DEFINE di **E09-01 — Livestock Subsystem Ablation** è stato completato e ha prodotto un audit utile del sottosistema livestock.

È però emersa una **incoerenza metodologica** da correggere prima di autorizzare il BUILD:

- il DEFINE dichiara correttamente **E08 — Productive Scale Optimization** come baseline dell'esperimento;
- nel disegno sperimentale e nel criterio decisionale viene però proposta **E07** come baseline primaria.

Questa revisione serve esclusivamente a riallineare il documento sperimentale.

**Non implementare E09-01. Non modificare il codice produttivo. Non eseguire benchmark. Non costruire submission. Non accedere a Kaggle.**

---

# Decisione metodologica vincolante

La baseline primaria di E09-01 deve essere:

> **E08 — 40 tile — Livestock ON**

Il treatment E09-01 deve essere:

> **E09-01 — 40 tile — Livestock OFF**

Questa è l'unica configurazione che realizza una **ablation controllata pura** rispetto a E08, perché modifica una sola variabile sperimentale:

`Livestock ON → Livestock OFF`

mantenendo invariato il footprint produttivo da 40 tile e tutto il resto della strategia E08.

---

# Ruolo di E07

E07 resta importante, ma deve essere trattato esclusivamente come **benchmark secondario di riferimento**.

Configurazione:

- **E07:** 24 tile + Livestock ON
- **E08:** 40 tile + Livestock ON
- **E09-01:** 40 tile + Livestock OFF

La lettura sperimentale deve quindi essere:

```text
E07
24 tile + Livestock ON
Mean Final Money = 13,320.37
        |
        | scaling 24 → 40 tile
        v
E08
40 tile + Livestock ON
Mean Final Money = 11,880.30
        |
        | livestock ablation
        v
E09-01
40 tile + Livestock OFF
Mean Final Money = ?
```

E07 non deve essere usato per definire il delta causale primario dell'ablation.

---

# Domanda sperimentale corretta

La domanda primaria di E09-01 resta:

> **Se rimuoviamo il livestock da E08 senza cambiare nient'altro, cosa succede?**

Più precisamente:

> La rimozione del sottosistema livestock consente alla configurazione produttiva da 40 tile introdotta in E08 di utilizzare meglio capitale, azioni, movimento e spazio?

---

# Interpretazione causale

E08 ha mostrato:

- footprint produttivo: **40 tile**;
- Mean Final Money: **$11,880.30**;
- Worker Movement Share: **61.6%**;
- `plant_pending` backlog: **17.96 tile/giorno**;
- livestock net balance: **-$3,977.34**.

E07, con footprint da 24 tile e stesso livestock attivo, aveva:

- Mean Final Money: **$13,320.37**.

Il peggioramento E07 → E08 ha quindi falsificato l'ipotesi che il semplice aumento dello spazio produttivo generasse maggiore valore.

E09-01 deve verificare una nuova possibilità:

> il footprint da 40 tile potrebbe non essere intrinsecamente inefficiente; potrebbe essere incompatibile con il carico operativo ed economico imposto dal livestock.

Questa interpretazione è centrale e deve essere esplicitata nel documento DEFINE aggiornato.

---

# Modifiche richieste al DEFINE

Aggiorna:

`docs/versions/E09_define_livestock_ablation.md`

e gli eventuali documenti di stato già modificati nella precedente fase DEFINE.

Non creare un nuovo esperimento.

Non rinominare E09-01.

Non introdurre E09-02.

---

## 1. Baseline primaria

Sostituisci ogni formulazione che presenta E07 come baseline primaria con:

> **Primary baseline: E08 — 40 tile — Livestock ON**

Dataset di riferimento:

`results/e08_productive_scale.json`

Le metriche E08 restano:

- Total Episodes: 30
- Completion Rate: 100.0%
- Disqualification Rate: 0.0%
- Win / Draw / Loss: 28 / 0 / 2
- Mean Final Money: **$11,880.30**
- Sample Std Dev (`ddof=1`): **$6,475.07**
- Median Final Money: **$9,790.50**
- Vs `pass`: **$10,987.80**
- Vs `random`: **$11,123.70**
- Vs `starter`: **$13,529.40**
- Livestock Net Balance: **-$3,977.34**
- Worker Movement Share: **61.6%**
- `plant_pending` backlog: **17.96 tile/giorno**

Verifica comunque i valori nel file sorgente prima di riscriverli.

---

## 2. Treatment E09-01

La configurazione sperimentale E09-01 deve essere definita come:

- footprint: **40 tile**
- livestock: **OFF**
- workforce: invariata rispetto a E08
- spatial partitioning: invariato rispetto a E08
- Water-First priority: invariata
- land expansion policy: invariata
- crop policy: invariata
- market policy non-livestock: invariata
- worker assignment: invariato salvo le conseguenze naturali della rimozione delle task livestock
- ogni altra logica E08: invariata

Non riportare la configurazione a 24 tile.

---

## 3. E07 come benchmark secondario

Mantieni E07 nel documento, ma etichettalo chiaramente come:

> **Secondary historical reference**

Serve per valutare se E09-01:

1. recupera semplicemente parte della regressione E08;
2. torna circa al livello E07;
3. supera anche E07.

Il confronto E09-01 vs E07 è quindi **descrittivo e strategico**, non il confronto causale primario.

---

# Disegno sperimentale corretto

Il benchmark futuro deve essere organizzato attorno a:

## Primary comparison

`E09-01 (40t, livestock OFF) − E08 (40t, livestock ON)`

Questo è il delta causale principale.

Se tecnicamente possibile, utilizzare:

- stessi opponent;
- stessi seed;
- stesso numero di episodi;
- stesso ordine degli episodi;
- stesso environment;
- stessi limiti;
- paired episodes.

La misura primaria deve essere:

`paired_delta_i = money_E09_i - money_E08_i`

e quindi:

- mean paired delta;
- median paired delta;
- paired win / tie / loss;
- dispersione dei delta;
- breakdown dei delta per opponent.

---

## Secondary comparison

`E09-01 − E07`

Serve esclusivamente a rispondere alla domanda strategica:

> l'ablazione del livestock consente alla configurazione da 40 tile di recuperare o superare la performance della configurazione E07 da 24 tile?

Questo confronto non deve sostituire E08 nel test dell'ipotesi.

---

# Criterio decisionale corretto

Rimuovi i criteri che usano E07 come baseline causale.

Non usare soglie arbitrarie come unica regola decisionale.

Il risultato deve essere interpretato principalmente attraverso:

- paired delta E09-01 vs E08;
- consistenza del segno del delta;
- ampiezza economica del miglioramento/peggioramento;
- distribuzione per opponent;
- eventuali outlier;
- completion/disqualification;
- cambiamento di movement share;
- cambiamento di `plant_pending`;
- capitale liberato;
- eventuale aumento della produzione colturale.

Prevedi tre conclusioni:

### A — Livestock negativo nella configurazione E08

E09-01 migliora in modo consistente rispetto a E08.

Interpretazione:

> Il sottosistema livestock contribuisce negativamente alla configurazione produttiva da 40 tile.

Se E09-01 raggiunge o supera anche E07, annotare inoltre:

> La regressione osservata in E08 non era necessariamente causata dal footprint da 40 tile in sé; il carico livestock può essere stato un fattore determinante nell'impedire lo sfruttamento della maggiore scala produttiva.

### B — Livestock positivo nella configurazione E08

E09-01 peggiora in modo consistente rispetto a E08.

Interpretazione:

> Nonostante il saldo diretto negativo calcolato, il livestock fornisce benefici indiretti sufficienti a contribuire positivamente alla performance complessiva.

### C — Effetto marginale o inconclusivo

E09-01 produce delta piccoli, instabili o fortemente dipendenti dall'opponent.

Interpretazione:

> Il livestock non può essere identificato come causa dominante della regressione E08 con l'evidenza disponibile.

---

# Audit già valido

Non rifare inutilmente l'intero audit.

Mantieni, previa verifica, i risultati già individuati:

- acquisto COW/SHEEP;
- pasture construction;
- placement;
- feeding;
- wheat feed buffer;
- harvest livestock;
- milk/wool handling;
- sales;
- capitale assorbito;
- movimento;
- utilizzo tile.

Mantieni anche il saldo diretto stimato:

> Livestock cost: **$4,426.67**  
> Livestock revenue: **$449.33**  
> Net direct balance: **-$3,977.34**

ma specifica che:

> il saldo diretto non dimostra da solo l'effetto causale complessivo del livestock; E09-01 serve precisamente a misurare anche gli effetti indiretti.

---

# Verifica della footprint

Controlla nel codice E08 la definizione esatta della footprint da 40 tile.

La revisione deve documentare chiaramente quali tile fanno parte della configurazione E08.

Quando il livestock viene rimosso:

- non ridurre il numero totale di tile previste da E08;
- non modificare la strategia di espansione;
- non introdurre una nuova footprint;
- le tile precedentemente interessate dal livestock devono essere gestite secondo il comportamento naturale della strategia E08 priva del ramo livestock.

Se per ottenere questo risultato saranno necessarie decisioni implementative non banali, documentarle nelle **Questioni aperte** senza implementarle.

---

# BUILD proposto

Aggiorna il piano BUILD affinché specifichi:

1. partire dalla configurazione E08;
2. creare una variante E09-01;
3. eliminare esclusivamente il comportamento livestock attivo;
4. mantenere footprint 40 tile;
5. mantenere invariati gli altri sottosistemi;
6. aggiungere test specifici che provino:
   - nessun acquisto animale;
   - nessun pasture build;
   - nessun feed;
   - nessun livestock harvest/placement;
   - nessuna riserva Wheat per feed;
   - nessuna vendita Milk/Wool generata dall'agente;
7. preservare le altre action policy E08;
8. predisporre logging necessario al paired VERIFY.

Non implementare questi punti in questa fase.

---

# VERIFY proposto

Il VERIFY futuro dovrà confrontare direttamente:

`E08 vs E09-01`

su **30 episodi paired** o sulla configurazione equivalente già utilizzata da E08.

Registrare almeno:

### Performance
- Final Money per episodio
- Mean
- Median
- Sample Std Dev
- paired delta
- mean paired delta
- median paired delta
- paired W/D/L

### Robustezza
- Completion Rate
- Disqualification Rate
- breakdown per opponent

### Meccanismo
- Worker Movement Share
- `plant_pending`
- tile productive utilization
- capitale speso in livestock
- ricavi livestock
- Wheat riservato/consumato per feed
- eventuali metriche già disponibili su idle/actions

Solo dopo il confronto primario E08/E09-01 aggiungere il riferimento E07.

---

# Aggiornamento PROJECT_STATE / NEW_SESSION

Correggi gli eventuali riferimenti che suggeriscono:

- E07 come baseline primaria di E09-01;
- footprint 24 tile per E09-01.

Lo stato corretto deve essere sintetizzabile come:

> E09-01 DEFINE revised: controlled livestock ablation from E08. Primary comparison is E08 40t Livestock ON vs E09-01 40t Livestock OFF. E07 remains a secondary historical reference.

Mantieni lo stato:

> **DEFINE COMPLETED / READY FOR BUILD**

solo se, dopo la correzione, non restano ambiguità implementative bloccanti.

---

# Vincoli

Durante questa revisione:

- NON modificare codice produttivo;
- NON modificare `src/agricola/agent.py`;
- NON creare la strategia E09;
- NON creare runner E09;
- NON eseguire benchmark;
- NON costruire submission;
- NON accedere a Kaggle;
- NON aprire browser;
- NON fare commit;
- NON fare push;
- NON creare tag.

Sono consentite solo:

- ispezione read-only;
- verifica dei dati;
- modifica della documentazione DEFINE/stato.

---

# Output finale richiesto

Al termine restituisci:

## 1. Correzione effettuata
Conferma esplicita:

> **Primary baseline = E08, 40 tile, Livestock ON**

e:

> **E09-01 treatment = 40 tile, Livestock OFF**

## 2. Ruolo di E07
Conferma che E07 è stato mantenuto esclusivamente come secondary historical reference.

## 3. Disegno VERIFY aggiornato
Descrivi in poche righe il paired comparison E08/E09-01.

## 4. File modificati
Elenca esclusivamente i file documentali modificati.

## 5. Questioni aperte
Riporta eventuali ambiguità residue.

## 6. Raccomandazione finale

Concludi con:

**READY FOR E09-01 BUILD**

oppure

**NOT READY FOR E09-01 BUILD**

---

# Principio metodologico finale

La catena sperimentale deve restare leggibile:

```text
E07: 24 tile + Livestock ON
        |
        | Productive Scale
        v
E08: 40 tile + Livestock ON
        |
        | Livestock Ablation
        v
E09-01: 40 tile + Livestock OFF
```

E09-01 deve isolare **il livestock**, non tornare alla configurazione E07.

La domanda da preservare è:

> **Se togliamo il livestock da E08 e non cambiamo nient'altro, il footprint da 40 tile torna a produrre valore?**
