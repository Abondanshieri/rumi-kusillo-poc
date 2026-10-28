import sys; sys.path.insert(0,'.')
from u import *
code='''
a="CR_Student_Procedural_fix"
bp=unreal.load_asset("/Game/Characters/Student/Rig/"+a+"."+a); ctrl=bp.get_controller_by_name("RigVMModel")
for n in ctrl.get_graph().get_nodes():
    if n.get_class().get_name()=="RigVMCommentNode" and str(n.get_comment_text())=="ORFANO":
        res["antes"]=[n.get_size().x,n.get_size().y]
        res["ok"]=ctrl.set_node_size(n,unreal.Vector2D(700,363),True,False)
        res["despues"]=[n.get_size().x,n.get_size().y]
'''
print(pyrun(code,'o16.out'))
