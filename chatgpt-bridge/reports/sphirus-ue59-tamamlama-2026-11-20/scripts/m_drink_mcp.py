# m_drink_mcp.py (MCP, in-memory edit of BP_GR_DayStation): the tea station's second use (drink, GR_Clip2) only played the montage;
# the contact / state / restore chain lived in the other branch, so GR_Tea never became 2, GR_Busy stayed true and move/look input
# stayed ignored after drinking (player locked). The drink branch now waits GR_ContactT and joins the same chain (label 3).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
S = '/Game/GraceRanger/SF/Day/BP_GR_DayStation'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': S, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
L = [l for l in dsl.split('\n') if '(`self.GR_Clip2`) 1.0 "MontageLength" 0.0 true)' in l]; assert len(L) == 1; old = L[0]
ind = old[:len(old) - len(old.lstrip())]
new = old + '\n' + ind + "(`KismetSystemLibrary.Delay` (`self.GR_ContactT`))\n" + ind + "(goto _label_3)"
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': S, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': new}]})
print('DRINK', str(r2)[:900] if r2.get('isError') else 'ok', str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': S + '.BP_GR_DayStation'}, 'bWarningsAsErrors': False}))[:150])
