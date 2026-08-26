# E06-07 — Kaggle External Validation

Proseguiamo il progetto **Kaggriculture Agent** dopo il completamento dell'esperimento:

`E06 — Water-First Scheduling`

Repository:

`C:\Users\pietr\Projects\kaggriculture-agent`

Stato corrente:

- E06 è `SHIPPED`;
- commit consolidato: `dc4c289 Finalize E06 water-first scheduling experiment`;
- tag: `v0.6-e06-water-first`;
- branch: `main`;
- `main` allineato con `origin/main`;
- working tree atteso: pulito.

Strategy shipped:

`WaterFirstHIRENWClusterROIAgent`

Standalone pronta:

`submission/submission.py`

La standalone è stata generata tramite:

`scripts/build_submission.py`

ed è già stata validata dalla suite:

`30 passed`

---

# Obiettivo

Effettuare la **submission ufficiale Kaggle di E06** utilizzando esclusivamente la standalone shipped:

`submission/submission.py`

Questa fase costituisce:

**External Validation**

e deve rimanere metodologicamente separata dal benchmark locale E06.

---

# 1. Verifica preliminare

Prima della submission esegui:

`git status`

e verifica che il working tree sia pulito.

Verifica inoltre:

- presenza di `submission/submission.py`;
- presenza della strategy Water-First nel bundle standalone;
- assenza di dipendenze dal package locale;
- corrispondenza della standalone con E06 shipped;
- nessuna modifica avvenuta dopo il commit/tag E06.

Non modificare l'algoritmo.

Non effettuare nuove ottimizzazioni.

---

# 2. Identificazione della submission

Utilizza una descrizione chiara e non ambigua, ad esempio:

`E06 - WaterFirstHIRENWClusterROIAgent - 9 tiles, WATER first, 1 farmer + 1 daily hand`

Se Kaggle impone limiti di lunghezza, abbrevia mantenendo almeno:

- `E06`;
- `WaterFirst`;
- riferimento a `HIRE` / multi-worker.

---

# 3. Submission Kaggle

Effettua la submission ufficiale della standalone:

`submission/submission.py`

alla competizione Kaggriculture utilizzando la stessa procedura già utilizzata e validata per le precedenti submission del progetto.

Prima di procedere, consulta se necessario:

`docs/versions/E05_kaggle_validation.md`

per mantenere lo stesso protocollo documentale.

Non modificare il file standalone durante il processo di submission.

---

# 4. Verifica dello stato

Dopo l'invio verifica che la submission risulti almeno:

`Complete`

o equivalente stato di completamento della piattaforma.

Registra:

- timestamp/data della submission;
- descrizione utilizzata;
- file inviato;
- stato Kaggle;
- eventuale Skill Rating / score mostrato;
- eventuali errori o warning.

---

# 5. Regola sullo Skill Rating

Il primo Skill Rating visualizzato dopo la submission deve essere considerato:

`PROVISIONAL / IN ASSESTAMENTO`

Non considerarlo automaticamente il risultato Kaggle definitivo.

L'esperienza E05 ha mostrato che il rating può cambiare sensibilmente dopo la prima valutazione.

Pertanto:

- registra il primo rating osservato;
- indica chiaramente che è dinamico;
- non formulare conclusioni definitive sul confronto con E01–E05;
- non modificare il verdict locale E06;
- non modificare il tag E06;
- non reinterpretare retroattivamente DEFINE, BUILD, VERIFY o REVIEW.

---

# 6. Baseline locale da mantenere separata

Il risultato locale consolidato E06 resta:

- Mean Final Money: `$24662.00 ± $1932.04`;
- Median Final Money: `$25847.00`;
- Total Weed Conversions: `70`;
- Completion Rate: `100%`;
- Disqualification Rate: `0%`;
- Win Rate: `100%`;
- Mean Paired Money Delta vs E05: `+$3093.07`;
- Money Higher vs E05: `29/30`;
- Weeds Lower vs E05: `30/30`;
- Experimental Verdict: `SUPPORTED`;
- SHIP Status: `PASSED`.

La metrica Kaggle è una **external validation differente** e non è direttamente intercambiabile con `Mean Final Money`.

---

# 7. Confronto storico Kaggle

Nel documento di validazione riporta gli Skill Rating storici disponibili, utilizzando i valori attualmente consolidati nel repository.

In particolare, verifica la documentazione corrente prima di copiare qualsiasi numero.

Per E06 registra esclusivamente:

`primo rating osservato`

e stato:

`IN ASSESTAMENTO`

finché non abbiamo evidenza che il valore si sia stabilizzato.

---

# 8. Documento di validazione esterna

Crea:

`docs/versions/E06_kaggle_validation.md`

Il documento deve contenere almeno:

1. **Experiment**
2. **Local SHIP Baseline**
3. **Standalone Artifact**
4. **Kaggle Submission Description**
5. **Submission Status**
6. **Initial Skill Rating**
7. **Rating Status: PROVISIONAL / IN ASSESTAMENTO**
8. **Historical Kaggle Comparison**
9. **Local vs External Validation**
10. **Interpretation Limits**
11. **Next Observation Required**

Esplicita chiaramente:

> Lo Skill Rating Kaggle osservato subito dopo la submission non viene considerato definitivo e non modifica il verdict locale E06.

---

# 9. Aggiornamento stato progetto

Aggiorna:

- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`
- `docs/EXPERIMENT_LOG.md`

Registrando:

`E06 Kaggle External Validation — IN ASSESTAMENTO`

Non cambiare:

`E06 — SHIPPED`

E06 deve restare shipped indipendentemente dal primo rating Kaggle.

---

# 10. Eventuale evidenza screenshot

Se durante la procedura è disponibile una schermata Kaggle che mostra chiaramente:

- submission E06;
- stato `Complete`;
- Skill Rating;

salvala secondo le convenzioni già utilizzate nel repository per le evidenze Kaggle.

Non creare screenshot artificiali.

Registra esclusivamente evidenze effettivamente osservate.

---

# 11. Git dopo la submission

Dopo aver completato la documentazione della submission:

esegui:

`git status --short`

e:

`git diff --stat`

Se le sole modifiche riguardano documentazione/evidenze della validazione Kaggle E06, procedi con:

`git add .`

`git commit -m "Add E06 Kaggle external validation"`

`git push origin main`

Non creare un nuovo tag.

Il tag sperimentale corretto resta:

`v0.6-e06-water-first`

---

# 12. Verifica finale

Esegui:

`git status`

e:

`git log -1 --oneline`

Il working tree deve risultare pulito e `main` allineato con `origin/main`.

---

# Output finale richiesto

Mostrami:

1. conferma della submission Kaggle E06;
2. descrizione utilizzata;
3. stato della submission;
4. primo Skill Rating osservato;
5. indicazione esplicita `PROVISIONAL / IN ASSESTAMENTO`;
6. confronto puramente descrittivo con gli score storici disponibili;
7. conferma che il verdict locale E06 resta invariato;
8. documento `E06_kaggle_validation.md` creato;
9. eventuali altre modifiche documentali/evidenze;
10. commit e push effettuati;
11. `git status`;
12. `git log -1 --oneline`.

**Fermati dopo aver registrato il primo risultato Kaggle. Non attendere che il rating si stabilizzi e non iniziare E07.**