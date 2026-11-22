# m_contact6_mcp.py (MCP, in-memory edit of BP_HybridA_Player; re-appliable; replaces the round-5 event GR_Contact) - 2026-11-23 round 6.
# CONTACT v2. Round-5 defects this answers (report 9765db9 + user review):
#   - knee / shin inside the obstacle while kneeling: the kneel started with the capsule still touching the obstacle (rebound 18 cm by an
#     impulse against ~1000 cm/s2 braking). Now a scripted retreat step (CT_RetD cm, shortened by the free space behind) happens FIRST;
#     the kneel only starts when the capsule is >= CT_KneelClr cm from the surface, otherwise the reaction stays a standing brace.
#   - every heavy contact = the same kneel: reaction is chosen from the contact: head-on block (wall / waist / knee) -> retreat + kneel
#     or brace (no room); low isolated obstacle at speed (shin height, the capsule would step over it) -> TRIP: stumble on, stagger, or a
#     forward fall to the ground + lying + get-up when the ground ahead is flat and free (three ground probes + chest probe); carrying
#     with both hands never falls prone (kneel / stagger instead), and has no hand support.
#   - point / normal / distance came from different traces: now all three are taken from the NEAREST hit; the hit actor's name is kept
#     and the same object cannot trigger again until the body has separated CT_SepMin cm from it (or 2.5 s passed).
#   - momentum: velocity after the impact = tangential part x CT_TanKeep + rebound along the normal (was: replaced by the rebound).
#   - control: lying / kneeling can be cut short by a move input after CT_CutMin s (safe phase); the get-up itself is not interruptible.
#   - stairs / ramps are not obstacles: a low hit only counts when a second knee-height probe finds nothing within the next 1.5 m.
# States: 0 normal, 3 blocked, 4 stagger (CT_Pend 1 = retreat before kneeling), 5 kneeling down, 6 on one knee, 7 standing up,
#         8 falling forward, 9 lying, 10 getting up.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; out = {}; NL = chr(10)
MOT = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; DRY = '--dry' in sys.argv
KN = '/Game/MC_Core_Motion/Animations/Kneel/'; FL = '/Game/Sphirus/Player/Anim/Fall/'
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
def play(asset, bi, bo, rate, start): return '(`AnimInstance.PlaySlotAnimationAsDynamicMontage` _ai "%s.%s" "DefaultSlot" %s %s %s 1 -1.0 %s)' % (asset, asset.split('/')[-1], bi, bo, rate, start)
def setvel(x): return '(set `MovementComponent.Velocity` %s (`self.CharacterMovement`))' % x
UP = mv('0.0', '0.0', '1.0')
L = []
L.append('(bind _dt %s)' % F('FClamp', v('GR_PDt'), '0.004', '0.05'))
L.append('(bind _ai (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)))')
L.append('(bind _vel (`self.GetVelocity`))')
L.append('(bind _sp %s)' % F('VSizeXY', '_vel'))
L.append('(bind _hasin (> %s 0.1))' % F('VSize', v('GR_RawIn')))
L.append('(bind _ind %s)' % F('Vector_Normal2D', v('GR_RawIn'), '0.0001'))
L.append('(bind _dir %s)' % selv(v('CT_HitDir'), selv(F('Vector_Normal2D', v('CT_PrevVel'), '0.0001'), selv('_ind', '(`self.GetActorForwardVector`)', '_hasin'), '(> %s 40.0)' % F('VSizeXY', v('CT_PrevVel'))), '(> %s 0)' % v('CT_State')))
L.append('(bind _rt %s)' % F('Cross_VectorVector', UP, '_dir'))
L.append('(bind _loc (`self.K2_GetActorLocation`))')
L.append('(bind _len (+ %s 30.0))' % F('FClamp', '(* _sp %s)' % v('CT_Look'), '45.0', '260.0'))
def trace(tag, st, en):
    L.append('(bind (_h%s _b%s) (`KismetSystemLibrary.LineTraceSingle` %s %s "TraceTypeQuery1"))' % (tag, tag, st, en))
def tr(tag, z, lat=None, ln='_len', back=False):
    st = '(+ _loc %s)' % mv('0.0', '0.0', z)
    if lat is not None: en = '(+ %s %s)' % (st, vs('_rt', lat))
    elif back: en = '(- %s %s)' % (st, vs('_dir', ln))
    else: en = '(+ %s %s)' % (st, vs('_dir', ln))
    trace(tag, st, en)
    L.append('(bind _d%s %s)' % (tag, sel('(- (`.Distance` (`GameplayStatics.BreakHitResult` _h%s)) 30.0)' % tag, '999.0', '_b' + tag)))
tr('hi', '52.0'); tr('mid', '6.0'); tr('kn', '-34.0'); tr('ll', '42.0', '-52.0'); tr('lr', '42.0', '52.0')
tr('sh', '-70.0'); tr('k2', '-34.0', ln='(+ _len 150.0)'); tr('bk', '6.0', ln='150.0', back=True)
def down(tag, d):
    st = '(+ (+ _loc %s) %s)' % (vs('_dir', d), mv('0.0', '0.0', '40.0'))
    trace(tag, st, '(- %s %s)' % (st, mv('0.0', '0.0', '190.0')))
    L.append('(bind _f%s %s)' % (tag, AND('_b' + tag, '(< %s 15.0)' % F('Abs', '(- (.z (`.ImpactPoint` (`GameplayStatics.BreakHitResult` _h%s))) (- (.z _loc) %s))' % (tag, v('CT_HalfH'))))))
down('g0', '(+ %s 85.0)' % F('FMin', '_dsh', '60.0')); down('g1', '120.0'); down('g2', '210.0'); down('g3', '300.0')
L.append('(bind _hh (`CapsuleComponent.GetScaledCapsuleHalfHeight` (`self.CapsuleComponent`)))')
tr('hd', '(- 168.0 _hh)', ln='(+ _len 20.0)')   # fixed 168 cm above the floor, also while crouched (the probe dropped with the capsule: crouch / stand flicker)
def upt(tag, off):
    st = '(+ _loc %s)' % vs('_dir', off)
    trace(tag, st, '(+ %s %s)' % (st, mv('0.0', '0.0', '135.0')))
upt('u0', '0.0'); upt('u1', '45.0'); upt('u2', '-45.0')
def hn(tag): return '(`.ImpactNormal` (`GameplayStatics.BreakHitResult` _h%s))' % tag
def hp(tag): return '(`.ImpactPoint` (`GameplayStatics.BreakHitResult` _h%s))' % tag
def ha(tag): return '(`KismetSystemLibrary.GetObjectName` (`.HitActor` (`GameplayStatics.BreakHitResult` _h%s)))' % tag
L.append('(bind _hitb %s)' % OR('_bhi', '_bmid', '_bkn'))
L.append('(bind _db %s)' % F('FMin', '_dhi', F('FMin', '_dmid', '_dkn')))
# nearest hit owns normal, point and identity (one contact = one trace)
nmid = AND('_bmid', '(<= _dmid _dhi)', '(<= _dmid _dkn)'); nhi = AND('_bhi', '(<= _dhi _dkn)')
L.append('(bind _n %s)' % F('Vector_Normal2D', selv(hn('mid'), selv(hn('hi'), hn('kn'), nhi), nmid), '0.0001'))
L.append('(bind _pt %s)' % selv(hp('mid'), selv(hp('hi'), hp('kn'), nhi), nmid))
L.append('(bind _obj (select `bool` %s :`true` %s :`false` (select `bool` %s :`true` %s :`false` %s)))' % (nmid, ha('mid'), nhi, ha('hi'), ha('kn')))
L.append('(bind _cosi (- 0.0 %s))' % F('Dot_VectorVector', '_dir', '_n'))
L.append('(bind _vn %s)' % sel(F('FMax', '(- 0.0 %s)' % F('Dot_VectorVector', '_vel', '_n'), '0.0'), '0.0', '_hitb'))
L.append('(bind _cls %s)' % F('SelectInt', '1', F('SelectInt', '2', F('SelectInt', '3', F('SelectInt', '4', '0', '_bhi'), '_bkn'), '_bmid'), AND('_bhi', '_bmid')))
L.append('(bind _c2h %s)' % v('GR_Load2H'))
L.append('(bind _carry %s)' % OR(v('GR_CarryActive'), '_c2h'))
L.append('(bind _fat %s)' % mot('Fat'))
L.append('(bind _gnd (`NavMovementComponent.IsMovingOnGround` (`self.CharacterMovement`)))')
L.append('(bind _st0 %s)' % v('CT_State'))
L.append('(bind _on %s)' % AND(v('CT_On'), '_gnd'))
L.append('(bind _cl (`AnimInstance.GetCurveValue` _ai "contact_l"))')
L.append('(bind _cr (`AnimInstance.GetCurveValue` _ai "contact_r"))')
for n in ('CT_Cool', 'CT_LockT', 'CT_CapT'):
    L.append(S(n, F('FMax', '(- %s _dt)' % v(n), '0.0')))
L.append(S('CT_T', sel('(+ %s _dt)' % v('CT_T'), '0.0', '(> _st0 0)')))
L.append(S('CT_SpRef', F('FMax', '_sp', '(- %s (* 15.0 _dt))' % v('CT_SpRef'))))
L.append(S('CT_Since', '(+ %s _dt)' % v('CT_Since')))
L.append(S('CT_Sep', F('FMax', v('CT_Sep'), F('FMin', '_db', '200.0'))))
# anticipation (head-on wall / waist-high with the input held)
# a knee-high obstacle is seen and respected at walking pace (below CT_KneeSeeV); at tempo / run it is what trips
L.append('(bind _kslow %s)' % AND('_bkn', '(< _sp %s)' % v('CT_KneeSeeV')))
L.append('(bind _head %s)' % AND('_on', OR('_bhi', '_bmid', '_kslow'), '(> _cosi %s)' % v('CT_CosHead'), '_hasin', '(> %s 0.5)' % F('Dot_VectorVector', '_ind', '_dir')))
L.append('(bind _dw %s)' % F('FMin', F('FMin', '_dhi', '_dmid'), sel('_dkn', '999.0', '_kslow')))
L.append(S('CT_Prox', F('FInterpTo', v('CT_Prox'), sel(F('MapRangeClamped', '_dw', '12.0', '70.0', '1.0', '0.0'), '0.0', '_head'), '_dt', '10.0')))
L.append('(bind _capa %s)' % sel('(+ 22.0 %s)' % F('Sqrt', '(* (* 2.0 %s) %s)' % (v('CT_Dec'), F('FMax', '(- _dw %s)' % v('CT_StandOff'), '0.0'))), '100000.0', '_head'))
# graze
L.append('(bind _gl %s)' % F('MapRangeClamped', '_sp', '150.0', '400.0', '3.0', '12.0'))
L.append('(bind _grl %s)' % AND('_on', '_bll', '(< _dll _gl)', '(> _sp 120.0)'))
L.append('(bind _grr %s)' % AND('_on', '_blr', '(< _dlr _gl)', '(> _sp 120.0)'))
L.append('(bind _gr %s)' % OR('_grl', '_grr'))
L.append(S('CT_Graze', F('FInterpTo', v('CT_Graze'), sel('1.0', '0.0', '_gr'), '_dt', '8.0')))
L.append('(bind _capg %s)' % sel(F('FMax', '(* %s %s)' % (v('CT_SpRef'), F('MapRangeClamped', F('FMin', '_dll', '_dlr'), '0.0', '10.0', '0.8', '1.0')), '150.0'), '100000.0', '_gr'))
L.append(S('PS_LRV', '(+ %s (* (* %s _dt) %s))' % (v('PS_LRV'), v('CT_GrazeLean'), sel(sel('1.0', '-1.0', '_grl'), '0.0', '_gr'))))
# round 6b: the wall-side elbow went 7-11 cm into the wall while skimming it (run arm swing abduction 20-45 deg): tuck that arm
L.append(S('PS_DAL', sel(F('FInterpTo', v('PS_DAL'), v('CT_Tuck'), '_dt', '12.0'), v('PS_DAL'), '_grl')))
L.append(S('PS_DAR', sel(F('FInterpTo', v('PS_DAR'), v('CT_Tuck'), '_dt', '12.0'), v('PS_DAR'), '_grr')))
# round 6b: LOW PASSAGE. Something at head height only (capsule top 176 cm; chest and waist probes free): duck under it instead of
# standing in front of it; stand up again when three vertical probes (here, 45 cm ahead, 45 cm behind) are clear. Only an automatic
# duck is undone automatically (a crouch chosen by the player stays).
L.append('(bind _lowp %s)' % AND('_on', '_bhd', '(not _bhi)', '(not _bmid)', '(not _bkn)', '_hasin', '(< _dhd %s)' % v('CT_DuckD'), '(== _st0 0)', '(> %s 0.5)' % F('Dot_VectorVector', '_ind', '_dir')))
# stairs / slopes
L.append(S('CT_Vz', F('FInterpTo', v('CT_Vz'), sel(F('FClamp', '(/ (- (.z _loc) %s) _dt)' % v('CT_ZPrev'), '-400.0', '400.0'), '0.0', '_gnd'), '_dt', '6.0')))
L.append(S('CT_ZPrev', '(.z _loc)'))
# round 6b: stairs. A walk stride (65 cm) spans two 30 cm treads, so the feet landed two steps apart and the pelvis could not rise
# above the rear leg's reach (knee 45 deg, pelvis 52 cm over the leading foot). On a steep rise (|Vz| / speed above CT_SlopeLo..Hi,
# stairs 18/30 = 0.6, a 15 deg ramp = 0.27) the speed is taken down to one-tread-per-step pace: CT_StairV walking, CT_StairRunV running.
L.append('(bind _slr (/ %s %s))' % (F('Abs', v('CT_Vz')), F('FMax', '_sp', '60.0')))
L.append('(bind _capst %s)' % sel(F('MapRangeClamped', '_slr', v('CT_SlopeLo'), v('CT_SlopeHi'), '400.0', sel(v('CT_StairRunV'), v('CT_StairV'), '(>= %s 1)' % v('GR_GaitSel'))), '100000.0', AND('_on', '(> %s 30.0)' % F('Abs', v('CT_Vz')))))
L.append('(bind _capz %s)' % F('FMin', '_capst', sel(F('MapRangeClamped', F('Abs', v('CT_Vz')), '60.0', '160.0', '400.0', '260.0'), '100000.0', AND('_on', '(> %s 60.0)' % F('Abs', v('CT_Vz'))))))
# impact (head-on block) and trip (isolated low obstacle)
same = AND('(== _obj %s)' % v('CT_ObjN'), '(< %s %s)' % (v('CT_Sep'), v('CT_SepMin')), '(< %s 2.5)' % v('CT_Since'))
hitA = AND('(> (- %s _vn) (+ (* 2600.0 _dt) 30.0))' % v('CT_VnPrev'), '(< _vn (* 0.4 %s))' % v('CT_VnPrev'), '(> %s %s)' % (v('CT_VnPrev'), v('CT_VMin')))
hitB = AND('(> (- %s _vn) (+ (* 5200.0 _dt) 30.0))' % v('CT_VnPrev2'), '(< _vn (* 0.3 %s))' % v('CT_VnPrev2'), '(> %s %s)' % (v('CT_VnPrev2'), v('CT_VMin')))
L.append('(bind _imp %s)' % AND('_on', '(== _st0 0)', '(<= %s 0.0)' % v('CT_Cool'), '(< _db 10.0)', OR(hitA, hitB), '(not %s)' % same))
L.append('(bind _iso %s)' % AND('_bsh', '(not _bk2)', '(not _hitb)'))
L.append('(bind _trip %s)' % AND('_on', '(== _st0 0)', '(<= %s 0.0)' % v('CT_Cool'), '_iso', '(< _dsh %s)' % F('FMax', '8.0', '(* _sp 0.04)'), '(> _sp %s)' % v('CT_TripV'), '(> %s 0.6)' % F('Dot_VectorVector', '_dir', F('Vector_Normal2D', '_vel', '0.0001'))))
L.append('(bind _vimp %s)' % sel('_sp', F('FMax', v('CT_VnPrev'), v('CT_VnPrev2')), '_trip'))
L.append('(bind _hf %s)' % sel(v('CT_TripH'), sel('1.0', sel('1.15', sel('1.5', '0.8', '(== _cls 3)'), '(== _cls 2)'), '(== _cls 1)'), '_trip'))
L.append('(bind _air %s)' % AND('(> _cl 50.0)', '(> _cr 50.0)'))
L.append('(bind _sv (* (* (* (/ %s %s) _hf) (+ (+ (+ 1.0 (* %s _fat)) %s) %s)) %s))' % ('_vimp', v('CT_VRef'), v('CT_KFat'), sel('0.25', '0.0', '_carry'), sel('0.2', '0.0', '_air'), F('Lerp', '1.0', v('CT_KAnt'), v('CT_Prox'))))
L.append('(bind _lvl %s)' % F('SelectInt', '3', F('SelectInt', '2', F('SelectInt', '1', '0', '(>= _sv %s)' % v('CT_SBump')), '(>= _sv %s)' % v('CT_SStag')), '(>= _sv %s)' % v('CT_SDown')))
L.append('(bind _flat %s)' % AND('_fg0', '_fg1', '_fg2', '_fg3', '(not _bhi)', '(not _bmid)'))
L.append('(bind _room %s)' % F('FClamp', '(/ (- _dbk 10.0) 45.0)', '0.0', '1.0'))
L.append('(bind _vtan (- %s %s))' % (v('CT_PrevVel'), vs('_n', F('Dot_VectorVector', v('CT_PrevVel'), '_n'))))
body = []
body.append('(if %s' % AND('_lowp', '(not (`self.bIsCrouched`))', v('CT_DuckOn')))
body.append('  (`self.Crouch`)')
body.append('  ' + S('CT_Duck', 'true') + ')')
body.append(S('CT_DuckT', sel('(+ %s _dt)' % v('CT_DuckT'), '0.0', v('CT_Duck'))))
body.append('(if %s' % AND(v('CT_Duck'), '(`self.bIsCrouched`)', '(not _bu0)', '(not _bu1)', '(not _bu2)', '(not _lowp)', '(> %s 0.45)' % v('CT_DuckT')))
body.append('  (`self.UnCrouch`)')
body.append('  ' + S('CT_Duck', 'false') + ')')
body.append('(if %s' % AND(v('CT_Duck'), '(not (`self.bIsCrouched`))', '(not _lowp)', '(> %s 0.45)' % v('CT_DuckT')))
body.append('  ' + S('CT_Duck', 'false') + ')')
# ---------- head-on impact ----------
body.append('(if _imp')
body.append('  ' + S('CT_HitDir', '_dir'))
for n, x in (('CT_LastS', '_sv'), ('CT_LastV', '_vimp'), ('CT_LastC', '_cls'), ('CT_LastL', '_lvl'), ('CT_Count', '(+ %s 1)' % v('CT_Count')), ('CT_Cool', '0.9'), ('CT_ObjN', '_obj'), ('CT_Sep', '0.0'), ('CT_Since', '0.0'),
             ('CT_Sup', F('SelectInt', '0', F('SelectInt', '1', '2', '(< _cl _cr)'), '_air')), ('CT_Kind', '1'), ('CT_Room', '_dbk')):
    body.append('  ' + S(n, x))
k = F('FClamp', '_sv', '0.0', '2.0')
body.append('  ' + S('PS_LPV', '(+ %s (* (* %s %s) %s))' % (v('PS_LPV'), k, v('CT_KickP'), F('Dot_VectorVector', '_dir', '(`self.GetActorForwardVector`)'))))
body.append('  ' + S('PS_LRV', '(+ %s (* (* %s %s) %s))' % (v('PS_LRV'), k, v('CT_KickR'), F('Dot_VectorVector', '_dir', '(`self.GetActorRightVector`)'))))
body.append('  (if (>= _lvl 1)')
body.append('    ' + S('CT_State', F('SelectInt', '4', '3', '(>= _lvl 2)')))
body.append('    ' + S('CT_T', '0.0'))
body.append('    ' + S('CT_Pend', F('SelectInt', '1', '0', '(== _lvl 3)')))
body.append('    ' + S('CT_RetN', '_n'))
body.append('    ' + S('CT_LockT', sel('30.0', sel('(+ 0.45 (* 0.3 _fat))', '0.16', '(== _lvl 2)'), '(== _lvl 3)')))
body.append('    ' + S('CT_CapT', sel('0.0', sel('1.2', '0.6', '(== _lvl 2)'), '(== _lvl 3)')))
body.append('    ' + setvel('(+ %s %s)' % (vs('_vtan', v('CT_TanKeep')), vs('_n', '(* _room %s)' % sel('0.0', sel('(+ 110.0 (* 50.0 _sv))', '(+ 40.0 (* 70.0 _sv))', '(== _lvl 2)'), '(== _lvl 3)')))) + ')')
body.append('  (if (>= _lvl 2)')
body.append('    ' + S('PS_DAL', '6.0'))
body.append('    ' + S('PS_DAR', '6.0') + '))')
# ---------- trip on an isolated low obstacle ----------
fall = AND('(== %s 3)' % v('CT_LastL'), '_flat', '(not _c2h)')   # latched values: pure nodes re-evaluate, and _trip turns false once CT_Cool is set
body.append('(if _trip')
body.append('  ' + S('CT_HitDir', '_dir'))
for n, x in (('CT_LastS', '_sv'), ('CT_LastV', '_vimp'), ('CT_LastC', '5'), ('CT_LastL', '_lvl'), ('CT_Count', '(+ %s 1)' % v('CT_Count')), ('CT_Cool', '1.2'), ('CT_Since', '0.0'), ('CT_Sep', '0.0'),
             ('CT_Sup', F('SelectInt', '0', F('SelectInt', '1', '2', '(< _cl _cr)'), '_air')), ('CT_Kind', '2'), ('CT_Room', sel('300.0', '0.0', '_flat'))):
    body.append('  ' + S(n, x))
body.append('  ' + S('CT_ObjN', ha('sh')))
body.append('  ' + S('PS_LPV', '(+ %s (* %s %s))' % (v('PS_LPV'), F('FClamp', v('CT_LastS'), '0.3', '2.0'), v('CT_TripKick'))))
body.append('  ' + S('CT_CapT', sel('1.0', '0.6', '(>= %s 2)' % v('CT_LastL'))))
body.append('  (if (>= %s 2)' % v('CT_LastL'))
body.append('    ' + S('PS_DAL', '6.0'))
body.append('    ' + S('PS_DAR', '6.0'))
body.append('    ' + S('CT_T', '0.0'))
body.append('    ' + S('CT_Pend', '0'))
body.append('    ' + S('CT_State', F('SelectInt', '8', '4', fall)))
body.append('    ' + S('CT_LockT', sel('30.0', '(+ 0.25 (* 0.3 _fat))', fall)))
body.append('    ' + S('CT_RetN', '_dir'))
body.append('    ' + S('CT_FallV', F('FClamp', '_sp', '300.0', '440.0')) + ')')
body.append('  (if %s' % fall)
body.append('    ' + play(FL + 'SphF_am_InjuredBelly_DropToFloor', '0.15', '0.05', v('CT_FallRate'), '1.9') + '))')
# ---------- stagger with pending kneel: retreat step first, kneel only with clearance ----------
body.append('(if %s' % AND('(== _st0 4)', '(== %s 1)' % v('CT_Pend'), '(< %s %s)' % (v('CT_T'), v('CT_RetT'))))
body.append('  ' + setvel(vs(v('CT_RetN'), '(* (* (/ (* 2.0 %s) %s) (- 1.0 (/ %s %s))) %s)' % (v('CT_RetD'), v('CT_RetT'), v('CT_T'), v('CT_RetT'), F('FClamp', '(/ (- %s 10.0) 45.0)' % v('CT_Room'), '0.0', '1.0')))) + ')')
body.append('(if %s' % AND('(== _st0 4)', '(== %s 1)' % v('CT_Pend'), '(>= %s %s)' % (v('CT_T'), v('CT_RetT')), OR('(>= _db %s)' % v('CT_KneelClr'), '(not _hitb)')))
body.append('  ' + play(KN + 'am_Stand_Trans_KneeB', '0.15', '0.2', '1.5', '0.45'))
body.append('  ' + S('CT_State', '5'))
body.append('  ' + S('CT_Pend', '0'))
body.append('  ' + S('CT_T', '0.0') + ')')
body.append('(if %s' % AND('(== _st0 4)', '(== %s 1)' % v('CT_Pend'), '(>= %s (+ %s 0.05))' % (v('CT_T'), v('CT_RetT'))))
body.append('  ' + S('CT_Pend', '2'))            # no room for the knee: stays a standing brace
body.append('  ' + S('CT_LockT', '(+ 0.55 (* 0.3 _fat))'))
body.append('  ' + S('CT_CapT', '1.4') + ')')
# ---------- kneel -> hold -> stand (hold can be cut by a move input after CT_CutMin) ----------
cut = AND('_hasin', '(> %s %s)' % (v('CT_T'), v('CT_CutMin')))
body.append('(if %s' % AND('(== _st0 5)', '(> %s 0.95)' % v('CT_T')))
body.append('  ' + play(KN + 'am_KneelB_Idle_01', '0.2', '0.2', '1.0', '0.0'))
body.append('  ' + S('CT_State', '6'))
body.append('  ' + S('CT_T', '0.0') + ')')
body.append('(if %s' % AND('(== _st0 6)', OR('(> %s (+ %s (* %s _fat)))' % (v('CT_T'), v('CT_DownHold'), v('CT_DownFat')), cut)))
body.append('  ' + play(KN + 'am_KneelB_Trans_Stand', '0.25', '0.3', '1.15', '0.0'))
body.append('  ' + S('CT_State', '7'))
body.append('  ' + S('CT_T', '0.0') + ')')
body.append('(if %s' % AND('(== _st0 7)', '(> %s 1.75)' % v('CT_T')))
body.append('  ' + S('CT_State', '0'))
body.append('  ' + S('CT_LockT', '0.0') + ')')
# ---------- forward fall -> lying -> get-up ----------
body.append('(if (== _st0 8)')
body.append('  ' + setvel(vs(v('CT_RetN'), '(* %s %s)' % (v('CT_FallV'), F('FClamp', '(- 1.0 (/ %s %s))' % (v('CT_T'), v('CT_FallTf')), '0.0', '1.0')))) + ')')
body.append('(if %s' % AND('(== _st0 8)', '(> %s %s)' % (v('CT_T'), v('CT_FallDur'))))
body.append('  ' + play(FL + 'SphF_am_InjuredBelly_DropToFloor_GetUp', '0.25', '0.25', '0.02', '0.3'))
body.append('  ' + S('CT_State', '9'))
body.append('  ' + S('CT_T', '0.0') + ')')
body.append('(if %s' % AND('(== _st0 9)', OR('(> %s (+ %s (* %s _fat)))' % (v('CT_T'), v('CT_LieHold'), v('CT_DownFat')), cut)))
body.append('  ' + play(FL + 'SphF_am_InjuredBelly_DropToFloor_GetUp', '0.15', '0.45', v('CT_UpRate'), '1.8'))
body.append('  ' + S('CT_State', '10'))
body.append('  ' + S('CT_T', '0.0') + ')')
body.append('(if %s' % AND('(== _st0 10)', '(> %s %s)' % (v('CT_T'), v('CT_UpDur'))))
body.append('  ' + S('CT_State', '0'))
body.append('  ' + S('CT_LockT', '0.0') + ')')
body.append('(if %s' % OR(AND('(== _st0 3)', '(> %s 0.5)' % v('CT_T')), AND('(== _st0 4)', '(!= %s 1)' % v('CT_Pend'), '(> %s 1.1)' % v('CT_T'))))
body.append('  ' + S('CT_State', '0') + ')')
# pressed against the surface with the stick into it
body.append('(if %s' % AND('_head', '(< _dw (+ %s 6.0))' % v('CT_StandOff'), '(< _sp 40.0)', '(> _cosi 0.7)', '(== _st0 0)'))
body.append('  ' + S('CT_LockT', F('FMax', v('CT_LockT'), '0.1')) + ')')
# outputs
capt = sel(sel('150.0', sel('250.0', '220.0', '(== %s 2)' % v('CT_Kind')), '(== %s 4)' % v('CT_State')), '100000.0', '(> %s 0.0)' % v('CT_CapT'))
capd = sel('0.0', '100000.0', AND('(>= %s 5)' % v('CT_State'), '(<= %s 7)' % v('CT_State')))
# round 6b: careful step over an isolated low obstacle below the trip speed (the toe went ~10 cm into a 25 cm log at 180 cm/s)
caps = sel(v('CT_StepV'), '100000.0', AND('_on', '_bsh', '(not _bk2)', '(not _hitb)', '(< _dsh 75.0)', '(<= _sp %s)' % v('CT_TripV')))
body.append(setmot('CtCap', sel(F('FMin', F('FMin', '_capa', F('FMin', '_capg', '_capz')), F('FMin', F('FMin', capt, capd), caps)), '100000.0', v('CT_On'))))
reach = AND('_head', OR('_bhi', '_bmid'), '(< _dw 55.0)', '(not _carry)', '(== %s 0)' % v('CT_State'))
brace = AND('(== %s 4)' % v('CT_State'), '(== %s 2)' % v('CT_Pend'), '_hitb', '(< _db 40.0)', '(not _carry)')
body.append('(bind _side %s)' % F('Dot_VectorVector', '(- _pt _loc)', '_rt'))
body.append(S('CT_ReachA', F('FInterpTo', v('CT_ReachA'), sel('0.85', sel(sel(F('MapRangeClamped', '_dw', '55.0', '25.0', '0.0', '1.0'), v('CT_GrazeReach'), reach), '0.0', AND('_on', '(not _carry)', OR(reach, '_gr'))), brace), '_dt', '7.0')))
ptw = '(+ (+ %s %s) %s)' % (mv('(.x _pt)', '(.y _pt)', '(+ (.z _loc) %s)' % sel('40.0', '8.0', '_bhi')), vs('_n', v('CT_HandOff')), vs('_rt', sel('14.0', '-14.0', '(>= _side 0.0)')))
ptg = selv('(+ (+ (+ %s %s) %s) %s)' % (hp('ll'), vs('_dir', '26.0'), mv('0.0', '0.0', '-22.0'), vs(hn('ll'), v('CT_HandOff'))), '(+ (+ (+ %s %s) %s) %s)' % (hp('lr'), vs('_dir', '26.0'), mv('0.0', '0.0', '-22.0'), vs(hn('lr'), v('CT_HandOff'))), '_grl')
body.append('(if %s' % OR(reach, brace))
body.append('  ' + S('CT_ReachPt', ptw))
body.append('  ' + S('CT_ReachN', '_n'))
body.append('  ' + S('CT_ReachF', UP))
body.append('  ' + S('CT_ReachR', '(>= _side 0.0)') + ')')
body.append('(if %s' % AND('_gr', '(not %s)' % OR(reach, brace)))
body.append('  ' + S('CT_ReachPt', ptg))
body.append('  ' + S('CT_ReachN', selv(hn('ll'), hn('lr'), '_grl')))
body.append('  ' + S('CT_ReachF', '_dir'))
body.append('  ' + S('CT_ReachR', '(not _grl)') + ')')
# round 6b PALM: hand rotation for the supporting hand (ABP_Sph_Body_GASP PalmR / PalmL, world space, c_palm6.py). Bone axes of the
# visible body (measured from recorded idle frames): right hand fingers = -X, palm = +Y ; left hand fingers = +X, palm = -Y.
# Palm faces into the surface (-normal); fingers along CT_ReachF projected into the surface plane (up on a wall, forward when grazing).
ABPB = '/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'
PN = F('Vector_Normal2D', v('CT_ReachN'), '0.0001'); PI_ = vs(PN, '-1.0')
FF = F('Normal', '(- %s %s)' % (v('CT_ReachF'), vs(PN, F('Dot_VectorVector', v('CT_ReachF'), PN))), '0.0001')
body.append('(bind _asb6 (cast `%s` (`SkeletalMeshComponent.GetAnimInstance` (`self.Manny`)))' % ABPB)
body.append('  (:`then`')
body.append('    (set `%s.PalmR` %s _asb6)' % (ABPB, F('MakeRotFromXY', vs(FF, '-1.0'), PI_)))
body.append('    (set `%s.PalmL` %s _asb6)' % (ABPB, F('MakeRotFromXY', FF, PN)))
body.append('    (set `%s.PalmAR` %s _asb6)' % (ABPB, sel('(* %s %s)' % (v('CT_ReachA'), v('CT_PalmK')), '0.0', v('CT_ReachR'))))
body.append('    (set `%s.PalmAL` %s _asb6)))' % (ABPB, sel('0.0', '(* %s %s)' % (v('CT_ReachA'), v('CT_PalmK')), v('CT_ReachR'))))
body.append(setmot('CtA', v('CT_ReachA')))
body.append(setmot('CtPt', v('CT_ReachPt')))
body.append(setmot('CtR', v('CT_ReachR')))
body.append(S('CT_VnPrev2', v('CT_VnPrev')))
body.append(S('CT_VnPrev', sel('_vn', '0.0', AND('_hitb', '(< _db 45.0)'))))
body.append(S('CT_PrevVel', '_vel'))
body.append(S('CT_DB', '_db'))
body.append(S('CT_Class', '_cls'))
body.append(S('CT_DBk', '_dbk'))
body.append(S('CT_DSh', sel('_dsh', '999.0', '_iso')))
body.append(S('CT_Flat', '_flat'))
ev = NL + NL + '(event `GR_Contact`' + NL + NL.join('  ' + x for x in L + body) + ')'
if DRY:
    print(ev); sys.exit(0)
PV = [(n, 'float') for n in ('CT_Since', 'CT_Sep', 'CT_SepMin', 'CT_TripV', 'CT_TanKeep', 'CT_TripKick', 'CT_RetD', 'CT_RetT', 'CT_KneelClr', 'CT_CutMin', 'CT_HandOff', 'CT_GrazeReach', 'CT_StandOff', 'CT_KneeSeeV', 'CT_SlopeLo', 'CT_SlopeHi', 'CT_StairV', 'CT_StairRunV', 'CT_Tuck', 'CT_DuckD', 'CT_DuckT', 'CT_StepV', 'CT_TripH', 'CT_FallRate', 'CT_FallV', 'CT_FallTf', 'CT_FallDur',
      'CT_LieHold', 'CT_UpRate', 'CT_UpDur', 'CT_HalfH', 'CT_Room', 'CT_DBk', 'CT_DSh')] + [(n, 'int') for n in ('CT_Pend', 'CT_Sup', 'CT_Kind')] + [('CT_Flat', 'bool'), ('CT_Duck', 'bool'), ('CT_DuckOn', 'bool'), ('CT_RetN', 'vector'), ('CT_HitDir', 'vector'), ('CT_ReachF', 'vector'), ('CT_PalmK', 'float'), ('CT_ReachN', 'vector'), ('CT_ObjN', 'string')]
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n, ty in PV:
    if '"%s"' % n in have: continue
    r = T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': ty})
    if isinstance(r, dict) and r.get('isError'): out['var_' + n] = str(r)[:200]
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'GR_Load2H', 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'GR_CarryActive', 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
assert '(event `GR_Contact`' in dsl
if not os.path.exists('Saved/UE59Work/dsl/player_before_contact6.dsl'): open('Saved/UE59Work/dsl/player_before_contact6.dsl', 'w', encoding='utf8').write(dsl)
i0 = dsl.index('(event `GR_Contact`'); c = [x for x in (dsl.find(NL + NL + '(event', i0), dsl.find(NL + NL + '(fn', i0)) if x > 0]
old = dsl[i0:min(c)] if c else dsl[i0:]
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old.rstrip(NL), 'newString': ev.strip()}]})
out['edit'] = str(r2)[:3000] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300]
print('CONTACT6', json.dumps(out)[:4500])
