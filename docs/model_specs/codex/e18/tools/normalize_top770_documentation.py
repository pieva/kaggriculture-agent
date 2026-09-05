"""Mechanical documentation-only aliasing; frozen runtime identifiers stay intact."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
NAME = re.compile(r"jesse(?:[\s_]+bullard)?", re.IGNORECASE)


def alias(text):
    return NAME.sub(lambda m: "TOP770" if m.group().isupper() else "Top770", text)


def main():
    paths = sorted(
        p
        for directory in (ROOT / "docs", ROOT / "experiments")
        for p in directory.rglob("*.md")
    )
    moves = {}
    for path in paths:
        if NAME.search(path.name):
            name = alias(path.name).replace("TOP770_770", "TOP770")
            target = path.with_name(name)
            assert target.is_relative_to(ROOT) and not target.exists(), target
            moves[path] = target
    changed = []
    retained = []
    for path in paths:
        old = path.read_text(encoding="utf-8")
        text = old
        for source, target in moves.items():
            text = text.replace(source.name, target.name)
        protected = []

        def protect(match, protected=protected):
            value = match.group()
            if value.startswith("```") and not re.match(
                r"```(?:json|python|py|bash|powershell)\b", value
            ):
                return alias(value)
            if NAME.search(value):
                protected.append(value)
                return f"@@TECHNICAL_REFERENCE_{len(protected) - 1}@@"
            return value

        # Keep historical executable paths and source-schema keys accurate.
        text = re.sub(r"```[\s\S]*?```", protect, text)
        text = re.sub(r"`[^`\n]*(?:\.json|\.py|\.csv)[^`\n]*`", protect, text)
        text = re.sub(r"\]\([^\n)]*\)", protect, text)
        text = alias(text)
        for index, value in enumerate(protected):
            text = text.replace(f"@@TECHNICAL_REFERENCE_{index}@@", value)
        if text != old:
            path.write_text(text, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))
        retained.extend(str(path.relative_to(ROOT)) for _ in protected)
    for source, target in moves.items():
        source.rename(target)
    # Only report destinations are renamed; controller/config/plan IDs are not.
    generators = []
    for path in (ROOT / "docs/model_specs/codex/e18/tools").glob("*.py"):
        old = path.read_text(encoding="utf-8")
        text = old
        for source, target in moves.items():
            text = text.replace(source.name, target.name)
        if text != old:
            path.write_text(text, encoding="utf-8")
            generators.append(str(path.relative_to(ROOT)))
    print(
        {
            "documents_updated": len(changed),
            "documents_renamed": len(moves),
            "report_destination_updates": generators,
            "preserved_technical_references": len(retained),
        }
    )


if __name__ == "__main__":
    main()
