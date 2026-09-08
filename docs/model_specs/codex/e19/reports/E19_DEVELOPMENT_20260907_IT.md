# E19.1 parametrica 662 — sviluppo 2026-09-07

L'istruzione «Sviluppa la E19 allora» autorizza l'avvio immediato, superando
il prerequisito E18. La pubblicazione E19 quando soddisfacente era già
autorizzata. E18 V24 non viene retroattivamente dichiarata definitiva.

## V1: solo capacità locale 7 → 6

Core identico al bundle E18 V24, profilo invariato salvo K=6. P=14,
9 COW/5 SHEEP, massimo 12 manovali, tre quadranti. Bootstrap limitato al
primo raccolto osservato. Nessun calendario o script per quadrante.

28 development: 662 popolata 28/28, zero perdite biologiche/errori contabili,
cassa media 65.538,57 contro 61.579,00 della 770 V24 (+6,430%). Sette missioni
terminali residue in cinque partite: V1 non pubblicata. Parità sorgente,
bundle e loader Kaggle superata nei quattro casi previsti.

## V2: prenotazione completa dei prelievi

Il trace del seed 180903005/seat 0 mostra al D30 H20 due missioni FEED
ammesse su grano apparentemente libero. I prelievi di altre missioni
esauriscono prima il magazzino, causando due batch di attesa; i percorsi
non terminano. `_requirements` riservava il consumo residuo, ignorando
il surplus dei PICKUP ancora pendenti.

La correzione riserva per ogni merce il massimo tra fabbisogno netto e
quantità dei prelievi pendenti. Dopo il prelievo osservato la prenotazione
si libera e la scorta passa all'inventario del lavoratore. Il test di
regressione verifica sia la prenotazione iniziale sia il suo rilascio.
È una modifica generale del core: nessuna condizione sulla topologia.

I due casi problematici 180903003/0 e 180903005/0 contro E18.16 ora
chiudono tutte le missioni e conservano 662 piena senza perdite. Le scelte
economiche cambiano; la verifica completa e il controllo 770 sul medesimo
core V2 sono necessari prima della decisione. Suite core/E19: 89 test passati.

Bundle V1/V2 e manifest restano separati e immutabili. Sorgenti V2 archiviati
in `artifacts/source`. I risultati in sviluppo non sono benchmark esterni
né dimostrano equivalenza ai Top770. I confronti usano le stesse coppie
seed/seat/avversario, senza assumere identiche traiettorie casuali dei mercati.

## Decisione finale V2

Entrambi i gate completi contengono 28 partite: 662 e 770 raggiunte e popolate
28/28; zero perdite biologiche, errori, discrepanze contabili e missioni
terminali residue. Cassa E19 68.348,71; controllo 770 sullo stesso core
63.426,64: **+7,760%**. Rispetto alla vecchia 770 V24: +10,994%; rispetto
alla storica E18.31: **−13,208%**. Quest'ultimo divario resta aperto.

Parità V2: 2.876 azioni identiche, quattro casi, loader Kaggle verificato.
Suite condivisa 86 test più quattro E19 passati (90 complessivi, verificati
nei run della suite comune e dell'estensione). Tempo massimo locale 2,284 s;
consumo massimo misurato dell'overage per partita 2,028 s su 60 disponibili.
Queste misure dipendono dalla macchina; la prova sulla piattaforma resta distinta.

| Giorno | Cassa E19 media | Cassa 770 media | COW E19 mediana | Colture E19 medie |
|---|---:|---:|---:|---:|
| 5 | 772,43 | 772,43 | 2 | 6 |
| 10 | 1.909,07 | 1.733,43 | 7 | 30,14 |
| 15 | 7.893,61 | 7.090,54 | 9 | 45,61 |
| 20 | 29.422,82 | 26.823,96 | 9 | 33,86 |
| 30 | 68.348,71 | 63.426,64 | 9 | 9,68 |

PASS D5–D10 medio 359,07 contro 345 del controllo: la maggiore cassa non
dimostra miglioramento uniforme dei KPI. Servizi giornalieri, cassa,
animali, colture e lavoratori completi sono nei JSON `E19_V2_VS_*`.

V2 è idonea come **prima baseline E19 per benchmark esterni**, non come
promozione sopra i Top o l'incumbent. Decisione tracciata in
`artifacts/derived/E19_V2_RELEASE_DECISION_20260907.json`.
File inviato a Kaggle: `submission/submission_codex_e19_1_662_v2.py`.
SHA256 `ba0a4780a0d25bc3535d842f6e40bb1ae9954e5da181b46cea28e62f0b1474bc`.
La ricevuta di pubblicazione è conservata separatamente, per non modificare
retroattivamente gli esiti e i manifest pre-upload.
