A="/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix"
L=unreal.BlueprintEditorLibrary
n=unreal.find_object(None,A+":AnimGraph.EdGraphNode_Comment_14")
d={"attrs":[a for a in dir(n) if not a.startswith("_")]}
for p in ["node_pos_x","node_pos_y","node_width","node_height","font_size","comment_color","comment","move_mode","comment_bubble_visible","b_color_comment_bubble","node_comment"]:
    try: d[p]=str(n.get_editor_property(p))
    except Exception as e: d[p]="ERR "+str(e)[:60]
for f in ["get_comment_text","get_comment_color","get_nodes_in_comment"]:
    try: d[f]=str(getattr(L,f)(n))[:200]
    except Exception as e: d[f]="ERR "+str(e)[:100]
res=d
