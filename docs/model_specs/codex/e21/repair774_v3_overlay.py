# E21 Repair3: observed crop survival before invalid animal services or bonus.
_REPAIR3_PARENT=Repaired774Policy
MODEL_VERSION='CODEX-E21-774-REPAIR3-WATER'
RELEASE_ID=MODEL_VERSION
class Repaired774Policy(_REPAIR3_PARENT):
    def __call__(self,observation,configuration=None):
        action=super().__call__(observation,configuration)
        if not 11<=observation['day']<28:return action
        action=_repair_copy(action)
        farm=observation['farms'][observation['player']]
        positions=[farm['farmer']]+farm['hands']
        commands=[action['farmer']]+action['hands']
        watered=set()
        for xy,c in zip(positions,commands):
            if c[0]=='WATER':watered.add(tuple(xy))
        for w,(xy,c) in enumerate(zip(positions,commands)):
            tile=farm['tiles'][xy[1]][xy[0]]
            if tuple(xy) in watered or not isinstance(tile,dict) or tile.get('kind')!='PLANT' or tile.get('watered_today'):continue
            invalid=c[0] in {'PASS','CARE','FEED','COLLECT_FERTILIZER'}
            survival=c[0]=='FERTILIZE' and tile.get('consecutive_unwatered',0)>=1
            if invalid or survival:
                commands[w]=['WATER'];watered.add(tuple(xy));self.metrics['crop_water_repairs']+=1
        action['farmer'],action['hands']=commands[0],commands[1:]
        return action
