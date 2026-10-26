"""memprobe230.py (editor job, read-only): one memory sample. builtins.MP230_TAG names it, builtins.MP230_GC (default False) runs a full
GC first. Process private bytes / commit / working set (ctypes GetProcessMemoryInfo), loaded UObject counts for chosen classes and total
(unreal.ObjectIterator), worlds alive. Appends one JSON line to Saved/Codex/SHME_V230_20261026/mem230.jsonl and prints MEM230 {...}."""
import unreal as u, json, time, ctypes, ctypes.wintypes as W, builtins
class PMC(ctypes.Structure):
    _fields_ = [('cb', W.DWORD), ('PageFaultCount', W.DWORD), ('PeakWorkingSetSize', ctypes.c_size_t), ('WorkingSetSize', ctypes.c_size_t),
                ('QuotaPeakPagedPoolUsage', ctypes.c_size_t), ('QuotaPagedPoolUsage', ctypes.c_size_t), ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t),
                ('QuotaNonPagedPoolUsage', ctypes.c_size_t), ('PagefileUsage', ctypes.c_size_t), ('PeakPagefileUsage', ctypes.c_size_t), ('PrivateUsage', ctypes.c_size_t)]
def mem():
    c = PMC(); c.cb = ctypes.sizeof(c); k = ctypes.windll.kernel32
    k.GetCurrentProcess.restype = W.HANDLE; k.K32GetProcessMemoryInfo.argtypes = [W.HANDLE, ctypes.POINTER(PMC), W.DWORD]; k.K32GetProcessMemoryInfo.restype = W.BOOL
    ok = k.K32GetProcessMemoryInfo(k.GetCurrentProcess(), ctypes.byref(c), c.cb)
    return {'private_gb': round(c.PrivateUsage / 1e9, 2), 'ws_gb': round(c.WorkingSetSize / 1e9, 2), 'peak_ws_gb': round(c.PeakWorkingSetSize / 1e9, 2)}
t0 = time.time()
if getattr(builtins, 'MP230_GC', False): u.SystemLibrary.collect_garbage()
gc_s = round(time.time() - t0, 2)
counts = {}
for cname in ('Object', 'World', 'Level', 'AnimSequence', 'PoseSearchDatabase', 'AnimMontage', 'Texture2D', 'StaticMesh', 'SkeletalMesh', 'Material', 'MaterialInstanceDynamic', 'Actor', 'ActorComponent', 'AnimInstance', 'Blueprint', 'BlueprintGeneratedClass', 'K2Node', 'EdGraph', 'Package', 'PythonGeneratedClass'):
    cl = getattr(u, cname, None)
    if cl is None: continue
    try: counts[cname] = sum(1 for _ in u.ObjectIterator(cl))
    except Exception as e: counts[cname] = 'err'
worlds = []
try: worlds = sorted(set(str(w.get_name()) for w in u.ObjectIterator(u.World)))[:12]
except Exception: pass
rec = {'tag': getattr(builtins, 'MP230_TAG', ''), 't': time.strftime('%H:%M:%S'), 'gc': bool(getattr(builtins, 'MP230_GC', False)), 'gc_s': gc_s, **mem(), 'counts': counts, 'worlds': worlds, 'probe_s': round(time.time() - t0, 2)}
open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V230_20261026/mem230.jsonl', 'a').write(json.dumps(rec) + '\n')
print('MEM230 ' + json.dumps(rec))
