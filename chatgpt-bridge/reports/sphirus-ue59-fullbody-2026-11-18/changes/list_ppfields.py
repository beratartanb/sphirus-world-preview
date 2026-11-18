# list_ppfields.py (read-only): post process settings fields related to exposure / tonemapping / local exposure in this build
import unreal as u
s = u.PostProcessSettings(); o = [n for n in dir(s) if not n.startswith('_') and not n.startswith('override_') and any(k in n for k in ('exposure', 'film', 'tonemap', 'local', 'histogram', 'bloom_intensity', 'eye'))]
open(u.Paths.project_dir() + 'Saved/UE59Work/probe/ppfields.txt', 'w').write('\n'.join(o)); print('PPFIELDS', len(o))
