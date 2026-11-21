# m_prompt_mcp.py (MCP, in-memory edit of BP_GR_DayStation + BP_GR_DayHub) - 2026-11-22 round 5.
# The Story Framework prompt of a station ("Uzan / Kalk" at the bed) stayed on screen for the whole station sequence, also while lying and
# during the fade to the next day. A station now hides its own prompt component when its sequence starts (hub busy) and shows it again
# when the sequence ends; the bed sequence ends in the hub (GR_Wake), which calls GR_PromptOn on every station.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
ST = '/Game/GraceRanger/SF/Day/BP_GR_DayStation'; HUB = '/Game/GraceRanger/SF/Day/BP_GR_DayHub'; out = {}; NL = chr(10)
def hide(b): return '(`SceneComponent.SetHiddenInGame` (`self.InteractionPromptLoc`) %s true)' % b
# ---- station ----
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': ST, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if 'GR_PromptOn' not in dsl:
    open('Saved/UE59Work/dsl/station_before_prompt.dsl', 'w', encoding='utf8').write(dsl)
    on = [l for l in dsl.split(NL) if l.strip() == '(set `%s.GR_Busy` true (`self.GR_Hub`))' % HUB]; assert len(on) == 1, len(on)
    off = [l for l in dsl.split(NL) if l.strip() == '(set `%s.GR_Busy` false (`self.GR_Hub`))' % HUB]; assert len(off) == 1, len(off)
    i1 = on[0][:len(on[0]) - len(on[0].lstrip())]; i2 = off[0][:len(off[0]) - len(off[0].lstrip())]
    ev = NL + NL + '(event `GR_PromptOn`' + NL + '  ' + hide('false') + ')'
    tail = dsl.rstrip(NL)
    i0 = tail.index('(event `GR_Swing`'); c = tail.find(NL + NL + '(', i0); blk = tail[i0:c] if c > 0 else tail[i0:]
    edits = [{'oldString': on[0], 'newString': on[0] + NL + i1 + hide('true')}, {'oldString': off[0], 'newString': i2 + hide('false') + NL + off[0]},
             {'oldString': blk[-240:], 'newString': blk[-240:] + ev}]
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': ST, 'revision': rv['revision'], 'scope': '', 'edits': edits})
    out['station_edit'] = str(r2)[:1800] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
    out['station_compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': ST + '.BP_GR_DayStation'}, 'bWarningsAsErrors': False}))[:200]
# ---- hub ----
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': HUB, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if 'GR_PromptOn' not in dsl:
    open('Saved/UE59Work/dsl/hub_before_prompt.dsl', 'w', encoding='utf8').write(dsl)
    off = [l for l in dsl.split(NL) if l.strip() == '(set `self.GR_Busy` false)']; assert len(off) == 1, len(off)
    ind = off[0][:len(off[0]) - len(off[0].lstrip())]
    loop = ind + '(bind _pst (`GameplayStatics.GetAllActorsOfClass` "%s.BP_GR_DayStation_C"))' % ST + NL + ind + '(for _pel _pst' + NL + ind + '  (bind _pas (cast `%s` _pel))' % ST + NL + ind + '  (`%s.GR_PromptOn` _pas))' % ST
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': HUB, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': off[0], 'newString': off[0] + NL + loop}]})
    out['hub_edit'] = str(r2)[:1800] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
    out['hub_compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': HUB + '.BP_GR_DayHub'}, 'bWarningsAsErrors': False}))[:200]
print('PROMPT', json.dumps(out)[:3000])
