# c_b4_wire.py (control or write; in memory, re-appliable): points the player at the B4 body form and its refitted garments.
# builtins.B4_OFF = True restores the previous assets (same mapping reversed). Prints the resulting assignment.
import unreal as u, builtins
B = '/Game/Sphirus/CharacterLab/B4_20261125'
MAP = {'/Game/Sphirus/CharacterLab/Sph_20261108/Built/MHC_Sph8/Body/SKM_MHC_Sph8_BodyMesh': B + '/Body/SKM_Sph_B4_BodyMesh',
       '/Game/Sphirus/CharacterLab/VF2_20261124/Garments/SKM_Sph_RetroTop_VF2': B + '/Garments/SKM_Sph_RetroTop_B4',
       '/Game/Sphirus/CharacterLab/VF2_20261124/Garments/SKM_Sph_CuffedShorts_VF2': B + '/Garments/SKM_Sph_CuffedShorts_B4',
       '/Game/Sphirus/CharacterLab/Sph_20261108/Out_S8Tank/MHC_S8Tank/Clothing/MHC_S8Tank_Outfits': B + '/Garments/SKM_Sph_S8Tank_B4',
       '/Game/Sphirus/CharacterLab/Day_20261107/Garments/SKM_Sph_Pants70': B + '/Garments/SKM_Sph_Pants70_B4',
       '/Game/Sphirus/CharacterLab/Day_20261107/Garments/SKM_Sph_Cargo': B + '/Garments/SKM_Sph_Cargo_B4',
       '/Game/Sphirus/CharacterLab/Day_20261107/Garments/SKM_Sph_Belt2': B + '/Garments/SKM_Sph_Belt2_B4'}
MAP.update(getattr(builtins, 'B4_EXTRA_MAP', None) or {})
if getattr(builtins, 'B4_OFF', False): MAP = {v: k for k, v in MAP.items()}
def key(o): return o.get_path_name().split('.')[0] if o else None
def sw(o):
    k = key(o); return u.load_asset(MAP[k]) if k in MAP else o
bp = u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'); c = u.get_default_object(bp.generated_class()); rep = {}
for arr in ('GR_OutfitTop', 'GR_OutfitLow', 'GR_BeltList'):
    v = list(c.get_editor_property(arr)); nv = [sw(x) for x in v]; c.set_editor_property(arr, nv); rep[arr] = [x.get_name() for x in nv]
sub = u.get_engine_subsystem(u.SubobjectDataSubsystem)
for h in sub.k2_gather_subobject_data_for_blueprint(bp):
    o = u.SubobjectDataBlueprintFunctionLibrary.get_object(sub.k2_find_subobject_data_from_handle(h))
    if isinstance(o, u.SkeletalMeshComponent) and o.get_name().split('_GEN')[0] in ('Manny', 'Henley', 'Shorts', 'GR_BeltSk'):
        m = o.get_skeletal_mesh_asset(); n = sw(m)
        if n is not m: o.set_editor_property('skeletal_mesh_asset', n)
        rep[o.get_name()] = o.get_skeletal_mesh_asset().get_name()
print('B4WIRE', rep)
