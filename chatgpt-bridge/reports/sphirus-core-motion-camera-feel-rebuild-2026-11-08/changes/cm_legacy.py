# cm_legacy.py: ABP_Sph_Driver gets ForceLegacy (bool, default false). While true the driver uses the old single database
# PSD_Sph_Loco2 regardless of gait, so the old selection can be recorded on the same build for before/after comparisons.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
D='/Game/Sphirus/Player/MM'
d=u.load_asset('/Game/Sphirus/Player/Anim/ABP_Sph_Driver')
if 'ForceLegacy' not in [str(x) for x in B.list_variables(d)]: B.add_variable(d,'ForceLegacy','bool')
L.compile_blueprint(d)
eg=B.get_graph(d,'EventGraph'); ge=GE(eg); N=[pn(n) for n in B.find_nodes(eg)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]
def pv(p,k):
    try: return str(B.get_pin_value([x for x in info(p).input_pins if str(x.name)==k][0].pin_id))
    except Exception: return None
# the LocoDB setters for Run/Jog/Walk hang off two branches; insert a ForceLegacy branch before the GaitSel==2 branch
sr=[p for p in N if 'LocoDB' in ins(p) and 'execute' in ins(p) and 'PSD_Sph_Run' in (pv(p,'LocoDB') or '')]; assert len(sr)==1; sr=sr[0]
b2=src((sr,'execute'))[0][0]; pre=src((b2,'execute')); print('B2',tp(b2),len(pre)); assert len(pre)==1
outs=[(q,str(ip.name)) for q in N for ip in info(q).input_pins if (sr,'then') in src((q,str(ip.name)))]; assert outs
bl=pn(ge.add_branch_node()); gl=pn(ge.add_get_member_variable_node('ForceLegacy','')); connect((gl,'ForceLegacy'),(bl,'Condition'))
disconnect((b2,'execute')); connect(pre[0],(bl,'execute')); connect((bl,'else'),(b2,'execute'))
sl=pn(ge.add_set_member_variable_node('LocoDB','')); value((sl,'LocoDB'),D+'/PSD_Sph_Loco2.PSD_Sph_Loco2'); connect((bl,'then'),(sl,'execute'))
for d_ in outs: connect((sl,'then'),d_)
L.compile_blueprint(d); print('ERR_D',errs(d)); assert not errs(d); assert EA.save_loaded_asset(d,False); print('DONE')
