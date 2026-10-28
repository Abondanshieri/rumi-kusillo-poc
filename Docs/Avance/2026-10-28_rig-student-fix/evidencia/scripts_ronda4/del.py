from d import *
def delc(node,prefix,tref):
    sl.S('PressKey',{'key':'Ctrl+A'}); sl.S('PressKey',{'key':'Home'}); time.sleep(2)
    r,k,a,b=mapbp.mapping('UpdateProceduralVariables','sp32')
    ref=r[node][0]
    sl.S('Click',{'ref':ref}); sl.S('Click',{'ref':ref}); sl.S('PressKey',{'key':'Home'}); time.sleep(2)
    t=snapall()
    tt=[l for l in t if re.search(r'text "'+prefix,l)]
    print(tt)
    if not tt: return False
    m=re.search(r'ref=(\w+)',tt[0]).group(1)
    pos=re.search(r'pos=(-?\d+),(-?\d+) size=(\d+)',tt[0]); cx=int(pos.group(1))+int(pos.group(3))//2
    print('center x',cx)
    if not (2400<cx<3430): return False
    sl.S('Click',{'ref':m}); time.sleep(1)
    t=snapall()
    ok=any('Font Size' in l for l in t)
    print('comment selected',ok)
    if ok:
        sl.S('PressKey',{'key':'Delete'}); time.sleep(1.5)
    return ok
