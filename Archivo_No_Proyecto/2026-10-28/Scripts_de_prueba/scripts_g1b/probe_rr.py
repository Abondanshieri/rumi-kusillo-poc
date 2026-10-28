import sys; sys.path.insert(0,'.')
from g1u import *
CODE='''
bp=unreal.load_asset("/Game/Characters/Student/Rig/CR_Student_Procedural_fix.CR_Student_Procedural_fix")
ctrl=bp.get_controller_by_name("RigVMModel")
res["m"]=[m for m in dir(ctrl) if "reroute" in m.lower()]
res["doc"]=ctrl.add_reroute_node_on_link.__doc__
res["doc2"]=ctrl.add_free_reroute_node.__doc__ if hasattr(ctrl,"add_free_reroute_node") else None
'''
print(json.dumps(pyrun(CODE,'rr.out'),indent=1))
