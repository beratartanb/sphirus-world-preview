"""verify236.py (fresh editor, read-only, SHME_KIND=measure): every earlier contract (verify235 -> verify234) plus V2.36: ABP database variables
per promoted group, the Update_MotionMatching hooks (CallFunction_42 + Select_3 read SHM236_DB_JogStop, CallFunction_40 reads SHM236_DB_JogResume),
V2.36 database entry lists / biases, SHM_StopSettle on every stop bin. builtins.V236_EXP = {group: True}. Earlier V2.35 rev DB expectations
are accepted when 'rev' is promoted to the V2.36 DBs. Prints VERIFY236."""
import builtins, json
E = dict(getattr(builtins, 'V236_EXP', {}))
builtins.V235_EXP = {'rev': True, 'route': True, 'gap': True, 'mouse': True}
g5 = {'__name__': 'v235'}
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V235_20261028/verify235.py', encoding='utf8').read(), g5)
import unreal as u
v5 = json.loads(buf.getvalue().split('VERIFY235 ', 1)[1].strip().splitlines()[0])
def _deliberate(b):
    b = str(b)
    if E.get('rev') and (b.startswith('rev dbs') or 'SHM224_DB_JR' in b) and 'PSD_SHM236_JogRev' in b: return True
    if E.get('load') and 'SHM230_DB_JRFwdL' in b and 'PSD_SHM236L_LoadRevFwd' in b: return True     # V2.31 contract expected the V2.31 loaded DB
    return False
bad = [b for b in v5['bad'] if not _deliberate(b)]
B = g5['B']; graph = g5['graph']; pn = g5['pn']
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
abp = u.load_asset(AP); cdo = u.get_default_object(abp.generated_class())
V6 = 'PSD_SHM236_'
want = {'stop': {'SHM236_DB_JogStop': ('PSD_SHM236_JogStop2', 'PSD_CP2_JogStop')},
        'start': {'SHM_JogStartDB_L': ('PSD_SHM236_JogStartS_L', 'PSD_SHM_JogStartS_L'), 'SHM_JogStartDB_R': ('PSD_SHM236_JogStartS_R', 'PSD_SHM_JogStartS_R')},
        'rev': {'SHM224_DB_JRFwd': ('PSD_SHM236_JogRevFwd', 'PSD_SHM235_JogRevFwd'), 'SHM224_DB_JRFwdM': ('PSD_SHM236_JogRevFwd', 'PSD_SHM235_JogRevFwd'),
                'SHM224_DB_JRBwd': ('PSD_SHM236_JogRevBwdX', 'PSD_SHM235_JogRevBwdX'), 'SHM224_DB_JRBwdM': ('PSD_SHM236_JogRevBwdX', 'PSD_SHM235_JogRevBwdX')},
        'load': {'SHM230_DB_JRFwdL': ('PSD_SHM236L_LoadRevFwd', 'PSD_SHM231L_LoadRevFwd')},
        'resume': {'SHM236_DB_JogResume': ('PSD_SHM236_JogResume', 'PSD_CP2_JogStart')}}
vars_ = {}
for g, kv in want.items():
    for k, (on, off) in kv.items():
        v = cdo.get_editor_property(k).get_name(); vars_[k] = v
        if v != (on if E.get(g) else off): bad.append('%s %s = %s' % (g, k, v))
# graph hooks
from qa_graph import info, src
gp = graph(abp, 'Update_MotionMatching'); nodes = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(gp)}
hooks = {}
for nd, pin, var in (('K2Node_CallFunction_42', 'Database', 'SHM236_DB_JogStop'), ('K2Node_Select_3', 'Option 0', 'SHM236_DB_JogStop'), ('K2Node_CallFunction_40', 'Database', 'SHM236_DB_JogResume')):
    s_ = [x[1] for x in src((nodes[nd], pin))]; hooks[nd] = s_
    if var not in s_: bad.append('hook %s.%s -> %s' % (nd, pin, s_))
ents = {}
V = '/Game/GraceRanger/SHME/Animations/V236/'
for n, need_pre, need_n, bias in (('PSD_SHM236_JogStop2', 'SHM236_JogStop_', 24, -3.0), ('PSD_SHM236_JogStartS_L', 'SHM236_JogStart_F_L', 1, None), ('PSD_SHM236_JogStartS_R', 'SHM236_JogStart_F_R', 1, None),
                                  ('PSD_SHM236_JogRevFwd', 'SHM236_JogRev_F_B', 32, -0.5), ('PSD_SHM236_JogRevBwdX', 'SHM236_JogRev_B_F', 32, -0.5), ('PSD_SHM236L_LoadRevFwd', 'SHM236L_LoadRev', 15, None),
                                  ('PSD_SHM236_JogResume', 'A_CT_Jog_Fwd', 1, None)):
    d = u.load_asset(V + n); names = [d.get_animation_asset(i).get_name() for i in range(d.get_num_animation_assets())]
    c = sum(x.startswith(need_pre) for x in names); b = round(d.get_editor_property('continuing_pose_cost_bias'), 3); ents[n] = [len(names), c, b]
    if c != need_n or (bias is not None and abs(b - bias) > 1e-3): bad.append('db %s %s' % (n, ents[n]))
AL = u.AnimationLibrary; miss = []
d = u.load_asset(V + 'PSD_SHM236_JogStop2')
for i in range(d.get_num_animation_assets()):
    a = d.get_animation_asset(i)
    if 'SHM_StopSettle' not in [str(x) for x in AL.get_animation_curve_names(a, u.RawCurveTrackTypes.RCT_FLOAT)]: miss.append(a.get_name())
if miss: bad.append('StopSettle missing %s' % miss[:4])
print('VERIFY236 ' + json.dumps({'v235_bad': v5['bad'], 'vars': vars_, 'hooks': hooks, 'dbs': ents, 'bad': bad, 'ALL_OK': not bad}, default=str))
