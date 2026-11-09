# cm_turn5.py (write): turn-brake floor 0.15 -> 0.5. True-clip telemetry (P_phys_e seg 4/9, SphClip curves) showed the
# reversal spent 0.57 s in blends and then a 45-degree start-turn clip: with the limit at 0.15 x gait speed the capsule
# turned almost in place (<= 27 cm/s at 260 deg/s) and no Core Motion clip has that combination - the start-turn clips
# move 26->157 cm/s while turning 180 in 0.7 s. Floor 0.5 (<= 90 cm/s walking during the turn, arc radius ~20 cm)
# matches the source clips; the velocity-direction redirect (GroundFriction 3) and the brake stay.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
def pv(p,k):
    try: return str(B.get_pin_value([x for x in info(p).input_pins if str(x.name)==k][0].pin_id))
    except Exception: return None
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); n=0
    for p in N:
        if tp(p).endswith('MapRangeClamped') and pv(p,'InRangeA')=='25.0' and pv(p,'InRangeB')=='135.0' and pv(p,'OutRangeB')=='0.15': value((p,'OutRangeB'),0.5); n+=1
    print('CHANGED',n); assert n==1
run(PP,build); print('DONE')
