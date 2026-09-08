# Piano biologico e del lavoro 770 — primo prototipo D1–D25

## Obiettivo e perimetro

Solo770. Un piano stabile di colture e servizi, corretto sulle osservazioni reali;
chiusura D26–D30 distinta ma considerata nelle scadenze già prima diD25.
Nessuna apertura della662 e nessuna nuova submission.

Il calendario di riferimento sotto è osservato nel Top770-001 già utilizzato,
non è il codice della sua policy né una ricostruzione delle sue aree. Le quantità
colturali coincidono nei cinque episodi fino aD25. Il programma del prototipo
non legge questi replay a runtime.

## Impegni biologici

- Grano: prima resa dopo2giorni, raccolta del ciclo completo a4giorni; programmare
  la nuova semina insieme alla raccolta. WATER nella finestra che incrementa la
  resa e quando necessario alla sopravvivenza. Mai saltare acqua al nuovo impianto.
- Fragole: prima produzione a10giorni, poi quattro eventi distanti2giorni.
  Acqua e fertilizzante devono precedere l'evento di produzione; raccogliere
  il prodotto disponibile e terminare il ciclo prima del deperimento.
- Animali: visita giornaliera FEED+CARE, raccolta del prodotto e fertilizzante
  quando presenti. Il CARE alimenta bonus per produzioni successive: non è un
  semplice extra da eliminare perché non genera cassa nella stessa ora.
- I cicli aperti entroD25 mantengono nel calendario gli eventi finoD30.
  Esempio: fragole impiantateD12 producono D22/D24/D26/D28. D26 non significa
  rimuoverle o ripartire da zero; significa riconsiderare la liquidazione.

## Organizzazione eseguibile introdotta

D1–D11 resta l'apertura assistita congelata, descritta dal calendario e verificata
azione per azione: questa parte NON è stata riscritta nel nuovo pianificatore.
D12–D25: intenzioni per casella fino a23grano/38fragole, conservando le colture
esistenti; aree contigue lungo una scansione serpentina, bilanciate con peso4
per animale e2per casella restante. I pesi sono una prima approssimazione, non
un certificato dei tempi. Divisione aggiornata all'inizio di ogni giornata con
il numero di lavoratori realmente presente. Preferenza territoriale morbida:
resta possibile l'aiuto fuori area. Prelievo grano per più animali dell'area
quando è già necessaria una visita al deposito e le scorte sono osservate.

V17 conserva troppo potere al vecchio selettore economico dei rinnovi e la
preferenza territoriale può prevalere su un percorso breve. V18 ammette semine
coerenti con l'intenzione usando cassa osservata, rinnovi alle scadenze del ciclo,
FEED giornaliero prioritario e penalità territoriale limitata a2azioni equivalenti.
Non è ancora un itinerario completo bloccato per tutta la giornata.

## Criterio di accettazione

Leggere insieme cassa propria/avversaria, cinque colture, MOVE/PASS, servizi,
perdite biologiche, infestanti e runtime. Nessuna promozione per una sola metrica.
Il certificato esistente dei nuovi investimenti protegge FEED/WATER del giorno:
NON dimostra la fattibilità di tutto il carico futuro. Prima di considerare
consolidato il piano serve un packing dei percorsi sui picchi futuri, comprensivo
di raccolte, CARE, fertilizzante e input condivisi. Questo limite rimane esplicito.

## Calendario osservato di riferimento D1–D25

Azioni riuscite per giorno, salvo MOVE richiesti; persone comprendono il farmer.
È un riferimento del carico effettivamente gestito dal Top, non una richiesta
di eseguire WATER su piante che non ne hanno bisogno né di assumere sempre13persone.

|D|Persone|Coltivate|Grano|Fragole|FEED|CARE|WATER|HARVEST|FERTILIZE|MOVE|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|1|6|19|7|0|2|4|19|0|0|49|
|2|5|19|7|0|4|4|7|0|0|30|
|3|5|19|7|0|4|5|22|3|0|59|
|4|6|19|7|0|3|5|23|4|0|72|
|5|5|19|7|0|5|6|10|3|0|54|
|6|6|19|3|4|6|6|23|4|0|65|
|7|9|31|7|12|8|8|28|5|0|102|
|8|9|37|9|16|7|10|29|0|0|103|
|9|11|37|5|20|11|13|40|7|0|125|
|10|12|37|5|20|13|13|41|6|0|131|
|11|12|34|13|21|13|13|21|15|0|150|
|12|12|58|20|38|13|13|57|4|0|114|
|13|10|62|24|38|13|13|23|11|0|107|
|14|11|59|21|38|14|14|64|7|0|118|
|15|11|61|23|38|14|14|47|13|4|115|
|16|13|61|23|38|14|14|51|15|8|139|
|17|13|61|23|38|14|14|52|21|4|142|
|18|13|61|23|38|14|14|44|19|7|160|
|19|13|61|23|38|14|14|49|27|4|135|
|20|13|61|23|38|14|14|46|18|8|149|
|21|13|61|23|38|14|14|50|27|12|134|
|22|13|61|23|38|14|14|35|36|5|146|
|23|13|61|27|34|14|14|48|26|1|139|
|24|13|61|35|26|14|14|39|32|0|131|
|25|13|61|39|22|14|14|55|21|8|130|
