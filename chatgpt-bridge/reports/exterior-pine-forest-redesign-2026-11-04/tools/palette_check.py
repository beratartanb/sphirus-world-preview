"""palette_check.py (offline, engine python): the Pine Forest redesign mesh palette with measured bounds from the XR3 library
(Saved/Codex/ExteriorIdentity_XR3_20261031/recon/library.json) + disk existence of every path. Prints the table; writes data/palette.json."""
import json, os, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
L = json.load(open('Saved/Codex/ExteriorIdentity_XR3_20261031/recon/library.json'))['meshes']
by = {k.split('/')[-1]: (k, v) for k, v in L.items()}
WANT = ['SM_PineTree01', 'SM_PineTree02', 'SM_PineTree03', 'SM_PineTree04', 'SM_PineTree05', 'SM_PineTree06', 'SM_PineTree07', 'SM_Pine_Juvenile_01', 'SM_PineTreeLow01', 'SM_PineTreeLow02', 'SM_PineTreeLow03', 'SM_PineTreeLowMed01', 'SM_PineTreeLowMed02', 'SM_PineTreeLowSmall01', 'SM_Pine_Med_Xtree_01', 'SM_Pine_Small_Xtree_01', 'SM_Pine_Xtree_01', 'SM_SonoSapling01', 'SM_SonoSapling02', 'SM_SonoSapling03', 'SM_SonoSapling04', 'SM_SonoTree01', 'SM_SonoTreeTall01',
        'SM_Fir_Tree_01', 'SM_Fir_Tree_03', 'SM_Fir_Tree_04', 'SM_Young_Black_Spruce_01', 'SM_Young_Black_Spruce_02', 'SM_Black_Spruce_01', 'SM_Oak_L_1', 'SM_Oak_L_2', 'SM_Oak_L_4', 'Pine_08',
        'SM_Bush_02', 'SM_Bush_03', 'SM_Bush_06', 'SM_Bush01', 'SM_Bush02', 'SM_Bush03', 'SM_BushB01', 'SM_BushB02', 'SM_BushB03', 'SM_BushB04', 'SM_BushC01', 'SM_Bush_SalixElag01', 'SM_Bush_SalixElag02', 'SM_Bush_SalixElag03',
        'SM_MossLeaf_01', 'SM_MossLeaf_02', 'SM_MossLeaf_03', 'SM_MossLeaf_04', 'SM_MossClump01', 'SM_MossPlant01', 'SM_WeedA_01', 'SM_WeedA_02', 'SM_GroundCover01', 'SM_GroundCover02', 'SM_GroundCover03', 'SM_GroundCover04', 'SM_IvyBed01',
        'SM_DeadPineNeedle01', 'SM_DeadLeaves01', 'SM_DeadLeaves02', 'SM_DeadLeaves03', 'SM_DeadLeaves04', 'SM_DeadBranch01', 'SM_FallenBranches01', 'SM_FallenBranches02', 'SM_PineAcorn01', 'SM_Mushroom01', 'SM_Mushroom02', 'SM_MushroomHanging01', 'SM_MushroomHanging02',
        'SM_PineGroundPatch01', 'SM_PineGroundPatch02', 'SM_PineGroundPatch03', 'SM_PineGroundPatch04', 'SM_PineGroundPatch05', 'SM_PineGroundPatch06', 'SM_RockyGround01', 'SM_RockyGround02', 'SM_ForestTrailPatches01', 'SM_ForestTrailPatches02', 'SM_GroundMossPatch01', 'SM_GroundMossPatch02', 'SM_GroundMossPatch03',
        'SM_TrunkPile01', 'SM_FallenTree01', 'SM_PineDeadTrunk01', 'SM_PineDeadTrunk02', 'SM_PineDeadTrunk03', 'SM_PineDeadTrunk04', 'SM_TreeStump01', 'SM_TreeStump02',
        'SM_PineGroundRock01', 'SM_PineGroundRock02', 'SM_PineGroundRock03', 'SM_PineGroundRock04', 'SM_PineGroundRock05', 'SM_PineGroundRock06', 'SM_CliffRock01', 'SM_CliffRock02', 'SM_CliffRockCurve01', 'SM_CliffRockCurve02', 'SM_PineCliff02', 'SM_PineCliff03', 'SM_ForestEmbankment01', 'SM_PineStone01', 'SM_PineStone02', 'SM_PineStone03', 'SM_PineStone04', 'SM_SmallStones01', 'SM_SmallStones02',
        'SM_Fern01', 'SM_Fern02', 'SM_Fern03', 'SM_Fern04', 'SM_FernLong01', 'SM_FernLong02', 'SM_FernLong03', 'SM_FernWide_01', 'SM_FernWild01', 'SM_FernWild02', 'SM_GrassSmall01', 'SM_GrassMedium01', 'SM_GrassLarge01', 'SM_GrassSmallSparse01', 'SM_GrassSmallDead01', 'SM_Grass_Sedge_01', 'SM_Grass_Sedge_02', 'SM_Big_Rock_01', 'SM_Middle_Rock_01', 'SM_FlatRock']
rows = []; miss = []; pal = {}
for n in WANT:
    if n not in by:
        miss.append(n); continue
    k, v = by[n]; e = v['ext']
    pal[n] = {'path': k, 'ext': e, 'org': v['org'], 'tris': v.get('tris'), 'nanite': v.get('nanite'), 'col': v.get('col'), 'mats': v.get('mats'), 'h': round(e[2] * 2), 'w': round(max(e[0], e[1]) * 2)}
    rows.append('%-26s h=%5.0f w=%5.0f org_z=%5.0f tris=%7s nanite=%-5s col=%-9s %s' % (n, e[2] * 2, max(e[0], e[1]) * 2, v['org'][2], v.get('tris'), v.get('nanite'), (v.get('col') or '')[:9], k.replace('/Game/', '')[:58]))
print('\n'.join(rows)); print('MISSING in library:', miss)
for n in miss:
    hits = []
    for root, ds, fs in os.walk('Content'):
        if n + '.uasset' in fs: hits.append(os.path.join(root, n).replace(os.sep, '/'))
    print('  ', n, '->', hits[:3])
    if hits: pal[n] = {'path': '/Game/' + hits[0][len('Content/'):], 'unmeasured': True}
os.makedirs('Saved/Codex/PineForestRedesign_20261104/data', exist_ok=True)
json.dump(pal, open('Saved/Codex/PineForestRedesign_20261104/data/palette.json', 'w'), indent=0)
missing_disk = [n for n, d in pal.items() if not os.path.exists('Content/' + d['path'][len('/Game/'):] + '.uasset')]
print('palette', len(pal), 'missing on disk', missing_disk)
