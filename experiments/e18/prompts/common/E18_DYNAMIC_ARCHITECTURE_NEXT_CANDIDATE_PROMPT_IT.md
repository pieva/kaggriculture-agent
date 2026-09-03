# E18 — prompt comune per la prossima candidate dinamica

Costruisci una nuova candidate autonoma partendo dalla tua linea, senza
importare controller o routine Codex. Il target resta 100.000 di final money,
ma la selezione non userà più KPI statici da soli.

La candidate deve osservare esclusivamente lo stato pubblico corrente
dell'avversario e dichiarare le feature usate. Deve implementare almeno due
regimi operativi con una transizione o decisione esplicita, tracciabile e
testabile. A parità di seed e seat, due fixture avversarie causalmente diverse
devono produrre action stream diversi e, quando previsto dal design, una
diversa allocazione topologica o del lavoro. Nomi, rating, replay ID, seed,
inventari privati e memoria cross-episode sono vietati.

Il freeze deve includere entry point callable, config separata, hash,
telemetria di attivazione e test. Misura almeno: denaro per classe di
avversario, action-stream divergence, topology/work-allocation divergence,
regimi osservati e transizioni, harvest yield, weed exit, perdite verificate
su tile+shed+inventari, errori e fallback. Per mixed-farming richiediamo
zero perdite; per crop-only richiediamo un lifecycle esplicito
`KEEP/HARVEST/DIG/REPLANT` e una riduzione delle weed.

Usa soltanto i seed development E18. Holdout e final confirmation restano
vietati senza autorizzazione del proprietario. Confronta il risultato con
`E18_DYNAMIC_ARCHITECTURE_TOURNAMENT_V1_REPORT_IT.md` e spiega separatamente
delta economico e delta architetturale: una media migliore senza attivazione
causale non basta, così come una topologia variabile senza controllo esplicito
non prova reattività.
