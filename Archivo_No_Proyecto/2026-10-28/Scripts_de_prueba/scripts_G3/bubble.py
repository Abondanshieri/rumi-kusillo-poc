import sys; sys.path.insert(0,".")
from g3u import *
code='''
A="/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix"
cnt=0; errs=[]
for g,c in (("EventGraph",14),("UpdateProceduralVariables",20)):
    for i in range(c):
        n=unreal.find_object(None,A+":"+g+".EdGraphNode_Comment_G3_%d"%i)
        for pn in ("comment_bubble_visible_in_details_panel","b_comment_bubble_visible_in_details_panel"):
            try:
                n.set_editor_property(pn,False); cnt+=1; break
            except Exception as e: errs.append(str(e)[:100])
res["cnt"]=cnt; res["errs"]=errs[:3]
n=unreal.find_object(None,A+":EventGraph.EdGraphNode_Comment_G3_0")
try: res["val"]=str(n.get_editor_property("comment_bubble_visible_in_details_panel"))
except Exception as e: res["val"]=str(e)[:100]
'''
print(pyrun(code,'bub.out',wait=40))
