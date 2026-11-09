# cm_steady2.py (write): A/B switch for the steady-state loop databases. Adds pawn bool GR_SteadyEnable (default true)
# ANDed into the GR_Steady condition, so a test prelude can disable the loop databases
# (PW.set_editor_property('GR_SteadyEnable',False)) and the full gait database behaviour can be measured on its own.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
bp0=u.load_asset(PP)
if 'GR_SteadyEnable' not in [str(x) for x in B.list_variables(bp0)]: B.add_variable(bp0,'GR_SteadyEnable','bool')
L.compile_blueprint(bp0)
cdo=u.get_default_object(bp0.generated_class()); cdo.set_editor_property('GR_SteadyEnable',True); print('DEFAULT',cdo.get_editor_property('GR_SteadyEnable'))
del bp0; gc.collect()
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]
    # the SelectFloat that feeds the GR_SteadyT setter: its bPickA is the steady condition
    st=[p for p in N if 'GR_SteadyT' in ins(p) and 'execute' in ins(p)]; assert len(st)==1,st; st=st[0]
    sel=src((st,'GR_SteadyT'))[0][0]; cond=src((sel,'bPickA')); assert len(cond)==1,cond
    disconnect((sel,'bPickA')); a=g.fn(M+'BooleanAND',A=cond[0],B=g.get('GR_SteadyEnable')); connect((a,'ReturnValue'),(sel,'bPickA')); print('AND inserted')
run(PP,build); print('DONE')
