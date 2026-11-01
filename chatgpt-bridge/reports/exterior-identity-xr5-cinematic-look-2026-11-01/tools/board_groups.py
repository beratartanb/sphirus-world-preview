"""board_groups.py <out.json>: asset lineup groups for xr3_board.py (what the library really looks like under the level's own light).
Each group = up to 4 meshes photographed together by the player camera; the first group of each family is the one in production use."""
import json, sys
P = '/Game/PineForestPack/Meshes/'; C = '/Game/Calysto/World/Vegetation/Meshes/'; F = '/Game/Fishermans_Cabin/Meshes/'; O = '/Game/OakForestEnv/Meshes/'
E = '/Game/Environment_Set/Environment/'
G = [
 ('trees_prod_pine', [[P + 'Trees/SM_PineTree01', 'PineTree01 (prod)', 1], [P + 'Trees/SM_PineTree03', 'PineTree03 (prod)', 1], [P + 'Trees/SM_PineTree05', 'PineTree05 (prod)', 1]]),
 ('trees_prod_fir', [[F + 'Foliage/Tree/SM_Fir_Tree_01', 'Fir_Tree_01 (prod)', 1], [F + 'Foliage/Tree/SM_Fir_Tree_03', 'Fir_Tree_03 (prod)', 1], [F + 'Foliage/Tree/SM_Fir_Tree_04', 'Fir_Tree_04 (prod)', 1]]),
 ('trees_pine_other', [[P + 'Trees/SM_PineTree02', 'PineTree02', 1], [P + 'Trees/SM_PineTree04', 'PineTree04', 1], [P + 'Trees/SM_PineTree06', 'PineTree06', 1], [P + 'Trees/SM_PineTree07', 'PineTree07', 1]]),
 ('trees_spruce', [[C + 'SM_Black_Spruce_01', 'Black_Spruce_01', 1], [C + 'SM_Black_Spruce_02', 'Black_Spruce_02', 1], [C + 'SM_Black_Spruce_03', 'Black_Spruce_03', 1], [C + 'SM_Black_Spruce_05', 'Black_Spruce_05', 1]]),
 ('trees_fir_other', [[F + 'Foliage/Tree/SM_Fir_Tree_02', 'Fir_Tree_02', 1], [F + 'Foliage/Tree/SM_Fir_Tree_05', 'Fir_Tree_05', 1], [F + 'Foliage/Tree/SM_Fir_Tree_06', 'Fir_Tree_06', 1], [F + 'Foliage/Tree/SM_Fir_Tree_08', 'Fir_Tree_08', 1]]),
 ('trees_xtree_sono', [[P + 'Trees/Xtrees/SM_Pine_Xtree_01', 'Pine_Xtree_01', 1], [P + 'Trees/Xtrees/SM_Pine_Xtree_03', 'Pine_Xtree_03', 1], [P + 'Trees/SM_SonoTree01', 'SonoTree01', 1], [P + 'Trees/SM_SonoTreeTall01', 'SonoTreeTall01', 1]]),
 ('trees_oak_alder', [[O + 'Trees_Leaf/Spring/SM_Oak_L_1', 'Oak_L_1 (prod)', 1], [C + 'SM_Speckled_Alder_01', 'Speckled_Alder_01', 1], [C + 'SM_Speckled_Alder_03', 'Speckled_Alder_03', 1], [C + 'SM_Dead_Tree_02', 'Dead_Tree_02', 1]]),
 ('trees_dead_low', [[P + 'Trees/LowPoly/SM_PineTreeLowDead01', 'PineTreeLowDead01', 1], [P + 'Trees/LowPoly/SM_PineTreeLowDead03', 'PineTreeLowDead03', 1], [P + 'Trees/LowPoly/SM_PineTreeLow01', 'PineTreeLow01', 1], [P + 'Trees/LowPoly/SM_PineTreeLowMed01', 'PineTreeLowMed01', 1]]),
 ('young_prod', [[P + 'Trees/SM_Pine_Juvenile_01', 'Pine_Juvenile_01 (prod)', 1], [C + 'SM_Young_Black_Spruce_01', 'Young_Black_Spruce_01 (prod)', 1], [C + 'SM_Young_Black_Spruce_02', 'Young_Black_Spruce_02 (prod)', 1], [P + 'Trees/Xtrees/SM_Pine_Small_Xtree_01', 'Pine_Small_Xtree_01', 1]]),
 ('young_sapling', [[P + 'Plants/SM_SonoSapling01', 'SonoSapling01', 1], [P + 'Plants/SM_SonoSapling02', 'SonoSapling02', 1], [P + 'Plants/SM_SonoSapling03', 'SonoSapling03', 1], [P + 'Trees/Xtrees/SM_Pine_Med_Xtree_01', 'Pine_Med_Xtree_01', 1]]),
 ('shrub_prod', [[F + 'Foliage/Bush/SM_Bush_02', 'Bush_02 (prod)', 1], [F + 'Foliage/Bush/SM_Bush_03', 'Bush_03 (prod)', 1], [F + 'Foliage/Bush/SM_Bush_06', 'Bush_06 (prod)', 1], [P + 'Plants/SM_Bush_SalixElag01', 'Bush_SalixElag01', 1]]),
 ('shrub_other', [[P + 'Plants/SM_Bush01', 'PF Bush01', 1], [P + 'Plants/SM_BushB01', 'PF BushB01', 1], [C + 'SM_Bog_Laurel_02', 'Bog_Laurel_02', 1], [C + 'SM_BogLaurelClump', 'BogLaurelClump', 1]]),
 ('ground_prod', [[P + 'Plants/SM_FernLong01', 'FernLong01 (prod)', 1], [P + 'Plants/SM_FernWild01', 'FernWild01 (prod)', 1], [P + 'GroundCover/SM_GroundCover03', 'GroundCover03 (prod)', 1], [P + 'Grass/SM_GrassMedium01', 'GrassMedium01 (prod)', 1]]),
 ('ground_calysto', [[C + 'SM_Bunchberry_02', 'Bunchberry_02', 1], [C + 'SM_Bluejoint_Grass_Clump_01', 'Bluejoint_Clump_01', 1], [C + 'SM_Sweetgrass_03', 'Sweetgrass_03', 1], [C + 'SM_Fireweed_Clump', 'Fireweed_Clump', 1]]),
 ('ground_moss_fungi', [[P + 'Moss/SM_MossClump01', 'MossClump01', 1], [P + 'TerrainPatches/SM_GroundMossPatch01', 'GroundMossPatch01', 1], [C + 'SM_MossPatch_01', 'Calysto MossPatch_01', 1], [C + 'SM_Dryad_Saddle_Clump_01', 'Dryad_Saddle_Clump', 1]]),
 ('ground_litter', [[P + 'DeadLeaves/SM_DeadLeaves02', 'DeadLeaves02 (prod)', 1], [P + 'GroundCover/SM_IvyBed01', 'IvyBed01', 1], [P + 'TerrainPatches/SM_PineGroundPatch02', 'PineGroundPatch02', 1], [P + 'TerrainPatches/SM_ForestTrailPatches01', 'ForestTrailPatches01', 1]]),
 ('rock_prod', [[P + 'Rocks/SM_PineStone01', 'PineStone01 (prod)', 1], [P + 'Cliffs/SM_PineGroundRock03', 'PineGroundRock03 (prod)', 1], [P + 'Cliffs/SM_ForestEmbankment01', 'ForestEmbankment01 (prod)', 1]]),
 ('rock_cliff', [[P + 'Cliffs/SM_CliffRock01', 'CliffRock01 (XR2)', 1], [P + 'Cliffs/SM_CliffRockCurve01', 'CliffRockCurve01 (XR2)', 1], [P + 'Cliffs/SM_PineCliff02', 'PineCliff02 (XR2)', 1], [P + 'Cliffs/SM_PineCliff03', 'PineCliff03 (XR2)', 1]]),
 ('rock_other', [[E + 'Rocks/Models/SM_Big_Rock_01', 'EnvSet Big_Rock_01', 1], [E + 'Rocks/Models/SM_Big_Rock_02', 'EnvSet Big_Rock_02', 1], [O + 'ScanAssets/SM_Boulder_1', 'Oak Boulder_1', 1], [C + 'SM_Rock_02', 'Calysto Rock_02', 1]]),
 ('rock_small', [[P + 'Cliffs/SM_PineGroundRock01', 'PineGroundRock01', 1], [P + 'Cliffs/SM_PineGroundRock05', 'PineGroundRock05', 1], [E + 'Rocks/Models/SM_Middle_Rock_02', 'EnvSet Middle_Rock_02', 1], [P + 'TerrainPatches/SM_RockyGround01', 'RockyGround01', 1]]),
 ('deadwood', [[P + 'TerrainPatches/SM_FallenTree01', 'FallenTree01 (XR2)', 1], [P + 'TerrainPatches/SM_PineDeadTrunk01', 'PineDeadTrunk01 (XR2)', 1], [C + 'SM_Fallen_Log_01', 'Calysto Fallen_Log_01', 1], [P + 'TerrainPatches/SM_TreeStump01', 'TreeStump01 (prod)', 1]]),
 ('roots', [[O + 'ScanAssets/SM_Root_4', 'Oak Root_4 (prod)', 1], [O + 'ScanAssets/SM_Root_1', 'Oak Root_1', 1], [E + 'Foliage/Models/SM_crooked_root_01', 'EnvSet crooked_root_01', 1], [O + 'ScanAssets/SM_Embankment_1', 'Oak Embankment_1', 1]]),
 ('props_use', [[F + 'Lamps/SM_Lamp_01', 'Lamp_01', 1], [F + 'Sign_Set/SM_Sign_Set_01', 'Sign_Set_01', 1], [F + 'Wheelbarrow/SM_Wheelbarrow', 'Wheelbarrow', 1], [F + 'Trap/SM_Trap_01', 'Trap_01', 1]]),
 ('props_use2', [[F + 'Sticks/SM_Sticks_01', 'Sticks_01', 1], [F + 'Wood_Box_Low/SM_Wooden_Box_Low_01', 'Wood_Box_Low', 1], [F + 'Fishing_Gear_01/SM_Fishing_Gear_01', 'Fishing_Gear_01', 1], [F + 'Ropes/SM_Rope_Tire_01', 'Rope_01', 1]]),
 ('props_build', [[F + 'Outhouse/SM_Outhouse_01', 'Outhouse_01', 1], [F + 'Toolshed/SM_Toolshed_01', 'Toolshed_01', 1], [F + 'Wooden_Dock/SM_Wooden_Dock_01', 'Wooden_Dock_01', 1], [F + 'Boat/SM_Boat_01', 'Boat_01 (XR2)', 1]]),
]
json.dump([{'name': n, 'items': it} for n, it in G], open(sys.argv[1], 'w'), indent=0); print('GROUPS', len(G))
