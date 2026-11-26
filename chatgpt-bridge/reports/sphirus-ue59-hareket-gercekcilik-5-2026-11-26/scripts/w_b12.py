# w_b12.py (write, gated): B12 = B11 closed body with the waist widened slightly at the sides (p_b12: torso_w +3..5 %% at z 97-119,
# waist width 19.5 -> 20.4 cm, circumference 57.7 -> 59.2, depth unchanged) + the six garments with the same field.
import builtins, unreal as u
D = u.Paths.project_dir(); B12R = '/Game/Sphirus/CharacterLab/B12_20261126'; B12W = D + 'Saved/UE59Work/b4/s12/'
builtins.B11_DST = B12R + '/Body/SKM_Sph_B12_BodyMesh'; builtins.B11_POS = 'b12_pos.json'
exec(open(D + 'Tools/UE59_20261126/w_b11_body.py', encoding='utf8').read())
exec(open(D + 'Tools/UE59_20261126/w_b11_weights.py', encoding='utf8').read())
G0 = [('/Game/Sphirus/CharacterLab/VF2_20261124/Garments/SKM_Sph_RetroTop_VF2', 'RetroTop', 'retrotop'), ('/Game/Sphirus/CharacterLab/VF2_20261124/Garments/SKM_Sph_CuffedShorts_VF2', 'CuffedShorts', 'cshorts'),
      ('/Game/Sphirus/CharacterLab/Sph_20261108/Out_S8Tank/MHC_S8Tank/Clothing/MHC_S8Tank_Outfits', 'S8Tank', 'tank'), ('/Game/Sphirus/CharacterLab/Day_20261107/Garments/SKM_Sph_Pants70', 'Pants70', 'pants70'),
      ('/Game/Sphirus/CharacterLab/Day_20261107/Garments/SKM_Sph_Cargo', 'Cargo', 'cargo'), ('/Game/Sphirus/CharacterLab/Day_20261107/Garments/SKM_Sph_Belt2', 'Belt2', 'belt2')]
builtins.B4_APPLY = [{'src': s, 'dst': '%s/Garments/SKM_Sph_%s_B12' % (B12R, n), 'delta': B12W + 'delta_g_%s.json' % k, 'keep_normals': True} for s, n, k in G0]
exec(open(D + 'Tools/UE59_20261124/b4_apply.py', encoding='utf8').read())
print('B12 done')
