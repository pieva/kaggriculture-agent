"""Local diagnostic: Repair2 opening, fixed774 geometry, observed-state calendar.

Reuses the existing V48 mission/route machinery; this is a calendar plus
dispatcher transfer, not a pure calendar ablation and not a public release.
"""
from pathlib import Path
from dataclasses import replace
import runpy,sys
ROOT=Path(__file__).resolve().parents[4]
VERSION='E21-CALENDAR774-C1'
ANIMALS={(4,1):'GOOSE',(3,2):'SHEEP',(4,2):'COW',(5,2):'COW',(6,2):'SHEEP',
 (3,3):'SHEEP',(4,3):'COW',(5,3):'COW',(2,4):'COW',(3,4):'SHEEP',
 (4,4):'COW',(5,4):'COW',(6,4):'COW',(7,4):'SHEEP',
 (3,5):'SHEEP',(4,5):'SHEEP',(3,6):'SHEEP',(4,6):'SHEEP'}
RESERVED=set(ANIMALS)|{(6,3)}

class Calendar774:
    def __init__(self,context=None):
        self.opening=runpy.run_path(str(ROOT/'submission/submission_codex_e21_774_repair2.py'))['create_agent'](context)
        bundle=runpy.run_path(str(ROOT/'submission/submission_codex_e18_770_v48_external.py'))
        module=sys.modules['_v48pkg.biological_plan_770_v48']
        source=(ROOT/'docs/model_specs/codex/e19/tools/biological_plan_770_v48.py').read_text(encoding='utf-8').replace('docs.model_specs.codex.e19.tools.','_v48pkg.')
        source=source.replace("targets={'WHEAT':23,'STRAWBERRY':38}","targets={'WHEAT':23,'STRAWBERRY':33}")
        source=source.replace("if pos in intentions or isinstance(tile,dict)","if pos in RESERVED or pos in intentions or isinstance(tile,dict)")
        source=source.replace("if pos in claims:continue\n            tile=core._tile(pos)","if pos in RESERVED or pos in claims:continue\n            tile=core._tile(pos)")
        # Ended strawberry cycles return to wheat; the final annual phase
        # prefers carrot only when maturity and one delivery day still fit.
        needle="            tile=core._tile(pos)\n            if core.day>=25:"
        assert source.count(needle)==1
        source=source.replace(needle,"            tile=core._tile(pos)\n            if core.day>=20 and intended=='STRAWBERRY':intended='WHEAT'\n            if core.day>=24:")
        source=source.replace("intended=max(choices,key=lambda c:(core._quote(c,'SELL',rules['CROPS'][c]['max_yield'])-rules['CROPS'][c]['seed'])/(rules['CROPS'][c]['max_yield_day']+1))","intended='CARROT' if 'CARROT' in choices else choices[0]")
        module.RESERVED=RESERVED
        scope=dict(module.__dict__);exec(compile(source,'<calendar774-biological>','exec'),scope)
        module.install.__code__=scope['install'].__code__
        self.planner=bundle['create_agent'](context);self.core=self.planner.core
        self.core.profile=replace(self.core.profile,target=18,maximum_hands=12,mix_weights=(('COW',8),('SHEEP',9),('GOOSE',1)))
        self.planner.profile=self.core.profile
        old_growth=self.core._growth
        def growth(cash):
            offers=[o for o in old_growth(cash) if o[4]!='NEW_ANIMAL' and tuple(o[0]) not in RESERVED]
            if self.core.day>=27:return offers
            claims={tuple(j['target']) for j in self.core.active.values()}
            for pos,species in ANIMALS.items():
                tile=self.core._tile(pos)
                if pos in claims or tile=='LOCKED' or isinstance(tile,dict) and tile.get('animal'):continue
                if isinstance(tile,dict) and tile.get('kind') not in ('WEED','PASTURE','COOP'):continue
                structure='COOP' if species=='GOOSE' else 'PASTURE'
                commands=[['DIG']] if isinstance(tile,dict) and tile.get('kind')=='WEED' else []
                if not isinstance(tile,dict) or tile.get('kind')!=structure:commands.append(['BUILD_'+structure])
                commands += [['PLACE',species],['FEED'],['CARE']]
                cost=300 if species=='GOOSE' else 400 if species=='COW' else 500
                if cash>=cost+self.core._quote('WHEAT','BUY',1):offers.append((pos,commands,4,1,'NEW_ANIMAL'))
            return offers
        self.core._growth=growth
        self.events=[]
    def __call__(self,observation,configuration=None):
        if observation['day']<11:return self.opening(observation,configuration)
        observation=dict(observation);observation.setdefault('step',observation['day']*24+observation['hour'])
        return self.planner(observation,configuration or {})
def create_agent(context=None):return Calendar774(context)
