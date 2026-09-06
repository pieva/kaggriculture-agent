# E18.30 — perché i PASS differiscono tra le due metà

Diagnosi del 2026-09-06 su richiesta del proprietario. Nessuna nuova simulazione,
modifica di policy, promozione o submission. Nei grafici D1 è il giorno motore 0.

## Esito

**Il criterio di assegnazione dovrebbe essere unico. E18.30 V2 è ancora ibrida:**
esegue prima le code individuali del parent, poi cerca un sottoinsieme di missioni
per alcuni worker che altrimenti farebbero PASS. Non c'è un nuovo dispatcher che
si accende a D15; ci sono invece regole a calendario ereditate nel piano e un
trattamento aggiuntivo che riesce ad aggirarne alcuni effetti nella seconda metà.

| Finestra senza sovrapposizione | PASS medi parent | PASS medi E18.30 | Riduzione | Top770, descrittivo |
|---|---:|---:|---:|---:|
| D1–D15 | 847,64 | 801,00 | 5,50% | 315,00 |
| D16–D30 | 720,43 | 289,29 | 59,85% | 199,00 |

Sette seed × due seat contro E18.16 per parent/candidata; cinque replay storici
final-770 per Top770. Quest'ultimo non è un confronto a parità di mercato/avversario.
Le finestre precedenti D1–D14 e D15–D30 restano nel JSON, non si mescolano con queste.

## Cause verificate nel codice e nei dati

1. **Apertura congelata:** il pool non opera a D1–D6 e lavora da H3 a H23.
   È stato un limite intenzionale dell'ablation, non una legge economica del gioco.
   Riferimento: `../tools/e18_30_mission_runtime.py`, `_prepare`, guard `day < 7`.
2. **Code personali ancora dominanti:** `_worker_command` del parent aspetta
   `row.turn`, o fa PASS se termina la propria coda. Il pool ammette solo worker
   con comando baseline PASS, senza inventario, con coda esaurita oppure un gap
   che consenta anche il ritorno. Non distribuisce globalmente il lavoro ordinario.
3. **Generatore ristretto:** recupera WATER già dovuti se l'ETA dell'owner sfora,
   PLANT→WATER pianificati a rischio, e fertilizzante disponibile non già prenotato.
   CARE, HARVEST e le normali semine/espansioni non sono un backlog comune ottimizzato.
   In tutti i 14 casi, **zero missioni del pool D1–D11** e PASS identici al parent.
   D8, D9, D10: rispettivamente 103, 97 e 105,64 PASS medi, senza intervento del pool.
4. **Svolta a calendario nel parent:** il piano contiene un cap di 3 raccolte
   fertilizzante a D16 e zero da D17 a D30. La routine `_animal_bundles` applica
   questi limiti. Prima, D7–D10 hanno sei raccolte pianificate al giorno; D11 tredici.
   Il runtime esclude le tile con raccolta ancora presente in qualunque coda parent.
   Da D16–D17 molte raccolte non sono più prenotate, quindi diventano eleggibili per
   il pool. Missioni fertilizzante medie: 9,86 a D16 e 9 a D17. Il beneficio è reale,
   ma soprattutto recupero di attività escluse dal vecchio piano, non prova che
   l'assegnazione globale sia già risolta.
5. **Altre differenze legacy:** personale di picco forzato da D16 a D30 e CARE
   disattivata a D19–D21 e D23–D25. Sono ulteriori regole datate, non un unico
   bilancio marginale dello stesso generatore. Il bridge HIRE opera ancora solo
   H1/H2. Non attribuire quantitativamente a ciascuna regola i PASS senza ablation.

## Cosa deve essere unico e cosa può variare

Un unico processo D1–D30: osservare → generare tutte le missioni candidate →
verificare cassa/scorte/capacità e ciclo completo → assegnare ai worker reali →
riconciliare l'esecuzione. Valutare rendimento netto per tempo totale, urgenza e
rischio, non soltanto distanza o il numero dei PASS.

Le attività scelte non devono essere identiche: prima contano investimenti e
attivazione della produzione, poi servizio/raccolta, alla fine la monetizzazione
entro il termine. Il tempo residuo e le scadenze biologiche sono vincoli legittimi.
Un cap di raccolta a zero da una data fissa non equivale a tale valutazione.

Direzione proposta, **non implementata in questa diagnosi**: trasferire anche
missioni ordinarie nel pool condiviso; separare le dipendenze reali dai turni
nominali delle vecchie code; valutare semine/animali con intero ciclo finanziato;
legare il personale al backlog utile e alla riserva per assunzioni/mangime/semi.
Mantenere 770, cap 14 e max 12 hands. Verificare distintamente D1–D15 e D16–D30
con lo stesso motore, includendo regressioni, stress di cassa e confronto E18.2.
Un PASS può comunque essere la scelta corretta se non esiste lavoro utile fattibile.

## Fonti e riproduzione

- Derivato con hash, 30 righe giornaliere e finestre:
  `../artifacts/derived/E18_30_PASS_PHASE_DIAGNOSIS_20260906.json`.
- Analizzatore: `../tools/analyze_e18_30_pass_phases.py`.
- Piano immutabile: `../artifacts/derived/E18_28_FULL_SEASON_C_PLAN_V1.json`.
- Pianificatore: `../tools/e18_18_capacity_trajectory_planner.py`,
  `_animal_bundles` e `build`.
- Esecutore code: `../tools/e18_19_retrying_trajectory_controller.py`,
  `_worker_command`; runtime pool: `../tools/e18_30_mission_runtime.py`.
- Grafici desktop: builder `../tools/build_e18_30_desktop_kpi.py`, dati invariati
  `../artifacts/derived/E18_30_TOP770_D01_D30_KPI_V3_MOBILE.json`. I 21 pannelli
  mantengono Top770 vs E18.30, mediana/min-max e definizioni standard V3.

Limite: questi derivati non contengono una partizione completa di ogni PASS V2 per
causa. Non presentare il vuoto del generatore come prova che tutti quei PASS siano
economicamente recuperabili, né dedurre le opportunità dalla sola cassa finale.
