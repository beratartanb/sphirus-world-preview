# m_camaim_mcp.py (MCP, in-memory edit of AC_Sph_Camera) - 2026-11-22 round 5.
# The context camera never pitches below "head top inside the frame". For the mask inspection the mask is held 36 cm below and in front
# of the head, so that rule turned the camera up to the room / ceiling whenever it sat near the shoulder (r5_maskA / r5_maskB frames) and
# only a camera high above the head could see the mask (head filling the frame). When a station asks for full aim at its target
# (OvW >= 0.99) the head rule is skipped and the camera looks at the target.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/Player/Camera/AC_Sph_Camera'; BP = AP + '.AC_Sph_Camera'; out = {}; NL = chr(10)
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
open('Saved/UE59Work/dsl/cam_before_aim.dsl', 'w', encoding='utf8').write(dsl)
L = [l for l in dsl.split(NL) if l.strip().startswith('(set `self.WorkRot` (`KismetMathLibrary.MakeRotator`')]; assert len(L) == 1, len(L)
l = L[0]; a = '(`KismetMathLibrary.FMax` (.pitch (`self.WorkRot`)) '; assert l.count(a) == 1 and 'OvW' not in l
i0 = l.index(a); d = 0
for i1 in range(i0, len(l)):
    if l[i1] == '(': d += 1
    elif l[i1] == ')':
        d -= 1
        if d == 0: break
fm = l[i0:i1 + 1]
new = l.replace(fm, '(`KismetMathLibrary.SelectFloat` (.pitch (`self.WorkRot`)) %s (>= (`self.OvW`) 0.99))' % fm)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': new}]})
out['edit'] = str(r2)[:1500] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200]
print('CAMAIM', json.dumps(out)[:2000])
