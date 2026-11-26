# m_fall4_mcp.py (MCP, in-memory; BP_HybridA_Player; re-appliable) - ACTIVE ragdoll fall shaped by the body's state.
# v1 (m_fall_mcp) let the body go almost limp with world-space motors -> it toppled like a stiff mannequin. Now:
# - motors are joint-space (bIsLocalSimulation) so gravity still takes the body while the muscles drive toward a TARGET POSE played in
#   the driver's DefaultSlot: a protective reach in the fall direction (GASP M_ragdoll_reach_forward/back/left/right: arms out, head up,
#   knees soften) during the topple, then the on-ground pose (M_ragdoll_poses_OnGround frame 0: arms by the head, knees bent) with weaker
#   tone once down (FL_GndT s);
# - physical state: muscle strength FL_Str = clamp(1 - FL_FatK * fatigue, 0.35, 1); the fall carries the current body velocity
#   (FL_VelK); severity FL_Sev = |impulse| / FL_SevV sets how long she stays down (FL_Daze = FL_DazeK * severity * (1 + fatigue));
#   the get-up plays slower when tired (rate 1.12 - 0.35 fatigue, clamped 0.75..1.12);
# - strong whole-region impacts (IMP_All with |IMP_Imp| >= FL_ImpMin) become falls instead of a stagger; the impact layer is idle
#   while a fall runs.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); BQ = chr(96)
def K(f): return BQ + 'KismetMathLibrary.' + f + BQ
def S(v): return '(' + BQ + 'self.' + v + BQ + ')'
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for nme in ('FL_Str', 'FL_FatK', 'FL_VelK', 'FL_Sev', 'FL_SevV', 'FL_Daze', 'FL_DazeK', 'FL_Ph', 'FL_GndT', 'FL_GndK', 'FL_DF', 'FL_DR', 'FL_Rate', 'FL_ImpMin', 'FL_ImpK'):
    if '"%s"' % nme not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': nme, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': nme, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if 'FL_GndT' in dsl: print('FALL4 already'); sys.exit()
L = dsl.split(NL)
def one(pred, what):
    a = [i for i, x in enumerate(L) if pred(x)]; assert len(a) == 1, (what, a); return a[0]
M = S('Mesh'); AI = '(`SkeletalMeshComponent.GetAnimInstance` %s)' % M
FAT = '(`/Game/Sphirus/Player/Motion/AC_Sph_Motion.Fat` (`self.SphMotion`))'
R = '/Game/Characters/UEFN_Mannequin/Animations/Ragdoll/'
def clip(n): return '"%s%s.%s"' % (R, n, n)
def play(c, bi, rate, ind): return ind + '(`AnimInstance.PlaySlotAnimationAsDynamicMontage` %s %s "DefaultSlot" %s 0.2 %s 1 -1.0 0.0)' % (AI, c, bi, rate)
def pad(k): return '(make `PhysicalAnimationData` true (* (* %s %s) %s) (* (* %s %s) %s))' % (S('FL_OS'), S('FL_Str'), k, S('FL_AVS'), S('FL_Str'), k)
edits = []
# E1: fire block - state, velocity, severity, direction, protective target pose, joint-space motors
i = one(lambda x: 'ApplyPhysicalAnimationSettingsBelow' in x and 'FL_OS' in x, 'E1'); ind = L[i][:len(L[i]) - len(L[i].lstrip())]
hv = '(%s (%s (.x %s) (.y %s) 0.0))' % (K('Normal'), K('MakeVector'), S('FL_Imp'), S('FL_Imp'))
pre = [ind + '(set `self.FL_Str` (%s (- 1.0 (* %s %s)) 0.35 1.0))' % (K('FClamp'), S('FL_FatK'), FAT),
       ind + '(set `self.FL_Imp` (+ %s (* (`self.GetVelocity`) %s)))' % (S('FL_Imp'), S('FL_VelK')),
       ind + '(set `self.FL_Sev` (%s (/ (%s %s) %s) 0.3 2.0))' % (K('FClamp'), K('VSize'), S('FL_Imp'), S('FL_SevV')),
       ind + '(set `self.FL_Daze` (* (* %s %s) (+ 1.0 %s)))' % (S('FL_DazeK'), S('FL_Sev'), FAT),
       ind + '(set `self.FL_DF` (%s %s (`Actor.GetActorForwardVector` self)))' % (K('Dot_VectorVector'), hv),
       ind + '(set `self.FL_DR` (%s %s (`Actor.GetActorRightVector` self)))' % (K('Dot_VectorVector'), hv),
       ind + '(set `self.FL_Ph` 0.0)',
       ind + '(set `self.IMP_Act` 0.0)',
       ind + '(if (>= (%s %s) (%s %s))' % (K('Abs'), S('FL_DF'), K('Abs'), S('FL_DR')),
       ind + '  (if (> %s 0.0)' % S('FL_DF'),
       play(clip('M_ragdoll_reach_forward'), '0.12', '1.0', ind + '    '),
       ind + '    (else',
       play(clip('M_ragdoll_reach_back'), '0.12', '1.0', ind + '      ') + '))',
       ind + '  (else',
       ind + '    (if (> %s 0.0)' % S('FL_DR'),
       play(clip('M_ragdoll_reach_right'), '0.12', '1.0', ind + '      '),
       ind + '      (else',
       play(clip('M_ragdoll_reach_left'), '0.12', '1.0', ind + '        ') + '))))']
edits.append({'oldString': L[i], 'newString': NL.join(pre) + NL + ind + '(`PhysicalAnimationComponent.ApplyPhysicalAnimationSettingsBelow` (`self.SphPhysAnim`) "pelvis" %s true)' % pad('1.0')})
# E2: ground phase after the topple
i = one(lambda x: x.lstrip().startswith('(set `self.FL_Still` (`KismetMathLibrary.SelectFloat`'), 'E2'); ind = L[i][:len(L[i]) - len(L[i].lstrip())]
gnd = [ind + '(if (and (< %s 0.5) (> %s %s))' % (S('FL_Ph'), S('FL_T'), S('FL_GndT')),
       play(clip('M_ragdoll_poses_OnGround'), '0.35', '0.001', ind + '  '),
       ind + '  (`PhysicalAnimationComponent.ApplyPhysicalAnimationSettingsBelow` (`self.SphPhysAnim`) "pelvis" %s true)' % pad(S('FL_GndK')),
       ind + '  (set `self.FL_Ph` 1.0))']
edits.append({'oldString': L[i], 'newString': L[i] + NL + NL.join(gnd)})
# E3: stay down at least FL_Daze
old = '(or (> (`self.FL_Still`) 0.35) (> (`self.FL_T`) (`self.FL_TMax`)))'
i = one(lambda x: old in x, 'E3'); edits.append({'oldString': L[i], 'newString': L[i].replace(old, '(or (and (> (`self.FL_Still`) 0.35) (> (`self.FL_T`) (`self.FL_Daze`))) (> (`self.FL_T`) (`self.FL_TMax`)))')})
# E4: get-up rate by fatigue, end time scaled
i = one(lambda x: 'PlaySlotAnimationAsDynamicMontage' in x and 'DropToFloor_GetUp' in x, 'E4'); ind = L[i][:len(L[i]) - len(L[i].lstrip())]
edits.append({'oldString': L[i], 'newString': ind + '(set `self.FL_Rate` (%s (- 1.12 (* 0.35 %s)) 0.75 1.12))' % (K('FClamp'), FAT) + NL + L[i].replace('"DefaultSlot" 0.0 0.5 1.0 1', '"DefaultSlot" 0.0 0.5 %s 1' % S('FL_Rate'))})
i = one(lambda x: '(>= (`self.FL_T`) (`self.FL_Len`))' in x, 'E4b'); edits.append({'oldString': L[i], 'newString': L[i].replace('(>= (`self.FL_T`) (`self.FL_Len`))', '(>= (`self.FL_T`) (/ (`self.FL_Len`) (`self.FL_Rate`)))')})
# E5: strong whole-region impacts -> fall; impact layer idle during a fall
i = one(lambda x: x.startswith('  (if (> (`self.IMP_Fire`) 0.5)'), 'E5')
conv = ['  (if (and (and (> %s 0.5) (> %s 0.5)) (>= (%s %s) %s))' % (S('IMP_Fire'), S('IMP_All'), K('VSize'), S('IMP_Imp'), S('FL_ImpMin')),
        '    (set `self.FL_Imp` (* %s %s))' % (S('IMP_Imp'), S('FL_ImpK')),
        '    (set `self.FL_Fire` 1.0)',
        '    (set `self.IMP_Fire` 0.0))']
edits.append({'oldString': L[i], 'newString': NL.join(conv) + NL + '  (if (and (> (`self.IMP_Fire`) 0.5) (< (`self.FL_State`) 0.5))'})
i = one(lambda x: x.startswith('  (if (> (`self.IMP_Act`) 0.5)'), 'E5b'); edits.append({'oldString': L[i], 'newString': '  (if (and (> (`self.IMP_Act`) 0.5) (< (`self.FL_State`) 0.5))'})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('FALL4', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:3000])
print('FALL4 compile', str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:400])
