# m_cam3_mcp.py (MCP, in-memory; AC_Sph_Camera; re-appliable) - movement realism pass 3.
# RUNNING CAMERA. The component already owns the speed terms (SpeedArm, FovRun, acceleration kick, ReduceMotion). Running LENGTHENED the
# arm (+4 cm) and the field of view rose by FovRun for run and sprint alike (saturated at 450 cm/s). Added a sprint band (450 -> 585 cm/s):
# FovSpr (field of view, scaled by DynFovScale and ReduceMotion like FovRun) and SprArm (arm length). The run values themselves are
# defaults (c_mr3_defaults): SpeedArm 4 -> -14 (closer to the shoulder), SprArm -4, FovSpr 3.5. No new shake, no roll, no blur.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
MA = '/Game/Sphirus/Player/Camera/AC_Sph_Camera'; BP = MA + '.AC_Sph_Camera'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}})); ch = False
for n in ('FovSpr', 'SprArm'):
    if '"%s"' % n not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True}); ch = True
if ch: T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': MA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`self.FovSpr`' in dsl: print('CAM3 already'); sys.exit(0)
L = dsl.split(NL)
def one(p):
    m = [x for x in L if x.startswith(p)]; assert len(m) == 1, (p, len(m)); return m[0]
lf = one('    (set `self.Fov` '); ld = one('    (set `self.D` '); mr = lambda a, b: '(%s _returnvalue_6 %s %s 0.0 1.0)' % (K % 'MapRangeClamped', a, b)
a = '(* %s %s)' % (mr('200.0', '450.0'), V('FovRun')); assert lf.count(a) == 1, lf.count(a)
b = '(* %s %s)' % (mr('200.0', '450.0'), V('SpeedArm')); assert ld.count(b) == 1, ld.count(b)
edits = [{'oldString': lf, 'newString': lf.replace(a, '(+ (* %s %s) (* %s %s))' % (mr('200.0', '450.0'), V('FovRun'), mr('450.0', '585.0'), V('FovSpr')))},
         {'oldString': ld, 'newString': ld.replace(b, '(+ (* %s %s) (* %s %s))' % (mr('200.0', '450.0'), V('SpeedArm'), mr('450.0', '585.0'), V('SprArm')))}]
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': MA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('CAM3', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:160])
