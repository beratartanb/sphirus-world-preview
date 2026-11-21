# m_dm_mcp.py (MCP, in-memory edit of AC_Sph_Motion) - 2026-11-22 round 5.
# CLIP-BOUND BRAKE WHILE THE INPUT IS HELD ("Dm"). When a held input lowers the max speed (run forward -> back diagonal 135 deg: 415 ->
# ~200; turn speed loss; gait change) the movement component brakes the capsule along its velocity with a fixed 500 cm/s2 (+friction,
# measured ~870) and does not turn it until the speed is under the cap. That brake is timed from the key press. The diamond / turn clip
# is entered by Motion Matching at the current foot phase, so its plant can come 0.15 s before the capsule has finished braking
# (T plan s6: R foot planted at capsule 228 cm/s heading 20 deg, clip already at its minimum -> foot lock broke at 20 cm, 22 cm slide).
# Now, while the capsule is over its max speed with the input held, the braking deceleration follows the driver clip's own speed curve
# (same construction as the clip-bound stop):   DmDecel = clamp((v - DmK * (2c - cPrev)) / dt, 500, DmMax)
#   c = movedata_speed of the driver pose, DmK = v / c latched over the first 0.12 s of the episode (0.5..1.8).
# A clip that does not slow down (loop) leaves the old 500 cm/s2. Output through RevDecel (CalculateBrakingDeceleration: FMax(500, RevDecel)).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; BP = AP + '.AC_Sph_Motion'; out = {}; NL = chr(10)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n, ty in [(n, 'float') for n in ('DmT', 'DmK', 'DmVin', 'DmDecel', 'DmMax', 'DmPrevC', 'DmMargin')] + [('DmOn', 'bool')]:
    if '"%s"' % n in have: continue
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': ty})
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
open('Saved/UE59Work/dsl/AC_Sph_Motion_before_dm.dsl', 'w', encoding='utf8').write(dsl)
assert '`self.DmDecel`' not in dsl, 'already built'
def line(prefix):
    L = [l for l in dsl.split(NL) if l.strip().startswith(prefix)]; assert len(L) == 1, (prefix, len(L)); return L[0]
M = '`KismetMathLibrary.%s`'
def v(n): return '(`self.%s`)' % n
rd = line('(set `self.RevDecel`'); ind = rd[:len(rd) - len(rd.lstrip())]
SPD = '(%s (`Actor.GetVelocity` _ascharacter))' % (M % 'VSizeXY')
C = '(`AnimInstance.GetCurveValue` (`SkeletalMeshComponent.GetAnimInstance` (`Character.Mesh` _ascharacter)) "movedata_speed")'
MAXW = '(`CharacterMovementComponent.MaxWalkSpeed` (`Character.CharacterMovement` _ascharacter))'
HASIN = '(> (%s (`Pawn.GetLastMovementInputVector` _ascharacter)) 0.1)' % (M % 'VSizeXY')
OVER = '(and (and %s (`self.DmOn`)) (and (> %s (+ %s %s)) (<= %s 0.01)))' % (HASIN, SPD, MAXW, v('DmMargin'), v('RcW'))
SF = M % 'SelectFloat'
pre = [
    '(set `self.DmVin` (%s %s %s (<= %s 0.0)))' % (SF, SPD, v('DmVin'), v('DmT')),
    '(set `self.DmK` (%s (%s (%s (%s 1.8 %s (<= %s 0.0)) (/ %s (%s %s 50.0))) 0.5 1.8) %s (and %s (< %s 0.12))))' % (
        SF, M % 'FClamp', M % 'FMin', SF, v('DmK'), v('DmT'), v('DmVin'), M % 'FMax', C, v('DmK'), OVER, v('DmT')),
    '(set `self.DmDecel` (%s (%s (/ (- %s (* %s (%s (- (* 2.0 %s) %s) 0.0))) (%s DeltaSeconds 0.001)) 500.0 %s) 0.0 %s))' % (
        SF, M % 'FClamp', SPD, v('DmK'), M % 'FMax', C, v('DmPrevC'), M % 'FMax', v('DmMax'), OVER),
    '(set `self.DmT` (%s (+ %s DeltaSeconds) 0.0 %s))' % (SF, v('DmT'), OVER),
    '(set `self.DmPrevC` %s)' % C,
]
s = rd.strip(); p = '(set `self.RevDecel` '; assert s.startswith(p) and s.count('(') == s.count(')')
rd2 = ind + '(set `self.RevDecel` (%s %s %s))' % (M % 'FMax', s[len(p):-1], v('DmDecel'))
edits = [{'oldString': rd, 'newString': NL.join(ind + x for x in pre) + NL + rd2}]
if '--dry' in sys.argv: print(NL.join(pre)); print(rd2); sys.exit(0)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
out['edit'] = str(r2)[:2200] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200]
print('DM', json.dumps(out)[:3000])
