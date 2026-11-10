exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP_Rx'); L.compile_blueprint(a)
for g in B.list_graphs(a):
    for n in GE(g).list_nodes_with_errors():
        try: print('ERRNODE',g.get_name(),type(n).__name__,str(n.get_editor_property('error_msg'))[:600])
        except Exception as e: print('ERRNODE',g.get_name(),type(n).__name__,'(msg n/a)',str(e)[:100])
        i=info(pn(n)); print('  pins in',[(str(x.name)) for x in i.input_pins],'out',[str(x.name) for x in i.output_pins])
