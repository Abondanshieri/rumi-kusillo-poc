import sys,json
sys.path.insert(0,'.'); sys.path.insert(0,'D:/Dev/Computacion_Grafica/Rumi 5.8/Tools/ue_scripts')
from u import *
B='editor_toolset.toolsets.blueprint.BlueprintTools'
def J(t,a):
    x=c.run_tool(B,t,a)['content'][0]['text']
    try: return json.loads(x).get('returnValue')
    except Exception: return x
bp={'refPath':'/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix'}
out={}
for gn in sys.argv[2:]:
    g=J('get_graph',{'blueprint':bp,'graph_name':gn}); base=g['refPath']+'.'
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
    out[gn]=nodes
# python side: title + size
names={g:list(v) for g,v in out.items()}
code='''
A="/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix"
L=unreal.BlueprintEditorLibrary
NM=%s
r={}
for g,ls in NM.items():
    r[g]={}
    for n in ls:
        o=unreal.find_object(None,A+":"+g+"."+n)
        d={}
        try: d["title"]=str(L.get_node_title(o))
        except Exception as e: d["title"]="ERR"
        try:
            s=L.get_node_size(o); d["w"]=s.x; d["h"]=s.y
        except Exception as e: d["w"]=-1
        try: d["cls"]=o.get_class().get_name()
        except Exception: pass
        r[g][n]=d
res["r"]=r
'''%json.dumps(names)
r=pyrun(code,'df.out',wait=40)
for g in out:
    for n,d in r['r'][g].items(): out[g][n].update(d)
json.dump(out,open(sys.argv[1],'w'),indent=1,ensure_ascii=False)
print({g:len(v) for g,v in out.items()}, r.get('EXC'))
