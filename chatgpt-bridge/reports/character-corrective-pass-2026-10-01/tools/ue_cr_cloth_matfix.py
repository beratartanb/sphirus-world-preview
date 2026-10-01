"""CORRECTIVE pass fix: the cloth build assigned the main fabric MI to every render section of the Chaos shorts (trims + drawstring
rendered as fabric). Set the cloth asset's material list to the per-section clothing MIs (section order = skeletal mesh slot order).
builtins.CR_MATFIX = {'ca': path, 'mats': [(slot, MI path), ...]}"""
import unreal as u, json, builtins
C = builtins.CR_MATFIX; EAL = u.EditorAssetLibrary; ca = u.load_asset(C['ca']); new = []
for slot, mp in C['mats']:
    sm = u.SkeletalMaterial(); sm.set_editor_property('material_interface', u.load_asset(mp)); sm.set_editor_property('material_slot_name', slot); new.append(sm)
before = [m.get_editor_property('material_interface').get_name() for m in ca.get_editor_property('materials')]
ca.set_editor_property('materials', new); ok = EAL.save_loaded_asset(ca, False)
after = [m.get_editor_property('material_interface').get_name() for m in u.load_asset(C['ca']).get_editor_property('materials')]
print('CR_MATFIX', json.dumps({'before': before, 'after': after, 'saved': ok, 'dirty': [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}))
