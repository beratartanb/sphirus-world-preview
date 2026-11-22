exec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
from qa_graph import obj
# probe_orb7.py (control, read-only): OffsetRootBone node settings + pin sources, and the Get_OffsetRoot* functions' node list
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); ag=B.get_graph(a,'AnimGraph'); o=[]
for p in [pn(x) for x in B.find_nodes(ag)]:
    if 'OffsetRootBone' in type(obj(p)).__name__:
        o.append(obj(p).get_editor_property('node').export_text())
        for x in info(p).input_pins:
            s=src((p,str(x.name))); o.append(' pin %s <- %s'%(x.name,[str(q[0]).split('.')[-1]+':'+str(q[1]) for q in s]))
for g in ('Get_OffsetRootRotationMode','Get_OffsetRootTranslationMode','Get_OffsetRootTranslationHalfLife','Get_OffsetRootTranslationRadius'):
    try:
        gg=B.get_graph(a,g); o.append('== '+g)
        for x in B.find_nodes(gg):
            q=pn(x); ob=obj(q); t=type(ob).__name__; ex=''
            try: ex=str(ob.get_editor_property('function_reference').export_text())[:120] if hasattr(ob,'get_editor_property') else ''
            except Exception: pass
            pins=[]
            for pi in info(q).input_pins:
                try: pins.append('%s=%s'%(pi.name,str(pi.default_value)[:30]))
                except Exception: pass
            o.append('  %s %s %s %s'%(t,str(q).split('.')[-1],ex,pins))
    except Exception as e: o.append('ERR %s %s'%(g,e))
open(u.Paths.project_dir()+'Saved/UE59Work/r7/orb7.txt','w',encoding='utf8').write('\n'.join(o)); print('ORB7',len(o))
