"""Admit economic service missions only if observed biological work still fits."""
import ast
from pathlib import Path
from docs.model_specs.codex.e19.tools.wheat_safe_continuity import install as install_ranked


def install(core):
    install_ranked(core)
    services = core._services

    def split_services():
        offers = []
        for target, commands, priority, value, kind in services():
            offers.append((target, commands, priority, value, kind))
            essential = [c for c in commands if c[0] in {'FEED', 'WATER'}]
            # Preserve a short survival-only alternative when the full mission
            # would monopolize a worker needed by another observed obligation.
            # Replacement WATER belongs after PLANT, not to the old plant.
            if ['HARVEST'] in commands:
                essential = [c for c in commands[:commands.index(['HARVEST'])]
                             if c[0] in {'FEED', 'WATER'}]
            if essential and essential != commands:
                offers.append((target, essential, 3 if priority == 3 else 2, 1, 'ESSENTIAL'))
        return offers

    core._services = split_services
    # Duplicate short offers are scheduler alternatives, not extra obligations.
    certificate = core._day_route_certificate
    def deduplicated_certificate(worker, job, offers=None):
        offers = split_services() if offers is None else offers
        return certificate(worker, job, [s for s in offers if s[4] != 'ESSENTIAL'])
    core._day_route_certificate = deduplicated_certificate

    root = Path(__file__).resolve().parents[5]
    tree = ast.parse((root/'submission/submission_codex_e19_control_770_v2.py').read_text(encoding='utf-8'))
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'CommonController')
    method = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == '__call__')
    count = [0, 0, 0]
    for n in ast.walk(method):
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'score' for t in n.targets):
            n.value.elts[0] = ast.parse('2 * int(priority == 3) + int(priority == 4)', mode='eval').body
            count[0] += 1
        if isinstance(n, ast.If) and ast.unparse(n.test) == "job['kind'].startswith('NEW_')":
            n.test = ast.parse("job['kind'] != 'ESSENTIAL' and any(cmd[0] in {'PLANT', 'BUILD_PASTURE', 'PLACE', 'HARVEST', 'CARE', 'FERTILIZE', 'COLLECT_FERTILIZER', 'DIG'} for cmd, pos in job['steps'])", mode='eval').body
            count[1] += 1
        if isinstance(n, ast.If) and ast.unparse(n.test) == "steps is None and kind == 'SERVICE'":
            n.test = ast.parse("steps is None and kind in {'SERVICE', 'ESSENTIAL'}", mode='eval').body
            count[2] += 1
    assert count == [1, 1, 1], count
    namespace = {}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[method], type_ignores=[])), str(__file__), 'exec'), core.__call__.__func__.__globals__, namespace)
    core.__class__ = type('WheatReservedController', (core.__class__,), {'__call__': namespace['__call__']})
