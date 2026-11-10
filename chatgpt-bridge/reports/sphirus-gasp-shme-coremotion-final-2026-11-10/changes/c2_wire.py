# c2_wire.py (write) on BP_Sph_GASPCharacter: add AC_Sph_Motion as 'SphMotion'; GASP CalculateMaxSpeed result x
# SphMotion.SpeedScale, CalculateMaxAcceleration result x SphMotion.AccScale (single CMC owner, scaled targets).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
P='/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'; MC='/Game/Sphirus/Player/Motion/AC_Sph_Motion.AC_Sph_Motion_C'
bp=u.load_asset(P); scs=u.get_engine_subsystem(u.SubobjectDataSubsystem); SD=u.SubobjectDataBlueprintFunctionLibrary
hs={str(SD.get_variable_name(SD.get_data(h))):h for h in scs.k2_gather_subobject_data_for_blueprint(bp)}
if 'SphMotion' not in hs:
    root=scs.k2_gather_subobject_data_for_blueprint(bp)[0]
    pr=u.AddNewSubobjectParams(parent_handle=root,new_class=u.load_object(None,MC),blueprint_context=bp)
    h,why=scs.add_new_subobject(pr); print('ADD',why); scs.rename_subobject_member_variable(bp,h,'SphMotion')
L.compile_blueprint(bp); print('VARS has SphMotion',[str(SD.get_variable_name(SD.get_data(h))) for h in scs.k2_gather_subobject_data_for_blueprint(bp) if 'Sph' in str(SD.get_variable_name(SD.get_data(h)))])
def scale(gname,prop):
    g=Gr(bp); g.g=B.get_graph(bp,gname); g.e=GE(g.g); N=[pn(x) for x in B.find_nodes(g.g)]
    ret=[p for p in N if type(obj(p)).__name__=='K2Node_FunctionResult']; assert len(ret)==1,ret; ret=ret[0]
    s=src((ret,'ReturnValue')); assert len(s)==1,s; disconnect((ret,'ReturnValue'))
    comp=(g.pos(g.e.add_get_member_variable_node('SphMotion','')),'SphMotion')
    pv=g.pos(g.e.add_get_member_variable_node(prop,MC)); connect(comp,(pv,'self'))
    m=g.fn(M+'Multiply_DoubleDouble',A=s[0],B=(pv,prop)); connect((m,'ReturnValue'),(ret,'ReturnValue')); print('SCALED',gname,'x',prop)
from qa_graph import obj
scale('CalculateMaxSpeed','SpeedScale'); scale('CalculateMaxAcceleration','AccScale')
L.compile_blueprint(bp); e=errs(bp); print('ERR',e); assert not e; assert EA.save_loaded_asset(bp,False); print('DONE')
