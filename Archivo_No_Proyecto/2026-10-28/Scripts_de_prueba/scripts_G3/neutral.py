import sys; sys.path.insert(0,".")
from g3u import *
code='''
A="/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix"
L=unreal.BlueprintEditorLibrary
out=[]
for g,names in (("EventGraph",["EdGraphNode_Comment","EdGraphNode_Comment_0","EdGraphNode_Comment_1","EdGraphNode_Comment_2","EdGraphNode_Comment_3","EdGraphNode_Comment_4"]),("UpdateProceduralVariables",["EdGraphNode_Comment_22","EdGraphNode_Comment_23","EdGraphNode_Comment_24"])):
    for nm in names:
        n=unreal.find_object(None,A+":"+g+"."+nm)
        if not n: continue
        L.set_comment_text(n,"[OBSOLETO] borrar con Supr")
        L.set_comment_color(n,unreal.LinearColor(0.25,0.25,0.25,0.5))
        n.set_editor_property("font_size",24)
        out.append([g,nm,L.get_comment_text(n)[:70],len(n.get_nodes_in_comment())])
res["out"]=out
'''
r=pyrun(code,'neu.out',wait=40)
print(r)
