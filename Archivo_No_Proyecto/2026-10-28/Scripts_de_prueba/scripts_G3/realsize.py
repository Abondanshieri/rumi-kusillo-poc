import sys; sys.path.insert(0,'.')
from g3u import *
EV='D:/Dev/Computacion_Grafica/Rumi 5.8/Docs/Avance/2026-10-28_rig-student-fix/evidencia/'
gn=sys.argv[1]; tab=sys.argv[2]
from ui import *
ensure(tab); L0=snap()
ref=tabref(tab,102)
S('Click',{'ref':ref}); time.sleep(1.5); print(fit())
L=snap()
print([re.search(r'text "(Zoom[^"]*)"',l).group(1) for l in L if re.search(r'text "Zoom',l)])
im=[]
for l in L:
    m=re.match(r'\s*image \[pos=(-?\d+),(-?\d+) size=(\d+),(\d+)\] \[ref=(\w+)\]',l)
    if m: im.append(tuple(map(int,m.groups()[:4]))+(m.group(5),))
im=[i for i in im if 461<=i[0]<1531 and 150<i[1]<855]
by={}
for i in im:
    k=(i[0],i[1])
    if k not in by or i[2]*i[3]>by[k][2]*by[k][3]: by[k]=i
plan=json.load(open(EV+'G3b_plan.json'))[gn]['pos']
refs=list(by.values())
xs=[r[0] for r in refs]; ys=[r[1] for r in refs]
gx=[v[0] for v in plan.values()]; gy=[v[1] for v in plan.values()]
k=((max(xs)-min(xs))/(max(gx)-min(gx))+(max(ys)-min(ys))/(max(gy)-min(gy)))/2
x0=min(xs)-k*min(gx); y0=min(ys)-k*min(gy)
print('k',k,len(refs),len(plan))
res={}
for n,(x,y) in plan.items():
    tx,ty=x0+k*x,y0+k*y
    b=min(refs,key=lambda r:(r[0]-tx)**2+(r[1]-ty)**2)
    res[n]={'w':b[2],'h':b[3],'err':round(((b[0]-tx)**2+(b[1]-ty)**2)**.5,1),'ref':b[4],'sx':b[0],'sy':b[1]}
errs=sorted(v['err'] for v in res.values())
print('err max',errs[-5:],'median',errs[len(errs)//2])
json.dump({'k':k,'x0':x0,'y0':y0,'nodes':res},open(EV+'G3b_real_sizes_%s.json'%gn,'w'),indent=1)
