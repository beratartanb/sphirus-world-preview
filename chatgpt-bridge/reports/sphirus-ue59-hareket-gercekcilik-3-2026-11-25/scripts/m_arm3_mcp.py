# m_arm3_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Posture; re-appliable) - movement realism pass 3.
# ARM / SHORTS. Measured on the visible body: the arm bones are NOT long (upper arm 0.154, forearm 0.142 of stature; wrist at 0.53 of
# stature) - the wrist passes 0.5 cm from the thigh axis surface in the walk (22 % of frames closer than 3 cm), -1.5 cm in stops.
# The posture layer servoes each arm to one mean abduction angle; it does not know where the thigh is.
# Now each arm's target abduction gets a clearance term: wrist distance to the same-side thigh axis (hip joint -> knee, radius CA_Rad);
# when it is below CA_Tgt the target opens by (CA_Tgt - clearance) x CA_K degrees (max CA_Max), fast in, slow out (peak hold over the
# stride), so the arm opens only as far as that gait needs and keeps its swing. PS_AbdBack adds abduction while moving backwards
# (CM jog-back clip: wrists 20 cm apart in front of the pelvis).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}})); ch = False
for n in ('CA_On', 'CA_Tgt', 'CA_K', 'CA_Max', 'CA_Fall', 'CA_Rise', 'CA_Rad', 'CA_L', 'CA_R', 'CA_CL', 'CA_CR', 'PS_AbdBack'):
    if '"%s"' % n not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True}); ch = True
if ch: T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`self.CA_L`' in dsl: print('ARM3 already'); sys.exit(0)
L = dsl.split(NL); i0 = [i for i, x in enumerate(L) if x.startswith('(event `GR_Posture`')][0]; i1 = [i for i, x in enumerate(L) if i > i0 and x.startswith('(event ')][0]; ev = L[i0:i1]
def one(p):
    m = [x for x in ev if x.startswith(p)]; assert len(m) == 1, (p, len(m)); return m[0]
S = lambda b: '(`SceneComponent.GetSocketLocation` (`self.Manny`) "%s")' % b
edits = []; pre = []
for f, h, meas in (('L', '_returnvalue_13', '_returnvalue_26'), ('R', '_returnvalue_14', '_returnvalue_27')):
    s = f.lower(); clear = '(- (%s (- %s (%s %s %s %s))) %s)' % (K % 'VSize', h, K % 'FindClosestPointOnSegment', h, S('thigh_' + s), S('calf_' + s), V('CA_Rad'))
    pre.append('  (set `self.CA_C%s` %s)' % (f, clear))
    des = '(%s (* (* (- %s %s) %s) %s) 0.0 %s)' % (K % 'FClamp', V('CA_Tgt'), V('CA_C' + f), V('CA_K'), V('CA_On'), V('CA_Max'))
    pre.append('  (set `self.CA_%s` (%s %s %s %s (%s %s %s (> %s %s))))' % (f, K % 'FInterpTo_Constant', V('CA_' + f), des, V('GR_PDt'), K % 'SelectFloat', V('CA_Rise'), V('CA_Fall'), des, V('CA_' + f)))
    l = one('  (set `self.PS_DA%s` ' % f); a = '(- _returnvalue_43 %s)' % meas; assert l.count(a) == 2, l.count(a)
    tgt = '(- (+ (+ _returnvalue_43 %s) (%s %s 0.0 (and %s (> _returnvalue_17 60.0)))) %s)' % (V('CA_' + f), K % 'SelectFloat', V('PS_AbdBack'), V('GR_Back'), meas)
    b = '(* %s %s)) 6.0)' % (V('CT_TuckNow'), V('CT_Graze')); assert l.count(b) == 1, b
    edits.append({'oldString': l, 'newString': l.replace(a, tgt).replace(b, b.replace(' 6.0)', ' (+ 6.0 (+ %s %s)))' % (V('CA_' + f), V('PS_AbdBack'))))})
la = one('  (set `self.PS_AbdL` '); edits.append({'oldString': la, 'newString': NL.join(pre) + NL + la})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('ARM3', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:160])
