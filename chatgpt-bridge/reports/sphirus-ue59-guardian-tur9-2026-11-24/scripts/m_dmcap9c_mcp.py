# m_dmcap9c_mcp.py (MCP, in-memory; re-appliable; after m_dmcap9b) - round 9: the ramp only applies when the new gait speed is below
# DmWalkV (step down to walk / tempo). Sprint -> run keeps the old behaviour (its transition clip was already selected and followed).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
MA = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; MB = MA + '.AC_Sph_Motion'; NL = chr(10)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': MB}}))
if '"DmWalkV"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': MB}, 'name': 'DmWalkV', 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': MB}, 'variableName': 'DmWalkV', 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': MB}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': MA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
l = [x for x in dsl.split(NL) if x.strip().startswith('(set `self.DmCap` ')]; assert len(l) == 1; l = l[0]
if 'DmWalkV' in l: print('DMCAP9C already'); sys.exit(0)
a = '(`KismetMathLibrary.FMax` (`self.GaitV`) (- (`self.DmCap`) (* (`KismetMathLibrary.FMax` (`self.DmRate`) (* (`self.DmCap`) (`self.DmRateK`))) DeltaSeconds)))'
assert l.count(a) == 1
b = '(`KismetMathLibrary.SelectFloat` %s (`self.GaitV`) (< (`self.GaitV`) (`self.DmWalkV`)))' % a
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': MA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': l.replace(a, b)}]})
print('DMCAP9C', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1200], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': MB}, 'bWarningsAsErrors': False}))[:100])
