import sys; sys.path.insert(0,'.')
from g3u import *
def tabref(name,y):
    for l in snap():
        m=re.match(r'\s*tab "%s" \[pos=(\d+),(\d+) size=\d+,\d+\] \[ref=(\w+)\]'%re.escape(name),l)
        if m and int(m.group(2))==y: return m.group(3)
def ensure(graph):
    r=tabref('Student_Skeleton_AnimBlueprint_fix',25)
    if r: S('Click',{'ref':r}); time.sleep(1.2)
    t=tabref(graph,102)
    if not t: raise Exception('sin tab '+graph)
    S('Click',{'ref':t}); time.sleep(1.2)
def imgs(minw=100):
    out=[]
    for l in snap():
        m=re.match(r'\s*image \[pos=(-?\d+),(-?\d+) size=(\d+),(\d+)\] \[ref=(\w+)\]',l)
        if m:
            x,y,w,h=map(int,m.groups()[:4])
            if 461<=x<1531 and 160<y<850: out.append((x,y,w,h,m.group(5)))
    return out
def zoomtxt():
    return [re.search(r'text "(Zoom[^"]*)"',l).group(1) for l in snap() if re.search(r'text "Zoom',l)]
def fit():
    for t in range(4):
        im=[i for i in imgs() if i[2]>=100]
        S('Click',{'ref':im[0][4]}); time.sleep(.6)
        S('PressKey',{'key':'Ctrl+A'}); time.sleep(1.2); S('PressKey',{'key':'Home'}); time.sleep(3)
        z=zoomtxt()
        if z and '1:1' not in z[0] and '-' in z[0]: return z
    return z
def tabtitle():
    return [l.strip()[:80] for l in snap() if 'text "' in l and ('>' in l or 'Student_Skeleton' in l)][:3]
def where():
    return [re.search(r'text "([^"]+)"',l).group(1) for l in snap() if re.match(r'\s*text "[^"]+" \[pos=\d+,13\d size=\d+,2\d\]',l)]
def ensure2(graph,tries=5):
    for t in range(tries):
        try: ensure(graph)
        except Exception as e: print('ensure fallo',e); time.sleep(1); continue
        w=where()
        if 'Student_Skeleton_AnimBlueprint_fix' in w and graph in w: return True
    return False
