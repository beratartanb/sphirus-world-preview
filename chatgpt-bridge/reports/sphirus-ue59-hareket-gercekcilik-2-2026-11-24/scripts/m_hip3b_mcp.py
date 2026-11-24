# m_hip3b_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Posture; after m_hip3; re-appliable) - movement realism pass 2.
# The neck counter-rotation on the DRIVER (c_hip3, HD_K) restored head yaw but doubled head roll on the visible body (run 7.0 -> 14.5 deg):
# the retarget copies the neck's local rotation onto a differently oriented MetaHuman neck. HD_K stays 0; the same counter-yaw goes to the
# visible body's own head input VI_Head (bone space; yaw axis = (0.98,-0.199,0), orthogonal to the existing lateral-tilt axis): HD_B x SH_Yaw.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; NL = chr(10); K = '`KismetMathLibrary.%s`'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"HD_B"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'HD_B', 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'HD_B', 'bInstanceEditable': True})
    T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`self.HD_B`' in dsl: print('HIP3B already'); sys.exit(0)
pre = '(set `/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP.VI_Head` '; suf = ' _asabp_sph_body_gasp)'
l = [x for x in dsl.split(NL) if x.strip().startswith(pre)]; assert len(l) == 1; l = l[0]; s_ = l.strip(); assert s_.endswith(suf); ind = l[:len(l) - len(l.lstrip())]
val = s_[len(pre):-len(suf)]; s = '(* (`self.SH_Yaw`) (`self.HD_B`))'
new = ind + pre + '(+ %s (* (%s 0.98 -0.199 0.0) (%s %s %s %s)))' % (val, K % 'MakeVector', K % 'MakeVector', s, s, s) + suf
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': new}]})
print('HIP3B', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1800], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:100])
