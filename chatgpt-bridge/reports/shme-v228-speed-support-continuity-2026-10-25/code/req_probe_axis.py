import unreal as u, json
out = {"Axis": [x for x in dir(u.Axis) if not x.startswith("_")][:20]}
LS = u.EditorLoadingAndSavingUtils; out["dirty"] = [p.get_name() for p in LS.get_dirty_content_packages()]
bp = u.load_asset("/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase")
for n in u.BlueprintEditorLibrary.find_nodes(u.BlueprintEditorLibrary.get_graph(bp, "AnimGraph")) if hasattr(u.BlueprintEditorLibrary, "find_nodes") else []:
    pass
print("AXIS228 " + json.dumps(out))
