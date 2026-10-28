import json,sl
def mapping(snapfile, panel='sp7'):
    d=json.load(open(snapfile))['nodes']
    refs=sl.nodes(panel)
    xs=[r[0] for r in refs]
    gx=[v[0] for v in d.values()]
    k=(max(xs)-min(xs))/(max(gx)-min(gx))
    x0=min(xs)-k*min(gx)
    ys=[r[1] for r in refs]; gy=[v[1] for v in d.values()]
    y0=min(ys)-k*min(gy)
    res={}
    used=set()
    items=sorted(d.items(),key=lambda a:(a[1][0],a[1][1]))
    for name,(x,y) in items:
        best=min((r for r in refs if r[4] not in used),key=lambda r:(r[0]-(x0+k*x))**2+(r[1]-(y0+k*y))**2)
        err=((best[0]-(x0+k*x))**2+(best[1]-(y0+k*y))**2)**.5
        used.add(best[4]); res[name]=(best[4],round(err,1))
    return res,k
if __name__=="__main__":
    r,k=mapping('D:/Dev/Computacion_Grafica/Rumi 5.8/Docs/Avance/2026-10-28_rig-student-fix/evidencia/snap_antes/CR_Student_Procedural_fix.json')
    print(k); 
    for a,b in r.items(): print(a,b)
