# V26: crollo del grano a D21

## Risultato verificato

Il grano passa da22caselle al checkpointD20 a9aD21, poi6aD22.
I sei casi V26 hanno gli stessi valori. A D21 vengono raccolte38unita di
grano, aD22altre9; PLANT e zero per entrambe le giornate, per tutte le colture.
Non ci sono nuove infestanti aD21: le caselle raccolte restano vuote.
Questo e un difetto di successione, non un nuovo episodio di morte del grano.

## Perche la risemina non segue la raccolta

La V26 ha separato la raccolta in scadenza dal contratto NEW_ROTATION per
non perdere il prodotto quando il nuovo ciclo non passa. La raccolta ottiene
priorita6; dopo averla eseguita il grano sparisce e la semina torna NEW_CROP,
priorita0. Non eredita una prenotazione di tempo o un lavoratore dal raccolto.

Il pianificatore dei percorsi include servizi attuali, pascoli da riempire e
rinnovi di colture ancora presenti. Le semine sulle caselle gia vuote non
vengono inserite in quelle code: arrivano come alternative di crescita nel
selettore successivo. Il preparatore rifiuta pero una destinazione diversa
dalla testa della coda del lavoratore. Le semine competono quindi con code
gia occupate dai servizi; quando una coda finisce spesso resta poco tempo.

Audit deterministico seme180903001seat0, azioni identiche fino al passo528:
- D21: proposte di crescita su14destinazioni distinte;77valutazioni di percorso
  fattibili in alcune ore, ma nessuna semina assegnata. Nessun rifiuto del
  certificato di crescita: le opzioni non arrivano a vincere la selezione.
- D22: proposte su21destinazioni distinte, nessun percorso di semina accettato
  dal preparatore, quindi ancora nessuna valutazione del certificato.
- Tra i rifiuti del preparatore,1405aD21 e2110aD22 hanno destinazione diversa
  dalla testa della coda. Sono chiamate ripetute, NON lavori o PASS distinti.
  Altri rifiuti possono riguardare distanza, input, tempo o vincoli ulteriori;
  non sono stati tutti classificati separatamente.
- La cassa osservata D21 va da40894a46522, con riserva manutenzione massima1465:
  non e un blocco generale per assenza di denaro.

## La giornata e occupata soprattutto dagli spostamenti

| KPI | D21 | D22 |
|---|---:|---:|
| MOVE | 185 | 166 |
| PASS | 16 | 26 |
| WATER riusciti | 28 | 21 |
| FEED riusciti | 12 | 14 |
| CARE riusciti | 11 | 12 |
| PLANT | 0 | 0 |

A D21 i PASS arrivano soltanto nelle ultime3ore. Non e corretto descrivere
questa giornata come una grande disponibilita di persone ferme: il lavoro
viene consumato nei percorsi e nei servizi, senza prenotare la continuita
colturale. Il poco PASS non garantisce un buon risultato produttivo.

## Correzione indicata

La separazione dalla risemina deve proteggere il raccolto senza cancellare
l'impegno successivo. Il piano deve includere anche le future caselle vuote:
una prenotazione HARVEST seguita da PLANT/WATER nello stesso giorno o nel
primo giorno fattibile, con capacita riservata e responsabilita esplicita.
La scelta del ciclo successivo deve includere la finestra di chiusura.
Non basta aumentare ancora una priorita, e non serve introdurre DIG dove
il grano raccolto ha gia lasciato terreno vuoto.

## Correzione del report

Il generatore conteneva testo UTF-8 reinterpretato piu volte come Windows-1252.
Riparati i testi nel generatore build_harvest_deadlines_770_report.py e
rigenerati i tre report della cartella harvest_deadlines_770_20260908.
Scrittura e lettura esplicite UTF-8. Verificati titolo, assenza dei marcatori
di mojibake e manifest; i dati di simulazione e le policy non sono cambiati.

Evidenze: audit.json; script ../../tools/analyze_v26_wheat_d21.py.
L'audit riporta eventi del replay completo ma diagnostica decisionale solo
fino aD22; eventuali conteggi di offerte dopoD22 non sono misurati.
