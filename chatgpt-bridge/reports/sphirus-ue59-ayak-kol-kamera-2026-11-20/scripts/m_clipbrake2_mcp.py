# m_clipbrake2_mcp.py (MCP, in-memory; save via gsave.sh) - refinement of the clip-bound stop brake (2026-11-19 evening):
#  1 the character applies BrakeDecel one frame later (bdw = previous bd in the 30 Hz readout), so the capsule trailed the falling
#    root-speed curve by one frame: the curve is extrapolated one frame ahead: c1 = max(0, 2c - ClipPrevC).
#  2 clips without root speed (turn-in-place picked while still moving: curve 0 at 167 cm/s) slammed the 3000 cap and dragged the
#    foot 35 cm: the clip brake only runs when the curve carries root speed (c > 1) or the capsule is nearly stopped (< 60 cm/s).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
BP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion.AC_Sph_Motion'; AP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; out = {}
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
out['add'] = 'exists' if '"ClipPrevC"' in have else T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'ClipPrevC', 'typeName': 'float'})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue'] if isinstance(r.get('content'), dict) else json.loads(r['content'])['returnValue']
d = rv['dsl']; i = d.find('(set `self.BrakeDecel` '); j = d.find('\n', i); old = d[i:j]
assert old.count('movedata_speed') == 1, old[:300]
open('Saved/UE59Work/dsl/clipbrake_line_before.txt', 'w', encoding='utf8').write(old)
AI = "(`SkeletalMeshComponent.GetAnimInstance` (`Character.Mesh` _ascharacter))"
CV = "(`AnimInstance.GetCurveValue` %s \"movedata_speed\")" % AI
SPD = "(`KismetMathLibrary.VSizeXY` (`Actor.GetVelocity` _ascharacter))"
C1 = "(`KismetMathLibrary.FMax` (- (* 2.0 %s) (`self.ClipPrevC`)) 0.0)" % CV
clip = "(`KismetMathLibrary.FClamp` (/ (- %s (* %s (`self.ClipK`))) (`KismetMathLibrary.FMax` DeltaSeconds 0.001)) (`self.ClipMin`) (`self.ClipMax`))" % (SPD, C1)
old_expr = "(`KismetMathLibrary.SelectFloat` (* (`KismetMathLibrary.MapRangeClamped` (`self.BrakeLatchSpeed`) 165.0 585.0 (`self.BrakeDecelLow`) (`self.BrakeDecelHigh`)) (- 1.0 (* (`self.BrakeEffortK`) (`self.EUse`)))) 2000.0 (`self.PhysBrake`))"
assert old.count(old_expr) == 1
cond = ("(and (and (and (`self.ClipBrakeOn`) (`self.PhysBrake`)) (and (<= (`KismetMathLibrary.VSizeXY` (`Pawn.GetLastMovementInputVector` _ascharacter)) 0.1) "
        "(not (`AnimInstance.IsAnyMontagePlaying` %s)))) (or (> %s 1.0) (< %s 60.0)))") % (AI, CV, SPD)
new = "(set `self.BrakeDecel` (`KismetMathLibrary.SelectFloat` " + clip + " " + old_expr + " " + cond + "))\n  (set `self.ClipPrevC` " + CV + ")"
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': new}]})
out['edit'] = r2 if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
json.dump(out, open('Saved/UE59Work/dsl/clipbrake2_apply.json', 'w'), indent=1, default=str); print('CLIPBRAKE2', json.dumps(out, default=str)[:1500])
