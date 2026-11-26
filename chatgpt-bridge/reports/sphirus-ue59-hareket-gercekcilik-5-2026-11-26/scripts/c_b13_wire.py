# c_b13_wire.py (control / write; in memory, re-appliable): player B12 -> B13 (waist a little wider at the sides). B13_OFF -> back to B12.
import unreal as u, builtins
B4 = '/Game/Sphirus/CharacterLab/B12_20261126'; B5 = '/Game/Sphirus/CharacterLab/B13_20261126'
N = ['Body/SKM_Sph_%s_BodyMesh', 'Garments/SKM_Sph_RetroTop_%s', 'Garments/SKM_Sph_CuffedShorts_%s', 'Garments/SKM_Sph_S8Tank_%s', 'Garments/SKM_Sph_Pants70_%s', 'Garments/SKM_Sph_Cargo_%s', 'Garments/SKM_Sph_Belt2_%s']
MAP = {'%s/%s' % (B4, n % 'B12'): '%s/%s' % (B5, n % 'B13') for n in N[1:]}
MAP['/Game/Sphirus/CharacterLab/B12_20261126/Body/SKM_Sph_B12_BodyMesh'] = B5 + '/Body/SKM_Sph_B13_BodyMesh'
if getattr(builtins, 'B13_OFF', False): MAP = {v: k for k, v in MAP.items()}
def key(o): return o.get_path_name().split('.')[0] if o else None
def sw(o):
    k = key(o); return u.load_asset(MAP[k]) if k in MAP else o
bp = u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'); c = u.get_default_object(bp.generated_class()); rep = {}
for arr in ('GR_OutfitTop', 'GR_OutfitLow', 'GR_BeltList'):
    v = list(c.get_editor_property(arr)); nv = [sw(x) for x in v]; c.set_editor_property(arr, nv); rep[arr] = [x.get_name() for x in nv]
sub = u.get_engine_subsystem(u.SubobjectDataSubsystem)
for h in sub.k2_gather_subobject_data_for_blueprint(bp):
    o = u.SubobjectDataBlueprintFunctionLibrary.get_object(sub.k2_find_subobject_data_from_handle(h))
    if isinstance(o, u.SkeletalMeshComponent) and o.get_name().split('_GEN')[0] in ('Manny', 'Henley', 'Shorts', 'GR_BeltSk', 'GR_Under'):
        m = o.get_skeletal_mesh_asset(); n = sw(m)
        if n is not m: o.set_editor_property('skeletal_mesh_asset', n)
        rep[o.get_name()] = o.get_skeletal_mesh_asset().get_name()
print('B13WIRE', rep)
