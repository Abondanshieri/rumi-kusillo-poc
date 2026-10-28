import sys; sys.path.insert(0,'.')
from g3u import *
im=json.load(open(SP+'imgs.json'))
big=[i for i in im if i[2]>=150][0]
S('Click',{'ref':big[4]}); time.sleep(.8)
S('PressKey',{'key':'Home'}); time.sleep(3)
print([re.search(r'text "(Zoom[^"]*)"',l).group(1) for l in snap() if re.search(r'text "Zoom',l)])
print(shot('z1.png',(461,125,1531,855)))
L=snap(); out=[]
for l in L:
    m=re.match(r'\s*(\w+)\s*("([^"]*)")?[^\[]*\[pos=(-?\d+),(-?\d+) size=(\d+),(\d+)\]',l)
    if m and 461<=int(m.group(4))<1531 and 160<int(m.group(5))<850: out.append(l.strip()[:120])
print(len(out)); print('\n'.join(out[:60]))
