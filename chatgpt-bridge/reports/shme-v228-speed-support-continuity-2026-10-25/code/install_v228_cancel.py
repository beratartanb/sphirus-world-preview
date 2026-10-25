"""install_v228_cancel.py (editor job) - V2.28 deliverable 1, the cancel paths of the authored reversal (measured on v228t2 rhC):
 - j24_rel (key released 0.27 s into the brake, speed 14 cm/s): intent lost -> the hold died -> Motion Matching jumped to a dense idle at
   57 s then a walk start (planted right foot slid 37 cm). With RelHold: while the clip is in its BRAKE phase (designed speed still along
   the old travel) the hold survives the lost intent and the clip-bound capsule brakes to the designed zero; the hold then ends at the zero
   crossing -> the stop comes from the brake stance, at zero speed.
 - j24_dbl (second request 0.5 s in, the body just past the zero crossing): RedirectEnd 3 killed the hold -> MM picked a jog pivot then a
   run start (27 cm). With CancelOn: a new intent that points along the clip's BRAKE direction (the player wants the old travel back) is a
   cancel: the hold database is re-routed to the OPPOSITE family (F_B -> JRBwd = B_F clips, whose push phase accelerates forward) with one
   interrupting search, the hold / clip-bound speed stay alive, the entry sign flips. No standing start.
Variables: SHM228_RelHold (0), SHM228_CancelOn (0) knobs; SHM228_EntrySign (+1 F_B / -1 B_F, latched while a clip is in the pose), SHM228_Brake,
SHM228_Reroute, SHM228_Cancel (telemetry). SHM_Snapshot: after SetSHM228_Cmd: EntrySign / Brake; the Hold's HasIntent term -> OR(HasIntent,
RelHold & Brake); IntentEnd -> AND(old, NOT (RelHold & Brake & lost)) AND NOT cancel; cancel -> SHM_HoldDB := the other JR database, PrevRev := 10
(no re-entry latch on the switch), Reroute := cancel; EntrySign := -EntrySign on reroute. Update_MotionMatching: on the steady hold path
(IfThenElse_56 else) a Reroute branch issues SetDatabaseToSearch(SHM_HoldDB, InterruptOnDatabaseChange) before the DoNotInterrupt call.
Knobs 0 = unchanged. Idempotent (SetSHM228_Brake present). builtins.V228_SAVE saves. Prints CANCEL228 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg, value
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CP) for n in names), ('unexpected dirty', names)
rl = [p for p in dirty if p.get_name() in DAS or p.get_name() in (AP, CP)]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': [p.get_name() for p in rl]}
bp = u.load_asset(AP)
ensure_vars(bp, [('SHM228_RelHold', 'float', 'SHM228'), ('SHM228_CancelOn', 'float', 'SHM228'), ('SHM228_EntrySign', 'float', 'SHM228'), ('SHM228_Brake', 'bool', 'SHM228'), ('SHM228_Reroute', 'bool', 'SHM228'), ('SHM228_Cancel', 'bool', 'SHM228')]); compile_ok(bp)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def step(s): out['step'] = s
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
if any('SetSHM228_Brake' in tid(p) for p in sn): out['snapshot'] = 'already'
else:
    cmdset = [p for p in sn if 'SetSHM228_Cmd' in tid(p)]; assert len(cmdset) == 1, cmdset
    hd = [p for p in sn if 'SetSHM227_Hold' in tid(p)]; assert len(hd) == 1, hd
    ie = [p for p in sn if 'SetSHM227_IntentEnd' in tid(p)]; assert len(ie) == 1, ie
    pr = [p for p in sn if 'SetSHM227_PrevRev' in tid(p)]; assert len(pr) == 1, pr
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'
    ct = (comp[0], 'ReturnValue')
    # ---- EntrySign / Brake after SetSHM228_Cmd
    step('entrysign')
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (cmdset[0], 'then') in src((p, 'execute'))]; assert nxt
    for x in nxt: disconnect((x, 'execute'))
    dv = gs.get('SHM228_DesV'); es = gs.get('SHM228_EntrySign')
    vW = [p for p in sn if 'GetCurveValue' in tid(p)]
    inClip = gs.within(gs.get('SHM228_On'), 0.5, 1.0e9)                 # On = clip in the pose & episode alive & knob
    pos = gs.within(dv, 1.0, 1.0e9); neg = gs.within(dv, -1.0e9, -1.0)
    sign_now = gs.select(pos, 1.0, gs.select(neg, -1.0, 0.0))
    esZero = gs.within(es, -0.5, 0.5)
    newES = gs.select(inClip, gs.select(esZero, sign_now, es), 0.0)      # latch the first sign while a clip is in the pose; 0 outside
    tail = gs.set('SHM228_EntrySign', newES, (cmdset[0], 'then'))
    esg = gs.get('SHM228_EntrySign')
    brake = gs.AND(inClip, gs.within(gs.mul(dv, esg), 3.0, 1.0e9))      # designed speed still along the entry (old travel) direction
    tail = gs.set('SHM228_Brake', brake, tail)
    # ---- cancel: new intent (RedirectEnd 3) along the brake direction while a clip is in the pose
    step('cancel')
    rdEnd = gs.get('RedirectEnd', COMP, ct)
    isNew = gs.within(rdEnd, 2.5, 3.5); isLost = gs.within(rdEnd, 3.5, 4.5)
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')
    fwd = gs.pure('/Script/Engine.Actor:GetActorForwardVector', {'self': pawn})
    ddir = gs.pure(M + 'Vector_Normal2D', {'A': gs.get('DesiredDir', COMP, ct), 'Tolerance': 0.0001})
    along = gs.pure(M + 'Dot_VectorVector', {'A': fwd, 'B': ddir})     # + : intent along the actor forward
    alongBrake = gs.within(gs.mul(along, esg), 0.3, 1.0e9)              # intent along the clip's brake (= old travel) direction
    cancel = gs.AND(gs.AND(gs.within(gs.get('SHM228_CancelOn'), 0.5, 1.0e9), inClip), gs.AND(isNew, alongBrake))
    tail = gs.set('SHM228_Cancel', cancel, tail)
    relKeep = gs.AND(gs.AND(gs.within(gs.get('SHM228_RelHold'), 0.5, 1.0e9), gs.get('SHM228_Brake')), isLost)
    cg = gs.get('SHM228_Cancel')
    # reroute: hold database := the opposite family; prev-rev latch disarmed; entry sign flipped
    step('reroute')
    # typed database pins refuse a generic SelectObject: branch the exec chain instead (cancel -> entry sign -> the other family database)
    yC, nC = gs.branch(cg, tail)
    yS, nS = gs.branch(gs.within(esg, 0.5, 1.0e9), yC)
    tB = gs.set('SHM_HoldDB', gs.get('SHM224_DB_JRBwd'), yS)      # F_B playing (entry sign +) -> B_F clips (JRBwd database)
    tF = gs.set('SHM_HoldDB', gs.get('SHM224_DB_JRFwd'), nS)      # B_F playing -> F_B clips
    rr = gs.record(gs.editor().add_set_member_variable_node('SHM228_Reroute', ''))
    arg(rr, 'SHM228_Reroute', cg); connect(tB, (rr, 'execute')); connect(tF, (rr, 'execute')); connect(nC, (rr, 'execute'))
    tail = (rr, 'then')
    tail = gs.set('SHM228_EntrySign', gs.select(cg, gs.mul(gs.get('SHM228_EntrySign'), -1.0), gs.get('SHM228_EntrySign')), tail)
    for x in nxt: connect(tail, (x, 'execute'))
    # ---- Hold: HasIntent term -> OR(HasIntent, RelHold & Brake)
    step('hold')
    ho = src((hd[0], 'SHM227_Hold')); assert len(ho) == 1, ho
    def find_intent(p, depth=0):
        if depth > 6: return None
        for q in info(p).input_pins:
            for s in src((p, q.name)):
                if 'HasIntent' in tid(s[0]) and 'Set' not in tid(s[0]): return (p, q.name, s)
                r = find_intent(s[0], depth + 1)
                if r: return r
        return None
    fi = find_intent(ho[0][0]); assert fi, 'HasIntent term not found'
    disconnect((fi[0], fi[1])); connect(gs.OR(fi[2], gs.AND(gs.AND(gs.within(gs.get('SHM228_RelHold'), 0.5, 1.0e9), gs.get('SHM228_Brake')), gs.NOT(gs.get('HasIntent', COMP, ct)))), (fi[0], fi[1]))
    out['hold_pin'] = fi[0].rsplit('.', 1)[-1] + ':' + fi[1]
    # ---- IntentEnd := AND(old, NOT(relKeep OR cancel))
    step('intentend')
    io = src((ie[0], 'SHM227_IntentEnd')); assert len(io) == 1, io
    disconnect((ie[0], 'SHM227_IntentEnd')); connect(gs.AND(io[0], gs.NOT(gs.OR(relKeep, cancel))), (ie[0], 'SHM227_IntentEnd'))
    # ---- PrevRev := 10 on reroute (no re-entry latch on the database switch)
    step('prevrev')
    po = src((pr[0], 'SHM227_PrevRev')); assert len(po) == 1, po
    disconnect((pr[0], 'SHM227_PrevRev')); connect(gs.select(gs.get('SHM228_Reroute'), 10.0, po[0]), (pr[0], 'SHM227_PrevRev'))
    out['snapshot'] = 'wired'
# ---- Update_MotionMatching: reroute search on the steady hold path
step('umm')
ug = pn(graph(bp, 'Update_MotionMatching')); gu = G(ug); un = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(ug))}
if any('SHM228_Reroute' in tid(p) for p in un.values()): out['umm'] = 'already'
else:
    c314 = un['K2Node_CallFunction_314']; assert 'SetDatabaseToSearch' in tid(c314), tid(c314)
    br56 = un['K2Node_IfThenElse_56']; assert (br56, 'else') in src((c314, 'execute')), 'hold path changed'
    mmn = src((c314, 'MotionMatchingNode'))[0]; dbp = src((c314, 'Database'))[0]
    disconnect((c314, 'execute'))
    y, n = gu.branch(gu.get('SHM228_Reroute'), (br56, 'else'))
    sd = gu.call('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch', y, {'MotionMatchingNode': mmn, 'Database': dbp})
    value((sd[0], 'InterruptMode'), 'InterruptOnDatabaseChange')
    connect(sd, (c314, 'execute')); connect(n, (c314, 'execute'))
    out['umm'] = {'branch': y[0].rsplit('.', 1)[-1], 'call': sd[0].rsplit('.', 1)[-1]}
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: float(cdo.get_editor_property(k)) for k in ('SHM227_RevHold', 'SHM228_ClipSpeed', 'SHM228_RelHold', 'SHM228_CancelOn')}
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and all(v == 0.0 for v in out['knobs'].values())
out['ok'] = ok
if ok and getattr(builtins, 'V228_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('CANCEL228 ' + json.dumps(out, default=str))
