"""db235_bias.py (editor job): continuing-pose preference on the V2.35 reversal databases. b1 (j30_rel_3200 rvR, 39.5 cm): in the release gap
the V2.34 ABP keep searches only the reversal DB and, with the default -0.05 continuing bias, re-enters a NEW bin at ct 0 every frame
(F_B P7 / P23 / P8 / P24 in 4 frames) instead of continuing the clip that is already reversing; the re-press then enters the slow family at
its own design speed (capsule 64 -> 248 -> 92 cm/s). The project stop DB uses -0.76 for the same reason. builtins.V235_BIAS = {'bias': -0.5}.
Only the two V235 candidate DBs change. Prints DBBIAS235 {...}."""
import unreal as u, json, builtins
b = float(dict(getattr(builtins, 'V235_BIAS', {})).get('bias', -0.5)); out = {}
for p in ['/Game/GraceRanger/SHME/Animations/V235/PSD_SHM235_JogRevFwd', '/Game/GraceRanger/SHME/Animations/V235/PSD_SHM235_JogRevBwdX']:
    d = u.load_asset(p); d.set_editor_property('continuing_pose_cost_bias', b)
    out[p.rsplit('/', 1)[1]] = [d.get_editor_property('continuing_pose_cost_bias'), u.EditorAssetLibrary.save_asset(p, False)]
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('DBBIAS235 ' + json.dumps(out, default=str))
