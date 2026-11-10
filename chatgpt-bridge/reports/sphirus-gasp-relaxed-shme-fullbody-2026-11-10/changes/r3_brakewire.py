# r3_brakewire.py (write) on BP_Sph_GASPCharacter: braking owner = SphMotion.
#   CalculateBrakingDeceleration: no-input option (2000) <- SphMotion.BrakeDecel
#   CalculateBrakingFriction: SelectFloat.A (3.0, used when there is no acceleration) <- SphMotion.BrakeFriction
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
P='/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'; MC='/Game/Sphirus/Player/Motion/AC_Sph_Motion.AC_Sph_Motion_C'
bp=u.load_asset(P)
def wire(gname,pick,prop):
    g=Gr(bp); g.g=B.get_graph(bp,gname); g.e=GE(g.g); N=[pn(x) for x in B.find_nodes(g.g)]
    tgt=pick(N); print(gname,'target',tgt,[str(x.name) for x in info(tgt[0]).input_pins])
    assert not src(tgt),'already wired'
    comp=(g.pos(g.e.add_get_member_variable_node('SphMotion','')),'SphMotion'); pv=g.pos(g.e.add_get_member_variable_node(prop,MC)); connect(comp,(pv,'self'))
    connect((pv,prop),tgt); print('WIRED',gname,prop,src(tgt))
tp=lambda p:str(info(p).type_id)
wire('CalculateBrakingDeceleration',lambda N:([p for p in N if tp(p).endswith('Seç')][0],'Option 0'),'BrakeDecel')
wire('CalculateBrakingFriction',lambda N:([p for p in N if tp(p).endswith('SelectFloat')][0],'A'),'BrakeFriction')
L.compile_blueprint(bp); e=errs(bp); print('ERR',e); assert not e; assert EA.save_loaded_asset(bp,False); print('DONE')
