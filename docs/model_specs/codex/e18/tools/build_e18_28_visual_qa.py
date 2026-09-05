"""Disposable local preview cases with real iframe widths and color schemes."""

import html
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def main():
    reference = (BASE / "reports/E18_28_TOP770_D01_D30_KPI_19.html").read_text(
        encoding="utf-8"
    )
    inner = html.unescape(re.search(r'srcdoc="(.*?)"', reference, re.DOTALL).group(1))
    # The QA document exports only DOM geometry, not runtime app state. The
    # production report remains sandboxed; this task-local QA frame is same-origin.
    qa_script = """<script>
    function inspect(){
      const svgs=[...document.querySelectorAll('section svg')];
      const info={width:innerWidth, panels:svgs.length, lines:document.querySelectorAll('[data-series-line]').length,
        axes:document.querySelectorAll('.axis-title').length,
        overlap:svgs.filter(s=>s.getAttribute('data-label-overlap')==='true').length,
        overflow:[...document.querySelectorAll('#top770-e28-diagnostic-d30 *')].some(e=>e.getBoundingClientRect().right>innerWidth+1)};
      let output=document.getElementById('qa-output');
      if(!output){output=document.createElement('output');output.id='qa-output';output.style.overflowWrap='anywhere';document.body.prepend(output)}
      output.textContent='QA '+JSON.stringify(info);
    }
    new ResizeObserver(inspect).observe(document.body);setTimeout(inspect,2000);
    </script>"""
    output = BASE / "reports/qa"
    output.mkdir(exist_ok=True)
    for width in (360, 736):
        for theme in ("light", "dark"):
            case = inner.replace(
                "</head>", f"<style>:root{{color-scheme:{theme}}}</style></head>"
            )
            case = case.replace("</body>", qa_script + "</body>")
            body = f'<!doctype html><html><head><meta charset="utf-8"><title>E18.28 QA {width} {theme}</title><style>body{{margin:0;color-scheme:{theme}}}iframe{{width:{width}px;height:720px;border:0;display:block}}</style></head><body><iframe title="E18.28 report QA" srcdoc="{html.escape(case, quote=True)}"></iframe></body></html>'
            (output / f"E18_28_{width}_{theme}.html").write_text(body, encoding="utf-8")


if __name__ == "__main__":
    main()
