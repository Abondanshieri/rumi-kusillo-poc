import sys; sys.path.insert(0,'.')
from u import *
code='''
res["BEL"]=[d for d in dir(unreal.BlueprintEditorLibrary) if not d.startswith("_")]
res["libs"]=[d for d in dir(unreal) if ("Blueprint" in d or "Graph" in d or "Node" in d) and ("Library" in d or "Subsystem" in d or "Util" in d)]
n=unreal.find_object(None,"/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix:EventGraph.EdGraphNode_Comment_20")
res["obj"]=str(n)
'''
r=pyrun(code,'o21.out'); print(r['libs']); print([x for x in r['BEL'] if any(k in x for k in ('remove','delete','node','comment','graph'))]); print(r['obj'])
