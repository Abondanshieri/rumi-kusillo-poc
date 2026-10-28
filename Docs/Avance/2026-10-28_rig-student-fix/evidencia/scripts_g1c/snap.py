import sys; sys.path.insert(0,'.')
from g1u import *
CODE='''
def snap_rig(p):
    bp=unreal.load_asset(p); ctrl=bp.get_controller_by_name("RigVMModel"); g=ctrl.get_graph()
    nodes={}; links=[]; vals={}
    for n in g.get_nodes():
        nm=str(n.get_name()); cl=n.get_class().get_name()
        pp=n.get_position(); s=n.get_size()
        d={"cls":cl,"title":str(n.get_node_title()),"pos":[pp.x,pp.y],"size":[s.x,s.y]}
        if cl=="RigVMCommentNode":
            d["text"]=str(n.get_comment_text()); d["font"]=n.get_comment_font_size(); d["color"]=str(n.get_node_color())
        if cl=="RigVMVariableNode": d["var"]=str(n.get_variable_name())
        nodes[nm]=d
        try: pins=n.get_all_pins_recursively()
        except Exception: pins=n.get_pins()
        for pin in pins:
            path=str(pin.get_pin_path())
            for t in pin.get_linked_target_pins():
                links.append([path,str(t.get_pin_path())])
            if len(pin.get_sub_pins())==0:
                try: vals[path]=str(pin.get_default_value())
                except Exception: pass
    return {"nodes":nodes,"links":links,"vals":vals}
for k in ["CR_Student_Procedural_fix","CR_Student_IK_fix"]:
    res[k]=snap_rig("/Game/Characters/Student/Rig/%s.%s"%(k,k))
'''
r=pyrun(CODE,'snap.out')
out=sys.argv[1]
json.dump(r,open(out,'w'),indent=1)
for k,v in r.items():
    if k=='EXC': print(v); continue
    print(k,len(v['nodes']),'nodos',len(v['links']),'links',len(v['vals']),'vals')
