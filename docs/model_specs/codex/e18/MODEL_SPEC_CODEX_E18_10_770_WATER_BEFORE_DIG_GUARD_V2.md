# MODEL_SPEC Codex E18.10 V2 — safe PASS-only WATER-before-DIG

## Correzione V1

V1 è invalidata: inserendo WATER nella task queue poteva sovrascrivere un
comando non-PASS sullo shed access `(4,5)`. V2 conserva la stessa ipotesi ma
sposta l'override dopo E18.9 e ammette esclusivamente:

`provider PASS + worker già sul target + Strawberry vivo unwatered → WATER`.

Qualsiasi comando non-PASS emesso dal controllo E18.9 resta bit-for-bit
autorevole. Il target `(4,5)` è escluso perché è anche uno shed access e deve
restare disponibile alla logistica. Non sono
ammessi move, routing, market mutation, variazioni di worker, cap o topologia.

## Controllo e gate

Controllo E18.9, topologia/fill `7-7-0`, 14 match development su sette seed e
entrambi i seat. Le soglie restano quelle preregistrate per V1:

- fill esatto 14/14 in tutti i match, zero perdite/errori/fallback/breach;
- WATER e crop service almeno `+1%`, PASS almeno `-1%`;
- late unwatered almeno `-2%`, harvest e unità almeno `+1%`;
- late crop tile-days non inferiori, DIG non superiori, move non oltre `+1%`;
- money medio non sotto `-2%`, worst matched almeno `-5%`.

Gate B Top-3 resta diagnostico e invariato. Holdout, final e upload non sono
autorizzati.

## Esito development — 2026-09-04

Gate A `FAIL` su tre sole soglie di volume, Gate B `FAIL`; nessuna promozione
formale. Safety e integrità passano: fill esatto `14/14` in `14/14`, perdite
uguali al controllo, zero errori, fallback, breach, route mutation e override
non-PASS. Record `12–2`; money medio `+1,70%`, matched medio `+1,46%`, worst
`-0,05%`. WATER `+1,77%`, DIG `-11,44%`, late unwatered `-4,10%`, late crop
tile-days `+5,21%`, harvest riusciti `+1,77%`, move `-0,22%` e ratio
`-0,42%`. Restano sotto soglia crop service `+0,51%`, unità raccolte `+0,58%`
e PASS `+0,22%`. È la migliore candidata 770 di ricerca, ma non è ancora una
release.
