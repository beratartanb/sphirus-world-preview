import unreal as u
u.SystemLibrary.execute_console_command(u.EditorLevelLibrary.get_editor_world(), 'ModelContextProtocol.StartServer')
print('GD45_MCP_START_SENT', flush=True)
