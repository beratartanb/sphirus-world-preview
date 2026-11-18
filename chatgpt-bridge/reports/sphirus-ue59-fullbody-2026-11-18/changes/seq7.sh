#!/bin/bash
# seq7.sh: interaction flow (player camera video) + save/load + empty hearth + mask bench / veranda door checks + matched perf
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
VSHOT=1 bash Tools/UE59_20261118/wood18.sh A flow
bash Tools/UE59_20261118/wood18.sh A pieces loadfire emptyfire
MB="(397,226,280)"
bash Tools/UE59_20261118/run2.sh I18_mask 397 120 241 90 "[('',2.0,0,-15,$MB),('',1.0,0,-20,$MB),('E',0.15,0,-20,$MB),('',8.0,0,-20,$MB),('E',0.15,0,-20,$MB),('',6.0,0,-20,$MB),('Escape',0.15,0,-20),('',3.0,0,-15)]" "pass"
VD="(775,1139,200)"
bash Tools/UE59_20261118/run2.sh I18_door 775 960 245 90 "[('',2.0,0,-10,$VD),('GOTO',2.5,0,-10,(775,1060,245)),('',1.0,0,-10,$VD),('E',0.15,0,-10,$VD),('',3.0,0,-10,$VD),('GOTO',4.0,0,-10,(775,1300,200)),('',2.0,0,-10)]" "pass"
bash Tools/UE59_20261118/perf18.sh M18
echo SEQ7_DONE
