# E18.32 — lavoro pronto e domanda produttiva

Decisione successiva del proprietario, 2026-09-06: **controllo provvisorio congelato,
non conforme al nuovo requisito di policy unica per tutti i quadranti**.
La prosecuzione è definita in `MODEL_SPEC_CODEX_E18_33_COMMON_RESOURCE_POLICY_V1.md`.
I risultati sotto sono validi per V9, non per quella nuova policy.

Stato corrente 2026-09-06: **E18.32 DEMAND RELEASE V9 pubblicata come controllo
provvisorio, NON benchmark E19 e non promossa a baseline parametrica**.
Autorizzazione esplicita del proprietario; submission 56056189, Complete,
upload 13:27:24 UTC. Receipt in `artifacts/derived/E18_32_KAGGLE_UPLOAD_RECEIPT_V9_20260906.json`.
Baseline pubblica E18.31 UNIFIED V11 immutabile (submission 56050866).
Il successivo controllo Q0/KPI è in `reports/E18_CLOSEOUT_AND_BOOTSTRAP_20260906_IT.md`.

## Ipotesi preregistrate

L'assegnazione E18.31 aggiunge lavoro solo ai PASS di code giornaliere prefissate.
Il piano E18.28 C conserva organico, orari, date colturali e blackout derivati
dalle precedenti iterazioni, compreso il programma BoostD10. Il nuovo mercato
E18.31 bypassa invece i vecchi override di mercato D11/D13: non confondere
codice presente nell'ereditarietà con codice effettivamente eseguito.

1. CLOCK: conservare l'ordine e le dipendenze materiali, togliere l'ora nominale
   come condizione di rilascio. Terra chiusa e risorse mancanti restano vincoli.
2. FERTILITY: trasformare fertilizzante disponibile in resa incrementale solo
   se il valore della produzione supera il ricavo alternativo della vendita.
   Missione completa, conferma osservata, riserva esclusiva e deadline incluse.
3. COMBINED: combinazione delle due correzioni, senza condizioni su D5/D10/D15,
   avversario, seed, replay o benchmark. Organico/mix invariati nella prima prova.

Non assumere che esistano abbastanza lavori redditizi per tutti i PASS.
Distinguere riduzione di attese, aumento di produzione e dimensionamento della
capacità. Non sostituire PASS con movimento o irrigazione senza valore.

## Verifica

Smoke sul motore ufficiale, poi sette seed di sviluppo 180903001–007, due
posizioni, E18.16 ed E18.2/V4D, confronto con i 28 casi E18.31 congelati.
Top770-001 e Top770-002 già consumati: nessun nuovo tuning sulle loro curve.
Controlli: cassa finale, PASS assoluti e /slot D1–10 e D5–10, azioni produttive,
MOVE, salario, crescita animali, D11–30, zero errori/perdite biologiche/missioni
incomplete, massimo 12 manovali, cap 14 animali, topologia finale 7-7-0.
Stesso seed non significa mercato controfattuale identico: il consumo RNG del
motore dipende anche dall'occupazione delle tile; riportare la variabilità.
Conservare ablation respinte e non dichiarare risolto il problema senza esito.

## Evoluzione implementata — V7

CLOCK, FERTILITY e COMBINED non selezionate: la prima e la terza perdono crop;
fertilità isolata non riduce i PASS iniziali. Sorgenti conservate, non incluse
nel bundle. Le versioni DEMAND intermedie riducono l'organico ma penalizzano
la crescita delle mucche: respinte finché manca il vincolo di consegna ricavi.

V7: `tools/e18_32_demand_routing_controller.py` e
`tools/e18_32_claim_routing_controller.py`. Ricomposizione dei bundle per tile,
domanda degli animali osservati, investimenti finanziabili nella stessa rotta,
deadline di consegna del reddito necessario alla crescita, assunzioni ridotte
solo con certificato e margine, rilascio servizi confermati prima del DROP.
Vincolo 770/cap 14/massimo 12 invariato. Non viene imposto un minimo giornaliero
derivato dal Top: la riduzione rispetto al calendario è ammessa solo quando
fattibile. Il programma agricolo E18.28 C resta controllo e fallback esplicito.

Audit riproducibile dei sei replay pubblici: 4.314 batch identici al controller
E18.31. D5–D10: 77,45% code esaurite, 16,60% attese, 5,95% raccolta fertilizzante
in testa a coda bloccata; condizioni immediate, non stima di reddito recuperabile.
Diagnosi e verifica: `reports/E18_32_PASS_ROOTS_AND_VERIFICATION_20260906_IT.md`.

## Correzione V9 — liquidità della manutenzione

Il gate completo V7 migliora i PASS (-27,01% D1–D10) e la cassa (+0,188%), ma
riduce di uno il FEED D2 e la lana D7. Il solo controllo delle prenotazioni
(V8) non risolve: il fertilizzante destinato a finanziare il cibo torna troppo
tardi al magazzino. V9 vieta la compattazione geometrica quando il nutrimento
già dovuto richiede incassi ancora da consegnare. Regola identica su tutti i
giorni; fallback esplicito, non nuova eccezione D2. V7 e V8 restano evidenze
intermedie e non sono il candidato corrente.

## Esito V9

28/28 safety pass sul motore originale e 71 test mirati. Rispetto a E18.31:
PASS D1–D10 428,93 → 322,07 (-24,91%); PASS/slot 24,41% → 19,96%; D5–D10
294,93 → 230,07 (-21,99%). Cassa media 78.750,29 → 78.931,18 (+0,230%):
28/28 delta positivi, ma vittorie ancora 16/28. Stesse consistenze giornaliere
di mucche e colture; stessa lana e raccolti colturali per ogni coppia.
Dodici manovali D16–D30 in tutti i casi. Organico iniziale ridotto solo con
verifica del carico: non dichiarare acquisita nuova produzione o risolti tutti
i PASS. D7 e D9 rimangono invariati, D12 aumenta i PASS pur riducendo i MOVE.

File corrente: `submission/submission_codex_e18_32_770_v9.py`, SHA-256
`4d2d32ac41b38af5f4f632ef9e8dd9af2ebd37f7e7bcb1795c2c31cda4e92789`.
Il file senza suffisso `_v9` è il precedente V7, conservato, non il finale.
Manifest e gate V9 sotto `artifacts/derived`; nessun nuovo Top770 o holdout,
nessun upload. Parità V9 completata: quattro casi, 2.876 batch per metodo,
source/standalone e caricatore Kaggle; chiamata massima 0,819 s.
Il mandato E18.33 supera ulteriori adattamenti sulla trajectory: generazione
del lavoro dallo stato, non nuovi target numerici copiati dai benchmark.
