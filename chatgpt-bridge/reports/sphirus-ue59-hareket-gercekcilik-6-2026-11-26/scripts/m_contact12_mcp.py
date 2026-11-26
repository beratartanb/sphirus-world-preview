# m_contact12_mcp.py (MCP, in-memory): fallback when no obstacle probe finds the contact (small / moving objects that already bounced
# off): the region comes from the contact point itself against the visible body's bone heights (above neck_01 head; above spine_03
# shoulder / chest by side; above pelvis - 8 forearm / belly; else legs) - for a small object the capsule contact sits at the object's height.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); BQ = chr(96)
def K(f): return BQ + 'KismetMathLibrary.' + f + BQ
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if 'RC_Lvl` 5.0' in dsl: print('RC12 already'); sys.exit()
L = dsl.split(NL)
i = [k for k, x in enumerate(L) if x.strip() == '(set `self.RC_Lvl` 0.0)']; assert len(i) == 1, i; i = i[0]
assert L[i - 1].strip() == '(elif true', L[i - 1]
j = i + 1
while not L[j].strip().startswith('(set `self.RC_Reg` 8.0)'): j += 1
ind = L[i][:len(L[i]) - len(L[i].lstrip())]; tailp = L[j][len(L[j].rstrip(')')) + 1:]  # closing parens after the RC_Reg 8 line (its own set paren excluded)
N = '(* HitNormal (`self.RC_NS`))'
def SZ(b): return '(.z (`SceneComponent.GetSocketLocation` (`self.Manny`) "%s"))' % b
def hit(sim, bone, al, k, reg):
    return ['(set `self.IMP_SimB` "%s")' % sim, '(set `self.IMP_Bone` "%s")' % bone, '(set `self.IMP_All` %s)' % al,
            '(set `self.IMP_Imp` (* %s (* %s (%s (* (`self.RC_VN`) (`self.RC_K`)) (`self.RC_Max`)))))' % (N, k, K('FMin')), '(set `self.RC_Reg` %s)' % reg]
def b(lines, d): return [ind + '  ' * d + x for x in lines]
lat = '(set `self.RC_Lat` (%s (- HitLocation (`SceneComponent.GetSocketLocation` (`self.Manny`) "spine_03")) (`Actor.GetActorRightVector` self)))' % K('Dot_VectorVector')
z = '(.z HitLocation)'
new = [ind + '(set `self.RC_Lvl` 5.0)', ind + lat,
       ind + '(if (> %s %s)' % (z, SZ('neck_01'))] + b(hit('spine_04', 'head', '0.0', '1.0', '1.0'), 1) + [
       ind + '  (elif (> %s %s)' % (z, SZ('spine_03')),
       ind + '    (if (> (%s (`self.RC_Lat`)) (`self.RC_ShW`))' % K('Abs'),
       ind + '      (if (> (`self.RC_Lat`) 0.0)'] + b(hit('spine_02', 'upperarm_r', '0.0', '1.0', '3.0'), 4) + [ind + '        (else'] + b(hit('spine_02', 'upperarm_l', '0.0', '1.0', '2.0'), 5) + [ind + '          ))',
       ind + '      (else'] + b(hit('spine_02', 'spine_04', '1.0', '0.8', '4.0'), 4) + [ind + '        ))',
       ind + '    (elif (> %s (- %s 8.0))' % (z, SZ('pelvis')),
       ind + '      (if (> (%s (`self.RC_Lat`)) (`self.RC_ArmW`))' % K('Abs'),
       ind + '        (if (> (`self.RC_Lat`) 0.0)'] + b(hit('upperarm_r', 'lowerarm_r', '0.0', '1.0', '6.0'), 5) + [ind + '          (else'] + b(hit('upperarm_l', 'lowerarm_l', '0.0', '1.0', '5.0'), 6) + [ind + '            ))',
       ind + '        (else'] + b(hit('spine_01', 'spine_03', '1.0', '0.7', '7.0'), 5) + [ind + '          ))',
       ind + '      (elif true'] + b(hit('spine_01', 'spine_01', '1.0', '0.5', '8.0'), 4) + [ind + '        ))))' + tailp]
old = NL.join(L[i:j + 1])
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': NL.join(new)}]})
print('RC12', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:3000], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
