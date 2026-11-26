# m_jump8_mcp.py (MCP, in-memory): the jump input starts neither a traversal nor a jump while she is down (FL_State) or hanging on a ledge
# (LG_State; there the jump only means "climb up", read by the ledge block). Crouched was already excluded; the input is not buffered
# (Started only), so no jump fires later after standing up.
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10)
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; L = rv['dsl'].split(NL)
OLD = '(and (not (`self.GR_Load2H`)) (not (`self.bIsCrouched`)))'
NEW = '(and (and (not (`self.GR_Load2H`)) (not (`self.bIsCrouched`))) (and (< (`self.FL_State`) 0.5) (< (`self.LG_State`) 0.5)))'
j = [i for i, x in enumerate(L) if x.startswith('(event `EnhancedInput|/Game/Sphirus/Player/Input/IA_Sph_Jump`')][0]
e = j + 1
while e < len(L) and not L[e].startswith('(event'): e += 1
hits = [i for i in range(j, e) if L[i].lstrip().startswith('(if (and ' + OLD)]
if not hits: print('JUMP8 already' if NEW in NL.join(L[j:e]) else 'JUMP8 anchor missing'); sys.exit()
edits = [{'oldString': L[i], 'newString': L[i].replace(OLD, NEW, 1)} for i in hits]
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('JUMP8', len(edits), 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2000], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
