import sys; sys.path.insert(0,'.')
from u import *
code='''
A="/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix"
L=unreal.BlueprintEditorLibrary
names={"AnimGraph":["14","16"],"EventGraph":["","1","2","3","4","20"],"UpdateProceduralVariables":["22","23","24"]}
rows=[]
for g,ks in names.items():
    for k in ks:
        nm="EdGraphNode_Comment"+("_"+k if k else "")
        n=unreal.find_object(None,A+":"+g+"."+nm)
        if not n: continue
        sz=L.get_node_size(n)
        rows.append({"graph":g,"name":nm,"texto":L.get_comment_text(n),"tam":[sz.x,sz.y],"fuente":n.get_editor_property("font_size"),"nodos_dentro":len(L.get_nodes_in_comment(n))})
res["abp_comentarios"]=rows
'''
r=pyrun(code,'o26.out'); json.dump(r,open('abp_comentarios_editor.json','w'),indent=1,ensure_ascii=False)
for x in r['abp_comentarios']: print(x)
ab={'refPath':'/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix:AnimGraph.AnimGraphNode_ControlRig_1'}
print(T(OB,'get_properties',{'instance':ab,'properties':['node']}))
