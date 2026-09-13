# E22 Q0 8C9S — calendario esterno v2

Mandato: applicare il calendario ricorrente nei sei replay esterni, mantenendo distinto il braccio 8C9S dalla replica 6C10S. E22 pubblicata **56206528** e la variante 8C9S v1 rimangono congelate. Nessuna pubblicazione Kaggle.

Bundle autonomo: `submission/submission_codex_e22_q0_8c9s_calendar_v2.py`.

## Calendario adottato

| Casella | Collocamento | Raccolte |
|---|---|---|
| (3,2) | D11 H20 | D17, D20, D23, D26, D29 |
| (4,1) | D11 H21 | D17, D20, D23, D26, D29 |
| (2,3) | D12 H7 | D18, D21, D24, D27, D30 |

Coordinate zero-based, D/H one-based. In (4,1) si applica il ramo osservato con pecora, non quello vuoto. Le ore di raccolta dipendono dal primo slot disponibile nei nostri percorsi: non esiste un'unica ora comune ai sei replay. Ogni raccolta verifica resa presente, e nei giorni previsti ha precedenza su alimentazione/cure; il servizio prosegue negli altri slot. D30 mantiene il recupero della resa eventualmente rimasta.

Nella v1 le prime due raccolte finali slittavano a D30 e il collocamento della terza pecora era D12 H12. Anticipare il collocamento di cinque ore nello stesso giorno non anticipa il primo giorno produttivo: l'età degli animali nel motore è giornaliera.

## Percorso D12 senza manodopera aggiuntiva

L'acquisto della terza pecora passa da H2 a H1. L'operaio 1 la prende H2, raccoglie il latte in (2,4) H5, si porta in (2,3) e colloca la pecora H7. Rientra al magazzino H11 e consegna il latte; un ordine di vendita relativo al latte trasportato consente di monetizzare la consegna. Riprende poi le cure dei pascoli e le operazioni sulle colture, chiudendo con PLANT WHEAT H23 e WATER H24 in (0,5).

Il percorso elimina due slot di raccolta fertilizzante. L'operaio 6 conserva il percorso originario e il grano: PICKUP SHEEP H5 e PLACE SHEEP H12 non servono più; lo slot H12 viene riutilizzato per il servizio della pecora già presente. Il controllo dei risultati verifica anche le assunzioni giornaliere, le quantità acquistate e tutti i quantitativi piantati/raccolti rispetto alla v1.

La restante politica della v1 resta invariata, comprese le vendite di lana e le sue limitazioni di alimentazione. La variante è un trasferimento del calendario, non una copia del piano completo degli avversari o una nuova politica di recupero degli errori.

## Evidenza e protocollo

Fonti numeriche: 56020742 / 108544555, 56124096 / 108549619, 56171606 / 108558711, 56165125 / 108561064, 56198022 / 108562089, 56205921 / 108575585. [Estrazione e template osservato](reports/external_pasture_trajectories/REPORT.md).

Confronto seriale su 180911301–307 nei due ruoli contro E22 congelata. Confronto con v1 tramite i precedenti incontri sugli stessi seed/ruoli e contro lo stesso controllo; non è un incontro diretto v1-v2. Il mercato condiviso può modificare anche gli incassi del controllo. Seed 180912401–407 mantenuti riservati.

[Risultati e decisione](reports/q0_8c9s_calendar_v2/REPORT.md), [dashboard D1–D30](reports/q0_8c9s_calendar_v2/REPORT.html), [confronto v1](reports/q0_8c9s_calendar_v2/VS_V1.json), [verifiche](reports/q0_8c9s_calendar_v2/VERIFICATION.json).

Esito completo: 4/14 vittorie contro E22 (due seed su sette), margine medio +130,57, mediana −2.324. Rispetto agli incontri v1 con lo stesso controllo, delta margine medio −222,57, nessun seed migliore; delta della sola cassa del candidato −149,29. Tutti i collocamenti e giorni di raccolta rispettati, zero fughe/errori contabili, nessuna differenza nelle assunzioni giornaliere o nei quantitativi totali piantati, raccolti e acquistati rispetto a v1. Conservare il calendario come variante interna, senza promuoverlo: in questo mix cambia la monetizzazione ma non aumenta la produzione. I seed di conferma rimangono intatti.

Riproduzione con il Python del checkout originale: eseguire nella worktree `tools/build_q0_calendar_v2.py`, `tools/compare_q0_calendar_v2.py`, `tools/verify_q0_calendar_v2.py`, `tools/report_q0_calendar_v2.py`. I risultati esistenti vengono riusati solo con hash identici; una simulazione alla volta. La ricorrenza osservata motiva il trasferimento, ma non dimostra ottimalità nel mix 8C9S.
