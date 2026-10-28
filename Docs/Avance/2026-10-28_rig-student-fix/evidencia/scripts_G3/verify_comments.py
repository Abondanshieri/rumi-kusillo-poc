import sys; sys.path.insert(0,".")
from g3u import *
EV='D:/Dev/Computacion_Grafica/Rumi 5.8/Docs/Avance/2026-10-28_rig-student-fix/evidencia/'
gn=sys.argv[1]
code='''
A="/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix"
L=unreal.BlueprintEditorLibrary
rows=[]
for k in [""]+[str(i) for i in range(0,120)]+["G3_"+str(i) for i in range(0,40)]:
    nm="EdGraphNode_Comment"+("_"+k if k else "")
    n=unreal.find_object(None,A+":%s."+nm)
    if not n: continue
    d={"name":nm,"texto":L.get_comment_text(n)}
    try:
        s=n.get_node_size(); d["w"]=s.x; d["h"]=s.y
    except Exception as e: d["w"]="ERR"
    try: d["nodos"]=[ (x.get_name()) for x in n.get_nodes_in_comment()]
    except Exception as e: d["nodos"]="ERR "+str(e)[:80]
    try: d["color"]=[n.get_comment_color().r,n.get_comment_color().g,n.get_comment_color().b,n.get_comment_color().a]
    except Exception as e: d["color"]="ERR"
    try: d["font"]=n.get_editor_property("font_size")
    except Exception as e: d["font"]="ERR"
    rows.append(d)
res["c"]=rows
'''%gn
r=pyrun(code,'vc_%s.out'%gn,wait=40)
json.dump(r,open(EV+'../evidencia/G3b_comentarios_verif_%s.json'%gn if False else SP+'vc_%s.json'%gn,'w'),indent=1,ensure_ascii=False)
if r is None: print('sin respuesta')
else:
    print(r.get('EXC'))
    for x in r.get('c',[]): print(x['name'],x['w'],x['h'],x.get('font'),len(x['nodos']) if isinstance(x['nodos'],list) else x['nodos'],x['texto'][:60])
