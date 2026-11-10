# q_gasp4.py (read-only): GASP character function graphs as node-type sequences + links (SetupInput, SetupCamera, EventGraph, UpdateMovement/Rotation).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
bp=u.load_asset('/Game/Blueprints/SandboxCharacter_CMC')
first=True
for g in B.list_graphs(bp):
    if g.get_name() not in ('SetupInput','SetupCamera','EventGraph','UpdateRotation_PreCMC','UpdateMovement_PreCMC','GetDesiredGait','CanSprint'): continue
    print('== GRAPH',g.get_name())
    for n in B.find_nodes(g):
        i=info(pn(n))
        if first: print('INFOFIELDS',[k for k in dir(i) if not k.startswith('_')]); first=False
        vals=[]
        for x in i.input_pins:
            try:
                v=str(B.get_pin_value(x.pin_id)); 
                if v and v not in ('None','0','0.0','False','') : vals.append('%s=%s'%(x.name,v[:50]))
            except Exception: pass
        print('  ',str(i.type_id)[:80],'|',(getattr(i,'title','') or '')[:40] if hasattr(i,'title') else '','|',vals[:5])
ac=u.load_asset('/Game/Blueprints/AC_PreCMCTick')
for g in B.list_graphs(ac):
    print('== AC_PreCMCTick',g.get_name(),[str(info(pn(n)).type_id)[:70] for n in B.find_nodes(g)])
