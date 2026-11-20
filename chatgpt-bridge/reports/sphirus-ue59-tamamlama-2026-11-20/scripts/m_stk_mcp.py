# m_stk_mcp.py (MCP, in-memory edit of AC_Sph_Motion; saved by a gated write job) - 2026-11-20 round 3.
# 1 Stop profile scale latched from the stop clip itself. Before: K = 1, or release speed / 375 above 470 cm/s. A tempo stop
#   (278 or 234 cm/s) on a 375 cm/s stop clip left the capsule coasting until the clip speed fell below it (contact drift
#   19-25 cm backward, 51-60 cm when the stop began inside a run turn clip). Now, during the first StLatch seconds after the
#   input is released, StK = clamp(release speed / movedata_speed of the driver pose, StKMin, StKMax) and is held afterwards:
#   the capsule follows the stop clip's own profile scaled to the real release speed for every gait and direction.
# 2 Start cap (StartCapOn): for StartDur seconds after leaving standstill the max speed is capped to the start clip's root
#   speed x StartK + StartAdd (TurnCap output, read by CalculateMaxSpeed), StartK = max walk speed / reference loop speed of
#   the band (200 / 278 / 500 / 585), so the capsule cannot run ahead of the first step.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; BP = AP + '.AC_Sph_Motion'; out = {}
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n, ty in (('StT', 'float'), ('StK', 'float'), ('StLatch', 'float'), ('StKMin', 'float'), ('StKMax', 'float'), ('StKOn', 'bool'),
              ('StartT', 'float'), ('StartDur', 'float'), ('StartAdd', 'float'), ('StartCapOn', 'bool'), ('StartCapK', 'float')):
    if '"%s"' % n in have: continue
    out['add_' + n] = 'err' if T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': ty}).get('isError') else 'ok'
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
open('Saved/UE59Work/dsl/AC_Sph_Motion_before_stk.dsl', 'w', encoding='utf8').write(dsl)
def line(prefix):
    L = [l for l in dsl.split('\n') if l.strip().startswith(prefix)]; assert len(L) == 1, (prefix, len(L)); return L[0]
C = '(`AnimInstance.GetCurveValue` (`SkeletalMeshComponent.GetAnimInstance` (`Character.Mesh` _ascharacter)) "movedata_speed")'
SPD = '(`KismetMathLibrary.VSizeXY` (`Actor.GetVelocity` _ascharacter))'
HASIN = '(> (`KismetMathLibrary.VSizeXY` (`Pawn.GetLastMovementInputVector` _ascharacter)) 0.1)'
MWS = '(`CharacterMovementComponent.MaxWalkSpeed` (`Character.CharacterMovement` _ascharacter))'
CP = '(`KismetMathLibrary.FMax` (- (* 2.0 %s) (`self.ClipPrevC`)) 0.0)' % C
old_b = line('(set `self.BrakeDecel`'); ind = old_b[:len(old_b) - len(old_b.lstrip())]
kold = "(`KismetMathLibrary.FMax` (`self.ClipK`) (`KismetMathLibrary.SelectFloat` (/ (`self.BrakeLatchSpeed`) (`KismetMathLibrary.FMax` (`self.ClipHiRef`) 1.0)) 0.0 (> (`self.BrakeLatchSpeed`) (`self.ClipHiMin`))))"
assert old_b.count(kold) == 1
new_b = old_b.replace(kold, "(`KismetMathLibrary.SelectFloat` (`self.StK`) %s (`self.StKOn`))" % kold)
REF = "(`KismetMathLibrary.SelectFloat` 585.0 (`KismetMathLibrary.SelectFloat` 500.0 (`KismetMathLibrary.SelectFloat` 278.0 200.0 (> %s 215.0)) (> %s 350.0)) (> %s 500.0))" % (MWS, MWS, MWS)
pre = [
    "(set `self.StT` (`KismetMathLibrary.SelectFloat` 0.0 (+ (`self.StT`) DeltaSeconds) %s))" % HASIN,
    "(set `self.StK` (`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.FClamp` (/ (`self.BrakeLatchSpeed`) (`KismetMathLibrary.FMax` %s 50.0)) (`self.StKMin`) (`self.StKMax`)) (`self.StK`) (and (not %s) (< (`self.StT`) (`self.StLatch`)))))" % (C, HASIN),
    "(set `self.StartT` (`KismetMathLibrary.SelectFloat` (+ (`self.StartT`) DeltaSeconds) 0.0 (and %s (or (> (`self.StartT`) 0.0) (< %s 30.0)))))" % (HASIN, SPD),
]
old_t = line('(set `self.TurnCap`')
new_t = ind + "(set `self.TurnCap` (`KismetMathLibrary.SelectFloat` (+ (* (* %s (/ %s %s)) (`self.StartCapK`)) (`self.StartAdd`)) 100000.0 (and (and (`self.StartCapOn`) (> (`self.StartT`) 0.0)) (and (< (`self.StartT`) (`self.StartDur`)) (> %s 1.0)))))" % (C, MWS, REF, C)
edits = [{'oldString': old_b, 'newString': '\n'.join(ind + s for s in pre) + '\n' + new_b}, {'oldString': old_t, 'newString': new_t}]
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
out['edit'] = str(r2)[:1500] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200]
print('STK', json.dumps(out)[:2200])
