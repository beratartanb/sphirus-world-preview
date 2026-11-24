exec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
# c_selt9.py (control job, in-memory build; saved later by a gated write job) on ABP_Sph_GASP - round 9.
# The reversal governor needs the speed of the clip Motion Matching actually selected at its real time. The AnimInstance curve
# 'movedata_speed' is blended over the 0.3 s blend, so right after a new clip is entered it still shows the previous clip's speed and the
# capsule overruns the turn clip's final plant by ~30 cm. New float SphSelTime = Result.SelectedTime, written next to CurrentSelectedAnim
# in Update_MotionMatching_PostSelection (same thread-safe function, one extra Set node).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
from qa_graph import obj
P='/Game/Sphirus/Player/GASP/ABP_Sph_GASP'; a=u.load_asset(P); have=[str(v) for v in B.list_variables(a)]
if 'SphSelTime' in have: print('SELT9 already')
else:
    B.add_variable(a,'SphSelTime','float'); L.compile_blueprint(a)
    g=B.get_graph(a,'Update_MotionMatching_PostSelection'); N={str(pn(x)).split('.')[-1]:pn(x) for x in B.find_nodes(g)}
    ent=N['K2Node_FunctionEntry_0']; brk=N['K2Node_CallFunction_1']; s0=N['K2Node_VariableSet_0']
    assert 'Result_SelectedTime' in [str(q.name) for q in info(brk).output_pins]
    n=GE(g).add_set_member_variable_node('SphSelTime',''); assert n; n.set_node_pos(u.IntPoint(-200,-260)); p=pn(n)
    connect((brk,'Result_SelectedTime'),(p,'SphSelTime'))
    disconnect((s0,'execute')); connect((ent,'then'),(p,'execute')); connect((p,'then'),(s0,'execute'))
    L.compile_blueprint(a); e=errs(a); print('SELT9 built ERR',e); assert not e
    print('SELT9 chain', src((s0,'execute')), src((p,'execute')))
