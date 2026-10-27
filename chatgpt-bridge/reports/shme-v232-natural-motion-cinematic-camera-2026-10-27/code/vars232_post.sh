# vars232_post.sh (appended to vars232.sh for the post-promotion chains): the V2.32 "before" through flags. pre232 = production with every
# promoted V2.32 knob at its V2.31 value (body AND camera) = matrix A; ncam = production body + the V2.31 camera = matrix B; ocam = V2.31
# body knobs + the new camera = matrix C; o (production) = matrix D. Content changed in place (idle-stance start copies in the start DBs,
# the rebuilt loaded F_B DB) cannot be undone by flags: the before keeps them (stated in the report).
PREB='"SHM224_DB_JRBwd":"/Game/GraceRanger/SHME/Animations/V226/PSD_SHM226_JogRevBwd","SHM224_DB_JRBwdM":"/Game/GraceRanger/SHME/Animations/V226/PSD_SHM226_JogRevBwd","SHM231_DB_JRBwdS":"/Game/GraceRanger/SHME/Animations/V231/PSD_SHM231S_SlowRevBwd","SHM230_DB_JRBwdL":"/Game/GraceRanger/SHME/Animations/V226/PSD_SHM226_JogRevBwd","SHM232_StartBind":0.0'
PRES='"SwingPelvisComp":0.0,"SwingFloorGuard":0.0'
cand pre232 "$PREB" "\"CamOrbitEnabled\":false,$PRES"
cand ncam "" '"CamOrbitEnabled":false'
cand ocam "$PREB" "$PRES"
