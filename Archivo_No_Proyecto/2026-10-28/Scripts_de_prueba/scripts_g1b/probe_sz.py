import sys; sys.path.insert(0,'.')
from g1u import *
asset='CR_Student_IK_fix'
sel=sys.argv[1].split(',')
L=snap()
tab=[re.search(r'\[ref=(\w+)\]',l).group(1) for l in L if l.strip().startswith('tab "%s"'%asset)][0]
S('Click',{'ref':tab}); time.sleep(1.5)
L=snap()
imgs=[]
for l in L:
    m=re.match(r'\s*image \[pos=(-?\d+),(-?\d+) size=(\d+),(\d+)\] \[ref=(\w+)\]',l)
    if m and 700<int(m.group(1))<1000 and 380<int(m.group(2))<700 and int(m.group(3))>100: imgs.append(m.group(5))
print(imgs)
S('Click',{'ref':imgs[0]}); time.sleep(.7)
code="bp=unreal.load_asset('/Game/Characters/Student/Rig/%s.%s')\nctrl=bp.get_controller_by_name('RigVMModel')\nres['sel']=ctrl.set_node_selection(%r)"%(asset,asset,sel)
print(pyrun(code,'sel.out',wait=20)); time.sleep(1)
S('PressKey',{'key':'Home'}); time.sleep(3)
L=snap()
for l in L:
    if 380<0 : pass
open(SP+'snap_probe.txt','w',encoding='utf8').write('\n'.join(L))
