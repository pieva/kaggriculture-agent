# Model spec — Codex E18.2 Capacity-Governed V4D V1

## Identità

- candidate: `CODEX_E18_2_CAPACITY_GOVERNED_V4D_V1`;
- model spec: `CODEX-E18.2-CAPACITY-GOVERNED-V4D-V1`;
- provider congelato: `CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28`;
- ruolo: candidate development E18, non ancora baseline Kaggle;
- memoria cross-episode: assente;
- input avversario: sola farm pubblica.

## Decisione architetturale

La topologia V4D `7-7-5` e i 19 slot zootecnici restano invariati. La prima
ablation `7-7-4`, che recuperava un pascolo Q2, ha prodotto regressioni
immediate fra circa `-35k` e `-60k` e viene respinta. Anche deviare un worker
`PASS` verso un task distante rompe la sincronizzazione V4D e viene respinto.

La V1 ammessa usa tre stati:

1. `DENSE_V4D`: azione del provider senza modifiche;
2. `RECOVERY`: un solo worker che il provider lascia in `PASS` può eseguire
   `HARVEST`, `DIG` o `WATER` esclusivamente se si trova già sul tile;
3. `RECLAIM_CROP`: implementato come envelope sperimentale ma disabilitato
   nella config congelata (`topology_reclaim_enabled=false`).

L'avversario pubblico modula l'azione soltanto nei casi di stress proprio
lieve: sopra la soglia pubblica abilita il servizio locale, sotto soglia resta
neutro. Uno stress proprio severo abilita comunque recovery e mantiene quindi
la sicurezza come vincolo primario. Stress idrico, weed e feed arretrato
attivano `RECOVERY`; due giorni puliti costituiscono l'isteresi di uscita.

## Invarianti

- nessuna nuova azione `PASS` rispetto al provider;
- nessuna deviazione di percorso in recovery;
- nessun cambiamento alla topologia di default;
- zero accesso a inventario privato avversario, rating, nome o replay ID;
- passthrough esatto V4D da D28 per preservare batching e liquidazione;
- fail closed al confine Kaggle;
- nessun holdout/final consumato.

## Frozen Engine Contract

Il contratto motore congelato stabilisce cosa la candidate può assumere dal
simulatore: schema delle osservazioni/azioni, orologio `720 = 30×24`, semantica
di tile e inventari, limiti di ordini e comportamento terminale. Non congela
la strategia; impedisce che un miglioramento apparente dipenda da una diversa
interpretazione del motore. E18.2 riusa integralmente il contratto già
verificato da V4D.

## Gate development

Matrice: 56 match, sette seed development, entrambi i seat, contro V4D,
E18.1, Claude E18.2 e Copilot E18.2; Antigravity escluso.

- `56-0`, denaro medio pool `121.149,84`;
- diretto V4D `14-0`, `93.401,71` contro `90.012,00`, delta `+3,77%`;
- `PASS` `688` contro `724` (`-4,97%`);
- weed tile-days `15` contro `14` (`+7,14%`, entro cap `+10%`);
- animali finali `19`, zero perdite, errori e fallback;
- due action-effect modes: `DENSE_V4D`, `RECOVERY`;
- gate `9/9 PASS`.

Questi risultati autorizzano il bundle standalone per una successiva
decisione di upload; non consumano holdout e non equivalgono a promozione
esterna.
