import unreal as u
c=getattr(u,"InputDeviceSubsystem",None)
print("IDS", c, [m for m in dir(c) if "recent" in m.lower() or "device" in m.lower()][:20] if c else None)
print("HDI", [m for m in dir(getattr(u,"HardwareDeviceIdentifier",object)) if not m.startswith("_")][:30])
