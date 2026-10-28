import sys,json,time,os,re
sys.path.insert(0,"D:/Dev/Computacion_Grafica/Rumi 5.8/Tools/ue_scripts")
sys.stdout.reconfigure(encoding='utf-8')
from ue_mcp import UnrealMCPClient
c=UnrealMCPClient()
SL='SlateInspectorToolset.SlateInspectorToolset'
SP="C:/Users/franc/AppData/Local/Temp/claude/D--Dev-Computacion-Grafica-Rumi-5-8/5d67f835-bc9e-4d91-a005-a97774592cec/scratchpad/g1/"
def S(tool,a=None): return c.run_tool(SL,tool,a or {})['content'][0]['text']
def snap(): return json.loads(S('Snapshot',{'ref':'w1','maxDepth':80}))['returnValue'].split('\n')
def pyrun(code,out='py.out',wait=60,fname='_g1run.py'):
    f=SP+fname; o=SP+out
    if os.path.exists(o): os.remove(o)
    open(f,'w',encoding='utf8').write("import unreal, json\nOUT=%r\nres={}\ntry:\n"%o+"\n".join("    "+l for l in code.split("\n"))+"\nexcept Exception:\n    import traceback; res['EXC']=traceback.format_exc()\nopen(OUT,'w',encoding='utf8').write(json.dumps(res,indent=1,default=str))\n")
    tb=[re.search(r'\[ref=(\w+)\]',l).group(1) for l in snap() if 'textbox' in l and 'pos=411,1056' in l]
    S('Type',{'ref':tb[0],'text':'py "%s"'%f,'submit':True})
    for i in range(wait*3):
        time.sleep(0.4)
        if os.path.exists(o): time.sleep(0.3); return json.load(open(o,encoding='utf8'))
    return None
