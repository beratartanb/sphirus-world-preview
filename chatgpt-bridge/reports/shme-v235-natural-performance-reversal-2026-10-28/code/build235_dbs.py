"""build235_dbs.py (editor job): V2.35 jog reversal databases from the support-exchange clips (gen235_rev.py), same membership rules as
production: PSD_SHM235_JogRevFwd = F_B bins + the REAR loops (= PSD_SHM226_JogRevFwd layout); PSD_SHM235_JogRevBwdX = B_F bins + REAR + the
forward exit loop A_CT_Jog_Fwd (= PSD_SHM232_JogRevBwdX layout). Full BranchIn windows (entry-window trap). Schema / biases from
PSD_SHM224_JogRevBwdO (V2.26 builder). The loops get one more BranchIn track (SHME_V235_*) -> they are in the write manifest.
A/B: abp_flags SHM224_DB_JRFwd / JRFwdM -> Fwd, SHM224_DB_JRBwd / JRBwdM -> BwdX. builtins.V235_DB = {'dry': bool}. Prints RDB226 {...}."""
import builtins, io
c = dict(getattr(builtins, 'V235_DB', {}))
src = io.open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V226_20261024/build_v226_revdbs.py', encoding='utf8').read()
a = "PLAN = {'PSD_SHM226_JogRevBwd': [V + 'SHM226_JogRev_B_F_P%d' % k for k in range(NPH)] + REAR, 'PSD_SHM226_JogRevFwd': [V + 'SHM226_JogRev_F_B_P%d' % k for k in range(NPH)] + REAR}"
assert src.count(a) == 1
b = ("V = '/Game/GraceRanger/SHME/Animations/V235/'\n"
     "PLAN = {'PSD_SHM235_JogRevFwd': [V + 'SHM235_JogRev_F_B_P%d' % k for k in range(32)] + REAR,\n"
     "        'PSD_SHM235_JogRevBwdX': [V + 'SHM235_JogRev_B_F_P%d' % k for k in range(32)] + REAR + [CT + 'A_CT_Jog_Fwd']}")
src = src.replace(a, b)
for x, y in (("tr = 'SHME_V226_' + n.replace('PSD_SHM226_', '')", "tr = 'SHME_V235_' + n.replace('PSD_SHM235_', '')"),
             ("win = ln if 'JogRev' not in c else min(ENTRY, ln - 0.01)", "win = ln")):
    assert src.count(x) == 1, x; src = src.replace(x, y)
builtins.V226_DRY = bool(c.get('dry', True)); builtins.V226_ENTRY = 100.0; builtins.V226_NPH = 32
exec(compile(src, 'build235_dbs.py', 'exec'), {'__name__': 'db235'})
