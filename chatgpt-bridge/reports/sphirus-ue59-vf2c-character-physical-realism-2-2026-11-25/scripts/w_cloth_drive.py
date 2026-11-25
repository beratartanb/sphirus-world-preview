# w_cloth_drive.py (write, gated; RELAUNCH AFTER - Blueprint compile): the face Anim Blueprint's update event (already used for blink)
# also writes the pawn velocity and a smoothed copy (VInterpTo, speed 4) into MPC_Sph_Cloth every frame. The fabric materials turn the
# difference into a small hem offset (w_garment3.py). Guarded by IsValid(pawn). Nothing else is touched.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
P = '/Game/Sphirus/CharacterLab/Hazel_20261106/Face/ABP_Hazel_Face'; a = u.load_asset(P); T = u.BlueprintToolset
have = [str(v) for v in B.list_variables(a)]; assert 'VF2_Blink' in have and 'VF2_VelS' not in have, have
B.add_variable(a, 'VF2_VelS', 'Vector'); L.compile_blueprint(a)
eg = B.get_graph(a, 'EventGraph'); e = GE(eg); K = '/Script/Engine.KismetMathLibrary:'; cnt = [40]
ev = T.add_event(a, 'BlueprintUpdateAnimation', u.IntPoint(0, 0)); evp = pn(ev)
tail = None
for n in T.find_nodes(eg):
    i = T.get_node_infos([n])[0]
    if 'VF2_LookR' in [str(p.name) for p in i.input_pins]: tail = (pn(n), 'then')
assert tail, 'blink chain not found'
def place(n):
    cnt[0] += 1; n.set_node_pos(u.IntPoint(300 + (cnt[0] % 6) * 300, 200 + (cnt[0] // 6) * 220)); return pn(n)
def fn(path, **kw):
    n = e.add_call_function_node(path); assert n, path; p = place(n)
    for k, v in kw.items():
        if isinstance(v, tuple): connect(v, (p, k))
        else: value((p, k), v)
    return p
pawn = (fn('/Script/Engine.AnimInstance:TryGetPawnOwner'), 'ReturnValue')
ok = (fn('/Script/Engine.KismetSystemLibrary:IsValid', Object=pawn), 'ReturnValue')
br = place(e.add_branch_node()); connect(ok, (br, 'Condition')); connect(tail, (br, 'execute')); tail = (br, 'then')
vel = (fn('/Script/Engine.Actor:GetVelocity', self=pawn), 'ReturnValue')
g = place(e.add_get_member_variable_node('VF2_VelS', ''))
vs = (fn(K + 'VInterpTo', Current=(g, 'VF2_VelS'), Target=vel, DeltaTime=(evp, 'DeltaTimeX'), InterpSpeed=4.0), 'ReturnValue')
s = place(e.add_set_member_variable_node('VF2_VelS', '')); connect(vs, (s, 'VF2_VelS')); connect(tail, (s, 'execute')); tail = (s, 'then')
MPC = '/Game/Sphirus/CharacterLab/VF2_20261124/Garments/MPC_Sph_Cloth.MPC_Sph_Cloth'
for name, src_ in (('Vel', vel), ('VelSmooth', vs)):
    col = (fn(K + 'Conv_VectorToLinearColor', InVec=src_), 'ReturnValue')
    c = fn('/Script/Engine.KismetMaterialLibrary:SetVectorParameterValue', Collection=MPC, ParameterName=name, ParameterValue=col)
    print('CD set node pins', [str(q.name) for q in info(c).input_pins]); connect(tail, (c, 'execute')); tail = (c, 'then')
gc.collect(); L.compile_blueprint(a); er = errs(a); print('CD ERR', er); assert not er
print('CD saved', EA.save_loaded_asset(a, False), 'vars', [str(v) for v in B.list_variables(a)])
