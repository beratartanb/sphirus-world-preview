# c_hair_bun.py (write context; in memory, re-appliable): player hair = approved C49 h1 bun (main + loose strands) bound to the Sph8 face
# (GB_Sph8_HairMainH1 / GB_Sph8_HairLooseH1, transfer from GD38), with the current copper material MI_Sph_Hair as override.
# HairMain2 keeps its slot; a HairLoose2 GroomComponent is added under the same parent. builtins.HAIR_BOB = True -> back to the VF2 messy bob
# (HairLoose2 emptied and hidden).
import unreal as u, builtins
C = '/Game/Sphirus/CharacterLab/CharacterCohesion_C49_20261104/Hair/'; B = '/Game/Sphirus/CharacterLab/B13_20261126/Hair/'
bp = u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'); sub = u.get_engine_subsystem(u.SubobjectDataSubsystem); L = u.SubobjectDataBlueprintFunctionLibrary
def comps():
    out = {}
    for h in sub.k2_gather_subobject_data_for_blueprint(bp):
        o = L.get_object(sub.k2_find_subobject_data_from_handle(h))
        if o: out[o.get_name().split('_GEN')[0]] = (h, o)
    return out
cs = comps(); hm, main = cs['HairMain2']
bob = getattr(builtins, 'HAIR_BOB', False)
if 'HairLoose2' not in cs and not bob:
    d = sub.k2_find_subobject_data_from_handle(hm); ph = L.get_parent_handle(d) if hasattr(L, 'get_parent_handle') else None
    if ph is None or not L.is_handle_valid(ph): ph = cs['Face'][0]
    print('HAIRBUN parent', L.get_object(sub.k2_find_subobject_data_from_handle(ph)).get_name())
    nh, fail = sub.add_new_subobject(u.AddNewSubobjectParams(parent_handle=ph, new_class=u.GroomComponent, blueprint_context=bp))
    print('HAIRBUN add', fail); sub.rename_subobject(nh, u.Text('HairLoose2')); cs = comps()
mat = main.get_editor_property('override_materials')
if bob:
    main.set_editor_property('groom_asset', u.load_asset('/Game/Sphirus/CharacterLab/VF2_20261124/Hair/GR_Sph_MessyBob_VF2')); main.set_editor_property('binding_asset', u.load_asset('/Game/Sphirus/CharacterLab/VF2_20261124/Hair/GB_Sph_MessyBob_VF2'))
    if 'HairLoose2' in cs:
        lo = cs['HairLoose2'][1]; lo.set_editor_property('groom_asset', None); lo.set_editor_property('binding_asset', None); lo.set_editor_property('visible', False)
else:
    main.set_editor_property('groom_asset', u.load_asset(C + 'GR_C49_HairMain_h1')); main.set_editor_property('binding_asset', u.load_asset(B + 'GB_Sph8_HairMainH1'))
    lo = cs['HairLoose2'][1]; lo.set_editor_property('groom_asset', u.load_asset(C + 'GR_C49_HairLoose_h1')); lo.set_editor_property('binding_asset', u.load_asset(B + 'GB_Sph8_HairLooseH1'))
    lo.set_editor_property('override_materials', list(mat)); lo.set_editor_property('visible', True)
    for k in ('simulation_settings',):
        try: lo.set_editor_property(k, main.get_editor_property(k))
        except Exception as e: print('HAIRBUN copy', k, repr(e)[:100])
cs = comps()
print('HAIRBUN', {k: (o.get_editor_property('groom_asset').get_name() if o.get_editor_property('groom_asset') else None, o.get_editor_property('binding_asset').get_name() if o.get_editor_property('binding_asset') else None, [m.get_name() for m in o.get_editor_property('override_materials') if m], o.get_attach_parent().get_name() if o.get_attach_parent() else None) for k, (h, o) in cs.items() if isinstance(o, u.GroomComponent)})
