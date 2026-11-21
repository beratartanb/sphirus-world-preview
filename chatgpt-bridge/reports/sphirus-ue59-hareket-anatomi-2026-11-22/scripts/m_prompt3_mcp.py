# m_prompt3_mcp.py (MCP, in-memory edit of BP_GR_DayStation; follows m_prompt_mcp.py + m_prompt2_mcp.py) - 2026-11-22 round 5.
# CanInteract did not hide the prompt either (r5_bed2 frames). The prompt is the station's own SFInteractionWidget_SC component, which
# shows itself inside DisplayFromRange. For the station sequence that range is set to 0 (remembered in GR_PromptRng) and restored at the
# end (GR_PromptOn). The CanInteract switch of m_prompt2 is removed again.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
ST = '/Game/GraceRanger/SF/Day/BP_GR_DayStation'; BP = ST + '.BP_GR_DayStation'; MGR = '/Game/StoryFramework/Core/Blueprints/Components/Core/SFInteractionManager_AC'
SFW = '/Game/StoryFramework/Core/Blueprints/Components/Other/SFInteractionWidget_SC'; out = {}; NL = chr(10)
def sw(b): return '(set `%s.CanInteract` %s (cast `%s` (`self.GetComponentByClass` (`GameplayStatics.GetPlayerController` 0) "%s.SFInteractionManager_AC_C")))' % (MGR, b, MGR, MGR)
RNG = '(`%s.DisplayFromRange` (`self.SFInteractionWidget_SC`))' % SFW
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"GR_PromptRng"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'GR_PromptRng', 'typeName': 'float'})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': ST, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
assert dsl.count(sw('false')) == 1 and dsl.count(sw('true')) == 2, (dsl.count(sw('false')), dsl.count(sw('true')))
edits = []
for l in dsl.split(NL):
    ind = l[:len(l) - len(l.lstrip())]
    if l.strip() == sw('false'):
        edits.append({'oldString': l, 'newString': ind + '(set `self.GR_PromptRng` (`KismetMathLibrary.FMax` (`self.GR_PromptRng`) %s))' % RNG + NL + ind + '(set `%s.DisplayFromRange` 0.0 (`self.SFInteractionWidget_SC`))' % SFW})
    elif l.strip() in (sw('true'), sw('true') + ')'):
        cl = ')' if l.strip().endswith('")))' + ')') else ''
        edits.append({'oldString': l, 'newString': ind + '(if (> (`self.GR_PromptRng`) 0.0)' + NL + ind + '  (set `%s.DisplayFromRange` (`self.GR_PromptRng`) (`self.SFInteractionWidget_SC`)))' % SFW + cl})
assert len(edits) == 3, len(edits)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': ST, 'revision': rv['revision'], 'scope': '', 'edits': edits})
out['edit'] = str(r2)[:2200] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200]
print('PROMPT3', json.dumps(out)[:3000])
