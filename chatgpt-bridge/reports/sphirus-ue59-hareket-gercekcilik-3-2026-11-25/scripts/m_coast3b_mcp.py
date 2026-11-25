# m_coast3b_mcp.py (MCP, in-memory; after m_coast3; re-appliable) - movement realism pass 3.
# The coast of m_coast3 braked at only ~170 cm/s2: above the speed limit the capsule deceleration is bound to the playing clip
# (DmDecel, clamp DmMin..DmMax) and the run -> walk transition clip keeps being re-entered. While coasting the player now publishes a
# floor for that deceleration (AC_Sph_Motion.DmCoastDec = CS_Dec, 0 otherwise): braking steps are a firm, speed-proportional brake.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
def addvars(BP, names, typ='float'):
    have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}})); ch = False
    for n in names:
        if '"%s"' % n not in have:
            T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': typ}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True}); ch = True
    if ch: T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
def edit(AP, tag, mk):
    r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
    e = mk(dsl)
    if e is None: print(tag, 'already'); return
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': e})
    print(tag, 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': AP + '.' + AP.split('/')[-1]}, 'bWarningsAsErrors': False}))[:160])
def one(dsl, pfx):
    m = [x for x in dsl.split(NL) if x.startswith(pfx)]; assert len(m) == 1, (pfx, len(m)); return m[0]
MA = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; addvars(MA + '.AC_Sph_Motion', ['DmCoastDec'])
def mk_m(dsl):
    if '`self.DmCoastDec`' in dsl: return None
    l = one(dsl, '  (set `self.DmDecel` '); a = '%s %s)' % (V('DmMin'), V('DmMax')); assert l.count(a) == 1
    return [{'oldString': l, 'newString': l.replace(a, '(%s %s %s) (%s %s %s))' % (K % 'FMax', V('DmMin'), V('DmCoastDec'), K % 'FMax', V('DmMax'), V('DmCoastDec')))}]
edit(MA, 'COAST3B motion', mk_m)
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; addvars(PA + '.BP_HybridA_Player', ['CS_Dec'])
def mk_p(dsl):
    if '`self.CS_Dec`' in dsl: return None
    l = one(dsl, '  (set `/Game/Sphirus/Player/Motion/AC_Sph_Motion.DmBoostAdd` ')
    return [{'oldString': l, 'newString': l + NL + '  (set `/Game/Sphirus/Player/Motion/AC_Sph_Motion.DmCoastDec` (%s %s 0.0 %s) (`self.SphMotion`))' % (K % 'SelectFloat', V('CS_Dec'), V('CS_Clear'))}]
edit(PA, 'COAST3B player', mk_p)
