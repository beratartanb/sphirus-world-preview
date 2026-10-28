"""verify235.py (fresh editor, read-only, SHME_KIND=measure): every earlier contract (verify234 with all V2.34 groups) plus V2.35:
ABP reversal DBs -> V235 (rev), DA RevOverHard (route), BP_GR_Player + child GR233_RecMouseScale 0.7 (mouse), SHM_UpdateRouting census
(RevOverHard read, V2.34 setters, > 150 nodes), V235 DB entry lists (32 bins + loops), continuing bias -0.5, the jog stop clip IS the restored
V2.34 file (sha1 differs from the stop1 backup). builtins.V235_EXP = {'rev', 'route', 'mouse'}. Prints VERIFY235."""
import builtins, json, hashlib, os
E = dict(getattr(builtins, 'V235_EXP', {}))
builtins.V234_EXP = {'loco': True, 'camfollow': True, 'revkeep': True, 'sprintcalm': True}
g4 = {'__name__': 'v234'}
exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V234_20261028/verify234.py', encoding='utf8').read(), g4)
import unreal as u
B = g4['B']; graph = g4['graph']; pn = g4['pn']; tid = g4['tid']
# the earlier contracts expect the V2.26 / V2.32 reversal DBs and the V2.33 mouse scale 0.35: exactly these deliberate V2.35 values are accepted
def _deliberate(b):
    b = str(b)
    if E.get('rev') and ('SHM224_DB_JR' in b) and ('PSD_SHM235_JogRev' in b or 'abp226.SHM224_DB_JR' in b): return True
    if E.get('mouse') and b.startswith('BP_GR_Player writer') and "'mouse': 0.7" in b and "'pad': 1.0" in b and "'set_ctl': 1" in b: return True
    return False
bad = [b for b in g4['bad'] if not _deliberate(b)]
cdo = g4['cdo']; sda = g4['sda']
want = {'SHM224_DB_JRFwd': 'PSD_SHM235_JogRevFwd', 'SHM224_DB_JRFwdM': 'PSD_SHM235_JogRevFwd', 'SHM224_DB_JRBwd': 'PSD_SHM235_JogRevBwdX', 'SHM224_DB_JRBwdM': 'PSD_SHM235_JogRevBwdX'}
dbs = {k: cdo.get_editor_property(k).get_name() for k in want}
if E.get('rev') and dbs != want: bad.append('rev dbs %s' % dbs)
if bool(E.get('route')) != bool(sda.get_editor_property('RevOverHard')): bad.append('RevOverHard %s' % sda.get_editor_property('RevOverHard'))
if bool(E.get('gap')) != bool(sda.get_editor_property('RevGapKeep')): bad.append('RevGapKeep %s' % sda.get_editor_property('RevGapKeep'))
gm = float(u.get_default_object(u.load_asset('/Game/GraceRanger/BP_GR_Player').generated_class()).get_editor_property('GR233_RecMouseScale'))
gc = float(u.get_default_object(u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player').generated_class()).get_editor_property('GR233_RecMouseScale'))
if E.get('mouse') and (abs(gm - 0.7) > 1e-3 or abs(gc - 0.7) > 1e-3): bad.append('mouse scale %s / child %s' % (gm, gc))
comp = u.load_asset('/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent')
rt = [tid(pn(n)) for n in B.find_nodes(graph(comp, 'SHM_UpdateRouting'))]; rov = sum('RevOverHard' in t for t in rt)
if rov < 1 or len(rt) < 150: bad.append('routing census nodes %d revover %d' % (len(rt), rov))
ent = {}
for p in ('/Game/GraceRanger/SHME/Animations/V235/PSD_SHM235_JogRevFwd', '/Game/GraceRanger/SHME/Animations/V235/PSD_SHM235_JogRevBwdX'):
    d = u.load_asset(p); names = [d.get_animation_asset(i).get_name() for i in range(d.get_num_animation_assets())]
    ent[p.rsplit('/', 1)[1]] = [len(names), sum(n.startswith('SHM235_JogRev_') for n in names), round(d.get_editor_property('continuing_pose_cost_bias'), 3)]
    if sum(n.startswith('SHM235_JogRev_') for n in names) != 32 or abs(d.get_editor_property('continuing_pose_cost_bias') + 0.5) > 1e-3: bad.append('db %s %s' % (p, ent[p.rsplit('/', 1)[1]]))
f = os.path.join(u.Paths.project_content_dir(), 'GraceRanger/SHME/Animations/Stops/SHM_A_CP2_Jog_Fwd_Stop.uasset')
sha = hashlib.sha1(open(f, 'rb').read()).hexdigest()
if sha != '1323d4cf743b401ea9a69a5377cb73f932197a01': bad.append('stop clip is not the restored V2.34 file (re-plan rejected)')
print('VERIFY235 ' + json.dumps({'v234_bad': g4['bad'], 'dbs': dbs, 'revoverhard': sda.get_editor_property('RevOverHard'), 'mouse': [gm, gc], 'route_nodes': len(rt),
                                  'revover': rov, 'v235_dbs': ent, 'stop_sha1': sha, 'bad': bad, 'ALL_OK': not bad}, default=str))
