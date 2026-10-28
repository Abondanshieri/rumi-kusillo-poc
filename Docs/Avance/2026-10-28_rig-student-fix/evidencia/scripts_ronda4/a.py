import sys,json,time; sys.path.insert(0,'.')
from h import *
sys.path.insert(0,r"D:/Dev/Computacion_Grafica/Rumi 5.8/Tools/ue_scripts")
from ue_mcp import UnrealMCPClient
c=UnrealMCPClient()
B='editor_toolset.toolsets.blueprint.BlueprintTools'; O='editor_toolset.toolsets.object.ObjectTools'
bp={'refPath':'/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix'}
def G(n): return json.loads(c.run_tool(B,'get_graph',{'blueprint':bp,'graph_name':n})['content'][0]['text'])['returnValue']
def mv(ref,x,y): return c.run_tool(B,'set_node_position',{'node':{'refPath':ref},'pos':{'x':x,'y':y}})['content'][0]['text']
def titles():
    t=snap().split('\n'); out={}
    for l in t:
        m=re.search(r'text "(LEAN|PIES|ATERR|PROCED|LOCOM|POST|INIT)[^"]*" \[pos=(-?\d+),(-?\d+) size=(\d+),(\d+)\]',l)
        if m: out[m.group(1)]=(int(m.group(2)),int(m.group(3)),int(m.group(4)))
    return out
