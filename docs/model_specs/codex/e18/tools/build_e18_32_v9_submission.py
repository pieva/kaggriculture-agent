"""Build V9 separately; preserve the tested V7 artifact and manifest."""
from docs.model_specs.codex.e18.tools import build_e18_32_submission as builder

OUTPUT=builder.ROOT/'submission/submission_codex_e18_32_770_v9.py'


def main():
    builder.OUTPUT=OUTPUT
    builder.VERSION='E18.32-DEMAND-RELEASE-770-V9'
    builder.GATE=builder.DERIVED/'E18_32_READY_WORK_GATE_RELEASE_V9_DEVELOPMENT_20260906.json'
    builder.MANIFEST=builder.DERIVED/'E18_32_SUBMISSION_MANIFEST_V9.json'
    builder.build()


if __name__=='__main__':
    main()
