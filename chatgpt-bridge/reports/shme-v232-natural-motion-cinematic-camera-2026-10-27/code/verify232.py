"""verify232.py (fresh editor, read-only): every earlier contract (verify231 -> verify230 -> V2.29 groups) plus V2.32. builtins.V232_EXP =
{group: True} (the promoted groups, promote232 names) and builtins.V232_EXPV = {DA/ABP key: expected value} for the promoted values.
V2.31 items superseded by a promoted V2.32 group are dropped with the reason (loadedbf: SHM230_DB_JRBwdL is the V2.32 loaded B_F DB).
V2.32 checks: DA knobs; ABP DB routes / StartBind; IntentTickPrePhysics stays false (tick order rejected); BP_GR_Player orbit wiring
(var, GR_UpdateSHMSignals setter, boom MakeRotator yaw = sum); component functions hold the orbit / T6 / T7 nodes; the X DBs hold their
forward exit loop; PSD_SHM231L_LoadRevFwd = 30 loaded bins + the P21 / P30 production fallback; the idle-stance start copies are in their
start databases. Prints VERIFY232 {... ALL_OK}."""
import builtins, json
X = dict(getattr(builtins, 'V232_EXP', {})); XV = dict(getattr(builtins, 'V232_EXPV', {}))
builtins.V231_EXP = {'slow': True, 'exit': True, 'fwdrev': True, 'inspect': True, 'steplift': True, 'tipend': True, 'loaded': True}
g = {'__name__': 'v231'}
exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V231_20261026/verify231.py', encoding='utf8').read(), g)
import unreal as u
bad = list(g.get('bad', []))
if X.get('loadedbf'): bad = [b for b in bad if not b.startswith('SHM230_DB_JRBwdL=')]   # superseded: the loaded B_F family DB (V2.32)
if X.get('bfexit'): bad = [b for b in bad if not b.startswith(('SHM224_DB_JRBwd=', 'SHM224_DB_JRBwdM=', 'v226:abp226.SHM224_DB_JRBwd'))]   # superseded: B_F DBs with the exit loop (V2.32; new values checked through V232_EXPV)
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); cdo = u.get_default_object(bp.generated_class()); sda = u.load_asset('/Game/GraceRanger/SHME/DA_SHM_Response_Default')
B = g['B']; graph = g['graph']; pn = g['pn']; tid = g['tid']
k = {}
for key, want in XV.items():
    src = sda if key.startswith(('Cam', 'Swing', 'Intent')) else cdo
    try: v = src.get_editor_property(key)
    except Exception as e: bad.append('missing %s' % key); continue
    vs = v.get_name() if hasattr(v, 'get_name') else v
    k[key] = vs
    if isinstance(want, (int, float)) and not isinstance(want, bool):
        if abs(float(vs) - float(want)) > 1e-4: bad.append('%s=%s want %s' % (key, vs, want))
    elif vs != want: bad.append('%s=%s want %s' % (key, vs, want))
if bool(sda.get_editor_property('IntentTickPrePhysics')): bad.append('IntentTickPrePhysics true (rejected in V2.32)')
gp = u.load_asset('/Game/GraceRanger/BP_GR_Player')
vl = [str(v) for v in B.list_variables(gp)]
sig = [tid(pn(n)) for n in B.find_nodes(graph(gp, 'GR_UpdateSHMSignals'))]
rig = graph(gp, 'GR_UpdateRig'); rn = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(rig)}
from qa_graph import src as qsrc
mk = rn.get('K2Node_CallFunction_43'); ysrc = [tid(a) for a, b in qsrc((mk, 'Yaw'))] if mk else []
orb = {'var': 'GR_SHM_CamOrbit' in vl, 'setter': any(t.endswith('SetGR_SHM_CamOrbit') for t in sig), 'boom_yaw_sum': any('DotProduct' in t or 'Dot_Vector' in t for t in ysrc)}
if not all(orb.values()): bad.append('orbit wiring %s' % orb)
comp = u.load_asset('/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent')
cam = [tid(pn(n)) for n in B.find_nodes(graph(comp, 'SHM_UpdateCameraV21'))]
bt = [tid(pn(n)) for n in B.find_nodes(graph(comp, 'SHM_UpdateBodyTargets'))]
fn = {'cam_orbit_nodes': sum('CamOrbit' in t for t in cam), 't6_nodes': sum('SHM232_PelvMean' in t for t in bt), 't7_nodes': sum('SHM232_FootH0' in t for t in bt)}
if fn['cam_orbit_nodes'] < 6: bad.append('camera function orbit nodes %s' % fn)
if X.get('swingpelvis') and fn['t6_nodes'] < 2: bad.append('T6 nodes %s' % fn)
if X.get('floorguard') and fn['t7_nodes'] < 2: bad.append('T7 nodes %s' % fn)
# V2.32: no LINKED Pawn.LastHitBy getter (DSL translator bug: control rotation read through a None pawn member) in the component
from qa_graph import info as qinfo
def lhb_linked(bp):
    h = {}
    for g_ in B.list_graphs(bp):
        gn = g_.get_name()
        try: k_ = sum(1 for n in B.find_nodes(graph(bp, gn)) if tid(pn(n)).endswith('|GetLastHitBy') and any(o.connected_pins for o in qinfo(pn(n)).output_pins))
        except Exception: k_ = 0
        if k_: h[gn] = k_
    return h
fn['lasthitby_linked'] = {'component': lhb_linked(comp), 'abp': lhb_linked(bp), 'player': lhb_linked(gp)}
if any(fn['lasthitby_linked'].values()): bad.append('linked LastHitBy %s' % fn['lasthitby_linked'])
V = '/Game/GraceRanger/SHME/Animations/'
dbs = {}
def names(p):
    d = u.load_asset(p); return [d.get_animation_asset(i).get_name() for i in range(d.get_num_animation_assets())] if d else []
for p, need in ((V + 'V232/PSD_SHM232_JogRevBwdX', 'A_CT_Jog_Fwd'), (V + 'V232/PSD_SHM232_LoadRevBwdX', 'A_CT_Jog_Fwd'), (V + 'V232/PSD_SHM232_SlowRevBwdX', 'A_CT_Jog_Fwd')):
    n = names(p); dbs[p.rsplit('/', 1)[-1]] = {'n': len(n), 'exit_loop': need in n}
    if X.get('bfexit') and not (n and need in n): bad.append('X db %s %s' % (p, dbs[p.rsplit('/', 1)[-1]]))
lf = names(V + 'V231/PSD_SHM231L_LoadRevFwd')
dbs['LoadRevFwd'] = {'loaded': sum(x.startswith('SHM231L_LoadRev_F_B') for x in lf), 'fallback': sorted(x for x in lf if x.startswith('SHM226_JogRev_F_B'))}
if dbs['LoadRevFwd']['loaded'] != 30 or dbs['LoadRevFwd']['fallback'] != ['SHM226_JogRev_F_B_P21', 'SHM226_JogRev_F_B_P30']: bad.append('LoadRevFwd %s' % dbs['LoadRevFwd'])
isn = names('/Game/GraceRanger/SHME/Animations/Starts/PSD_SHM_JogStartQ_R'); dbs['JogStartQ_R_IS'] = sum(x.startswith('SHM232_IS_') for x in isn)
if X.get('idlestart') and dbs['JogStartQ_R_IS'] < 1: bad.append('idle-stance start copies missing in PSD_SHM_JogStartQ_R')
print('VERIFY232 ' + json.dumps({'v231_bad_raw': g.get('bad', []), 'knobs': k, 'orbit_wiring': orb, 'functions': fn, 'dbs': dbs, 'bad': bad, 'ALL_OK': not bad}, default=str))
