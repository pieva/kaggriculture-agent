# H001: una richiesta di assunzione in meno all avvio di D20

Un seed per modello (180910201), ciascuno dal proprio stato originale. Prova del banco, non selezione di un candidato o confronto causale fra topologie. Il trattamento rimuove una richiesta HIRE una sola volta; le assunzioni successive restano libere.

| Modello | Cassa controllo | Cassa intervento | Delta | Esito |
|---|---:|---:|---:|---|
| E18 | 43673 | 51603 | +7930 | gain |
| E19 | 36786 | 40882 | +4096 | gain |
| E20.1 | 43717 | 44130 | +413 | gain |

Lettura competitiva supplementare, aggiunta dopo il pilota: anche l avversario reagisce e cambia cassa. Il margine non era un criterio preselezionato di H001 e va esplicitato nei protocolli successivi.

| Modello | Delta cassa avversario | Delta margine sullo stesso avversario |
|---|---:|---:|
| E18 | +3763 | +4167 |
| E19 | +9565 | -5469 |
| E20.1 | -5088 | +5501 |

## Reazione immediata delle assunzioni

Numero di manovali dopo i primi tre batch e prima dell ultimo batch di D20; farmer escluso. Questo distingue il mancato recupero del lavoratore da una diversa sequenza di assunzione.

| Modello | Condizione | Dopo H1 | Dopo H2 | Dopo H3 | Prima H24 |
|---|---|---:|---:|---:|---:|
| E18 | control | 6 | 12 | 12 | 12 |
| E18 | omit_one_hire | 5 | 11 | 11 | 11 |
| E19 | control | 6 | 11 | 12 | 12 |
| E19 | omit_one_hire | 5 | 12 | 12 | 12 |
| E20.1 | control | 6 | 12 | 12 | 12 |
| E20.1 | omit_one_hire | 5 | 12 | 12 | 12 |

## D20: intervento meno controllo

| Modello | Cassa | Assunzioni | Salari | Vendite | Acquisti | MOVE | PASS | WATER | FEED | CARE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| E18 | +144 | -1 | -144 | +0 | +0 | -15 | +0 | -13 | -5 | -5 |
| E19 | -100 | +0 | +0 | +0 | +100 | +12 | -10 | +1 | +0 | -1 |
| E20.1 | -875 | +0 | +0 | -770 | +105 | -6 | +0 | +2 | +0 | +0 |

## D20-D22: intervento meno controllo

| Modello | Cassa | Assunzioni | Salari | Vendite | Acquisti | MOVE | PASS | WATER | FEED | CARE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| E18 | +185 | -1 | -144 | +39 | -2 | -15 | +0 | -27 | -7 | -7 |
| E19 | -70 | +0 | +0 | +54 | +124 | +24 | -23 | +4 | -1 | -1 |
| E20.1 | -431 | +0 | +0 | -467 | -36 | +3 | +6 | -2 | +0 | -1 |

## D20-D30: intervento meno controllo

| Modello | Cassa | Assunzioni | Salari | Vendite | Acquisti | MOVE | PASS | WATER | FEED | CARE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| E18 | +7930 | -1 | -144 | +7884 | +98 | -23 | +18 | -52 | -15 | -13 |
| E19 | +4096 | +1 | +8 | +3828 | -276 | +68 | -45 | +21 | -5 | -7 |
| E20.1 | +413 | +0 | +0 | +457 | +44 | +48 | -60 | +8 | -8 | -4 |

## Sicurezza e validita

| Modello | Stress controllo / intervento | Fughe controllo / intervento |
|---|---:|---:|
| E18 | 22 / 34 | 0 / 1 |
| E19 | 6 / 5 | 0 / 0 |
| E20.1 | 3 / 0 | 0 / 0 |

Interpretazione del pilota: il guadagno di E18 non e accettabile come miglioramento, perche aumenta lo stress e compare una fuga animale. Il risparmio di salario e soltanto 144: la maggior parte del delta terminale deriva dalle vendite successive. E19 ed E20.1 recuperano rapidamente l organico; qui il trattamento cambia soprattutto la sequenza. I segni economici positivi non dimostrano una regola generalizzabile.

Il prossimo test deve separare numero di manovali, orario di disponibilita e assegnazione dei percorsi. Ogni nuova condizione va definita prima dei risultati e ripetuta su piu seed, senza accedere ai seed di validazione riservati.

Tutti e tre i controlli ricostruiscono 456 azioni per agente e riproducono le 263 coppie di azioni e i 263 stati successivi fino al terminale. Ogni ramo completa 719 chiamate per agente senza errori nei core che espongono il contatore. Si ignora nella parita solo il budget di tempo residuo, che dipende dal runtime. La prova non certifica il timeout della submission.

Gli agenti conservano le rispettive memorie ricostruite dalla propria storia e reagiscono alle osservazioni modificate. L intervento comprende cambi di assegnazione, rifornimenti, produzione e reazione dell avversario: non e una misura isolata del valore salariale di un lavoratore.

Nessuna promozione. Ogni effetto va replicato su un campione diagnostico piu ampio prima di trasformarlo in una regola. [Dati](H001_RESULT.json) - [Protocollo](../../PROTOCOL.md).
