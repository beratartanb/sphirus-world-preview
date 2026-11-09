# cm_turn4.py (write): reversal brake without the gait-ease lag. Measured (P_phys_a seg 4): after W->S the capsule reached
# 99 cm/s at 0.5 s while still facing 120 deg off the travel direction, although GR_TurnScale had dropped to 0.15: the
# scale fed the TARGET of the 3/s max-speed ease (kept for gait changes), so the speed limit only fell slowly.
# New structure (no feedback): GR_SpeedBase = FInterpTo(GR_SpeedBase, gait target, dt, 3)   (gait ease on its own var)
#                              MaxWalkSpeed = GR_SpeedBase * GR_TurnScale                    (turn brake applied instantly)
# While the facing turns (260 deg/s, 0.7 s for 180) the limit is 0.15 x gait speed, so the body turns almost in place -
# the Core Motion start-turn clips (turn 180 in 0.7 s while accelerating 26->157) match that contract; the pack's pivot
# clips have no root yaw (q_prof) and cannot match an orient-to-movement capsule.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
bp0=u.load_asset(PP)
if 'GR_SpeedBase' not in [str(x) for x in B.list_variables(bp0)]: B.add_variable(bp0,'GR_SpeedBase','float')
L.compile_blueprint(bp0); del bp0; gc.collect(); print('STEP var')
def pv(p,k):
    try: return str(B.get_pin_value([x for x in info(p).input_pins if str(x.name)==k][0].pin_id))
    except Exception: return None
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id)
    sms=[p for p in N if tp(p).endswith('SetMaxWalkSpeed')]; assert len(sms)==1; sm=sms[0]
    fi=src((sm,'MaxWalkSpeed'))[0][0]; assert tp(fi).endswith('FInterpTo'),tp(fi); print('EASE',pv(fi,'InterpSpeed'))
    mul=src((fi,'Target'))[0][0]; assert 'Multiply' in tp(mul) or 'float*float' in tp(mul),tp(mul)
    gait=src((mul,'A'))[0]; scale=src((mul,'B'))[0]; print('GAIT src',tp(gait[0])[-30:],'SCALE src',tp(scale[0])[-30:])
    pre=src((sm,'execute')); assert len(pre)==1
    disconnect((fi,'Target')); connect(gait,(fi,'Target'))
    disconnect((fi,'Current')); connect(g.get('GR_SpeedBase'),(fi,'Current'))
    disconnect((sm,'execute')); t=g.set('GR_SpeedBase',(fi,'ReturnValue'),pre[0]); connect(t,(sm,'execute'))
    disconnect((sm,'MaxWalkSpeed')); m2=g.fn(M+'Multiply_DoubleDouble',A=g.get('GR_SpeedBase'),B=g.get('GR_TurnScale')); connect((m2,'ReturnValue'),(sm,'MaxWalkSpeed'))
    print('STEP rewired')
run(PP,build)
bp=u.load_asset(PP); cdo=u.get_default_object(bp.generated_class()); cdo.set_editor_property('GR_SpeedBase',180.0)
L.compile_blueprint(bp); assert EA.save_loaded_asset(bp,False); print('DONE')
