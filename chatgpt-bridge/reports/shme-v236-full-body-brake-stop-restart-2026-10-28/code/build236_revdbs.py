"""build236_revdbs.py (editor job): V2.36 reversal databases from the whole-body clips (same membership rules as production / V2.35):
PSD_SHM236_JogRevFwd = F_B bins + REAR loops; PSD_SHM236_JogRevBwdX = B_F bins + REAR + A_CT_Jog_Fwd; PSD_SHM236L_LoadRevFwd = loaded F_B
bins (16) + REAR. Full BranchIn windows. Schema / biases from PSD_SHM224_JogRevBwdO (V2.26 builder). The loops get one more BranchIn track
(SHME_V236_*) -> they are in the write manifest. A/B: abp_flags SHM224_DB_JRFwd / JRFwdM -> Fwd, SHM224_DB_JRBwd / JRBwdM -> BwdX,
SHM230_DB_JRFwdL -> LoadRevFwd. builtins.V236_RDB = {'dry': bool}. Prints RDB226 {...}."""
import builtins, io
c = dict(getattr(builtins, 'V236_RDB', {}))
src = io.open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V226_20261024/build_v226_revdbs.py', encoding='utf8').read()
a = "PLAN = {'PSD_SHM226_JogRevBwd': [V + 'SHM226_JogRev_B_F_P%d' % k for k in range(NPH)] + REAR, 'PSD_SHM226_JogRevFwd': [V + 'SHM226_JogRev_F_B_P%d' % k for k in range(NPH)] + REAR}"
assert src.count(a) == 1
b = ("V = '/Game/GraceRanger/SHME/Animations/V236/'\n"
     "PLAN = {'PSD_SHM236_JogRevFwd': [V + 'SHM236_JogRev_F_B_P%d' % k for k in range(32)] + REAR,\n"
     "        'PSD_SHM236_JogRevBwdX': [V + 'SHM236_JogRev_B_F_P%d' % k for k in range(32)] + REAR + [CT + 'A_CT_Jog_Fwd'],\n"
     "        'PSD_SHM236L_LoadRevFwd': [V + 'SHM236L_LoadRev_F_B_P%d' % k for k in range(16) if k != 15] + [V + 'SHM236_JogRev_F_B_P30', V + 'SHM236_JogRev_F_B_P31'] + REAR}")   # loaded P15 failed its plan (28.6 cm planted drift): the rested whole-body bins of the same phase stand in (V2.32 fallback rule)
src = src.replace(a, b)
for x, y in (("tr = 'SHME_V226_' + n.replace('PSD_SHM226_', '')", "tr = 'SHME_V236_' + n.replace('PSD_SHM236_', '').replace('PSD_SHM236L_', 'L_')"),
             ("win = ln if 'JogRev' not in c else min(ENTRY, ln - 0.01)", "win = ln")):
    assert src.count(x) == 1, x; src = src.replace(x, y)
builtins.V226_DRY = bool(c.get('dry', True)); builtins.V226_ENTRY = 100.0; builtins.V226_NPH = 32
exec(compile(src, 'build236_revdbs.py', 'exec'), {'__name__': 'db236'})
