# trace_plan.py (measure, read-only): horizontal complex line-trace marching at fixed heights -> surface outline points per actor.
# Output Saved/UE59Work/r2g2/trace_plan.json
import unreal as u, json, builtins
w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
ZS=getattr(builtins,'R2G_TZ',None) or [190,300,540,640]
X0,X1,Y0,Y1,ST=-120,1640,-260,1560,10
TT=u.TraceTypeQuery.TRACE_TYPE_QUERY1
def march(a,b):
    pts=[]; s=a; n=0
    d=(b-a); L=d.length(); d=d/L
    while n<60:
        h=u.SystemLibrary.line_trace_single(w,s,b,TT,True,[],u.DrawDebugTrace.NONE,False)
        if not h: break
        t=h.to_tuple()
        if not t[0]: break
        p=t[4]; act=t[9]; pts.append((round(p.x),round(p.y),act.get_actor_label() if act else '?'))
        s=p+d*2.0; n+=1
        if (b-s).length()<3 or (s-a).length()>=L: break
    return pts
out={}
for z in ZS:
    H=[]
    y=Y0
    while y<=Y1:
        H+=march(u.Vector(X0,y,z),u.Vector(X1,y,z)); H+=march(u.Vector(X1,y,z),u.Vector(X0,y,z)); y+=ST
    x=X0
    while x<=X1:
        H+=march(u.Vector(x,Y0,z),u.Vector(x,Y1,z)); H+=march(u.Vector(x,Y1,z),u.Vector(x,Y0,z)); x+=ST
    out[str(z)]=H
    print('Z',z,len(H))
json.dump(out,open(u.Paths.project_dir()+'Saved/UE59Work/r2g2/trace_plan.json','w'))
