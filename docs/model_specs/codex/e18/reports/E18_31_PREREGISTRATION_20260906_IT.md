# E18.31 — assegnazione e investimento basati sullo stato

Stato: sviluppo, nessuna promozione o submission autorizzata da questo documento.
Priorità dell'utente: risolvere insieme PASS e ritardo mucche, con dettaglio D5–D10;
nessun altro filone prima di una verifica di entrambi.

Baseline congelata: E18.30 CROP_POOL V2. Solo simulatori e campioni interni.
Nessun dato, traiettoria o target giornaliero Top770 alimenta la nuova policy.
Invarianti: 7-7-0, massimo 14 animali, 9 COW + 5 SHEEP, massimo 12 manovali.

Ipotesi da verificare prima dell'implementazione:

- Il piano sovra-assegna personale rispetto al proprio lavoro pronto: distinguere
  code esaurite, attese di calendario e dipendenze reali negli step D5–D10.
- L'acquisto anticipato senza missione di collocamento immobilizza cassa. La
  decisione corretta deve collegare spazio, acquisto, tragitto, FEED e sostenibilità
  delle cure successive; non spostare semplicemente le date di acquisto.
- Un recupero che usa solo il fertilizzante non prenotato non può riparare questa
  lacuna iniziale. Le stesse condizioni di ammissibilità devono valere D1–D30.

Protocollo: traccia baseline, ablation separate assegnazione/espansione, combinata;
confronti appaiati sui sette seed di sviluppo già usati 180903001–180903007,
entrambi i posti, campioni E18.16 e E18.2/V4D. Holdout non usato per tarare.
Conservare anche esperimenti falliti e hash sorgente, non sovrascrivere E18.30.
Verificare denaro finale, PASS D5–D10 e D1–D15, COW-days e collocamenti,
animali immobilizzati, FEED/WATER effettivi, perdite, inventario finale e cap.
Meno PASS senza lavoro utile o con perdite biologiche non costituisce successo.

## Chiarimento del proprietario — stesso turno, prima della revisione V4

Non attendere una soluzione autonoma dei PASS prima dell'espansione animale:
le nuove mucche sono una possibile causa del recupero di capacità inutilizzata.
La decisione di investimento deve includere lavoro creato, raccolta anticipata
del fertilizzante e cure sostenibili. Prenotazioni/conferme sono vincoli della
decisione integrata, non un obiettivo sostitutivo o una fase da ottimizzare da sola.
V1–V3 restano esperimenti falliti, non candidati alla promozione.
