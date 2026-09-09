"""D29: do not reserve service capacity for optional fertilizer collection."""


def install(core):
    cells=dict(zip(core._services.__code__.co_freevars,core._services.__closure__))
    assert 'services' in cells
    original=cells['services'].cell_contents
    def services():
        offers=original()
        if core.day!=28:return offers
        result=[]
        for target,commands,priority,value,kind in offers:
            filtered=[c for c in commands if c[0]!='COLLECT_FERTILIZER']
            if filtered:
                result.append((target,filtered,priority,value-(core._quote('FERTILIZER','SELL',1) if len(filtered)<len(commands) else 0),kind))
        return result
    cells['services'].cell_contents=services
