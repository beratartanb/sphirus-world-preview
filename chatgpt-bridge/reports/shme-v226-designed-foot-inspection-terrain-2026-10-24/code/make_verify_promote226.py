"""make_verify_promote226.py: derives verify_prod226.py and promote226.py from the V2.25 jobs (offline python, no editor)."""
import ast, pathlib
R = pathlib.Path(__file__).resolve().parents[2]
src = (R / 'Tools/SHME_V225_20261023/verify_prod225.py').read_text(encoding='utf8')
old = "if out['pie'] or out['dirty']: bad.append('pie_or_dirty')"
new = r'''# ---- V2.26
EXP6 = dict({'Reversal226': False, 'StepEdgeOn': False, 'InspectZoomOn': False, 'Probes': True}, **getattr(_b, 'V226_EXP', {}))
want6b = 'PSD_SHM226_JogRevBwd' if EXP6['Reversal226'] else want_bwd; want6f = 'PSD_SHM226_JogRevFwd' if EXP6['Reversal226'] else want_fwd
for m, nm in (('SHM224_DB_JRBwd', want6b), ('SHM224_DB_JRFwd', want6f)):
    v = ac.get_editor_property(m); out['abp'][m + '_226'] = v.get_name() if v else None
    if not v or v.get_name() != nm: bad.append('abp226.' + m)
for k in ('StepEdgeOn', 'InspectZoomOn'):
    try: xv = sda.get_editor_property(k); out['shm'][k] = xv
    except Exception: xv = None; bad.append('shm226.missing.' + k)
    if xv is not None and bool(xv) != EXP6[k]: bad.append('shm226.' + k)
try: out['shm']['InspectTag'] = str(sda.get_editor_property('InspectTag')); out['shm']['InspectJump'] = sda.get_editor_property('InspectJump')
except Exception: bad.append('shm226.inspecttag')
if out['shm'].get('InspectTag') != 'GR_Inspect': bad.append('shm226.inspecttag.value')
snn6 = [tid(pn(n)) for n in B.find_nodes(graph(abp, 'SHM_Snapshot'))]
if not any('SetSHM226_ShiftL' in t for t in snn6): bad.append('snapshot.shift')
fk6 = [n for n in B.find_nodes(graph(abp, 'FeetIK_Layer')) if n.get_class().get_name() == 'AnimGraphNode_ModifyBone' and 'BCS_WorldSpace' in n.get_editor_property('node').export_text()]
out['abp']['shift_nodes'] = len(fk6)
if len(fk6) != 2: bad.append('feetik.shift')
bt6 = [tid(pn(n)) for n in B.find_nodes(graph(comp, 'SHM_UpdateBodyTargets'))]
if not any('SetSwingShiftL' in t for t in bt6): bad.append('comp.swingshift')
cv6 = [tid(pn(n)) for n in B.find_nodes(graph(comp, 'SHM_UpdateCameraV21'))]
if not any('ActorHasTag' in t for t in cv6) or not any('GetActorBounds' in t for t in cv6): bad.append('comp.inspect.contract')
if not any('SetInspectHitName' in t for t in cv6): bad.append('comp.inspect.telemetry')
V6 = '/Game/GraceRanger/SHME/Animations/V226/'
for dbn, fam in ((V6 + 'PSD_SHM226_JogRevBwd', 'B_F'), (V6 + 'PSD_SHM226_JogRevFwd', 'F_B')):
    d_ = u.load_asset(dbn)
    if not d_: bad.append('missing.' + dbn.rsplit('/', 1)[-1]); continue
    ents = [d_.get_animation_asset(i).get_name() for i in range(d_.get_num_animation_assets())]
    piv = [e for e in ents if 'JogRev_' + fam in e]
    if len(piv) != 32 or any('Pivot' in e for e in ents) or 'A_RB_Jog_Rear' not in ents: bad.append('db226.' + dbn.rsplit('/', 1)[-1])
    out.setdefault('db226', {})[dbn.rsplit('/', 1)[-1]] = len(ents)
    s0 = u.load_asset(V6 + 'SHM226_JogRev_%s_P0' % fam)
    cur = [str(c) for c in u.AnimationLibrary.get_animation_curve_names(s0, u.RawCurveTrackTypes.RCT_FLOAT)] if s0 else []
    out.setdefault('curves226', {})[fam] = cur
    if 'footspeed_l' not in cur or 'footspeed_r' not in cur: bad.append('curves226.' + fam)
for dbn in ('/Game/GraceRanger/Animations/CorePerformance/PSD_CP2_JogPivots', '/Game/GraceRanger/SHME/Animations/Redirect/PSD_SHM_Redirect_JogReversalQ', '/Game/GraceRanger/SHME/Animations/V224/PSD_SHM224_JogRevBwdO', '/Game/GraceRanger/SHME/Animations/V225/PSD_SHM225_JogRevBwd'):
    d_ = u.load_asset(dbn)
    if not d_: continue
    ents = [d_.get_animation_asset(i).get_name() for i in range(d_.get_num_animation_assets())]
    if any(e.startswith('SHM226_') for e in ents): bad.append('db_leak226.' + dbn.rsplit('/', 1)[-1])
try:   # house targets: tag + query probe on the four R05 masks (editor world)
    acts = {a.get_actor_label(): a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()}
    masks = {}
    for nm in ('R05_Workshop_Mask_Silent', 'R05_Workshop_Mask_Gilded', 'R05_Workshop_Mask_Cerulean', 'R05_Workshop_Mask_Cracked'):
        a = acts.get(nm)
        if not a: masks[nm] = 'missing'; bad.append('mask.missing.' + nm); continue
        probes = [c for c in a.get_components_by_class(u.SphereComponent) if 'GR_Inspect' in [str(t) for t in c.component_tags]]
        masks[nm] = {'tag': 'GR_Inspect' in [str(t) for t in a.tags], 'probes': len(probes)}
        if not masks[nm]['tag']: bad.append('mask.tag.' + nm)
        if EXP6['Probes'] and len(probes) != 1: bad.append('mask.probe.' + nm)
    out['masks'] = masks
except Exception as e: out['masks'] = 'ERR ' + str(e)[:100]
if out['pie'] or out['dirty']: bad.append('pie_or_dirty')'''
assert src.count(old) == 1; src = src.replace(old, new)
src = src.replace("print('VERIFY225 ' + json.dumps(out, default=str))", "print('VERIFY226 ' + json.dumps(out, default=str))")
src = src.replace('"""verify_prod225.py (read-only editor job): V2.25 production state', '"""verify_prod226.py (read-only editor job): V2.26 production state (V2.25 checks + V2.26 via builtins.V226_EXP: Reversal226 (32-bin DBs), StepEdgeOn, InspectZoomOn, InspectTag, Snapshot SHM226_ShiftL, 2 world-space shift ModifyBones, SwingShift in BodyTargets, tag + bounds contract and hit telemetry in CameraV21, V226 DBs 32+4 without pivots, footspeed curves on the clips, no SHM226 leak, mask tags + probes). Base: V2.25 production state', 1)
(R / 'Tools/SHME_V226_20261024/verify_prod226.py').write_text(src, encoding='utf8'); ast.parse(src)
p = (R / 'Tools/SHME_V225_20261023/promote225.py').read_text(encoding='utf8')
p = p.replace("V5 = '/Game/GraceRanger/SHME/Animations/V225/'", "V5 = '/Game/GraceRanger/SHME/Animations/V225/'; V6 = '/Game/GraceRanger/SHME/Animations/V226/'")
old_p = "if 'Reversal' in D:\n"
new_p = ("if 'Reversal226' in D and D['Reversal226']:   # V2.26: the 32-bin clips\n"
         "    tgt = {'SHM224_DB_JRBwd': V6 + 'PSD_SHM226_JogRevBwd', 'SHM224_DB_JRBwdM': V6 + 'PSD_SHM226_JogRevBwd', 'SHM224_DB_JRFwd': V6 + 'PSD_SHM226_JogRevFwd', 'SHM224_DB_JRFwdM': V6 + 'PSD_SHM226_JogRevFwd'}\n"
         "    for v, pth in tgt.items():\n        a = u.load_asset(pth); assert a, pth; set_defaults(abp, {v: a})\n"
         "if 'Reversal' in D:\n")
assert p.count(old_p) == 1; p = p.replace(old_p, new_p)
p = p.replace("for k, dk in (('StepPrepEnabled', 'StepPrep'), ('CamInspectEnabled', 'Inspect')):", "for k, dk in (('StepPrepEnabled', 'StepPrep'), ('CamInspectEnabled', 'Inspect'), ('StepEdgeOn', 'StepEdge'), ('InspectZoomOn', 'InspectZoom')):")
p = p.replace("for k in ('StepPrepEnabled', 'CamInspectEnabled', 'SwingLiftEnabled', 'CamFollowEnabled')}", "for k in ('StepPrepEnabled', 'CamInspectEnabled', 'SwingLiftEnabled', 'CamFollowEnabled', 'StepEdgeOn', 'InspectZoomOn')}")
p = p.replace("ok = 'UP_TO_DATE' in str(st) and not errs and ('Reversal' not in D or", "ok = 'UP_TO_DATE' in str(st) and not errs and ('Reversal226' not in D or not D['Reversal226'] or a['SHM224_DB_JRBwd'] == 'PSD_SHM226_JogRevBwd') and ('Reversal' not in D or")
p = p.replace("print('PROMO225 '", "print('PROMO226 '").replace('"""promote225.py (editor job): V2.25 production.', '"""promote226.py (editor job): V2.26 production (V2.25 keys + Reversal226 = the 32-bin databases, StepEdge, InspectZoom).')
(R / 'Tools/SHME_V226_20261024/promote226.py').write_text(p, encoding='utf8'); ast.parse(p)
print('verify_prod226 + promote226 written')
