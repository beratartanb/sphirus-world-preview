# cm_gait1.py: gait calibration against the Core Motion clips (walk 197, jog 294, run 532 cm/s root speed).
# Speeds: walk 180 outdoors / 150 indoors (rate 0.91 / 0.76), jog 300 (1.02), run 500 (0.94), crouch 110.
# Shift hold to run 1.2 s -> 0.9 s. GR_GaitSel (0 walk, 1 jog, 2 run) written each tick for the driver's database choice. CMC: acceleration 450 (walk reaches speed in 0.4 s, run in 1.1 s as the start clips do),
# braking 650, rotation rate 260 deg/s. MM node: play rate 0.7-1.25. Trajectory: prediction 6 x 0.25 s (was 8 x 0.4 s).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
import re
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
def pv(p,k):
    try: return str(B.get_pin_value([x for x in info(p).input_pins if str(x.name)==k][0].pin_id))
    except Exception: return None
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); hits={}
    for p in N:
        for ip in info(p).input_pins:
            k=str(ip.name)
            try: v=str(B.get_pin_value(ip.pin_id))
            except Exception: continue
            if v in ('165.0','330.0','480.0') and tp(p).endswith('SelectFloat'):
                nv={'165.0':180.0,'330.0':300.0,'480.0':500.0}[v]; B.set_pin_value(ip.pin_id,str(nv)); hits.setdefault(v,0); hits[v]+=1
            if v=='1.2' and ('Greater' in tp(p) or 'Büyük' in tp(p) or '>' in tp(p)):
                B.set_pin_value(ip.pin_id,'0.9'); hits.setdefault('1.2',0); hits['1.2']+=1
    print('SPEEDHITS',hits); print('STEP speeds'); assert hits.get('165.0') and hits.get('330.0') and hits.get('480.0')
    # gait selector: the run AND node (ShiftT > x AND speed > 250) and GR_Gait == 1 feed Select nodes; write GR_GaitSel
    tick=[p for p in N if tp(p).endswith('Üst:Tick')][0]
    first=[(q,str(ip.name)) for q in N for ip in info(q).input_pins if (tick,'then') in src((q,str(ip.name)))]; assert first
    runs=[p for p in N if (tp(p).endswith('BooleanAND') or tp(p).endswith('ANDBoolean')) and any(pv(s[0],'B')=='250.0' for s in src((p,'B')))]; assert len(runs)==1,runs
    g1=[p for p in N if 'A' in [str(x.name) for x in info(p).input_pins] and pv(p,'B')=='1' and any(tp(s[0]).endswith('GetGR_Gait') for s in src((p,'A')))]; assert g1,'gait1'
    print('STEP found',len(first),len(runs),len(g1)); sel=(g.fn(M+'SelectInt',A=2,B=(g.fn(M+'SelectInt',A=1,B=0,bPickA=(g1[0],'ReturnValue')),'ReturnValue'),bPickA=(runs[0],'ReturnValue')),'ReturnValue')
    [disconnect(f_) for f_ in first]; t=g.set('GR_GaitSel',sel,(tick,'then'))
    for f_ in first: connect(t,f_)
    print('GAITSEL wired',len(first))
bp0=u.load_asset(PP)
if 'GR_GaitSel' not in [str(x) for x in B.list_variables(bp0)]: B.add_variable(bp0,'GR_GaitSel','int'); L.compile_blueprint(bp0)
del bp0; gc.collect()
run(PP,build); print('STEP pawn graph saved')
bp=u.load_asset(PP); cdo=u.get_default_object(bp.generated_class()); cm=cdo.get_editor_property('character_movement')
cm.set_editor_property('max_walk_speed',180.0); cm.set_editor_property('max_acceleration',450.0); cm.set_editor_property('braking_deceleration_walking',650.0); cm.set_editor_property('rotation_rate',u.Rotator(roll=0.0,pitch=0.0,yaw=260.0))
L.compile_blueprint(bp); assert EA.save_loaded_asset(bp,False); print('PAWN saved',cm.get_editor_property('rotation_rate'))
d=u.load_asset('/Game/Sphirus/Player/Anim/ABP_Sph_Driver'); ag=[g for g in B.list_graphs(d) if g.get_name()=='AnimGraph'][0]
for n in B.find_nodes(ag):
    cn=n.get_class().get_name()
    if 'MotionMatching' in cn:
        nd=n.get_editor_property('node'); t=str(nd.export_text())
        t=re.sub(r'PlayRateRangeOverride=\(Min=[0-9.]+,Max=[0-9.]+\)','PlayRateRangeOverride=(Min=0.700000,Max=1.250000)',t); t=re.sub(r'PlayRate=\(Min=[0-9.]+,Max=[0-9.]+\)','PlayRate=(Min=0.700000,Max=1.250000)',t)
        nd.import_text(t); n.set_editor_property('node',nd); print('MM rate 0.7-1.25')
    if 'HistoryCollector' in cn:
        nd=n.get_editor_property('node'); t=str(nd.export_text())
        t=t.replace('TrajectoryPredictionCount=8','TrajectoryPredictionCount=6').replace('PredictionSamplingInterval=0.400000','PredictionSamplingInterval=0.250000')
        nd.import_text(t); n.set_editor_property('node',nd); print('TRAJ 6x0.25')
L.compile_blueprint(d); print('ERR_D',errs(d)); assert not errs(d); assert EA.save_loaded_asset(d,False); print('DONE')
