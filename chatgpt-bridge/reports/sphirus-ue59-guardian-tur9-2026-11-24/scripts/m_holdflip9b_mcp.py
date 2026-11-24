# m_holdflip9b_mcp.py (MCP, in-memory; BP_Sph_GASPCharacter; after m_holdflip9) - round 9: the hold only skips the ACCELERATION opening.
# The friction opening on the command frame existed before round 9 (speed > 480) and is needed for the sprint -> back choice:
# measured on old_U_B 30 Hz: accel open + low friction -> wrong pivot; normal accel + full friction -> wrong pivot;
# normal accel + low friction (round 8 behaviour) -> transition clip, then the pivot at release.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
GA = '/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'; NL = chr(10); M = '`/Game/Sphirus/Player/Motion/AC_Sph_Motion.%s` (`self.SphMotion`)'
OPP = '(< (`KismetMathLibrary.Dot_VectorVector` (`KismetMathLibrary.Vector_Normal2D` (`self.GetPendingMovementInputVector`)) (`KismetMathLibrary.Vector_Normal2D` (`MovementComponent.Velocity` (`self.CharacterMovement`)))) -0.7)'
W = '(and %s (< (%s) 0.5))' % (OPP, M % 'RcNoFlip')
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': GA, 'scope': 'CalculateGroundFriction'}); rv = r['content']['returnValue']; l = [x for x in rv['dsl'].split(NL) if x.strip().startswith('(return ')][0]
if W not in l: print('HOLDFLIP9B already'); sys.exit(0)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': GA, 'revision': rv['revision'], 'scope': 'CalculateGroundFriction', 'edits': [{'oldString': l, 'newString': l.replace(W, OPP)}]})
print('HOLDFLIP9B', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1200], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': GA + '.BP_Sph_GASPCharacter'}, 'bWarningsAsErrors': False}))[:90])
