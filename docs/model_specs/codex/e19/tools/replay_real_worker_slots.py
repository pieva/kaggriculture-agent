"""Real-worker slot counting shared with the frozen V51 external report."""
def slots(replay,seat):
    days=[dict(day=d,slots=0,explicit_pass=0,implicit_idle=0,move=0,
       pass_hours=[0]*24,slot_hours=[0]*24,worker_pass={},pass_critical_water=0,
       pass_unfed_animals=0,pass_current_tile_service=0) for d in range(1,31)]
    for i in range(1,len(replay['steps'])):
        o=replay['steps'][i-1][seat]['observation'];day=o['day'];hour=o['hour']
        farm=o['farms'][seat];priv=o['private'];a=replay['steps'][i][seat].get('action') or {}
        positions=[farm['farmer'],*farm['hands']]
        commands=[a.get('farmer',['PASS']),*a.get('hands',[])]
        tiles=[t for row in farm['tiles'] for t in row if isinstance(t,dict)]
        critical=any(t.get('kind')=='PLANT' and not t.get('watered_today') and t.get('consecutive_unwatered',0)>=1 for t in tiles)
        unfed=any(t.get('animal') and not t.get('fed_today') for t in tiles)
        active_positions={tuple(positions[w]) for w,c in enumerate(commands[:len(positions)]) if isinstance(c,list) and c and c[0]!='PASS'}
        z=days[day]
        for w,pos in enumerate(positions):
            z['slots']+=1;z['slot_hours'][hour]+=1
            c=commands[w] if w<len(commands) else None
            if not isinstance(c,list) or not c:
                z['implicit_idle']+=1;continue
            op=c[0]
            if op in {'NORTH','SOUTH','EAST','WEST'}:z['move']+=1
            if op!='PASS':continue
            z['explicit_pass']+=1;z['pass_hours'][hour]+=1
            z['worker_pass'][str(w)]=z['worker_pass'].get(str(w),0)+1
            z['pass_critical_water']+=critical;z['pass_unfed_animals']+=unfed
            x,y=pos;t=farm['tiles'][y][x];inv=priv['inventories'][w]
            local=isinstance(t,dict) and (t.get('kind')=='PLANT' and not t.get('watered_today') or t.get('animal') and (not t.get('cared_today') or not t.get('fed_today') and inv.get('WHEAT',0)>0))
            z['pass_current_tile_service']+=bool(local and tuple(pos) not in active_positions)
    return days
