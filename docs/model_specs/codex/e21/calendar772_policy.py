"""Common-calendar diagnostic on the frozen published E20.1 772 dispatcher."""
from pathlib import Path
import runpy
ROOT=Path(__file__).resolve().parents[4]
PARENT=ROOT/'submission/submission_codex_e20_772_e20v28_loaderfix.py'
VERSION='CALENDAR772-C1'
def create_agent(context=None):
    bundle=runpy.run_path(str(PARENT))
    globals_=bundle['create_agent'].__globals__
    source=globals_['_BIO_SOURCE']
    def change(old,new,count=1):
        nonlocal source
        assert source.count(old)==count,(old,source.count(old))
        source=source.replace(old,new)
    change("targets={'WHEAT':23,'STRAWBERRY':38}","targets={'WHEAT':23,'STRAWBERRY':33}")
    change("if pos in intentions or isinstance(tile,dict)","if pos in core.e20_reserved or pos in intentions or isinstance(tile,dict)")
    change("            tile=core._tile(pos)\n            if core.day>=25:","            tile=core._tile(pos)\n            if core.day>=20 and intended=='STRAWBERRY':intended='WHEAT'\n            if core.day>=24:")
    change("intended=max(choices,key=lambda c:(core._quote(c,'SELL',rules['CROPS'][c]['max_yield'])-rules['CROPS'][c]['seed'])/(rules['CROPS'][c]['max_yield_day']+1))","intended='CARROT' if 'CARROT' in choices else choices[0]",2)
    globals_['_BIO_SOURCE']=source
    return bundle['create_agent'](context)
