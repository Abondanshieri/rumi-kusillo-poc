from d import *
import statistics
def mapping2(graphjson,k0=None):
    d=json.load(open(graphjson))['UpdateProceduralVariables']['nodes']
    im=sl.imgs('sp32')
    refs={}
    for x,y,w,h,r in im:
        if w>=60 and h>=18 and 140<y<840 and 2381<x<3450 and not (w==161 and h==24):
            key=(x,y)
            if key not in refs or h<refs[key][3]: refs[key]=(x,y,w,h,r)
    refs=list(refs.values())
    xs=[r[0] for r in refs]; ys=[r[1] for r in refs]
    gx=[v['x'] for v in d.values()]; gy=[v['y'] for v in d.values()]
    best=None
    for k in ([k0] if k0 else [0.1450+0.0005*i for i in range(0,10)]):
        x0=min(xs)-k*min(gx); y0=min(ys)-k*min(gy)
        for it in range(8):
            res={}
            for n,v in d.items():
                tx,ty=x0+k*v['x'],y0+k*v['y']
                b=min(refs,key=lambda r:(r[0]-tx)**2+(r[1]-ty)**2)
                res[n]=(b[4],(b[0]-tx,b[1]-ty))
            dx=statistics.median(v[1][0] for v in res.values()); dy=statistics.median(v[1][1] for v in res.values())
            x0+=dx; y0+=dy
        err=statistics.median(((v[1][0]-dx)**2+(v[1][1]-dy)**2)**.5 for v in res.values())
        if best is None or err<best[0]: best=(err,k,x0,y0,res)
    err,k,x0,y0,res=best
    out={n:(v[0],round((((v[1][0])**2+(v[1][1])**2)**.5),1)) for n,v in res.items()}
    return out,k,err
