import hashlib,json,sys
from pathlib import Path
from datetime import datetime,timezone
root=Path.cwd();b=root/'docs/model_specs/codex/e19/artifacts/derived'
manifest=json.loads((b/'v48_external_manifest.json').read_text(encoding='utf-8'))
for f in ['submission/submission_codex_e19_control_770_v2.py','submission/submission_codex_e18_770_assisted_start_v1_candidate.py']:
    manifest['sources'][f]=hashlib.sha256((root/f).read_bytes()).hexdigest()
manifest['validation']=dict(standalone_full_game_seed=180903001,seat=0,frozen_sides_equal=True,calls=719,errors=0,incomplete=0,local_policy_benchmark_cases=6)
(b/'v48_external_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
if len(sys.argv)>1:
    sid=None if sys.argv[1]=='unknown' else int(sys.argv[1]);status=sys.argv[2]
    url='https://www.kaggle.com/competitions/kaggriculture/submissions' + (f'?submissionId={sid}' if sid is not None else '')
    receipt=dict(submission_id=sid,status=status,url=url,observed_utc=datetime.now(timezone.utc).isoformat(),file=manifest['output'],sha256=manifest['sha256'],validation=manifest['validation'])
    (b/'v48_external_publication_receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    note=f'''# V48 pubblicata per benchmark esterno — 2026-09-08

Submission Kaggle {sid}, stato osservato {status}. File `{manifest['output']}`, SHA256 `{manifest['sha256']}`. URL: {url}
Policy V48 invariata. Bundle di 16 moduli verificati contro hash congelati; partita completa standalone seme 180903001 posizione 0 identica nei sides al riferimento, 719 chiamate, zero errori/incomplete. I sei benchmark locali della policy restano validi. Attendere i replay esterni per valutare generalizzazione; il punteggio locale non implica rating Kaggle. Nessuna variante 662. Diagnosi aperta: perdite produttive D16–D23, separandole da due fragole esaurite D28 senza produzione persa.

---

'''
    for f in [root/'docs/NEW_SESSION.md',root/'docs/PROJECT_STATE.md']:
        f.write_text(note+f.read_text(encoding='utf-8'),encoding='utf-8')
    print(json.dumps(receipt,indent=2))
