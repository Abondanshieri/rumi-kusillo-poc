import sys; sys.path.insert(0,'.')
from u import *
def find():
    out={}
    for l in snap():
        m=re.search(r'text "(INIT \(|Set references)[^"]*" \[pos=(-?\d+),(-?\d+) size=(\d+),(\d+)\] \[ref=(\w+)\]',l)
        if m: out[m.group(1)]=(int(m.group(2)),int(m.group(3)),int(m.group(4)),int(m.group(5)),m.group(6))
    return out
print(find())
# nodo cualquiera dentro del panel
imgs=[]
for l in snap():
    m=re.match(r'\s*image \[pos=(-?\d+),(-?\d+) size=(\d+),(\d+)\] \[ref=(\w+)\]',l)
    if m and 480<int(m.group(1))<1400 and 200<int(m.group(2))<800 and 100<int(m.group(3))<500 and 50<int(m.group(4))<500: imgs.append((int(m.group(1)),int(m.group(2)),m.group(5)))
print(imgs[:6])
S('Click',{'ref':'i6662'}); time.sleep(.6)
for i in range(4): S('PressKey',{'key':'Subtract'}); time.sleep(.3)
time.sleep(2)
print(find())
shot('abp_ev.png',(389,102,1531,752))
