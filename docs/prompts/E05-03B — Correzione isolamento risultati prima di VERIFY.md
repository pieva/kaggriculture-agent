# E05-03B — Correzione isolamento risultati prima di VERIFY

La BUILD E05 è tecnicamente riuscita, ma prima di autorizzare VERIFY deve essere risolta un'anomalia negli artifact dei risultati.

Segui ancora la fase:

`BUILD`

Non eseguire il benchmark completo da 30 episodi.

Non passare ancora a VERIFY.

## Problema rilevato

Dopo lo smoke test E05:

```powershell
.venv\Scripts\python.exe scripts/run_eval.py --opponents starter --episodes 1
```

`git status --short` mostra:

```text
M results/e01_baseline.json
```

e `git diff --stat` mostra una modifica molto ampia del file:

```text
results/e01_baseline.json | 499 ++-----------------------------------------
```

Questo artifact appartiene a E01 e **non deve essere modificato da E05**.

## Attività richieste

1. Ispeziona `scripts/run_eval.py` e determina perché lo smoke test E05 ha scritto in:

   `results/e01_baseline.json`

2. Verifica se il percorso di output E01 è hard-coded o utilizzato come default.

3. Ripristina:

   `results/e01_baseline.json`

   **esattamente alla versione corrente di `HEAD`**, senza ricostruirlo manualmente e senza modificarne il contenuto storico.

4. Introduci la modifica minima necessaria affinché E05 utilizzi un artifact dedicato, preferibilmente:

   `results/e05_hire_multiworker.json`

   oppure un nome equivalente coerente con le convenzioni reali del repository.

5. La modifica deve preservare la compatibilità con gli esperimenti precedenti.

6. Non modificare gli artifact E01, E02, E03 o E04.

7. Ripeti:

```powershell
.venv\Scripts\python.exe -m pytest tests/
```

8. Rigenera, se necessario, la standalone submission:

```powershell
.venv\Scripts\python.exe scripts/build_submission.py
```

9. Ripeti **un solo smoke episode** E05 salvando esplicitamente il risultato nell'artifact E05 dedicato.

10. Verifica nuovamente:

```powershell
git diff --stat
git status --short
```

## Verifica obbligatoria

Al termine deve risultare che:

- `results/e01_baseline.json` non è modificato;
- nessun artifact E01–E04 è stato modificato;
- lo smoke E05 è salvato in un file risultati E05 dedicato;
- tutti i test continuano a passare;
- lo smoke episode completa 720/720 turni;
- Disqualification Rate resta `0%`;
- il lifecycle `HIRE` continua a mostrare 30 ingaggi nell'episodio.

Il valore economico dello smoke test non deve essere utilizzato per ottimizzare o modificare la strategia.

## Documentazione

Aggiorna:

`docs/versions/E05_build_antigravity.md`

aggiungendo:

- anomalia rilevata;
- causa;
- correzione applicata;
- verifica che gli artifact storici siano rimasti invariati.

La dichiarazione:

`Deviazioni dal PLAN: Nessuna`

deve essere corretta se l'anomalia o la modifica infrastrutturale costituiscono una deviazione rilevante.

## Condizione finale

Mostra:

1. causa dell'overwrite;
2. modifica applicata;
3. risultato completo di `pytest`;
4. risultato dello smoke test;
5. percorso del file risultati E05;
6. `git diff --stat`;
7. `git status --short`.

Poi **FERMATI**.

Non eseguire il benchmark E05 da 30 episodi.

Non effettuare REVIEW o SHIP.

Attendi approvazione esplicita per VERIFY.