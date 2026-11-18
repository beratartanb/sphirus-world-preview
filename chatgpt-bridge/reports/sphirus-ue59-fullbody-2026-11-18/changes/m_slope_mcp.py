# m_slope_mcp.py (engine python, outside the editor; MCP client): in-memory edit of AC_Sph_Motion (NOT saved here; save goes through gsave.sh)
#  adds SlopeDeg, SlopePrev, SlopeLean, SlopeKUp, SlopeKDown, SlopeMaxUp, SlopeMaxDown, SlopeOn and extends the EffLean target with a
#  slope term (uphill forward lean, downhill slight back lean), then compiles. Output -> Saved/UE59Work/dsl/slope_apply.json
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105'))
import umcp
umcp.init()
def T(full, args):
    ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
BP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion.AC_Sph_Motion'; AP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'
out = {}
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n, t in (('SlopeDeg', 'float'), ('SlopePrev', 'Vector'), ('SlopeLean', 'float'), ('SlopeKUp', 'float'), ('SlopeKDown', 'float'), ('SlopeMaxUp', 'float'), ('SlopeMaxDown', 'float'), ('SlopeSlowUp', 'float'), ('SlopeSlowDown', 'float'), ('SlopeOn', 'bool')):
    if '"%s"' % n in have or "'%s'" % n in have: out['add_' + n] = 'exists'; continue
    out['add_' + n] = T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': t})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); out['read_err'] = r.get('isError') if isinstance(r, dict) else None
rv = r['content']['returnValue'] if isinstance(r.get('content'), dict) else json.loads(r['content'])['returnValue']
e = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Saved', 'UE59Work', 'dsl', 'slope_edit.json')))
assert rv['dsl'].count(e['old']) == 1 and rv['dsl'].count(e['old2']) == 1, 'old statements not unique/present'
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': e['old'], 'newString': e['new']}, {'oldString': e['old2'], 'newString': e['new2']}]})
out['edit'] = r2 if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Saved', 'UE59Work', 'dsl', 'slope_apply.json'), 'w'), indent=1, default=str)
print('SLOPE_APPLY', json.dumps(out, default=str)[:1500])
