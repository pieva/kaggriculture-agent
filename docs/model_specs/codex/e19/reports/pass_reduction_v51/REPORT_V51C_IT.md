# V51 — percorsi completi impegnati al giorno 29

Stato: **LOCAL_CANDIDATE_ONLY**. Confronto con V49F congelata.

La modifica inserisce direttamente nel controllore i percorsi verificati per FEED, CARE, WATER e HARVEST. I prelievi sono esatti e condivisi; il lavoro attivo riserva tutte le proprie destinazioni. Il rientro viene incluso quando richiesto dalla policy. Le attività facoltative restano al controllore ereditato dopo queste assegnazioni.

| Seed | Posto | Δ cash | Δ PASS | Δ MOVE | Δ FEED |
|---|---:|---:|---:|---:|---:|
| 180903001 | 0 | +222 | -65 | -18 | +0 |
| 180903001 | 1 | +222 | -65 | -18 | +0 |
| 180903002 | 0 | +298 | -65 | -18 | +0 |
| 180903002 | 1 | +298 | -65 | -18 | +0 |
| 180903003 | 0 | +515 | -29 | -67 | +0 |
| 180903003 | 1 | +515 | -29 | -67 | +0 |

Medie delle differenze:

| Metrica | Δ medio |
|---|---:|
| cash | +345.0000 |
| pass_count | -53.0000 |
| share | -0.5388 |
| slots | -100.6667 |
| move | -34.3333 |
| hire_cash | -329.0000 |
| FEED | +0.0000 |
| CARE | +0.0000 |
| WATER | +0.0000 |
| HARVEST | +0.3333 |
| losses | +0.0000 |
| escapes | +0.0000 |

Criteri:

- complete: PASS
- pass_absolute: PASS
- pass_share: PASS
- move: PASS
- cash_mean: PASS
- cash_cases: PASS
- losses: PASS
- escapes: PASS
- services: PASS
- obligations: PASS

## Verifiche e limiti

6 simulazioni complete sui seed di sviluppo già esposti. Azioni D1–D28 identiche alla baseline in tutti i casi. V48, V49F e V50: bundle e sorgenti verificati contro i manifest congelati.

Consultare gli audit di validazione.

[Risultati e gate](summary_v51a.json) · [Integrità](integrity.json) · [Protocollo](PROTOCOL_IT.md)
