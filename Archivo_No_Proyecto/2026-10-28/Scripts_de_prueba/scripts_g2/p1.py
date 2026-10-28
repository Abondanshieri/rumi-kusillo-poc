A="/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix"
L=unreal.BlueprintEditorLibrary
g=unreal.find_object(None,A+":AnimGraph")
rows=[]
for nm in ["AnimGraphNode_Root_0","AnimGraphNode_Slot_0","AnimGraphNode_StateMachine_0","AnimGraphNode_StateMachine_1","AnimGraphNode_SaveCachedPose_0","AnimGraphNode_Inertialization_0","AnimGraphNode_ControlRig_1","EdGraphNode_Comment_14","EdGraphNode_Comment_16","EdGraphNode_Comment"]:
    n=unreal.find_object(None,A+":AnimGraph."+nm)
    if not n: rows.append([nm,None]); continue
    try:
        sz=L.get_node_size(n)
        try: p=L.get_node_pos(n); pp=[p.x,p.y]
        except Exception as e: pp=str(e)[:80]
        rows.append([nm,pp,sz.x,sz.y])
    except Exception as e: rows.append([nm,'ERR',str(e)[:100]])
res["rows"]=rows
res["cm"]=[ (n.get_name()) for n in g.get_graph_nodes_of_class(unreal.EdGraphNode_Comment)] if hasattr(g,"get_graph_nodes_of_class") else None
