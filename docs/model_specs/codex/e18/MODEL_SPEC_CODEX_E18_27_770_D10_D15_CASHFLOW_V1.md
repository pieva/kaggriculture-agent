# MODEL SPEC — Codex E18.27 770 D10-D15 Cashflow V1

## Stato e preregistrazione

2026-09-05: candidata development in costruzione, non promossa, nessun upload.
Parent E18.26 congelato; target 7-7-0, 14 pascoli/animali, mix 9 Cow + 5
Sheep, massimo 12 hands. D30 escluso dal trattamento.

Prima ablation: raccolto Melon D11 invece di D13 e almeno 11 hands in D11
per finanziare/eseguire le missioni di raccolta, servizio e consegna.
Nessuna altra regola di mercato, refill, semina o chiusura cambia in V1.
L'obiettivo iniziale è stabilire quanto risolve l'anticipo dei ricavi prima
di aggiungere guardie finanziarie o ripianificare altri cicli.

D1-D9 deve essere identico al parent sia come piano sia come action stream
nei confronti matched. D10 resta nel perimetro ammesso ma non viene alterato
deliberatamente da questa prima ablation. Le regole D16-D30 rimangono quelle
del parent; gli stati possono divergere per conseguenza del trattamento.

## Gate

1. Planner: zero azioni illegali, fughe o starvation nello shadow; percorsi
   entro 24 turni e 12 hands, cap/topologia conservati. Eventuali gate
   legacy di composizione/output devono essere esposti, non cancellati.
2. Smoke preregistrato: seed 180903001, entrambi i seat contro E18.16 ed
   E18.25, confrontando anche E18.26 sugli stessi opponent/seed/seat.
3. Verificare incassi Melon D11-D12, FEED D11-D15 completo, zero fughe su
   D1-D30, mix 9+5 a D15 e D30, cassa e composizione giornaliere.
4. Delta finale positivo matched in entrambi i seat; distinguere il delta
   sul parent dal margine contro l'incumbent. Target crop D15: 38 Strawberry
   + 23 Wheat, con ogni scarto dichiarato.
5. Solo dopo i gate precedenti: estendere ai sette seed development
   180903001–180903007 del manifest e confrontare E18.2/V4D. Nessun holdout
   o final confirmation. Nessuna submission di una candidata fallita.

Fonte della diagnosi e programma successivo:
`reports/E18_26_D10_D15_CASH_FEED_DIAGNOSIS_AND_NEXT_PRIORITIES_IT.md`.

## Artefatti

- config: `configs/CODEX_E18_27_770_D10_D15_CASHFLOW_V1.json`;
- controller/builder: `tools/e18_27_d10_d15_cashflow_controller.py`;
- piano: `artifacts/derived/E18_27_770_D10_D15_CASHFLOW_PLAN_V1.json` (da generare);
- i risultati non sono ancora disponibili alla preregistrazione.

## Primo risultato e ablation V2 preregistrata

V1: smoke completato su 8 match (4 coppie matched). Zero fughe, FEED completo
D11-D15, mix 9+5 D15/D30 e prefisso D1-D9 identico. Reward contro E18.16
61.934/62.944 (parent 54.761/53.968); contro E18.25 75.682/75.522 (parent
63.172/63.020). Rimangono 29 Strawberry invece di 38; i 71 Melon vengono
raccolti D11 ma venduti D12. V1 non è promossa.

V2, da verificare separatamente: stessa raccolta D11, tutte le semine Q2
pianificate D12 dopo l'incasso, almeno 11 hands D11-D12 e SELL nello stesso
batch dei DROP Melon effettivamente emessi, usando inventari osservati.
Nessun cambiamento alle regole di chiusura/ritiro. Il posticipo delle semine
Q2 cambia la successiva età biologica, che va misurata fino a D30.
Prima verifica: medesimo smoke contro E18.16 ed E18.25, entrambi i seat,
confronto con parent e con V1 congelata. Gate e seed invariati; nessuna
promozione giustificata dalla sola cassa D11.

V2 mostra nello smoke un prefisso di ordini D1-D9 diverso dal parent:
l'orizzonte di acquisto a cinque giorni vede le nuove date Q2. Questo viola
l'isolamento preregistrato, anche quando le consistenze D10 coincidono.
V3 corregge soltanto questa retroazione: prima di D10, i fabbisogni futuri
del mercato sono quelli E18.26; da D10 usa il piano candidato. Piano offline
identico V2/V3. V3 deve ripetere lo smoke e dimostrare hash action stream
D1-D9 identico al parent prima di qualsiasi estensione della matrice.
