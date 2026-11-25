# hk_arm4.py (prelude, after the round-9 hook line): logs world transforms of the bones in builtins.B4_BONES of the visible body
# (Manny) every frame -> row.hook.bt = {bone: [x, y, z, qx, qy, qz, qw]}; also the garment mesh names on Henley / Shorts.
import builtins, unreal as _u4
_b4base = builtins.VID_TICKHOOK; _b4 = {'m': None}
def _b4hook(pw, ai, st, w_):
    o = _b4base(pw, ai, st, w_)
    try:
        if _b4['m'] is None:
            cs = {c.get_name(): c for c in pw.get_components_by_class(_u4.SkeletalMeshComponent)}
            _b4['m'] = cs.get('Manny'); _b4['g'] = [str(cs[n].get_skeletal_mesh_asset().get_name()) if n in cs and cs[n].get_skeletal_mesh_asset() else None for n in ('Henley', 'Shorts', 'Manny')]
        m = _b4['m']; bt = {}
        for b in builtins.B4_BONES:
            t = m.get_socket_transform(b, _u4.RelativeTransformSpace.RTS_WORLD); p = t.translation; q = t.rotation
            bt[b] = [round(p.x, 3), round(p.y, 3), round(p.z, 3), round(q.x, 5), round(q.y, 5), round(q.z, 5), round(q.w, 5)]
        o['bt'] = bt; o['gm'] = _b4['g']
    except Exception as e: o['bterr'] = repr(e)[:160]
    return o
builtins.VID_TICKHOOK = _b4hook
