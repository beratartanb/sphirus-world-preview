# m_holdflip9_mcp.py (MCP, in-memory; AC_Sph_Motion + BP_HybridA_Player + BP_Sph_GASPCharacter; re-appliable) - round 9.
# Regression found on the saved round-9 state: the flip-frame opening (m_flip9, made for quick A/D) also fired on the frame a BACK command
# arrives at sprint. Motion Matching then entered CM_af_Loco_Jog_Bwd_Pivot for one frame before the back-input hold (GR_StopHold) took
# over, and at the hold's release it chose the back START clip instead of the PIVOT (30 Hz slide 2.2 -> 16 cm, the round-8 fork again).
# A/B on the same plan: flip opening neutral -> pivot, 2.2 cm. Now the player publishes the hold (AC.RcNoFlip) and the flip opening is
# skipped while it holds. Quick A/D is lateral to the camera and never uses the hold, so it keeps the opening.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
MA = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; MB = MA + '.AC_Sph_Motion'; GA = '/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'; GB = GA + '.BP_Sph_GASPCharacter'
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; PB = PA + '.BP_HybridA_Player'; NL = chr(10); out = {}
M = '`/Game/Sphirus/Player/Motion/AC_Sph_Motion.%s` (`self.SphMotion`)'; ok = lambda r: 'ok' if not (isinstance(r, dict) and r.get('isError')) else str(r)[:1200]
if '"RcNoFlip"' not in json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': MB}})):
    out['add'] = str(T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': MB}, 'name': 'RcNoFlip', 'typeName': 'float'}))[:120]
    T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': MB}, 'bWarningsAsErrors': False})
# player: publish the hold right after it is computed
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if 'AC_Sph_Motion.RcNoFlip`' in dsl: out['player'] = 'already'
else:
    l = [x for x in dsl.split(NL) if x.strip().startswith('(set `self.GR_StopHold` ')]; assert len(l) == 1, len(l); l = l[0]; ind = l[:len(l) - len(l.lstrip())]
    new = l + NL + ind + '(set `/Game/Sphirus/Player/Motion/AC_Sph_Motion.RcNoFlip` (`KismetMathLibrary.SelectFloat` 1.0 0.0 (`self.GR_StopHold`)) (`self.SphMotion`))'
    out['player'] = ok(T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': new}]}))
out['compP'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': PB}, 'bWarningsAsErrors': False}))[:90]
OPP = '(< (`KismetMathLibrary.Dot_VectorVector` (`KismetMathLibrary.Vector_Normal2D` (`self.GetPendingMovementInputVector`)) (`KismetMathLibrary.Vector_Normal2D` (`MovementComponent.Velocity` (`self.CharacterMovement`)))) -0.7)'
for sc in ('CalculateMaxAcceleration', 'CalculateGroundFriction'):
    r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': GA, 'scope': sc}); rv = r['content']['returnValue']; dsl = rv['dsl']
    l = [x for x in dsl.split(NL) if x.strip().startswith('(return ')]; assert len(l) == 1; l = l[0]
    if 'RcNoFlip' in l: out[sc] = 'already'
    elif l.count(OPP) != 1: out[sc] = 'PATTERN? %d' % l.count(OPP)
    else: out[sc] = ok(T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': GA, 'revision': rv['revision'], 'scope': sc, 'edits': [{'oldString': l, 'newString': l.replace(OPP, '(and %s (< (%s) 0.5))' % (OPP, M % 'RcNoFlip'))}]}))
out['compG'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': GB}, 'bWarningsAsErrors': False}))[:90]
print('HOLDFLIP9', json.dumps(out))
