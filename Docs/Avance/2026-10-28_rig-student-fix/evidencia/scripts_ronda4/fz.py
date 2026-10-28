from mr import *
def setfont(js,node,prefix,val,tab=None):
    sl.S('PressKey',{'key':'Ctrl+A'}); sl.S('PressKey',{'key':'Home'}); time.sleep(2)
    r,k,e=mapr(js)
    ref=r[node][0]
    sl.S('Click',{'ref':ref}); sl.S('Click',{'ref':ref}); sl.S('PressKey',{'key':'Home'}); time.sleep(2)
    t=snapall()
    tt=[l for l in t if re.search(r'text "'+prefix+r'[^"]*" \[pos=-?\d+,\d+ size=\d+,\d+\]',l)]
    if not tt: print('no title',prefix); return False
    m=re.search(r'ref=(\w+)',tt[0]).group(1); p=re.search(r'pos=(-?\d+),(-?\d+) size=(\d+)',tt[0])
    cx=int(p.group(1))+int(p.group(3))//2; cy=int(p.group(2))
    print(prefix,tt[0].strip()[:80],cx,cy)
    if not (2400<cx<3430 and 140<cy<1030): return False
    sl.S('Click',{'ref':m}); time.sleep(1)
    t=snapall()
    for i,l in enumerate(t):
        if 'generic "Font Size' in l:
            for l2 in t[i:i+6]:
                if 'slider' in l2:
                    sl_=re.search(r'ref=(\w+)',l2).group(1)
                    sl.S('Click',{'ref':sl_,'doubleClick':True}); sl.S('Type',{'ref':sl_,'text':str(val),'submit':True}); return True
    print('no font'); return False
