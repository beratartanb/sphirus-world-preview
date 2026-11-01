import builtins, json
clips = json.load(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V244_20261101/data/latstop244_clips.json'))
builtins.V242_LDB = {'dry': False, 'clips': clips, 'name': 'PSD_SHM244_LatStop'}
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V244_20261101/build244_latdb.py', encoding='utf-8').read(), 'build244_latdb.py', 'exec'), {'__name__': '__job__'})
