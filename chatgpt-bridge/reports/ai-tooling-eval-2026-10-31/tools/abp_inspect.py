"""Read-only inspection of the two dirty AnimBlueprints (measure job: no save, no revert, no compile, no graph probes).

1. Dirty flag, on-disk file hash vs the last V2.40 write manifest (blk2.state.json).
2. CDO values of every ABP key the QA harness touched this session vs the production value the harness captured when it first
   touched the key (builtins.SHM_PROD_TOUCHED['abp'], i.e. the value loaded from disk). Equal = in-memory defaults are production.
3. The V2.40 knob defaults that verify240 checks.
4. Blueprint status (up to date / dirty / error) as reported by the editor.
Output: <OUT>/abp_inspect.json
"""
import unreal as u, json, os, hashlib, builtins

OUT = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\t1b'
os.makedirs(OUT, exist_ok=True)
ABPS = ['/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching',
        '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase']
PROJ = u.Paths.convert_relative_path_to_full(u.Paths.project_dir())
MAN = os.path.join(PROJ, 'Saved/Codex/SHME_V240_20261030/checkpoint/manifests/blk2.state.json')
KNOBS = {'SHM239_Own': 0.0, 'SHM240_ExtOn': 0.0, 'SHM240_HeadOn': 0.0, 'SHM240_YSpd': 80.0, 'SHM240_BlkSpd': 60.0, 'SHM240_AOFadeRate': 4.0}


def norm(v):
    if hasattr(v, 'get_path_name') and not isinstance(v, str):
        return v.get_path_name()
    if isinstance(v, float):
        return round(v, 6)
    if hasattr(v, 'x') and hasattr(v, 'z'):
        return [round(v.x, 4), round(v.y, 4), round(v.z, 4)]
    return v if isinstance(v, (int, bool, str, type(None))) else str(v)


dirty = sorted(p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages())
man = json.load(open(MAN))
res = {'dirty_content_packages': dirty, 'abps': {}}
touched = (getattr(builtins, 'SHM_PROD_TOUCHED', None) or {}).get('abp', {})
res['harness_session_state_present'] = getattr(builtins, 'SHM_PROD_TOUCHED', None) is not None
res['harness_dirty_base_at_first_run'] = getattr(builtins, 'SHM_PROD_DIRTY_BASE', None)
for path in ABPS:
    bp = u.load_asset(path)
    cdo = u.get_default_object(bp.generated_class())
    f = os.path.join(PROJ, 'Content', path[len('/Game/'):] + '.uasset')
    sha = hashlib.sha1(open(f, 'rb').read()).hexdigest()
    row = {'dirty': path in dirty, 'disk_sha1': sha, 'manifest_blk2_sha1': man.get(path), 'disk_equals_last_v240_write': sha == man.get(path),
           'disk_mtime': os.path.getmtime(f)}
    try:
        row['bp_status'] = str(bp.get_editor_property('status'))
    except Exception as ex:
        row['bp_status'] = 'n/a %s' % ex
    # harness-touched keys: production (first-touch) value vs current CDO value
    # qa_pie layout: SHM_PROD_TOUCHED['abp'][key][path] = production value; restore happens at the START of the next run
    tk = {k: v[path] for k, v in touched.items() if isinstance(v, dict) and path in v} if isinstance(touched, dict) else {}
    cmp = {}
    for k, prod in tk.items():
        try:
            cur = norm(cdo.get_editor_property(k))
        except Exception as ex:
            cur = 'ERR %s' % ex
        cmp[k] = {'production': prod, 'current': cur, 'equal': cur == prod}
    row['harness_touched_keys'] = cmp
    row['harness_touched_all_equal'] = all(v['equal'] for v in cmp.values()) if cmp else None
    kn = {}
    for k, exp in KNOBS.items():
        try:
            kn[k] = norm(cdo.get_editor_property(k))
        except Exception:
            pass
    for k in ('SHM240_BlkDB',):
        try:
            kn[k] = norm(cdo.get_editor_property(k))
        except Exception:
            pass
    row['v240_knobs_current'] = kn
    res['abps'][path] = row
res['v240_knob_expected'] = dict(KNOBS, SHM240_BlkDB='.../Dense/PSD_Dense_Stand_Idles')
json.dump(res, open(os.path.join(OUT, 'abp_inspect.json'), 'w'), indent=1, default=str)
print('ABP_INSPECT', json.dumps({p.rsplit('/', 1)[-1]: {'dirty': r['dirty'], 'disk_eq_v240': r['disk_equals_last_v240_write'],
                                                        'touched': len(r['harness_touched_keys']), 'all_equal': r['harness_touched_all_equal'],
                                                        'knobs': r['v240_knobs_current']} for p, r in res['abps'].items()}, default=str))
