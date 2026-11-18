#!/bin/bash
# perf18.sh <suffix>: matched real-time frame cost on the uphill trail (perf_cam.sh route, editor PIE): after / before (runtime revert of
# the 2026-11-18 changes: no light function, flat capsule base, slope layer off) / after again. Summaries with an_perf.py.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; S=$1
B="sun_=[a for a in u.GameplayStatics.get_all_actors_of_class(W,u.DirectionalLight) if a.get_name()=='DirectionalLight_0'][0].get_components_by_class(u.DirectionalLightComponent)[0]; sun_.set_light_function_material(None); PW.get_movement_component().set_editor_property('use_flat_base_for_floor_checks',True,u.PropertyAccessChangeNotifyMode.NEVER); [c for c in PW.get_components_by_class(u.ActorComponent) if c.get_name()=='SphMotion'][0].set_editor_property('SlopeOn',False,u.PropertyAccessChangeNotifyMode.NEVER)"
for r in a1 b1 a2 b2; do
  case $r in a*) X="pass";; b*) X="$B";; esac
  bash Tools/Camera_20261112/perf_cam.sh P18_${S}_$r True "$X" 2>&1 | tail -2
done
"/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" Tools/Camera_20261112/an_perf.py P18_${S}_a1 P18_${S}_b1 P18_${S}_a2 P18_${S}_b2 2>&1 | tail -40
echo PERF18_DONE
