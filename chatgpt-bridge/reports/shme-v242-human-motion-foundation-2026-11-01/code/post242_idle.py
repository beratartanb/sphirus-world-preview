"""post242_idle.py (per-run POST): reload the live idle database from disk after a V2.42 weighted-idle candidate run (see pre242_idle.py)."""
import builtins, pathlib
builtins.V242_IDLE_POST = True
exec(compile(open(str(pathlib.Path(__file__).resolve().parent / 'pre242_idle.py') if '__file__' in globals() else r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V242_20261101/pre242_idle.py', encoding='utf-8').read(), 'pre242_idle.py', 'exec'), {'__name__': '__job__', '__file__': __file__ if '__file__' in globals() else ''})
