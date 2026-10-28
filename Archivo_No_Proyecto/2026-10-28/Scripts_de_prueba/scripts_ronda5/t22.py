import sys; sys.path.insert(0,'.')
from u import *
code='''
A="/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix"
L=unreal.BlueprintEditorLibrary
for nm in ["EdGraphNode_Comment_20","EdGraphNode_Comment"]:
    c=unreal.find_object(None,A+":EventGraph."+nm)
    rows=[]
    for n in L.get_nodes_in_comment(c):
        p=L.get_node_pos(n); rows.append([str(n.get_name()),p.x,p.y,str(L.get_node_title(n)) if hasattr(L,"get_node_title") else ""])
    res[nm]={"texto":L.get_comment_text(c),"color":str(L.get_comment_color(c)),"nodos":rows}
'''
r=pyrun(code,'o22.out'); json.dump(r,open('init_comment_antes.json','w'),indent=1,ensure_ascii=False)
for k,v in r.items(): print(k,v['texto'],v['color'],len(v['nodos']),v['nodos'][:12])
