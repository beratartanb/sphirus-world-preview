# m_fallposture9b_mcp.py (MCP, in-memory; BP_HybridA_Player; after m_fallposture9; re-appliable) - round 9.
# Real owner of "hands and chest in the air while lying" (measured with hk_fall9: row.hook.bl): the visible body's landing / stop lean
# limiter (ABP_Sph_Body_GASP PL_Spine3 / PL_Spine5, component-space, cap LeanCorrMax 40 deg). A prone trunk reads as a 90 deg forward
# lean, so the limiter sat at its cap (-20 / -20 deg) through falling, lying and getting up and bent the spine 40 deg off the floor
# (driver hands z 0, head 20 cm; visible hands 36 / 62, head 53). The posture layer was only a small part (PS off: unchanged).
# The limiter's cap now follows the fall weight PS_FW (0 while falling / lying, back to 1 as the pelvis rises in the get-up).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; NL = chr(10)
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if 'ABP_Sph_Body_GASP.LeanCorrMax`' in dsl: print('FALLPOSTURE9B already'); sys.exit(0)
l = [x for x in dsl.split(NL) if x.strip().startswith('(set `/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP.VI_Spine3` ')]; assert len(l) == 1; l = l[0]; ind = l[:len(l) - len(l.lstrip())]
new = ind + '(set `/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP.LeanCorrMax` (* 40.0 (`self.PS_FW`)) _asabp_sph_body_gasp)' + NL + l
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': new}]})
print('FALLPOSTURE9B', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:100])
