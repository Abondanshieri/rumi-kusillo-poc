"""Captura legible por bloque + medicion de rectangulos reales de nodos desde el Snapshot de Slate (editor)."""
import sys, base64; sys.path.insert(0,'D:/Dev/Computacion_Grafica/Rumi 5.8/Docs/Avance/2026-10-28_rig-student-fix/evidencia/scripts_g1c')
from g1u import *
from PIL import Image
asset=sys.argv[1]; tag=sys.argv[2]; names=sys.argv[3].split(','); out=sys.argv[4]
IMG=r'\s*image \[pos=(-?\d+),(-?\d+) size=(\d+),(\d+)\]'
def mytab():
    L=snap(); t=[re.search(r'\[ref=(\w+)\]',l).group(1) for l in L if l.strip().startswith('tab "%s"'%asset)]
    if t: S('Click',{'ref':t[0]}); time.sleep(1.0)
def ok(L): return any(re.search(r'text "%s" \[pos=\d+,13\d'%asset,l) for l in L)
for intento in range(6):
    mytab()
    code="bp=unreal.load_asset('/Game/Characters/Student/Rig/%s.%s')\nctrl=bp.get_controller_by_name('RigVMModel')\nctrl.set_node_selection([])\nres['sel']=ctrl.set_node_selection(%r)"%(asset,asset,names)
    pyrun(code,'sel.out',wait=20); time.sleep(.3); mytab()
    L=snap(); z=[re.search(r'\[ref=(\w+)\]',l).group(1) for l in L if 'text "Zoom' in l][0]
    S('Click',{'ref':z}); time.sleep(.3); S('PressKey',{'key':'Home'}); time.sleep(3)
    L=snap(); zt=[l for l in L if 'text "Zoom' in l][0]
    if not ok(L): continue
    rects=[]
    for i,l in enumerate(L):
        m=re.match(IMG,l)
        if m and i+3<len(L):
            x,y,w,h=map(int,m.groups()); m2=re.match(IMG,L[i+1])
            if m2 and (int(m2.group(1)),int(m2.group(2)),int(m2.group(3)))==(x,y,w) and int(m2.group(4))<=40 and 389<=x<1530 and 127<=y<860:
                t=''
                for k in range(i+2,min(i+6,len(L))):
                    mt=re.match(r'\s*text "([^"]+)" \[pos=',L[k])
                    if mt: t=mt.group(1); break
                rects.append((x,y,w,h,t))
    j=json.loads(S('Screenshot',{'ref':'w1'}))['returnValue']
    open(SP+'raw.png','wb').write(base64.b64decode(j['data']))
    Image.open(SP+'raw.png').crop((389,160,1531,860)).save(out)
    zz=re.search(r'"(Zoom[^"]*)"',zt).group(1)
    json.dump(dict(zoom=zz,rects=rects),open(out.replace('.png','.json'),'w'))
    print(tag,zz,len(rects),'nodos visibles'); break
