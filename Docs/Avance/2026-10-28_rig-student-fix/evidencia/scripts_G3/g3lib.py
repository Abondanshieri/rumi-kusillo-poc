import sys,json,os
sys.path.insert(0,"D:/Dev/Computacion_Grafica/Rumi 5.8/Tools/ue_scripts")
sys.stdout.reconfigure(encoding='utf-8')
from ue_mcp import UnrealMCPClient
c=UnrealMCPClient()
B='editor_toolset.toolsets.blueprint.BlueprintTools'
OB='editor_toolset.toolsets.object.ObjectTools'
EV="D:/Dev/Computacion_Grafica/Rumi 5.8/Docs/Avance/2026-10-28_rig-student-fix/evidencia/"
SP="C:/Users/franc/AppData/Local/Temp/claude/D--Dev-Computacion-Grafica-Rumi-5-8/5d67f835-bc9e-4d91-a005-a97774592cec/scratchpad/"
def T(ts,tool,a):
    r=c.run_tool(ts,tool,a); t=r['content'][0]['text']
    try:
        j=json.loads(t); return j.get('returnValue',j)
    except Exception: return t
def J(tool,a): return T(B,tool,a)
BP={'refPath':'/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix'}
def G(n): return J('get_graph',{'blueprint':BP,'graph_name':n})
def dump(gn):
    g=G(gn); base=g['refPath']+'.'
    ns=J('find_nodes',{'graph':g,'title':'','node_class':'','entry_points_only':False})
    nodes={}
    for i in range(0,len(ns),20):
        for inf in J('get_node_infos',{'nodes':ns[i:i+20]}):
            nn=inf['node']['refPath'].replace(base,'')
            pins=[]
            for d,lst in (('in',inf['input_pins']),('out',inf['output_pins'])):
                for p in lst:
                    pins.append({'dir':d,'idx':p['pin_id']['index_id'],'name':p['name'],'type':p['type_id'],'value':p['value'],
                      'links':[[cp['node']['refPath'].replace(base,''),cp['index_id']] for cp in p['connected_pins']]})
            nodes[nn]={'x':round(inf['position']['x']),'y':round(inf['position']['y']),'type':inf.get('type_id'),'pins':pins}
    return nodes
