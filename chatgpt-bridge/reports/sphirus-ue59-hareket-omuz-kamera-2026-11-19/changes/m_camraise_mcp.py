# m_camraise_mcp.py (engine python, MCP client, in-memory edit of AC_Sph_Camera; save through gsave.sh):
# tight-space camera: instead of pulling the camera straight toward the head at head height when the boom is blocked
# (L, Y and Z all x SafeFrac), raise it by up to TightRaise cm (limited by the ceiling probe DUp - 40), smoothed (5/s).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
BP = '/Game/Sphirus/Player/Camera/AC_Sph_Camera.AC_Sph_Camera'; AP = '/Game/Sphirus/Player/Camera/AC_Sph_Camera'; out = {}
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n in ('TightRaise', 'TRaiseA'):
    out['add_' + n] = 'exists' if ('"%s"' % n in have) else T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'})
out['ie'] = T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'name': 'TightRaise', 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue'] if isinstance(r.get('content'), dict) else json.loads(r['content'])['returnValue']
old = "(set `self.Z` (* (`self.Z`) (`self.SafeFrac`)))"
new = ("(set `self.TRaiseA` (`KismetMathLibrary.FInterpTo` (`self.TRaiseA`) (* (`KismetMathLibrary.MapRangeClamped` (`self.SafeFrac`) 1.0 0.4 0.0 1.0) "
       "(`KismetMathLibrary.FMin` (`self.TightRaise`) (`KismetMathLibrary.FMax` (- (`self.DUp`) 40.0) 0.0))) DeltaSeconds 5.0))\n"
       "  (set `self.Z` (+ (* (`self.Z`) (`self.SafeFrac`)) (`self.TRaiseA`)))")
assert rv['dsl'].count(old) == 1, 'old not unique'
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': new}]})
out['edit'] = r2 if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
json.dump(out, open('Saved/UE59Work/dsl/camraise_apply.json', 'w'), indent=1, default=str); print('CAMRAISE', json.dumps(out, default=str)[:1500])
