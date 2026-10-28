import sys; sys.path.insert(0,'.')
from u import *
code='''
R="/Game/Characters/Student/Rig/"
add={"CR_Student_Procedural_fix":lambda t:0 if t=="ORFANO" else 120,"CR_Student_IK_fix":lambda t:0 if t=="CADERA" else 200}
for a,f in add.items():
    bp=unreal.load_asset(R+a+"."+a); ctrl=bp.get_controller_by_name("RigVMModel"); log=[]
    for n in ctrl.get_graph().get_nodes():
        if n.get_class().get_name()!="RigVMCommentNode": continue
        t=str(n.get_comment_text()); s=n.get_size(); d=f(t)
        if d:
            ctrl.set_node_size(n,unreal.Vector2D(s.x+d,s.y))
        s2=n.get_size(); log.append([t,[s.x,s.y],[s2.x,s2.y]])
    res[a]=log
'''
r=pyrun(code,'o18.out',wait=20); print(json.dumps(r))
