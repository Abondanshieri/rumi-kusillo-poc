import sys; sys.path.insert(0,'.')
from g3u import *
n=int(sys.argv[1]); key='Subtract' if n<0 else 'Add'
L=snap()
im=[]
for l in L:
    m=re.match(r'\s*image \[pos=(-?\d+),(-?\d+) size=(\d+),(\d+)\] \[ref=(\w+)\]',l)
    if m and 470<int(m.group(1))<1500 and 200<int(m.group(2))<800 and int(m.group(3))>=100: im.append(m.group(5))
S('Click',{'ref':im[0]}); time.sleep(.5)
for i in range(abs(n)):
    S('PressKey',{'key':key}); time.sleep(.3)
time.sleep(1.5)
print([re.search(r'text "(Zoom[^"]*)"',l).group(1) for l in snap() if re.search(r'text "Zoom',l)])
