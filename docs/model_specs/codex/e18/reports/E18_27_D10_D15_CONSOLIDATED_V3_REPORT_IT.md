# E18.27 V3 — risultati consolidati D10-D15

Candidata development, non promossa. Topologia 770, cap 14, massimo 12 hands. Chiusura D30 non modificata.

18 casi matched unici, 36 episodi unici (parent e candidata). Lo smoke seed 1 ripetuto nella matrice development è verificato identico e deduplicato.

## Confronti economici interni

Le prime due colonne sono le prestazioni del parent e della candidata contro lo stesso avversario: non sono il punteggio dell'avversario. Tutti i seed sono development già preregistrati.

| Avversario | Casi matched | E18.26 media | E18.27 V3 media | Delta | Delta % | Casi positivi | Avversario contro V3, media | Vittorie V3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| E18.16 | 14 | 60964.6 | 69156.0 | +8191.4 | +13.44% | 10/14 | 86316.0 | 0/14 |
| E18.25 | 2 | 63096.0 | 75002.5 | +11906.5 | +18.87% | 2/2 | 58562.0 | 2/2 |
| E18.2/V4D | 2 | 56543.0 | 57680.0 | +1137.0 | +2.01% | 1/2 | 85694.0 | 0/2 |

## Traiettoria D10-D15

Seed 180903001, entrambi i seat contro E18.16, mediane. Nelle coppie E18.26 / E18.27 V3. H24 è il checkpoint storico; la colonna successiva include anche l'ultimo batch della giornata, registrato nel primo stato del giorno dopo.

| D | Cassa H24 | Cassa dopo tutte le azioni D | Persone | Strawberry | Crop totali | Animali H24 |
|---:|---:|---:|---:|---:|---:|---:|
| 10 | 1451 / 1451 | 1451 / 1451 | 12 / 12 | 20 / 20 | 37 / 37 | 13 / 13 |
| 11 | 1128 / 3956 | 67 / 10321 | 9 / 12 | 20 / 20 | 37 / 25 | 13 / 13 |
| 12 | 236 / 9766 | 236 / 9766 | 9 / 12 | 29 / 38 | 51 / 50 | 13 / 13 |
| 13 | 9 / 12158 | 6399 / 14098 | 12 / 8 | 29 / 38 | 39 / 50 | 13 / 13 |
| 14 | 11630 / 14010 | 11697 / 14010 | 9 / 9 | 29 / 38 | 44 / 55 | 9 / 14 |
| 15 | 11728 / 13712 | 12591 / 14585 | 10 / 10 | 29 / 38 | 52 / 61 | 9 / 14 |

## Diagnosi dell'effetto

V1 anticipa HARVEST a D11: elimina le fughe nello smoke, ma vende in D12 e resta a 29 Strawberry. V2 completa DROP+SELL in D11 e attiva tutte le semine Q2 in D12, ma altera richieste di acquisto antecedenti D10 tramite l'orizzonte futuro. V3 mantiene il piano V2 e congela il fabbisogno futuro del mercato al parent fino a D9: il prefisso viene verificato come action stream completo, non soltanto come consistenze.

Sul seed 180903001 contro E18.16, V3 raccoglie/vende 71 Melon nelle azioni D11, incassando 12.445. Il checkpoint H24 è 3.956, ma dopo l'ultimo batch D11 la cassa è 10.321: l'ultimo incasso non va attribuito erroneamente a un nuovo giorno produttivo. Rispetto al parent viene sacrificata una sola unità Melon, mantenendo la copertura FEED e finanziando l'attivazione di 38 Strawberry in D12. Il target D15 è 38 Strawberry + 23 Wheat e 9 Cow + 5 Sheep.

Non è stata aggiunta una politica generale di refill: la candidata previene le fughe osservate; una risposta economica a perdite forzate resta da testare separatamente. Neppure una riserva finanziaria universale è stata dimostrata: l'evidenza riguarda questo trattamento e questi avversari/seed.

## Gate

```json
{
  "prefix_d1_d9_identical": true,
  "zero_errors": true,
  "zero_escapes": true,
  "feed_d11_d15_complete": true,
  "resources_cap_14": true,
  "hands_cap_12": true,
  "topology_770_d15_d30": true,
  "mix_9_5_d15_d30": false,
  "crops_d15_38_23": false,
  "melon_sold_by_d12": true,
  "matched_parent_positive": false,
  "incumbent_margin_nonnegative": false
}
```

Il planner espone ancora due FAIL legacy: picco 62 crop entro D13 (61 a D15) e output shadow almeno 885 (868). I vincoli di sicurezza, legalità e fattibilità passano; quei due target non vengono cancellati né convertiti silenziosamente in PASS. La candidata va giudicata anche sugli esiti reali matched, senza promuoverla soltanto perché supera E18.26.

## Prossima fase e limiti

La matrice estesa non ripete tutti i PASS dello smoke: nel seed 180903004 (entrambi i seat) e nel 180903005 seat 1 restano 37 Strawberry invece di 38 a D15. Nel seed 180903007 entrambi i seat arrivano a D10 con un animale già mancante e terminano con 9 Cow + 4 Sheep: nessuna fuga, ma acquisizione/placement non recuperato. Questi casi sono enumerati nel dataset consolidato.

Contro E18.16, i seed 180903003 e 180903004 sono negativi in entrambi i seat; worst delta -21.920. Nel seed 4 seat 0 la candidata è avanti di 1.115 a D15 e 2.164 a D20, ma perde 14.504 a fine partita. In D16-D30 vende 144 Milk contro 96 incassando 10.148 contro 20.442, e 142 Strawberry contro 116 incassando 8.703 contro 16.057. Il volume Wheat venduto scende da 353 a 316. Il vantaggio si deteriora già D20-D25: non basta attribuire tutto all'ultimo giorno o alla sola quantità prodotta. Offerta, prezzi realizzati e risposta avversaria richiedono ulteriore separazione causale.

Il miglioramento del parent non prova superiorità su E18.16 o E18.2/V4D: usare le colonne del confronto diretto e i relativi gate. E18.2/V4D è controllo competitivo storico con topologia diversa, non un benchmark architetturale omogeneo né una proposta di cambiare la 770. Lo smoke contro V4D usa un solo seed, non sette.

Nessuna submission, promozione, holdout/final confirmation, commit o push. La chiusura D30 resta una seconda fase: missioni complete di raccolta/consegna/vendita prima del taglio hands, valorizzazione dei residui e cutoff basati sul ritorno entro il termine. Conservare le ablation e verificare che eventuali nuove modifiche non riaprano il divario D10-D15.

Dataset consolidato: `E18_27_D10_D15_CONSOLIDATED_V3.json`.
