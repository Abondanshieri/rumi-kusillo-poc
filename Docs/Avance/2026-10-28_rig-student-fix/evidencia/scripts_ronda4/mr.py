from d import *
import statistics
def mapr(js,panel_x=(2309,3450),y=(150,1040),skip=('Comment',)):
    d={n:v for n,v in json.load(open(js))['nodes'].items() if not any(s in n for s in skip)}
    im=sl.imgs('w1')
    refs={}
    for x,yy,w,h,r in im:
        if w>=6 and h>=6 and panel_x[0]<x<panel_x[1] and y[0]<yy<y[1] and w<400 and h<400:
            key=(x,yy)
            if key not in refs or h<refs[key][3]: refs[key]=(x,yy,w,h,r)
    refs=list(refs.values())
    xs=[r[0] for r in refs]; ys=[r[1] for r in refs]
    gx=[v[0] for v in d.values()]; gy=[v[1] for v in d.values()]
    k0=(max(xs)-min(xs))/(max(gx)-min(gx))
    best=None
    for k in [k0*(0.85+0.02*i) for i in range(0,16)]:
        x0=min(xs)-k*min(gx); y0=min(ys)-k*min(gy)
        for it in range(10):
            res={}
            for n,v in d.items():
                tx,ty=x0+k*v[0],y0+k*v[1]
                b=min(refs,key=lambda r:(r[0]-tx)**2+(r[1]-ty)**2)
                res[n]=(b[4],(b[0]-tx,b[1]-ty))
            dx=statistics.median(v[1][0] for v in res.values()); dy=statistics.median(v[1][1] for v in res.values())
            x0+=dx; y0+=dy
        err=statistics.median(((v[1][0]-dx)**2+(v[1][1]-dy)**2)**.5 for v in res.values())
        if best is None or err<best[0]: best=(err,k,res)
    err,k,res=best
    return {n:(v[0],round((v[1][0]**2+v[1][1]**2)**.5,1)) for n,v in res.items()},k,err
