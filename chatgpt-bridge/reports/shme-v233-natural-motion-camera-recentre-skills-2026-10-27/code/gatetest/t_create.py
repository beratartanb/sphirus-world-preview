"""gate test T7: a 'generator' creates one listed scratch asset and one UNLISTED scratch asset and saves the unlisted one through the real
class (bypassing the proxy) -> the post-job disk / dirty audit must fail the job (GUARD_WRITTEN / GUARD_DIRTY)."""
import unreal as u
at = u.AssetToolsHelpers.get_asset_tools()
r = {}
for n in ('GT_Listed', 'GT_Unlisted'):
    a = at.create_asset(n, '/Game/_GateTest233', u.DataTable, u.DataTableFactory()) if False else at.create_asset(n, '/Game/_GateTest233', u.CurveFloat, u.CurveFloatFactory())
    r[n] = bool(a)
real_eal = u.EditorAssetLibrary._c          # what an older captured reference would hold
r['bypass_save_unlisted'] = real_eal.save_asset('/Game/_GateTest233/GT_Unlisted', False)
try: r['proxy_save_unlisted'] = u.EditorAssetLibrary.save_asset('/Game/_GateTest233/GT_Unlisted', False)
except Exception as e: r['proxy_save_unlisted'] = 'BLOCKED ' + str(e)[:120]
r['proxy_save_listed'] = u.EditorAssetLibrary.save_asset('/Game/_GateTest233/GT_Listed', False)
print('GATETEST', r)
