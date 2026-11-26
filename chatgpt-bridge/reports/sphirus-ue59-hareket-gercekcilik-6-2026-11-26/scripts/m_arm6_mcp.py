# m_arm6_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Posture; re-appliable) - pass 6 relaxed arms.
# Measured (a6_* / a6k_* idle recordings): the arm-abduction servo PS_DAL/R sat on its hard -14 deg floor in idle while the arms stayed
# 12 / 9 deg open (target 8.5); the source of the opening was the retarget (fixed in RTG_Sph_UEFN_to_MH). Here:
# - the -14 deg floor becomes PS_DAMin (so the servo can reach a relaxed target);
# - the arm-thigh clearance uses the B13 thigh radius tapered along the femur (measured 8.3 cm at the hip -> 5.2 cm near the knee, plus the
#   shorts) instead of one 10.5 cm cylinder: CA_Rad0 at the hip joint, CA_Rad1 at the knee, interpolated by the palm's position on the axis.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10)
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n in ('PS_DAMin', 'CA_Rad0', 'CA_Rad1'):
    if '"%s"' % n not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if 'PS_DAMin' in dsl and 'CA_Rad0' in dsl: print('ARM6 already'); sys.exit()
L = dsl.split(NL); edits = []
old = '(`KismetMathLibrary.FMin` -14.0 (* (`self.CT_TuckNow`) (`self.CT_Graze`)))'
for i, x in enumerate(L):
    if old in x and ('(set `self.PS_DAL`' in x or '(set `self.PS_DAR`' in x):
        edits.append({'oldString': x, 'newString': x.replace(old, '(`KismetMathLibrary.FMin` (`self.PS_DAMin`) (* (`self.CT_TuckNow`) (`self.CT_Graze`)))')})
assert len(edits) == 2, len(edits)
def SL(b): return '(`SceneComponent.GetSocketLocation` (`self.Manny`) "%s")' % b
for s, hb in (('L', 'l'), ('R', 'r')):
    i = [k for k, x in enumerate(L) if x.lstrip().startswith('(set `self.CA_C%s`' % s)]; assert len(i) == 1, (s, i); x = L[i[0]]
    palm = '(`KismetMathLibrary.VLerp` _returnvalue_%d %s (`self.CA_Palm`))' % (13 if hb == 'l' else 14, SL('middle_01_' + hb))
    t = '(/ (`KismetMathLibrary.Dot_VectorVector` (- %s %s) (- %s %s)) (`KismetMathLibrary.VSizeSquared` (- %s %s)))' % (palm, SL('thigh_' + hb), SL('calf_' + hb), SL('thigh_' + hb), SL('calf_' + hb), SL('thigh_' + hb))
    rad = '(`KismetMathLibrary.MapRangeClamped` %s 0.0 1.0 (`self.CA_Rad0`) (`self.CA_Rad1`))' % t
    assert x.count('(`self.CA_Rad`)') == 1, x.count('(`self.CA_Rad`)')
    edits.append({'oldString': x, 'newString': x.replace('(`self.CA_Rad`)', rad)})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('ARM6', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
