# flowtab.sh <slab "c,w"> <label=npz>... : print stand-off table in a slab |(|x-PX|) - c| < w
S=$1; shift; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
SLAB=$S "/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b --factory-startup --python Tools/CharacterLookdev_20260930/blender_g11re_flow.py -- Saved/Codex/GD11_HeadRefinementF_20261004/pv/flow_tmp.png Saved/Codex/CharacterGuardian7_20261002/headC8.npy "$@" 2>&1 | grep FLOW | "/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" -c "
import sys,json; d=json.loads(sys.stdin.read().split('FLOW ',1)[1])['standoff_cm_by_angle']; k0=list(d)[0]
ks=[k for k in d[k0] if -75<=int(k)<=60 and int(k)%10==0]; print('slab $S ang', ' '.join('%5s'%k for k in ks))
for n in d: print('%-14s'%n, ' '.join('%5s'%(d[n][k] if d[n][k] is not None else '-') for k in ks))"
