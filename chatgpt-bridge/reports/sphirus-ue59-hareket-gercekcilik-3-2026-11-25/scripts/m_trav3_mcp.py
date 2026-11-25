# m_trav3_mcp.py (MCP, in-memory; BP_HybridA_Player IA_Sph_Jump; re-appliable) - movement realism pass 3.
# CONTEXTUAL TRAVERSAL ENTRY. The player inherits AC_TraversalLogic + MotionWarping from the GASP base character (vault / hurdle /
# mantle on LevelBlock_Traversable actors, ledge transforms from the block, warped montages chosen by CHT_TraversalMontages), but the
# project's own jump key called Jump() directly, so the component was never asked. With TR_On > 0.5 the jump key first asks
# TryTraversalAction (inputs from the base class GetTraversalCheckInputs); only when the check finds nothing does the normal jump run.
# Player initiated only; never while crouched or carrying with two hands (same gate as the jump). TR_On 0 = previous behaviour.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"TR_On"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'TR_On', 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'TR_On', 'bInstanceEditable': True}); T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`self.TR_On`' in dsl: print('TRAV3 already'); sys.exit(0)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"TR_Fail"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'TR_Fail', 'typeName': 'bool'}); T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
    r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
g = '(and (not (`self.GR_Load2H`)) (not (`self.bIsCrouched`)))'; old = '    (if %s' % g + NL + '      (set `CharacterMovementComponent.JumpZVelocity`'; assert dsl.count(old) == 1, dsl.count(old)
new = NL.join(['    (set `self.TR_Fail` true)',
    '    (if (and %s (> %s 0.5))' % (g, V('TR_On')),
    '      (bind (_trfail _trmfail) (`/Game/Blueprints/AC_TraversalLogic.TryTraversalAction` (`self.AC_TraversalLogic`) (`self.GetTraversalCheckInputs`) "None"))',
    '      (set `self.TR_Fail` _trfail))',
    '    (if (and %s %s)' % (g, V('TR_Fail')),
    '      (set `CharacterMovementComponent.JumpZVelocity`'])
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': new}]})
print('TRAV3', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:3000], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300])
