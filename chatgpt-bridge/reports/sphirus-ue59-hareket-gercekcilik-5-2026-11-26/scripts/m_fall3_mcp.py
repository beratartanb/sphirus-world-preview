# m_fall3_mcp.py (MCP, in-memory): gameplay trigger for the physical fall - a landing faster than FL_LandV (cm/s, negative, default -1100,
# about a 6 m drop) starts the ragdoll fall with a forward pitch (FL_LandK * forward + small up), then the face-down get-up.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10)
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for nme in ('FL_LandV', 'FL_LandK'):
    if '"%s"' % nme not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': nme, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': nme, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if 'FL_LandV' in dsl: print('FALL3 already'); sys.exit()
L = dsl.split(NL); a = [i for i, x in enumerate(L) if x.startswith('(event `self.OnLanded`')]; assert len(a) == 1, a
p = a[0] + 2; assert "Sph_GASPLanded" in L[p], L[p]
add = ['  (if (< (.z (`self.GetVelocity`)) (`self.FL_LandV`))',
       '    (set `self.FL_Imp` (+ (* (`Actor.GetActorForwardVector` self) (`self.FL_LandK`)) (`KismetMathLibrary.MakeVector` 0.0 0.0 40.0)))',
       '    (set `self.FL_Fire` 1.0))']
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': L[p - 1] + NL + L[p], 'newString': L[p - 1] + NL + L[p] + NL + NL.join(add)}]})
print('FALL3', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
