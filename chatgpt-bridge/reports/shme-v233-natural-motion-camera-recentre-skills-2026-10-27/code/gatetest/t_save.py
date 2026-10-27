"""gate test: try to save one out-of-manifest asset (DA, only if dirty) and one manifest asset (A_CT_Ref, only if dirty -> no write)."""
import unreal as u
r = {}
for p in ('/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Animations/Continuity/SampleReference/A_CT_Ref_Walk_Stop_F_Lfoot'):
    try: r[p.rsplit('/', 1)[-1]] = 'saved=%s' % u.EditorAssetLibrary.save_asset(p, True)
    except Exception as e: r[p.rsplit('/', 1)[-1]] = 'BLOCKED ' + str(e)[:160]
print('GATETEST', r)
