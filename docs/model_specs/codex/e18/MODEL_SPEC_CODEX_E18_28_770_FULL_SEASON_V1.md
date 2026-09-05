# E18.28 — Full Season 770 V1

Autorizzazione del proprietario, 2026-09-05: ottimizzare l'intero D1-D30,
continuità della produzione/personale, acquisti mucche progressivi D1-D10,
verifica economica carote e una candidata quotidiana per Kaggle. Questa
specifica estende la precedente finestra solo D25-D30; non ne altera i dati.
Esito sviluppo: **C selezionata per verifica esterna quotidiana**, non promossa
a incumbent. B migliora il parent, D/E respinte per perdita animali. Parity
standalone verificata su 719 azioni per seat, incluso il loader file Kaggle.

Vincoli: 7-7-0, 14 pascoli, cap 14 animali, massimo 12 hands + farmer.
Non si ottimizza il numero di tile invendute al terminale: mantenere missioni
produttive fino a D30, con DROP/SELL prima dell'ultimo step eseguibile H23.

Trattamenti preregistrati:

- A: workforce mantenuta fino a D30, route terminali H23 e vendite dei DROP
  reali, senza introdurre cicli annuali tardivi aggiuntivi.
- B: A + nuove missioni annuali Wheat D26-D28; D25 conserva le colture parent.
  Le retirement Strawberry D27/D28 restano invariate; le successive vengono
  pianificate a D30 (il motore può esaurire la pianta prima). Nuovi annuali
  raccolti a età 3, oppure 2 al terminale. WATER e logistica prenotati, niente
  semine che non maturano entro D30, niente DIG terminale senza valore.
- C: identiche missioni B, con Carrot nelle sole nuove semine da D26.
  Test controllato della composizione: non si sceglie usando prezzi futuri.
- D_WHEAT/D_CARROT: B/C + sviluppo mucche più progressivo: Q0 +1 D3 e +1 D5;
  Q1 +2 D8, +2 D9, +1 D10. Target 2,2,3,3,4,4,4,6,8,9. D7 resta dedicato
  all'unlock finanziato dalla lana; non si anticipano animali su terra chiusa.
  Gli incrementi sono discreti perché gli animali sono interi; non è una
  pretesa di crescita matematica continua.
- E_CARROT: ulteriore tentativo Q0 +1 D4/D5 e protezioni JIT/inflight da D1.
  D ed E sono ablation fallite, non caratteristiche della candidata pubblicata.

A/B/C preservano azioni e mercato D1-D24 (incluso lookahead); D modifica
esplicitamente l'apertura. Non tuning per seed, identità o dati privati altrui.
Controlli interni: parent E18.27 V3, E18.16 e E18.2/V4D competitivo storico.
Seed development 180903001–180903007, entrambi i seat; smoke iniziale seed 1.
Holdout/final non autorizzati né consumati.

Gate: piano biologico/route valido, engine reale, zero errori e perdite
animali, cap risorse e layout; confronto economico matched, regressioni per
seed esposte, costi carote/workforce e ricavi effettivi riconciliati. Nessuna
promozione per il solo volume. Si pubblica una sola candidata giornaliera
tecnicamente valida, con vantaggi e limiti documentati e parity standalone.

## Risultati e limiti effettivi

Su 7 seed development × 2 seat contro E18.16: parent E18.27 V3 69.156;
B 72.343,57; C 74.491,57 (+7,72% parent, +2.148 contro B). Tutti i 14 delta
C-parent sono positivi, minimo +3.104. C perde però 13/14 scontri diretti
contro E18.16. Contro E18.2/V4D nello smoke: 60.612 contro 85.329, 0/2 vittorie.
Nessuna affermazione di chiusura del gap con i top o con la migliore pubblicata.

C mantiene 12 hands D25-D30 e produzione fino ai raccolti/vendite D30;
non mantiene piante invendute a fine partita. Nel seed smoke le crop H24
D25-D30 sono 61,60,58,61,23,0. Anche Top770 riduce le consistenze durante la
liquidazione D29-D30: non confondere attività produttiva e stock terminale.
Zero fughe/errori e zero residui prodotti/semi nei 14 casi; cap 14 rispettato.
Il seed 180903007 eredita un posto vuoto (9 Cow + 4 Sheep), ancora da recuperare.

La progressione mucche richiesta resta **non risolta**: nello smoke D produce
74.300 con una fuga Sheep; E 69.912 con una fuga, contro C 77.898. Gli acquisti
anticipati interferiscono con finanziamento, pickup e servizio FEED: spostare
le sole date non garantisce esecuzione. Pubblicare C evita di introdurre il
difetto, ma lascia l'apertura 2,2,2,2,4,4,4,4,4,9 da ottimizzare separatamente.

I check legacy del planner `all_composition_checkpoints_match`, picco precoce
e residui shadow non sono nuovi gate economici: alcuni restano falsi. Sono
esplicitamente conservati nel piano; la validazione usa route/capacità,
legalità, sicurezza biologica e stati terminali del motore reale.

Report: estendere il formato a 19 pannelli con MOVE/PASS per giornata,
colture non irrigate al checkpoint (non automaticamente morte per sete),
perdite animali verificate per giornata e tile WEED. Conservare fonti/derivati
prima della cancellazione mirata della sola cache Kaggle riscaricabile.

L'aggiornamento conclusivo di NEW_SESSION/PROJECT_STATE, la pulizia finale
del repository e commit/push sono rinviati ai primi cicli esterni, come
richiesto. Config, specifica e risultati di sviluppo vengono salvati durante
il lavoro per tracciabilità; questo non è un allineamento anticipato di Git.
