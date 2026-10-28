import sys; sys.path.insert(0,'.')
from u import *
from snaprig import SNAP_CODE
code=SNAP_CODE+'''
R="/Game/Characters/Student/Rig/"
for k,a in [("PR_fix","CR_Student_Procedural_fix"),("IK_fix","CR_Student_IK_fix"),("PR_orig","CR_Student_Procedural"),("IK_orig","CR_Student_IK")]:
    res[k]=snap_rig(R+a+"."+a)
# pines TwoBoneIK / BasicIK de las 4 rigs (lectura viva)
pins={}
for k,a in [("PR_fix","CR_Student_Procedural_fix"),("IK_fix","CR_Student_IK_fix"),("PR_orig","CR_Student_Procedural"),("IK_orig","CR_Student_IK")]:
    bp=unreal.load_asset(R+a+"."+a); ctrl=bp.get_controller_by_name("RigVMModel"); g=ctrl.get_graph()
    for n in g.get_nodes():
        if n.get_class().get_name()=="RigVMUnitNode" and ("IK" in str(n.get_node_title()) or "IK" in str(n.get_name())):
            d={}
            for p in n.get_pins():
                nm=str(p.get_name())
                if nm in ("PrimaryAxis","SecondaryAxis","SecondaryAxisWeight","PoleVector","Weight"):
                    d[nm]=str(p.get_default_value())
            pins[k+"/"+str(n.get_name())+" ["+str(n.get_node_title())+"]"]=d
res["pins"]=pins
'''
r=pyrun(code,'snap_fin.out',wait=40)
json.dump(r,open('snap_ronda6_final.json','w'),indent=1)
if 'EXC' in r: print(r['EXC'])
for k in ('PR_fix','IK_fix','PR_orig','IK_orig'):
    v=r[k]; print(k,len(v['nodes']),len(v['links']),v['npins'])
for k,v in r['pins'].items(): print(k,v)
