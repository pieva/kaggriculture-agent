# E23 — delta evolutivi rispetto alle due E22

Confronto descrittivo di replay rappresentativi. E23 indica ricette candidate osservate nelle submission 56222223 e 56223630, non bundle implementati. Coordinate zero-based; giorni e ore one-based. Nessuna stima causale di guadagno.

E22.1 usa la versione Q2 Grano 56228842. La traiettoria E22.2 proviene dal parent fix 56228129: la versione corrente 56231638 coincide fino a D27 e aggiunge la successione Q2 Grano a D28–30. I delta tardivi del parent riportati sotto vanno interpretati tenendo conto di questa modifica già acquisita.

## E22.1 → E23_geese8

Replay: 108891785 → 108922213.

| Casella | Animale E22, collocamento | Animale candidato, collocamento |
|---|---|---|

### Colture ai checkpoint

| Giorno | Caselle differenti | Conteggi E22 | Conteggi candidato |
|---|---:|---|---|
| 12 | 0 | {'WHEAT': 21, 'STRAWBERRY': 33} | {'WHEAT': 21, 'STRAWBERRY': 33} |
| 20 | 0 | {'WHEAT': 25, 'STRAWBERRY': 33} | {'WHEAT': 25, 'STRAWBERRY': 33} |
| 22 | 0 | {'WHEAT': 30, 'STRAWBERRY': 28} | {'WHEAT': 30, 'STRAWBERRY': 28} |
| 25 | 0 | {'WHEAT': 37, 'CARROT': 4, 'STRAWBERRY': 17} | {'WHEAT': 37, 'CARROT': 4, 'STRAWBERRY': 17} |
| 28 | 2 | {'CARROT': 26, 'WHEAT': 19, 'STRAWBERRY': 5} | {'CARROT': 26, 'WHEAT': 18, 'STRAWBERRY': 4} |
| 29 | 1 | {'CARROT': 13, 'WHEAT': 11} | {'CARROT': 13, 'WHEAT': 10} |
| 30 | 0 | {} | {} |

### Comandi richiesti sulle caselle animali

Sono richieste, non conteggi di servizi riusciti.

| Specie/servizio | E22 | Candidato |
|---|---:|---:|
| COW CARE | 217 | 211 |
| COW COLLECT_FERTILIZER | 195 | 200 |
| COW FEED | 182 | 155 |
| COW HARVEST | 74 | 73 |
| GOOSE CARE | 55 | 53 |
| GOOSE COLLECT_FERTILIZER | 44 | 45 |
| GOOSE FEED | 52 | 52 |
| GOOSE HARVEST | 27 | 28 |
| SHEEP CARE | 142 | 141 |
| SHEEP COLLECT_FERTILIZER | 131 | 132 |
| SHEEP FEED | 133 | 122 |
| SHEEP HARVEST | 39 | 39 |

Organico ai checkpoint differente (giorno, E22, candidato): [(20, 10, 11), (23, 10, 11), (24, 10, 12), (25, 10, 11), (26, 10, 11), (27, 10, 11), (28, 10, 11)].

## E22.1 → E23_geese9

Replay: 108891785 → 108922490.

| Casella | Animale E22, collocamento | Animale candidato, collocamento |
|---|---|---|
| (6, 2) | SHEEP D10 H14 | COW D10 H14 |

### Colture ai checkpoint

| Giorno | Caselle differenti | Conteggi E22 | Conteggi candidato |
|---|---:|---|---|
| 12 | 0 | {'WHEAT': 21, 'STRAWBERRY': 33} | {'WHEAT': 21, 'STRAWBERRY': 33} |
| 20 | 0 | {'WHEAT': 25, 'STRAWBERRY': 33} | {'WHEAT': 25, 'STRAWBERRY': 33} |
| 22 | 0 | {'WHEAT': 30, 'STRAWBERRY': 28} | {'WHEAT': 30, 'STRAWBERRY': 28} |
| 25 | 0 | {'WHEAT': 37, 'CARROT': 4, 'STRAWBERRY': 17} | {'WHEAT': 37, 'CARROT': 4, 'STRAWBERRY': 17} |
| 28 | 2 | {'CARROT': 26, 'WHEAT': 19, 'STRAWBERRY': 5} | {'CARROT': 26, 'WHEAT': 18, 'STRAWBERRY': 4} |
| 29 | 1 | {'CARROT': 13, 'WHEAT': 11} | {'CARROT': 13, 'WHEAT': 10} |
| 30 | 0 | {} | {} |

### Comandi richiesti sulle caselle animali

Sono richieste, non conteggi di servizi riusciti.

| Specie/servizio | E22 | Candidato |
|---|---:|---:|
| COW CARE | 217 | 231 |
| COW COLLECT_FERTILIZER | 195 | 219 |
| COW FEED | 182 | 165 |
| COW HARVEST | 74 | 78 |
| GOOSE CARE | 55 | 53 |
| GOOSE COLLECT_FERTILIZER | 44 | 43 |
| GOOSE FEED | 52 | 52 |
| GOOSE HARVEST | 27 | 30 |
| SHEEP CARE | 142 | 121 |
| SHEEP COLLECT_FERTILIZER | 131 | 113 |
| SHEEP FEED | 133 | 82 |
| SHEEP HARVEST | 39 | 34 |

Organico ai checkpoint differente (giorno, E22, candidato): [(20, 10, 11), (22, 11, 12), (23, 10, 11), (24, 10, 11), (25, 10, 11), (26, 10, 11), (27, 10, 11), (28, 10, 11)].

## E22.2_parent → E23_sheep

Replay: 108891966 → 108915255.

| Casella | Animale E22, collocamento | Animale candidato, collocamento |
|---|---|---|
| (2, 3) | SHEEP D12 H12 | SHEEP D12 H7 |
| (3, 2) | SHEEP D11 H20 | SHEEP D11 H19 |
| (4, 1) | SHEEP D11 H21 | SHEEP D11 H20 |
| (5, 2) | COW D8 H15 | COW D8 H16 |
| (5, 3) | COW D7 H13 | SHEEP D7 H13 |
| (5, 4) | COW D7 H12 | SHEEP D7 H12 |
| (6, 2) | SHEEP D10 H14 | SHEEP D10 H7 |
| (6, 3) | SHEEP D9 H22 | SHEEP D9 H10 |
| (7, 4) | SHEEP D9 H10 | SHEEP D9 H14 |

### Colture ai checkpoint

| Giorno | Caselle differenti | Conteggi E22 | Conteggi candidato |
|---|---:|---|---|
| 12 | 1 | {'WHEAT': 21, 'STRAWBERRY': 33} | {'STRAWBERRY': 33, 'WHEAT': 20} |
| 20 | 0 | {'WHEAT': 25, 'STRAWBERRY': 33} | {'WHEAT': 25, 'STRAWBERRY': 33} |
| 22 | 0 | {'WHEAT': 30, 'STRAWBERRY': 28} | {'WHEAT': 30, 'STRAWBERRY': 28} |
| 25 | 4 | {'WHEAT': 37, 'CARROT': 4, 'STRAWBERRY': 17} | {'WHEAT': 41, 'STRAWBERRY': 17} |
| 28 | 1 | {'CARROT': 26, 'WHEAT': 18, 'STRAWBERRY': 4} | {'CARROT': 27, 'WHEAT': 17, 'STRAWBERRY': 4} |
| 29 | 1 | {'CARROT': 13, 'WHEAT': 10} | {'CARROT': 14, 'WHEAT': 9} |
| 30 | 0 | {} | {} |

### Comandi richiesti sulle caselle animali

Sono richieste, non conteggi di servizi riusciti.

| Specie/servizio | E22 | Candidato |
|---|---:|---:|
| COW CARE | 198 | 155 |
| COW COLLECT_FERTILIZER | 195 | 152 |
| COW FEED | 186 | 120 |
| COW HARVEST | 72 | 57 |
| SHEEP CARE | 195 | 242 |
| SHEEP COLLECT_FERTILIZER | 177 | 225 |
| SHEEP FEED | 186 | 214 |
| SHEEP HARVEST | 54 | 70 |

Organico ai checkpoint differente (giorno, E22, candidato): [(7, 7, 8), (8, 7, 8), (9, 8, 9), (10, 8, 9), (12, 10, 11), (14, 9, 10), (15, 9, 10), (16, 10, 11), (19, 11, 12), (20, 10, 11), (21, 11, 12), (23, 10, 11), (24, 10, 12), (25, 10, 12), (26, 10, 12), (27, 10, 11), (28, 10, 12)].

## E22.2_parent → E23_sheep_D8

Replay: 108891966 → 108921530.

| Casella | Animale E22, collocamento | Animale candidato, collocamento |
|---|---|---|
| (2, 3) | SHEEP D12 H12 | SHEEP D12 H7 |
| (5, 2) | COW D8 H15 | SHEEP D8 H16 |
| (6, 2) | SHEEP D10 H14 | SHEEP D10 H8 |
| (6, 3) | SHEEP D9 H22 | SHEEP D9 H10 |
| (6, 4) | COW D8 H10 | SHEEP D8 H10 |
| (7, 4) | SHEEP D9 H10 | SHEEP D9 H14 |

### Colture ai checkpoint

| Giorno | Caselle differenti | Conteggi E22 | Conteggi candidato |
|---|---:|---|---|
| 12 | 1 | {'WHEAT': 21, 'STRAWBERRY': 33} | {'STRAWBERRY': 33, 'WHEAT': 20} |
| 20 | 0 | {'WHEAT': 25, 'STRAWBERRY': 33} | {'WHEAT': 25, 'STRAWBERRY': 33} |
| 22 | 0 | {'WHEAT': 30, 'STRAWBERRY': 28} | {'WHEAT': 30, 'STRAWBERRY': 28} |
| 25 | 0 | {'WHEAT': 37, 'CARROT': 4, 'STRAWBERRY': 17} | {'WHEAT': 37, 'CARROT': 4, 'STRAWBERRY': 17} |
| 28 | 0 | {'CARROT': 26, 'WHEAT': 18, 'STRAWBERRY': 4} | {'CARROT': 26, 'WHEAT': 18, 'STRAWBERRY': 4} |
| 29 | 0 | {'CARROT': 13, 'WHEAT': 10} | {'CARROT': 13, 'WHEAT': 10} |
| 30 | 0 | {} | {} |

### Comandi richiesti sulle caselle animali

Sono richieste, non conteggi di servizi riusciti.

| Specie/servizio | E22 | Candidato |
|---|---:|---:|
| COW CARE | 198 | 160 |
| COW COLLECT_FERTILIZER | 195 | 155 |
| COW FEED | 186 | 140 |
| COW HARVEST | 72 | 59 |
| SHEEP CARE | 195 | 237 |
| SHEEP COLLECT_FERTILIZER | 177 | 227 |
| SHEEP FEED | 186 | 207 |
| SHEEP HARVEST | 54 | 80 |

Organico ai checkpoint differente (giorno, E22, candidato): [(8, 7, 8), (9, 8, 9), (10, 8, 9), (12, 10, 11), (14, 9, 10), (15, 9, 10), (16, 10, 11), (17, 11, 12), (19, 11, 12), (20, 10, 11), (21, 11, 12), (23, 10, 11), (24, 10, 11), (25, 10, 11), (26, 10, 12), (27, 10, 11), (28, 10, 11)].
