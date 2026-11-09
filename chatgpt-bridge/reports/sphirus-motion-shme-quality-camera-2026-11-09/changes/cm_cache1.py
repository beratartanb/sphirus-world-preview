# cm_cache1.py (write, two phases): ROOT CAUSE - in ABP_Sph_Driver the DefaultSlot output fed two consumers (UpperBody
# slot source and the layered-bone-blend base pose). An anim node with two consumers is updated twice per frame, so
# everything upstream (pose history collector, idle gate, idle sequence player, motion matching) advanced twice: idle
# played at 2x (5.8 s period for an 11.47 s clip), the trajectory history got two entries per frame (search preferred
# slow poses), blends stuttered.
# Phase 1 (no save node yet): add Save Cached Pose 'LocoCache' fed by DefaultSlot (consumers untouched), save.
# Phase 2 (after an editor restart, when the palette knows the cache): add two Use Cached Pose readers and move the two
# consumers onto them, so DefaultSlot has exactly one consumer.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
_LF=open(u.Paths.project_dir()+'Saved/Codex/Day_20261107/cache_progress.txt','a')
def P(*a):
    print(*a); print(*a,file=_LF); _LF.flush()
d=u.load_asset('/Game/Sphirus/Player/Anim/ABP_Sph_Driver'); ag=[g for g in B.list_graphs(d) if g.get_name()=='AnimGraph'][0]
nodes=B.find_nodes(ag)
defslot=[n for n in nodes if n.get_class().get_name()=='AnimGraphNode_Slot' and str(n.get_editor_property('node').get_editor_property('slot_name'))=='DefaultSlot']; assert len(defslot)==1
pdef=pn(defslot[0]); cons=[]
for n in nodes:
    p=pn(n)
    for ip in info(p).input_pins:
        try:
            if (pdef,'Pose') in src((p,str(ip.name))): cons.append((p,str(ip.name),n.get_class().get_name()))
        except Exception: pass
P('CONSUMERS',[(c[2],c[1]) for c in cons])
saves=[n for n in nodes if n.get_class().get_name()=='AnimGraphNode_SaveCachedPose']
if not saves:
    sn=B.create_node(ag,'Animation|CachedPoses|YeniÖnbelleğealınmışpozukaydet...',u.IntPoint(-200,900)); assert sn
    sn.set_editor_property('cache_name','LocoCache'); connect((pdef,'Pose'),(pn(sn),'Pose'))
    L.compile_blueprint(d); P('ERR_D',errs(d)); assert not errs(d); assert EA.save_loaded_asset(d,False); P('PHASE1 DONE (save node added, restart editor for phase 2)')
else:
    P('SAVE exists',saves[0].get_editor_property('cache_name'))
    real=[c for c in cons if c[2]!='AnimGraphNode_SaveCachedPose']; P('REAL consumers',[(c[2],c[1]) for c in real])
    uses=[n for n in nodes if n.get_class().get_name()=='AnimGraphNode_UseCachedPose']
    if len(real)==2:
        types=[t for t in B.find_node_types(ag,'LocoCache')]; P('USE types',types)
        if not types: types=[t for t in B.find_node_types(ag,'nbelleğealınmışpoz') if 'Yeni' not in t]; P('USE types (generic)',types[:5])
        assert types,'no use-cached-pose type in palette'
        ut=[t for t in types if 'LocoCache' in t] or types; ut=ut[0]
        for i,c in enumerate(real):
            un=B.create_node(ag,ut,u.IntPoint(0,1100+200*i)); assert un; P('USE node',un.get_class().get_name(),[str(x.name) for x in info(pn(un)).output_pins])
            disconnect((c[0],c[1])); connect((pn(un),'Pose'),(c[0],c[1])); P('STEP use ->',c[2],c[1])
        L.compile_blueprint(d); P('ERR_D',errs(d)); assert not errs(d); assert EA.save_loaded_asset(d,False); P('PHASE2 DONE')
    else: P('PHASE2 already applied; real consumers',len(real))
