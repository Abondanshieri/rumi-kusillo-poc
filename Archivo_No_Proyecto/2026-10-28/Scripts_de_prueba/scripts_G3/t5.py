import sys; sys.path.insert(0,'.')
from g3u import *
r=pyrun('''
A="/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix"
g=unreal.find_object(None,A+":EventGraph")
res["g"]=str(g)
res["gp"]=[x for x in dir(g) if not x.startswith("_")]
res["cls"]=[x for x in dir(unreal) if "Comment" in x or x.startswith("EdGraph") or "NodeCreator" in x]
n=unreal.find_object(None,A+":EventGraph.EdGraphNode_Comment_0")
for p in ["nodes","node_pos_x","NodePosX","node_width","NodeWidth"]:
    try: res["p_"+p]=str(g.get_editor_property(p))[:200] if p=="nodes" else str(n.get_editor_property(p))
    except Exception as e: res["p_"+p]="ERR "+str(e)[:200]
''','t5.out',wait=25)
print(json.dumps(r,indent=0,ensure_ascii=False)[:5000])
