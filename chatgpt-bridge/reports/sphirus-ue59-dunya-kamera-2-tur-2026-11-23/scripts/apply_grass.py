# apply_grass.py: mute the lime-yellow subsurface / variation colours of the project-owned ground-layer foliage instances (GroundLayer20261111).
# Baseline values are stored once in Tools/R2G2_20261123/grass_base.json and every run computes from that baseline (idempotent, reversible with desat 0, gain 1).
import unreal as u, builtins, json, os
CFG={'desat':0.45,'gain':0.85,'keys':('Translucency Color','Color Variation 2','Color Variation 3')}; CFG.update(getattr(builtins,'R2G_GRASS',None) or {})
D='/Game/GraceRanger/Environment/GroundLayer20261111/Materials/'
N=('MI_GL_GrassMedium01','MI_GL_GrassShort01','MI_GL_GrassSmallSparse01','MI_GL_GrassLarge01','MI_GL_GrassLarge02','MI_GL_GrassLarge03','MI_GL_GroundCover01_FO','MI_GL_GroundCover02_FO','MI_GL_GroundCover03_FO','MI_GL_GroundCover04_FO')
ML=u.MaterialEditingLibrary; BF=u.Paths.project_dir()+'Tools/R2G2_20261123/grass_base.json'
base=json.load(open(BF)) if os.path.exists(BF) else {}
new_base=not base; out=[]
for n in N:
    mi=u.load_asset(D+n)
    if not mi: print('GRASS missing',n); continue
    for k in CFG['keys']:
        if new_base: c=ML.get_material_instance_vector_parameter_value(mi,k); base.setdefault(n,{})[k]=[c.r,c.g,c.b,c.a]
        r,g,b,a=base[n][k]; l=0.2126*r+0.7152*g+0.0722*b; t=CFG['desat']; q=CFG['gain']
        ML.set_material_instance_vector_parameter_value(mi,k,u.LinearColor((r+(l-r)*t)*q,(g+(l-g)*t)*q,(b+(l-b)*t)*q,a))
    ML.update_material_instance(mi); out.append(mi)
if new_base: json.dump(base,open(BF,'w'),indent=1)
c=ML.get_material_instance_vector_parameter_value(u.load_asset(D+N[0]),'Translucency Color'); print('GRASS',len(out),'instances; GrassMedium01 Translucency',[round(v,3) for v in (c.r,c.g,c.b)],'base',[round(v,3) for v in base[N[0]]['Translucency Color'][:3]])
builtins.R2G_GRASS_ASSETS=out
