# Diagnosi integrata della transizione dopo D11

La diagnosi precedente sul solo rinnovo del grano era incompleta. Occorre distinguere espansione iniziale, mantenimento delle rotazioni e conversione delle colture nel finale. Nessuna nuova politica promossa.

## Colture presenti: mediana dei 14 casi assistita e dei 5 Top770-001

| Giorno | Coltura | Assistita | Top770-001 |
|---|---|---:|---:|
| D12 | WHEAT | 13 | 20 |
| D12 | STRAWBERRY | 21 | 38 |
| D12 | CARROT | 0 | 0 |
| D12 | TOMATO | 0 | 0 |
| D12 | MELON | 0 | 0 |
| D13 | WHEAT | 12 | 24 |
| D13 | STRAWBERRY | 23 | 38 |
| D13 | CARROT | 0 | 0 |
| D13 | TOMATO | 3 | 0 |
| D13 | MELON | 3 | 0 |
| D15 | WHEAT | 0 | 23 |
| D15 | STRAWBERRY | 26 | 38 |
| D15 | CARROT | 0 | 0 |
| D15 | TOMATO | 5 | 0 |
| D15 | MELON | 3 | 0 |
| D20 | WHEAT | 0 | 23 |
| D20 | STRAWBERRY | 26 | 38 |
| D20 | CARROT | 0 | 0 |
| D20 | TOMATO | 5 | 0 |
| D20 | MELON | 3 | 0 |
| D25 | WHEAT | 10 | 39 |
| D25 | STRAWBERRY | 10 | 22 |
| D25 | CARROT | 0 | 0 |
| D25 | TOMATO | 0 | 0 |
| D25 | MELON | 0 | 0 |
| D28 | WHEAT | 24 | 6 |
| D28 | STRAWBERRY | 5 | 15 |
| D28 | CARROT | 0 | 38 |
| D28 | TOMATO | 0 | 0 |
| D28 | MELON | 0 | 0 |

Le mediane marginali non sono additive: non ricostruire la mediana della superficie totale sommando questa tabella.

## Semine eseguite: media per partita

| Finestra | Coltura | Assistita | Top770-001 |
|---|---|---:|---:|
| D12–D15 | WHEAT | 0.00 | 31.00 |
| D12–D15 | STRAWBERRY | 3.71 | 17.00 |
| D12–D15 | CARROT | 0.00 | 0.00 |
| D12–D15 | TOMATO | 5.00 | 0.00 |
| D12–D15 | MELON | 3.00 | 0.00 |
| D25–D29 | WHEAT | 23.86 | 26.40 |
| D25–D29 | STRAWBERRY | 0.00 | 0.00 |
| D25–D29 | CARROT | 7.57 | 27.60 |
| D25–D29 | TOMATO | 0.00 | 0.00 |
| D25–D29 | MELON | 0.00 | 0.00 |

## Evidenza dal controller

Ricostruito il caso seed180903001 seat0 della base, con parità dei KPI e del ledger verificata. A D13 H1 la cassa libera è 17.244; il controller propone 27 destinazioni per ciascuna delle cinque colture. Il grano ha valore stimato positivo (130), ma inferiore a melone (429), fragola (240) e pomodoro (194). Questi sono valori interni, non profitti realizzati.

La graduatoria usa il guadagno del singolo ciclo diviso per le azioni del percorso iniziale. Non confronta esplicitamente i ricavi, i tempi e il lavoro di successioni colturali alternative. Le semine devono inoltre superare un certificato che include servizi facoltativi: i contatori di rifiuto crescono durante D12–D15. Sono rifiuti di combinazioni candidato-lavoratore, non conteggi di caselle perse.

La causa non è un divieto di seminare grano, né assenza di cassa nel caso osservato. Le criticità identificate sono selezione delle colture e capacità di eseguire le missioni. Il peso causale dei singoli componenti richiede prove separate; la traiettoria storica Top non basta a dimostrare che copiare il mix produca lo stesso profitto nel mercato locale.

## Criteri per la prossima revisione

Valutare insieme espansione D12–D15 di tutte le colture, continuità D16–D24 e conversioni D25–D30. Confrontare guadagno per tempo di occupazione e lavoro dell’intero ciclo, comprese le successive semine, mantenendo la fattibilità di alimentazione e irrigazione. Verificare la cassa relativa contro V4D nelle stesse partite e tutte le perdite biologiche. Non usare il solo numero di caselle di grano come criterio di successo.

## Prova del certificato sulle missioni economiche

Sei casi conclusi, prefisso D1–D11 invariato. Risultati: {"cases": 6, "cash": 57706.333333333336, "reference": 108536.0, "crop_starvation": 0, "animal_escapes": 0, "errors": 0, "incomplete": 0, "wheat": {"12": 13.0, "13": 13.0, "15": 11.0, "20": 4.0, "28": 25.0}, "relative_pct": -46.832080292867495}. La prova non è promossa: non riproduce l’espansione iniziale e peggiora il confronto economico. Un primo prototipo con errore di indice è esplicitamente invalidato nella cartella productive_continuity_20260907; i risultati corretti sono solo nella cartella wheat_reserved_20260907.
