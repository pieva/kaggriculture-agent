# E20.3: controllo diagnostico a negozi invariati

**SOLO DIAGNOSI SINTETICA — NON VALIDO PER SUBMISSION.** Nessuna modifica sul disco al motore installato. Nel processo diagnostico il calendario dei negozi del controllo E20.2 viene ripristinato dopo ogni refresh; tutte le azioni e le reazioni dell'avversario restano libere. Le policy ricevono solo la normale osservazione corrente.

Due controlli completi riproducono esattamente le partite originali. Tutte le sei partite hanno 719 chiamate per agente, zero errori core E20 e prefisso identico fino a D11.

| Seed | Ruolo | Delta cassa con negozi ufficiali endogeni | Delta a negozi invariati |
|---|---:|---:|---:|
| 180911301 | 0 | -13895 | -294 |
| 180911301 | 1 | -13895 | -294 |
| 180911303 | 0 | -2264 | -263 |
| 180911303 | 1 | +4 | -604 |

Il grande calo del seed 301 non misura il solo rendimento del mix animale: il controllo e la variante ricevono negozi diversi. Il confronto sintetico elimina questa variazione della domanda; non è una nuova misura del risultato Kaggle né rende il campione più indipendente. La cassa della variante resta inferiore in tutti i casi diagnostici. Mix 8/8 non adottato.

[Risultati](RESULT.json) · [Protocollo](../../E20_3_FIXED_TOWN_PROTOCOL.json) · [Esiti sul motore invariato](../e20_3_mix_development/REPORT.md)
