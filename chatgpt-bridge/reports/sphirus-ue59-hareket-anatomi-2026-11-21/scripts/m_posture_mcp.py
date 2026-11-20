# m_posture_mcp.py (MCP, in-memory edit of BP_HybridA_Player; saved by a gated write job) - 2026-11-21 round 4.
# POSTURE CONTROLLER (event GR_Posture, called every tick). Replaces the constant carriage offsets of the body posture layer
# (ABP_Sph_Body_GASP VI_/VW_/VR_/VA_/VD_ vectors) with slow integral corrections measured on the visible body itself:
#  spine: A1..A4 = sagittal lean over the MetaHuman bind of pelvis->spine_03, spine_03->spine_05, spine_05->neck_01, neck_01->head.
#     The thorax follows the lumbar lean in a smooth gradient: target A2 = R2 x A1, A3 = R3 x A1, A4 = R4 x A1 (clip families with
#     different inherent postures - Neutral walk/run, Relaxed sprint/idle, Core Motion jog - end in the same carriage; fast motion of
#     the clip passes through: time constant 1/PS_K). Corrections C3 (spine_03), C5 (spine_05), CN (neck_01), CH (head pitch).
#  shoulders: shoulder joint position in the thorax frame (forward / lift over spine_05) -> clavicle yaw (CY) / pitch (CP).
#  arms: ArmRoll keeps the hanging arm vertical under the corrected chest; hip clearance PA: the wrist may not enter the hip zone
#     (lateral distance from the pelvis line below RH beside the hip, RW beside the waist, RF in front) - upper-arm abduction rises
#     fast when it does and decays slowly.
#  Montages (interactions, carry): values ease to the legacy constants. In the air: hold.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; out = {}
ABP = '/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'
FL = ['PS_K','PS_R2','PS_R3','PS_R4','PS_B1','PS_B2','PS_B3','PS_B4','PS_C3','PS_C5','PS_CN','PS_CH','PS_HK','PS_HMove','PS_KAR','PS_ShF','PS_ShL','PS_ShLRun','PS_KC',
      'PS_CYL','PS_CYR','PS_CPL','PS_CPR','PS_RH','PS_RW','PS_RF','PS_KAU','PS_KAD','PS_PAL','PS_PAR','PS_PAMax','GR_PDt','PS_A1','PS_A2','PS_A3','PS_A4','PS_ArmBase','PS_Eff','PS_CHR','PS_HRS','PS_Bent','PS_KARBent']
DRY = '--dry' in sys.argv
M = '`KismetMathLibrary.%s`'
def S(b): return '(`SceneComponent.GetSocketLocation` (`self.Manny`) "%s")' % b
def v(n): return '(`self.%s`)' % n
def dot(a, b): return '(%s %s %s)' % (M % 'Dot_VectorVector', a, b)
def clamp(x, lo, hi): return '(%s %s %s %s)' % (M % 'FClamp', x, lo, hi)
def sel(a, b, c): return '(%s %s %s %s)' % (M % 'SelectFloat', a, b, c)
def ab(x): return '(%s %s)' % (M % 'Abs', x)
UP = '(%s 0.0 0.0 1.0)' % (M % 'MakeVector')
def lean(a, b): return '(%s %s %s)' % (M % 'DegAtan2', dot('(- %s %s)' % (b, a), '_fw'), dot('(- %s %s)' % (b, a), UP))
DT = v('GR_PDt')
def gain(e, k): return clamp('(* (* %s %s) (+ 1.0 (/ %s 8.0)))' % (k, DT, ab(e)), '0.0', '0.5')
def ease(cur, legacy): return '(%s %s %s %s 3.0)' % (M % 'FInterpTo', cur, legacy, DT)
def integ(cur, e, k, lo, hi, legacy):
    # ACT: integrate; montage: ease to legacy; air: hold
    return sel(clamp('(+ %s (* %s %s))' % (cur, gain(e, k), e), lo, hi), sel(ease(cur, legacy), cur, '_mont'), '_act')
L = []
L.append('(bind _ai (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)))')
L.append('(bind _mont (`AnimInstance.IsAnyMontagePlaying` _ai))')
L.append('(bind _act (and (and (`self.PS_On`) (not _mont)) (`NavMovementComponent.IsMovingOnGround` (`self.CharacterMovement`))))')
# body frame from the hip line (not the capsule: the capsule snaps to the input direction, the body follows through the root offset)
L.append('(bind _rt (%s (- %s %s) 0.0001))' % (M % 'Vector_Normal2D', S('thigh_r'), S('thigh_l')))
L.append('(bind _fw (%s _rt %s))' % (M % 'Cross_VectorVector', UP))
for b, n in (('pelvis', '_p0'), ('spine_03', '_s3'), ('spine_05', '_s5'), ('neck_01', '_n1'), ('head', '_hd'), ('upperarm_l', '_ul'), ('upperarm_r', '_ur'), ('hand_l', '_hl'), ('hand_r', '_hr')):
    L.append('(bind %s %s)' % (n, S(b)))
L.append('(bind _a1 (- %s %s))' % (lean('_p0', '_s3'), v('PS_B1')))
L.append('(bind _a2 (- %s %s))' % (lean('_s3', '_s5'), v('PS_B2')))
L.append('(bind _a3 (- %s %s))' % (lean('_s5', '_n1'), v('PS_B3')))
L.append('(bind _a4 (- %s %s))' % (lean('_n1', '_hd'), v('PS_B4')))
L.append('(bind _d %s)' % clamp('_a1', '-15.0', '30.0'))
L.append('(bind _sp (%s (`self.GetVelocity`)))' % (M % 'VSizeXY'))
L.append('(bind _runa %s)' % clamp('(/ (- _sp 200.0) 215.0)', '0.0', '1.0'))
L.append('(bind _mova %s)' % clamp('(/ _sp 150.0)', '0.0', '1.0'))
for n, x in (('PS_A1', '_a1'), ('PS_A2', '_a2'), ('PS_A3', '_a3'), ('PS_A4', '_a4')): L.append('(set `self.%s` %s)' % (n, x))
L.append('(set `self.PS_C3` %s)' % integ(v('PS_C3'), '(- (+ (* %s _d) (* 4.0 %s)) _a2)' % (v('PS_R2'), v('PS_Eff')), v('PS_K'), '-25.0', '15.0', '-4.0'))
L.append('(set `self.PS_C5` %s)' % integ(v('PS_C5'), '(- (+ (* %s _d) (* 5.0 %s)) _a3)' % (v('PS_R3'), v('PS_Eff')), v('PS_K'), '-40.0', '15.0', '-12.0'))
L.append('(set `self.PS_CN` %s)' % integ(v('PS_CN'), '(- (* %s _d) _a4)' % v('PS_R4'), v('PS_K'), '-25.0', '30.0', '12.0'))
# head pitch (face axis = local +Y of the head bone): target = -HK x lean - HMove x moving; + roll tips the head down
HP = '(%s %s)' % (M % 'DegAsin', dot('(%s (`SceneComponent.GetSocketRotation` (`self.Manny`) "head"))' % (M % 'GetRightVector'), UP))
L.append('(bind _hp %s)' % HP)
L.append('(set `self.PS_CH` %s)' % integ(v('PS_CH'), '(- _hp (- (- 0.0 (* %s %s)) (* %s _mova)))' % (v('PS_HK'), clamp('_d', '0.0', '25.0'), v('PS_HMove')), v('PS_K'), '-25.0', '25.0', '-2.0'))
# head roll level (head lateral axis = local Z of the head bone)
L.append('(bind _ht (%s %s))' % (M % 'DegAsin', dot('(%s (`SceneComponent.GetSocketRotation` (`self.Manny`) "head"))' % (M % 'GetUpVector'), UP)))
L.append('(set `self.PS_CHR` %s)' % integ(v('PS_CHR'), '(* %s _ht)' % v('PS_HRS'), '(* 0.5 %s)' % v('PS_K'), '-10.0', '10.0', '0.0'))
# thorax frame: u = spine_03 -> neck_01, f = right x u
L.append('(bind _u (%s (- _n1 _s3) 0.0001))' % (M % 'Normal'))
L.append('(bind _f (%s _rt _u))' % (M % 'Cross_VectorVector'))
SHL = '(+ %s (* %s _runa))' % (v('PS_ShL'), v('PS_ShLRun'))
CG = clamp('(* (* %s %s) 4.0)' % (v('PS_KC'), DT), '0.0', '0.5')
def cint(pv, sign, target, meas):
    return '(set `self.%s` %s)' % (pv, sel(clamp('(%s %s (* %s (- %s %s)))' % (sign, v(pv), CG, target, meas), '-14.0', '14.0'), sel(ease(v(pv), '0.0'), v(pv), '_mont'), '_act'))
L.append('(bind _shf (- %s (* 0.5 (+ %s %s))))' % (v('PS_ShF'), dot('(- _ul _s5)', '_f'), dot('(- _ur _s5)', '_f')))
L.append('(bind _shl (- %s (* 0.5 (+ %s %s))))' % (SHL, dot('(- _ul _s5)', '_u'), dot('(- _ur _s5)', '_u')))
L.append(cint('PS_CYL', '+', '_shf', '0.0'))
L.append(cint('PS_CYR', '-', '_shf', '0.0'))
L.append(cint('PS_CPL', '+', '_shl', '0.0'))
L.append(cint('PS_CPR', '-', '_shl', '0.0'))
# hip clearance
for sd, hn, sg, pv in (('l', '_hl', '-1.0', 'PS_PAL'), ('r', '_hr', '1.0', 'PS_PAR')):
    L.append('(bind _lat%s (* %s %s))' % (sd, sg, dot('(- %s _p0)' % hn, '_rt')))
    L.append('(bind _fwd%s %s)' % (sd, dot('(- %s _p0)' % hn, '_fw')))
    L.append('(bind _z%s %s)' % (sd, dot('(- %s _p0)' % hn, UP)))
    side = '(%s _z%s 6.0 14.0 %s %s)' % (M % 'MapRangeClamped', sd, v('PS_RH'), v('PS_RW'))
    rmin = '(%s _fwd%s 8.0 22.0 %s %s)' % (M % 'MapRangeClamped', sd, side, v('PS_RF'))
    L.append('(bind _err%s (- %s _lat%s))' % (sd, rmin, sd))
    up = '(* (* %s %s) (%s _err%s 0.0))' % (v('PS_KAU'), DT, M % 'FMax', sd)
    dn = '(* (* %s %s) (* %s %s))' % (v('PS_KAD'), DT, v(pv), sel('1.0', '0.0', '(< _err%s -1.0)' % sd))
    L.append('(set `self.%s` %s)' % (pv, sel(clamp('(- (+ %s %s) %s)' % (v(pv), up, dn), '0.0', v('PS_PAMax')), sel(ease(v(pv), '0.0'), v(pv), '_mont'), '_act')))
L.append('(set `self.PS_Bent` (%s %s (%s (* 0.5 (+ _zl _zr)) -8.0 10.0 0.0 1.0) %s 3.0))' % (M % 'FInterpTo', v('PS_Bent'), M % 'MapRangeClamped', DT))
ARMROLL = '(* (- 0.0 (%s %s %s %s)) (+ %s %s))' % (M % 'Lerp', v('PS_KAR'), v('PS_KARBent'), v('PS_Bent'), v('PS_C3'), v('PS_C5'))
body = ['(if (`self.PS_On`)',
        '  (bind _asb (cast `%s` (`SkeletalMeshComponent.GetAnimInstance` (`self.Manny`)))' % ABP,
        '    (:`then`']
def W(n, x, y, z): body.append('      (set `%s.%s` (%s %s %s %s) _asb)' % (ABP, n, M % 'MakeVector', x, y, z))
def lin(*terms):
    # terms: (expr, (a,b,c)) -> three component expressions (posture nodes of these bones work in PARENT-BONE space; probe_axes.py)
    o = []
    for i in range(3):
        parts = ['(* %s %s)' % (e, repr(float(c[i]))) for e, c in terms if abs(c[i]) > 0.0005]
        x = parts[0] if parts else '0.0'
        for q in parts[1:]: x = '(+ %s %s)' % (x, q)
        o.append(x)
    return o
AX = json.load(open('Saved/UE59Work/r4/axes.json'))
def C(b, k): return AX[b]['cols'][k]
W('VI_Spine3', *lin((v('PS_C3'), C('spine_03', 0))))
W('VI_Spine5', *lin((v('PS_C5'), C('spine_05', 0))))
W('VI_Neck1', *lin((v('PS_CN'), C('neck_01', 0))))
W('VI_Head', *lin((v('PS_CH'), C('head', 0)), (v('PS_CHR'), C('head', 1))))
W('VI_ClavL', *lin((v('PS_CPL'), C('clavicle_l', 1)), (v('PS_CYL'), C('clavicle_l', 2))))
W('VI_ClavR', *lin((v('PS_CPR'), C('clavicle_r', 1)), (v('PS_CYR'), C('clavicle_r', 2))))
W('VI_ArmL', *lin((ARMROLL, C('upperarm_l', 0)), ('(+ %s %s)' % (v('PS_PAL'), v('PS_ArmBase')), C('upperarm_l', 1))))
W('VI_ArmR', *lin((ARMROLL, C('upperarm_r', 0)), ('(- 0.0 (+ %s %s))' % (v('PS_PAR'), v('PS_ArmBase')), C('upperarm_r', 1))))
body[-1] = body[-1] + ')'
body += ['    (:`CastFailed`', '      _)))']
ev = '\n\n(event `GR_Posture`\n' + '\n'.join('  ' + x for x in L + body) + ')'
open('Saved/UE59Work/dsl/posture_event.dsl', 'w', encoding='utf8').write(ev)
if DRY: print(ev[:2500]); print(len(ev)); sys.exit(0)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n, ty in [(n, 'float') for n in FL] + [('PS_On', 'bool')]:
    if '"%s"' % n in have: continue
    r = T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': ty})
    if isinstance(r, dict) and r.get('isError'): out['add_' + n] = 'err'
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
open('Saved/UE59Work/dsl/player_before_posture.dsl', 'w', encoding='utf8').write(dsl)
REAPPLY = '`GR_Posture`' in dsl
def line(prefix):
    Ls = [l for l in dsl.split('\n') if l.strip().startswith(prefix)]; assert len(Ls) == 1, (prefix, len(Ls)); return Ls[0]
par = line("(`parent.ReceiveTick` DeltaSeconds)"); ind = par[:len(par) - len(par.lstrip())]
bp0 = line('(`parent.ReceiveBeginPlay`)'); ind0 = bp0[:len(bp0) - len(bp0.lstrip())]
# tick order: GASP's PreCMC component (and so the movement component) ticks after the pawn tick, so the strafe / gait state written
# by the pawn from this frame's input reaches the movement component in the same frame (was one frame late: capsule flipped 180 deg
# for one frame on W->S, Motion Matching picked a Turn_180 clip for that frame)
edits = [{'oldString': bp0, 'newString': bp0 + '\n' + ind0 + '(`ActorComponent.AddTickPrerequisiteActor` (`self.AC_PreCMCTick`) self)'},
         {'oldString': par, 'newString': par + '\n' + ind + '(set `self.GR_PDt` DeltaSeconds)\n' + ind + '(`self.GR_Posture`)'},
         {'oldString': dsl.rstrip('\n')[-200:], 'newString': dsl.rstrip('\n')[-200:] + ev}]
if REAPPLY:
    NL = chr(10); i0 = dsl.index('(event `GR_Posture`'); i1 = dsl.find(NL + NL + '(event', i0); old = dsl[i0:] if i1 < 0 else dsl[i0:i1]
    edits = [{'oldString': old.rstrip(NL), 'newString': ev.strip()}]
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
out['edit'] = str(r2)[:2500] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300]
print('POSTURE', json.dumps(out)[:3200])
