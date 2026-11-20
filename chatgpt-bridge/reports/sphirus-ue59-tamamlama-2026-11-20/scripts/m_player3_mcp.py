# m_player3_mcp.py (MCP, in-memory edit of BP_HybridA_Player; saved by a gated write job) - 2026-11-20 round 3.
# 1 Same-frame back/strafe state. GR_Back was computed from GetLastMovementInputVector (updated by the movement component AFTER the
#   actor tick) and after parent.ReceiveTick, so the strafe flag reached the GASP character 1-2 frames after S was pressed: the first
#   search ran non-strafing and picked a "turn around" start/turn clip (walk S start: Reface_Start_F_L_180 for 0.4 s, planted foot
#   26 cm; run W->S: one frame of Run_Turn_180 before the pivot). Now the raw input of this frame (GR_RawIn, written by the
#   IA_Sph_Move handler) drives GR_Back and the gait state is written BEFORE parent.ReceiveTick.
# 2 Sprint stop-hold: S pressed while moving faster than GR_StopHoldMin (470): movement input is withheld until the speed is
#   below 80 cm/s (or S is no longer held), so the clip-bound sprint stop plays and the backward start follows from near
#   standstill, instead of a run pivot at sprint speed (planted foot 27-50 cm). Any other direction cancels the hold at once.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; out = {}
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n, ty in (('GR_RawIn', 'Vector'), ('GR_StopHold', 'bool'), ('GR_StopHoldMin', 'float')):
    if '"%s"' % n in have: continue
    out['add_' + n] = 'err' if T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': ty}).get('isError') else 'ok'
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
open('Saved/UE59Work/dsl/player_before_r3.dsl', 'w', encoding='utf8').write(dsl)
def line(prefix):
    L = [l for l in dsl.split('\n') if l.strip().startswith(prefix)]; assert len(L) == 1, (prefix, len(L)); return L[0]
SP = "(`KismetMathLibrary.VSizeXY` (`self.GetVelocity`))"
par = line("(`parent.ReceiveTick` DeltaSeconds)"); ind = par[:len(par) - len(par.lstrip())]
old_back = line("(set `self.GR_Back`"); assert old_back.count('_returnvalue_21') >= 1
new_back = old_back.replace('_returnvalue_21', '(`self.GR_RawIn`)')
i0 = new_back.index('(and (> (`KismetMathLibrary.VSize` (`self.GR_RawIn`)) 0.1)');
# BACKNOW = the "(and (not falling) (and input>0.1 (< dot ...)))" branch is embedded; stop-hold uses the same raw test without hysteresis detail
BACKRAW = "(and (> (`KismetMathLibrary.VSize` (`self.GR_RawIn`)) 0.1) (< (`KismetMathLibrary.Dot_VectorVector` (`KismetMathLibrary.Normal` (`self.GR_RawIn`)) (`KismetMathLibrary.GetForwardVector` (`KismetMathLibrary.MakeRotator` 0.0 0.0 (.yaw (`Controller.GetControlRotation` (`self.GetController`)))))) (`self.GR_BackCos`)))"
hold = ind + "(set `self.GR_StopHold` (and %s (or (and (not (`self.GR_Back`)) (> %s (`self.GR_StopHoldMin`))) (and (`self.GR_StopHold`) (> %s 80.0)))))" % (BACKRAW, SP, SP)
old_s = line("(set `self.SphContextSpeedScale`")
edits = [
    {'oldString': par + '\n', 'newString': ''},
    {'oldString': old_back, 'newString': hold + '\n' + new_back},
    {'oldString': old_s, 'newString': old_s + '\n' + ind + "(`parent.ReceiveTick` DeltaSeconds)"},
]
i0 = dsl.index("(event `EnhancedInput|/Game/Sphirus/Player/Input/IA_Sph_Move`"); blk = dsl[i0:dsl.index('\n\n', i0)]
s0 = blk[blk.index("  (:`Triggered`"):]
new_m = ("  (:`Triggered`\n"
         "    (set `self.GR_RawIn` (+ (* (`KismetMathLibrary.GetForwardVector` _returnvalue) (`KismetMathLibrary.MakeVector` _y _y _y)) (* (`KismetMathLibrary.GetRightVector` _returnvalue) (`KismetMathLibrary.MakeVector` _x _x _x))))\n"
         "    (if (not (`self.GR_StopHold`))\n"
         "      (`self.AddMovementInput` (`KismetMathLibrary.GetForwardVector` _returnvalue) _y)\n"
         "      (`self.AddMovementInput` (`KismetMathLibrary.GetRightVector` _returnvalue) _x)))\n"
         "  (:`Completed`\n"
         "    (set `self.GR_RawIn` (`KismetMathLibrary.MakeVector` 0.0 0.0 0.0)))\n"
         "  (:`Canceled`\n"
         "    (set `self.GR_RawIn` (`KismetMathLibrary.MakeVector` 0.0 0.0 0.0))))")
edits.append({'oldString': s0, 'newString': new_m})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
out['edit'] = str(r2)[:1800] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300]
print('PLAYER3', json.dumps(out)[:2400])
