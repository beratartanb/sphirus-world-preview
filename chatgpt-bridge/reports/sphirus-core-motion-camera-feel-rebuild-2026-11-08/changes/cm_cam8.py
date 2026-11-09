# cm_cam8.py: shoulder offset proportional to the arm length. The fixed 30-44 cm shoulder pushed the character to the
# left edge of the frame once the arm got short (action arm 70 -> character centre at ~13 % of the width, cut off at
# the edge in the chop video). Target: character centre near the left third at every arm length -> shoulder ~= 0.24 x arm:
#   indoor lerp 30-38 -> 21-27 (arm 85-115), outdoor lerp 36-44 -> 26-33 (arm 105-140), action 34 -> 17 (arm 70).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
def pv(p,k):
    try: return str(B.get_pin_value([x for x in info(p).input_pins if str(x.name)==k][0].pin_id))
    except Exception: return None
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); n=0
    for p in N:
        t=tp(p)
        if t.endswith('Lerp') or t.endswith('|Lerp'):
            a,b=pv(p,'A'),pv(p,'B')
            if (a,b)==('30.0','38.0'): value((p,'A'),21.0); value((p,'B'),27.0); n+=1; print('LERP indoor')
            if (a,b)==('36.0','44.0'): value((p,'A'),26.0); value((p,'B'),33.0); n+=1; print('LERP outdoor')
        if t.endswith('SelectFloat') and any('IsLookInputIgnored' in tp(s[0]) for s in src((p,'bPickA'))) and pv(p,'A')=='34.0':
            value((p,'A'),17.0); n+=1; print('ACTION shoulder')
    print('CHANGED',n); assert n>=3,n   # the speed lerps exist twice (indoor/outdoor pairs), so 3-5 edits are expected
run(PP,build); print('DONE')
