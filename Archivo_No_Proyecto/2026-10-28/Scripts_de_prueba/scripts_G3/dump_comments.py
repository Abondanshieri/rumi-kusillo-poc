import sys,json
sys.path.insert(0,'.')
from u import *
code='''
A="/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix"
L=unreal.BlueprintEditorLibrary
rows=[]
for g in ["EventGraph","UpdateProceduralVariables","TestFunc","AnimGraph"]:
    for k in [""]+[str(i) for i in range(0,60)]:
        nm="EdGraphNode_Comment"+("_"+k if k else "")
        n=unreal.find_object(None,A+":"+g+"."+nm)
        if not n: continue
        d={"graph":g,"name":nm}
        for key,fn in [("texto",lambda:L.get_comment_text(n)),("size",lambda:str(L.get_node_size(n))),("color",lambda:str(L.get_comment_color(n))),("nin",lambda:len(L.get_nodes_in_comment(n)))]:
            try: d[key]=fn()
            except Exception as e: d[key]="ERR "+str(e)[:80]
        for pr in ["font_size","node_pos_x","node_pos_y","node_width","node_height","comment_color","color_comment_bubble","comment_bubble_visible","comment_bubble_pinned","move_mode","comment_depth"]:
            try: d[pr]=str(n.get_editor_property(pr))
            except Exception as e: d[pr]="ERR"
        rows.append(d)
res["c"]=rows
'''
r=pyrun(code,'dc.out')
json.dump(r,open('comments_antes.json','w'),indent=1,ensure_ascii=False)
for x in r.get('c',[]): print(x)
print(r.get('EXC'))
