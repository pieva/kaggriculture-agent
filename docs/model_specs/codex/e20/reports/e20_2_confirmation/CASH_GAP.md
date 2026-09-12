# Perché E18 ha più o meno cassa di E20.2

Divario medio E18 meno E20.2: +3539.0. Identità contabile verificata in tutti i 14 scontri.

| Componente | Contributo al vantaggio E18 |
|---|---:|
| initial | +0.0 |
| sales | +18290.7 |
| purchase_saving | -14422.4 |
| hire_saving | -329.4 |
| land_saving | +0.0 |
| unit_actions | +0.0 |

| Prodotto | Maggiori ricavi E18 |
|---|---:|
| WHEAT | +8115.6 |
| WOOL | +6407.1 |
| FERTILIZER | +3179.1 |
| MELON | +2125.4 |
| EGG | +1176.4 |
| MILK | +85.0 |
| STRAWBERRY | -646.0 |
| CARROT | -2152.1 |

| Fase | Flusso netto E18 meno E20.2 |
|---|---:|
| D1-11 | +0.0 |
| D12-19 | +2679.7 |
| D20-30 | +859.3 |

La scomposizione quantità/prezzo nel JSON è una identità simmetrica, non una stima controfattuale: cambiare produzione o calendario delle vendite cambia anche il mercato e le azioni avversarie. Se un modello non vende un prodotto, tutto il divario viene attribuito alla componente volume e il prezzo mancante resta nullo.

Scorte terminali, raccolto e venduto sono riportati separatamente; un prodotto rimasto in deposito o sul terreno non contribuisce alla cassa. PASS e servizi sono descrittori operativi e non vengono assunti come causa.

[Dati per seed, ruolo, prodotto e fase](CASH_GAP.json) · [22 KPI](REPORT.html)
