import sys; sys.path.insert(0,'.')
from g1u import *
CODE='''
bp=unreal.load_asset("/Game/Characters/Student/Rig/CR_Student_Procedural_fix.CR_Student_Procedural_fix")
ctrl=bp.get_controller_by_name("RigVMModel")
n1=ctrl.add_reroute_node_on_link_path("Get_PelvisOffset.Value -> Sub_FootOffsetR.B",unreal.Vector2D(600,5000),"Reroute_PelvisOffset_1",False,False)
res["n1"]=str(n1.get_name()) if n1 else None
n2=ctrl.add_reroute_node_on_link_path("Reroute_PelvisOffset_1.Value -> Sub_FootOffsetR.B",unreal.Vector2D(1250,6400),"Reroute_PelvisOffset_2",False,False)
res["n2"]=str(n2.get_name()) if n2 else None
'''
print(json.dumps(pyrun(CODE,'rr.out'),indent=1))
