# w_face_life.py (write, gated; RELAUNCH AFTER - Blueprint compile): natural blink + small glances on the face Anim Blueprint.
# ABP_Hazel_Face AnimGraph is CopyPoseFromMesh -> ModifyCurve(constant rest expression) -> Output. Three more ModifyCurve nodes are chained
# behind it; each holds one constant curve map (lids closed / eyes left / eyes right) and its ALPHA pin is driven by a float variable that
# the event graph writes every update from game time: two triangular pulse trains with different periods give an irregular blink rhythm
# (about 14 per minute, 0.22 s each), two slow windows give an occasional small glance. No other asset is touched.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
from qa_graph import obj
import re as _re
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
P = '/Game/Sphirus/CharacterLab/Hazel_20261106/Face/ABP_Hazel_Face'; a = u.load_asset(P); T = u.BlueprintToolset
have = [str(v) for v in B.list_variables(a)]; assert 'VF2_Blink' not in have, 'already installed'
for n in ('VF2_Blink', 'VF2_LookL', 'VF2_LookR'): B.add_variable(a, n, 'float')
L.compile_blueprint(a); assert 'VF2_LookR' in [str(v) for v in B.list_variables(a)]
# ---------------------------------------------------------------- AnimGraph
ag = B.get_graph(a, 'AnimGraph'); mc = res = None
for n in T.find_nodes(ag):
    i = T.get_node_infos([n])[0]; ins = [str(p.name) for p in i.input_pins]
    if 'Alpha' in ins and 'SourcePose' in ins: mc = pn(n)
    if 'Result' in ins: res = pn(n)
assert mc and res; TID = str(info(mc).type_id); mo = [str(x.name) for x in info(mc).output_pins]; print('FL modify out pins', mo, 'type', TID)
disconnect((res, 'Result')); prev = (mc, mo[0]); x = 900
CH = [('VF2_Blink', '(("CTRL_expressions_eyeBlinkL", 1.000000),("CTRL_expressions_eyeBlinkR", 1.000000))'),
      ('VF2_LookL', '(("CTRL_expressions_eyeLookLeftL", 1.000000),("CTRL_expressions_eyeLookLeftR", 1.000000))'),
      ('VF2_LookR', '(("CTRL_expressions_eyeLookRightL", 1.000000),("CTRL_expressions_eyeLookRightR", 1.000000))')]
for var, cmap in CH:
    n_ = B.create_node(ag, TID, (x, 300)); assert n_; tq = pn(n_); o = obj(tq); nd = o.get_editor_property('node'); t = nd.export_text()
    t2, c = _re.subn(r'CurveMap=.*?,CurveValues=', 'CurveMap=' + cmap + ',CurveValues=', t, count=1); assert c == 1, t[:300]
    t2 = _re.sub(r'ApplyMode=\w+', 'ApplyMode=Blend', t2)
    nd.import_text(t2); o.set_editor_property('node', nd); c2 = o.get_editor_property('node').export_text(); assert cmap.split('"')[1] in c2 and 'ApplyMode=Blend' in c2, c2[:400]
    connect(prev, (tq, 'SourcePose')); g2 = pn(GE(ag).add_get_member_variable_node(var, '')); connect((g2, var), (tq, 'Alpha')); prev = (tq, mo[0]); x += 320
connect(prev, (res, 'Result'))
# ---------------------------------------------------------------- EventGraph: variables from game time
eg = B.get_graph(a, 'EventGraph'); e = GE(eg); K = '/Script/Engine.KismetMathLibrary:'; cnt = [0]
def fn(path, **kw):
    n = e.add_call_function_node(path); assert n, path; cnt[0] += 1; n.set_node_pos(u.IntPoint(300 + (cnt[0] % 6) * 300, 200 + (cnt[0] // 6) * 220)); p = pn(n)
    for k, v in kw.items():
        if isinstance(v, tuple): connect(v, (p, k))
        else: value((p, k), v)
    return p
ev = T.add_event(a, 'BlueprintUpdateAnimation', u.IntPoint(0, 0)); assert ev; evp = pn(ev); print('FL event pins', [str(q.name) for q in info(evp).output_pins])
tm = (fn('/Script/Engine.KismetSystemLibrary:GetGameTimeInSeconds'), 'ReturnValue')
def pulse(period, t0, rise, hold, fall, peak):
    r = (fn(K + 'FMod', Dividend=tm, Divisor=period), 'Remainder')
    up = (fn(K + 'MapRangeClamped', Value=r, InRangeA=t0, InRangeB=t0 + rise, OutRangeA=0.0, OutRangeB=peak), 'ReturnValue')
    dn = (fn(K + 'MapRangeClamped', Value=r, InRangeA=t0 + rise + hold, InRangeB=t0 + rise + hold + fall, OutRangeA=peak, OutRangeB=0.0), 'ReturnValue')
    return (fn(K + 'FMin', A=up, B=dn), 'ReturnValue')
blink = (fn(K + 'FMax', A=pulse(4.3, 0.4, 0.07, 0.03, 0.12, 1.0), B=pulse(7.1, 3.2, 0.07, 0.03, 0.12, 1.0)), 'ReturnValue')
lookl = pulse(11.3, 5.0, 0.18, 1.3, 0.25, 0.10); lookr = pulse(17.9, 9.5, 0.18, 0.9, 0.25, 0.08)
tail = (evp, 'then')
for var, src_ in (('VF2_Blink', blink), ('VF2_LookL', lookl), ('VF2_LookR', lookr)):
    s = e.add_set_member_variable_node(var, ''); assert s, var; cnt[0] += 1; s.set_node_pos(u.IntPoint(300 + (cnt[0] % 6) * 300, 200 + (cnt[0] // 6) * 220)); sp = pn(s)
    connect(src_, (sp, var)); connect(tail, (sp, 'execute')); tail = (sp, 'then')
gc.collect(); L.compile_blueprint(a); er = errs(a); print('FL ERR', er); assert not er
print('FL saved', EA.save_loaded_asset(a, False), 'vars', [str(v) for v in B.list_variables(a)])
print('FL dirty', [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
