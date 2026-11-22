# m_gov6d_mcp.py (MCP, in-memory; BP_Sph_GASPCharacter.CalculateGroundFriction) - round 6b.
# m_gov6c tested the reversal with GetCurrentAcceleration, but UpdateMovement_PreCMC runs BEFORE the movement component consumes this
# frame's input, so the acceleration was still last frame's (forward): the first reversal frame kept full friction and, being over the
# backward max speed, braked with friction x 2 x v + 500 (584 -> 413 cm/s in one 45 ms frame, f6_B_var t 15.27). Motion Matching then
# entered the turn clip 0.23 s before its plant from a pose ~50 cm behind it -> the "planted" foot travelled 58-76 cm (30 Hz: 28 cm).
# Now the test uses the PENDING movement input of this frame.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
GC = '/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': GC, 'scope': 'CalculateGroundFriction'}); rv = r['content']['returnValue']; d = rv['dsl']
A = '(`CharacterMovementComponent.GetCurrentAcceleration` (`self.CharacterMovement`))'; assert d.count(A) == 1, d.count(A)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': GC, 'revision': rv['revision'], 'scope': 'CalculateGroundFriction', 'edits': [{'oldString': A, 'newString': '(`self.GetPendingMovementInputVector`)'}]})
print('GOV6D', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': GC + '.BP_Sph_GASPCharacter'}, 'bWarningsAsErrors': False}))[:120])
