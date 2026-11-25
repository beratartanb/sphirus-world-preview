# m_p1b_mcp.py (MCP, in-memory; BP_HybridA_Player; re-appliable) - movement realism pass 3.
# (1) Walk -> brisk walk (tempo, 180 -> 278 cm/s) took 0.3 s: the gait step-up acceleration scale is now published by the player per
#     gait (AC_Sph_Motion.GaitUpAcc = GU_Tempo while the tempo gait is active, GU_Run otherwise).
# (2) CROUCH: the jump key did not check the crouch state. ACharacter refuses the jump while crouched but keeps bPressedJump while the
#     key is held, so the jump fired the moment she stood up, and the jump montage + forward launch played on the crouched body.
#     The key is now ignored while crouched (no Jump(), no montage, no pending launch): nothing is buffered.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}})); ch = False
for n in ('GU_Run', 'GU_Tempo'):
    if '"%s"' % n not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True}); ch = True
if ch: T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']; L = dsl.split(NL); edits = []
if '`self.GU_Tempo`' not in dsl:
    m = [x for x in L if x.startswith('  (set `self.GR_TempoAct` ')]; assert len(m) == 1
    edits.append({'oldString': m[0], 'newString': m[0] + NL + '  (set `/Game/Sphirus/Player/Motion/AC_Sph_Motion.GaitUpAcc` (%s %s %s %s) (`self.SphMotion`))' % (K % 'SelectFloat', V('GU_Tempo'), V('GU_Run'), V('GR_TempoAct'))})
j0 = [i for i, x in enumerate(L) if x.startswith('(event `EnhancedInput|/Game/Sphirus/Player/Input/IA_Sph_Jump`')][0]
jl = [x for x in L[j0:j0 + 12] if x.strip() == '(if (not (`self.GR_Load2H`))']
if jl:
    assert dsl.count(jl[0] + NL + '      (set `CharacterMovementComponent.JumpZVelocity`') == 1
    edits.append({'oldString': jl[0] + NL + '      (set `CharacterMovementComponent.JumpZVelocity`', 'newString': '    (if (and (not (`self.GR_Load2H`)) (not (`self.bIsCrouched`)))' + NL + '      (set `CharacterMovementComponent.JumpZVelocity`'})
if not edits: print('P1B already'); sys.exit(0)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('P1B', len(edits), 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:160])
