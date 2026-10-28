import sys; sys.path.insert(0,'.')
from u import *
def save_tab(title):
    L=snap()
    tab=[re.search(r'\[ref=(\w+)\]',l).group(1) for l in L if l.strip().startswith('tab "%s"'%title)][0]
    S('Click',{'ref':tab}); time.sleep(2)
    L=snap()
    imgs=[]
    for l in L:
        m=re.match(r'\s*image \[pos=(-?\d+),(-?\d+) size=(\d+),(\d+)\] \[ref=(\w+)\]',l)
        if m and 480<int(m.group(1))<1400 and 200<int(m.group(2))<800 and 100<int(m.group(3))<500 and 50<int(m.group(4))<500: imgs.append(m.group(5))
    S('Click',{'ref':imgs[0]}); time.sleep(.7)
    S('PressKey',{'key':'Ctrl+S'}); time.sleep(5)
if __name__=="__main__":
    save_tab(sys.argv[1])
