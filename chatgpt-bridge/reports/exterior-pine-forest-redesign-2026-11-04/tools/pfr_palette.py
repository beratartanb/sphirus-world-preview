"""pfr_palette.py: the Pine Forest redesign palette - roles, swap tables (existing vendor-mix meshes -> Pine Forest Pack family),
measured bounds (Saved/Codex/PineForestRedesign_20261104/data/palette.json from palette_check.py) and the FoliageType plan.
Pine Forest Pack = dominant identity (canopy, understory, floor, rocks, deadwood); Environment_Set = big-rock accents only where the
PFP cliff family cannot give a single bedrock mass; Calysto black spruce = a few dark sub-canopy accents (kept, reduced)."""
import json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
PAL = json.load(open(os.path.join(ROOT, 'Saved/Codex/PineForestRedesign_20261104/data/palette.json')))
PF = '/Game/PineForestPack/Meshes/'
M = {k: v['path'] for k, v in PAL.items()}            # short name -> package path


def ext(name):
    """half extents [x, y, z] and origin [x, y, z] (cm, unscaled) from the measured library"""
    v = PAL[name]; return v['ext'], v['org']


# ---- canopy: Fishermans firs (10-12 m, yellow-green) -> PFP mid pines of the same height band (family unification, no height jump)
FIR_SWAP = {
    'SM_Fir_Tree_01': [('SM_PineTree06', 0.85, 1.05), ('SM_PineTreeLowMed02', 0.75, 0.95), ('SM_SonoTreeTall01', 0.95, 1.15)],   # 10.3 m -> 11-13.6 / 12-15 / 10-12 m
    'SM_Fir_Tree_03': [('SM_PineTree06', 0.95, 1.15), ('SM_PineTreeLowMed02', 0.8, 1.0), ('SM_PineTree05', 0.6, 0.75)],          # 12.2 m
    'SM_Fir_Tree_04': [('SM_PineTree06', 0.9, 1.1), ('SM_PineTreeLowMed01', 0.95, 1.2), ('SM_PineTree07', 0.55, 0.7)],           # 11.7 m
}
# ---- sub-canopy / young: Calysto young spruce (2.4-2.9 m) -> PFP juveniles + broadleaf saplings (showcase language); 35 % kept as dark accents
YOUNG_SWAP = {
    'SM_Young_Black_Spruce_01': [('SM_Pine_Juvenile_01', 0.8, 1.1), ('SM_SonoSapling01', 1.1, 1.5), ('SM_PineTreeLowSmall01', 0.8, 1.1)],
    'SM_Young_Black_Spruce_02': [('SM_Pine_Juvenile_01', 0.9, 1.2), ('SM_SonoTree01', 0.7, 0.95), ('SM_SonoSapling01', 1.2, 1.6)],
    'Pine_08': [('SM_Pine_Juvenile_01', 0.8, 1.0)],
}
YOUNG_KEEP_FRACTION = 0.35
# ---- midstory: Fishermans bushes -> PFP bush family (height matched)
BUSH_SWAP = {
    'SM_Bush_02': [('SM_Bush02', 0.95, 1.2), ('SM_Bush01', 0.6, 0.8), ('SM_Bush_SalixElag01', 1.2, 1.5)],      # 1.9 m
    'SM_Bush_03': [('SM_Bush03', 0.9, 1.2), ('SM_BushB01', 0.7, 0.9), ('SM_Bush_SalixElag02', 1.2, 1.5)],       # 1.1 m
    'SM_Bush_06': [('SM_Bush02', 0.9, 1.15), ('SM_Bush_SalixElag01', 1.1, 1.4), ('SM_BushB01', 1.1, 1.3)],      # 1.7 m
}
# ---- litter: red-purple broadleaf (DeadLeaves02) under conifers -> needle floor clumps (03/04) + branches; broadleaf only under the oaks
LITTER_SWAP = {'SM_DeadLeaves02': [('SM_DeadLeaves03', 0.7, 1.0), ('SM_DeadLeaves04', 0.6, 0.75), ('SM_DeadBranch01', 0.8, 1.0)]}
# ---- Megascans roots/patches (Fab) are kept (they are scanned ground detail) but the flat Nordic patch is removed on slopes by the design
# ---- new PFP floor families (instances authored by the design, placed as NEW foliage types)
_MATD = '/Game/GraceRanger/Environment/Exterior20260921/Materials/'
FT_MATS = {   # owned foliage type -> override materials (owned instances; the vendor meshes and instances stay untouched). p3: darker litter cards
    'FT_EX_PF_DeadLeaves03': [_MATD + 'MI_EX_PF_DeadLeaves01'], 'FT_EX_PF_DeadLeaves04': [_MATD + 'MI_EX_PF_DeadLeaves02']}
NEW_TYPES = {   # name -> (mesh short name, cull [start, end], collision, cast_shadow, align_to_normal, random_yaw, scale range)
    'FT_EX_PF_PineTree02': ('SM_PineTree02', [35000, 43000], True, True, False, True, (0.9, 1.15)),
    'FT_EX_PF_PineTree04': ('SM_PineTree04', [42000, 56000], True, True, False, True, (1.0, 1.3)),
    'FT_EX_PF_PineTree06': ('SM_PineTree06', [17000, 22000], True, True, False, True, (0.85, 1.15)),
    'FT_EX_PF_PineTree07': ('SM_PineTree07', [35000, 43000], True, True, False, True, (0.9, 1.1)),
    'FT_EX_PF_PineLowMed01': ('SM_PineTreeLowMed01', [17000, 22000], True, True, False, True, (0.9, 1.2)),
    'FT_EX_PF_PineLowMed02': ('SM_PineTreeLowMed02', [17000, 22000], True, True, False, True, (0.8, 1.0)),
    'FT_EX_PF_SonoTreeTall': ('SM_SonoTreeTall01', [17000, 22000], True, True, False, True, (0.95, 1.15)),
    'FT_EX_PF_SonoTree': ('SM_SonoTree01', [9000, 14000], False, True, False, True, (0.7, 1.0)),
    'FT_EX_PF_PineLowSmall': ('SM_PineTreeLowSmall01', [9000, 14000], False, True, False, True, (0.8, 1.1)),
    'FT_EX_PF_Sapling01': ('SM_SonoSapling01', [6000, 9000], False, True, True, True, (1.0, 1.6)),
    'FT_EX_PF_Sapling02': ('SM_SonoSapling02', [5000, 8000], False, True, True, True, (1.0, 1.5)),
    'FT_EX_PF_Sapling03': ('SM_SonoSapling03', [4000, 6500], False, False, True, True, (1.0, 1.5)),
    'FT_EX_PF_Bush01': ('SM_Bush01', [4200, 6800], False, True, False, True, (0.6, 1.0)),
    'FT_EX_PF_Bush02': ('SM_Bush02', [4200, 6800], False, True, False, True, (0.9, 1.2)),
    'FT_EX_PF_Bush03': ('SM_Bush03', [4200, 6800], False, True, False, True, (0.9, 1.2)),
    'FT_EX_PF_BushB01': ('SM_BushB01', [4200, 6800], False, True, False, True, (0.8, 1.3)),
    'FT_EX_PF_Salix01': ('SM_Bush_SalixElag01', [4200, 6800], False, True, False, True, (1.1, 1.5)),
    'FT_EX_PF_Salix02': ('SM_Bush_SalixElag02', [4200, 6800], False, True, False, True, (1.1, 1.5)),
    'FT_EX_PF_DeadLeaves03': ('SM_DeadLeaves03', [2200, 4200], False, False, True, True, (0.7, 1.0)),
    'FT_EX_PF_DeadLeaves04': ('SM_DeadLeaves04', [2500, 4500], False, False, True, True, (0.6, 0.75)),
    'FT_EX_PF_Needle': ('SM_DeadPineNeedle01', [1500, 2500], False, False, True, True, (1.5, 3.0)),
    'FT_EX_PF_MossLeaf01': ('SM_MossLeaf_01', [2500, 3500], False, False, True, True, (2.0, 3.0)),
    'FT_EX_PF_MossLeaf02': ('SM_MossLeaf_02', [2500, 3500], False, False, True, True, (1.8, 2.8)),
    'FT_EX_PF_MossLeaf03': ('SM_MossLeaf_03', [2500, 3500], False, False, True, True, (1.8, 2.8)),
    'FT_EX_PF_MossLeaf04': ('SM_MossLeaf_04', [2500, 3500], False, False, True, True, (1.6, 2.6)),
    'FT_EX_PF_MossClump': ('SM_MossClump01', [2000, 3000], False, False, True, True, (2.0, 3.0)),
    'FT_EX_PF_WeedA01': ('SM_WeedA_01', [3000, 4500], False, False, True, True, (1.2, 2.2)),
    'FT_EX_PF_GroundCover02': ('SM_GroundCover02', [2500, 4000], False, False, True, True, (0.9, 1.3)),
    'FT_EX_PF_Cone': ('SM_PineAcorn01', [1200, 2000], False, False, True, True, (1.4, 2.2)),
    'FT_EX_PF_FallenBranches01': ('SM_FallenBranches01', [3000, 5000], False, False, True, True, (0.8, 1.2)),
    'FT_EX_PF_Mushroom01': ('SM_Mushroom01', [1500, 2500], False, False, True, True, (1.2, 2.0)),
    'FT_EX_PF_GroundPatch': ('SM_PineGroundPatch03', [4000, 6000], False, False, True, True, (0.9, 1.3)),
    'FT_EX_PF_GroundPatch01': ('SM_PineGroundPatch01', [4500, 7000], False, False, True, True, (0.9, 1.2)),
    'FT_EX_PF_GroundPatch04': ('SM_PineGroundPatch04', [4500, 7000], False, False, True, True, (0.8, 1.1)),
    'FT_EX_PF_RockyGround': ('SM_RockyGround01', [5000, 8000], False, True, True, True, (0.8, 1.2)),
    'FT_EX_PF_TrailPatch01': ('SM_ForestTrailPatches01', [4500, 7000], False, False, True, True, (0.85, 1.1)),
    'FT_EX_PF_TrailPatch02': ('SM_ForestTrailPatches02', [4500, 7000], False, False, True, True, (0.8, 1.1)),
    'FT_EX_PF_GroundRock02': ('SM_PineGroundRock02', [12000, 18000], True, True, False, True, (0.8, 1.4)),
    'FT_EX_PF_GroundRock04': ('SM_PineGroundRock04', [12000, 18000], True, True, False, True, (0.9, 1.5)),
    'FT_EX_PF_GroundRock06': ('SM_PineGroundRock06', [10000, 16000], True, True, False, True, (0.9, 1.6)),
    'FT_EX_PF_DeadTrunk04': ('SM_PineDeadTrunk04', [8000, 14000], True, True, True, True, (0.9, 1.3)),
    'FT_EX_PF_FernLong02': ('SM_FernLong02', [4000, 6800], False, False, True, True, (0.9, 1.4)),
}
# existing owned types reused as-is (mesh -> FT name is resolved in the editor by mesh + cull, as before)
EXISTING_OK = ['SM_PineTree01', 'SM_PineTree03', 'SM_PineTree05', 'SM_Pine_Juvenile_01', 'SM_Fern01', 'SM_Fern02', 'SM_Fern03', 'SM_FernLong01', 'SM_FernWide_01', 'SM_FernWild01',
               'SM_GrassSmall01', 'SM_GrassMedium01', 'SM_GroundCover01', 'SM_GroundCover03', 'SM_DeadBranch01', 'SM_PineStone01', 'SM_PineStone02', 'SM_PineStone03', 'SM_PineStone04', 'SM_SmallStones01',
               'SM_PineDeadTrunk01', 'SM_PineDeadTrunk02', 'SM_PineDeadTrunk03', 'SM_TreeStump01', 'SM_TreeStump02', 'SM_PineGroundRock01', 'SM_PineGroundRock03', 'SM_PineGroundRock05', 'SM_ForestEmbankment01', 'SM_FallenTree01',
               'SM_Grass_Sedge_01', 'SM_Grass_Sedge_02', 'SM_Grass_Sedge_04', 'SM_Oak_L_1', 'SM_Oak_L_2', 'SM_Oak_L_4', 'SM_Young_Black_Spruce_01', 'SM_Young_Black_Spruce_02', 'wgxjfhr_tier_1', 'tkwqbbofa_tier_1']
VENDOR_OUT = ['SM_Fir_Tree_01', 'SM_Fir_Tree_03', 'SM_Fir_Tree_04', 'SM_Bush_02', 'SM_Bush_03', 'SM_Bush_06', 'SM_DeadLeaves02', 'Pine_08']   # leave the map (0 instances) in this design

if __name__ == '__main__':
    bad = [v[0] for v in NEW_TYPES.values() if v[0] not in PAL]
    print('new types', len(NEW_TYPES), 'unmeasured meshes', bad)
    for k, (mesh, cull, col, sh, al, ry, sc) in NEW_TYPES.items():
        e, o = ext(mesh); print('%-28s %-24s h=%4.0f cull=%s col=%s shadow=%s' % (k, mesh, e[2] * 2, cull, col, sh))
