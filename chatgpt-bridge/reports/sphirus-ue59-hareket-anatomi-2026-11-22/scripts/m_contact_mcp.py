# m_contact_mcp.py (MCP, in-memory edit of BP_HybridA_Player + AC_Sph_Motion; re-appliable) - 2026-11-22 round 5.
# CONTACT CONTEXT + STATE-DEPENDENT REACTION (event GR_Contact, every tick after GR_Posture). There was no collision reaction owner in the
# GASP player: the capsule simply stopped at full animation speed. Owner = the player Blueprint (state), outputs through the existing
# owners: AC_Sph_Motion (speed cap CtCap inside TurnCap, hand reach CtA / CtPt / CtR on the existing reach IK), the posture springs
# (PS_LPV / PS_LRV trunk impulse, PS_DAL / PS_DAR arm flare) and the driver slot (kneel / stand clips).
#  SENSE (5 line traces along last frame's travel direction, Visibility): chest 138 cm, waist 92 cm, knee 52 cm (above the 45 cm step
#   height), and one lateral line per side at 128 cm. -> distance from the capsule surface, surface normal, incidence, class
#   (1 wall = chest+waist, 2 waist-high, 3 knee-high, 4 chest-only), approach speed along the normal.
#  ANTICIPATE (head-on, wall / waist-high, input held): max speed <= 60 + sqrt(2 * CT_Dec * (d - 10)) (a comfortable brake before the
#   surface) and the nearer hand reaches to the surface inside arm length. Knee-high obstacles are not anticipated (they are what trips).
#   Pressed against the surface: the into-wall input is dropped (stands, hand on the wall) until the stick points > ~45 deg away.
#  GRAZE (surface beside the body closer than 3..12 cm by speed): nearer hand to the surface, trunk leans away, speed follows 80-100 %
#   of the recent speed (rubbing slows down progressively).
#  IMPACT (the approach speed collapses in one frame at the surface): severity
#       S = v_impact / CT_VRef x height (wall 1, waist 1.15, knee 1.5, chest-only 0.8) x (1 + CT_KFat * fatigue + 0.25 carrying
#           + 0.2 no foot on the ground) x (1 .. CT_KAnt when it was anticipated)
#   S < CT_SBump: trunk impulse only | < CT_SStag: blocked - rebound step, 0.16 s no input, speed held 0.6 s
#   | < CT_SDown: stagger - larger rebound (recovery steps come from Motion Matching), arms out, 0.45 s + fatigue no input, 1.2 s slow
#   | else: balance lost - drops to one knee, stays (longer when tired), stands up; input ignored meanwhile.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; out = {}; NL = chr(10)
MOT = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; MBP = MOT + '.AC_Sph_Motion'; DRY = '--dry' in sys.argv
KN = '/Game/MC_Core_Motion/Animations/Kneel/'
M = '`KismetMathLibrary.%s`'
def v(n): return '(`self.%s`)' % n
def F(name, *a): return '(%s %s)' % (M % name, ' '.join(a))
def AND(*x):
    r = x[0]
    for y in x[1:]: r = '(and %s %s)' % (r, y)
    return r
def OR(*x):
    r = x[0]
    for y in x[1:]: r = '(or %s %s)' % (r, y)
    return r
def sel(a, b, c): return F('SelectFloat', a, b, c)
def selv(a, b, c): return F('SelectVector', a, b, c)
def vs(vec, f): return '(* %s %s)' % (vec, F('MakeVector', f, f, f))
def mv(x, y, z): return F('MakeVector', x, y, z)
def mot(n): return '(`%s.%s` (`self.SphMotion`))' % (MOT, n)
def setmot(n, x): return '(set `%s.%s` %s (`self.SphMotion`))' % (MOT, n, x)
def S(n, x): return '(set `self.%s` %s)' % (n, x)
UP = mv('0.0', '0.0', '1.0')
L = []
L.append('(bind _dt %s)' % F('FClamp', v('GR_PDt'), '0.004', '0.05'))
L.append('(bind _ai (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)))')
L.append('(bind _vel (`self.GetVelocity`))')
L.append('(bind _sp %s)' % F('VSizeXY', '_vel'))
L.append('(bind _hasin (> %s 0.1))' % F('VSize', v('GR_RawIn')))
L.append('(bind _ind %s)' % F('Vector_Normal2D', v('GR_RawIn'), '0.0001'))
L.append('(bind _dir %s)' % selv(F('Vector_Normal2D', v('CT_PrevVel'), '0.0001'), selv('_ind', '(`self.GetActorForwardVector`)', '_hasin'), '(> %s 40.0)' % F('VSizeXY', v('CT_PrevVel'))))
L.append('(bind _rt %s)' % F('Cross_VectorVector', UP, '_dir'))
L.append('(bind _loc (`self.K2_GetActorLocation`))')
L.append('(bind _len (+ %s 30.0))' % F('FClamp', '(* _sp %s)' % v('CT_Look'), '45.0', '260.0'))
def tr(tag, z, lat=None):
    st = '(+ _loc %s)' % mv('0.0', '0.0', z)
    en = '(+ %s %s)' % (st, vs('_dir', '_len')) if lat is None else '(+ %s %s)' % (st, vs('_rt', lat))
    L.append('(bind (_h%s _b%s) (`KismetSystemLibrary.LineTraceSingle` %s %s "TraceTypeQuery1"))' % (tag, tag, st, en))
    L.append('(bind _d%s %s)' % (tag, sel('(- (`.Distance` (`GameplayStatics.BreakHitResult` _h%s)) 30.0)' % tag, '999.0', '_b' + tag)))
tr('hi', '52.0'); tr('mid', '6.0'); tr('kn', '-34.0'); tr('ll', '42.0', '-52.0'); tr('lr', '42.0', '52.0')
def hn(tag): return '(`.ImpactNormal` (`GameplayStatics.BreakHitResult` _h%s))' % tag
def hp(tag): return '(`.ImpactPoint` (`GameplayStatics.BreakHitResult` _h%s))' % tag
L.append('(bind _hitb %s)' % OR('_bhi', '_bmid', '_bkn'))
L.append('(bind _db %s)' % F('FMin', '_dhi', F('FMin', '_dmid', '_dkn')))
L.append('(bind _n %s)' % F('Vector_Normal2D', selv(hn('mid'), selv(hn('hi'), hn('kn'), '_bhi'), '_bmid'), '0.0001'))
L.append('(bind _pt %s)' % selv(hp('hi'), selv(hp('mid'), hp('kn'), '_bmid'), '_bhi'))
L.append('(bind _cosi (- 0.0 %s))' % F('Dot_VectorVector', '_dir', '_n'))
L.append('(bind _vn %s)' % sel(F('FMax', '(- 0.0 %s)' % F('Dot_VectorVector', '_vel', '_n'), '0.0'), '0.0', '_hitb'))
L.append('(bind _cls %s)' % F('SelectInt', '1', F('SelectInt', '2', F('SelectInt', '3', F('SelectInt', '4', '0', '_bhi'), '_bkn'), '_bmid'), AND('_bhi', '_bmid')))
L.append('(bind _carry %s)' % OR(v('GR_CarryActive'), v('GR_Load2H')))
L.append('(bind _fat %s)' % mot('Fat'))
L.append('(bind _gnd (`NavMovementComponent.IsMovingOnGround` (`self.CharacterMovement`)))')
L.append('(bind _st0 %s)' % v('CT_State'))
L.append('(bind _on %s)' % AND(v('CT_On'), '_gnd'))
# timers
for n in ('CT_Cool', 'CT_LockT', 'CT_CapT'):
    L.append(S(n, F('FMax', '(- %s _dt)' % v(n), '0.0')))
L.append(S('CT_T', sel('(+ %s _dt)' % v('CT_T'), '0.0', '(> _st0 0)')))
L.append(S('CT_SpRef', F('FMax', '_sp', '(- %s (* 15.0 _dt))' % v('CT_SpRef'))))
# anticipation (head-on wall / waist-high with the input held)
L.append('(bind _head %s)' % AND('_on', OR('_bhi', '_bmid'), '(> _cosi %s)' % v('CT_CosHead'), '_hasin', '(> %s 0.5)' % F('Dot_VectorVector', '_ind', '_dir')))
L.append('(bind _dw %s)' % F('FMin', '_dhi', '_dmid'))
L.append(S('CT_Prox', F('FInterpTo', v('CT_Prox'), sel(F('MapRangeClamped', '_dw', '12.0', '70.0', '1.0', '0.0'), '0.0', '_head'), '_dt', '10.0')))
L.append('(bind _capa %s)' % sel('(+ 60.0 %s)' % F('Sqrt', '(* (* 2.0 %s) %s)' % (v('CT_Dec'), F('FMax', '(- _dw 10.0)', '0.0'))), '100000.0', '_head'))
# graze (surface beside the body)
L.append('(bind _gl %s)' % F('MapRangeClamped', '_sp', '150.0', '400.0', '3.0', '12.0'))
L.append('(bind _grl %s)' % AND('_on', '_bll', '(< _dll _gl)', '(> _sp 120.0)'))
L.append('(bind _grr %s)' % AND('_on', '_blr', '(< _dlr _gl)', '(> _sp 120.0)'))
L.append('(bind _gr %s)' % OR('_grl', '_grr'))
L.append(S('CT_Graze', F('FInterpTo', v('CT_Graze'), sel('1.0', '0.0', '_gr'), '_dt', '8.0')))
L.append('(bind _capg %s)' % sel(F('FMax', '(* %s %s)' % (v('CT_SpRef'), F('MapRangeClamped', F('FMin', '_dll', '_dlr'), '0.0', '10.0', '0.8', '1.0')), '150.0'), '100000.0', '_gr'))
L.append(S('PS_LRV', '(+ %s (* (* %s _dt) %s))' % (v('PS_LRV'), v('CT_GrazeLean'), sel(sel('1.0', '-1.0', '_grl'), '0.0', '_gr'))))
# stairs / slopes: the ground under the capsule rises or falls quickly -> slower (260 cm/s on 18/30 stairs, ~330 on a 15 deg ramp)
L.append(S('CT_Vz', F('FInterpTo', v('CT_Vz'), sel(F('FClamp', '(/ (- (.z _loc) %s) _dt)' % v('CT_ZPrev'), '-400.0', '400.0'), '0.0', '_gnd'), '_dt', '6.0')))
L.append(S('CT_ZPrev', '(.z _loc)'))
L.append('(bind _capz %s)' % sel(F('MapRangeClamped', F('Abs', v('CT_Vz')), '60.0', '160.0', '400.0', '260.0'), '100000.0', AND('_on', '(> %s 60.0)' % F('Abs', v('CT_Vz')))))
# impact: the approach speed collapses in one frame at the surface
hitA = AND('(> (- %s _vn) (+ (* 2600.0 _dt) 30.0))' % v('CT_VnPrev'), '(< _vn (* 0.4 %s))' % v('CT_VnPrev'), '(> %s %s)' % (v('CT_VnPrev'), v('CT_VMin')))
hitB = AND('(> (- %s _vn) (+ (* 5200.0 _dt) 30.0))' % v('CT_VnPrev2'), '(< _vn (* 0.3 %s))' % v('CT_VnPrev2'), '(> %s %s)' % (v('CT_VnPrev2'), v('CT_VMin')))
L.append('(bind _imp %s)' % AND('_on', '(== _st0 0)', '(<= %s 0.0)' % v('CT_Cool'), '(< _db 10.0)', OR(hitA, hitB)))
L.append('(bind _vimp %s)' % F('FMax', v('CT_VnPrev'), v('CT_VnPrev2')))
L.append('(bind _hf %s)' % sel('1.0', sel('1.15', sel('1.5', '0.8', '(== _cls 3)'), '(== _cls 2)'), '(== _cls 1)'))
L.append('(bind _air %s)' % AND('(> (`AnimInstance.GetCurveValue` _ai "contact_l") 50.0)', '(> (`AnimInstance.GetCurveValue` _ai "contact_r") 50.0)'))
L.append('(bind _sv (* (* (* (/ %s %s) _hf) (+ (+ (+ 1.0 (* %s _fat)) %s) %s)) %s))' % ('_vimp', v('CT_VRef'), v('CT_KFat'), sel('0.25', '0.0', '_carry'), sel('0.2', '0.0', '_air'), F('Lerp', '1.0', v('CT_KAnt'), v('CT_Prox'))))
L.append('(bind _lvl %s)' % F('SelectInt', '3', F('SelectInt', '2', F('SelectInt', '1', '0', '(>= _sv %s)' % v('CT_SBump')), '(>= _sv %s)' % v('CT_SStag')), '(>= _sv %s)' % v('CT_SDown')))
body = []
body.append('(if _imp')
body.append('  ' + S('CT_LastS', '_sv'))
body.append('  ' + S('CT_LastV', '_vimp'))
body.append('  ' + S('CT_LastC', '_cls'))
body.append('  ' + S('CT_LastL', '_lvl'))
body.append('  ' + S('CT_Count', '(+ %s 1)' % v('CT_Count')))
body.append('  ' + S('CT_Cool', '0.9'))
k = F('FClamp', '_sv', '0.0', '2.0')
body.append('  ' + S('PS_LPV', '(+ %s (* (* %s %s) %s))' % (v('PS_LPV'), k, v('CT_KickP'), F('Dot_VectorVector', '_dir', '(`self.GetActorForwardVector`)'))))
body.append('  ' + S('PS_LRV', '(+ %s (* (* %s %s) %s))' % (v('PS_LRV'), k, v('CT_KickR'), F('Dot_VectorVector', '_dir', '(`self.GetActorRightVector`)'))))
body.append('  (if (>= _lvl 1)')
body.append('    ' + S('CT_State', F('SelectInt', '5', F('SelectInt', '4', '3', '(== _lvl 2)'), '(== _lvl 3)')))
body.append('    ' + S('CT_T', '0.0'))
body.append('    ' + S('CT_LockT', sel('30.0', sel('(+ 0.45 (* 0.3 _fat))', '0.16', '(== _lvl 2)'), '(== _lvl 3)')))
body.append('    ' + S('CT_CapT', sel('0.0', sel('1.2', '0.6', '(== _lvl 2)'), '(== _lvl 3)')))
body.append('    (set `MovementComponent.Velocity` %s (`self.CharacterMovement`)))' % vs('_n', sel('40.0', sel('(+ 110.0 (* 50.0 _sv))', '(+ 40.0 (* 70.0 _sv))', '(== _lvl 2)'), '(== _lvl 3)')))
body.append('  (if (>= _lvl 2)')
body.append('    ' + S('PS_DAL', '6.0'))
body.append('    ' + S('PS_DAR', '6.0') + ')')
body.append('  (if (== _lvl 3)')
body.append('    (`AnimInstance.PlaySlotAnimationAsDynamicMontage` _ai "%sam_Stand_Trans_KneeB.am_Stand_Trans_KneeB" "DefaultSlot" 0.15 0.2 1.5 1 -1.0 0.45)))' % KN)
# state progression (kneel -> hold -> stand)
body.append('(if %s' % AND('(== _st0 5)', '(> %s 0.95)' % v('CT_T')))
body.append('  (`AnimInstance.PlaySlotAnimationAsDynamicMontage` _ai "%sam_KneelB_Idle_01.am_KneelB_Idle_01" "DefaultSlot" 0.2 0.2 1.0 1 -1.0 0.0)' % KN)
body.append('  ' + S('CT_State', '6'))
body.append('  ' + S('CT_T', '0.0') + ')')
body.append('(if %s' % AND('(== _st0 6)', '(> %s (+ %s (* %s _fat)))' % (v('CT_T'), v('CT_DownHold'), v('CT_DownFat'))))
body.append('  (`AnimInstance.PlaySlotAnimationAsDynamicMontage` _ai "%sam_KneelB_Trans_Stand.am_KneelB_Trans_Stand" "DefaultSlot" 0.25 0.3 1.15 1 -1.0 0.0)' % KN)
body.append('  ' + S('CT_State', '7'))
body.append('  ' + S('CT_T', '0.0') + ')')
body.append('(if %s' % AND('(== _st0 7)', '(> %s 1.75)' % v('CT_T')))
body.append('  ' + S('CT_State', '0'))
body.append('  ' + S('CT_LockT', '0.0') + ')')
body.append('(if %s' % OR(AND('(== _st0 3)', '(> %s 0.5)' % v('CT_T')), AND('(== _st0 4)', '(> %s 1.1)' % v('CT_T'))))
body.append('  ' + S('CT_State', '0') + ')')
# pressed against the surface with the stick into it: drop the input (stands with the hand on the wall)
body.append('(if %s' % AND('_head', '(< _dw 5.0)', '(< _sp 25.0)', '(> _cosi 0.7)', '(== _st0 0)'))
body.append('  ' + S('CT_LockT', F('FMax', v('CT_LockT'), '0.1')) + ')')
# outputs
capt = sel(sel('150.0', '220.0', '(== %s 4)' % v('CT_State')), '100000.0', '(> %s 0.0)' % v('CT_CapT'))
capd = sel('0.0', '100000.0', '(>= %s 5)' % v('CT_State'))
body.append(setmot('CtCap', sel(F('FMin', F('FMin', '_capa', F('FMin', '_capg', '_capz')), F('FMin', capt, capd)), '100000.0', v('CT_On'))))
reach = AND('_head', '(< _dw 55.0)', '(not _carry)', '(== %s 0)' % v('CT_State'))
body.append('(bind _side %s)' % F('Dot_VectorVector', '(- _pt _loc)', '_rt'))
body.append(S('CT_ReachA', F('FInterpTo', v('CT_ReachA'), sel(sel(F('MapRangeClamped', '_dw', '55.0', '25.0', '0.0', '1.0'), '0.7', reach), '0.0', AND('_on', '(not _carry)', OR(reach, '_gr'))), '_dt', '7.0')))
ptw = '(+ (+ %s %s) %s)' % (mv('(.x _pt)', '(.y _pt)', '(+ (.z _loc) %s)' % sel('40.0', '8.0', '_bhi')), vs('_n', '2.0'), vs('_rt', sel('14.0', '-14.0', '(>= _side 0.0)')))
ptg = selv('(+ (+ %s %s) %s)' % (hp('ll'), vs('_dir', '14.0'), mv('0.0', '0.0', '-8.0')), '(+ (+ %s %s) %s)' % (hp('lr'), vs('_dir', '14.0'), mv('0.0', '0.0', '-8.0')), '_grl')
body.append('(if %s' % reach)
body.append('  ' + S('CT_ReachPt', ptw))
body.append('  ' + S('CT_ReachR', '(>= _side 0.0)') + ')')
body.append('(if %s' % AND('_gr', '(not %s)' % reach))
body.append('  ' + S('CT_ReachPt', ptg))
body.append('  ' + S('CT_ReachR', '(not _grl)') + ')')
body.append(setmot('CtA', v('CT_ReachA')))
body.append(setmot('CtPt', v('CT_ReachPt')))
body.append(setmot('CtR', v('CT_ReachR')))
body.append(S('CT_VnPrev2', v('CT_VnPrev')))
body.append(S('CT_VnPrev', sel('_vn', '0.0', AND('_hitb', '(< _db 45.0)'))))
body.append(S('CT_PrevVel', '_vel'))
body.append(S('CT_DB', '_db'))
body.append(S('CT_Class', '_cls'))
ev = NL + NL + '(event `GR_Contact`' + NL + NL.join('  ' + x for x in L + body) + ')'
if DRY:
    print(ev); sys.exit(0)
# ---------- variables ----------
PV = [(n, 'float') for n in ('CT_Look', 'CT_Dec', 'CT_CosHead', 'CT_VMin', 'CT_VRef', 'CT_KFat', 'CT_KAnt', 'CT_SBump', 'CT_SStag', 'CT_SDown', 'CT_KickP', 'CT_KickR', 'CT_GrazeLean', 'CT_DownHold', 'CT_DownFat',
      'CT_Cool', 'CT_LockT', 'CT_CapT', 'CT_T', 'CT_SpRef', 'CT_Prox', 'CT_Graze', 'CT_VnPrev', 'CT_VnPrev2', 'CT_LastS', 'CT_LastV', 'CT_ReachA', 'CT_DB', 'CT_Vz', 'CT_ZPrev')] + \
     [(n, 'int') for n in ('CT_State', 'CT_LastC', 'CT_LastL', 'CT_Count', 'CT_Class')] + [(n, 'bool') for n in ('CT_On', 'CT_ReachR')] + [(n, 'vector') for n in ('CT_PrevVel', 'CT_ReachPt')]
MV = [('CtCap', 'float'), ('CtA', 'float'), ('CtPt', 'vector'), ('CtR', 'bool')]
for bp, lst in ((BP, PV), (MBP, MV)):
    have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': bp}}))
    for n, ty in lst:
        if '"%s"' % n in have: continue
        r = T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': bp}, 'name': n, 'typeName': ty})
        if isinstance(r, dict) and r.get('isError'): out['var_' + n] = str(r)[:200]
        T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': bp}, 'variableName': n, 'bInstanceEditable': True})
# ---------- AC_Sph_Motion: CtCap in TurnCap, Ct reach override ----------
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': MOT, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`self.CtCap`' not in dsl:
    def line(prefix):
        X = [l for l in dsl.split(NL) if l.strip().startswith(prefix)]; assert len(X) == 1, (prefix, len(X)); return X[0]
    tc = line('(set `self.TurnCap`'); ra = line('(set `self.ReachA`'); ind = tc[:len(tc) - len(tc.lstrip())]; ind2 = ra[:len(ra) - len(ra.lstrip())]
    s = tc.strip(); p = '(set `self.TurnCap` '; assert s.startswith(p)
    tc2 = ind + '(set `self.TurnCap` (%s %s (`self.CtCap`)))' % (M % 'FMin', s[len(p):-1])
    gt = '(> (`self.CtA`) (`self.ReachA`))'
    ra2 = ra + NL + ind2 + '(set `self.ReachPt` (%s (`self.CtPt`) (`self.ReachPt`) %s))' % (M % 'SelectVector', gt) + NL + ind2 + '(set `self.ReachR` (or (and (`self.CtR`) %s) (and (`self.ReachR`) (not %s))))' % (gt, gt) + NL + ind2 + '(set `self.ReachA` (%s (`self.ReachA`) (`self.CtA`)))' % (M % 'FMax')
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': MOT, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': tc, 'newString': tc2}, {'oldString': ra, 'newString': ra2}]})
    out['mot_edit'] = str(r2)[:1800] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
    out['mot_compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': MBP}, 'bWarningsAsErrors': False}))[:160]
# ---------- player ----------
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '(event `GR_Contact`' in dsl:
    i0 = dsl.index('(event `GR_Contact`'); c = [x for x in (dsl.find(NL + NL + '(event', i0), dsl.find(NL + NL + '(fn', i0)) if x > 0]
    old = dsl[i0:min(c)] if c else dsl[i0:]; edits = [{'oldString': old.rstrip(NL), 'newString': ev.strip()}]
else:
    open('Saved/UE59Work/dsl/player_before_contact.dsl', 'w', encoding='utf8').write(dsl)
    call = [l for l in dsl.split(NL) if l.strip() == '(`self.GR_Posture`)']; assert len(call) == 1, len(call); ind = call[0][:len(call[0]) - len(call[0].lstrip())]
    gate = '(if (not (`self.GR_StopHold`))'; assert dsl.count(gate) == 1, dsl.count(gate)
    i0 = dsl.index('(event `GR_Posture`'); i1 = dsl.find(NL + NL + '(', i0); pe = dsl[i0:i1].rstrip(NL)
    edits = [{'oldString': call[0], 'newString': call[0] + NL + ind + '(`self.GR_Contact`)'},
             {'oldString': gate, 'newString': '(if (and (not (`self.GR_StopHold`)) (<= (`self.CT_LockT`) 0.0))'},
             {'oldString': pe[-300:], 'newString': pe[-300:] + ev}]
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
out['edit'] = str(r2)[:2600] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300]
print('CONTACT', json.dumps(out)[:4000])
