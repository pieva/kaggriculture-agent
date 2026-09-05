"""Task-local four-case visual QA, with geometry exposed as rendered DOM text."""

import html
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def main():
    document = (BASE / "reports/E18_29_B3_SIMULATION_REPORT_D01_D30.html").read_text(encoding="utf-8")
    inner = html.unescape(re.search(r'srcdoc="(.*?)"', document, re.DOTALL).group(1))
    qa_script = """<script>
    function inspect(){
      const root=document.getElementById('e29-simulation-d30');
      const svgs=[...root.querySelectorAll('section svg')];
      const info={width:innerWidth,panels:svgs.length,lines:root.querySelectorAll('[data-series-line]').length,
        axes:root.querySelectorAll('.axis-title').length,bars:root.querySelectorAll('[data-reason-bar]').length,
        series:[...root.querySelectorAll('button[data-series]')].map(b=>b.dataset.series),
        parentLines:root.querySelectorAll('[data-series-line="parent"]').length,
        overlap:svgs.filter(s=>s.getAttribute('data-label-overlap')==='true').length,
        overflow:[...root.querySelectorAll('*')].filter(e=>e.getClientRects().length).some(e=>e.getBoundingClientRect().right>innerWidth+1),
        theme:getComputedStyle(document.documentElement).colorScheme};
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
            case = inner.replace("</head>", f"<style>:root{{color-scheme:{theme}}}</style></head>")
            case = case.replace("</body>", qa_script + "</body>")
            body = f'<!doctype html><html><head><meta charset="utf-8"><title>E18.29 QA {width} {theme}</title><style>body{{margin:0;color-scheme:{theme}}}iframe{{width:{width}px;height:850px;border:0;display:block}}</style></head><body><iframe title="E18.29 report QA" srcdoc="{html.escape(case, quote=True)}"></iframe></body></html>'
            (output / f"E18_29_{width}_{theme}.html").write_text(body, encoding="utf-8")


if __name__ == "__main__":
    main()
