import unreal as u
D='/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/'
for n in ('CHT_PoseSearchDatabases','CHT_PoseSearchDatabases_Dense','CHT_PoseSearchDatabases_Relaxed'):
    c=u.load_asset(D+n)
    try:
        cd=c.get_editor_property('context_data')
        print('CHT',n,[str(x.export_text())[:220] for x in cd] if cd else cd)
    except Exception as e: print('CHT',n,'ERR',str(e)[:150])
    try: print('   result',c.get_editor_property('result_type'), c.get_editor_property('output_object_type'))
    except Exception as e: print('   res ERR',str(e)[:100])
    try:
        rows=c.get_editor_property('results_structs'); print('   rows',len(rows))
    except Exception as e: print('   rows ERR',str(e)[:100])
    try:
        cols=c.get_editor_property('columns_structs'); print('   cols',len(cols),[str(x.export_text())[:160] for x in cols][:8])
    except Exception as e: print('   cols ERR',str(e)[:100])
