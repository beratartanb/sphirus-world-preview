import unreal as u
print("BGE", [m for m in dir(u.BlueprintGraphEditor) if not m.startswith("_")])
