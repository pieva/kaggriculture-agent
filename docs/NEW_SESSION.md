# Nuova sessione — E23, architettura dal confronto con i top 2750–3000

La prossima sessione è dedicata a **E23**. Ripartire dal [brief E23](model_specs/codex/e23/README.md), non da ulteriori modifiche isolate al calendario E22.

## Prima lettura

1. [Atlante top 2750–3000](model_specs/codex/e22/reports/top_2750_3000_20260914/REPORT.html): 25 replay, topologie, collocamenti, percorsi e ricorrenze.
2. [Khalid vs E22.1](model_specs/codex/e22/reports/top_2750_3000_20260914/KHALID_VS_E22_1.md): stessa famiglia di strutture, variazione 8C6S/9C5S e Q3 solo in 2/5 replay.
3. [Registro bundle e pubblicazioni](model_specs/codex/e22/VERSIONS.json) e [stato del progetto](PROJECT_STATE.md).

## Stato salvato

- **E22.1 Q2 Grano v1:** submission **56228842, Complete**, verificata alla chiusura del 14/09/2026. Invio alle 12:36:55 Europe/Rome; primi risultati esterni da acquisire, senza reinviare. SHA256 `5db3ef642ddf8cac5a8797ee92baea40a7caa6ab9eb1908db482b7fdc3c4b18a`. [Report](model_specs/codex/e22/reports/e22_1_q2_grano_v1/REPORT.html): 20/20 scenari positivi, +68,15 medio; 14/14 vittorie dirette, +73,43 medio; stessa manodopera e mix 8C6S3G.
- **E22.2 fix v1:** submission 56228129, Complete all'ultima verifica. SHA256 `a9bdbcf5d0e2fefc7ecd2154336a69bf876ef52c7b8fcda2df81749abd492ac9`. [Report](model_specs/codex/e22/reports/e22_2_fix_v1/REPORT.html); la correzione meccanica non dimostra superiorità economica.
- Originali congelati: E22.1 submission 56206528, E22.2 submission 56212495. Nessuna policy E23 implementata.

## Obiettivo operativo

Acquisire i risultati esterni pendenti; confrontare i top per fasi, capitale, specie, Q3, colture e costo dei percorsi; formulare ipotesi economiche misurabili; progettare la nuova architettura E23 e testarne gli interventi separatamente, mantenendo report 22 KPI + prezzi e controlli contabili.

I semi 180911301–307 sono esposti; 180912401–407 restano riservati. Non assumere che la ricorrenza nei top equivalga a ottimalità. Nessun monitor automatico o nuovo task è stato avviato.

## Ripresa tecnica

Ramo corrente `codex/e22-2-pascoli-release`; usare questo workspace. Python: `C:/Users/pietr/Projects/kaggriculture-agent/.venv/Scripts/python.exe`. I report sono in `docs/model_specs/codex/e22/reports`; il server locale usa la porta 8768 quando attivo. Per E23 si può aprire un ramo dedicato con prefisso `codex/` dal commit di chiusura.

[Chiusura e cache locali](model_specs/codex/e22/reports/closeout_20260914/README.md) · [Cronologia della sessione E22](archive/E22_NEW_SESSION_20260914.md).
