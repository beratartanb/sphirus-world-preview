"""CORRECTIVE pass: cloth collision physics assets (copies of the body PA in CharacterCorrective_20261001/Cloth):
PHYS_CR_ShortsCollider  = body capsules (pelvis / thighs / spine) unchanged
PHYS_CR_HenleyCollider  = pelvis + spine_02 capsules inflated to the OUTER surface of the shorts waistband (garment-to-garment proxy:
                          the Henley hem rests / compresses on the band instead of passing through it)"""
import unreal as u, json
EAL = u.EditorAssetLibrary; F = '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Cloth'; SRC = '/Game/Sphirus/CharacterLab/ShoulderFix_20260928/Assembly/SHOULDER_FIX_NATIVE/Body/PHYS_MH_SHOULDER_FIX_NATIVE'
INFL = {'PHYS_CR_ShortsCollider': {}, 'PHYS_CR_HenleyCollider': {'pelvis': 2.6, 'spine_02': 1.6}}
out = {}
for name, infl in INFL.items():
    p = F+'/'+name
    if EAL.does_asset_exist(p): EAL.delete_asset(p)
    assert EAL.duplicate_asset(SRC, p); pa = u.load_asset(p); rep = {}
    for b in u.ObjectIterator(u.BodySetup):
        if b.get_outer() != pa: continue
        bn = str(b.get_editor_property('bone_name'))
        if bn in infl:
            import re
            t = b.get_editor_property('agg_geom').export_text(); t2 = re.sub(r'Radius=([0-9.]+)', lambda m: 'Radius=%.6f' % (float(m.group(1))+infl[bn]), t)
            g2 = u.KAggregateGeom(); assert g2.import_text(t2); b.modify(); b.set_editor_property('agg_geom', g2)   # whole-struct text import (element setters do not persist)
            rep[bn] = [round(s.get_editor_property('radius'), 2) for s in b.get_editor_property('agg_geom').get_editor_property('sphyl_elems')]
    pa.modify(); out[name] = {'saved': EAL.save_loaded_asset(pa, False), 'inflated': rep}
print('CR_COLLIDER', json.dumps(out))
