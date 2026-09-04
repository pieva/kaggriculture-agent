# Copilot E18 — zero-hands diagnosis V3

## Obiettivo

Questa revisione è stata costruita come prova del Gate 0 richiesto dal prompt: prima di introdurre qualsiasi regime o reattività, isolare e correggere il contesto di dismissione del lavoro che impedisce all'agente di assumere anche un solo hand. Il punto non è cambiare etichetta o movimento, ma rendere reale il contratto azione/osservazione: il primo passo produttivo deve essere `HIRE` quando il team di lavoro è vuoto.

## Evidenza osservata

Nel V2 Copilot E18 la logica di allocazione e regime era presente ma il payload di mercato non conteneva mai un ordine di assunzione di un hand quando `hands == 0`. Il risultato era un ciclo in cui il controller poteva cambiare regime, cambiare label o muoversi, ma restava in una situazione di dead stack: nessun hand, nessuna azione produttiva, denaro statico e plateau economico.

L'analisi è coerente con il report di torneo: i profili Copilot mostrano picchi medi di crop/animali/hands pari a zero e una mancanza terminale di azioni produttive. In questo contesto, la variabilità di regime non è un segnale di reattività ma un sintomo di un loop funzionante solo a livello di label, non di economia.

## Diagnosi

Root cause: `missing_hire_dispatch_when_hands_empty`.

Il punto tecnico è semplice e verificabile:

- il controller opera sul farm senza controllo di guardrail iniziale;
- se `hands == []`, non vengono emessi ordini di mercato di `HIRE`;
- nessun task di terreno può essere eseguito finché non ci sono worker disponibili;
- di conseguenza non si genera mai una catena produttiva `DIG -> PLANT -> WATER -> HARVEST -> SELL`.

La correzione del Gate 0 è quindi rigorosamente solo un gatto di compatibilità produttiva: risolvi il contratto di assunzione e poi poi prosegui con la logica economica / regime. Nessun regime viene introdotto finché non si ottiene almeno un flusso completo di lavoro.

## Versione implementata

- Source: `src/agricola/strategy/copilot/e18_dispatch_diagnosis_v1.py`
- Config: `docs/model_specs/copilot/e18/configs/COPILOT_E18_3_DISPATCH_DIAGNOSIS_V1.json`
- Test: `docs/model_specs/copilot/e18/tests/test_copilot_e18_dispatch_diagnosis_v1.py`
- Runner: `docs/model_specs/copilot/e18/tools/run_copilot_e18_dispatch_diagnosis_v1_dev_benchmark.py`

## Verifica eseguita

### Test unitari e smoke

Eseguito con il venv del repo:

`python -m pytest docs/model_specs/copilot/e18/tests/test_copilot_e18_dispatch_diagnosis_v1.py -q`

Risultato: 3 test passed.

### Lint

Eseguito con:

`python -m ruff check src/agricola/strategy/copilot/e18_dispatch_diagnosis_v1.py docs/model_specs/copilot/e18/tests/test_copilot_e18_dispatch_diagnosis_v1.py docs/model_specs/copilot/e18/tools/run_copilot_e18_dispatch_diagnosis_v1_dev_benchmark.py`

Risultato: Nessun errore Ruff sui nuovi file.

## Artefatti generati

- JSON: `docs/model_specs/copilot/artifacts/derived/E18_COPILOT_DISPATCH_DIAGNOSIS_V1_DEVELOPMENT_FIXTURES.json`
- CSV: `docs/model_specs/copilot/artifacts/derived/E18_COPILOT_DISPATCH_DIAGNOSIS_V1_DEVELOPMENT_FIXTURES.csv`

### SHA-256

- JSON: `7CF63B721318AFD330C45B4F83593FEE531E87D8BC11BB9EB0FFEB216B687DAC`
- CSV: `76C910ABDDF835C42AE19CC877F95473712D8DCD66D4BB1D16206532910C8DB2`

## Risultato di Gate 0

Passato in senso diagnostico: l'agente ora emette in modo esplicito `HIRE` quando non ci sono hands e dispone di denaro sufficiente. Questo apre la finestra per far passare il contratto produttivo a `DIG -> PLANT -> WATER -> HARVEST -> SELL` senza introdurre reattività o regime prematuri.

## Verdict

- Tecnico: OK sui nuovi file, zero errori e ruff pulito.
- Produttivo: OK sul Gate 0, con assunzione di worker iniziale attivata.
- Dinamico: non ancora applicato; la reattività è stata lasciata fuori dal raggio per rispettare il gate di diagnosi.
- Sicurezza: non applicata a livello di meccanica di mercato; il fatto è stato isolato e corretto senza toccare i file congelati di V1/V2 o di competitor.

Questo è il punto corretto per proseguire con la baseline economica V3: prima serve un assunzione reale di lavoro, poi si introdurrà la seconda leva (allocazione/workforce, budget, raccolta/vendita) e solo infine il regime causale.
