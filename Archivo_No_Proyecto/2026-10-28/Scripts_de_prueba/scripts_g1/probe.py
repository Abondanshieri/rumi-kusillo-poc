import sys; sys.path.insert(0,'.')
from g1u import *
CODE='''
bp=unreal.load_asset("/Game/Characters/Student/Rig/CR_Student_IK_fix.CR_Student_IK_fix")
ctrl=bp.get_controller_by_name("RigVMModel")
res["ctrl"]=[m for m in dir(ctrl) if any(k in m for k in ("comment","position","size","color","reroute","rename","begin","end","undo","notif"))]
g=ctrl.get_graph()
c=[n for n in g.get_nodes() if n.get_class().get_name()=="RigVMCommentNode"][0]
res["cn"]=[m for m in dir(c) if not m.startswith("_")]
res["bp_save"]=[m for m in dir(unreal.EditorAssetLibrary) if "save" in m or "dirty" in m]
'''
r=pyrun(CODE,'probe.out')
print(json.dumps(r,indent=0))
