# E17 — Submission Codex per confronto esterno Kaggle

Data: 2026-09-02

Release: `CODEX-E17.0-EXTERNAL-CONTROL-V1`

Stato: `UPLOADED / SCORE_STABILIZING`

## Decisione

Antigravity non è disponibile per esaurimento dei crediti; un torneo locale a
tre non sarebbe quindi né completo né informativo. Su autorizzazione del
proprietario, E17 prosegue con un confronto esterno Kaggle.

La submission E17 è deliberatamente un **controllo esterno**: usa la logica
Codex V9 3Q già validata e non introduce modifiche comportamentali. Il wrapper
standalone dichiara la release E17 e il parent V9; la routine eseguibile e le
719 azioni restano invariate.

File da caricare:

`submission/submission_codex.py`

SHA-256:

`0428A6244C28E064BEDCEDC21C793D50A7C3231B8B7ADADF154BF40667833FC6`

## Evoluzione sintetizzata

1. La linea Codex è passata dalla dual-Q V7.3 alla V9 3Q mixed high-density,
   portando lo score Kaggle osservato da `598,3` a `1159,9`: `+561,6`, pari a
   `+93,9%`.
2. Il benchmark discovery E17 su nove replay ha mostrato che non esiste un solo
   archetipo vincente: timing, topologia, diversificazione, densità e gestione
   terminale devono essere separati causalmente.
3. Il repository è stato riordinato verticalmente e la Foundation C2.1 è
   rimasta immutata e verificata.
4. E17.0 ha introdotto `E17_LEDGER_V1` fuori dal decision path. Sulla V9 sono
   state ottenute parità azioni `4314/4314`, parità outcome `6/6`, copertura
   record 100%, zero errori, zero fallback delta e zero fughe EOD derivate.
5. Antigravity e Copilot hanno prodotto baseline native indipendenti, ma la
   prima non è produttiva e la seconda è ancora economicamente molto distante
   dalla V9. L'indisponibilità di Antigravity rende inutile simulare un torneo
   locale incompleto.

## Perché la submission resta comportamentalmente identica alla V9

E17.0 era una fase di osservabilità, non di ottimizzazione. Alterare adesso la
policy e chiamarla E17 confonderebbe l'effetto del nuovo codice con quello del
nuovo protocollo di misura. Cambiano soltanto docstring e identificatore di
release; la candidate mantiene esattamente le azioni della freeze V9:

```text
STANDALONE_IMPORT: PASS
WRAPPER_BYTE_IDENTITY_WITH_FROZEN_V9: NO — METADATA_ONLY_DELTA
BEHAVIORAL_IDENTITY_WITH_FROZEN_V9: PASS
ACTION_PARITY: 719/719 PASS
E17_0_ACTION_PARITY: 4314/4314 PASS
CANONICAL_SMOKE_STATUS: DONE
REPOSITORY_TEST_SUITE: 62/62 PASS
POLICY_MUTATION: NO
```

Il ledger non è incluso nella submission: serviva alla verifica offline e non
deve appesantire o influenzare il percorso decisionale su Kaggle.

## Risultati attesi

### Aspettativa primaria

- esecuzione Kaggle valida, senza errore o fallback;
- comportamento strategico identico alla precedente V9;
- score atteso **nell'intorno del riferimento 1159,9**, senza una previsione
  causale di miglioramento sistematico.

Il valore `1159,9` è un riferimento preregistrato, non una garanzia né un
intervallo statistico. Mix degli avversari, aggiornamento del rating e varianza
della piattaforma non sono stati caratterizzati abbastanza per definire una
banda numerica affidabile.

### Regola di interpretazione

- risultato vicino a `1159,9`: conferma della ripetibilità esterna della V9
  dopo riordino e strumentazione;
- risultato sensibilmente inferiore: segnale da replicare prima di dichiarare
  una regressione, poiché la logica d'azione è immutata;
- risultato sensibilmente superiore: non attribuibile a E17.0 come
  miglioramento di policy; va trattato inizialmente come effetto del contesto
  competitivo e verificato con una replica;
- nessun risultato di questa submission autorizza da solo E17.1 o la fusione
  post-hoc di più fattori strategici.

## Aggiornamento dell'esito esterno

La candidate è stata caricata come submission Kaggle `559588638`. Gli
screenshot forniti dal proprietario il 2026-09-02 documentano:

| Evidenza osservata | Valore |
|---|---:|
| Rating di ingresso | `600` |
| Ultimo rating visibile | `996` |
| Delta osservato | `+396` |
| Episodi visibili citati | `104788911`, `104789736` |
| Stato della misura | `INTERMEDIA / NON STABILE` |

Tra gli outcome recenti visibili figurano vittorie con denaro finale `102.751`
e `62.286`; screenshot precedenti mostravano inoltre `153.369` e `108.839`.
Sono esempi di singoli episodi, non una stima aggregata della performance. Nel
fotogramma più recente è ancora presente un incontro in corso: `996` non viene
quindi promosso a score finale né confrontato causalmente con `1159,9`.

L'aspettativa primaria sopra è preregistrata e resta separata dall'osservazione
post-upload. Poiché la policy è identica alla V9, l'eventuale scostamento va
prima attribuito a dinamica del rating, mix degli avversari e varianza; la
prossima evoluzione E17 sarà scelta soltanto dopo la stabilizzazione.

## Descrizione Kaggle consigliata

```text
E17 Codex 3Q - V9 congelata, parità 4314/4314, ledger 100%, 0 errori; controllo esterno.
```

## Provenance

- manifest release:
  `experiments/e17/artifacts/freeze/codex/E17_EXTERNAL_SUBMISSION_MANIFEST.json`;
- report E17.0:
  `experiments/e17/reports/codex/E17_0_IMPLEMENTATION_AND_PARITY_REPORT.md`;
- riepilogo comune:
  `experiments/e17/reports/common/E17_0_GATE_AND_BLOCKER_SUMMARY.md`;
- strategia congelata:
  `experiments/e17/design/E17_STRATEGY_FROZEN_V1.md`.

```text
KAGGLE_ARTIFACT_READY: YES
KAGGLE_UPLOAD_EXECUTED: YES
KAGGLE_SUBMISSION_ID: 559588638
KAGGLE_INTERIM_RATING: 996
KAGGLE_SCORE_STABLE: NO
LOCAL_TOURNAMENT: SKIPPED
HOLDOUT_CONSUMED: NO
FINAL_CONFIRMATION_CONSUMED: NO
E17_1_STARTED: NO
```
