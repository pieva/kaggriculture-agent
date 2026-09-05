# E18.19 — delta interno contro E18.18

## Verdetto

`PASS` sul delta causale del solo layer di
esecuzione. Seed, piano, topologia, composizione target e mercato sono comuni;
il trattamento E18.19 aggiunge ack, retry limitato e recupero dello stato.

| Seat E18.19 | E18.19 | E18.18 | Margine | Topologia | Animali | Backlog |
|---:|---:|---:|---:|---|---|---:|
| 0 | 92554 | 54654 | +37900 | {"Q0": 7, "Q1": 7} | {"COW": 9, "SHEEP": 5} | 26 |
| 1 | 94168 | 55213 | +38955 | {"Q0": 7, "Q1": 7} | {"COW": 9, "SHEEP": 5} | 29 |

Mediana E18.19 `93361.0`, mediana E18.18
`54933.5`, delta `+38427.5`
(`+69.95%`).

Questo PASS dimostra il miglioramento rispetto all'executor E18.18, non la
promozione rispetto all'incumbent E18.16. Fa fede separatamente lo smoke Gate 1
contro E18.16.

## Check

```json
{
  "candidate_exact_770": true,
  "candidate_exact_9_cow_5_sheep": true,
  "candidate_wins_both_seats": true,
  "zero_errors": true
}
```
