# m_prompt2_mcp.py (MCP, in-memory edit of BP_GR_DayStation; follows m_prompt_mcp.py) - 2026-11-22 round 5.
# Hiding the station's InteractionPromptLoc component did not remove the prompt (r5_bed frames: "Yatak / Uzan / Kalk" visible while lying
# and on the black fade frame): the prompt is drawn by the Story Framework interaction manager on the player controller. The station now
# switches that manager's CanInteract off for its sequence and on again at the end (GR_PromptOn, also called by the hub after waking).
# builtins-free; argument 'mode=<name>' picks the manager switch to use (default CanInteract).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
ST = '/Game/GraceRanger/SF/Day/BP_GR_DayStation'; MGR = '/Game/StoryFramework/Core/Blueprints/Components/Core/SFInteractionManager_AC'; out = {}; NL = chr(10)
def sw(b): return '(set `%s.CanInteract` %s (cast `%s` (`self.GetComponentByClass` (`GameplayStatics.GetPlayerController` 0) "%s.SFInteractionManager_AC_C")))' % (MGR, b, MGR, MGR)
def hide(b): return '(`SceneComponent.SetHiddenInGame` (`self.InteractionPromptLoc`) %s true)' % b
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': ST, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
assert 'GR_PromptOn' in dsl and '.CanInteract`' not in dsl, 'state unexpected'
edits = []
for l in dsl.split(NL):
    if l.strip() == hide('true'): edits.append({'oldString': l, 'newString': l + NL + l[:len(l) - len(l.lstrip())] + sw('false')})
i0 = dsl.index('(event `GR_PromptOn`'); c = dsl.find(NL + NL + '(', i0); blk = (dsl[i0:c] if c > 0 else dsl[i0:]).rstrip(NL)
assert blk.endswith(hide('false') + ')'), blk[-120:]
edits.append({'oldString': blk, 'newString': blk[:-1] + NL + '  ' + sw('true') + ')'})
offl = [l for l in dsl.split(NL) if l.strip() == hide('false')]; assert len(offl) == 1, len(offl)
edits.append({'oldString': offl[0], 'newString': offl[0] + NL + offl[0][:len(offl[0]) - len(offl[0].lstrip())] + sw('true')})
assert len(edits) == 3, len(edits)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': ST, 'revision': rv['revision'], 'scope': '', 'edits': edits})
out['edit'] = str(r2)[:1800] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': ST + '.BP_GR_DayStation'}, 'bWarningsAsErrors': False}))[:200]
print('PROMPT2', json.dumps(out)[:3000])
