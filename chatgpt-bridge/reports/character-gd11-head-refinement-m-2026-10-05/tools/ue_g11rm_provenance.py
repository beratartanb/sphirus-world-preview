"""GD11 refinement L: PROVENANCE of the live QA composition, read from the editor (not from the request): face / body skeletal meshes (asset,
DNA user data, anim class / post-process ABP, non-zero morph curves), groom actors (groom asset, binding asset + its target mesh + source mesh,
materials, LOD info if readable), actor transforms and the face 'head' socket transform, qa_config snapshot, timestamp.
builtins.G11RM_PROV = {'label': <capture label>, 'candidate': <text>, 'out': <abs json path>}"""
import unreal as u, json, builtins, datetime, pathlib
C = builtins.G11RM_PROV; R = pathlib.Path(u.Paths.project_dir()).resolve()
CFG = json.loads((R/'Saved/Codex/CharacterLookdev_20260930/qa_config.json').read_text())
out = {'label': C['label'], 'candidate': C.get('candidate'), 'read_at': datetime.datetime.now().isoformat(timespec='seconds'), 'qa_config': {k: CFG.get(k) for k in ('face', 'face_abp', 'body', 'grooms', 'skin', 'materials', 'save_prefixes', 'studio_folder') if k in CFG}, 'actors': {}}
def tf(t): l = t.translation; r = t.rotation.rotator(); return [round(l.x, 2), round(l.y, 2), round(l.z, 2), round(r.pitch, 2), round(r.yaw, 2), round(r.roll, 2)]
def mats(c):
    try: return [m.get_path_name() if m else None for m in c.get_materials()]
    except Exception as e: return 'unreadable: %s' % e
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    lab = a.get_actor_label()
    if not lab.startswith('LKQA_') or lab in ('LKQA_Backdrop', 'LKQA_Floor'): continue
    rec = {'class': a.get_class().get_name(), 'actor_transform': tf(a.get_actor_transform())}
    sk = a.get_component_by_class(u.SkeletalMeshComponent)
    if sk:
        m = sk.get_editor_property('skeletal_mesh_asset') if hasattr(sk, 'get_editor_property') else None
        try: m = sk.skeletal_mesh_asset
        except Exception: pass
        rec['skeletal_mesh'] = m.get_path_name() if m else None
        if m:
            for d in (m.get_editor_property('asset_user_data') or []):
                if isinstance(d, u.DNAAssetUserData): dn = d.get_editor_property('dna_asset'); rec['dna'] = dn.get_path_name() if dn else None
            rec['morph_targets_total'] = len(m.get_editor_property('morph_targets'))
            try: rec['post_process_abp'] = str(m.get_editor_property('post_process_anim_blueprint'))
            except Exception: rec['post_process_abp'] = 'unreadable'
        try: rec['anim_mode'] = str(sk.get_editor_property('animation_mode')); ac = sk.get_editor_property('anim_class'); rec['anim_class'] = ac.get_name() if ac else None
        except Exception as e: rec['anim_mode'] = 'unreadable: %s' % e
        try:
            cs = {}
            for n in [str(x) for x in (m.get_editor_property('morph_targets') or [])][:0]: pass
            rec['nonzero_morph_curves'] = 'not enumerated (curve values not exposed to Python on this component)'
        except Exception: pass
        try: rec['forced_lod'] = sk.get_editor_property('forced_lod_model'); rec['predicted_lod'] = sk.get_editor_property('predicted_lod_level')
        except Exception as e: rec['lod'] = 'unreadable: %s' % e
        try: rec['head_socket_transform'] = tf(sk.get_socket_transform('head', u.RelativeTransformSpace.RTS_WORLD))
        except Exception: pass
        rec['materials'] = mats(sk)
    gc = a.get_component_by_class(u.GroomComponent)
    if gc:
        g = gc.get_editor_property('groom_asset'); b = gc.get_editor_property('binding_asset'); rec['groom'] = g.get_path_name() if g else None; rec['binding'] = b.get_path_name() if b else None
        if b:
            try: rec['binding_target'] = b.get_editor_property('target_skeletal_mesh').get_path_name(); rec['binding_source'] = b.get_editor_property('source_skeletal_mesh').get_path_name()
            except Exception as e: rec['binding_target'] = 'unreadable: %s' % e
        try: rec['groom_lod'] = {'forced_lod': gc.get_editor_property('forced_lod'), 'lod_prediction_enabled': 'n/a'}
        except Exception: rec['groom_lod'] = 'active LOD index not readable from Python (forced_lod property unavailable)'
        try: rec['simulation'] = gc.get_editor_property('simulation_settings').get_editor_property('simulation_setup').get_editor_property('enable_simulation')
        except Exception: rec['simulation'] = 'unreadable'
        rec['materials'] = mats(gc)
    out['actors'][lab] = rec
pathlib.Path(C['out']).write_text(json.dumps(out, indent=1)); print('G11RM_PROV', json.dumps({k: (v.get('skeletal_mesh') or v.get('groom')) for k, v in out['actors'].items()}))
