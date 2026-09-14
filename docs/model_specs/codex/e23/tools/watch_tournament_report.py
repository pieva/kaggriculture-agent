"""Refresh the local tournament artifact as this finite experiment progresses."""
import contextlib,importlib,io,json,sys,time
from pathlib import Path
import report_tournament4 as report
import diagnose_tournament5 as diagnose
ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/model_specs/codex/e23/reports/tournament5_v1'

def main():
 last=-1
 while True:
  n=len(list((OUT/'matches').glob('E*.json')))
  if n!=last:
   try:
    sys.argv=[__file__,'--five']
    with contextlib.redirect_stdout(io.StringIO()):
     importlib.reload(report);report.main();diagnose.main()
    last=n
    summary=json.loads((OUT/'SUMMARY.json').read_text())
    print(json.dumps(dict(completed=n,expected=140,standings=[dict(version=s['key'],played=s['n'],wins=s['wins'],mean_margin=round(s['margin_mean'],1)) for s in summary['standings']])),flush=True)
    if n==140:break
   except json.JSONDecodeError:pass  # A match result is being written; retry once complete.
  time.sleep(10)

if __name__=='__main__':main()
