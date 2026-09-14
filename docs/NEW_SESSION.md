# New Session — indicatori per colmare il gap con i top

## Mandato corrente e costi

La prossima sessione deve **trovare indicatori osservabili che possano colmare il gap con i top**, usando prima i dati già raccolti. Non ripartire da altri semplici cambi di mix o da tornei estesi.

L'utente ha segnalato circa **50 € di crediti spesi senza ottenere una policy migliore**: importo riferito, non verificato contabilmente. L'assistente ha riconosciuto il dimensionamento eccessivo del lavoro e degli aggiornamenti. Il risultato pratico richiesto resta migliorare E22, non produrre altra sola reportistica. Analisi mirata sui dati salvati; prima di nuove simulazioni individuare una modifica concreta, beneficio plausibile e test minimo con limite di costo/partite concordato. Nessun monitor, nuova attività o esecuzione lunga automatica. Nessuna pubblicazione Kaggle autorizzata. Aggiornamenti sintetici su risultati o decisioni utili.

## Report da aprire per primo

**[REPORT DEL TORNEO A CINQUE — LINK BROWSER](http://127.0.0.1:8771/tournament5_v1/REPORT.html)**

[HTML versionato](model_specs/codex/e23/reports/tournament5_v1/REPORT.html). Percorso assoluto: `C:/Users/pietr/Projects/kaggriculture-agent/docs/model_specs/codex/e23/reports/tournament5_v1/REPORT.html`.

Il link localhost richiede il server locale attivo. Se non risponde, dal checkout avviare soltanto il server di lettura, **non il torneo**:

```powershell
.venv/Scripts/python.exe -m http.server 8771 --bind 127.0.0.1 --directory docs/model_specs/codex/e23/reports
```

Ramo `codex/e23-evolution-tournament`; checkout `C:/Users/pietr/Projects/kaggriculture-agent`. Python `.venv/Scripts/python.exe`. Simulazioni e aggiornamento automatico report sono terminati.

## Stato congelato

140 incontri conclusi: 10 coppie × 7 semi × 2 posti, 56 partite per versione. Nessun pareggio.

| Versione | Mix | Vittorie | Stato |
|---|---|---:|---|
| E22.1 | 8C6S3G | 40/56 | Q2 Grano, submission 56228842 |
| E23.1 | 9C5S3G | 34/56 | Locale, non promossa |
| E22.2 | 8C9S | 30/56 | fix Q2 Grano, submission 56231638 |
| E23.3 | 7C10S | 24/56 | Locale, non promossa |
| E23.2 | 6C11S | 12/56 | Locale, non promossa |

E23.1 contro E22.1: 4–10, delta medio −982,71 monete. E23.2 contro E22.2: 2–12, −2.244,29. E23.3 contro E22.2: 4–10, −916. La 7C10S batte la 6C11S 12–2, +1.432,43 medie; l'ultimo seme favorisce invece 6C11S.

Verificati 280 lati: mix attesi e Q2 Grano raccolto ovunque, zero fughe e discrepanze contabili. Nessuna differenza di ricompensa nei 70 confronti a posti invertiti: non sono campioni indipendenti. E23.1 lascia tre latti non raccolti sulla nuova mucca; nessuna differenza inventariale nei prodotti animali raccolti. Il pollaio Q2 era già eliminato nelle E22 correnti.

Semi **180911301–180911307 già esposti**; **180912401–180912407 riservati e mai usati**. Non usare quelli riservati per selezionare indicatori. Nessuna E23 pubblicata. Risultati locali, non stime del rating Kaggle.

## Indicatori da indagare — ipotesi, non risultati già dimostrati

1. **Domanda e saturazione per prodotto:** compratori/capacità visibili, livelli e pendenze dei prezzi, stock e produzione propria/avversaria osservabili; valore atteso della prossima produzione al momento della scelta.
2. **Margine marginale e rientro del capitale:** ricavi realizzati al netto di acquisti, alimentazione, lavoro e trasporti; alternativa migliore sulla stessa casella.
3. **Rotazioni e calendario dei top:** semina, primo raccolto, rinnovo/dismissione, grano comprato/autoconsumato; ingressi Q3/pomodori collegati a domanda e compratori. Cercare trigger ripetuti, non copiare a posteriori un calendario.
4. **Servizi e vendite:** prodotto disponibile contro raccolto/venduto, attesa prima del deposito, slot di alimentazione/cura, fertilizzante e rendimento dei percorsi.

Verificare gli indicatori **prima** delle decisioni in più replay dei top, includendo controesempi. Partire da poche coordinate e finestre temporali; evitare scansioni indiscriminate. Separare contabilmente il gap senza attribuire causalità a differenze fra mercati diversi. Usare solo informazioni disponibili nell'osservazione della policy: niente prezzi futuri o inventario privato dell'avversario.

Consegna attesa prima di altro consumo sperimentale: pochi indicatori con definizione e disponibilità temporale, evidenze/controesempi, una regola implementabile, beneficio plausibile e protocollo minimo. Concordare il budget prima di nuove simulazioni.

## Dati da riutilizzare

- [Gruppo vicino a 3000](model_specs/codex/e23/reports/near3000_20260914/BENCHMARK_SET.md): Catalyst 56218385, Thomas Tschinkel 56222223, Deodims & Co 56223630. Screening 11 team 2950–3000, 55 replay-lato e 9 replay di conferma. Sui 24 replay dei tre riferimenti: 23/24 stesse 17 coordinate animali e nucleo 33 fragole/25 grani a D20. Frequenza non significa ottimalità. Mengfei non è assunto come modello stabile.
- [Ricorrenze](model_specs/codex/e23/reports/recurrence_20260914/REPORT.md), [delta evolutivi](model_specs/codex/e23/reports/evolution_delta_20260914/PROPOSAL.md), [confronto con oche](model_specs/codex/e23/reports/geese_vs_e221_20260914/REPORT.html), [senza oche](model_specs/codex/e23/reports/sheep_vs_e222_20260914/REPORT.html). Gli ultimi due confrontavano mercati differenti, non stimavano un guadagno causale.
- [Implementazione](model_specs/codex/e23/IMPLEMENTATION.md): mix e servizi evoluti sulle rotte E22, senza copiare tutto il calendario dei top. Tutte le E23 condividono le correzioni E22.2: non attribuire il delta della 9C5S3G al solo animale cambiato.
- [Risultati/contabilità](model_specs/codex/e23/reports/tournament5_v1/SUMMARY.json), [diagnostica](model_specs/codex/e23/reports/tournament5_v1/DIAGNOSTICS.json), [verifica](model_specs/codex/e23/reports/tournament5_v1/VERIFICATION.json), [bundle/hash](model_specs/codex/e23/reports/tournament5_v1/BUNDLES.json).
- [Checkpoint analitico](model_specs/codex/e23/ANALYSIS_CHECKPOINT.zip): profili completi dei match/collaudi, replay baseline del confronto senza oche, CSV giornalieri e copie delle dipendenze esterne di audit. Estrarre nella radice di un checkout quando servono questi file esclusi da Git; **non rilanciare partite per ricrearli**. [Manifesto di conservazione](model_specs/codex/e23/STATE_MANIFEST.json).
- Replay grezzi del torneo conservati localmente in `docs/model_specs/codex/e23/reports/tournament5_v1/matches/*.replay.json.gz`, con [manifesto e SHA256](model_specs/codex/e23/reports/tournament5_v1/REPLAY_MANIFEST.json). Replay top in `data/replays/json/e23_near3000_20260914/`. Le cache grezze voluminosissime restano locali, fuori dal push; nessun file cancellato.
- Chiusura E22 e dipendenze originali: `C:/Users/pietr/.codex/worktrees/756c/kaggriculture-agent`, ramo `codex/e22-2-pascoli-release`. I generatori contengono questo percorso assoluto: su un altro ambiente adattare il percorso ai sorgenti salvati, senza eseguire il runner del torneo.

[Cronologia precedente archiviata](archive/E23_NEW_SESSION_before_indicator_handoff_20260914.md): i vecchi mandati E22/torneo sono storici e non vanno riavviati.
