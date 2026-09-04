# Audit delta Foundation — evidenza E18.16

**Data:** 2026-09-04

**Esito:** `NO_FOUNDATION_REVISION_REQUIRED`

**Foundation verificata:** C2.1 reconciled

## Evidenza nuova

La linea exact `7-7-0` ha mostrato due fatti operativi:

1. con 14 pascoli disponibili, il provider poteva acquistare una quindicesima
   risorsa `COW`/`SHEEP`, lasciandola nello shed senza slot di collocamento;
2. un animale con `consecutive_unfed == 1` e `fed_today == false` richiede
   `FEED` entro l'EOD corrente per evitare la fuga deterministica.

E18.16 tratta il primo punto con un cap di policy sulle risorse complessive
(`tile + shed + worker inventory`) e il secondo con un guard FEED D20. Entrambi
sono vincoli del MODEL_SPEC Codex, non nuove leggi dell'ambiente.

## Copertura C2.1

- `LIV-STRUCT` definisce la capacità strutturale come conteggio di COOP e
  PASTURE; `POL-CAP` mantiene separata la capacità deliberativa servibile.
- `INV-02` espone l'inventario dettagliato dello shed e gli inventari worker
  sono osservabili: le risorse animali in transito sono quindi derivabili
  senza aggiungere stato engine-native.
- `ELG-20` descrive correttamente `BUY_ANIMAL`: l'engine verifica denaro,
  slot ordine e capacità shed, non la disponibilità di una struttura. Il cap
  14 è pertanto una scelta di policy.
- `LIV-05`, `LIV-07`, `LIV-08` ed `ELG-15`, insieme alla sequenza EOD 8.2
  della State Machine, coprono già integralmente la deadline FEED osservata.

## Decisione

Nessun file canonico della Foundation viene modificato. Aggiungere un feature
ID specifico per il cap 14 confonderebbe un parametro della strategia Codex
con il contratto ambientale. La sola azione necessaria è rendere esplicito nel
MODEL_SPEC E18.16 che il cap conta animali collocati e in inventario, cosa già
implementata e verificata dal gate di parità.
