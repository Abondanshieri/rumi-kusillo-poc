import sys,base64; sys.path.insert(0,'.')
from g1u import *
from PIL import Image
def shot(asset,out,sel=None):
    code='''
a="%s"
bp=unreal.load_asset("/Game/Characters/Student/Rig/"+a+"."+a)
sub=unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
sub.close_all_editors_for_asset(bp)
res["abrir"]=sub.open_editor_for_assets([bp])
'''%asset
    pyrun(code,'ro.out',wait=20); time.sleep(4)
    L=snap()
    tab=[re.search(r'\[ref=(\w+)\]',l).group(1) for l in L if l.strip().startswith('tab "%s"'%asset)][0]
    S('Click',{'ref':tab}); time.sleep(2)
    L=snap()
    imgs=[]
    for l in L:
        m=re.match(r'\s*image \[pos=(-?\d+),(-?\d+) size=(\d+),(\d+)\] \[ref=(\w+)\]',l)
        if m and 700<int(m.group(1))<1000 and 380<int(m.group(2))<700 and int(m.group(3))>100: imgs.append(m.group(5))
    z=[l for l in L if re.search(r'text "Zoom',l)]
    zy=int(re.search(r'pos=(\d+),(\d+)',z[0]).group(2))
    S('Click',{'ref':imgs[0]}); time.sleep(.7)
    if sel:
        code="bp=unreal.load_asset('/Game/Characters/Student/Rig/%s.%s')\nctrl=bp.get_controller_by_name('RigVMModel')\nres['sel']=ctrl.set_node_selection(%r)"%(asset,asset,sel)
        pyrun(code,'sel.out',wait=20); time.sleep(1)
    else:
        S('PressKey',{'key':'Ctrl+A'}); time.sleep(1.2)
    S('PressKey',{'key':'Home'}); time.sleep(4)
    top=zy-20
    j=json.loads(S('Screenshot',{'ref':'w1'}))['returnValue']
    open(SP+'raw.png','wb').write(base64.b64decode(j['data']))
    Image.open(SP+'raw.png').crop((389,top,1531,top+700)).save(out)
    return out
if __name__=="__main__": print(shot(sys.argv[1],sys.argv[2],sys.argv[3].split(",") if len(sys.argv)>3 else None))
