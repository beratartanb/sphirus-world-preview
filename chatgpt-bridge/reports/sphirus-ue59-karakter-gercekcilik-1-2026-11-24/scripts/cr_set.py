# cr_set.py (control, in memory): apply Saved/UE59Work/cr1/set.json. {"mi":{asset:{"S":{..},"V":{..}}}, "groom":{component name:{regex:replacement on simulation_settings text}}, "dump":[asset,...]}
# Previous values are written to cr1/prev_last.json so a candidate can be reverted exactly. Nothing is saved here.
import unreal as u, json, re
D=u.Paths.project_dir()+'Saved/UE59Work/cr1/'; S=json.loads(open(D+'set.json',encoding='utf8').read()); ME=u.MaterialEditingLibrary; prev={'mi':{},'groom':{}}; out=[]
for p,d in S.get('mi',{}).items():
    m=u.load_asset(p); pv=prev['mi'].setdefault(p,{'S':{},'V':{}})
    for n,v in d.get('S',{}).items():
        pv['S'][n]=ME.get_material_instance_scalar_parameter_value(m,n); ME.set_material_instance_scalar_parameter_value(m,n,float(v))
    for n,v in d.get('V',{}).items():
        c=ME.get_material_instance_vector_parameter_value(m,n); pv['V'][n]=[c.r,c.g,c.b,c.a]; ME.set_material_instance_vector_parameter_value(m,n,u.LinearColor(*v))
    ME.update_material_instance(m); out.append('MI %s %s'%(p.split('/')[-1],{k:(round(pv['S'][k],3),d['S'][k]) for k in d.get('S',{})}))
if S.get('groom'):
    bp=u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'); sds=u.get_engine_subsystem(u.SubobjectDataSubsystem)
    for h in sds.k2_gather_subobject_data_for_blueprint(bp):
        ob=u.SubobjectDataBlueprintFunctionLibrary.get_object(sds.k2_find_subobject_data_from_handle(h))
        if not ob: continue
        nm=ob.get_name().replace('_GEN_VARIABLE','')
        if nm in S['groom'] and nm not in prev['groom']:
            g=S['groom'][nm]; ss=ob.get_editor_property('simulation_settings'); t0=ss.export_text(); t=t0; prev['groom'][nm]={'sim':t0}
            for a,b in g.get('sim',{}).items():
                t2=re.sub(a,b,t); out.append('GROOM %s %s -> %s %s'%(nm,a,b,'ok' if t2!=t else 'NOCHANGE')); t=t2
            ss.import_text(t); ob.set_editor_property('simulation_settings',ss)
            if 'physics_asset' in g:
                prev['groom'][nm]['physics_asset']=ob.get_editor_property('physics_asset').get_path_name() if ob.get_editor_property('physics_asset') else None
                ob.set_editor_property('physics_asset',u.load_asset(g['physics_asset']) if g['physics_asset'] else None)
            if g.get('print'): out.append('SIMTEXT '+ob.get_editor_property('simulation_settings').export_text())
    u.BlueprintEditorLibrary.compile_blueprint(bp)
for p in S.get('dump',[]):
    m=u.load_asset(p); out.append('DUMP '+p.split('/')[-1]+' parent '+str(m.get_editor_property('parent').get_path_name())+' S '+str({str(n):round(ME.get_material_instance_scalar_parameter_value(m,n),3) for n in ME.get_scalar_parameter_names(m)})[:1500]+' V '+str({str(n):[round(x,2) for x in ME.get_material_instance_vector_parameter_value(m,n).to_tuple()] for n in ME.get_vector_parameter_names(m)})[:600])
open(D+'prev_last.json','w',encoding='utf8').write(json.dumps(prev)); open(D+'set_out.txt','w',encoding='utf8').write('\n'.join(out)); print('CRSET',len(out))
