"""fix_v232_lasthitby.py (editor job, editor closed to PIE): V2.32 repair - the cinematic-orbit block in BP_SHM_HumanMotionComponent
SHM_UpdateCameraV21 reads the control rotation through (Piyon|GetControlRotation :self OwnerChar); the DSL translator resolved the
Controller version and bridged Pawn -> Controller through Pawn.LastHitBy (always None): every frame 3 'Accessed None LastHitBy' errors
(Set CamOrbitTarget / LookT / PrevCtl) and the control yaw read as 0 -> the orbit was driven by the body yaw against WORLD X, not against
the player's view, and the look-priority gate never fired (invisible in harness runs with yaw0 = 0). Same bug as V2.21 (MontTick).
Fix = the V2.21 repair (every GetLastHitBy -> Pawn::GetController, same self) on every component graph that holds one; reports any
GetLastHitBy left in BP_GR_Player / the ABP. builtins.V232_LHB_SAVE saves. Prints LHB232 {...}."""
import builtins, json
_lhb = {'__name__': 'lhb_lib'}
exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V221_20261021/fix_v221_lasthitby.py', encoding='utf8').read(), _lhb)
u = _lhb['u']; B = _lhb['B']; graph = _lhb['graph']; pn = _lhb['pn']; tid = _lhb['tid']
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
def scan(bp):
    hits = {}
    for g in B.list_graphs(bp):
        gname = g.get_name() if hasattr(g, 'get_name') else str(g)
        try:
            # LINKED GetLastHitBy only: the V2.21 patch rewires the consumers and leaves the old getter unconnected
            k = sum(1 for n in B.find_nodes(graph(bp, gname)) if tid(pn(n)).endswith('|GetLastHitBy') and any(o.connected_pins for o in _lhb['info'](pn(n)).output_pins))
            if k: hits[gname] = k
        except Exception: pass
    return hits
CP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent'
comp = u.load_asset(CP)
out = {'before': scan(comp)}
out['patched'] = _lhb['patch'](comp, list(out['before']))
out['after'] = scan(comp)
st, errs = _lhb['compile_ok'](comp); out.update({'status': str(st), 'nerr': len(errs)})
out['others'] = {p.rsplit('/', 1)[-1]: scan(u.load_asset(p)) for p in ('/Game/GraceRanger/BP_GR_Player', '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase')}
if getattr(builtins, 'V232_LHB_SAVE', False) and 'UP_TO_DATE' in str(st) and not errs and not out['after']:
    out['saved'] = bool(u.EditorAssetLibrary.save_loaded_asset(comp, False))
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('LHB232 ' + json.dumps(out, default=str))
