# Proposta evolutiva: due E22 → due E23

Proposta progettuale, non implementata o valutata economicamente. Baseline correnti: E22.1 Q2 Grano 56228842 (8C6S3G), E22.2 fix Q2 Grano 56231638 (8C9S). E23 designa due ricette candidate tratte dal gruppo vicino a 3000, non submission esistenti.

| Ramo | Base E22 | Prima ricetta E23 proposta | Delta geometrico e animale |
|---|---|---|---|
| Con oche | 8C6S3G, 14 pascoli/3 pollai | 9C5S3G | Stesse strutture; pecora → mucca in (6,2), collocamento D10 H14 |
| Senza oche | 8C9S, 17 pascoli | 6C11S, variante D8 | Stesse strutture; mucca → pecora in (6,4) D8 H10 e (5,2) D8 H16 |

Sono scelte della specie prima del primo collocamento, non sostituzioni tardive di animali già presenti. Il ramo con oche 8C6S3G resta un controllo utile: nel replay Thomas 108922213 tutti i collocamenti animali coincidono con E22.1, inclusi giorni e ore. Le mappe colturali dei due replay coincidono nei primi 27 checkpoint giornalieri. Le conversioni fragola → grano D22–24 erano già in E22: non costituiscono da sole un'innovazione E23.

## Due possibili disposizioni 6C11S

- **D8, scelta evolutiva proposta:** mucche → pecore in (6,4) e (5,2). Verificata nello screening di Catalyst 108924584 e Deodims 108921530. Nel secondo replay, la casella (5,2) è occupata un'ora dopo il parent E22.2. Le mappe colturali ai checkpoint D20, D22, D25 e D28–30 coincidono col parent fix; mantenere in aggiunta Q2 Grano della nostra versione corrente.
- **D7, alternativa distinta:** mucche → pecore in (5,4) D7 H12 e (5,3) D7 H13. Ripetuta nei tre replay Thomas 108915255, 108908204, 108901867. Nel replay confrontato varia anche la successione tardiva: a D25 quattro caselle sono ancora a grano invece che a carote. Non combinare le due disposizioni come se fossero lo stesso piano.

Entrambe richiedono ripianificazione dei servizi. Esempio D8: pecora (6,3) collocata D9 H10 anziché H22, (6,2) D10 H8 anziché H14, (2,3) D12 H7 anziché H12. Il mix finale uguale non implica uguali cicli produttivi o rotte.

## Cosa conservare e cosa cambiare

Conservare le strutture alle stesse coordinate, il nucleo 33 fragole/25 grani, Q2 Grano e i controlli esecutivi già verificati nel fix E22.2. Valutare il trasferimento di questi controlli anche al ramo con oche, senza presumere che siano già tutti presenti in E22.1.

Adeguare acquisti e cassa alla specie scelta, disponibilità del mangime, CARE, FEED, raccolta, consegna e vendite latte/lana. La modifica di una specie non si riduce a cambiare BUY_ANIMAL e PLACE. Per la prima ablation conservare il calendario colturale E22; trasferire separatamente eventuali miglioramenti di servizi e vendite osservati nei top.

Nei singoli replay rappresentativi l'organico cumulato ai checkpoint è 260 giornate-manovale per entrambe le E22, 268 per i due rami Thomas con oche, 278 per Deodims senza oche e 281 per Thomas senza oche. Sono 8, 18 o 21 giornate-manovale aggiuntive, non ore o monete, e non una stima di fabbisogno minimo. I mercati dei replay sono differenti.

## Sequenza sperimentale

1. Congelare i due controlli E22 correnti e due ricette interne con/senza oche; nessun automatismo di scelta fra i rami nella prima prova.
2. Isolare il cambio di mix, con i soli servizi necessari a renderlo eseguibile. Nel ramo con oche includere anche il controllo 8C6S3G con gli stessi interventi esecutivi, per distinguere mix e robustezza.
3. Confrontare gli orari di servizio/raccolta/consegna osservati nei top come intervento separato, poi combinarli se utili.
4. Confronti accoppiati sui semi esposti, entrambi i ruoli, una simulazione alla volta. Misurare cassa e margine, prezzi realizzati, produzione venduta, costo lavoro, mangime, servizi mancati, scarti e residui. Semi riservati per conferma dopo la scelta.
5. Solo successivamente studiare una regola osservabile per scegliere fra i due portafogli; dieci pomodori/Q3 resta un intervento distinto.

La trasformazione è plausibile e localizzata nella geometria, ma il guadagno economico resta da misurare. Lo score dei top non è trasferibile copiando mix o mappa.

[Delta dettagliati dei replay](DETAILS.md) · [Dati estratti](PROFILES.json) · [Gruppo di confronto](../near3000_20260914/BENCHMARK_SET.md)
