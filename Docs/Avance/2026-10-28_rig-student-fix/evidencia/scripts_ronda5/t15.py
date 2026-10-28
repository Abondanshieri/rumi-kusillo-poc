import sys; sys.path.insert(0,'.')
from u import *
tab,name=sys.argv[1],sys.argv[2]
S('Click',{'ref':tab}); time.sleep(1.5)
# elegir un nodo cualquiera del grafo para dar foco
L=snap()
imgs=[]
for l in L:
    m=re.match(r'\s*image \[pos=(-?\d+),(-?\d+) size=(\d+),(\d+)\] \[ref=(\w+)\]',l)
    if m and 420<int(m.group(1))<1500 and 250<int(m.group(2))<800 and 60<int(m.group(3))<400 and 40<int(m.group(4))<400: imgs.append(m.group(5))
print(imgs[:5])
S('Click',{'ref':imgs[0]}); time.sleep(.5)
S('PressKey',{'key':'Ctrl+A'}); time.sleep(1.5); S('PressKey',{'key':'Home'}); time.sleep(4)
print(shot(name,(389,102,1531,752)))
