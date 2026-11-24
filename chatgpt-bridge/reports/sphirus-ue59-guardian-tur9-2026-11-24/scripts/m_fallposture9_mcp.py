# m_fallposture9_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Posture; re-appliable) - round 9.
# Fall / lying / get-up: "hands hang in the air" root cause. The DRIVER pose of the prone fall is correct (g8_log_sprint lying: hands z 0,
# forearm 1.5, head 20, pelvis 14 cm). The VISIBLE body showed hands at 37 / 63 cm and the head at 54 cm: the posture layer (upright
# spine carriage, arm carriage angles PS_A1..4 = 87 / 47 deg, head levelling) kept correcting a torso that is meant to be horizontal.
# New weight PS_FW (1 = posture layer as before): 0 while falling / lying (CT_State 8, 9), during get-up (10) it returns with the driver
# pelvis height (40 -> 75 cm above the floor). All VI_* outputs of the posture layer are multiplied by PS_FW, so on the ground the visible
# body is the retargeted clip pose: palms and forearms on the floor, weight on hands and knees while pushing up.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; NL = chr(10)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"PS_FW"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'PS_FW', 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'PS_FW', 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']; L = dsl.split(NL)
if 'self.PS_FW`' in dsl: print('FALLPOSTURE9 already'); sys.exit(0)
l0 = [x for x in L if x.strip().startswith('(bind _returnvalue_19 (`KismetMathLibrary.FClamp` (`self.GR_PDt`)')]; assert len(l0) == 1, len(l0); l0 = l0[0]; ind = l0[:len(l0) - len(l0.lstrip())]
PH = '(- (.z (`SceneComponent.GetSocketLocation` (`self.Mesh`) "pelvis")) (- (.z (`self.K2_GetActorLocation`)) 88.0))'
TG = '(`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.SelectFloat` 0.0 (`KismetMathLibrary.MapRangeClamped` %s 40.0 75.0 0.0 1.0) (< (`self.CT_State`) 10)) 1.0 (>= (`self.CT_State`) 8))' % PH
edits = [{'oldString': l0, 'newString': l0 + NL + ind + '(set `self.PS_FW` (`KismetMathLibrary.FInterpTo` (`self.PS_FW`) %s _returnvalue_19 8.0))' % TG}]
suf = ' _asabp_sph_body_gasp)'; n = 0
for x in L:
    s_ = x.strip()
    if s_.startswith('(set `/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP.VI_') and suf in s_:
        j = s_.rindex(suf); tail = s_[j + len(suf):]; assert set(tail) <= set(')'), tail   # the last line also closes its block
        i = s_.index('` ') + 2; head = s_[:i]; val = s_[i:j]
        edits.append({'oldString': x, 'newString': x[:len(x) - len(x.lstrip())] + head + '(* %s (`KismetMathLibrary.MakeVector` (`self.PS_FW`) (`self.PS_FW`) (`self.PS_FW`)))' % val + suf + tail}); n += 1
assert n == 10, n
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('FALLPOSTURE9', n, 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:100])
