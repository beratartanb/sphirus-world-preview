"""verify231.py (fresh editor, read-only): every earlier contract (verify230 = V2.29 groups + V2.30 knobs / markers / null-safe probe) plus V2.31:
the promoted knob values (builtins.V231_EXP = {group: True}), the V2.31 graph markers, the inspection resolver (function present, called in
SHM_Tick right after the camera function, the camera function reads its outputs, no member call on the hit in the DSL), the curved sprint
loops at rate_scale 1.0, the slow / loaded databases present. V2.30's 'candidate on' item is re-evaluated here (LoadedOn is a V2.31 group).
Prints VERIFY231 {... ALL_OK}."""
import builtins, json
X = dict(getattr(builtins, 'V231_EXP', {}))
builtins.V230_EXP = {'lowrev': True, 'idleguard': True}
g = {'__name__': 'v230'}
exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V230_20261026/verify230.py', encoding='utf8').read(), g)
import unreal as u
bad = [b for b in g.get('bad', []) if not b.startswith('candidate on')]
# V2.28 inspection contract (InspectFocusMode 1 = actor location) is superseded by the V2.31 resolver (InspectFocusMode 2 = owner root mesh
# bounds behind IsValid); the V2.31 value is checked below
if X.get('inspect'): bad = [b for b in bad if not b.startswith('InspectFocusMode=')]
k30 = g.get('k', {})
if k30.get('SHM230_FamGate') or k30.get('StepPrepEnabled') or (k30.get('SHM230_LoadedOn') and not X.get('loaded')) or (X.get('loaded') and not k30.get('SHM230_LoadedOn')): bad.append('candidate/loaded %s' % k30)
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); cdo = u.get_default_object(bp.generated_class()); sda = u.load_asset('/Game/GraceRanger/SHME/DA_SHM_Response_Default')
B = g['B']; graph = g['graph']; pn = g['pn']; tid = g['tid']
k = {}
for name, grp, on, off, src in (('SHM231_SlowOn', 'slow', 1.0, 0.0, 'abp'), ('SHM231_ExitAuth', 'exit', 1.0, 0.0, 'abp'), ('SHM231_TipEndHold', 'tipend', 1.0, 0.0, 'abp'),
                                 ('RedirectLowRevFwdMax', 'fwdrev', 330.0, 0.0, 'da'), ('SwingLiftBaseComp', 'steplift', 1.0, 0.0, 'da')):
    try: val = float((cdo if src == 'abp' else sda).get_editor_property(name))
    except Exception as e: bad.append('missing %s %s' % (name, e)); continue
    k[name] = val
    if abs(val - (on if X.get(grp) else off)) > 1e-6: bad.append('%s=%s (group %s %s)' % (name, val, grp, bool(X.get(grp))))
k['InspectFocusMode'] = float(sda.get_editor_property('InspectFocusMode'))
if X.get('inspect') and abs(k['InspectFocusMode'] - 2.0) > 1e-6: bad.append('InspectFocusMode %s' % k['InspectFocusMode'])
if X.get('loaded'):
    for n, want in (('SHM230_DB_JRFwdL', 'PSD_SHM231L_LoadRevFwd'), ('SHM230_DB_JRBwdL', 'PSD_SHM226_JogRevBwd')):
        v = cdo.get_editor_property(n); k[n] = v.get_name() if v else None
        if k[n] != want: bad.append('%s=%s' % (n, k[n]))
vlist = [str(v) for v in B.list_variables(bp)]
for m in ('SHM231_SRFix', 'SHM231_SRFixB', 'SHM231_EPFix', 'SHM231_EPFixB', 'SHM231_TEFix'):
    if m not in vlist: bad.append('marker ' + m)
comp = u.load_asset('/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent')
res = graph(comp, 'SHM231_InspectResolve'); tick = graph(comp, 'SHM_Tick')
rt = [tid(pn(n)) for n in B.find_nodes(res)] if res else []
tt = [tid(pn(n)) for n in B.find_nodes(tick)] if tick else []
cv = [tid(pn(n)) for n in B.find_nodes(graph(comp, 'SHM_UpdateCameraV21'))]
ins = {'resolver': bool(res), 'resolver_isvalid': sum('IsValid' in t for t in rt), 'resolver_tags': any('ComponentHasTag' in t for t in rt) and any('ActorHasTag' in t for t in rt),
       'tick_call': any(t.split('|')[-1] == 'SHM231_InspectResolve' for t in tt), 'cam_reads_insfocus': any('SHM231_InsFocus' in t for t in cv), 'cam_sets_inshit': any('SetSHM231_InsHit' in t for t in cv),
       'cam_member_tag_calls': any(('ActorHasTag' in t or 'ComponentHasTag' in t or 'GetActorBounds' in t) for t in cv)}
if not (ins['resolver'] and ins['resolver_isvalid'] >= 2 and ins['resolver_tags'] and ins['tick_call'] and ins['cam_reads_insfocus'] and ins['cam_sets_inshit']) or ins['cam_member_tag_calls']: bad.append('inspect231 %s' % ins)
rates = {}
for t in ('R12', 'L12', 'R25', 'L25', 'R40', 'L40'):
    s = u.load_asset('/Game/GraceRanger/SHME/Animations/Curves/A_SHM_Sprint_Curve_' + t); rates[t] = round(float(s.get_editor_property('rate_scale')), 3)
    if abs(rates[t] - 1.0) > 1e-3: bad.append('curve rate %s %s' % (t, rates[t]))
dbs = {n: u.EditorAssetLibrary.does_asset_exist('/Game/GraceRanger/SHME/Animations/V231/' + n) for n in ('PSD_SHM231S_SlowRevBwd', 'PSD_SHM231S_SlowRevFwd', 'PSD_SHM231L_LoadRevFwd')}
if not all(dbs.values()): bad.append('dbs %s' % dbs)
print('VERIFY231 ' + json.dumps({'v230_bad_raw': g.get('bad', []), 'knobs': k, 'inspect231': ins, 'curve_rates': rates, 'dbs': dbs, 'bad': bad, 'ALL_OK': not bad}, default=str))
