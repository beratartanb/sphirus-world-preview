import unreal as u, math
X=u.AnimPoseExtensions; o=[]
for p in ('/Game/MC_Core_Motion/Animations/Kneel/am_Stand_Trans_KneeB','/Game/MC_Core_Motion/Animations/Kneel/am_KneelB_Idle_01','/Game/MC_Core_Motion/Animations/Kneel/am_KneelB_Trans_Stand'):
    s=u.load_asset(p); d=s.get_play_length(); opt=u.AnimPoseEvaluationOptions(); row=[]
    for k in range(int(d/0.2)+1):
        ps=X.get_anim_pose_at_time(s,min(k*0.2,d),opt); pl=X.get_bone_pose(ps,'pelvis',u.AnimPoseSpaces.WORLD).translation; row.append('%.0f'%pl.z)
    o.append('%s len %.2f pelvisZ/0.2s %s'%(p.split('/')[-1],d,' '.join(row)))
g=u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
c=g.capsule_component; o.append('CAPSULE r %.1f hh %.1f  maxstep %.1f walkable %.1f'%(c.capsule_radius,c.capsule_half_height,g.character_movement.max_step_height,g.character_movement.get_walkable_floor_angle()))
print('CT0\n'+'\n'.join(o))
