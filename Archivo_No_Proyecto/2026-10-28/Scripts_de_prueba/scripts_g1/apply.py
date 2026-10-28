import sys; sys.path.insert(0,'.')
from g1u import *
import layout
rig=sys.argv[1]
pos,com=layout.proc() if rig=='proc' else layout.ik()
asset='CR_Student_Procedural_fix' if rig=='proc' else 'CR_Student_IK_fix'
CODE='''
pos=%s
com=%s
bp=unreal.load_asset("/Game/Characters/Student/Rig/%s.%s")
ctrl=bp.get_controller_by_name("RigVMModel"); g=ctrl.get_graph()
existing={}
for n in g.get_nodes():
    if n.get_class().get_name()=="RigVMCommentNode": existing[str(n.get_comment_text())]=str(n.get_name())
log=[]
for nm,(x,y) in pos.items():
    ok=ctrl.set_node_position_by_name(nm,unreal.Vector2D(x,y),False)
    if not ok: log.append("FALLO pos "+nm)
for t,d in com.items():
    col=unreal.LinearColor(*d["color"])
    if t in existing: nm=existing[t]
    else:
        n=ctrl.add_comment_node(t,unreal.Vector2D(*d["pos"]),unreal.Vector2D(*d["size"]),col,"",False)
        nm=str(n.get_name()); log.append("nuevo "+t+" "+nm)
    ctrl.set_node_position_by_name(nm,unreal.Vector2D(*d["pos"]),False)
    ctrl.set_node_size_by_name(nm,unreal.Vector2D(*d["size"]),False)
    ctrl.set_node_color_by_name(nm,col,False)
    ctrl.set_comment_text_by_name(nm,t,120,True,True,False)
res["log"]=log
'''%(json.dumps({k:list(v) for k,v in pos.items()}),json.dumps({k:{kk:list(vv) for kk,vv in v.items()} for k,v in com.items()}),asset,asset)
r=pyrun(CODE,'apply_%s.out'%rig)
print(r)
