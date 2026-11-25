# m_coast3_mcp.py (MCP, in-memory; BP_HybridA_Player tick + AC_Sph_Motion DmCap; re-appliable) - movement realism pass 3.
# BRAKING STEPS. A key release at run / sprint speed went straight into the stop clip: 575 -> 0 cm/s in 0.50 s, 138 cm, ONE foot plant,
# 1600 cm/s2. A body cannot lose that momentum in one contact. Now, when the keys are released above CS_VMin, the player keeps walking
# input along the velocity ("coast") with the WALK gait requested, so the existing ramped speed limit (AC_Sph_Motion.DmCap, round 9)
# brings the capsule down through the run -> walk transition clip; the ramp is faster while coasting (DmBoostAdd = CS_K). At CS_VEnd the
# input is dropped and the normal stop clip plays from that lower speed. The number of braking steps therefore follows the release speed.
# Not forced: no coast when a wall / object is within the braking distance (trace at thigh height along the velocity), when the floor
# ends there (ledge, water edge), in the air, crouched, moving backwards, during a reaction lock, or as soon as any key is pressed.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
def addvars(BP, names, typ='float'):
    have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}})); ch = False
    for n in names:
        if '"%s"' % n not in have:
            T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': typ}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True}); ch = True
    if ch: T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
def edit(AP, tag, mk):
    r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
    e = mk(dsl)
    if e is None: print(tag, 'already'); return
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': e})
    print(tag, 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': AP + '.' + AP.split('/')[-1]}, 'bWarningsAsErrors': False}))[:160])
def one(dsl, pfx):
    m = [x for x in dsl.split(NL) if x.startswith(pfx)]; assert len(m) == 1, (pfx, len(m)); return m[0]
# --- AC_Sph_Motion: DmBoostAdd
MA = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; addvars(MA + '.AC_Sph_Motion', ['DmBoostAdd'])
def mk_m(dsl):
    if '`self.DmBoostAdd`' in dsl: return None
    l = one(dsl, '  (set `self.DmCap` '); a = '(%s %s (* %s %s))' % (K % 'FMax', V('DmRate'), V('DmCap'), V('DmRateK')); assert l.count(a) == 1
    return [{'oldString': l, 'newString': l.replace(a, '(* %s (+ 1.0 %s))' % (a, V('DmBoostAdd')))}]
edit(MA, 'COAST3 motion', mk_m)
# --- player
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
addvars(PA + '.BP_HybridA_Player', ['CS_On', 'CS_VMin', 'CS_VEnd', 'CS_Max', 'CS_Look', 'CS_K', 'CS_T']); addvars(PA + '.BP_HybridA_Player', ['CS_Clear'], 'bool')
def mk_p(dsl):
    if '`self.CS_T`' in dsl: return None
    sh = one(dsl, '  (set `self.GR_StopHold` (and'); sg = one(dsl, '  (set `self.GR_GaitSel` (`KismetMathLibrary.SelectInt` 0 (`self.GR_GaitSel`) (and (and (and (and (and (`self.GR_SoftStartOn`)')
    sp = '(%s (`self.GetVelocity`))' % (K % 'VSizeXY'); vd = '(%s (`self.GetVelocity`))' % (K % 'Vector_Normal2D'); mv = lambda x: '(%s %s %s %s)' % (K % 'MakeVector', x, x, x)
    pre = '(and (and (and (> %s 0.5) (< (%s %s) 0.1)) (and (> %s (%s %s %s (> %s 0.0))) (< %s %s))) (and (and (not (`NavMovementComponent.IsFalling` (`self.CharacterMovement`))) (not (`self.bIsCrouched`))) (and (and (<= %s 0.0) (not %s)) (> (%s %s (`self.GetActorForwardVector`)) 0.7))))' % (
        V('CS_On'), K % 'VSize', V('GR_RawIn'), sp, K % 'SelectFloat', V('CS_VEnd'), V('CS_VMin'), V('CS_T'), V('CS_T'), V('CS_Max'), V('CT_LockT'), V('GR_Back'), K % 'Dot_VectorVector', vd)
    s0 = '(+ (`self.K2_GetActorLocation`) (%s 0.0 0.0 -30.0))' % (K % 'MakeVector'); dist = '(+ (* %s %s) 60.0)' % (sp, V('CS_Look')); e0 = '(+ %s (* %s %s))' % (s0, vd, mv(dist))
    blk = NL.join([
        '  (if %s' % pre,
        '    (bind (_cshit _csblocked) (`KismetSystemLibrary.LineTraceSingle` %s %s))' % (s0, e0),
        '    (bind (_cshit_2 _csfloor) (`KismetSystemLibrary.LineTraceSingle` %s (+ %s (%s 0.0 0.0 -120.0))))' % (e0, e0, K % 'MakeVector'),
        '    (set `self.CS_Clear` (and (not _csblocked) _csfloor))',
        '    (else',
        '      (set `self.CS_Clear` false)))',
        '  (set `self.CS_T` (%s (+ %s DeltaSeconds) 0.0 %s))' % (K % 'SelectFloat', V('CS_T'), V('CS_Clear')),
        '  (set `/Game/Sphirus/Player/Motion/AC_Sph_Motion.DmBoostAdd` (%s %s 0.0 %s) (`self.SphMotion`))' % (K % 'SelectFloat', V('CS_K'), V('CS_Clear')),
        '  (if %s' % V('CS_Clear'),
        '    (`self.AddMovementInput` %s 1.0))' % vd])
    return [{'oldString': sh, 'newString': blk + NL + sh}, {'oldString': sg, 'newString': sg + NL + '  (set `self.GR_GaitSel` (%s 0 %s %s))' % (K % 'SelectInt', V('GR_GaitSel'), V('CS_Clear'))}]
edit(PA, 'COAST3 player', mk_p)
