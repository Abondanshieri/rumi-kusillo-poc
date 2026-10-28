"""Mide tamano REAL de cada nodo: selecciona por API, Home (zoom 1:1), lee el widget del nodo en el Snapshot de Slate.
El editor es compartido con otros agentes: se reclica la pestana propia y se valida el titulo del grafo en cada intento."""
import sys; sys.path.insert(0,'.')
from g1u import *
asset=sys.argv[1]; out=sys.argv[2]
names=[n for n,v in json.load(open('../snap_g1_despues.json'))[asset]['nodes'].items() if v['cls']!='RigVMCommentNode']
if len(sys.argv)>3: names=sys.argv[3].split(',')
res_all=json.load(open(out)) if os.path.exists(out) else {}
VC=(959,505)
IMG=r'\s*image \[pos=(-?\d+),(-?\d+) size=(\d+),(\d+)\]'
def mytab():
    L=snap()
    t=[re.search(r'\[ref=(\w+)\]',l).group(1) for l in L if l.strip().startswith('tab "%s"'%asset)]
    if t: S('Click',{'ref':t[0]}); time.sleep(1.0)
def ok(L):
    return any(re.search(r'text "%s" \[pos=\d+,13\d'%asset,l) for l in L)
POS={n:tuple(v['pos']) for n,v in json.load(open('../snap_g1_despues.json'))[asset]['nodes'].items() if v['cls']!='RigVMCommentNode'}
from collections import Counter
TT={n:v['title'] for n,v in json.load(open('../snap_g1_despues.json'))[asset]['nodes'].items()}
todo=[n for n in names if not n.startswith('Reroute')]
for nm in list(todo):
  if nm in res_all: continue
  for intento in range(6):
    mytab()
    code="bp=unreal.load_asset('/Game/Characters/Student/Rig/%s.%s')\nctrl=bp.get_controller_by_name('RigVMModel')\nctrl.set_node_selection([])\nres['sel']=ctrl.set_node_selection([%r])"%(asset,asset,nm)
    pyrun(code,'sel.out',wait=20); time.sleep(.3)
    mytab()
    L=snap()
    z=[re.search(r'\[ref=(\w+)\]',l).group(1) for l in L if 'text "Zoom' in l][0]
    S('Click',{'ref':z}); time.sleep(.3)
    S('PressKey',{'key':'Home'}); time.sleep(2.5)
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
                if (x2,y2,w2)==(x,y,w) and h2<=40:
                    ttl=''
                    for k in range(i+2,min(i+6,len(L))):
                        mt=re.match(r'\s*text "([^"]+)" \[pos=',L[k])
                        if mt: ttl=mt.group(1); break
                    im.append((x,y,w,h,ttl))
    cand=[r for r in im if (not r[4] or r[4].startswith(TT[nm]) or TT[nm].startswith(r[4]))]
    if not cand: continue
    r0=min(cand,key=lambda r:(r[0]+r[2]/2-960)**2+(r[1]+r[3]/2-490)**2)
    ox,oy=r0[0]-POS[nm][0], r0[1]-POS[nm][1]; cnt=1
    got={}
    for (x,y,w,h,tt) in im:
        for n,(gx,gy) in POS.items():
            if ((not tt or tt.startswith(TT[n]) or TT[n].startswith(tt))) and abs(x-gx-ox)<=1 and abs(y-gy-oy)<=1: got[n]=dict(w=w,h=h)
    if nm not in got:
        print('  dbg',nm,'off',(ox,oy),cnt,[(r[0],r[1],r[2],r[3],r[4]) for r in im][:6],flush=True); continue
    TX=[]
    for l in L:
        mt=re.match(r'\s*text "([^"]+)" \[pos=(-?\d+),(-?\d+) size=(\d+),(\d+)\]',l)
        if mt: TX.append((mt.group(1),int(mt.group(2)),int(mt.group(3)),int(mt.group(4))))
    for n,v in got.items():
        gx,gy=POS[n]; x0=gx+ox; y0=gy+oy
        v['rows']=[(t,tx-x0,ty-y0,tw) for (t,tx,ty,tw) in TX if x0<=tx<=x0+v['w'] and y0<=ty<=y0+v['h']]
        res_all.setdefault(n,dict(v,fuente=nm))
    json.dump(res_all,open(out,'w'),indent=1)
    print(nm,'->',{n:(v['w'],v['h']) for n,v in got.items()},'votos',cnt,flush=True); break
  else:
    print(nm,'FALLO',flush=True)
json.dump(res_all,open(out,'w'),indent=1)
