# m_posture7_mcp.py = m_posture6 + round-7 CHEST ROLL DAMPER (trunk roll of the visible body around its own low-pass is
# counter-rotated through spine_03 / spine_05 by PS_RK; head lateral sway 8-11 cm at walk / run, an_bob7.py). Earlier header:
# m_posture6_mcp.py = m_posture2_mcp.py + round-6 change: the clip's own spine / neck flexion is no longer removed completely at run speed
# (keep factor = Lerp(1, PS_KeepRun, RunA) instead of 1 - RunA; user review: the natural source motion was zeroed above 415 cm/s).
# m_posture2_mcp.py (MCP, in-memory edit of BP_HybridA_Player; saved by a gated write job) - 2026-11-22 round 5.
# POSTURE CONTROLLER v2 (event GR_Posture, replaces the round-4 body). User feedback on v1: arms now too open, head / neck too
# straight, upright and held forward, shoulders not relaxed, fatigue collapses the body.
#  spine   v1 forced thorax / upper back / neck to fixed ratios of the lumbar lean (walk ended exactly on the stiff bind posture).
#          v2 target = ratio rule + (1 - RunA) x clamp(Keep x (clip's own value - rule), +-KeepMax): at idle / walk part of the
#          clip's natural flexion stays; at run the rule holds (the run clips curl 30-40 deg). Lower gain (PS_K).
#  head    v1 pinned the face axis to -1 deg in every gait. v2 target looks down a little (HP0 + HMove x moving + HK x lean) and
#          keeps HKeep of the clip's own pitch; roll levelling at 0.4 gain.
#  effort  PS_Eff = AC_Sph_Motion.Fat (slow). Small target offsets (E2/E3/E4 deg, head EH, shoulders ShEffF / ShEffL) - the ABP's
#          VE_ vectors (sudden 15 deg slump when a run ended) are zeroed by c_bodyspace2.py. One owner, no stacked layers.
#  shoulders  lift target closer to the clip (ShL), half of the L/R lift difference is evened out (ShAsym).
#  arms    v1 only pushed wrists out of a 21 cm zone (slow release) -> wings. v2: per-arm integrator DA brings the MEAN upper-arm
#          abduction (thorax frame) to a gait target (AbdBase + AbdRun + AbdSpr; raw clips: walk 17, tempo 22/15, run 36/27 L/R);
#          the forearm compensates so the hand does not swing into the hip / across the body: valgus KV x adduction (straight
#          arm) and humeral external rotation KR x adduction (flexed arm). The clearance term stays only as a penetration guard
#          (RH 18.3 / RW 15 / RF 1, fast release, max PAMax).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; out = {}; NL = chr(10)
ABP = '/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'; MOT = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'
NEW = ['PS_Keep', 'PS_KeepMax', 'PS_E2', 'PS_E3', 'PS_E4', 'PS_EH', 'PS_HP0', 'PS_HKeep', 'PS_ShAsym', 'PS_ShEffF', 'PS_ShEffL', 'PS_DAL', 'PS_DAR', 'PS_KArm',
       'PS_AbdBase', 'PS_AbdRun', 'PS_AbdSpr', 'PS_KV', 'PS_KR', 'PS_HRK', 'PS_AbdL', 'PS_AbdR', 'PS_KeepRun', 'PS_Lu', 'PS_LuK', 'PS_LuMax', 'PS_LuRun', 'PS_RD', 'PS_RB', 'PS_RK', 'PS_RLP', 'PS_RSign', 'PS_RInit']
DRY = '--dry' in sys.argv
M = '`KismetMathLibrary.%s`'
def S(b): return '(`SceneComponent.GetSocketLocation` (`self.Manny`) "%s")' % b
def v(n): return '(`self.%s`)' % n
def dot(a, b): return '(%s %s %s)' % (M % 'Dot_VectorVector', a, b)
def clamp(x, lo, hi): return '(%s %s %s %s)' % (M % 'FClamp', x, lo, hi)
def sel(a, b, c): return '(%s %s %s %s)' % (M % 'SelectFloat', a, b, c)
def ab(x): return '(%s %s)' % (M % 'Abs', x)
def fmax(a, b): return '(%s %s %s)' % (M % 'FMax', a, b)
UP = '(%s 0.0 0.0 1.0)' % (M % 'MakeVector')
def lean(a, b): return '(%s %s %s)' % (M % 'DegAtan2', dot('(- %s %s)' % (b, a), '_fw'), dot('(- %s %s)' % (b, a), UP))
DT = v('GR_PDt')
def gain(e, k, div='8.0'): return clamp('(* (* %s %s) (+ 1.0 (/ %s %s)))' % (k, DT, ab(e), div), '0.0', '0.5')
def ease(cur, legacy): return '(%s %s %s %s 3.0)' % (M % 'FInterpTo', cur, legacy, DT)
def integ(cur, e, k, lo, hi, legacy, div='8.0'):
    return sel(clamp('(+ %s (* %s %s))' % (cur, gain(e, k, div), e), lo, hi), sel(ease(cur, legacy), cur, '_mont'), '_act')
L = []
L.append('(bind _ai (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)))')
L.append('(bind _mont (`AnimInstance.IsAnyMontagePlaying` _ai))')
L.append('(bind _act (and (and (`self.PS_On`) (not _mont)) (`NavMovementComponent.IsMovingOnGround` (`self.CharacterMovement`))))')
L.append('(bind _rt (%s (- %s %s) 0.0001))' % (M % 'Vector_Normal2D', S('thigh_r'), S('thigh_l')))
L.append('(bind _fw (%s _rt %s))' % (M % 'Cross_VectorVector', UP))
for b, n in (('pelvis', '_p0'), ('spine_03', '_s3'), ('spine_05', '_s5'), ('neck_01', '_n1'), ('head', '_hd'), ('upperarm_l', '_ul'), ('upperarm_r', '_ur'),
             ('lowerarm_l', '_el'), ('lowerarm_r', '_er'), ('hand_l', '_hl'), ('hand_r', '_hr')):
    L.append('(bind %s %s)' % (n, S(b)))
L.append('(set `self.PS_Eff` (%s %s (`%s.Fat` (`self.SphMotion`)) %s 1.0))' % (M % 'FInterpTo', v('PS_Eff'), MOT, DT))
L.append('(bind _a1 (- %s %s))' % (lean('_p0', '_s3'), v('PS_B1')))
L.append('(bind _a2 (- %s %s))' % (lean('_s3', '_s5'), v('PS_B2')))
L.append('(bind _a3 (- %s %s))' % (lean('_s5', '_n1'), v('PS_B3')))
L.append('(bind _a4 (- %s %s))' % (lean('_n1', '_hd'), v('PS_B4')))
L.append('(bind _d %s)' % clamp('_a1', '-15.0', '30.0'))
L.append('(bind _sp (%s (`self.GetVelocity`)))' % (M % 'VSizeXY'))
L.append('(bind _runa %s)' % clamp('(/ (- _sp 200.0) 215.0)', '0.0', '1.0'))
L.append('(bind _mova %s)' % clamp('(/ _sp 150.0)', '0.0', '1.0'))
for n, x in (('PS_A1', '_a1'), ('PS_A2', '_a2'), ('PS_A3', '_a3'), ('PS_A4', '_a4')): L.append('(set `self.%s` %s)' % (n, x))
# MOMENTUM RESPONSE (round 5): the trunk leans toward the acceleration of the body (start: forward, brake: back, turn: into the
# turn) through an under-damped spring, so it rocks back and settles after the acceleration ends. Target angle = PS_LK x atan(a / g).
VEL = '(`self.GetVelocity`)'
L.append('(bind _dts (%s %s 0.004 0.05))' % (M % 'FClamp', DT))
L.append('(bind _acc (/ (- %s (`self.PS_PrevV`)) _dts))' % VEL)
L.append('(set `self.PS_PrevV` %s)' % VEL)
L.append('(set `self.PS_AccF` (%s %s %s _dts 10.0))' % (M % 'FInterpTo', v('PS_AccF'), clamp(dot('_acc', '_fw'), '-2500.0', '2500.0')))
L.append('(set `self.PS_AccR` (%s %s %s _dts 10.0))' % (M % 'FInterpTo', v('PS_AccR'), clamp(dot('_acc', '_rt'), '-2500.0', '2500.0')))
for ax, st, vel in (('PS_AccF', 'PS_LP', 'PS_LPV'), ('PS_AccR', 'PS_LR', 'PS_LRV')):
    tg = sel('(* %s (%s %s 981.0))' % (v('PS_LK'), M % 'DegAtan2', v(ax)), '0.0', '_act')
    L.append('(set `self.%s` (+ %s (* _dts (- (* (* %s %s) (- %s %s)) (* (* (* 2.0 %s) %s) %s)))))' % (vel, v(vel), v('PS_LW'), v('PS_LW'), tg, v(st), v('PS_LZ'), v('PS_LW'), v(vel)))
    L.append('(set `self.%s` %s)' % (st, clamp('(+ %s (* _dts %s))' % (v(st), v(vel)), '-12.0', '12.0')))
# START LUNGE LIMITER (round 6): every run / sprint start clip of the project (Neutral and Relaxed) is an athletic lunge - raw trunk pitch
# 41-61 deg, pelvis drop 15-22 cm (probe_starts6.py); in game the visible trunk reached 30 deg and the head dipped 33 cm in 0.45 s
# (f5_L_60 s9). The trunk pitch above PS_LuMax (+ PS_LuRun x RunA) is taken back through spine_03 / spine_05 (gain PS_LuK, 8 /s).
L.append('(bind _ltot %s)' % lean('_p0', '_n1'))
L.append('(set `self.PS_Lu` (%s %s %s _dts 8.0))' % (M % 'FInterpTo', v('PS_Lu'), sel(clamp('(* (- 0.0 %s) %s)' % (v('PS_LuK'), fmax('(- _ltot (+ %s (* %s _runa)))' % (v('PS_LuMax'), v('PS_LuRun')), '0.0')), '-24.0', '0.0'), '0.0', '_act')))
# ROUND 7 CHEST ROLL DAMPER: roll = lateral lean of pelvis->neck_01 in the hip-line frame; the previous correction is taken out so the
# estimate is the uncorrected roll; dynamic part = estimate - low-pass (PS_RLP 1/s); correction PS_RD = PS_RSign x PS_RK x dynamic.
L.append('(bind _rl (- %s %s))' % ('(%s %s %s)' % (M % 'DegAtan2', dot('(- _n1 _p0)', '_rt'), dot('(- _n1 _p0)', UP)), v('PS_RD')))
L.append('(set `self.PS_RB` %s)' % sel('(%s %s _rl _dts %s)' % (M % 'FInterpTo', v('PS_RB'), v('PS_RLP')), '_rl', '(> %s 0.5)' % v('PS_RInit')))
L.append('(set `self.PS_RInit` 1.0)')
L.append('(set `self.PS_RD` %s)' % sel(clamp('(* (* %s %s) (- _rl %s))' % (v('PS_RSign'), v('PS_RK'), v('PS_RB')), '-8.0', '8.0'), '0.0', '_act'))
def tgt(ratio, raw, eff):
    rule = '(* %s _d)' % v(ratio)
    keep = ('(* (%s 1.0 %s _runa) ' % (M % 'Lerp', v('PS_KeepRun'))) + '%s)' % clamp('(* %s (- %s %s))' % (v('PS_Keep'), raw, rule), '(- 0.0 %s)' % v('PS_KeepMax'), v('PS_KeepMax'))
    return '(+ (+ %s %s) (* %s %s))' % (rule, keep, v(eff), v('PS_Eff'))
RAW2 = '(- _a2 %s)' % v('PS_C3'); RAW3 = '(- _a3 (+ %s %s))' % (v('PS_C3'), v('PS_C5')); RAW4 = '(- _a4 (+ (+ %s %s) %s))' % (v('PS_C3'), v('PS_C5'), v('PS_CN'))
L.append('(bind _t2 %s)' % tgt('PS_R2', RAW2, 'PS_E2'))
L.append('(bind _t3 %s)' % tgt('PS_R3', RAW3, 'PS_E3'))
L.append('(bind _t4 %s)' % tgt('PS_R4', RAW4, 'PS_E4'))
L.append('(set `self.PS_C3` %s)' % integ(v('PS_C3'), '(- _t2 _a2)', v('PS_K'), '-25.0', '15.0', '-4.0'))
L.append('(set `self.PS_C5` %s)' % integ(v('PS_C5'), '(- _t3 _a3)', v('PS_K'), '-40.0', '15.0', '-12.0'))
L.append('(set `self.PS_CN` %s)' % integ(v('PS_CN'), '(- _t4 _a4)', v('PS_K'), '-25.0', '30.0', '12.0'))
# head pitch (face axis = local +Y of the head bone); + CH tips the head down, so the clip's own pitch = measured + CH
HP = '(%s %s)' % (M % 'DegAsin', dot('(%s (`SceneComponent.GetSocketRotation` (`self.Manny`) "head"))' % (M % 'GetRightVector'), UP))
L.append('(bind _hp %s)' % HP)
L.append('(bind _tp0 (- 0.0 (+ (+ (+ %s (* %s _mova)) (* %s %s)) (* %s %s))))' % (v('PS_HP0'), v('PS_HMove'), v('PS_HK'), clamp('_d', '0.0', '25.0'), v('PS_EH'), v('PS_Eff')))
L.append('(bind _tp (+ _tp0 %s))' % clamp('(* %s (- (+ _hp %s) _tp0))' % (v('PS_HKeep'), v('PS_CH')), '-6.0', '6.0'))
L.append('(set `self.PS_CH` %s)' % integ(v('PS_CH'), '(- _hp _tp)', v('PS_K'), '-25.0', '25.0', '-2.0'))
L.append('(bind _ht (%s %s))' % (M % 'DegAsin', dot('(%s (`SceneComponent.GetSocketRotation` (`self.Manny`) "head"))' % (M % 'GetUpVector'), UP)))
L.append('(set `self.PS_CHR` %s)' % integ(v('PS_CHR'), '(* %s _ht)' % v('PS_HRS'), '(* %s %s)' % (v('PS_HRK'), v('PS_K')), '-10.0', '10.0', '0.0'))
# thorax frame: u = spine_03 -> neck_01, f = right x u
L.append('(bind _u (%s (- _n1 _s3) 0.0001))' % (M % 'Normal'))
L.append('(bind _f (%s _rt _u))' % (M % 'Cross_VectorVector'))
L.append('(bind _lfl %s)' % dot('(- _ul _s5)', '_u')); L.append('(bind _lfr %s)' % dot('(- _ur _s5)', '_u'))
L.append('(bind _lfm (* 0.5 (+ _lfl _lfr)))')
SHL = '(- (+ %s (* %s _runa)) (* %s %s))' % (v('PS_ShL'), v('PS_ShLRun'), v('PS_ShEffL'), v('PS_Eff'))
SHF = '(+ %s (* %s %s))' % (v('PS_ShF'), v('PS_ShEffF'), v('PS_Eff'))
L.append('(bind _shf (- %s (* 0.5 (+ %s %s))))' % (SHF, dot('(- _ul _s5)', '_f'), dot('(- _ur _s5)', '_f')))
L.append('(bind _shll (- %s (%s _lfm _lfl %s)))' % (SHL, M % 'Lerp', v('PS_ShAsym')))
L.append('(bind _shlr (- %s (%s _lfm _lfr %s)))' % (SHL, M % 'Lerp', v('PS_ShAsym')))
CG = clamp('(* (* %s %s) 4.0)' % (v('PS_KC'), DT), '0.0', '0.5')
def cint(pv, sign, err):
    return '(set `self.%s` %s)' % (pv, sel(clamp('(%s %s (* %s %s))' % (sign, v(pv), CG, err), '-14.0', '14.0'), sel(ease(v(pv), '0.0'), v(pv), '_mont'), '_act'))
L.append(cint('PS_CYL', '+', '_shf')); L.append(cint('PS_CYR', '-', '_shf'))
L.append(cint('PS_CPL', '+', '_shll')); L.append(cint('PS_CPR', '-', '_shlr'))
# arms: mean abduction per arm (thorax frame) -> gait target
L.append('(bind _tabd (+ (+ %s (* %s %s)) (* %s %s)))' % (v('PS_AbdBase'), v('PS_AbdRun'), clamp('(/ (- _sp 180.0) 235.0)', '0.0', '1.0'), v('PS_AbdSpr'), clamp('(/ (- _sp 415.0) 170.0)', '0.0', '1.0')))
for sd, un, en, sg, da, dbg in (('l', '_ul', '_el', '-1.0', 'PS_DAL', 'PS_AbdL'), ('r', '_ur', '_er', '1.0', 'PS_DAR', 'PS_AbdR')):
    L.append('(bind _abd%s (%s (* %s %s) (- 0.0 %s)))' % (sd, M % 'DegAtan2', sg, dot('(- %s %s)' % (en, un), '_rt'), dot('(- %s %s)' % (en, un), '_u')))
    L.append('(set `self.%s` _abd%s)' % (dbg, sd))
    # round 7d: while skimming a side wall the contact layer tucks the wall-side arm to CT_Tuck; the -14 deg floor cancelled most of it
    # (elbow 4.9 cm inside the wall at run), so the floor follows the graze amount.
    L.append('(set `self.%s` %s)' % (da, integ(v(da), '(- _tabd _abd%s)' % sd, v('PS_KArm'), '(%s -14.0 (* %s %s))' % (M % 'FMin', v('CT_TuckNow'), v('CT_Graze')), '6.0', '0.0', '10.0')))
# hip / waist / front penetration guard
for sd, hn, sg, pv in (('l', '_hl', '-1.0', 'PS_PAL'), ('r', '_hr', '1.0', 'PS_PAR')):
    L.append('(bind _lat%s (* %s %s))' % (sd, sg, dot('(- %s _p0)' % hn, '_rt')))
    L.append('(bind _fwd%s %s)' % (sd, dot('(- %s _p0)' % hn, '_fw')))
    L.append('(bind _z%s %s)' % (sd, dot('(- %s _p0)' % hn, UP)))
    side = '(%s _z%s 6.0 14.0 %s %s)' % (M % 'MapRangeClamped', sd, v('PS_RH'), v('PS_RW'))
    rmin = '(%s _fwd%s 8.0 22.0 %s %s)' % (M % 'MapRangeClamped', sd, side, v('PS_RF'))
    L.append('(bind _err%s (- %s _lat%s))' % (sd, rmin, sd))
    up = '(* (* %s %s) (%s _err%s 0.0))' % (v('PS_KAU'), DT, M % 'FMax', sd)
    dn = '(* (* %s %s) (* %s %s))' % (v('PS_KAD'), DT, v(pv), sel('1.0', '0.0', '(< _err%s -0.5)' % sd))
    L.append('(set `self.%s` %s)' % (pv, sel(clamp('(- (+ %s %s) %s)' % (v(pv), up, dn), '0.0', v('PS_PAMax')), sel(ease(v(pv), '0.0'), v(pv), '_mont'), '_act')))
L.append('(set `self.PS_Bent` (%s %s (%s (* 0.5 (+ _zl _zr)) -8.0 10.0 0.0 1.0) %s 3.0))' % (M % 'FInterpTo', v('PS_Bent'), M % 'MapRangeClamped', DT))
ARMROLL = '(* (- 0.0 (%s %s %s %s)) (+ %s %s))' % (M % 'Lerp', v('PS_KAR'), v('PS_KARBent'), v('PS_Bent'), v('PS_C3'), v('PS_C5'))
body = ['(if (`self.PS_On`)',
        '  (bind _asb (cast `%s` (`SkeletalMeshComponent.GetAnimInstance` (`self.Manny`)))' % ABP,
        '    (:`then`']
def W(n, x, y, z): body.append('      (set `%s.%s` (%s %s %s %s) _asb)' % (ABP, n, M % 'MakeVector', x, y, z))
def lin(*terms):
    o = []
    for i in range(3):
        parts = ['(* %s %s)' % (e, repr(float(c[i]))) for e, c in terms if abs(c[i]) > 0.0005]
        x = parts[0] if parts else '0.0'
        for q in parts[1:]: x = '(+ %s %s)' % (x, q)
        o.append(x)
    return o
AX = json.load(open('Saved/UE59Work/r4/axes.json'))
def C(b, k): return AX[b]['cols'][k]
W('VI_Spine3', *lin(('(+ (+ %s (* 0.5 %s)) (* 0.5 %s))' % (v('PS_C3'), v('PS_LP'), v('PS_Lu')), C('spine_03', 0)), ('(+ (* 0.5 %s) (* 0.5 %s))' % (v('PS_LR'), v('PS_RD')), C('spine_03', 1))))
W('VI_Spine5', *lin(('(+ (+ %s (* 0.5 %s)) (* 0.5 %s))' % (v('PS_C5'), v('PS_LP'), v('PS_Lu')), C('spine_05', 0)), ('(+ (* 0.5 %s) (* 0.5 %s))' % (v('PS_LR'), v('PS_RD')), C('spine_05', 1))))
W('VI_Neck1', *lin((v('PS_CN'), C('neck_01', 0))))
W('VI_Head', *lin(('(- %s (* 0.3 %s))' % (v('PS_CH'), v('PS_LP')), C('head', 0)), ('(- %s (* 0.4 %s))' % (v('PS_CHR'), v('PS_LR')), C('head', 1))))
W('VI_ClavL', *lin((v('PS_CPL'), C('clavicle_l', 1)), (v('PS_CYL'), C('clavicle_l', 2))))
W('VI_ClavR', *lin((v('PS_CPR'), C('clavicle_r', 1)), (v('PS_CYR'), C('clavicle_r', 2))))
W('VI_ArmL', *lin((ARMROLL, C('upperarm_l', 0)), ('(+ (+ %s %s) %s)' % (v('PS_DAL'), v('PS_PAL'), v('PS_ArmBase')), C('upperarm_l', 1))))
W('VI_ArmR', *lin((ARMROLL, C('upperarm_r', 0)), ('(- 0.0 (+ (+ %s %s) %s))' % (v('PS_DAR'), v('PS_PAR'), v('PS_ArmBase')), C('upperarm_r', 1))))
# forearm node in PARENT (upper arm) space: roll -1 = humeral external rotation, pitch +1 = valgus (probe_fore.py), both sides
for sd, da in (('L', 'PS_DAL'), ('R', 'PS_DAR')):
    add = fmax('(- 0.0 %s)' % v(da), '0.0')
    W('VI_Fore' + sd, '(- 0.0 (* (* %s %s) %s))' % (v('PS_KR'), add, v('PS_Bent')), '(* (* %s %s) (- 1.0 %s))' % (v('PS_KV'), add, v('PS_Bent')), '0.0')
body[-1] = body[-1] + ')'
body += ['    (:`CastFailed`', '      _)))']
ev = NL + NL + '(event `GR_Posture`' + NL + NL.join('  ' + x for x in L + body) + ')'
open('Saved/UE59Work/dsl/posture2_event.dsl', 'w', encoding='utf8').write(ev)
if DRY: print(len(ev)); sys.exit(0)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"PS_PrevV"' not in have: T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'PS_PrevV', 'typeName': 'Vector'})
for n in NEW + ['PS_AccF', 'PS_AccR', 'PS_LP', 'PS_LPV', 'PS_LR', 'PS_LRV', 'PS_LK', 'PS_LW', 'PS_LZ']:
    if '"%s"' % n in have: continue
    r = T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'})
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
open('Saved/UE59Work/dsl/player_before_posture2.dsl', 'w', encoding='utf8').write(dsl)
i0 = dsl.index('(event `GR_Posture`'); i1 = dsl.find(NL + NL + '(event', i0); old = dsl[i0:] if i1 < 0 else dsl[i0:i1]
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old.rstrip(NL), 'newString': ev.strip()}]})
out['edit'] = str(r2)[:2500] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300]
print('POSTURE2', json.dumps(out)[:3200])
