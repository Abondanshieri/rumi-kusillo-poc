"""Mide tamano REAL de cada nodo: selecciona por API, Home (zoom 1:1), lee el widget del nodo en el Snapshot de Slate.
El editor es compartido con otros agentes: se reclica la pestana propia y se valida el titulo del grafo en cada intento."""
import sys; sys.path.insert(0,'.')
from g1u import *
asset=sys.argv[1]; out=sys.argv[2]
names=[n for n,v in json.load(open('../snap_g1_despues.json'))[asset]['nodes'].items() if v['cls']!='RigVMCommentNode']
if len(sys.argv)>3: names=sys.argv[3].split(',')
res_all={}
VC=(959,505)
IMG=r'\s*image \[pos=(-?\d+),(-?\d+) size=(\d+),(\d+)\]'
def mytab():
    L=snap()
    t=[re.search(r'\[ref=(\w+)\]',l).group(1) for l in L if l.strip().startswith('tab "%s"'%asset)]
    if t: S('Click',{'ref':t[0]}); time.sleep(1.0)
def ok(L):
    return any(re.search(r'text "%s" \[pos=\d+,13\d'%asset,l) for l in L)
for nm in names:
  for intento in range(5):
    mytab()
    code="bp=unreal.load_asset('/Game/Characters/Student/Rig/%s.%s')\nctrl=bp.get_controller_by_name('RigVMModel')\nres['sel']=ctrl.set_node_selection([%r])"%(asset,asset,nm)
    pyrun(code,'sel.out',wait=20); time.sleep(.3)
    mytab()
    L=snap()
    z=[re.search(r'\[ref=(\w+)\]',l).group(1) for l in L if 'text "Zoom' in l][0]
    S('Click',{'ref':z}); time.sleep(.3)
    S('PressKey',{'key':'Home'}); time.sleep(1.5)
    L=snap()
    zt=[l for l in L if 'text "Zoom' in l][0]
    if not ok(L) or '1:1' not in zt: continue
    im=[]
    for i,l in enumerate(L):
        m=re.match(IMG,l)
        if m and i+1<len(L):
            x,y,w,h=map(int,m.groups())
            m2=re.match(IMG,L[i+1])
            if m2 and 389<x<1530 and 127<y<860 and w>=30 and h>=30:
                x2,y2,w2,h2=map(int,m2.groups())
                if (x2,y2,w2)==(x,y,w) and h2<=34: im.append((x,y,w,h))
    if not im: continue
    best=min(im,key=lambda r:(r[0]+r[2]/2-VC[0])**2+(r[1]+r[3]/2-VC[1])**2)
    res_all[nm]=dict(w=best[2],h=best[3],zoom='1:1',cands=len(im),intentos=intento+1)
    print(nm,res_all[nm],flush=True); break
  else:
    res_all[nm]=dict(err='fallo'); print(nm,'FALLO',flush=True)
json.dump(res_all,open(out,'w'),indent=1)
