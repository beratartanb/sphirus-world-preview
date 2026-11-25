# m_foothold2_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Foot; re-appliable) - movement pass 4, fix of m_foothold.
# The stop foot hold never latched: its "both contact curves > 50" support test is never true after a stop (debug recording p4D_stop:
# SH_T ran up to 2 s, SH_Lat stayed false). Support is now taken from the measured driver-foot speeds of the same event
# (SL_VR / SL_VL, cm/s): both feet still (< SH_VStill) = both in support.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10)
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"SH_VStill"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'SH_VStill', 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'SH_VStill', 'bInstanceEditable': True})
    T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
L = [x for x in dsl.split(NL) if x.startswith('  (set `self.SH_Lat` ')]; assert len(L) == 1, len(L); old = L[0]
if '`self.SH_VStill`' in old: print('FOOTHOLD2 already'); sys.exit(0)
import re
cr = re.search(r'\(> \(`AnimInstance\.GetCurveValue` \(`SkeletalMeshComponent\.GetAnimInstance` \(`self\.Mesh`\)\) "contact_r"\) 50\.0\)', old)
cl = re.search(r'\(> \(`AnimInstance\.GetCurveValue` \(`SkeletalMeshComponent\.GetAnimInstance` \(`self\.Mesh`\)\) "contact_l"\) 50\.0\)', old)
assert cr and cl, old[:400]
new = old.replace(cr.group(0), '(< (`self.SL_VR`) (`self.SH_VStill`))').replace(cl.group(0), '(< (`self.SL_VL`) (`self.SH_VStill`))')
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': new}]})
print('FOOTHOLD2', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:3000], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300])
