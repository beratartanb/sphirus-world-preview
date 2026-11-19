# m_clipbrake_mcp.py (engine python, MCP client, in-memory edit of AC_Sph_Motion; save through gsave.sh) - 2026-11-19 evening.
# CLIP-BOUND STOP BRAKE. Diagnosis (an_stop3 on sim time, frame dumps): in a stop the planted foot slides because the capsule
# keeps moving after the stop clip has planted the foot - capsule PhysBrake decel (380..1100 by entry speed) does not follow the
# clip's own root speed (e.g. M_Neutral_Run_Stop_F: 500 cruise then 287/59/0 per 0.13 s). OffsetRootBone does not absorb it
# (no root-motion attribute reaches it: radius 25/45 had no effect). Fix: while stopping (no move input, PhysBrake, no montage)
# the brake decel is the one that brings the capsule to the root speed of the animation actually playing:
#   BrakeDecel = clamp((speed - movedata_speed * ClipK) / dt, ClipMin, ClipMax)
# movedata_speed is the authored root-speed curve of every GASP stop/loop clip, read from the blended driver pose.
# ClipBrakeOn=false restores the old brake exactly. ClipMin keeps a floor so a curve above the speed never stalls a stop.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
BP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion.AC_Sph_Motion'; AP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; out = {}
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n, t in (('ClipBrakeOn', 'bool'), ('ClipK', 'float'), ('ClipMin', 'float'), ('ClipMax', 'float')):
    out['add_' + n] = 'exists' if ('"%s"' % n in have) else T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': t})
    out['ie_' + n] = T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue'] if isinstance(r.get('content'), dict) else json.loads(r['content'])['returnValue']
old_expr = "(`KismetMathLibrary.SelectFloat` (* (`KismetMathLibrary.MapRangeClamped` (`self.BrakeLatchSpeed`) 165.0 585.0 (`self.BrakeDecelLow`) (`self.BrakeDecelHigh`)) (- 1.0 (* (`self.BrakeEffortK`) (`self.EUse`)))) 2000.0 (`self.PhysBrake`))"
old = "(set `self.BrakeDecel` " + old_expr + ")"
assert rv['dsl'].count(old) == 1, 'old not unique'
AI = "(`SkeletalMeshComponent.GetAnimInstance` (`Character.Mesh` _ascharacter))"
clip = ("(`KismetMathLibrary.FClamp` (/ (- (`KismetMathLibrary.VSizeXY` (`Actor.GetVelocity` _ascharacter)) (* (`AnimInstance.GetCurveValue` %s \"movedata_speed\") (`self.ClipK`))) "
        "(`KismetMathLibrary.FMax` DeltaSeconds 0.001)) (`self.ClipMin`) (`self.ClipMax`))") % AI
cond = ("(and (and (`self.ClipBrakeOn`) (`self.PhysBrake`)) (and (<= (`KismetMathLibrary.VSizeXY` (`Pawn.GetLastMovementInputVector` _ascharacter)) 0.1) "
        "(not (`AnimInstance.IsAnyMontagePlaying` %s))))") % AI
new = "(set `self.BrakeDecel` (`KismetMathLibrary.SelectFloat` " + clip + " " + old_expr + " " + cond + "))"
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': new}]})
out['edit'] = r2 if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
json.dump(out, open('Saved/UE59Work/dsl/clipbrake_apply.json', 'w'), indent=1, default=str); print('CLIPBRAKE', json.dumps(out, default=str)[:2500])
