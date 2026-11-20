# m_day2_mcp.py: station part of m_day_mcp.py (the hub part was applied first): after the bed station (kind 9) has finished,
# call the hub's GR_Sleep (fade, day reset, wake sequence).
import json, sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
S = '/Game/GraceRanger/SF/Day/BP_GR_DayStation'; H = '/Game/GraceRanger/SF/Day/BP_GR_DayHub'
h = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': H, 'scope': ''})['content']['returnValue']['dsl']; print('HUB has GR_Sleep', h.count('(event `GR_Sleep`'), 'FireSt', h.count('GR_FireSt'))
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': S, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
L = [l for l in dsl.split('\n') if 'BP_GR_DayHub.GR_Store` (`self.GR_Hub`)' in l]; assert len(L) == 1; old = L[0]
m = re.match(r'^(\s*)(\(`/Game/GraceRanger/SF/Day/BP_GR_DayHub\.GR_Store` \(`self\.GR_Hub`\)\))(\)*)$', old); assert m, old[-80:]
ind = m.group(1); tail = m.group(3)
new = ind + m.group(2) + '\n' + ind + "(if (== (`self.GR_Kind`) 9)\n" + ind + "  (`/Game/GraceRanger/SF/Day/BP_GR_DayHub.GR_Sleep` (`self.GR_Hub`)))" + tail
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': S, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': new}]})
print('STATION', str(r2)[:800] if r2.get('isError') else 'ok', str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': S + '.BP_GR_DayStation'}, 'bWarningsAsErrors': False}))[:150])
