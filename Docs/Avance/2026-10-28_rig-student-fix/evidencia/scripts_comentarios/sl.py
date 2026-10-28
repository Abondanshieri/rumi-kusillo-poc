import sys,json
sys.path.insert(0,"D:/Dev/Computacion_Grafica/Rumi 5.8/Tools/ue_scripts")
from ue_mcp import UnrealMCPClient
c=UnrealMCPClient()
def S(tool,args=None):
    r=c.run_tool('SlateInspectorToolset.SlateInspectorToolset',tool,args or {})
    return r['content'][0]['text']
if __name__=="__main__":
    t=S(sys.argv[1],json.loads(sys.argv[2]) if len(sys.argv)>2 else {})
    open(r"C:\Users\franc\AppData\Local\Temp\claude\D--Dev-Computacion-Grafica-Rumi-5-8\5d67f835-bc9e-4d91-a005-a97774592cec\scratchpad\sl_out.txt","w",encoding="utf8").write(t)
    print(len(t))
def shot(ref,path):
    import base64
    r=c.run_tool('SlateInspectorToolset.SlateInspectorToolset','Screenshot',{'ref':ref})
    t=json.loads(r['content'][0]['text'])['returnValue']
    open(path,'wb').write(base64.b64decode(t['data']))
import re
def nodes(ref='sp4'):
    t=json.loads(S('Snapshot',{'ref':ref,'maxDepth':60}))['returnValue']
    out=[]
    for l in t.split('\n'):
        m=re.match(r'\s*image \[pos=(-?\d+),(-?\d+) size=(\d+),(\d+)\] \[ref=(\w+)\]',l)
        if m:
            x,y,w,h=map(int,m.groups()[:4])
            if w>100 and h>60 and y>200 and y<880: out.append((x,y,w,h,m.group(5)))
    return sorted(out)
def multi(refs):
    first=True
    for r in refs:
        S('Click',{'ref':r,'modifiers':{'bShift':False,'bCtrl':not first,'bAlt':False,'bCmd':False}})
        first=False
def comment(refs,text):
    S('Click',{'ref':refs[0]})
    multi(refs)
    S('PressKey',{'key':'C'})
    t=json.loads(S('Snapshot',{'ref':'sp4','maxDepth':60}))['returnValue']
    tb=[re.search(r'\[ref=(\w+)\]',l).group(1) for l in t.split('\n') if 'textbox [focused]' in l]
    print('focused tb',tb)
    if tb: S('Type',{'ref':tb[0],'text':text,'submit':True})
def comment(refs,text,panel='sp7'):
    S('Click',{'ref':refs[0]})
    multi(refs)
    S('PressKey',{'key':'C'})
    t=json.loads(S('Snapshot',{'ref':panel,'maxDepth':60}))['returnValue']
    tb=[]
    for l in t.split('\n'):
        if 'textbox' in l and 'Buscar' not in l:
            m=re.search(r'pos=(\d+),(\d+) size=(\d+),(\d+)\] \[ref=(\w+)\]',l)
            if m and int(m.group(3))>=300 and int(m.group(4))>=25: tb.append(m.group(5))
    print('tb',tb)
    if tb: S('Type',{'ref':tb[0],'text':text,'submit':True})
def imgs(panel):
    t=json.loads(S('Snapshot',{'ref':panel,'maxDepth':60}))['returnValue']
    out=[]
    for l in t.split('\n'):
        m=re.match(r'\s*image \[pos=(-?\d+),(-?\d+) size=(\d+),(\d+)\] \[ref=(\w+)\]',l)
        if m: out.append((int(m.group(1)),int(m.group(2)),int(m.group(3)),int(m.group(4)),m.group(5)))
    return out
def at(im,x,y,tol=6):
    c=[i for i in im if abs(i[0]-x)<=tol and abs(i[1]-y)<=tol and i[2]>=100 and i[3]>=60]
    return c[0][4] if c else None
def titles(panel):
    return [i for i in imgs(panel) if 20<=i[3]<=30 and i[2]>=60]
def commentsel(text,panel):
    S('PressKey',{'key':'C'})
    t=json.loads(S('Snapshot',{'ref':panel,'maxDepth':60}))['returnValue']
    tb=[]
    for l in t.split('\n'):
        if 'textbox' in l and 'Buscar' not in l:
            m=re.search(r'pos=(\d+),(\d+) size=(\d+),(\d+)\] \[ref=(\w+)\]',l)
            if m and int(m.group(3))>=300 and int(m.group(4))>=25: tb.append(m.group(5))
    print('tb',tb)
    if tb: S('Type',{'ref':tb[0],'text':text,'submit':True})
