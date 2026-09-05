# E18.22 — Diagnosi rifiuti crop

Seed `180903001`, entrambi i seat, comportamento E18.22 invariato.

| Causa | Eventi unici sui due seat |
|---|---:|
| `HARVEST:TILE_EMPTY` | 65 |
| `HARVEST:TILE_WEED` | 15 |
| `PLANT:TILE_LOCKED` | 22 |

Gli eventi completi conservano giorno, turno, worker, posizione, argomenti e
snapshot della tile per selezionare l'ablation E18.23 senza confondere cause.
