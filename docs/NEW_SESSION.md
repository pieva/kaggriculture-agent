# NEW_SESSION — Kaggriculture

## Ripartenza operativa anti-PASS — 2026-09-05

Decisione del proprietario: l'eccesso di PASS è un sintomo del motore di
assegnazione, da riprogettare. Sviluppo attivo: **E18.30 — mission dispatcher**.
Non riprendere le vecchie priorità D25-D30 o crescita mucche come primo task.
La cronologia precedente è conservata in
`docs/history/NEW_SESSION_PRE_ANTI_PASS_20260905.md`, non è una seconda fonte
di istruzioni correnti. Stato sintetico: `docs/PROJECT_STATE.md`.

## Invarianti e controlli

- Topologia target esatta **7-7-0**, 14 pascoli, cap 14 animali e massimo
  12 manovali. Non variare topologia fino a una riduzione consistente del gap.
- Sola linea attiva Codex; Antigravity, Claude e Copilot restano congelati.
- Ultima pubblicata: **E18.28 C**, submission Kaggle **56036993**,
  `submission/submission_codex_e18_28_770.py`, SHA-256
  `8788f68c74b95c56c21feffba6fd5c49654d1c2dc5e71b5a0ca94800f988969d`.
  File immutabile, controllo parent, non incumbent promosso.
- **E18.29 B3** è development, non pubblicata e non promossa: guadagno locale
  +7,68% su 14 casi contro E18.16 rispetto al parent, PASS -26,78%, MOVE +8,09%.
  Resta una morte Strawberry D12 ereditata: gate mortalità assoluta fallito.
  Non confondere questi risultati interni con i replay pubblici E18.28.
- E18.16 ed E18.2 sono campioni interni; E18.2 resta riferimento esterno
  storico migliore indicato dal proprietario. Gli score nei vecchi report
  sono snapshot datati, non valori live.
- Top770 è l'alias documentale. ID/hash e identificativi tecnici congelati
  preservano la provenienza; non rinominare piani/config rompendo i loader.

## Evidenza di origine, non obiettivo da copiare

Corpus pubblico congelato a episodio 105876558: **30 partite competitive,
17 sconfitte e 13 vittorie, 30 avversari**, self-test escluso. Parità shadow
21.570/21.570 batch con E18.28 pubblicata; non simulazioni controfattuali.
PASS medi 1.573,7. Nelle sconfitte D15-D30: 746,3 PASS, di cui 622,8 code
esaurite (83,5%) e 123,5 attese pianificate; zero blocchi immediati in questa
finestra non esclude effetti indiretti di precedenti mancate esecuzioni.
Il fenomeno è presente anche nelle vittorie: PASS non spiega da solo l'esito.

In 105864674 e 105874761 le assunzioni D11 falliscono per cassa: rimangono
7 e 3 manovali. Nessun nuovo HIRE dopo H2 malgrado incassi successivi;
WATER/HARVEST rimangono assegnati a lavoratori assenti. I due casi totalizzano
32 morti crop. Non assumere che tutti i lavori siano recuperabili a fine giorno.

Flussi monetari verificati 29/30 (tutte le 17 sconfitte); un'eccezione da 81
in 105852748 resta N/D, non zero. Nessuna fuga nei 29 casi verificati.
Nessuno dei 17 vincitori avversari è exact770: gap economici descrittivi,
non stime di guadagno causalmente recuperabile a parità di architettura.
Le opportunità locali HARVEST/CARE/WATER/fertilizzante sono proxy sovrapposti,
non ricavi da sommare e non autorizzano missioni incomplete.

Fonti da leggere, sotto `docs/model_specs/codex/e18/`:

1. `reports/E18_28_EXTERNAL_PASS_CAUSES_AND_NEXT_ACTIONS_IT.md`.
2. `reports/E18_28_EXTERNAL_PASS_DIAGNOSIS_20260905_IT.md`.
3. `artifacts/derived/E18_28_EXTERNAL_PASS_DIAGNOSIS_20260905_V2.json`
   e profili `artifacts/derived/e18_28_external_pass_20260905_v2/`.
   I profili senza suffisso v2 sono preliminari, non usare per conclusioni.
4. `MODEL_SPEC_CODEX_E18_29_770_ANTI_PASS_V3.md`.
5. `MODEL_SPEC_CODEX_E18_30_770_MISSION_DISPATCHER_V1.md`.

## Sequenza di sviluppo

1. Separare obiettivo economico, missione completa e azione; ledger unico di
   missioni con identità, prerequisiti, deadline, risorse e stato verificato.
2. Assegnare soltanto ai manovali osservati, rimettere nel pool i lavori orfani;
   un comando emesso non costituisce conferma di esecuzione. Nessuna assunzione
   soltanto prevista può aggiungere capacità al batch corrente.
3. Prima tranche isolata: nucleo di assegnazione e test di contratti/regressione.
   Poi adattatore osservazioni, acknowledgement e route admission completa.
   Tenere separati recupero payroll/HIRE e missioni discrezionali redditizie.
4. Congelare economia, mix e topologia del parent per la prima ablation.
   Mai ridurre PASS aggiungendo movimento, WATER inutile o lavoro senza vendita.
5. Confronto matched su sette seed development × due seat contro E18.16,
   smoke E18.2 e confronto delta con E18.28 C; E18.29 B3 controllo secondario.
   Misurare cassa finale/minima, mortality, servizio WATER/FEED, raccolti/vendite,
   PASS normalizzati, MOVE/productive, deadline mancate e missioni orfane.
   Test avversari/seed multipli; nessun tuning per episodio o Top770.
6. Non promuovere il nucleo isolato come agente funzionante. Prima del rilascio:
   safety senza nuove perdite, beneficio economico robusto, parità standalone
   e gate preregistrati; holdout non ancora consumato.

## Verifica esterna e formato di analisi

Resta il processo concordato: sviluppo sui campioni interni completamente
ispezionabili; submission quotidiana del migliore sviluppo eleggibile per
verifica esterna, analisi quotidiana dei top per architetture/strategie.
Non forzare l'upload di una regressione o consumare holdout per rispettare
la cadenza. Non è una nuova autorizzazione a creare automazioni duplicate.

Grafici sempre **Top770 vs una sola versione**, D1-D30, standard V3 comune:
21 pannelli incluso WATER/FEED riusciti al giorno, senza Cause PASS.
Conservare tutte le specie, cassa, personale, MOVE/PASS, mancata irrigazione,
perdite verificate, weed e ricoveri vuoti distinti. Affiancare tabelle KPI
economico-operativi e denominatori reali, non soltanto consistenze.
`experiments/e18/reports/common/E18_AGENT_COMPARISON_REPORT_STANDARD_V3_IT.md`.

## Organizzazione e chiusura

Strategie, specifiche, tool, test e dati Codex sotto `docs/model_specs/codex/e18/`;
`experiments/` contiene protocolli e materiale comune. Conservare anche risultati
negativi, fonti e audit. Eliminare solo cache riscaricabili catalogate e QA
rigenerabili, previa verifica hash/path; niente rimozione di evidenza unica.
Il monitor dei primi replay E18.28 è stato messo in pausa: questa chiusura
viene eseguita nella sessione attuale, senza duplicare commit o upload.
