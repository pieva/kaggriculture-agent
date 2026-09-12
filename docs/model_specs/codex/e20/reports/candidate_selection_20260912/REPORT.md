# Selezione per verifica esterna dei 22 KPI — 12 settembre 2026

**Scelta complessiva: E18. Scelta esplorativa della serie E20: E20.2. Nessun upload eseguito.**

E18 conserva la migliore evidenza esterna storica disponibile; non è stato verificato qui il punteggio Kaggle corrente. Nel torneo interno ha +3539 di margine medio contro E20.2 (5/7 seed positivi), ma soltanto +859,7 contro E19 (2/7 positivi). Il vantaggio medio su E19 dipende quindi da pochi scenari favorevoli: non prova dominanza generale.

## Tentativi effettivamente conclusi

| Revisione | Partite / seed | Margine medio vs E18 | Seed positivi | Margine sulle 4 partite comuni |
|---|---:|---:|---:|---:|
| E20.2 | 14 / 7 | -3539.0 | 2/7 | -6975.2 |
| E20.3 | 4 / 2 | -4787.0 | 1/2 | -4787.0 |
| E20.4 | 4 / 2 | -7253.5 | 1/2 | -7253.5 |
| E20.5 | 4 / 2 | -9477.5 | 0/2 | -9477.5 |
| E20.6 | 4 / 2 | -10544.0 | 0/2 | -10544.0 |
| E20.7 | 14 / 7 | -9662.0 | 0/7 | -12528.2 |

Le quattro partite comuni sono i seed 180911301 e 180911303, entrambi i ruoli. Non confrontare direttamente medie di campioni differenti. I seed sono ormai esposti allo sviluppo; i due ruoli non sono repliche indipendenti. Nessuna revisione E20.3–E20.7 ha passato il proprio gate. E20.2 resta la base della serie, non una vincitrice dimostrata su E18 né su ogni precedente E20 non ritestata.

- E20.3: mix 8 mucche / 8 pecore; respinto.
- E20.4: scelta condizionale grano/carote; v34 invalida per errore tecnico, v35 riparata ma respinta.
- E20.5: domanda dei negozi osservati nelle proiezioni; respinta.
- E20.6: rimozione del minimo storico nelle stime SELL; respinta.
- E20.7: controller E18 adattato a 772; respinta, 0/7 seed positivi. Il prototipo v38 non è stato simulato; i risultati sono del v39.

## Che cosa abbiamo imparato

Il divario E18–E20.2 è contabile: +18290,7 vendite, −14422,4 maggiori acquisti, −329,4 maggiori costi di assunzione = +3539. Circa il 76% nasce già tra D12 e D19. Più ricavi di grano non equivalgono a più produzione: E18 acquista e vende più grano, con raccolti simili. I PASS non sono una causa dimostrata.

Le azioni cambiano anche il consumo del RNG delle infestanti e quindi i negozi futuri. A seed uguale la domanda può divergere: questo è un effetto reale del motore, da distinguere dall’efficienza produttiva. Il controllo sintetico con negozi fissati aiuta la diagnosi ma è escluso dalla selezione e dal ranking.

## Artefatto e verifica esterna

Bundle E18: `submission\submission_codex_e18_2_capacity_governed_v4d.py`; SHA256 `c5fb1fc4966b81f238cdd0de4ca5e15b16ea6b8ae077a08ecc881f8729fd01f7`. Per uno slot destinato al migliore complessivo scegliere questo bundle. Se invece lo scopo è misurare esternamente una nuova E20, scegliere il bundle congelato E20v32 / E20.2, dichiarando il carattere esplorativo. Nessuna submission è stata inviata da questa selezione.

La lettura esterna deve usare tutti i primi replay completi disponibili, dichiarando numerosità, avversari e ruoli; confrontare le traiettorie dei 22 KPI e separare D1–11, D12–19, D20–30. Conservare replay e hash, verificare errori e completezza, ricostruire vendite/acquisti/assunzioni e calendario negozi. Evitare conclusioni da singoli replay favorevoli.

## Report leggibili

- [Torneo a tre, 22 KPI](../e20_2_confirmation/REPORT.html)
- [E20.7 contro E18, 22 KPI](../e20_7_controller_transfer/REPORT_22_KPI.html)
- [Ricostruzione delle cause della cassa](../e20_2_confirmation/CASH_GAP.md)

Stato: selezione effettuata sui candidati sviluppati fino a E20.7. E20.8–E20.10 non generate; limite massimo E20.10 confermato, nessuna E20.11. I seed indipendenti 180912401–407 restano inutilizzati.
