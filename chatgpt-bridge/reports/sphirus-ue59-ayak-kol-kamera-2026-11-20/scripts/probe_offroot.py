# probe_offroot.py (read-only): OffsetRootBone / stop plant settings on the ABP_Sph_GASP CDO + the OffsetRootBone node settings.
import unreal as u
a = u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); d = u.get_default_object(a.generated_class()); o = []
for k in ('OffsetRootBoneEnabled', 'OffsetRootTranslationRadius', 'PlantSettings_Stops', 'InterpolationSettings_Stops', 'PlantSettings_Default', 'InterpolationSettings_Default', 'UseThreadSafeUpdate'):
    try:
        v = d.get_editor_property(k); o.append('%s = %s' % (k, v.export_text() if hasattr(v, 'export_text') else v))
    except Exception as e: o.append('%s ? %s' % (k, str(e)[:80]))
ar = u.AssetRegistryHelpers.get_asset_registry()
for cls in ('AnimGraphNode_OffsetRootBone', 'AnimGraphNode_FootPlacement'):
    for i in range(4):
        n = u.find_object(None, '/Game/Sphirus/Player/GASP/ABP_Sph_GASP.ABP_Sph_GASP:AnimGraph.%s_%d' % (cls, i))
        if n:
            nd = n.get_editor_property('node'); o.append('NODE %s_%d %s' % (cls, i, nd.export_text()[:1500] if hasattr(nd, 'export_text') else nd))
open(u.Paths.project_dir() + 'Saved/UE59Work/probe/offroot.txt', 'w').write('\n'.join(o)); print('OR', len(o))
