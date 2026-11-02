"""footpitch (measure): ankle->ball pitch (deg below horizontal, clip FK) at frames 0 / 25% / 50% for the SHM_JogQ start copies, their
source clips (same name without the SHM_JogQ_ prefix, found via the asset registry, any folder), the V2.48 crops and reference clips.
Also the skeleton of each clip (a retarget defect shows as a different skeleton or a constant offset)."""
import unreal as u, json, sys, importlib, math
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import v137_animedit as ae; importlib.reload(ae)
ar = u.AssetRegistryHelpers.get_asset_registry()
seqs = {str(a.asset_name): str(a.package_name) for a in ar.get_assets_by_class(u.TopLevelAssetPath('/Script/Engine', 'AnimSequence'), True)}
J = '/Game/GraceRanger/SHME/Animations/Starts/Jog/'
names = [n for n in seqs if n.startswith('SHM_JogQ_')]
want = []
for n in sorted(names):
    want.append(seqs[n]); src = n[len('SHM_JogQ_'):]
    if src in seqs: want.append(seqs[src])
for n in ('SHM248_Jog_Start_TurnL135_crop', 'A_CT_Jog_Fwd', 'af_Stand_Idle_NaturalBaseline_Phase275', 'SHM237_JogStart_F_Lfoot', 'A_LS_Jog_Left_Start', 'SHM232_IS_af_Loco_Jog_Start_TurnL045_Lfoot_AAMS', 'M_Neutral_Run_Start_F_Lfoot'):
    if n in seqs: want.append(seqs[n])
out = {}
def pitch(c, f, s):
    fo = c.comp('foot_' + s, f)[0]; ba = c.comp('ball_' + s, f)[0]
    return round(math.degrees(math.atan2(-(ba[2] - fo[2]), math.hypot(ba[0] - fo[0], ba[1] - fo[1]))), 1)
for p in want:
    try:
        seq = u.load_asset(p); c = ae.Clip(seq, ['foot_l', 'foot_r', 'ball_l', 'ball_r'])
        fr = [0, c.nf // 4, c.nf // 2]
        out[p] = {'skel': str(seq.get_editor_property('skeleton').get_name()), 'nf': c.nf, 'pitch_l': [pitch(c, f, 'l') for f in fr], 'pitch_r': [pitch(c, f, 'r') for f in fr]}
    except Exception as e: out[p] = 'err ' + str(e)[:80]
print('FOOTPITCH249 ' + json.dumps(out))
