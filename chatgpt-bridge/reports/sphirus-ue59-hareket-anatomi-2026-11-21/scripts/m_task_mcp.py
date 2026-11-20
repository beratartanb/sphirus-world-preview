# m_task_mcp.py (MCP, in-memory edit of BP_GR_DayHub; saved by a gated write job) - 2026-11-21 round 4.
# Task order: GR_Dressed (first outfit choice of the day) always added the fire task (GR_T2) and the tea task (GR_T3), also when
# the fire already burned / the tea was already drunk -> "Bitki topla ve cayi hazirla" came back after the wardrobe. Each task is
# now added only while its state is not finished (GR_Fire < 2, GR_Tea < 2).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
H = '/Game/GraceRanger/SF/Day/BP_GR_DayHub'; out = {}
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': H, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
open('Saved/UE59Work/dsl/hub_before_task.dsl', 'w', encoding='utf8').write(dsl)
NL = chr(10)
i0 = dsl.index('(event `GR_Dressed`'); i1 = dsl.find(NL + NL + '(event', i0); blk = dsl[i0:i1] if i1 > 0 else dsl[i0:]
L = blk.split(NL); t2 = [l for l in L if 'AddTask' in l and '`self.GR_T2`' in l]; t3 = [l for l in L if 'AddTask' in l and '`self.GR_T3`' in l]
assert len(t2) == 1 and len(t3) == 1, (len(t2), len(t3))
assert 'GR_Fire`) 2' not in blk, 'already built'
def wrap(line, var):
    ind = line[:len(line) - len(line.lstrip())]; body = line.strip(); tail = ''
    while body.endswith('))') and body.count('(') < body.count(')'): body = body[:-1]; tail += ')'
    return ind + '(if (< (`self.%s`) 2)' % var + NL + ind + '  ' + body + ')' + tail
edits = [{'oldString': t2[0], 'newString': wrap(t2[0], 'GR_Fire')}, {'oldString': t3[0], 'newString': wrap(t3[0], 'GR_Tea')}]
if '--dry' in sys.argv: print(edits[0]['newString'][-260:]); print(edits[1]['newString'][-260:]); sys.exit(0)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': H, 'revision': rv['revision'], 'scope': '', 'edits': edits})
out['edit'] = str(r2)[:1800] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': H + '.BP_GR_DayHub'}, 'bWarningsAsErrors': False}))[:200]
print('TASK', json.dumps(out)[:2400])
