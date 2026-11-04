D=Saved/Codex/SHME_V255_20261104; export O=$D/run255_h.out; source $D/lib255.sh
relaunch h120 120
WARM=1 ab h120w "s54_revR:c7 j54_rev:c7 s54_r90:c7" $D/vars255.sh
ab h120 "fz_sprint_m:c7 fz_jog_m:c7" $D/vars255.sh
echo H_DONE >> $O
relaunch end2 60
echo TH255_DONE >> $O
