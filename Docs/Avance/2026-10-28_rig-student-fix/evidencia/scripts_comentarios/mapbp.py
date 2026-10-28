import json,sl
SN='D:/Dev/Computacion_Grafica/Rumi 5.8/Docs/Avance/2026-10-28_rig-student-fix/evidencia/snap_antes/ABP_fix.json'
def mapping(graph,panel,K=None):
    d=json.load(open(SN))[graph]['nodes']
    im=sl.imgs(panel)
    # candidate title bars: for each unique pos pick image with smallest height >=20
    bypos={}
    for x,y,w,h,r in im:
        if w>=60 and h>=18 and y>140 and y<760 and not (w==161 and h==24):
            key=(x,y)
            if key not in bypos or h<bypos[key][3]: bypos[key]=(x,y,w,h,r)
    refs=list(bypos.values())
    xs=[r[0] for r in refs]; ys=[r[1] for r in refs]
    gx=[v['x'] for v in d.values()]; gy=[v['y'] for v in d.values()]
    kx=(max(xs)-min(xs))/(max(gx)-min(gx)); ky=(max(ys)-min(ys))/(max(gy)-min(gy))
    k=K if K else (kx+ky)/2
    x0=min(xs)-k*min(gx); y0=min(ys)-k*min(gy)
    res={}; used=set()
    for name,v in sorted(d.items(),key=lambda a:(a[1]['x'],a[1]['y'])):
        tx,ty=x0+k*v['x'],y0+k*v['y']
        cand=refs
        if not cand: print('sin ref',name); continue
        b=min(cand,key=lambda r:(r[0]-tx)**2+(r[1]-ty)**2)
        res[name]=(b[4],round(((b[0]-tx)**2+(b[1]-ty)**2)**.5,1)); used.add(b[4])
    return res,k,len(refs),len(d)
if __name__=="__main__":
    r,k,a,b=mapping('UpdateProceduralVariables','sp32')
    print(k,a,b)
    print(sorted(r.items(),key=lambda a:-a[1][1])[:10])
