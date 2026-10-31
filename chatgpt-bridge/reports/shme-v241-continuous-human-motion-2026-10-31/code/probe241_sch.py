"""probe241_sch.py (measure job) - V2.41: channels / weights of the takeover entry schema and which databases use it. Prints SCHP241 {...}."""
import unreal as u, json
AR = u.AssetRegistryHelpers.get_asset_registry()
s = u.load_asset('/Game/GraceRanger/SHME/Animations/V239/PSS_SHM239_Takeover'); out = {'channels': []}
def ch(c, d=0):
    r = {'cls': c.get_class().get_name()}
    for k in ('weight', 'sample_time_offset', 'bone', 'sample_role', 'input_query_pose'):
        try: r[k] = str(c.get_editor_property(k))[:60]
        except Exception: pass
    try: r['sub'] = [ch(x, d + 1) for x in c.get_editor_property('sub_channels')]
    except Exception: pass
    return r
for c in s.get_editor_property('channels'): out['channels'].append(ch(c))
for k in ('sample_rate', 'data_preprocessor'):
    try: out[k] = str(s.get_editor_property(k))
    except Exception: pass
users = []
for d in AR.get_assets_by_path('/Game/GraceRanger/SHME/Animations', True):
    if str(d.asset_class_path.asset_name) != 'PoseSearchDatabase': continue
    deps = AR.get_dependencies(d.package_name, u.AssetRegistryDependencyOptions())
    if deps and any('PSS_SHM239_Takeover' in str(x) for x in deps): users.append(str(d.package_name))
out['users'] = users; out['n_users'] = len(users)
print('SCHP241 ' + json.dumps(out))
