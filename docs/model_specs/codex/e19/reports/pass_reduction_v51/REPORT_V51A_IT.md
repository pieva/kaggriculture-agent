# V51 — percorsi completi impegnati al giorno 29

Stato: **REJECTED**. Confronto con V49F congelata.

La modifica inserisce direttamente nel controllore i percorsi verificati per FEED, CARE, WATER e HARVEST. I prelievi sono esatti e condivisi; il lavoro attivo riserva tutte le proprie destinazioni. Il rientro viene incluso quando richiesto dalla policy. Le attività facoltative restano al controllore ereditato dopo queste assegnazioni.

| Seed | Posto | Δ cash | Δ PASS | Δ MOVE | Δ FEED |
|---|---:|---:|---:|---:|---:|
| 180903001 | 0 | -816 | -62 | -41 | +0 |
| 180903002 | 0 | -497 | -62 | -41 | +0 |
| 180903003 | 0 | -1153 | -23 | -81 | +0 |

Medie delle differenze:

| Metrica | Δ medio |
|---|---:|
| cash | -822.0000 |
| pass_count | -49.0000 |
| share | -0.4213 |
| slots | -132.0000 |
| move | -54.3333 |
| hire_cash | -356.0000 |
| FEED | +0.0000 |
| CARE | +0.0000 |
| WATER | -16.3333 |
| HARVEST | +0.3333 |
| losses | +0.0000 |
| escapes | +0.0000 |

Criteri:

- complete: PASS
- pass_absolute: PASS
- pass_share: PASS
- move: PASS
- cash_mean: FAIL
- cash_cases: PASS
- losses: PASS
- escapes: PASS
- services: PASS
- obligations: PASS

## Verifiche e limiti

3 simulazioni complete sui seed di sviluppo già esposti. Azioni D1–D28 identiche alla baseline in tutti i casi. V48, V49F e V50: bundle e sorgenti verificati contro i manifest congelati.

Runtime diagnostico con actTimeout=120: non è una certificazione del runtime standard. Nessuna submission. I seed nuovi non sono stati usati.

[Risultati e gate](summary_v51a.json) · [Integrità](integrity.json) · [Protocollo](PROTOCOL_IT.md)
