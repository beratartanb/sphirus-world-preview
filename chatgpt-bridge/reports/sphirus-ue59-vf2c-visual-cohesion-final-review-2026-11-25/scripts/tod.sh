#!/bin/bash
# tod.sh <tag> <sun pitch> <sun yaw> <sun lux> <sun kelvin> <sky intensity>: PIE-only lighting condition, four fixed views. Nothing is saved.
cd "<PROJECT>"
export PRE="sun=u.GameplayStatics.get_all_actors_of_class(W,u.DirectionalLight)[0]; sky=u.GameplayStatics.get_all_actors_of_class(W,u.SkyLight)[0]; sun.set_actor_rotation(u.Rotator(pitch=$2,yaw=$3,roll=0),False); c=sun.light_component; c.set_intensity($4); c.set_temperature($5); s=sky.light_component; s.set_intensity($6); s.recapture_sky(); print('PRE tod $1 ok')"
bash Tools/VF2_20261124/vf2_world_tour.sh tod_$1 Tools/VF2C_20261125/views_tod.txt 2>&1 | grep -E "SLOT|PRE|fps" | cut -c1-40
