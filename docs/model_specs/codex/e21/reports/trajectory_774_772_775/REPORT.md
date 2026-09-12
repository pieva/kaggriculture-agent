# Traiettorie 774 / 772 / 775

La 774 è una ricostruzione moderna persistente: non è il vecchio eseguibile perduto. Il ramo superstite non attiva il reclaim: resta in RECOVERY e chiude 775, zero rollback.


| Regione | Fase | Distanza da 772 | Distanza da 775 | Più vicina |
|---|---|---:|---:|---|
| Q0 | D1–11 | 0.0062 | 0.0000 | 775 |
| Q0 | D12–19 | 0.4301 | 0.1259 | 775 |
| Q0 | D1–19 | 0.1019 | 0.0327 | 775 |
| Q1 | D1–11 | 0.0000 | 0.0000 | pari |
| Q1 | D12–19 | 0.3891 | 0.2452 | 775 |
| Q1 | D1–19 | 0.0654 | 0.0289 | 775 |

La casella (4,7) ospita una pecora in 14/14 replay E18 verificati. Le transizioni della casella, incluse costruzione e collocazione, sono riportate nei dati. L’oca è contata tra gli animali.

Un solo seed esposto 180911301; ruolo 0 per tutte le curve. 774 e 772 affrontano E18; E18 775 affronta E20.2. Il diverso avversario e i negozi endogeni limitano il confronto a una descrizione, non a un effetto causale o ranking.

22 KPI standard. Nei quadranti la cassa non è attribuita; persone indica presenza al checkpoint, MOVE è attribuito al quadrante di partenza. WATER/FEED/CARE sono esecuzioni verificate riapplicando i batch registrati; le somme Q0–Q3 coincidono con tutti i KPI globali non monetari in 90 giornate-modello. Checkpoint 24×D−1: prima dell’ultimo batch per D1–29, terminale per D30. La distanza usa il divario assoluto medio normalizzato per escursione di ciascun KPI, omette le costanti e pesa ugualmente i KPI; è una misura descrittiva scelta dopo la run.

[{"reference": "772 · E20.2", "first_action_step": 255, "day": 11, "hour": 15}, {"reference": "775 · E18", "first_action_step": 266, "day": 12, "hour": 2}]

[Report con grafici](REPORT.html)

## Interpretazione verificata

D1–D11: Q0 identica alla 775; Q1 identica a entrambe. D12–D19: complessivamente più vicina alla 775 in entrambi i quadranti. L’apertura coincide per costruzione, non è prova di superiorità.

Il target ospita una pecora in 14/14 replay. La 774 ha 18 animali a D12, poi 19 da D13 dopo la collocazione di una pecora nel pascolo prima vuoto (6,3). Acquisti invariati rispetto a E18: 8 mucche, 11 pecore, 1 oca. Non è una riduzione persistente degli animali.

Prima run: reclaim mai attivato, RECOVERY e zero rollback, finale 775. Seconda: envelope persistente D12 con routing ereditato E20v39 ridotto a un target, senza rollback né bypass terminale, cap 18/19. È una ricostruzione moderna, non la variante storica esatta e non E21 biologica.
