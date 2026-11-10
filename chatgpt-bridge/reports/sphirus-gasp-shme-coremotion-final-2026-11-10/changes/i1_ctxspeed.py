# i1_ctxspeed.py (write) on BP_Sph_GASPCharacter: context speed multiplier owned by the GASP character.
# SphContextSpeedScale (float, default 1.0) multiplies the CalculateMaxSpeed result after SphMotion.SpeedScale.
# Children set it from their own context (BP_HybridA_Player: house interior = 0.75 -> walk 200 -> 150 cm/s, the old house pace).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
from qa_graph import obj
P='/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'; V='SphContextSpeedScale'
bp=u.load_asset(P)
if V not in [str(v) for v in B.list_variables(bp)]: B.add_variable(bp,V,'float')
L.compile_blueprint(bp)
g=Gr(bp); g.g=B.get_graph(bp,'CalculateMaxSpeed'); g.e=GE(g.g); N=[pn(x) for x in B.find_nodes(g.g)]
ret=[p for p in N if type(obj(p)).__name__=='K2Node_FunctionResult']; assert len(ret)==1,ret; ret=ret[0]
s=src((ret,'ReturnValue')); assert len(s)==1,s; print('RET src',s)
assert not any(V in [str(x.name) for x in info(p).output_pins] for p in N),'already wired'
disconnect((ret,'ReturnValue'))
m=g.fn(M+'Multiply_DoubleDouble',A=s[0],B=g.get(V)); connect((m,'ReturnValue'),(ret,'ReturnValue'))
L.compile_blueprint(bp); cdo=u.get_default_object(bp.generated_class()); cdo.set_editor_property(V,1.0)
L.compile_blueprint(bp); e=errs(bp); print('ERR',e); assert not e; assert EA.save_loaded_asset(bp,False)
print('CDO',V,cdo.get_editor_property(V)); print('DONE')
