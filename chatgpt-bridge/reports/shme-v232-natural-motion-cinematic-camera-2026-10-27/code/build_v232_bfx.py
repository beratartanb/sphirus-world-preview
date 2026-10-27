"""build_v232_bfx.py (editor job) - V2.32 A: B_F (backpedal -> forward) reversal databases WITH their exit loop. The production
PSD_SHM226_JogRevBwd (and the V2.31 slow / loaded B_F DBs) hold the B_F bins + the REAR loops only (build_v226_revdbs PLAN): when an authored
B_F clip ends, the episode ends one frame later (SHME PostPhysics, the ABP reads it next frame) and that frame's search in the B_F DB finds
no forward loop -> it picks ANOTHER B_F bin at its end pose (another loop phase) for one frame (blip232: 61 of 139 blips in 82 V2.31 runs;
visible balls jump 440-640 cm/s). The F_B DBs already hold their exit loop (rear) and never blip. New DBs (V232 folder, nothing in
production edited): <same bins> + REAR + the forward exit loop (jog: A_CT_Jog_Fwd; slow: A_CT_Walk_Fwd). A/B through SHM224_DB_JRBwd /
JRBwdM / SHM230_DB_JRBwdL / SHM231_DB_JRBwdS. builtins.V232_BFX = {'dry': bool}. Prints RDB226 {...} (the V2.26 builder)."""
import builtins, io
c = dict(getattr(builtins, 'V232_BFX', {}))
src = io.open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V226_20261024/build_v226_revdbs.py', encoding='utf8').read()
a = "PLAN = {'PSD_SHM226_JogRevBwd': [V + 'SHM226_JogRev_B_F_P%d' % k for k in range(NPH)] + REAR, 'PSD_SHM226_JogRevFwd': [V + 'SHM226_JogRev_F_B_P%d' % k for k in range(NPH)] + REAR}"
assert src.count(a) == 1
b = ("V1 = '/Game/GraceRanger/SHME/Animations/V231/'\n"
     "PLAN = {'PSD_SHM232_JogRevBwdX': [V + 'SHM226_JogRev_B_F_P%d' % k for k in range(32)] + REAR + [CT + 'A_CT_Jog_Fwd'],\n"
     "        'PSD_SHM232_LoadRevBwdX': [V1 + 'SHM231L_LoadRev_B_F_P%d' % k for k in range(32)] + REAR + [CT + 'A_CT_Jog_Fwd'],\n"
     "        'PSD_SHM232_SlowRevBwdX': [V1 + 'SHM231S_SlowRev_B_F_P%d' % k for k in range(16)] + REAR + [CT + 'A_CT_Walk_Fwd', CT + 'A_CT_Jog_Fwd']}\n"
     "PLAN = {k: [p for p in v if EAL.does_asset_exist(p)] for k, v in PLAN.items()}\n"
     "V = '/Game/GraceRanger/SHME/Animations/V232/'")
src = src.replace(a, b)
for x, y in (("tr = 'SHME_V226_' + n.replace('PSD_SHM226_', '')", "tr = 'SHME_V232_' + n.replace('PSD_SHM232_', '')"),
             ("win = ln if 'JogRev' not in c else min(ENTRY, ln - 0.01)", "win = ln if not any(k in c for k in ('JogRev_', 'LoadRev_', 'SlowRev_')) else min(ENTRY, ln - 0.01)")):
    assert src.count(x) == 1, x; src = src.replace(x, y)
builtins.V226_DRY = bool(c.get('dry', True)); builtins.V226_ENTRY = 100.0; builtins.V226_NPH = 32
exec(compile(src, 'build_v232_bfx.py', 'exec'), {'__name__': 'bfx232'})
