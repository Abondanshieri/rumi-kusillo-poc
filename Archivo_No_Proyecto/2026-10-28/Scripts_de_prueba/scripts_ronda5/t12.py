import sys; sys.path.insert(0,'.')
from u import *
code='''
for a in ["Procedural_fix","IK_fix"]:
    p="/Game/Characters/Student/Rig/CR_Student_%s.CR_Student_%s"%(a,a)
    bp=unreal.load_asset(p); ctrl=bp.get_controller_by_name("RigVMModel")
    rows=[]
    for n in ctrl.get_graph().get_nodes():
        cl=n.get_class().get_name()
        if cl=="RigVMCommentNode":
            pp=n.get_position(); s=n.get_size()
            rows.append([str(n.get_name()),str(n.get_comment_text()),n.get_comment_font_size(),n.get_comment_bubble_visible(),[pp.x,pp.y],[s.x,s.y]])
    res[a]=rows
'''
r=pyrun(code)
print(json.dumps(r,indent=0)[:3000])
