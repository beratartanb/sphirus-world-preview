import unreal as u
db = u.load_asset("/Game/GraceRanger/SHME/Animations/Starts/PSD_SHM_JogStartQ_R")
print("DBAPI", [m for m in dir(db) if "anim" in m.lower() or "asset" in m.lower() or "remove" in m.lower()])
