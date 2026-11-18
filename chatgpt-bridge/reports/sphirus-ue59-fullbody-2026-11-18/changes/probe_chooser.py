# probe_chooser.py (read-only): dump the Relaxed locomotion chooser (columns, rows touching stop databases)
import unreal as u
c = u.load_asset('/Game/Sphirus/Player/GASP/Choosers/CHT_Sph_PoseSearchDatabases_Relaxed'); o = ['CLASS %s' % c.get_class().get_name()]
for n in sorted(dir(c)):
    if n.startswith('_'): continue
    try: v = c.get_editor_property(n)
    except Exception: continue
    s = v.export_text() if hasattr(v, 'export_text') else str(v)
    o.append('PROP %s = %s' % (n, s[:300]))
try:
    for i, col in enumerate(c.get_editor_property('columns_structs')):
        o.append('COL %d %s' % (i, col.export_text()[:3000] if hasattr(col, 'export_text') else str(col)[:3000]))
except Exception as e: o.append('COLS ? %s' % e)
try:
    rd = c.get_editor_property('result_data')
    for i, r in enumerate(rd): o.append('ROW %d %s' % (i, (r.export_text() if hasattr(r, 'export_text') else str(r))[:400]))
except Exception as e: o.append('ROWS ? %s' % e)
open(u.Paths.project_dir() + 'Saved/UE59Work/probe/chooser.txt', 'w', encoding='utf8').write('\n'.join(o)); print('CHOOSER', len(o))
