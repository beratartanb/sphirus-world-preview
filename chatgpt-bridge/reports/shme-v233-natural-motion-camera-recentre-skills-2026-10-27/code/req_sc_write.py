import builtins, unreal as u
bp = u.load_asset("/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase")
db = u.get_default_object(bp.generated_class()).get_editor_property("SHM211_DB_Sprint")
print("SPRINTDB", db.get_path_name())
builtins.SC233 = {"dry": False, "db": db.get_path_name().split(".")[0]}
exec(open(r"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V233_20261027/gen233_sprintcalm.py", encoding="utf8").read())
