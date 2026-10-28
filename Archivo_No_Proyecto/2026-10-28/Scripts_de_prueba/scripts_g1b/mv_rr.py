import sys; sys.path.insert(0,'.')
from g1u import *
CODE='''
bp=unreal.load_asset("/Game/Characters/Student/Rig/CR_Student_Procedural_fix.CR_Student_Procedural_fix")
ctrl=bp.get_controller_by_name("RigVMModel")
res["a"]=ctrl.set_node_position_by_name("Reroute_PelvisOffset_1",unreal.Vector2D(1000,5900),False)
res["b"]=ctrl.set_node_position_by_name("Reroute_PelvisOffset_2",unreal.Vector2D(1150,6800),False)
'''
print(pyrun(CODE,'rr.out'))
