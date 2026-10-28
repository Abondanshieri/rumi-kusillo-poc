import sys,os,json,itertools
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from ub import analyze
R="D:/Dev/Computacion_Grafica/Rumi 5.8/Content/Characters/Student/"
def rects(path):
    out={}
    for d in analyze(path):
        if "NodePosX" in d and d["outer"]!="Rig" or ("NodePosX" in d and d["outer"]=="Rig"):
            pass
    return None
def rep(path,use):
    res={}
    for d in analyze(path):
        if use=="bp" and "NodePosX" in d:
            x,y,w,h=d["NodePosX"],d["NodePosY"],d["NodeWidth"],d["NodeHeight"]
        elif use=="rig" and "Position" in d:
            x,y=d["Position"]; w,h=d["Size"]
        else: continue
        res.setdefault(d["outer"],[]).append((d["name"],x,y,w,h))
    return res
def inter(a,b):
    w=min(a[1]+a[3],b[1]+b[3])-max(a[1],b[1]); h=min(a[2]+a[4],b[2]+b[4])-max(a[2],b[2])
    return (w,h) if w>0 and h>0 else None
out={}
for label,path,use in [("ABP_fix",R+"Student_Skeleton_AnimBlueprint_fix.uasset","bp"),("CR_Student_Procedural_fix",R+"Rig/CR_Student_Procedural_fix.uasset","rig"),("CR_Student_IK_fix",R+"Rig/CR_Student_IK_fix.uasset","rig")]:
    for g,rs in rep(path,use).items():
        pairs=[]
        for a,b in itertools.combinations(rs,2):
            i=inter(a,b)
            if i: pairs.append({"a":a[0],"b":b[0],"overlap_wh":i})
        gaps=[]
        for a,b in itertools.combinations(rs,2):
            if not inter(a,b):
                dx=max(b[1]-(a[1]+a[3]),a[1]-(b[1]+b[3]),-1e9); dy=max(b[2]-(a[2]+a[4]),a[2]-(b[2]+b[4]),-1e9)
                gaps.append({"a":a[0],"b":b[0],"gap_x":dx,"gap_y":dy})
        out[label+"/"+g]={"rects(name,x,y,w,h)":rs,"overlaps":pairs,"separations":gaps}
        print(label,g,len(rs),"comentarios,",len(pairs),"solapes",pairs)
json.dump(out,open(sys.argv[1] if len(sys.argv)>1 else "ov.json","w"),indent=1)
