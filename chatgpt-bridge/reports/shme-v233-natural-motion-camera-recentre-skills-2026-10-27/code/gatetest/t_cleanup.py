"""gate test cleanup: delete the two scratch assets of T7 (both listed in the cleanup manifest as new / existing)."""
import unreal as u
r = {n: u.EditorAssetLibrary.delete_asset('/Game/_GateTest233/' + n) for n in ('GT_Listed', 'GT_Unlisted') if u.EditorAssetLibrary.does_asset_exist('/Game/_GateTest233/' + n)}
r['dir'] = u.EditorAssetLibrary.delete_directory('/Game/_GateTest233')
print('GATETEST cleanup', r)
