#!/bin/bash
# run255_q.sh : V2.55 final candidate c7h at 60: scripted, fuzz, direction matrix, regression, uneven ground / walls against production; captures for the user
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V255_20261104; export O=$D/run255_q.out; source $D/lib255.sh
export V219_EDARGS="-UseFixedTimeStep -FPS=60"
SC="s54_revR s54_revL s54_r90 s54_l90 s54_r135 j54_rev j54_r90 j38_c90l j54_r135 w54_rev s54_tap s54_mid s54_lr"
FZ="fz_sprint_a fz_sprint_m fz_jog_a fz_jog_m fz_walk_a fz_walk_m"
DM="fz_dm_walk_0 fz_dm_walk_60 fz_dm_walk_m120 fz_dm_jog_0 fz_dm_jog_60 fz_dm_jog_m120 fz_dm_sprint_0 fz_dm_sprint_60 fz_dm_sprint_m120"
RG="wstart w42_id taps jstart j36_stop j45_sl2 gait w43_idle j40_rlw"
TR="t255_hill_s t255_hill_j t255_hill90_s t255_bump_s t255_step_j t255_step_s t255_wall_s t255_wall_b j40_wall cam32_wallturn"
WARM=1 ab q60w "s54_revR:c7h s54_revL:c7h s54_r90:c7h s54_l90:c7h j54_rev:c7h j54_r90:c7h j38_c90l:c7h" $D/vars255.sh
J=""; for s in $SC $FZ $DM $RG $TR; do J="$J $s:c7h"; done
for s in $TR s54_revR j54_rev w54_rev wstart gait fz_sprint_m; do J="$J $s:o"; done
ab q60 "$J" $D/vars255.sh
echo Q_AB_DONE >> $O
CAP_START=4.6 CAP_SECS=3.2 ab qcap "s54_revR:c7hS s54_revR:c7hG s54_revR:c7hD j54_rev:c7hS j54_rev:c7hG j54_rev:c7hD s54_r90:c7hS s54_r90:c7hG j54_r90:c7hS j54_r90:c7hG s54_revL:c7hS" $D/vars255.sh
echo TQ255_DONE >> $O
