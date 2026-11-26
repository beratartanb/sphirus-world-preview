# m_contact13_mcp.py (MCP, in-memory): a real contact strong enough to knock her down now leads to a fall (pass 6).
# Before: the region reaction impulse is capped (RC_Max 650 x region gain <= 1) and the torso regions are 0.5-0.8 of it, so a real hit never
# reached the fall threshold FL_ImpMin 600 (falls only came from injected IMP_PLAN / FL_PLAN or high landings). Now: if the normal relative
# speed of the contact exceeds RC_FallV (900 cm/s - well above a sprint into a wall, ~650, which the anticipation already brakes), the hit
# becomes a whole-body hit (IMP_All 1) with an impulse along the contact normal of min(vn, RC_FallMax) -> the existing tick routes it into
# the fall (FL_Imp = IMP_Imp * FL_ImpK, plus the body velocity).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10)
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n in ('RC_FallV', 'RC_FallMax', 'RC_KO'):
    if '"%s"' % n not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if 'RC_FallV`' in dsl: print('RC13 already'); sys.exit()
L = dsl.split(NL)
a = [i for i, x in enumerate(L) if x.strip().startswith('(set `self.IMP_Push` (`KismetMathLibrary.SelectFloat` (`self.RC_PushK`)')]; assert len(a) == 1, a
ind = L[a[0]][:len(L[a[0]]) - len(L[a[0]].lstrip())]
ko = [ind + '(set `self.RC_KO` 0.0)',
      ind + '(if (> (`self.RC_VN`) (`self.RC_FallV`))',
      ind + '  (set `self.IMP_All` 1.0)',
      ind + '  (set `self.IMP_Imp` (* (* HitNormal (`self.RC_NS`)) (`KismetMathLibrary.FMin` (* (`self.RC_VN`) (`self.RC_K`)) (`self.RC_FallMax`))))',
      ind + '  (set `self.RC_KO` 1.0))']
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': L[a[0]], 'newString': NL.join(ko) + NL + L[a[0]]}]})
print('RC13', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:3000], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
