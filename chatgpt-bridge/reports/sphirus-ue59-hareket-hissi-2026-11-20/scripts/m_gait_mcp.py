# m_gait_mcp.py (MCP, in-memory edit of BP_HybridA_Player; save via gsave.sh) - 2026-11-20.
# Gait ladder walk / tempo / run / sprint + backward tier + reversal brake hold.
#  - GR_TempoOn: toggled by IA_Sph_Pace (was a no-op). Tempo tier = Gait RUN with the Core Motion jog databases (GR_TempoVals
#    swapped into ABP_Sph_GASP.CM_Vals) at RunSpeeds x GR_KTempoRun (back: x GR_KTempoBack).
#  - S (GR_Back) no longer forces the walk gait: back tier = tempo when Shift/Sprint/TempoOn, else walk.
#  - GR_BrakeHold: when S is pressed against a forward run (speed > 200, input opposing velocity) the RUN gait is kept until the
#    velocity has reversed (or GR_HoldMax s), so the run pivot (brake - plant - push back) plays instead of a walk pivot at run speed.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; out = {}
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n, ty, opt in (('GR_TempoOn', 'bool', {}), ('GR_TempoAct', 'bool', {}), ('GR_TempoPrev', 'bool', {}), ('GR_BrakeHold', 'bool', {}), ('GR_HoldT', 'float', {}),
                   ('GR_KTempoRun', 'float', {}), ('GR_KTempoBack', 'float', {}), ('GR_HoldMax', 'float', {}),
                   ('GR_TempoVals', '/Script/PoseSearch.PoseSearchDatabase', {'containerType': 'Array'}), ('GR_NormVals', '/Script/PoseSearch.PoseSearchDatabase', {'containerType': 'Array'})):
    if '"%s"' % n in have: out['add_' + n] = 'exists'; continue
    r = T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': ty, 'options': opt}); out['add_' + n] = str(r)[:160]
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
open('Saved/UE59Work/dsl/player_before_gait.dsl', 'w', encoding='utf8').write(dsl)
def line(prefix):
    L = [l for l in dsl.split('\n') if l.strip().startswith(prefix)]; assert len(L) == 1, (prefix, len(L)); return L[0]
SP = "(`KismetMathLibrary.VSizeXY` (`self.GetVelocity`))"
RUNOK = "(not (or (> (`self.GR_HomeContext`) 0.5) (`self.GR_Load2H`)))"
DOTV = "(`KismetMathLibrary.Dot_VectorVector` (`KismetMathLibrary.Vector_Normal2D` (`self.GetLastMovementInputVector`)) (`KismetMathLibrary.Vector_Normal2D` (`self.GetVelocity`)))"
RUN = "(and (or (== (`self.GR_Gait`) 1) (== (`self.GR_Pace`) 1)) %s)" % RUNOK
TEMPO = "(and (`self.GR_TempoOn`) %s)" % RUNOK
SPR = "(and (and (== (`self.GR_Pace`) 1) %s) (and (not (`self.GR_CarryActive`)) (or (> %s 250.0) (== (`self.GR_GaitSel`) 2))))" % (RUNOK, SP)
J = "(`KismetMathLibrary.SelectInt` 1 0 (or %s %s))" % (RUN, TEMPO)
old_g = line("(set `self.GR_GaitSel`"); ind = old_g[:len(old_g) - len(old_g.lstrip())]
new_g = '\n'.join(ind + s for s in (
    "(set `self.GR_HoldT` (`KismetMathLibrary.SelectFloat` (+ (`self.GR_HoldT`) DeltaSeconds) 0.0 (and (and (and (`self.GR_Back`) %s) (>= (`self.GR_GaitSel`) 1)) (or (> (`self.GR_HoldT`) 0.0) (and (> %s 200.0) (< %s -0.2))))))" % (RUNOK, SP, DOTV),
    "(set `self.GR_BrakeHold` (and (and (> (`self.GR_HoldT`) 0.0) (< (`self.GR_HoldT`) (`self.GR_HoldMax`))) (not (and (> %s 0.5) (> %s 120.0)))))" % (DOTV, SP),
    "(set `self.GR_GaitSel` (`KismetMathLibrary.SelectInt` 1 (`KismetMathLibrary.SelectInt` %s (`KismetMathLibrary.SelectInt` 2 %s %s) (`self.GR_Back`)) (`self.GR_BrakeHold`)))" % (J, J, SPR),
    "(set `self.GR_TempoAct` (and (and (not (`self.GR_BrakeHold`)) (== (`self.GR_GaitSel`) 1)) (or (`self.GR_Back`) (not %s))))" % RUN,
    "(if (and (`self.GR_TempoAct`) (not (`self.GR_TempoPrev`)))",
    "  (bind _asabp_sph_gasp_t (cast `/Game/Sphirus/Player/GASP/ABP_Sph_GASP` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)))",
    "    (:`then`",
    "      (set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.CM_Vals` (`self.GR_TempoVals`) _asabp_sph_gasp_t))",
    "    (:`CastFailed`",
    "      _))",
    "  (set `self.GR_TempoPrev` true))",
    "(if (and (not (`self.GR_TempoAct`)) (`self.GR_TempoPrev`))",
    "  (bind _asabp_sph_gasp_n (cast `/Game/Sphirus/Player/GASP/ABP_Sph_GASP` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)))",
    "    (:`then`",
    "      (set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.CM_Vals` (`self.GR_NormVals`) _asabp_sph_gasp_n))",
    "    (:`CastFailed`",
    "      _))",
    "  (set `self.GR_TempoPrev` false))"))
edits = [{'oldString': old_g, 'newString': new_g}]
old_c = line("(set `self.CharacterInputState`"); a = "(or (or (== (`self.GR_GaitSel`) 0) _returnvalue_26) (`self.GR_Back`))"; assert old_c.count(a) == 1
edits.append({'oldString': old_c, 'newString': old_c.replace(a, "(or (== (`self.GR_GaitSel`) 0) _returnvalue_26)")})
old_s = line("(set `self.SphContextSpeedScale`")
a1 = "(`KismetMathLibrary.SelectFloat` (`self.GR_KCarryJog`) 1.0 (`self.GR_CarryActive`))"; a2 = "(`KismetMathLibrary.SelectFloat` (`self.GR_BackK`) 1.0 (`self.GR_Back`))"
assert old_s.count(a1) == 1 and old_s.count(a2) == 1
new_s = old_s.replace(a1, "(* %s (`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.SelectFloat` (`self.GR_KTempoBack`) (`self.GR_KTempoRun`) (`self.GR_Back`)) 1.0 (`self.GR_TempoAct`)))" % a1)
new_s = new_s.replace(a2, "(`KismetMathLibrary.SelectFloat` (`self.GR_BackK`) 1.0 (and (`self.GR_Back`) (== (`self.GR_GaitSel`) 0)))")
edits.append({'oldString': old_s, 'newString': new_s})
i0 = dsl.index("(event `EnhancedInput|/Game/Sphirus/Player/Input/IA_Sph_Pace`"); blk = dsl[i0:dsl.index('\n\n', i0)]
s0 = blk[blk.index("  (:`Started`"):]
edits.append({'oldString': s0, 'newString': "  (:`Started`\n    (set `self.GR_TempoOn` (not (`self.GR_TempoOn`)))))"})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
out['edit'] = str(r2)[:1500] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:600]
json.dump(out, open('Saved/UE59Work/dsl/gait_apply.json', 'w'), indent=1, default=str); print('GAIT', json.dumps(out, default=str)[:2500])
