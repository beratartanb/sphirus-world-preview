# mk_contact7.py: builds m_contact7_mcp.py / c_contact7_defaults.py from the round-6 contact script by explicit, asserted text edits.
import io
s = io.open('Tools/UE59_20261123/m_contact6_mcp.py', encoding='utf8').read()
s = s.replace('# m_contact6_mcp.py (MCP,', '# m_contact7_mcp.py = m_contact6 + round 7: VISIBLE STAGGER with root-motion reaction clips chosen by contact side / support foot,\n'
              '# predictive impact before the swing foot enters a knee-high obstacle, forward fall with protective hands (prone clip), fall travel that\n'
              '# carries the feet past the obstacle, get-up only with head room. Earlier header follows.\n# m_contact6_mcp.py (MCP,', 1)
RB = '/Game/Sphirus/Player/Anim/React/SphR_am_Stand_ReactBumpLight_'
ST = '/Game/Characters/UEFN_Mannequin/Animations/Jump/M_Neutral_Jump_F_Land_Stumble_'
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90]); s = s.replace(a, b)
# 1) head-on stagger (lvl 2): side-dependent root-motion reaction clip instead of a scripted rebound velocity
a = "body.append('    ' + setvel('(+ %s %s)' % (vs('_vtan', v('CT_TanKeep')), vs('_n', '(* _room %s)' % sel('0.0', sel('(+ 110.0 (* 50.0 _sv))', '(+ 40.0 (* 70.0 _sv))', '(== _lvl 2)'), '(== _lvl 3)')))) + ')')"
b = "\n".join([
    "body.append('    (if (!= _lvl 2)')",
    "body.append('      ' + setvel('(+ %s %s)' % (vs('_vtan', v('CT_TanKeep')), vs('_n', '(* _room %s)' % sel('0.0', '(+ 40.0 (* 70.0 _sv))', '(== _lvl 3)')))) + ')')",
    "body.append('    (if (== _lvl 2)')",
    "body.append('      ' + S('CT_HSide', F('Dot_VectorVector', vs('_n', '-1.0'), '(`self.GetActorRightVector`)')))",
    "body.append('      ' + S('CT_RClip', F('SelectInt', '2', F('SelectInt', '1', '0', '(< %s -0.35)' % v('CT_HSide')), '(> %s 0.35)' % v('CT_HSide'))))",
    "body.append('      ' + S('CT_RRate', F('FClamp', '(+ 0.9 (* 0.25 _sv))', '0.9', '1.35')))",
    "body.append('      ' + S('CT_LockT', '(/ %s %s)' % (v('CT_RLock'), v('CT_RRate'))))",
    "body.append('      (if (== %s 0)' % v('CT_RClip'))",
    "body.append('        ' + play(RB + 'Front', '0.12', '0.4', v('CT_RRate'), '0.0') + ')')",
    "body.append('      (if (== %s 1)' % v('CT_RClip'))",
    "body.append('        ' + play(RB + 'FrontLeft', '0.12', '0.4', v('CT_RRate'), '0.0') + ')')",
    "body.append('      (if (== %s 2)' % v('CT_RClip'))",
    "body.append('        ' + play(RB + 'FrontRight', '0.12', '0.4', v('CT_RRate'), '0.0') + ')))')"])
rep(a, b)
# 2) trip lvl 2: forward stumble starting on the support foot (root motion); lvl 3: prone fall with the hands reaching for the floor
a = "body.append('    ' + S('CT_State', F('SelectInt', '8', '4', fall)))\nbody.append('    ' + S('CT_LockT', sel('30.0', '(+ 0.25 (* 0.3 _fat))', fall)))"
b = a + "\n" + "\n".join([
    "body.append('    (if (not %s)' % fall)",
    "body.append('      ' + S('CT_RRate', F('FClamp', '(/ _sp 340.0)', '0.9', '1.4')))",
    "body.append('      ' + S('CT_LockT', '(/ %s %s)' % (v('CT_SLock'), v('CT_RRate'))))",
    "# round 8: airborne at the trip (CT_Sup 0) no longer defaults to the right-foot variant: the lower foot (the one that lands next) decides",
    "body.append('      ' + S('CT_RClip', F('SelectInt', '4', '3', OR('(== %s 1)' % v('CT_Sup'), AND('(== %s 0)' % v('CT_Sup'), '(< (.z (`SceneComponent.GetSocketLocation` (`self.Mesh`) \"foot_l\")) (.z (`SceneComponent.GetSocketLocation` (`self.Mesh`) \"foot_r\")))')))))",
    "body.append('      (if (== %s 4)' % v('CT_RClip'))",
    "body.append('        ' + play(ST + 'Lfoot', '0.1', '0.4', v('CT_RRate'), v('CT_SStart')) + ')')",
    "body.append('      (if (== %s 3)' % v('CT_RClip'))",
    "body.append('        ' + play(ST + 'Rfoot', '0.1', '0.4', v('CT_RRate'), v('CT_SStart')) + '))')"])
rep(a, b)
rep("play(FL + 'SphF_am_InjuredBelly_DropToFloor', '0.15', '0.05', v('CT_FallRate'), '1.9')", "play(FL + 'SphF_am_Stand_Trans_ProneCrawl', '0.12', '0.05', v('CT_FallRate'), v('CT_FallStart'))")
rep("play(FL + 'SphF_am_InjuredBelly_DropToFloor_GetUp', '0.25', '0.25', '0.02', '0.3')", "play(FL + 'SphF_am_ProneCrawl_Trans_Stand', '0.25', '0.25', '0.02', '0.0')")
rep("play(FL + 'SphF_am_InjuredBelly_DropToFloor_GetUp', '0.15', '0.45', v('CT_UpRate'), '1.8')", "play(FL + 'SphF_am_ProneCrawl_Trans_Stand', '0.15', '0.45', v('CT_UpRate'), '0.0')")
# 3) fall travel by distance (feet end past the obstacle)
rep("setvel(vs(v('CT_RetN'), '(* %s %s)' % (v('CT_FallV'), F('FClamp', '(- 1.0 (/ %s %s))' % (v('CT_T'), v('CT_FallTf')), '0.0', '1.0'))))",
    "setvel(vs(v('CT_RetN'), '(* %s %s)' % (v('CT_FallV'), F('FClamp', '(- 1.0 (/ %s (/ (* 2.0 %s) %s)))' % (v('CT_T'), v('CT_FallDist'), v('CT_FallV')), '0.0', '1.0'))))")
# 4) get up only with head room
rep("body.append('(if %s' % AND('(== _st0 9)', OR('(> %s (+ %s (* %s _fat)))' % (v('CT_T'), v('CT_LieHold'), v('CT_DownFat')), cut)))",
    "body.append('(if %s' % AND('(== _st0 9)', OR('(> %s (+ %s (* %s _fat)))' % (v('CT_T'), v('CT_LieHold'), v('CT_DownFat')), cut), '(not _bu0)', '(not _bu1)', '(not _bu2)'))")
# 5) stagger end: after the lock, a move input stops the reaction montage (control comes back in a safe phase)
a = "body.append('(if %s' % OR(AND('(== _st0 3)', '(> %s 0.5)' % v('CT_T')), AND('(== _st0 4)', '(!= %s 1)' % v('CT_Pend'), '(> %s 1.1)' % v('CT_T'))))"
b = ("body.append('(if %s' % AND('(== _st0 4)', '(!= %s 1)' % v('CT_Pend'), '(<= %s 0.0)' % v('CT_LockT'), '_hasin', '(`AnimInstance.IsAnyMontagePlaying` _ai)'))\n"
     "body.append('  (`AnimInstance.StopSlotAnimation` _ai 0.3 \"DefaultSlot\"))')\n"
     + a.replace("'(> %s 1.1)' % v('CT_T')", "'(> %s %s)' % (v('CT_T'), v('CT_StagEnd'))"))
rep(a, b)
# 6) predictive impact
rep("L.append('(bind _imp %s)' % AND('_on', '(== _st0 0)', '(<= %s 0.0)' % v('CT_Cool'), '(< _db 10.0)', OR(hitA, hitB), '(not %s)' % same))",
    "L.append('(bind _pred %s)' % AND('_hitb', '(< _db (+ %s (* _sp %s)))' % (v('CT_PreD0'), v('CT_PreDK')), '(> _vn %s)' % v('CT_VMin'), '(> _cosi 0.75)', '(not _head)'))\n"
    "L.append('(bind _imp %s)' % AND('_on', '(== _st0 0)', '(<= %s 0.0)' % v('CT_Cool'), OR(AND('(< _db 10.0)', OR(hitA, hitB)), '_pred'), '(not %s)' % same))")
rep("L.append('(bind _vimp %s)' % sel('_sp', F('FMax', v('CT_VnPrev'), v('CT_VnPrev2')), '_trip'))",
    "L.append('(bind _vimp %s)' % sel('_sp', F('FMax', F('FMax', v('CT_VnPrev'), v('CT_VnPrev2')), sel('_vn', '0.0', '_pred')), '_trip'))")
rep("'CT_KneeSeeV',", "'CT_KneeSeeV', 'CT_RRate', 'CT_RLock', 'CT_SLock', 'CT_SStart', 'CT_FallStart', 'CT_FallDist', 'CT_StagEnd', 'CT_PreD0', 'CT_PreDK', 'CT_HSide',")
rep("[(n, 'int') for n in ('CT_Pend', 'CT_Sup', 'CT_Kind')]", "[(n, 'int') for n in ('CT_Pend', 'CT_Sup', 'CT_Kind', 'CT_RClip')]")
rep("KN = '/Game/MC_Core_Motion/Animations/Kneel/'", "KN = '/Game/MC_Core_Motion/Animations/Kneel/'\nRB = '%s'\nST = '%s'" % (RB, ST))
# 7) round 7d: a knee-high obstacle is stood off further than a wall (CT_KneeExtra): the feet, not the chest, are the forward-most part of a
#    walking body; with the wall stand-off the swing foot of the last stride (load carry, walk) ended 9 cm inside the obstacle face.
rep("L.append('(bind _dw %s)' % F('FMin', F('FMin', '_dhi', '_dmid'), sel('_dkn', '999.0', '_kslow')))",
    "L.append('(bind _dw %s)' % F('FMin', F('FMin', '_dhi', '_dmid'), sel('_dkn', '999.0', '_kslow')))\n"
    "L.append('(bind _so (+ %s %s))' % (v('CT_StandOff'), sel(v('CT_KneeExtra'), '0.0', AND('_kslow', '(<= _dkn %s)' % F('FMin', '_dhi', '_dmid')))))")
rep("F('FMax', '(- _dw %s)' % v('CT_StandOff'), '0.0')", "F('FMax', '(- _dw _so)', '0.0')")
rep("'(< _dw (+ %s 6.0))' % v('CT_StandOff')", "'(< _dw (+ _so 6.0))'")
rep("'CT_StandOff', 'CT_KneeSeeV',", "'CT_StandOff', 'CT_KneeExtra', 'CT_KneeSeeV',")
# 8) round 7d: ONE-HAND CARRY. A prop held in one hand (GR_HoldProp -> GR_Prop on hand_r, GR_HoldPropL -> GR_PropL on hand_l) no longer
#    disables the hands: only a two-hand load (or both hands busy) does. A head-on reach / brace uses the free hand when the near-side hand
#    is busy; a side-wall graze reaches only with a free wall-side hand.
rep("L.append('(bind _carry %s)' % OR(v('GR_CarryActive'), '_c2h'))",
    "L.append('(bind _carry %s)' % OR(v('GR_CarryActive'), '_c2h'))\n"
    "L.append('(bind _b1r (`SceneComponent.IsVisible` (`self.GR_Prop`)))')\n"
    "L.append('(bind _b1l (`SceneComponent.IsVisible` (`self.GR_PropL`)))')\n"
    "L.append('(bind _nofree %s)' % OR('_c2h', AND('_b1r', '_b1l')))")
rep("'(< _dw 55.0)', '(not _carry)',", "'(< _dw 55.0)', '(not _nofree)',")
rep("'(< _db 40.0)', '(not _carry)')", "'(< _db 40.0)', '(not _nofree)')")
rep("body.append('(bind _side %s)' % F('Dot_VectorVector', '(- _pt _loc)', '_rt'))",
    "body.append('(bind _side %s)' % F('Dot_VectorVector', '(- _pt _loc)', '_rt'))\n"
    "body.append('(bind _rr %s)' % OR(AND('(>= _side 0.0)', '(not _b1r)'), '_b1l'))\n"
    "body.append('(bind _grok %s)' % OR(AND('_grl', '(not _b1l)'), AND('_grr', '(not _b1r)')))")
rep("AND('_on', '(not _carry)', OR(reach, '_gr'))", "AND('_on', '(not _nofree)', OR(reach, '_grok'))")
rep("vs('_rt', sel('14.0', '-14.0', '(>= _side 0.0)')))", "vs('_rt', sel('14.0', '-14.0', '_rr')))")
rep("body.append('  ' + S('CT_ReachR', '(>= _side 0.0)') + ')')", "body.append('  ' + S('CT_ReachR', '_rr') + ')')")
rep("body.append('(if %s' % AND('_gr', '(not %s)' % OR(reach, brace)))", "body.append('(if %s' % AND('_grok', '(not %s)' % OR(reach, brace)))")
#    a busy wall-side arm (prop in that hand, it cannot reach) is tucked CT_TuckBusy further: the prop hand swung 5.8 cm into the side wall.
#    CT_TuckNow (the current tuck target) is what the posture layer's arm floor follows.
rep("L.append(S('PS_DAL', sel(F('FInterpTo', v('PS_DAL'), v('CT_Tuck'), '_dt', '12.0'), v('PS_DAL'), '_grl')))\n"
    "L.append(S('PS_DAR', sel(F('FInterpTo', v('PS_DAR'), v('CT_Tuck'), '_dt', '12.0'), v('PS_DAR'), '_grr')))",
    "L.append(S('CT_TuckNow', sel('(+ %s %s)' % (v('CT_Tuck'), v('CT_TuckBusy')), v('CT_Tuck'), OR(AND('_grl', '_b1l'), AND('_grr', '_b1r')))))\n"
    "L.append(S('PS_DAL', sel(F('FInterpTo', v('PS_DAL'), v('CT_TuckNow'), '_dt', '12.0'), v('PS_DAL'), '_grl')))\n"
    "L.append(S('PS_DAR', sel(F('FInterpTo', v('PS_DAR'), v('CT_TuckNow'), '_dt', '12.0'), v('PS_DAR'), '_grr')))")
#    head-on reach starts earlier (70 cm, full at 35) and ramps faster: during the ramp the IK blended the walk-swing hand (already past
#    the wall face) with the target and the hand crossed the face for 5 frames (6.2 cm).
rep("F('MapRangeClamped', '_dw', '55.0', '25.0', '0.0', '1.0')", "F('MapRangeClamped', '_dw', '70.0', '35.0', '0.0', '1.0')")
rep("'(< _dw 55.0)', '(not _nofree)',", "'(< _dw 70.0)', '(not _nofree)',")
rep("OR(reach, '_grok'))), brace), '_dt', '7.0')))", "OR(reach, '_grok'))), brace), '_dt', '10.0')))")
rep("'CT_StandOff', 'CT_KneeExtra',", "'CT_StandOff', 'CT_KneeExtra', 'CT_TuckNow', 'CT_TuckBusy', 'CT_BwdV', 'CT_BwdK',")
# 9) round 7d: FALSE DUCK at a full-height wall. The head probe is 20 cm longer than the chest probe, so a wall entered the head probe
#    first and read as a head-height-only obstacle (low passage) -> auto-crouch, knees into the wall (corridor end wall, walk). The low
#    passage now also needs a chest-height probe of the head probe's length to be free.
rep("tr('hd', '(- 168.0 _hh)', ln='(+ _len 20.0)')", "tr('hd', '(- 168.0 _hh)', ln='(+ _len 20.0)'); tr('hx', '52.0', ln='(+ _len 20.0)')")
rep("AND('_on', '_bhd', '(not _bhi)',", "AND('_on', '_bhd', '(not _bhx)', '(not _bhi)',")
# 10) round 7d: BACKWARD TRAVEL INTO AN OBSTACLE. Nobody sees what is behind them: moving backwards (velocity against the facing) the
#     head-on anticipation (stand-off brake, reaching hand) is off above CT_BwdV (a slow careful back-step keeps it), so the body bumps. A head-on hit from behind (hit normal along the
#     facing) plays the ReactBumpLight Back / BackLeft / BackRight clips (forward recovery steps away from the obstacle).
rep("L.append('(bind _head %s)' % AND('_on', OR('_bhi', '_bmid', '_kslow'),",
    "L.append('(bind _bwd (and (> %s %s) (< %s -0.5)))' % (v('CT_SpRef'), v('CT_BwdV'), F('Dot_VectorVector', F('Vector_Normal2D', v('CT_PrevVel'), '0.0001'), '(`self.GetActorForwardVector`)')))\n"
    "L.append('(bind _head %s)' % AND('_on', '(not _bwd)', OR('_bhi', '_bmid', '_kslow'),")
rep("body.append('      ' + S('CT_RClip', F('SelectInt', '2', F('SelectInt', '1', '0', '(< %s -0.35)' % v('CT_HSide')), '(> %s 0.35)' % v('CT_HSide'))))",
    "body.append('      ' + S('CT_RClip', F('SelectInt', '2', F('SelectInt', '1', '0', '(< %s -0.35)' % v('CT_HSide')), '(> %s 0.35)' % v('CT_HSide'))))\n"
    "body.append('      ' + S('CT_RClip', F('SelectInt', F('SelectInt', '7', F('SelectInt', '6', '5', '(< %s -0.35)' % v('CT_HSide')), '(> %s 0.35)' % v('CT_HSide')), v('CT_RClip'), '(> %s 0.35)' % F('Dot_VectorVector', '_n', '(`self.GetActorForwardVector`)'))))")
rep("body.append('        ' + play(RB + 'FrontRight', '0.12', '0.4', v('CT_RRate'), '0.0') + ')))')",
    "body.append('        ' + play(RB + 'FrontRight', '0.12', '0.4', v('CT_RRate'), '0.0') + ')')\n"
    "body.append('      (if (== %s 5)' % v('CT_RClip'))\n"
    "body.append('        ' + play(RB + 'Back', '0.12', '0.4', v('CT_RRate'), '0.0') + ')')\n"
    "body.append('      (if (== %s 6)' % v('CT_RClip'))\n"
    "body.append('        ' + play(RB + 'BackLeft', '0.12', '0.4', v('CT_RRate'), '0.0') + ')')\n"
    "body.append('      (if (== %s 7)' % v('CT_RClip'))\n"
    "body.append('        ' + play(RB + 'BackRight', '0.12', '0.4', v('CT_RRate'), '0.0') + ')))')")
#     an unseen hit from behind (no anticipation, no bracing arms) is CT_BwdK times more severe; CT_SpRef / CT_PrevVel = pre-impact speed and
#     direction (the velocity of the impact frame is already the post-collision one).
rep("L.append('(bind _sv (* ", "L.append('(bind _sv0 (* ")
_i = s.index("L.append('(bind _sv0 (* "); _j = s.index(chr(10), _i)
s = s[:_j + 1] + "L.append('(bind _sv (* _sv0 %s))' % sel(v('CT_BwdK'), '1.0', '_bwd'))" + chr(10) + s[_j + 1:]
# 11) round 8: STUMBLE SPEED. Land_Stumble re-accelerates to a 500 cm/s run by itself (root 300 cm/s at 1.02 s -> 500 at 2.0 s) and was
#     played at entry/340 (1.22 at run): the capsule went 415 -> 635 cm/s during the stagger. The play rate is now steered every tick so the
#     clip's own root speed tracks CT_StumK x entry speed (rate 0.7..1.3): a stumble loses speed, it does not gain it.
rep("# pressed against the surface with the stick into it",
    "body.append('(if %s' % AND('(== _st0 4)', '(>= %s 3)' % v('CT_RClip'), '(<= %s 4)' % v('CT_RClip'), '(`AnimInstance.IsAnyMontagePlaying` _ai)'))\n"
    "body.append('  (`AnimInstance.Montage_SetPlayRate` _ai (`AnimInstance.GetCurrentActiveMontage` _ai) %s))' % F('FClamp', '(/ (* %s %s) %s)' % (v('CT_StumK'), v('CT_LastV'), F('FClamp', '(+ 300.0 (* 205.0 (- (`AnimInstance.Montage_GetPosition` _ai (`AnimInstance.GetCurrentActiveMontage` _ai)) 1.02)))', '300.0', '500.0')), '0.7', '1.3'))\n"
    "# pressed against the surface with the stick into it")
rep("'CT_BwdV', 'CT_BwdK',", "'CT_BwdV', 'CT_BwdK', 'CT_StumK',")
io.open('Tools/UE59_20261124/m_contact7_mcp.py', 'w', encoding='utf8').write(s)
d = io.open('Tools/UE59_20261123/c_contact6_defaults.py', encoding='utf8').read()
a = "'CT_KneeSeeV':230.0,"; assert a in d
d = d.replace(a, a + "'CT_RLock':1.1,'CT_SLock':0.9,'CT_SStart':1.02,'CT_FallStart':0.0,'CT_FallDist':185.0,'CT_StagEnd':2.2,'CT_PreD0':6.0,'CT_PreDK':0.025,'CT_KneeExtra':28.0,'CT_TuckBusy':0.0,'CT_BwdV':200.0,'CT_BwdK':1.7,'CT_StumK':0.85,")
d = d.replace("'CT_FallRate':2.2", "'CT_FallRate':1.5").replace("'CT_UpRate':2.0", "'CT_UpRate':1.3").replace('c_contact6_defaults', 'c_contact7_defaults')
io.open('Tools/UE59_20261124/c_contact7_defaults.py', 'w', encoding='utf8').write(d)
print('MK7 ok')
