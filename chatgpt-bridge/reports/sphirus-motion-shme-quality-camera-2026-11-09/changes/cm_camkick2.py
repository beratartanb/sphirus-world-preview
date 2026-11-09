# cm_camkick2.py (write): fix of cm_camkick1. Live probe: GR_ArmBase eases correctly but GR_Accel stays 0 - the setter
# order was Set GR_PrevSpeed -> Set GR_Accel, and Blueprint pins evaluate lazily when the setter runs, so (speed -
# GR_PrevSpeed) was always 0. New order: Set GR_ArmBase -> Set GR_Accel -> Set GR_PrevSpeed -> Set GR_CamKick -> arm.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; ins=lambda p:[str(x.name) for x in info(p).input_pins]
    S={}
    for v in ('GR_ArmBase','GR_PrevSpeed','GR_Accel','GR_CamKick'):
        c=[p for p in N if v in ins(p) and 'execute' in ins(p)]; assert len(c)==1,(v,c); S[v]=c[0]
    assert src((S['GR_PrevSpeed'],'execute'))[0][0]==S['GR_ArmBase'] and src((S['GR_Accel'],'execute'))[0][0]==S['GR_PrevSpeed'] and src((S['GR_CamKick'],'execute'))[0][0]==S['GR_Accel']
    for v in ('GR_PrevSpeed','GR_Accel','GR_CamKick'): disconnect((S[v],'execute'))
    connect((S['GR_ArmBase'],'then'),(S['GR_Accel'],'execute')); connect((S['GR_Accel'],'then'),(S['GR_PrevSpeed'],'execute')); connect((S['GR_PrevSpeed'],'then'),(S['GR_CamKick'],'execute'))
    print('REORDERED')
run(PP,build)
bp=u.load_asset(PP); cdo=u.get_default_object(bp.generated_class()); cdo.set_editor_property('GR_ArmBase',140.0)
L.compile_blueprint(bp); assert EA.save_loaded_asset(bp,False); print('DONE')
