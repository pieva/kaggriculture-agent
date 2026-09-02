# E17 — RQ3 pre-check: timing di Q2 e frontiera D8/D10/D11

- **Data:** 2026-09-02
- **Fase:** `DEFINE / E17.0`
- **Gate:** freeze di strategia e parity misurazione già passati; nessuna mutazione di policy
- **Domanda causale:** `RQ3 — Q2 a D10 produce un ciclo utile aggiuntivo?`
- **Stato:** preregistrazione iniziale del passo successivo autorizzato; nessun cambio alla baseline Codex congelata

## 1. Stato della evidenza corrente

Il corpus di 9 replay del benchmark Top-3 mostra tre profili distinti:

- `tetsuya`: Q1 a D7, Q2 a D10, score medio forte, topologia mista e zero fughe derivate;
- `OceanMix`: Q1 a D6, Q2 a D11, routing più efficiente e layout fortemente compatti;
- `Crop Dusta`: Q1 a D5–D6, Q2 a D8–D9, score di leaderboard, ma alto movimento e 31 fughe derivate.

Dal dump aggregato dei replay:

| Player | Q1 day | Q2 day | Score finale medio | Note |
|---|---:|---:|---:|---|
| `tetsuya` | 7 | 10 | ~96.568 | stabile, 0 fughe |
| `OceanMix` | 6 | 11 | ~82.535 | efficient routing, layout compatto |
| `Crop Dusta` | 5–6 | 8–9 | ~91.361 | anticipo massimo, movimento alto, fughe |

L'evidenza non supporta ancora la conclusione che “Q2 più precoce = meglio”. Il vantaggio di Crop Dusta è osservato insieme a:

- più specie coltivate;
- più movimento;
- più rischio di occupazione non serviceable;
- più fughe native/derivate all'EOD;
- più inventario invenduto e più contesa di mercato locale.

## 2. Ipotesi causale da testare

L'ipotesi di lavoro è la seguente:

> `Il beneficio di una Q2 anticipata non è indipendente dalla topologia e dal servicing del bestiame. Il vantaggio di D8/D9 è plausibile solo se la componente spaziale e di feed/care resta serviceable; altrimenti il timing precoce aumenta movimento, fuga e varianza.`

In termini di RQ3:

- `D11` è il punto di riferimento della baseline Codex V9 e della logica di saturazione stabile;
- `D10` è il timing “robusto” condiviso da `tetsuya` e da una routine mista;
- `D8` è il confine frontiera di `Crop Dusta`, ma richiede validazione causale indipendente.

## 3. Esperimento autorizzato e limitato

L'esperimento successivo deve essere rigorosamente monofattoriale:

1. mantenere congelata la baseline `CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY`;
2. introdurre solo un parametro di timing Q2 in un ramo sperimentale dedicato;
3. confrontare, per gli stessi seed e gli stessi avversari, le tre condizioni:
   - `Q2 = D11` (baseline);
   - `Q2 = D10` (timing intermedio);
   - `Q2 = D8` (frontiera aggressiva);
4. congelare tutti gli altri fattori: mix crop, specie animali, lavoro, capital allocation, routing logico, market policy;
5. misurare non solo score finale, ma anche:
   - movimento totale;
   - numero di fughe animali derivati;
   - cash finale;
   - giorno di primo output Q2;
   - occupancy finale e tile non coltivate dedicate ai crop/animali;
   - conteggio di assistenti e massimo hands;
   - ricavi e inventario invenduto.

## 4. Criterio di accettazione

Accettiamo il “timing D8” come plausibilmente utile solo se, rispetto a D10 e D11, produce:

- score mediano superiore o equivalente;
- senza aumento sistematico di fughe derivati;
- senza aumento di move per unità produttiva oltre una soglia credibile;
- senza collasso di cash floor o inventario alla chiusura;
- con topologia Q2 serviceable e non dominata da occupazione dispersa.

Se D8 non soddisfa questi requisiti mantenendo invariato il resto del sistema, la domanda causale va respinta come “timing precoce senza topologia/servicing adeguato”.

## 5. Procedura implementativa consigliata

Poiché il codice di policy non deve essere mutato in-place, la procedura corretta è:

- creare una nuova candidate sperimentale per `RQ3` in un ramo/dir dedicato;
- lasciare la fonte frozen invariata;
- aggiungere un solo parametro di orchestrazione del timing del secondo quadrante;
- usare il ledger come misura obbligatoria di ogni run;
- registrare i risultati in `experiments/e17/artifacts/runs/` e in un report di sintesi con tabella comparativa.

## 6. Conclusione del pre-check

Il passo successivo autorizzato non è “copiare D8”, né “rimpiazzare la baseline con l'archetipo Crop Dusta”.

Il passo successivo autorizzato è: `RQ3 con controllo monofattoriale del timing Q2`.

Questa è la forma di esperimento più vicina al requisito di E17: un solo fattore, un solo meccanismo, uno stato di ledger verificato. Se la frontiera D8 è utile, la causalità dovrà emergere come effetto di timing e non come semplice corrispondenza con il profilo più aggressivo del benchmark.
