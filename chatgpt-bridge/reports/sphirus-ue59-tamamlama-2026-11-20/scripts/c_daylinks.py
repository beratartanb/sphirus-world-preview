# c_daylinks.py: link the hub instance on the house map to its hearth / tea stations (editor world)
import unreal as u
A={a.get_actor_label():a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if a.get_actor_label() in ('GR_DayHub','GR_Day_Fire','GR_Day_Tea')}
h=A['GR_DayHub']; h.modify(); h.set_editor_property('GR_FireSt',A['GR_Day_Fire']); h.set_editor_property('GR_TeaSt',A['GR_Day_Tea'])
print('LINK',h.get_editor_property('GR_FireSt').get_actor_label(),h.get_editor_property('GR_TeaSt').get_actor_label(),h.get_outermost().get_name())
