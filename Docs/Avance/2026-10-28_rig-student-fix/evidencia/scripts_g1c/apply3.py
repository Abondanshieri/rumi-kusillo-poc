import sys; sys.path.insert(0,'.')
from g1u import *
which=sys.argv[1]; src=sys.argv[2]
asset='CR_Student_Procedural_fix' if which=='proc' else 'CR_Student_IK_fix'
d=json.load(open(src))
RENAME={'Add_HipsZ':'SINSALIDA_Add_HipsZ','Add_LeftFootZ':'SINSALIDA_Add_LeftFootZ','Add_RightFootZ':'SINSALIDA_Add_RightFootZ','Clamp_LeftOffset':'SINSALIDA_Clamp_LeftOffset','Clamp_RightOffset':'SINSALIDA_Clamp_RightOffset'} if which=='proc' else {}
CODE='''
pos=%s
com=%s
ren=%s
bp=unreal.load_asset("/Game/Characters/Student/Rig/%s.%s")
ctrl=bp.get_controller_by_name("RigVMModel"); g=ctrl.get_graph()
existing={}
for n in g.get_nodes():
    if n.get_class().get_name()=="RigVMCommentNode": existing[str(n.get_comment_text())]=str(n.get_name())
log=[]
for nm,(x,y) in pos.items():
    if g.find_node_by_name(nm) is None: nm=ren.get(nm,nm)
    ok=ctrl.set_node_position_by_name(nm,unreal.Vector2D(x,y),False)
    if not ok: log.append("FALLO pos "+nm)
used=set()
for c in com:
    t=c["title"]; col=unreal.LinearColor(*c["color"])
    if t in existing: nm=existing[t]
    else:
        n=ctrl.add_comment_node(t,unreal.Vector2D(*c["pos"]),unreal.Vector2D(*c["size"]),col,"",False)
        nm=str(n.get_name()); log.append("nuevo "+t+" "+nm)
    used.add(t)
    ctrl.set_node_position_by_name(nm,unreal.Vector2D(*c["pos"]),False)
    ctrl.set_node_size_by_name(nm,unreal.Vector2D(*c["size"]),False)
    ctrl.set_node_color_by_name(nm,col,False)
    ctrl.set_comment_text_by_name(nm,t,120,True,True,False)
log.append("comentarios sin usar: "+str([t for t in existing if t not in used]))
for a,b in ren.items():
    if g.find_node_by_name(a) is None: log.append('ya renombrado '+b); continue
    try: log.append("rename %%s -> %%s: %%s"%%(a,b,ctrl.rename_node(g.find_node_by_name(a),b,False)))
    except Exception as e: log.append("rename FALLO "+a+" "+str(e))
res["log"]=log
'''%(json.dumps({k:v for k,v in d['pos'].items()}),json.dumps([dict(b,title=b['title']) for b in d['boxes']]),json.dumps(RENAME),asset,asset)
r=pyrun(CODE,'apply3_%s.out'%which)
print(r)
