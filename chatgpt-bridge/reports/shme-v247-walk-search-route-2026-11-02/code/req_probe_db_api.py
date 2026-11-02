import unreal as u, json
P = '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/PSD_Dense_Stand_Walk_Loops'; db = u.load_asset(P)
out = {'entries': [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]}
out['methods'] = [m for m in dir(db) if not m.startswith('_') and any(k in m.lower() for k in ('asset', 'remove', 'add', 'anim', 'entry', 'index'))]
try: out['props_anim'] = str(db.get_editor_property('animation_assets'))[:200]
except Exception as e: out['props_anim'] = 'ERR ' + str(e)[:80]
for cand in ('AnimationAssets', 'animation_assets', 'Entries', 'database_assets'):
    try: out['prop_' + cand] = str(db.get_editor_property(cand))[:120]
    except Exception as e: out['prop_' + cand] = 'ERR ' + str(e)[:60]
out['lib'] = [m for m in dir(u) if 'PoseSearch' in m and ('Library' in m or 'Util' in m)]
print('DBAPI247 ' + json.dumps(out))
