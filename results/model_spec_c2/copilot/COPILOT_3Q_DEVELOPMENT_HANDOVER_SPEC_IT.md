# SPECIFICA STRATEGICA ED EVOLUZIONE 3Q PER LO SVILUPPO DI COPILOT
## Sintesi delle Evidenze Sperimentali, Lesson Learned e Linee Guida per il Torneo a 3

> **Destinatario**: Copilot Development Team  
> **Oggetto**: Handover architetturale per lo sviluppo del modello **Copilot C2 3Q (Tri-Quadrant)**  
> **Data**: 2026-09-01  
> **Origine Evidenze**:
> 1. Replay Ufficiale Kaggle Top-1 `104498819` (`keiz` **$158,575.00**);
> 2. Replay Ufficiale Kaggle `104515697` (Diagnosi Dead-Zone Q2);
> 3. Torneo Interno Head-to-Head Antigravity 3Q vs Codex 3Q (**14-0 Sweep**).

---

## 1. L'Evoluzione dei Modelli: Dalle Origini 1Q al 3Q Central Mega-Cluster

L'evoluzione dei controller nel ciclo C2 ha attraversato quattro fasi distinte:

```text
┌───────────────────────────┐     ┌───────────────────────────┐
│   1Q: Compact Q0 (25t)    │ ──> │    2Q: Dual-Q Q0+Q1 (50t) │
│   Cap: ~$57k - $62k       │     │    Cap: ~$87k - $91k      │
│   7 Operai, 6 Animali     │     │    13 Operai, 12 Animali  │
└───────────────────────────┘     └─────────────┬─────────────┘
                                                │
                                                ▼
┌───────────────────────────┐     ┌───────────────────────────┐
│ 3Q Mega-Cluster (75t)     │ <── │ 3Q Naive Mirrored (75t)   │
│ Target: $100k - $150k+    │     │ Problema: Dead-Zone Q2    │
│ 13 Operai, 19-20 Animali  │     │ Cammino lungo -> Erbacce  │
└───────────────────────────┘     └───────────────────────────┘
```

### Le Evidenze Sperimentali Acquisite

1. **Fase 1Q (Compact Q0 - 25 tile)**:
   - *Limiti*: Massima saturazione di Q0 con 7 operai e 6 animali raggiunge un tetto fisiologico di **~\$60,000.00**. Non c'è spazio sufficiente per scalare la mandria o le colture.
2. **Fase 2Q (Dual-Q Q0+Q1 - 50 tile)**:
   - Sblocco di Q1 al Day 6 (\$1,000). Raddoppio delle colture e 12 animali attivi (6 mucche + 6 pecore).
   - Risultati: **\$91,010.42 Lordo**, **\$87,740.00 Picco Netto**, **\$83,272.00 nel Replay 562040596**.
   - *Punto di forza*: Lo specchiamento orizzontale $x \rightarrow 9-x$ posiziona i pascoli di Q1 vicino allo shed `(5,4)`, mantenendo i tempi di cammino bassi.
3. **Fase 3Q Naive (Specchiatura Verticale $y \rightarrow 9-y$ — Errore nel Replay `104515697`)**:
   - Sbloccando Q2 con la semplice specchiatura verticale, le colture sono state spinte ai bordi estremi sud ($y=8,9$), lasciando la zona centrale adiacente al capanno `(4,5)` **completamente vuota (terra nuda)**.
   - *Conseguenza*: I lavoratori perdevano 6-8 passi per raggiungere le colture periferiche, che degeneravano in erbacce (`WEED`), abbassando la resa netta.
4. **Fase 3Q Central Mega-Cluster (Risoluzione Definitiva)**:
   - Ispirata dal vincitore assoluto `keiz` ($158k), tutti i pascoli vengono concentrati nel nucleo $5\times 5$ centrale a distanza Chebyshev $\le 2$ dai capanni (`(4,4)`, `(5,4)`, `(4,5)`).
   - I 7 tile centrali di Q2 vengono saturati con pascoli per Pecore (\$240 per lana a zero passi di cammino).
   - Risultato nel torneo interno contro Codex 3Q: **14 vittorie su 14 match (100% Win Rate)** con un vantaggio medio di **+\$7,751.43**.

---

## 2. I 5 Principi Architetturali Indispensabili per Copilot 3Q

Per sviluppare un modello Copilot 3Q altamente competitivo, è necessario implementare tassativamente questi 5 principi:

### Principio 1: Topologia Spaziale a Distanza Chebyshev $\le 2$
Mai lasciare la zona centrale di Q2 vuota e mai spingere le colture sui bordi remoti.
- **Q0 Pascoli Centrali**: `(3,4), (4,3), (3,3), (2,4), (4,2), (3,2)` (3 Mucche, 3 Pecore)
- **Q1 Pascoli Centrali**: `(6,4), (5,3), (6,3), (7,4), (5,2), (6,2)` (3 Mucche, 3 Pecore)
- **Q2 Pascoli Centrali**: `(3,5), (4,6), (3,6), (4,7), (3,7), (2,5), (2,6)` (7 Pecore adiacenti a `(4,5)`)
- **Q2 Colture Concentriche (8 slot compatti)**: `(2,7), (3,8), (4,8), (1,5), (1,6), (1,7), (0,5), (0,6)`

### Principio 2: Vincolo Salariale Fibonacci a 13 Lavoratori
- La forza lavoro ottimale è **esattamente 13 lavoratori totali (1 Farmer + 12 Hands)**.
- Il costo salariale giornaliero per 12 hands è di **\$376/giorno**.
- **Pericolo da evitare**: Assumere il 14° lavoratore fa scattare il salario a **\$609/giorno**. Nei match a 2 o 3 giocatori, dove la vendita simultanea di meloni fa scendere i prezzi di mercato, un salario di \$609/giorno porta rapidamente alla bancarotta.

### Principio 3: Protezione del Floor Salariale Dinamico
Prima di eseguire ordini di mercato facoltativi (`BUY_LAND`, `BUY_ANIMAL`, `BUY_SEED`), il controller deve verificare che la cassa residua garantisca il pagamento dei salari a fine giornata (ore 23:00):
$$\text{Cash Residua} - \text{Costo Ordine} \ge \text{Salari Giornalieri} + \$50.00$$

### Principio 4: Dinamica Reale delle Fragole (`max_yield: 4`)
- Le Fragole **non sono infinite**: producono esattamente 4 volte (max 4-8 unità per pianta) e poi cessano definitivamente.
- Utilizzare i **Meloni** per i grandi picchi di cassa precoci (Day 10/12) e le **Fragole** per il flusso di cassa costante a metà partita.

### Principio 5: Autoproduzione del Foraggio e Monetizzazione del Concime
- **Grano Autoprodotto**: Coltivare 2-3 tile a grano rapido per produrre foraggio a **\$1.67/unità** invece di acquistarlo a **\$25.00** dal mercato (-93% di costi vivi).
- **Vendita Sistematica del Concime**: Vendere ogni giorno tutto il concime prodotto dagli animali per incassare oltre **+\$14,000.00** di cassa pulita.

---

## 3. Matrice della Forza Lavoro Consigliata per Copilot 3Q (13 Operai)

| ID Operaio | Ruolo Primario | Assegnazione Territoriale | Compito Chiave |
|---|---|---|---|
| **W0 (Farmer)** | Master Logistics & Market | Presidio centrale `(4,4)` / `(5,4)` / `(4,5)` | Vendite beni finiti, acquisti sementi JIT, semine emergenza |
| **W1, W2, W3** | Colture Q0 | Zone colturali Q0 (18 tile) | Irrigazione sincronizzata, raccolta Meloni e Fragole |
| **W4** | Zootecnia Mucche Q0 | 3 Pascoli Mucche Q0 | Mungitura e cura Mucche Q0 |
| **W5** | Zootecnia Pecore Q0 | 3 Pascoli Pecore Q0 | Tosatura (\$240/u) e foraggio Pecore Q0 |
| **W6** | Relief & Concime Q0 | Q0 Pascoli e Colture | Raccolta e stoccaggio letame Q0 |
| **W7, W8, W9** | Colture Q1 | Zone colturali Q1 (17 tile) | Irrigazione e raccolta Q1 |
| **W10** | Zootecnia Mucche Q1 | 3 Pascoli Mucche Q1 | Mungitura e cura Mucche Q1 |
| **W11** | Zootecnia Pecore Q1 | 3 Pascoli Pecore Q1 | Tosatura e foraggio Pecore Q1 |
| **W12** | Relief & Concime Q1 | Q1 Pascoli e Colture | Raccolta letame Q1 e foraggio grano |
| **W13 (Hand 12)**| Zootecnia & Colture Q2 | 7 Pascoli Pecore Q2 + Anello Colture | Tosatura 7 Pecore Q2 (0 passi da `(4,5)`) e cura colture |

---

## 4. Prossimo Step: Il Torneo Triangolare (Antigravity vs Codex vs Copilot)

Con l'adozione di questa specifica da parte di Copilot, sarà possibile avviare il **Torneo a 3 Giocatori**:
- **Setup**: Partite a 2 giocatori con rotazione completa delle coppie (Antigravity vs Copilot, Codex vs Copilot, Antigravity vs Codex) su tutti i semi di test;
- **Obiettivo**: Misurare la robustezza della politica di mercato in presenza di concorrenza agguerrita sui prezzi delle merci.
