import sys,json
sys.path.insert(0,"D:/Dev/Computacion_Grafica/Rumi 5.8/Tools/ue_scripts")
sys.stdout.reconfigure(encoding='utf-8')
from ue_mcp import UnrealMCPClient
c=UnrealMCPClient()
CR='animation_toolset.toolsets.controlrig.ControlRigTools'
OB='editor_toolset.toolsets.object.ObjectTools'
BP='editor_toolset.toolsets.blueprint.BlueprintTools'
def T(ts,tool,a):
    r=c.run_tool(ts,tool,a); t=r['content'][0]['text']
    try: return json.loads(t).get('returnValue',json.loads(t))
    except Exception: return t
RIG={'IK':'/Game/Characters/Student/Rig/CR_Student_IK_fix','PR':'/Game/Characters/Student/Rig/CR_Student_Procedural_fix'}
def cr(k):
    p=RIG[k]; n=p.split('/')[-1]
    return {'refPath':p+'.'+n},{'refPath':p+'.'+n+':RigVMModel'}
import base64,time
SL='SlateInspectorToolset.SlateInspectorToolset'
SP=r"C:/Users/franc/AppData/Local/Temp/claude/D--Dev-Computacion-Grafica-Rumi-5-8/5d67f835-bc9e-4d91-a005-a97774592cec/scratchpad/"
def S(tool,a=None): return c.run_tool(SL,tool,a or {})['content'][0]['text']
def shot(name,box):
    j=json.loads(S('Screenshot',{'ref':'w1'}))['returnValue']
    p=SP+name
    open(p,'wb').write(base64.b64decode(j['data']))
    from PIL import Image
    Image.open(p).crop(box).save(p)
    return p
def snap(): return json.loads(S('Snapshot',{'ref':'w1','maxDepth':80}))['returnValue'].split('\n')
import os
def pyrun(code,out='py.out',wait=12):
    """Ejecuta Python de editor via consola (comando py) y devuelve lo escrito en out."""
    f=SP+'_runG3.py'; o=SP+out
    if os.path.exists(o): os.remove(o)
    open(f,'w',encoding='utf8').write("import unreal, json\nOUT=%r\nres={}\ntry:\n"%o+"\n".join("    "+l for l in code.split("\n"))+"\nexcept Exception:\n    import traceback; res['EXC']=traceback.format_exc()\nopen(OUT,'w',encoding='utf8').write(json.dumps(res,indent=1,default=str))\n")
    tb=[re.search(r'\[ref=(\w+)\]',l).group(1) for l in snap() if 'textbox' in l and re.search(r'pos=\d+,10[3-9]\d',l)]
    S('Type',{'ref':tb[0],'text':'py "%s"'%f,'submit':True})
    for i in range(wait*5):
        time.sleep(0.4)
        if os.path.exists(o): time.sleep(0.3); return json.load(open(o,encoding='utf8'))
    return None
import re
