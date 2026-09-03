# Protocollo Codex — monitor Kaggle E18.1 e trigger V2

## Ambito

- submission Kaggle: `55981615`;
- episodio iniziale noto: `105139822`;
- URL: `https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=55981615&episodeId=105139822`;
- frequenza richiesta: una rilevazione ogni ora, fuso `Europe/Rome`;
- ruolo: validazione esterna diagnostica, non promozione automatica.

## Snapshot valido

Ogni rilevazione deve contenere:

1. timestamp ISO con fuso;
2. score/rating pubblico numerico della submission;
3. stato della submission e indicazione di match in corso, se disponibile;
4. insieme degli episode ID visibili e numero di episodi completati;
5. eventuale errore di autenticazione o pagina incompleta.

Uno snapshot senza score numerico, proveniente da una pagina non autenticata o
con contenuto non caricato non è valido e non entra nella finestra.

## Regola di stabilizzazione

La situazione è `STABLE` soltanto quando esistono quattro snapshot validi e
consecutivi, distanziati di circa un'ora e distribuiti su almeno tre ore, tali
che:

```text
max(score_1..score_4) - min(score_1..score_4) < 50
```

Inoltre ogni delta adiacente deve avere valore assoluto <50. La formulazione
usa un intervallo totale inferiore a 50, non l'ambigua espressione `±50` che
permetterebbe una banda larga 100 punti.

Per evitare una falsa stabilità da pagina congelata, almeno una delle seguenti
condizioni deve essere vera:

- nella finestra compare almeno un nuovo episodio completato;
- Kaggle dichiara esplicitamente conclusa l'elaborazione e negli ultimi due
  snapshot non risultano match in corso.

Una variazione ≥50 azzera il contatore e apre una nuova finestra. Errori di
login/rete non azzerano gli snapshot validi precedenti ma non contano come
ora osservata.

## Comportamento delle notifiche

- non notificare a ogni ora se lo stato è invariato e non azionabile;
- notificare autenticazione scaduta, pagina illeggibile o variazione ≥50;
- notificare una sola volta il passaggio a `STABLE`, includendo i quattro
  score, intervallo, timestamp ed episode count;
- dopo `STABLE`, disattivare il polling durante analisi e sviluppo per evitare
  un secondo trigger concorrente.

## Azioni autorizzate dopo STABLE

1. Enumerare tutti gli episode ID attribuiti alla submission `55981615`.
2. Recuperare i replay mancanti in una directory temporanea, verificando
   episode ID e SHA-256; non versionare i JSON grezzi.
3. Aggiornare `data/replays/json/json.md` con catalogo e provenienza.
4. Costruire artifact derivati e un report per tutti i replay, includendo:
   money, win/loss, seat, avversario e proxy di pressione; decisione di regime;
   topologia per quadrante e giorno di attivazione; crop lifecycle, raccolto,
   weed, irrigazione, workforce, backlog; zootecnia e perdite verificate;
   divergenza fra classi di avversario e fra fasce di rating osservato.
5. Verificare esplicitamente se `7-7-0` viene mai attivato. Se resta 0%,
   classificare E18.1 come selector non calibrato sull'ambiente esterno.
6. Sviluppare una nuova candidate Codex in nuovi path V2, senza modificare il
   freeze E18.1. Le soglie devono derivare dal corpus stabile, non dal nome o
   rating dell'avversario e non da memoria cross-episode non disponibile.
7. Eseguire soltanto i seed development E18 e il torneo a quattro congelato.
   Holdout/final restano non autorizzati; nessuna submission Kaggle automatica.

## Gate Codex V2

- media development ≥100.000;
- zero errori/fallback/perdite verificate;
- almeno due regimi realmente attivati nel pool;
- divergenza condizionata di azioni e architettura ≥12/14;
- nessuna regressione >5% contro E17 V4D nello scontro diretto e nello stesso
  pool comune; E18.1 resta una sonda architetturale, non il controllo
  economico;
- report separato fra prestazione locale e validazione esterna.

## Stato operativo

`NOT_SCHEDULED`: il protocollo è pronto, ma deve essere installato tramite il
meccanismo nativo di automazione quando disponibile. Non sostituire con un
Windows Scheduled Task o uno script cron esterno.
