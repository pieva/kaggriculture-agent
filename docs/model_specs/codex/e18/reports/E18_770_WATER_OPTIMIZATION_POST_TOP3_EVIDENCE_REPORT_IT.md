# E18 7-7-0 — ottimizzazione WATER dopo il benchmark Top-3

## Decisione

E18.10 V2 resta il controllo congelato `7-7-0`; E18.16 diventa la nuova base
di ricerca dopo avere passato Gate A con cap 14 e safety FEED. Gate B Top-3
resta fallito e non è autorizzato alcun holdout, final-confirmation o upload
Kaggle. L'evidenza WATER converge su una conclusione: il maggior WATER dei top
non è una leva isolata, ma l'effetto osservabile di un lifecycle crop più
denso e di rotte che completano il lavoro locale.

## Esperimenti chiusi

| Variante | Evidenza | Esito |
|---|---|---|
| E18.11 invalid-command → WATER | 14 match; WATER `+0,97%`, money e output invariati | respinta: accounting, non valore |
| E18.12 cap bestiame 14 | spot; blocca il 15° animale, perdita D20 invariata e rimpiazzo entro D21 H23 | cap accettato come invariante; performance standalone neutra |
| E18.13 deadline FEED D20 | 14 match; perdite `0` vs `14`, money medio `+0,33%`, worst matched `-2,85%` | respinta: rischio di coda |
| E18.14 coop → crop | spot; WATER `+2,05%`, MOVE `-0,39%`, money `-2,94%` | respinta: lavoro oca liberato ma non ripianificato |
| E18.15 hand WATER Q2 | spot D15–D19; WATER `+21`, output e stress invariati, money `-1.165` | respinta: costo pari ai 5 hire |
| E18.16 cap 14 + FEED | 14 match; perdite `0` vs `14`, money `+1,18%`, worst `-0,95%`, record `8–6` | Gate A PASS; nuova base di ricerca |

Il 15° animale nasce da un buffer legacy: dopo aver raggiunto 14 risorse a D12
H2, il provider emette ancora `BUY_ANIMAL SHEEP 1` a D12 H3 e il cap 15 lo
ammette. E18.12 lo blocca; il risultato economico resta neutro solo perché la
morte D20 obbliga poi a comprare un rimpiazzo.

E18.13 dimostra che una correzione locale può eliminare la morte, ma lasciando
anche il quindicesimo animale nello shed peggiora la coda. E18.16 chiude le due
metà dello stesso difetto: salva il quattordicesimo pascolo senza comprare il
surplus, portando il worst da `-2,85%` a `-0,95%`. E18.15 resta il test causale
più netto sulla tesi WATER: 21 azioni aggiuntive non producono un solo harvest
o unità in più e non riducono il late unwatered.

## Evidenza di fase contro gli exact 7-7-0 top

| Fase | Profilo | MOVE | PASS | WATER | HARVEST | PLANT | DIG |
|---|---|---:|---:|---:|---:|---:|---:|
| D1–D10 | E18.10 V2 | 672 | 364 | 239 | 35 | 63 | 0 |
| D1–D10 | top exact 770 | 779 | 235,7 | 252 | 32 | 63 | 0 |
| D11–D20 | E18.10 V2 | 1396 | 342 | 375 | 135 | 73 | 10 |
| D11–D20 | top exact 770 | 1327 | 172,3 | 464 | 150 | 90 | 5 |
| D21–D30 | E18.10 V2 | 1534 | 143 | 311 | 233 | 66 | 37 |
| D21–D30 | top exact 770 | 1354,3 | 121,7 | 454,7 | 285 | 90 | 38 |

Il gap si apre soprattutto da D11: i top combinano più PLANT, WATER e HARVEST
con meno MOVE e PASS. Non basta aggiungere WATER allo stream esistente; serve
rendere coerenti calendario, assegnazione e completamento delle rotte.

## Specifica proposta per E18.17

Nome di lavoro: `770 synchronized crop lifecycle / route completion`.

Vincoli congelati:

- topologia e fill esatti `7-7-0`;
- farmer più 12 hands, senza hire aggiuntivi;
- base E18.16: coop/oca invariati, cap COW/SHEEP 14 e safety FEED D20;
- nessun overlay post-provider e nessuna regola legata a nomi o replay;
- decisioni soltanto da stato pubblico corrente.

Unica famiglia causale: ripianificare in modo coerente la fase crop D11–D30.
Ogni missione deve chiudere il cluster locale prima di attraversare un
quadrante; WATER e HARVEST sono ordinati per età/stress/deadline; DIG è ammesso
solo quando esistono insieme seed di sostituzione e assegnazione del worker.

I profili top sono target diagnostici, non una schedule da copiare. Il gate di
fase deve richiedere almeno la direzione seguente rispetto a E18.10 V2:

- D11–D20: più PLANT/WATER/HARVEST, MOVE sotto 1396 e PASS nettamente sotto
  342;
- D21–D30: più WATER/HARVEST/PLANT, MOVE sotto 1534 e PASS sotto 143;
- output finale superiore, non soltanto contatori di servizio;
- nessuna regressione di topologia, fill, safety o worst matched money.

La prima implementazione deve strumentare KPI per fase e route completion.
Solo dopo un segnale positivo su sviluppo si preregistrano soglie numeriche
contro il controllo; holdout e upload rimangono bloccati.
