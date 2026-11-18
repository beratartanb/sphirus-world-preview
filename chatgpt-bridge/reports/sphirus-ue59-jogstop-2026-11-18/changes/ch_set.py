# ch_set.py (runtime/in-memory only, no save): set the Stand Idles stop speed bands of the Sphirus Relaxed chooser.
# builtins.CH_EDGES = (walk_run_edge, run_sprint_edge); (170, 400) = shipped values. Prints the resulting row ranges.
import unreal as u, builtins, re
u.load_asset('/Game/Sphirus/Player/GASP/Choosers/CHT_Sph_PoseSearchDatabases_Relaxed')
s_ = u.find_object(None, '/Game/Sphirus/Player/GASP/Choosers/CHT_Sph_PoseSearchDatabases_Relaxed.CHT_Sph_PoseSearchDatabases_Relaxed:Stand Idles')
cols_ = list(s_.get_editor_property('columns_structs')); t_ = cols_[0].export_text(); assert 'Speed2D' in t_, t_[:200]
a_, b_ = getattr(builtins, 'CH_EDGES', (170, 400))
rv_ = re.search(r'RowValues=\((.*?)\)\),bDisabled', t_)
t2_ = re.sub(r'\(Min=20\.000000,Max=[0-9.]+\),\(Min=[0-9.]+,Max=[0-9.]+\),\(Min=[0-9.]+,Max=999',
             '(Min=20.000000,Max=%.6f),(Min=%.6f,Max=%.6f),(Min=%.6f,Max=999' % (a_, a_, b_, b_), t_)
assert t2_ != t_ or (a_, b_) == tuple(float(x) for x in re.findall(r'\(Min=20\.000000,Max=([0-9.]+)\),\(Min=[0-9.]+,Max=([0-9.]+)\)', t_)[0]), 'pattern'
cols_[0].import_text(t2_); s_.set_editor_property('columns_structs', cols_, u.PropertyAccessChangeNotifyMode.NEVER)
print('CHSET', re.search(r'RowValues=\(\(Max=20\.000000\),(\(Min[^)]*\),\(Min[^)]*\),\(Min[^)]*\))', s_.get_editor_property('columns_structs')[0].export_text()).group(1))
