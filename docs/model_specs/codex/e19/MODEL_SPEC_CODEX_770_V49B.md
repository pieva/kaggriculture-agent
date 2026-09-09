# Codex 770 V49B — revisione respinta

Variante locale non pubblicata, successiva alla [V49 A](MODEL_SPEC_CODEX_770_V49.md).
Limita il recupero a visite di un comando nell'ultimo tick del giorno e la
riduzione del target di manovali a una persona rispetto all'estimatore V48.
Sul seed di sviluppo 180903003 posto 0: cassa 62.007 contro 62.931, PASS 1.057
contro 1.076, MOVE 3.507 contro 3.488. Gate MOVE non superato; perdita economica.
Non estesa alla validazione. Nessun dato di validazione ha orientato la modifica.

Sorgenti: `tools/local_service_770_v49b.py`, `tools/workload_770_v49b.py`,
`tools/policy_770_v49b.py`, builder `tools/build_v49b_submission.py`.
Tutti i 18 sorgenti V48 sono ereditati invariati. Hash e inventario completo:
[manifest B](reports/pass_reduction_v49_20260909/candidate_b_manifest.json).
Risultato: [screen B](reports/pass_reduction_v49_20260909/development_v49b_180903003_0.json).
Revisione successiva: [V49C](MODEL_SPEC_CODEX_770_V49C.md).
